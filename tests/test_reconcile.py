import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from taxvault.reconcile import (
    DEFAULT_FIXTURES_AVAILABLE,
    FIXTURES_DIR,
    build_report,
    load_documents,
    reconcile,
)


class TestReconcileFixtures(unittest.TestCase):
    def setUp(self):
        self.documents = load_documents(FIXTURES_DIR)
        self.result = reconcile(self.documents)

    def test_income_reconciles(self):
        # W-2 wages 72000 + 1099-NEC 12000 = 84000 = 1040 line 9.
        self.assertEqual(self.result.income_total, 84000.0)
        self.assertEqual(self.result.return_total_income, 84000.0)
        self.assertTrue(self.result.income_reconciles)
        self.assertEqual(self.result.income_difference, 0.0)

    def test_withholding_reconciles(self):
        self.assertTrue(self.result.withholding_reconciles)

    def test_missing_form_gap(self):
        # 1040 expects a 1099-INT that is not in the catalog.
        self.assertIn("synthetic_1099int", self.result.missing_forms)
        self.assertFalse(self.result.is_ready)

    def test_injection_detected_not_acted_on(self):
        ids = {f.doc_id for f in self.result.injection_findings}
        self.assertIn("syn-1099nec-0001", ids)

    def test_report_validates_and_renders(self):
        report = build_report(self.result)
        report.validate()
        out = report.render()
        self.assertIn("Tax-Year Readiness Report", out)
        self.assertIn("NOT READY", out)
        self.assertIn("Readiness Gaps", out)
        self.assertIn("1099-INT", out)


class TestReconcileSynthetic(unittest.TestCase):
    def test_ready_when_complete(self):
        docs = [
            {"doc_id": "w", "kind": "synthetic_w2",
             "fields": {"wages": {"value": 50000.0}, "federal_withholding": {"value": 5000.0}}},
            {"doc_id": "r", "kind": "synthetic_1040", "tax_year": 2025,
             "fields": {"total_income": {"value": 50000.0},
                        "federal_withholding": {"value": 5000.0}},
             "expected_forms": ["synthetic_w2"]},
        ]
        result = reconcile(docs)
        self.assertTrue(result.income_reconciles)
        self.assertTrue(result.withholding_reconciles)
        self.assertEqual(result.missing_forms, [])
        self.assertTrue(result.is_ready)

    def test_mismatch_flagged(self):
        docs = [
            {"doc_id": "w", "kind": "synthetic_w2",
             "fields": {"wages": {"value": 50000.0}}},
            {"doc_id": "r", "kind": "synthetic_1040", "tax_year": 2025,
             "fields": {"total_income": {"value": 60000.0}},
             "expected_forms": ["synthetic_w2"]},
        ]
        result = reconcile(docs)
        self.assertFalse(result.income_reconciles)
        self.assertEqual(result.income_difference, -10000.0)


class TestFixturesPresent(unittest.TestCase):
    def test_fixtures_available(self):
        self.assertTrue(DEFAULT_FIXTURES_AVAILABLE)


if __name__ == "__main__":
    unittest.main()
