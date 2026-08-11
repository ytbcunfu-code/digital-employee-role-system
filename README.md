# Digital Employee Role System

An open, file-first operating model for teams that use AI agents to do real work without losing accountability, evidence, or human approval.

The project provides seven reusable role specifications, machine-checkable task and delivery artifacts, approval gates, and a validator that prevents an AI draft from being mistaken for an approved or externally delivered result.

## Why this exists

Most multi-agent demos optimize for more agents talking to each other. Real organizations need something different:

- one accountable owner for every task;
- an explicit source of truth;
- evidence-backed delivery instead of self-reported completion;
- a human decision point before publication, submission, deployment, payment, or signing;
- durable files that survive the current chat session.

## Core model

```text
Human request
    ↓
Orchestrator identifies object, scope and approval gate
    ↓
One primary specialist executes; reviewers are optional
    ↓
Delivery receipt links evidence and verification
    ↓
Human approves or rejects the external action
```

The seven reference roles are:

| ID | Role | Accountable outcome |
|---|---|---|
| C0 | Orchestrator | routing, conflict handling and internal acceptance |
| C1 | Commercial | opportunity, commercial terms and payment follow-through |
| C2 | Media | brand, content production and publication readiness |
| C3 | Solution | discovery, solution design and demonstrable prototypes |
| C4 | Application | policy/program applications and evidence consistency |
| C5 | Delivery | implementation, milestones, acceptance and delivery risk |
| C6 | Engineering | product code, testing, security, release and operations |

## Three approval gates

- **G0 — Start:** approve a new object or major workstream.
- **G1 — Content:** approve a version as the formal internal baseline.
- **G2 — External action:** approve sending, publishing, uploading, submitting, deploying, purchasing, signing, or deleting.

An internal review, generated file, successful API write, or UI toast is not G1 or G2.

## Quick start

```bash
python3 scripts/validate_artifacts.py
python3 -m unittest discover -s tests -v
```

Then copy the examples:

```bash
cp examples/manufacturing-demo/task.json my-task.json
cp examples/manufacturing-demo/delivery.json my-delivery.json
python3 scripts/validate_artifacts.py --task my-task.json --delivery my-delivery.json
```

See [docs/quickstart.md](docs/quickstart.md) and [docs/architecture.md](docs/architecture.md).

## Safety and privacy

This repository contains no customer records, credentials, production data, private company paths, or internal approval links. Example names and data are fictional. See [SECURITY.md](SECURITY.md).

## Maintainer

Created and maintained by Guo Shuai at 贵州万兔万兔科技有限公司. Contributions and implementation reports are welcome.

## License

[MIT](LICENSE)
