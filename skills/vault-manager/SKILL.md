---
name: vault-manager
description: |
  Manage the AI Employee Obsidian vault. Read, write, and organize files
  in the vault structure. Use for all vault operations.
---

# Vault Manager Skill

Manage files and folders in the AI Employee Obsidian vault.

## Quick Reference

### Read a File
```bash
# Read any file in the vault
qwen --prompt "Read the file: Dashboard.md" --cwd /path/to/vault
```

### Write a File
```bash
# Create or update a file
qwen --prompt "Create a new file in /Needs_Action with the following content: ..." --cwd /path/to/vault
```

### List Directory
```bash
# List files in a folder
qwen --prompt "List all .md files in the Needs_Action folder" --cwd /path/to/vault
```

## File Operations

### Create Action File
When a watcher detects a new item, create an action file:

```markdown
---
type: email
from: sender@example.com
subject: Meeting Request
received: 2026-02-25T10:30:00Z
priority: normal
status: pending
---

# Email: Meeting Request

## Content
[Email body here]

## Suggested Actions
- [ ] Reply to sender
- [ ] Schedule meeting
- [ ] Archive after processing
```

### Create Approval Request
For actions requiring human approval:

```markdown
---
type: approval_request
action: payment
amount: 500.00
recipient: Vendor Name
created: 2026-02-25T10:30:00Z
expires: 2026-02-26T10:30:00Z
status: pending
---

# Approval Required: Payment

## Details
- **Amount**: $500.00
- **To**: Vendor Name
- **Reason**: Invoice #123

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
```

### Update Dashboard
After processing, update the dashboard:

```markdown
## Recent Activity
- [2026-02-25 10:30] Processed: Email from sender@example.com
- [2026-02-25 10:25] Payment approved: $500 to Vendor Name
```

## Folder Structure

```
AI_Employee_Vault/
├── Inbox/              # Raw incoming items
├── Needs_Action/       # Items requiring processing
├── In_Progress/        # Currently being worked on
│   └── <agent>/        # Agent-specific work folder
├── Done/               # Completed items
├── Pending_Approval/   # Awaiting human approval
├── Approved/           # Approved, ready for action
├── Rejected/           # Rejected items
├── Plans/              # Multi-step task plans
├── Briefings/          # CEO briefing reports
├── Logs/               # Action logs
├── Accounting/         # Financial records
├── Invoices/           # Generated invoices
└── Updates/            # Status updates
```

## Best Practices

1. **Always use frontmatter** - YAML metadata at top of each file
2. **Include timestamps** - ISO format for all dates
3. **Track status** - Use status field: pending, in_progress, done
4. **Move files** - Don't delete, move to appropriate folder
5. **Log everything** - Update Dashboard.md after actions
