HIPAA_CONTROLS = {
    "164.308.A.1": {
        "name": "Security Management Process",
        "description": "Implement policies and procedures to prevent, detect, and correct security violations",
        "safeguard": "Administrative",
    },
    "164.308.A.2": {
        "name": "Workforce Security",
        "description": "Implement policies to ensure appropriate access to ePHI",
        "safeguard": "Administrative",
    },
    "164.308.A.3": {
        "name": "Security Awareness Training",
        "description": "Implement a security awareness and training program",
        "safeguard": "Administrative",
    },
    "164.308.A.4": {
        "name": "Security Management",
        "description": "Implement procedures to address security incidents",
        "safeguard": "Administrative",
    },
    "164.308.A.5": {
        "name": "Contingency Plan",
        "description": "Establish and implement procedures for responding to emergencies",
        "safeguard": "Administrative",
    },
    "164.308.A.6": {
        "name": "Evaluation",
        "description": "Periodic technical and nontechnical evaluations",
        "safeguard": "Administrative",
    },
    "164.308.A.7": {
        "name": "Business Associate Contracts",
        "description": "Ensure business associates comply with security rules",
        "safeguard": "Administrative",
    },
    "164.310.A.1": {
        "name": "Facility Access Controls",
        "description": "Limit physical access to electronic information systems",
        "safeguard": "Physical",
    },
    "164.310.B": {
        "name": "Workstation Use",
        "description": "Policies for workstation use and physical security of workstations",
        "safeguard": "Physical",
    },
    "164.310.C": {
        "name": "Workstation Security",
        "description": "Physical safeguards for workstations",
        "safeguard": "Physical",
    },
    "164.310.D.1": {
        "name": "Device and Media Controls",
        "description": "Policies for disposition of hardware and electronic media",
        "safeguard": "Physical",
    },
    "164.312.A.1": {
        "name": "Access Control",
        "description": "Implement technical policies for access to ePHI",
        "safeguard": "Technical",
    },
    "164.312.A.2": {
        "name": "Audit Controls",
        "description": "Implement hardware, software, and procedural mechanisms",
        "safeguard": "Technical",
    },
    "164.312.B": {
        "name": "Integrity Controls",
        "description": "Protect ePHI from improper alteration or destruction",
        "safeguard": "Technical",
    },
    "164.312.C.1": {
        "name": "Transmission Security",
        "description": "Protect ePHI transmitted electronically",
        "safeguard": "Technical",
    },
    "164.314.A": {
        "name": "Organizational Requirements",
        "description": "Requirements for group health plans",
        "safeguard": "Administrative",
    },
    "164.314.B.1": {
        "name": "Requirements for Covered Entities",
        "description": "Satisfy organizational requirements",
        "safeguard": "Administrative",
    },
    "164.316": {
        "name": "Documentation Requirements",
        "description": "Maintain written security policies and procedures",
        "safeguard": "Documentation",
    },
}


def get_hipaa_controls():
    return HIPAA_CONTROLS


def get_hipaa_safeguards():
    return list(set(control["safeguard"] for control in HIPAA_CONTROLS.values()))


def assess_hipaa_control(control_id: str, evidence: dict) -> dict:
    if control_id not in HIPAA_CONTROLS:
        return {"error": "Unknown control"}

    control = HIPAA_CONTROLS[control_id]
    score = 0
    max_score = 100

    if evidence.get("policy_documented"):
        score += 20
    if evidence.get("procedure_implemented"):
        score += 25
    if evidence.get("training_completed"):
        score += 15
    if evidence.get("audit_trail"):
        score += 15
    if evidence.get("testing_performed"):
        score += 15
    if evidence.get("incident_response"):
        score += 10

    status = "compliant" if score >= 75 else "partial" if score >= 40 else "non_compliant"

    return {
        "control_id": control_id,
        "control_name": control["name"],
        "safeguard": control["safeguard"],
        "description": control["description"],
        "score": score,
        "max_score": max_score,
        "status": status,
        "evidence": evidence,
    }
