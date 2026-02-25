#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrator - Main process manager for AI Employee.

This script:
1. Checks /Needs_Action folder for new items
2. Invokes Qwen Code to process items
3. Manages the Ralph Wiggum loop for multi-step tasks
4. Handles approval workflow

Usage:
    python orchestrator.py /path/to/vault
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List


class Orchestrator:
    """Main orchestrator for AI Employee operations."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.in_progress = self.vault_path / 'In_Progress'
        self.done = self.vault_path / 'Done'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Ensure directories exist
        for folder in [self.needs_action, self.in_progress, self.done, 
                       self.pending_approval, self.approved]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Agent identifier
        self.agent_name = os.getenv('AGENT_NAME', 'qwen-agent-1')
    
    def check_needs_action(self) -> List[Path]:
        """Check for items in Needs_Action folder."""
        if not self.needs_action.exists():
            return []
        
        items = list(self.needs_action.glob('*.md'))
        return items
    
    def claim_item(self, item_path: Path) -> Path:
        """
        Claim an item by moving it to In_Progress/<agent>.
        
        Returns the new path.
        """
        agent_folder = self.in_progress / self.agent_name
        agent_folder.mkdir(parents=True, exist_ok=True)
        
        new_path = agent_folder / item_path.name
        item_path.rename(new_path)
        return new_path
    
    def complete_item(self, item_path: Path):
        """Move completed item to Done folder."""
        # Remove from In_Progress/<agent>
        if item_path.parent.parent == self.in_progress:
            new_path = self.done / item_path.name
        else:
            new_path = self.done / item_path.name

        item_path.rename(new_path)
        print(f'[OK] Completed: {item_path.name}')
    
    def check_approvals(self) -> List[Path]:
        """Check for approved items ready for action."""
        if not self.approved.exists():
            return []
        
        return list(self.approved.glob('*.md'))
    
    def update_dashboard(self, action: str, details: str):
        """Update the dashboard with recent activity."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

        if not self.dashboard.exists():
            return

        content = self.dashboard.read_text(encoding='utf-8')

        # Find the Recent Activity section and add entry
        lines = content.split('\n')
        new_lines = []
        in_recent_activity = False
        skip_no_activity = False

        for i, line in enumerate(lines):
            # Skip the "*No recent activity*" placeholder
            if '*No recent activity*' in line:
                skip_no_activity = True
                continue
            
            new_lines.append(line)
            if line.strip() == '## Recent Activity':
                in_recent_activity = True
                # Add new entry after this header
                new_lines.append(f'- [{timestamp}] {action}: {details}')
            elif in_recent_activity and line.startswith('##'):
                in_recent_activity = False

        self.dashboard.write_text('\n'.join(new_lines), encoding='utf-8')
    
    def process_with_qwen(self, item_path: Path, prompt: str) -> str:
        """
        Process an item using Qwen Code.

        This invokes Qwen Code with the appropriate context and prompt.
        Returns the output from Qwen.
        """
        # Build the Qwen Code command
        # Using positional prompt format: qwen [query..]
        # And -y for YOLO mode (auto-approve) for Bronze tier
        # Use directory parameter for working directory
        cmd = 'qwen -y ' + prompt.replace('"', '\\"')

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                shell=True,  # Required on Windows for proper command resolution
                cwd=str(self.vault_path)  # Set working directory
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return 'ERROR: Qwen Code timed out after 5 minutes'
        except FileNotFoundError:
            return 'ERROR: Qwen Code not found. Please install and configure.'
        except Exception as e:
            return f'ERROR: {str(e)}'
    
    def run_approval_check(self):
        """Process approved items."""
        approved_items = self.check_approvals()
        
        for item in approved_items:
            content = item.read_text(encoding='utf-8')
            print(f'Processing approved item: {item.name}')
            
            # Parse the approval and execute the action
            # This is a placeholder - actual implementation depends on action types
            self.update_dashboard('Approval processed', item.name)
            item.rename(self.done / item.name)
    
    def run_cycle(self):
        """Run one processing cycle."""
        items = self.check_needs_action()
        
        if not items:
            print('No items to process')
            return
        
        for item in items:
            print(f'Processing: {item.name}')
            
            # Claim the item
            claimed_path = self.claim_item(item)
            
            # Read the item content
            content = claimed_path.read_text(encoding='utf-8')
            
            # Build prompt for Qwen
            prompt = f'''You are the AI Employee processing a task from the vault.

VAULT: {self.vault_path}
TASK FILE: {claimed_path.name}

TASK CONTENT:
{content}

---
YOUR TASK (execute autonomously, do not ask questions):
1. Read Company_Handbook.md for rules
2. Analyze the task above
3. Take appropriate action based on the task type
4. Update Dashboard.md with your progress in the Recent Activity section
5. Move this task file to /Done folder when complete

For Bronze Tier: Simply acknowledge the task, update Dashboard.md, and indicate completion.
Respond with what you did and confirm when the task is complete.'''
            
            # Process with Qwen Code
            print('Invoking Qwen Code...')
            result = self.process_with_qwen(claimed_path, prompt)
            print(f'Result: {result[:500]}...' if len(result) > 500 else f'Result: {result}')
            
            # For Bronze tier, we just log that Qwen was invoked
            # More advanced processing in higher tiers
            self.update_dashboard('Task processed', item.name)
            self.complete_item(claimed_path)
    
    def run(self, continuous: bool = False):
        """
        Run the orchestrator.
        
        Args:
            continuous: If True, run continuously checking for new items
        """
        print(f'AI Employee Orchestrator starting...')
        print(f'Vault: {self.vault_path}')
        print(f'Agent: {self.agent_name}')
        print('')
        
        if continuous:
            import time
            try:
                while True:
                    self.run_cycle()
                    self.run_approval_check()
                    time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                print('\nOrchestrator stopped by user')
        else:
            self.run_cycle()
            self.run_approval_check()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print('Usage: python orchestrator.py <vault_path> [--continuous]')
        print('')
        print('Arguments:')
        print('  vault_path    - Path to your Obsidian vault')
        print('  --continuous  - Optional: Run continuously (default: run once)')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    continuous = '--continuous' in sys.argv
    
    orchestrator = Orchestrator(vault_path)
    orchestrator.run(continuous)


if __name__ == '__main__':
    main()
