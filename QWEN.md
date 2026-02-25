# AI Employee Project - Context Guide

## Project Overview

This is a **Personal AI Employee** hackathon project focused on building autonomous "Digital FTEs" (Full-Time Equivalent employees). The project creates a local-first, agent-driven automation system where AI agents powered by **Qwen Code** and **Obsidian** proactively manage personal and business affairs 24/7.

**Note:** This project uses **Qwen Code** instead of Claude Code as the reasoning engine.

### Core Architecture

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Brain** | Qwen Code | Reasoning engine for decision-making |
| **Memory/GUI** | Obsidian (Markdown) | Dashboard and long-term knowledge base |
| **Senses** | Python Watcher Scripts | Monitor Gmail, WhatsApp, filesystems |
| **Hands** | MCP Servers | External actions (email, browser automation, payments) |

### Key Concepts

- **Watcher Pattern**: Lightweight Python scripts run continuously, monitoring inputs and creating actionable `.md` files in `/Needs_Action` folders
- **Ralph Wiggum Loop**: A persistence pattern that keeps Qwen iterating until multi-step tasks are complete
- **Human-in-the-Loop (HITL)**: Sensitive actions require approval via file movement (`/Pending_Approval` → `/Approved`)
- **Monday Morning CEO Briefing**: Autonomous weekly audit generating revenue reports and bottleneck analysis

## Directory Structure

```
AI-Employee-0/
├── AI_Employee_Vault/          # Obsidian vault (Bronze Tier - COMPLETE)
│   ├── Inbox/                  # Drop files here for processing
│   ├── Needs_Action/           # Items awaiting processing
│   ├── In_Progress/            # Currently being worked on
│   ├── Done/                   # Completed items
│   ├── Pending_Approval/       # Awaiting human approval
│   ├── Approved/               # Approved actions ready to execute
│   ├── Rejected/               # Rejected items
│   ├── Plans/                  # Multi-step task plans
│   ├── Briefings/              # CEO briefing reports
│   ├── Logs/                   # Action logs
│   ├── Accounting/             # Financial records
│   ├── Invoices/               # Generated invoices
│   ├── Dashboard.md            # Real-time status
│   ├── Company_Handbook.md     # Rules of engagement
│   ├── Business_Goals.md       # Q1 2026 objectives
│   ├── README.md               # Vault documentation
│   ├── orchestrator.py         # Main process manager
│   ├── verify_bronze.py        # Bronze tier verification
│   ├── Sample_Test_File.md     # Test file for verification
│   └── watchers/
│       ├── base_watcher.py     # Abstract base class
│       ├── filesystem_watcher.py # File system monitor
│       └── requirements.txt    # Python dependencies
├── skills/                     # Qwen Code Agent Skills
│   ├── vault-manager/          # Vault file operations
│   ├── task-processor/         # Task processing logic
│   ├── watcher-manager/        # Watcher process management
│   └── qwen-ralph-loop/        # Ralph Wiggum persistence
├── .agents/
│   └── skills/
│       └── browsing-with-playwright/  # Browser automation skill
├── .qwen/
│   └── skills/
│       └── browsing-with-playwright/  # Qwen skill integration
├── skills-lock.json            # Skill versioning
├── QWEN.md                     # This file
└── Personal AI Employee Hackathon 0_...md  # Full hackathon blueprint
```

## Building and Running

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Qwen Code | Active subscription | Primary reasoning engine |
| Obsidian | v1.10.6+ | Knowledge base & dashboard |
| Python | 3.13+ | Watcher scripts & orchestration |
| Node.js | v24+ LTS | MCP servers |
| GitHub Desktop | Latest | Version control |

### Quick Start (Bronze Tier)

```bash
# 1. Navigate to vault
cd AI_Employee_Vault

# 2. Install dependencies
pip install -r watchers/requirements.txt

# 3. Start the file system watcher
python watchers/filesystem_watcher.py .

# 4. Run the orchestrator (process pending items)
python orchestrator.py .

# 5. Or run orchestrator continuously
python orchestrator.py . --continuous
```

### Using Qwen Code

```bash
# Process a specific task
qwen --prompt "Check Needs_Action folder and process any pending items" --cwd AI_Employee_Vault

# With Ralph Wiggum loop for multi-step tasks
qwen --prompt "Process EMAIL_abc123.md completely - read, plan, act, and move to Done" --cwd AI_Employee_Vault
```

### Playwright MCP Server (for browser automation)

```bash
# Start the browser automation server
bash .agents/skills/browsing-with-playwright/scripts/start-server.sh

# Verify server is running
python .agents/skills/browsing-with-playwright/scripts/verify.py

# Stop the server
bash .agents/skills/browsing-with-playwright/scripts/stop-server.sh
```

