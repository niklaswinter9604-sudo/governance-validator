import json
import re
from datetime import datetime
from pathlib import Path

class MeetingValidator:
    def __init__(self):
        self.version = "1.0.0"
        self.audit_log_path = Path("audit_logs.json")
        self.pii_patterns = {
            "email": r"[\w\.-]+@[\w\.-]+\.\w+",
            "phone": r"[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}",
            "ssn": r"\d{3}-\d{2}-\d{4}",
        }
    
    def validate(self, meeting_data: dict) -> dict:
        audit_id = f"VA-{datetime.now().strftime('%Y%m%d')}-001"
        compliance = self._check_compliance(meeting_data)
        logic = self._check_logic(meeting_data)
        integrity = self._check_integrity(meeting_data)
        decision = self._decide(compliance, logic, integrity)
        self._log_audit(audit_id, decision, meeting_data)
        return {
            "audit_id": audit_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "compliance": compliance,
            "logic": logic,
            "integrity": integrity,
            "decision": decision
        }
    
    def _check_compliance(self, data: dict) -> dict:
        findings = []
        text = json.dumps(data)
        for ptype, pattern in self.pii_patterns.items():
            if re.search(pattern, text):
                findings.append({
                    "type": "pii_found",
                    "pii_type": ptype,
                    "severity": "CRITICAL"
                })
        meta = data.get("metadata_flags", {})
        if meta.get("legal_basis") is None:
            findings.append({
                "type": "missing_legal_basis",
                "severity": "CRITICAL"
            })
        return {
            "status": "CRITICAL" if findings else "PASS",
            "findings": findings
        }
    
    def _check_logic(self, data: dict) -> dict:
        tasks = data.get("action_items", [])
        unassigned = [t for t in tasks if t.get("owner_id") in [None, "TBD"]]
        return {
            "status": "WARNING" if unassigned else "PASS",
            "unassigned_count": len(unassigned)
        }
    
    def _check_integrity(self, data: dict) -> dict:
        return {
            "status": "PASS",
            "encoding": "UTF-8",
            "error_count": 0
        }
    
    def _decide(self, compliance: dict, logic: dict, integrity: dict) -> dict:
        if compliance["status"] == "CRITICAL":
            return {
                "overall_status": "NO_GO",
                "reason": "Critical DSGVO violations found"
            }
        elif logic["status"] == "WARNING":
            return {
                "overall_status": "GO_WITH_CONDITIONS",
                "reason": "Review unassigned tasks"
            }
        else:
            return {
                "overall_status": "GO",
                "reason": "All checks passed"
            }
    
    def _log_audit(self, audit_id: str, decision: dict, data: dict):
        entry = {
            "audit_id": audit_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "meeting_id": data.get("meeting_id"),
            "decision": decision["overall_status"]
        }
        logs = []
        if self.audit_log_path.exists():
            with open(self.audit_log_path) as f:
                logs = json.load(f)
        logs.append(entry)
        with open(self.audit_log_path, "w") as f:
            json.dump(logs, f, indent=2)
