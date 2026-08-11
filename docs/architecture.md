# Architecture

## The file-backed control loop

```text
Source of truth ──→ Task card ──→ Role execution ──→ Delivery receipt
       ↑                                                   │
       └────────── human review and approval gate ─────────┘
```

### 1. Source of truth

The authoritative business record remains outside the agent conversation. A task references it; it does not copy or silently rewrite it.

### 2. Task card

A task card defines the object, objective, one primary role, inputs, acceptance criteria, allowed actions, and approval state.

### 3. Role execution

One specialist is accountable. Reviewers can challenge facts, test an artifact, or inspect compliance, but they do not create a second owner.

### 4. Delivery receipt

A delivery receipt reports an outcome, evidence paths, verification results, unresolved gaps, and the next human decision. “I finished” without evidence is not a delivery.

### 5. Approval gate

G0 starts work, G1 freezes a formal content baseline, and G2 permits an external or irreversible action. These gates are independent.

## Truth layers

| Layer | Purpose | May it overwrite the source of truth? |
|---|---|---|
| Authoritative record | approved facts and originals | n/a |
| AI work area | tasks, drafts, analyses, QA | no |
| Formal artifact | human-approved output | only through an explicit governed update |

## Design choices

- **Files before chat history:** state can be reviewed, versioned, and transferred.
- **Hierarchy before mesh:** the orchestrator routes; specialists do not form an uncontrolled group chat.
- **Evidence before status:** completion depends on checks, not confidence language.
- **Least privilege:** external actions are denied unless explicitly approved.
- **Small schemas:** task and delivery artifacts stay human-readable.
