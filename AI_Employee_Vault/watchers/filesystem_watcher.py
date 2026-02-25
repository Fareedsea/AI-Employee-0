#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File System Watcher - Monitors a drop folder for new files.

This is the simplest watcher to set up - just drop files into the
monitored folder and they'll be processed automatically.

Usage:
    python filesystem_watcher.py /path/to/vault /path/to/drop_folder
"""

import sys
import time
import hashlib
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from base_watcher import BaseWatcher


class DropFolderHandler(FileSystemEventHandler):
    """Handle file creation events in the drop folder."""
    
    def __init__(self, needs_action_folder: Path):
        super().__init__()
        self.needs_action = needs_action_folder
        self.processed_hashes = set()
    
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        source = Path(event.src_path)
        
        # Skip hidden files and temp files
        if source.name.startswith('.') or source.suffix.endswith('.tmp'):
            return
        
        # Generate unique ID from file content
        file_hash = self._hash_file(source)
        if file_hash in self.processed_hashes:
            return
        
        self.processed_hashes.add(file_hash)
        
        # Create action file
        self.create_action_file(source, file_hash)
    
    def _hash_file(self, path: Path) -> str:
        """Generate a hash for the file content."""
        hasher = hashlib.md5()
        try:
            with open(path, 'rb') as f:
                buf = f.read(65536)  # Read first 64KB
                hasher.update(buf)
            return hasher.hexdigest()
        except Exception as e:
            print(f"Error hashing file: {e}")
            return str(datetime.now().timestamp())
    
    def create_action_file(self, source: Path, file_hash: str):
        """Create a markdown action file for the dropped file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        action_filename = f'FILE_DROP_{timestamp}_{source.name}.md'
        action_path = self.needs_action / action_filename
        
        try:
            file_size = source.stat().st_size
        except Exception:
            file_size = 0
        
        content = f'''---
type: file_drop
original_name: {source.name}
source_path: {source.absolute()}
size: {file_size}
hash: {file_hash}
received: {datetime.now().isoformat()}
status: pending
---

# File Drop for Processing

A new file has been dropped for processing.

## File Details
- **Original Name**: {source.name}
- **Size**: {self._format_size(file_size)}
- **Received**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Suggested Actions
- [ ] Review file content
- [ ] Determine required action
- [ ] Process and move to /Done

## Notes
Add your processing notes here...
'''
        
        try:
            action_path.write_text(content, encoding='utf-8')
            print(f'✓ Created action file: {action_filename}')
        except Exception as e:
            print(f'✗ Error creating action file: {e}')
    
    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f'{size:.1f} {unit}'
            size /= 1024
        return f'{size:.1f} TB'


class FileSystemWatcher(BaseWatcher):
    """Watcher that monitors a folder for new files."""
    
    def __init__(self, vault_path: str, drop_folder: str = None):
        super().__init__(vault_path, check_interval=60)
        
        # Use provided drop folder or create default
        if drop_folder:
            self.drop_folder = Path(drop_folder)
        else:
            self.drop_folder = self.vault_path / 'Inbox'
        
        self.drop_folder.mkdir(parents=True, exist_ok=True)
    
    def check_for_updates(self) -> list:
        """
        This method is not used with watchdog (event-driven),
        but required by base class.
        """
        return []
    
    def create_action_file(self, item) -> Path:
        """
        This method is not used with watchdog (event-driven),
        but required by base class.
        """
        pass
    
    def run(self):
        """Start the file system observer."""
        self.logger.info(f'Monitoring drop folder: {self.drop_folder}')
        
        event_handler = DropFolderHandler(self.needs_action)
        observer = Observer()
        observer.schedule(event_handler, str(self.drop_folder), recursive=False)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            self.logger.info('File system watcher stopped')
        observer.join()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print('Usage: python filesystem_watcher.py <vault_path> [drop_folder]')
        print('')
        print('Arguments:')
        print('  vault_path   - Path to your Obsidian vault')
        print('  drop_folder  - Optional: Folder to monitor (default: <vault>/Inbox)')
        print('')
        print('Example:')
        print('  python filesystem_watcher.py "C:/Users/You/ObsidianVault"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    drop_folder = sys.argv[2] if len(sys.argv) > 2 else None
    
    watcher = FileSystemWatcher(vault_path, drop_folder)
    watcher.run()


if __name__ == '__main__':
    main()
