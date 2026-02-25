---
type: sample
from: test@example.com
subject: Test File - Delete After Verification
received: 2026-02-25T00:00:00Z
priority: low
status: pending
---

# Sample Test File

This is a sample file to test the AI Employee system.

## Purpose
Use this file to verify that:
1. File System Watcher detects new files
2. Orchestrator processes items in Needs_Action
3. Qwen Code can read and respond to tasks
4. Files are moved to Done after processing

## Test Instructions

1. **Move this file** to the `Inbox/` folder
2. **Start the watcher**: `python watchers/filesystem_watcher.py .`
3. **Watch for action file** created in `Needs_Action/`
4. **Run orchestrator**: `python orchestrator.py .`
5. **Verify file** is moved to `Done/`

## Expected Flow

```
Inbox/
  ↓ (Watcher detects)
Needs_Action/
  ↓ (Orchestrator claims)
In_Progress/qwen-agent-1/
  ↓ (Qwen processes)
Done/
```

## Success Criteria

- [ ] Watcher creates action file in Needs_Action
- [ ] Orchestrator claims the file
- [ ] Qwen Code processes the task
- [ ] File ends up in Done folder
- [ ] Dashboard.md is updated

---
*This is a test file - safe to delete after verification*
