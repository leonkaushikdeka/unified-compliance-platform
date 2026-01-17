SOC2_CONTROLS = {
    "CC1.1": {
        "name": "COSO Principle 1",
        "description": "The entity demonstrates a commitment to integrity and ethical values",
        "category": "Control Environment",
    },
    "CC1.2": {
        "name": "COSO Principle 2",
        "description": "The board of directors demonstrates independence from management",
        "category": "Control Environment",
    },
    "CC1.3": {
        "name": "COSO Principle 3",
        "description": "Management establishes, with board oversight, structures and authority",
        "category": "Control Environment",
    },
    "CC2.1": {
        "name": "COSO Principle 13",
        "description": "Entity obtains or generates and uses relevant, quality information",
        "category": "Information & Communication",
    },
    "CC2.2": {
        "name": "COSO Principle 14",
        "description": "Entity communicates internally to achieve objectives",
        "category": "Information & Communication",
    },
    "CC3.1": {
        "name": "COSO Principle 5",
        "description": "Entity selects and develops control activities",
        "category": "Risk Assessment",
    },
    "CC3.2": {
        "name": "COSO Principle 6",
        "description": "Entity selects and develops general control activities",
        "category": "Risk Assessment",
    },
    "CC4.1": {
        "name": "COSO Principle 7",
        "description": "Entity selects and develops control activities",
        "category": "Monitoring Activities",
    },
    "CC5.1": {
        "name": "COSO Principle 11",
        "description": "Entity considers potential for fraud",
        "category": "Risk Assessment",
    },
    "CC6.1": {
        "name": "Logical & Physical Access",
        "description": "Entity implements logical access controls",
        "category": "Logical Access",
    },
    "CC6.2": {
        "name": "User Authentication",
        "description": "Entity implements multi-factor authentication",
        "category": "Logical Access",
    },
    "CC7.1": {
        "name": "System Operations",
        "description": "Entity defines security operating parameters",
        "category": "System Operations",
    },
    "CC7.2": {
        "name": "Change Management",
        "description": "Entity manages changes to infrastructure and data",
        "category": "System Operations",
    },
    "CC8.1": {
        "name": "Business Continuity",
        "description": "Entity mitigates security incidents",
        "category": "Business Continuity",
    },
    "CC9.1": {
        "name": "Risk Mitigation",
        "description": "Entity identifies and selects risk mitigation strategies",
        "category": "Risk Mitigation",
    },
}


def get_soc2_controls():
    return SOC2_CONTROLS


def get_soc2_categories():
    return list(set(control["category"] for control in SOC2_CONTROLS.values()))


def assess_soc2_control(control_id: str, evidence: dict) -> dict:
    if control_id not in SOC2_CONTROLS:
        return {"error": "Unknown control"}

    control = SOC2_CONTROLS[control_id]
    score = 0
    max_score = 100

    if evidence.get("policy_exists"):
        score += 20
    if evidence.get("policy_reviewed"):
        score += 10
    if evidence.get("procedure_documented"):
        score += 20
    if evidence.get("training_completed"):
        score += 15
    if evidence.get("testing_performed"):
        score += 20
    if evidence.get("audit_passed"):
        score += 15

    status = "compliant" if score >= 70 else "partial" if score >= 40 else "non_compliant"

    return {
        "control_id": control_id,
        "control_name": control["name"],
        "category": control["category"],
        "description": control["description"],
        "score": score,
        "max_score": max_score,
        "status": status,
        "evidence": evidence,
    }
