import unittest
from datetime import datetime
from rules import classify
class RuleTests(unittest.TestCase):
    def setUp(self):
        self.now=datetime(2026,10,19,12)
        self.row=dict(status="in_transit",last_scan_at="2026-10-17T12:00:00",pickup_due_at="2026-10-16T12:00:00",promised_delivery_at="2026-10-20T12:00:00")
    def test_boundary(self): self.assertEqual(classify(self.row,self.now)["category"],"Stale tracking")
    def test_recent(self):
        self.row["last_scan_at"]="2026-10-19T11:00:00";self.assertIsNone(classify(self.row,self.now))
    def test_terminal(self):
        for status in ["delivered","returned"]:
            self.row["status"]=status;self.assertIsNone(classify(self.row,self.now))
    def test_failed(self):
        self.row["status"]="delivery_failed";self.assertEqual(classify(self.row,self.now)["priority"],"P1")
    def test_pickup(self):
        self.row["status"]="pickup_pending";self.assertEqual(classify(self.row,self.now)["category"],"Pickup overdue")
    def test_breach(self):
        self.row["promised_delivery_at"]="2026-10-18T12:00:00";self.assertEqual(classify(self.row,self.now)["priority"],"P1")
    def test_future(self):
        self.row["last_scan_at"]="2026-10-20T12:00:00";self.assertEqual(classify(self.row,self.now)["category"],"Invalid tracking data")
if __name__=="__main__": unittest.main()
