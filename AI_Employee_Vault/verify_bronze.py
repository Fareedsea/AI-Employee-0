#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Bronze Tier Completion

Check that all Bronze tier deliverables are in place:
1. Obsidian vault with Dashboard.md and Company_Handbook.md
2. Folder structure: /Inbox, /Needs_Action, /Done, etc.
3. One working Watcher script
4. Qwen Code integration
5. Agent Skills implemented
"""

import sys
from pathlib import Path
from datetime import datetime


class BronzeTierVerifier:
    """Verify Bronze tier completion."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path).resolve()  # Use absolute path
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def check(self, name: str, condition: bool, warning: bool = False):
        """Check a condition and print result."""
        if condition:
            symbol = "[OK]" if not warning else "[WARN]"
            print(f"{symbol} {name}")
            if warning:
                self.warnings += 1
            else:
                self.passed += 1
        else:
            print(f"[FAIL] {name}")
            self.failed += 1
    
    def verify(self):
        """Run all verification checks."""
        print("=" * 60)
        print("BRONZE TIER VERIFICATION")
        print(f"Vault: {self.vault_path}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print("")
        
        # 1. Core Files
        print("1. Core Files")
        print("-" * 40)
        self.check(
            "Dashboard.md exists",
            (self.vault_path / 'Dashboard.md').exists()
        )
        self.check(
            "Company_Handbook.md exists",
            (self.vault_path / 'Company_Handbook.md').exists()
        )
        self.check(
            "Business_Goals.md exists",
            (self.vault_path / 'Business_Goals.md').exists()
        )
        
        # Verify Dashboard has required sections
        dashboard_content = (self.vault_path / 'Dashboard.md').read_text() if (self.vault_path / 'Dashboard.md').exists() else ""
        self.check(
            "Dashboard has Recent Activity section",
            'Recent Activity' in dashboard_content
        )
        
        # Verify Company Handbook has rules
        handbook_content = (self.vault_path / 'Company_Handbook.md').read_text() if (self.vault_path / 'Company_Handbook.md').exists() else ""
        self.check(
            "Company_Handbook has Rules of Engagement",
            'Rules of Engagement' in handbook_content or 'Core Principles' in handbook_content
        )
        print("")
        
        # 2. Folder Structure
        print("2. Folder Structure")
        print("-" * 40)
        required_folders = [
            'Inbox',
            'Needs_Action',
            'In_Progress',
            'Done',
            'Pending_Approval',
            'Approved',
            'Rejected',
            'Plans',
            'Briefings',
            'Logs',
            'Accounting',
            'Invoices'
        ]
        
        for folder in required_folders:
            self.check(
                f"/{folder} folder exists",
                (self.vault_path / folder).exists()
            )
        print("")
        
        # 3. Watcher Scripts
        print("3. Watcher Scripts")
        print("-" * 40)
        watchers_folder = self.vault_path / 'watchers'
        self.check(
            "watchers/ folder exists",
            watchers_folder.exists()
        )
        self.check(
            "base_watcher.py exists",
            (watchers_folder / 'base_watcher.py').exists()
        )
        self.check(
            "filesystem_watcher.py exists",
            (watchers_folder / 'filesystem_watcher.py').exists()
        )
        self.check(
            "requirements.txt exists",
            (watchers_folder / 'requirements.txt').exists()
        )
        
        # Check if watchdog is installed
        try:
            import watchdog
            self.check(
                "watchdog package installed",
                True
            )
        except ImportError:
            self.check(
                "watchdog package installed",
                False,
                warning=True
            )
        print("")
        
        # 4. Orchestrator
        print("4. Orchestrator")
        print("-" * 40)
        self.check(
            "orchestrator.py exists",
            (self.vault_path / 'orchestrator.py').exists()
        )
        
        # Check orchestrator has Qwen integration
        orchestrator_content = (self.vault_path / 'orchestrator.py').read_text() if (self.vault_path / 'orchestrator.py').exists() else ""
        self.check(
            "Orchestrator has Qwen Code integration",
            'qwen' in orchestrator_content.lower()
        )
        print("")
        
        # 5. Agent Skills
        print("5. Agent Skills")
        print("-" * 40)
        # Skills are in parent directory (project root)
        skills_folder = self.vault_path.parent / 'skills'
        self.check(
            "skills/ folder exists",
            skills_folder.exists()
        )
        
        required_skills = [
            'vault-manager',
            'task-processor',
            'watcher-manager',
            'qwen-ralph-loop'
        ]
        
        for skill in required_skills:
            skill_path = skills_folder / skill
            self.check(
                f"{skill} skill exists",
                skill_path.exists() and (skill_path / 'SKILL.md').exists()
            )
        print("")
        
        # 6. README
        print("6. Documentation")
        print("-" * 40)
        self.check(
            "README.md exists",
            (self.vault_path / 'README.md').exists()
        )
        
        readme_content = (self.vault_path / 'README.md').read_text() if (self.vault_path / 'README.md').exists() else ""
        self.check(
            "README has Quick Start section",
            'Quick Start' in readme_content
        )
        self.check(
            "README lists Bronze Tier deliverables",
            'Bronze Tier' in readme_content
        )
        print("")
        
        # Summary
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Passed:   {self.passed}")
        print(f"Warnings: {self.warnings}")
        print(f"Failed:   {self.failed}")
        print("")
        
        if self.failed == 0:
            if self.warnings == 0:
                print("[SUCCESS] BRONZE TIER COMPLETE!")
                print("")
                print("Next steps:")
                print("1. Install watchdog: pip install -r watchers/requirements.txt")
                print("2. Start watcher: python watchers/filesystem_watcher.py .")
                print("3. Drop a file in Inbox/ to test")
                print("4. Run orchestrator: python orchestrator.py .")
                return 0
            else:
                print("[SUCCESS] BRONZE TIER COMPLETE (with warnings)")
                print("")
                print("Please address the warnings above.")
                return 0
        else:
            print("[FAIL] BRONZE TIER INCOMPLETE")
            print("")
            print("Please fix the failed checks above.")
            return 1


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        # Default to current directory
        vault_path = Path.cwd()
    else:
        vault_path = Path(sys.argv[1])
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    verifier = BronzeTierVerifier(vault_path)
    sys.exit(verifier.verify())


if __name__ == '__main__':
    main()