### MCP Client Usage

```bash
# List available tools
python scripts/mcp-client.py list -u http://localhost:8808

# Navigate to a URL
python scripts/mcp-client.py call -u http://localhost:8808 \
  -t browser_navigate -p '{"url": "https://example.com"}'

# Take a page snapshot
python scripts/mcp-client.py call -u http://localhost:8808 \
  -t browser_snapshot -p '{}'
```

## Development Conventions

### Skill Structure

All skills follow this structure:
- `SKILL.md`: Main documentation with usage examples
- `scripts/`: Executable scripts for server lifecycle and utilities
- `references/`: Auto-generated MCP tool documentation

### File Naming

- Watcher scripts: `<domain>_watcher.py` (e.g., `gmail_watcher.py`)
- Action files: `<TYPE>_<identifier>.md` (e.g., `EMAIL_abc123.md`)
- Approval requests: `APPROVAL_REQUIRED_<description>.md`

### Folder Conventions

| Folder | Purpose |
|--------|---------|
| `/Inbox` | Raw incoming items (drop zone) |
| `/Needs_Action` | Items requiring processing |
| `/In_Progress/<agent>` | Claimed tasks (prevents double-work) |
| `/Pending_Approval` | Awaiting human approval |
| `/Approved` | Approved actions ready for execution |
| `/Done` | Completed tasks |
| `/Briefings` | CEO briefing reports |

## Agent Skills

### vault-manager
Manage files and folders in the AI Employee Obsidian vault. Read, write, and organize files.

### task-processor
Process tasks from the Needs_Action folder. Read tasks, create plans, execute actions, and track completion.

### watcher-manager
Manage watcher scripts that monitor for new items. Start, stop, and monitor watcher processes.

### qwen-ralph-loop
Implement the Ralph Wiggum persistence pattern. Keep Qwen Code working until tasks are complete.

## Key Files Reference

| File | Description |
|------|-------------|
| `Personal AI Employee Hackathon 0_...md` | Complete hackathon blueprint with tiered deliverables |
| `AI_Employee_Vault/Dashboard.md` | Real-time status and recent activity |
| `AI_Employee_Vault/Company_Handbook.md` | Rules of engagement and approval thresholds |
| `AI_Employee_Vault/Business_Goals.md` | Q1 2026 objectives and metrics |
| `AI_Employee_Vault/orchestrator.py` | Main process manager for Qwen Code integration |
| `AI_Employee_Vault/verify_bronze.py` | Bronze tier verification script |
| `skills/*/SKILL.md` | Agent skill documentation |

## Hackathon Tiers

### Bronze Tier (COMPLETE ✓)

**Estimated time:** 8-12 hours

**Deliverables:**
- [x] Obsidian vault with Dashboard.md and Company_Handbook.md
- [x] One working Watcher script (File System Watcher)
- [x] Qwen Code successfully reading from and writing to the vault
- [x] Basic folder structure: /Inbox, /Needs_Action, /Done
- [x] All AI functionality implemented as Agent Skills

**Verification:** Run `python verify_bronze.py .` in AI_Employee_Vault

### Silver Tier (Next Steps)

**Estimated time:** 20-30 hours

**Deliverables:**
- [ ] All Bronze requirements plus:
- [ ] Two or more Watcher scripts (Gmail + WhatsApp)
- [ ] LinkedIn auto-posting for business
- [ ] Claude/Qwen reasoning loop that creates Plan.md files
- [ ] One working MCP server for external action
- [ ] Human-in-the-loop approval workflow
- [ ] Basic scheduling via cron or Task Scheduler

### Gold Tier (Future)

**Estimated time:** 40+ hours

**Deliverables:**
- [ ] All Silver requirements plus:
- [ ] Full cross-domain integration (Personal + Business)
- [ ] Odoo accounting integration via MCP
- [ ] Facebook/Instagram/Twitter integration
- [ ] Weekly Business and Accounting Audit
- [ ] Ralph Wiggum loop for autonomous multi-step completion

## Wednesday Research Meetings

- **When:** Wednesdays at 10:00 PM
- **Where:** [Zoom](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1) | [YouTube](https://www.youtube.com/@panaversity)
- **Purpose:** Teaching and showcasing AI Employee builds

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
```

### Files not being processed
1. Check that files are in `/Needs_Action` folder
2. Verify file extension is `.md`
3. Check orchestrator logs for errors

### Verification fails
```bash
# Run verification with full output
cd AI_Employee_Vault
python verify_bronze.py .
```

---
*AI Employee v0.1 - Powered by Qwen Code*
*Bronze Tier Complete - 2026-02-25*
