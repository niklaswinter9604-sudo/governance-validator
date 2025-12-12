# MeetingAgent Governance Validator v1.0

## Quick Start

conda activate validator
python app/app.py


Server läuft auf: http://localhost:8080

## Test

Health Check
curl http://localhost:8080/health

Validate Meeting
curl -X POST http://localhost:8080/validate
-H "Content-Type: application/json"
-d @tests/fixtures/clean_meeting.json


## Features
- ✅ PII Detection (Email, Phone, SSN)
- ✅ DSGVO Compliance Check
- ✅ Task Logic Validation
- ✅ Immutable Audit Trail
- ✅ Human-in-the-Loop Decision Making

## Architecture
- Flask API (Python)
- JSON-based validation
- Compliance-grade audit logging

## Status
Production-Ready POC
