---
name: qwen-ralph-loop
description: |
  Implement the Ralph Wiggum persistence pattern for Qwen Code.
  Keep Qwen working on multi-step tasks until completion.
---

# Ralph Wiggum Loop for Qwen Code

Keep Qwen Code working autonomously until tasks are complete.

## How It Works

1. Orchestrator creates a state file with the task prompt
2. Qwen Code works on the task
3. Qwen indicates completion (or tries to exit)
4. Loop checker: Is task file in /Done?
5. YES → Task complete
6. NO → Re-inject prompt and continue

## Basic Loop Pattern

```bash
#!/bin/bash
# ralph-loop.sh - Ralph Wiggum loop for Qwen Code

TASK_FILE="$1"
PROMPT="$2"
MAX_ITERATIONS=${3:-10}

VAULT_PATH="/path/to/vault"
DONE_FOLDER="$VAULT_PATH/Done"
iteration=0

echo "Starting Ralph Wiggum Loop for: $TASK_FILE"
echo "Max iterations: $MAX_ITERATIONS"

while [ $iteration -lt $MAX_ITERATIONS ]; do
    iteration=$((iteration + 1))
    echo ""
    echo "=== Iteration $iteration ==="
    
    # Run Qwen Code
    qwen --prompt "$PROMPT" --cwd "$VAULT_PATH"
    
    # Check if task is complete (file moved to Done)
    if [ -f "$DONE_FOLDER/$TASK_FILE" ]; then
        echo "✓ Task completed!"
        exit 0
    fi
    
    # Check for completion marker in output
    if echo "$OUTPUT" | grep -q "TASK_COMPLETE"; then
        echo "✓ Task marked as complete"
        exit 0
    fi
    
    echo "Task not complete, continuing..."
done

echo "✗ Max iterations reached"
exit 1
```

## Usage

```bash
# Process a single task with Ralph loop
bash ralph-loop.sh "EMAIL_abc123.md" "Process this email and reply to sender" 10

# Or invoke directly
./ralph-loop.sh "FILE_DROP_invoice.pdf" "Review invoice and create payment approval" 5
```

## Completion Strategies

### 1. File Movement (Recommended)
Task is complete when file is moved to /Done:

```python
# In your processing code:
def complete_task(task_file):
    shutil.move(
        f'In_Progress/{task_file}',
        f'Done/{task_file}'
    )
    print('TASK_COMPLETE')
```

### 2. Output Marker
Task is complete when Qwen outputs specific marker:

```markdown
## Task Status
- All actions completed
- Dashboard updated
- Files moved to appropriate folders

TASK_COMPLETE
```

### 3. State File
Check for a completion state file:

```bash
# Check for completion state
if [ -f "$VAULT_PATH/Completed/$TASK_FILE.done" ]; then
    echo "Task completed"
    exit 0
fi
```

## Integration with Orchestrator

```python
# In orchestrator.py
def process_with_ralph_loop(self, item_path: Path, prompt: str, max_iterations: int = 10):
    """Process item with Ralph Wiggum loop."""
    
    for iteration in range(max_iterations):
        print(f'Iteration {iteration + 1}/{max_iterations}')
        
        # Run Qwen Code
        result = self.process_with_qwen(item_path, prompt)
        
        # Check if complete
        if self.is_complete(item_path):
            print('Task complete!')
            return result
        
        # Check for completion marker
        if 'TASK_COMPLETE' in result:
            print('Completion marker found!')
            return result
    
    print('Max iterations reached')
    return result

def is_complete(self, item_path: Path) -> bool:
    """Check if task is complete."""
    # Task is complete if file is in Done folder
    done_path = self.done / item_path.name
    return done_path.exists()
```

## Best Practices

1. **Set reasonable max iterations** - 5-10 for most tasks
2. **Clear completion criteria** - Define what "done" looks like
3. **Log each iteration** - Track progress and debug issues
4. **Graceful degradation** - Handle partial completion
5. **Timeout protection** - Don't loop forever

## Example: Email Processing Loop

```bash
#!/bin/bash
# Process email with Ralph loop

VAULT="/path/to/vault"
TASK_FILE="EMAIL_abc123.md"

PROMPT="
Read the email in Needs_Action/$TASK_FILE
1. Identify sender and subject
2. Check Company_Handbook for response rules
3. Draft appropriate reply
4. If approval needed, create file in Pending_Approval
5. If no approval needed, send reply
6. Move email to Done when complete
7. Update Dashboard.md

Output TASK_COMPLETE when all steps are done.
"

bash ralph-loop.sh "$TASK_FILE" "$PROMPT" 10
```
