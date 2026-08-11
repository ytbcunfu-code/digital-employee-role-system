# Quick start

## 1. Choose the work object

Use a stable object identifier, for example `DEMO-001`. Link the authoritative source instead of pasting confidential data into the task.

## 2. Create a task

Copy `templates/task-card.json` and set one primary role. Keep `external_action` false unless the human has approved G2.

## 3. Execute and verify

The role produces an artifact and records the checks used to verify it. Optional reviewers can independently inspect the result.

## 4. Create a delivery receipt

Copy `templates/delivery-receipt.json`. Use one of four outcomes: `passed`, `conditional`, `failed`, or `pending_evidence`.

## 5. Validate

```bash
python3 scripts/validate_artifacts.py --task path/to/task.json --delivery path/to/delivery.json
```

The command exits non-zero when required fields are missing, role ownership is invalid, task IDs do not match, evidence is absent, or an external action is requested without G2 approval.

## 6. Human decision

The human either approves the next gate, requests a correction, or leaves the item pending evidence. The validator never grants an approval by itself.
