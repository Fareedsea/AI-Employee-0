---
name: watcher-manager
description: |
  Manage watcher scripts that monitor for new items. Start, stop, and
  monitor watcher processes for Gmail, WhatsApp, and file system.
---

# Watcher Manager Skill

Manage the watcher processes that monitor for new items.

## Available Watchers

| Watcher | Purpose | Check Interval |
|---------|---------|----------------|
| File System | Monitor drop folder | Event-driven |
| Gmail | Check new emails | 2 minutes |
| WhatsApp | Monitor messages | 30 seconds |

## Starting Watchers

### File System Watcher (Bronze Tier)
```bash
# Start the file system watcher
python watchers/filesystem_watcher.py /path/to/vault

# Or with custom drop folder
python watchers/filesystem_watcher.py /path/to/vault /path/to/drop_folder
```

### Gmail Watcher (Silver Tier)
Requires Gmail API setup:
```bash
python watchers/gmail_watcher.py /path/to/vault
```

### WhatsApp Watcher (Silver Tier)
Requires Playwright MCP:
```bash
python watchers/whatsapp_watcher.py /path/to/vault
```

## Running in Background

### Windows (PowerShell)
```powershell
# Start watcher in background
Start-Process python -ArgumentList "watchers/filesystem_watcher.py", "/path/to/vault" -WindowStyle Hidden
```

### Using PM2 (Recommended for production)
```bash
# Install PM2
npm install -g pm2

# Start watcher
pm2 start watchers/filesystem_watcher.py --interpreter python -- /path/to/vault

# Save process list
pm2 save

# Setup startup
pm2 startup
```

## Monitoring Watchers

### Check if Running
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep watcher
```

### View Logs
```bash
# PM2 logs
pm2 logs

# Or check watcher output directly
tail -f /path/to/vault/watchers/watcher.log
```

## Watcher Output Format

When a watcher detects a new item, it creates a file like:

```markdown
---
type: file_drop
original_name: invoice.pdf
source_path: C:/Users/You/Drop/invoice.pdf
size: 24576
received: 2026-02-25T10:30:00Z
status: pending
---

# File Drop for Processing

## File Details
- **Original Name**: invoice.pdf
- **Size**: 24.0 KB
- **Received**: 2026-02-25 10:30:00

## Suggested Actions
- [ ] Review file content
- [ ] Determine required action
- [ ] Process and move to /Done
```

## Stopping Watchers

### Manual Stop
```bash
# Press Ctrl+C in the terminal running the watcher
```

### PM2 Stop
```bash
# Stop specific watcher
pm2 stop filesystem_watcher

# Stop all
pm2 stop all
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Watcher not detecting files | Check folder permissions, verify path |
| Too many action files | Increase check_interval |
| Watcher crashed | Check logs, restart with PM2 auto-restart |
| Duplicate processing | Verify processed_ids tracking |
