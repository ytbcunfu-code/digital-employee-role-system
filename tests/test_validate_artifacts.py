import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validator", ROOT / "scripts" / "validate_artifacts.py"
)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(validator)


def valid_task():
    return {
        "task_id": "TASK-1",
        "object_id": "OBJECT-1",
        "objective": "Produce one verifiable artifact",
        "primary_role": "C3",
        "source_of_truth": ["source.md"],
        "inputs": ["input.md"],
        "acceptance_criteria": ["test passes"],
        "allowed_actions": ["read", "draft", "test"],
        "external_action": False,
        "approval": {
            "gate": "G1",
            "status": "pending",
            "approved_by": "",
            "approved_at": "",
        },
    }


def valid_delivery():
    return {
        "task_id": "TASK-1",
        "outcome": "conditional",
        "summary": "Artifact exists; one evidence gap remains.",
        "evidence": ["artifact.md"],
        "verification": ["test passes"],
        "open_gaps": ["human approval"],
        "next_human_decision": "Approve or reject G1",
    }


class ValidatorTests(unittest.TestCase):
    def test_valid_pair(self):
        task = valid_task()
        self.assertEqual([], validator.validate_task(task))
        self.assertEqual([], validator.validate_delivery(valid_delivery(), task))

    def test_c7_finance_role_is_valid_for_internal_task(self):
        task = valid_task()
        task["primary_role"] = "C7"
        self.assertEqual([], validator.validate_task(task))

    def test_c7_payment_task_requires_explicit_approved_g2(self):
        task = valid_task()
        task["primary_role"] = "C7"
        task["objective"] = "Prepare and execute an approved supplier payment"
        task["external_action"] = True
        self.assertIn(
            "external_action=true requires approved G2",
            validator.validate_task(task),
        )

        task["approval"].update(
            {
                "gate": "G2",
                "status": "approved",
                "approved_by": "human approver",
                "approved_at": "2026-10-29T09:00:00+08:00",
            }
        )
        self.assertEqual([], validator.validate_task(task))

    def test_external_action_requires_g2(self):
        task = valid_task()
        task["external_action"] = True
        self.assertIn("external_action=true requires approved G2", validator.validate_task(task))

    def test_approved_g2_requires_identity_and_time(self):
        task = valid_task()
        task["external_action"] = True
        task["approval"]["gate"] = "G2"
        task["approval"]["status"] = "approved"
        errors = validator.validate_task(task)
        self.assertIn("approved task requires approval.approved_by", errors)
        self.assertIn("approved task requires approval.approved_at", errors)

    def test_delivery_task_id_must_match(self):
        task = valid_task()
        delivery = valid_delivery()
        delivery["task_id"] = "TASK-OTHER"
        self.assertIn(
            "delivery.task_id must match task.task_id",
            validator.validate_delivery(delivery, task),
        )


if __name__ == "__main__":
    unittest.main()
