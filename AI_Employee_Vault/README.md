# AI Employee Vault

Your Personal AI Employee's knowledge base and working directory.

## Quick Start

### 1. Install Watcher Dependencies

```bash
cd watchers
pip install -r requirements.txt
```

### 2. Start the File System Watcher

```bash
# From the vault root
python watchers/filesystem_watcher.py .
```

Or with a custom drop folder:
```bash
python watchers/filesystem_watcher.py . /path/to/your/drop/folder
```

### 3. Run the Orchestrator

```bash
# Process all pending items once
python orchestrator.py .

# Or run continuously
python orchestrator.py . --continuous
```

### 4. Use Qwen Code

```bash
# Process a specific task
qwen --prompt "Check Needs_Action folder and process any pending items" --cwd .

# With Ralph Wiggum loop for multi-step tasks
qwen --prompt "Process EMAIL_abc123.md completely - read, plan, act, and move to Done" --cwd .
```

## Folder Structure

```
AI_Employee_Vault/
├── Inbox/              # Drop files here for processing
├── Needs_Action/       # Items awaiting processing
├── In_Progress/        # Currently being worked on
├── Done/               # Completed items
├── Pending_Approval/   # Awaiting your approval
├── Approved/           # Approved actions ready to execute
├── Plans/              # Multi-step task plans
├── Briefings/          # CEO briefing reports
├── Logs/               # Action logs
└── watchers/           # Watcher scripts
```

## Key Files

- **Dashboard.md** - Real-time status and recent activity
- **Company_Handbook.md** - Rules of engagement
- **Business_Goals.md** - Q1 2026 objectives and metrics

## Bronze Tier Deliverables

✅ Obsidian vault with Dashboard.md and Company_Handbook.md
✅ Folder structure: /Inbox, /Needs_Action, /Done, etc.
✅ File System Watcher (monitors drop folder)
✅ Qwen Code integration for task processing
✅ Agent Skills implemented (vault-manager, task-processor, watcher-manager, qwen-ralph-loop)

## Next Steps (Silver Tier)

- Add Gmail Watcher
- Add WhatsApp Watcher
- Implement MCP servers for external actions
- Add scheduling via cron/Task Scheduler

## Troubleshooting

### Watcher not starting
```bash
# Check Python version (need 3.13+)
python --version

# Install dependencies
pip install -r watchers/requirements.txt
```

### Qwen Code not found
```bash
# Verify Qwen Code installation
qwen --version

# Or check PATH
where qwen  # Windows
which qwen  # Mac/Linux
```

### Files not being processed
1. Check that files are in `/Needs_Action` folder
2. Verify file extension is `.md`
3. Check orchestrator logs for errors

---
*AI Employee v0.1 - Powered by Qwen Code*
