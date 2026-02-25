---
name: task-processor
description: |
  Process tasks from the Needs_Action folder. Read tasks, create plans,
  execute actions, and track completion.
---

# Task Processor Skill

Process tasks autonomously following the AI Employee rules.

## Task Processing Workflow

### Step 1: Read Task
```bash
qwen --prompt "Read and analyze the task file: Needs_Action/EMAIL_abc123.md" --cwd /path/to/vault
```

### Step 2: Check Handbook
```bash
qwen --prompt "Check Company_Handbook.md for rules about processing emails" --cwd /path/to/vault
```

### Step 3: Create Plan (for multi-step tasks)
```markdown
---
created: 2026-02-25T10:30:00Z
status: in_progress
---

# Plan: Process Email Request

## Objective
Reply to client inquiry about pricing

## Steps
- [x] Read email content
- [x] Check Company_Handbook for response rules
- [ ] Draft reply
- [ ] Request approval if needed
- [ ] Send reply
- [ ] Archive email

## Notes
Client is a known contact - can auto-reply per handbook rules.
```

### Step 4: Execute Actions
Based on task type:

| Task Type | Action |
|-----------|--------|
| Email reply | Draft and send (or request approval) |
| File processing | Read, categorize, take action |
| Payment request | Create approval file |
| Meeting request | Check calendar, propose times |

### Step 5: Update Dashboard
```bash
qwen --prompt "Update Dashboard.md with: 'Processed email from client@example.com - sent pricing info'" --cwd /path/to/vault
```

### Step 6: Mark Complete
Move task file to /Done folder.

## Task Types

### Email Tasks
- Check if sender is known contact
- Apply response rules from handbook
- Draft reply or request approval

### File Drop Tasks
- Read file content
- Determine required action
- Process or escalate

### Approval Tasks
- Check approval thresholds
- Create approval request file
- Wait for human action

## Response Templates

### Email Reply Template
```markdown
Subject: Re: {original_subject}

Dear {name},

Thank you for your message. {response_body}

Best regards,
AI Employee

---
*This message was processed by AI Employee v0.1*
```

### Status Update Template
```markdown
## Task Status: {task_name}
- **Started**: {start_time}
- **Completed**: {end_time}
- **Result**: {success/failure}
- **Notes**: {any_relevant_details}
```
