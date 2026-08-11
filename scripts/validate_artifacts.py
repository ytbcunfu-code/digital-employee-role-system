#!/usr/bin/env python3
"""Validate digital-employee task cards and delivery receipts with stdlib only."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROLES = {f"C{i}" for i in range(7)}
OUTCOMES = {"passed", "conditional", "failed", "pending_evidence"}
GATES = {"G0", "G1", "G2"}
APPROVAL_STATES = {"pending", "approved", "rejected"}

TASK_FIELDS = {
    "task_id",
    "object_id",
    "objective",
    "primary_role",
    "source_of_truth",
    "inputs",
    "acceptance_criteria",
    "allowed_actions",
    "external_action",
    "approval",
}

DELIVERY_FIELDS = {
    "task_id",
    "outcome",
    "summary",
    "evidence",
    "verification",
    "open_gaps",
    "next_human_decision",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, str) and item.strip() for item in value
    )


def validate_task(task: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(TASK_FIELDS - task.keys())
    if missing:
        errors.append(f"task missing fields: {', '.join(missing)}")
        return errors

    for key in ("task_id", "object_id", "objective"):
        if not isinstance(task[key], str) or not task[key].strip():
            errors.append(f"task.{key} must be a non-empty string")

    if task["primary_role"] not in ROLES:
        errors.append("task.primary_role must be one of C0..C6")

    for key in ("source_of_truth", "inputs", "acceptance_criteria", "allowed_actions"):
        if not nonempty_list(task[key]):
            errors.append(f"task.{key} must be a non-empty string array")

    if not isinstance(task["external_action"], bool):
        errors.append("task.external_action must be boolean")

    approval = task["approval"]
    if not isinstance(approval, dict):
        errors.append("task.approval must be an object")
        return errors

    gate = approval.get("gate")
    status = approval.get("status")
    if gate not in GATES:
        errors.append("task.approval.gate must be G0, G1, or G2")
    if status not in APPROVAL_STATES:
        errors.append("task.approval.status must be pending, approved, or rejected")
    if task["external_action"] and not (gate == "G2" and status == "approved"):
        errors.append("external_action=true requires approved G2")
    if status == "approved":
        if not str(approval.get("approved_by", "")).strip():
            errors.append("approved task requires approval.approved_by")
        if not str(approval.get("approved_at", "")).strip():
            errors.append("approved task requires approval.approved_at")
    return errors


def validate_delivery(delivery: dict[str, Any], task: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(DELIVERY_FIELDS - delivery.keys())
    if missing:
        errors.append(f"delivery missing fields: {', '.join(missing)}")
        return errors

    if delivery["task_id"] != task.get("task_id"):
        errors.append("delivery.task_id must match task.task_id")
    if delivery["outcome"] not in OUTCOMES:
        errors.append(f"delivery.outcome must be one of {sorted(OUTCOMES)}")
    if not isinstance(delivery["summary"], str) or not delivery["summary"].strip():
        errors.append("delivery.summary must be a non-empty string")
    for key in ("evidence", "verification"):
        if not nonempty_list(delivery[key]):
            errors.append(f"delivery.{key} must be a non-empty string array")
    if not isinstance(delivery["open_gaps"], list):
        errors.append("delivery.open_gaps must be an array")
    if not isinstance(delivery["next_human_decision"], str) or not delivery[
        "next_human_decision"
    ].strip():
        errors.append("delivery.next_human_decision must be a non-empty string")
    return errors


def default_paths(root: Path) -> tuple[Path, Path]:
    base = root / "examples" / "manufacturing-demo"
    return base / "task.json", base / "delivery.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=Path)
    parser.add_argument("--delivery", type=Path)
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    default_task, default_delivery = default_paths(root)
    task_path = args.task or default_task
    delivery_path = args.delivery or default_delivery

    try:
        task = load_json(task_path)
        delivery = load_json(delivery_path)
        errors = validate_task(task) + validate_delivery(delivery, task)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {task_path} + {delivery_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
