ISO27001_CONTROLS = {
    "A.5": {
        "name": "Information Security Policies",
        "description": "Management direction for information security",
        "domain": "Organizational Controls",
    },
    "A.6": {
        "name": "Information Security Roles",
        "description": "Segregation of duties for security",
        "domain": "Organizational Controls",
    },
    "A.7": {
        "name": "Security Awareness Training",
        "description": "Security awareness and competence of personnel",
        "domain": "Organizational Controls",
    },
    "A.8": {
        "name": "Asset Management",
        "description": "Identify and document organizational assets",
        "domain": "People Controls",
    },
    "A.9": {
        "name": "Access Control",
        "description": "Prevent unauthorized access to systems and information",
        "domain": "Technological Controls",
    },
    "A.10": {
        "name": "Cryptography",
        "description": "Ensure proper use of cryptography",
        "domain": "Technological Controls",
    },
    "A.11": {
        "name": "Physical Security",
        "description": "Prevent unauthorized physical access to information",
        "domain": "Physical Controls",
    },
    "A.12": {
        "name": "Operations Security",
        "description": "Ensure correct and secure operations",
        "domain": "Technological Controls",
    },
    "A.13": {
        "name": "Network Security",
        "description": "Ensure protection of information in networks",
        "domain": "Technological Controls",
    },
    "A.14": {
        "name": "System Acquisition",
        "description": "Security requirements for information systems",
        "domain": "Technological Controls",
    },
    "A.15": {
        "name": "Supplier Relationships",
        "description": "Protect information accessible by suppliers",
        "domain": "Organizational Controls",
    },
    "A.16": {
        "name": "Incident Management",
        "description": "Consistent approach to security incident management",
        "domain": "Organizational Controls",
    },
    "A.17": {
        "name": "Business Continuity",
        "description": "Information security continuity in adverse situations",
        "domain": "Organizational Controls",
    },
    "A.18": {
        "name": "Compliance",
        "description": "Avoid breaches of legal and contractual obligations",
        "domain": "Compliance Controls",
    },
}


def get_iso27001_controls():
    return ISO27001_CONTROLS


def get_iso27001_domains():
    return list(set(control["domain"] for control in ISO27001_CONTROLS.values()))


def assess_iso27001_control(control_id: str, evidence: dict) -> dict:
    if control_id not in ISO27001_CONTROLS:
        return {"error": "Unknown control"}

    control = ISO27001_CONTROLS[control_id]
    score = 0
    max_score = 100

    if evidence.get("policy_implemented"):
        score += 20
    if evidence.get("procedure_documented"):
        score += 20
    if evidence.get("evidence_collected"):
        score += 20
    if evidence.get("training_completed"):
        score += 15
    if evidence.get("audit_completed"):
        score += 15
    if evidence.get("continuous_improvement"):
        score += 10

    status = "compliant" if score >= 75 else "partial" if score >= 40 else "non_compliant"

    return {
        "control_id": control_id,
        "control_name": control["name"],
        "domain": control["domain"],
        "description": control["description"],
        "score": score,
        "max_score": max_score,
        "status": status,
        "evidence": evidence,
    }
