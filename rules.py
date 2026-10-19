from datetime import datetime
TERMINAL={"delivered","returned"}
def classify(row, now):
    if row["status"] in TERMINAL: return None
    scan=datetime.fromisoformat(row["last_scan_at"])
    if scan>now: return {"category":"Invalid tracking data","priority":"P1","action":"Review timestamp before contacting customer"}
    if row["status"]=="delivery_failed": category="Failed delivery"; action="Review attempt reason and confirm recipient availability"; priority="P1"
    elif row["status"]=="pickup_pending" and datetime.fromisoformat(row["pickup_due_at"])<now: category="Pickup overdue"; action="Verify pickup status and prepare carrier follow-up"; priority="P2"
    elif row["status"]=="in_transit" and (now-scan).total_seconds()>=48*3600: category="Stale tracking"; action="Review last scan and prepare investigation request"; priority="P2"
    else: return None
    if datetime.fromisoformat(row["promised_delivery_at"])<now: priority="P1"
    return {"category":category,"priority":priority,"action":action}
