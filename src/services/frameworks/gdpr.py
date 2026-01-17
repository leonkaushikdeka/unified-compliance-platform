GDPR_CONTROLS = {
    "ART5.1.A": {
        "name": "Lawfulness, fairness, transparency",
        "description": "Personal data processed lawfully, fairly and transparently",
        "article": "Article 5(1)(a)",
    },
    "ART5.1.B": {
        "name": "Purpose limitation",
        "description": "Personal data collected for specified, explicit and legitimate purposes",
        "article": "Article 5(1)(b)",
    },
    "ART5.1.C": {
        "name": "Data minimization",
        "description": "Personal data adequate, relevant and limited to what is necessary",
        "article": "Article 5(1)(c)",
    },
    "ART5.1.D": {
        "name": "Accuracy",
        "description": "Personal data accurate and kept up to date",
        "article": "Article 5(1)(d)",
    },
    "ART5.1.E": {
        "name": "Storage limitation",
        "description": "Personal data kept for no longer than necessary",
        "article": "Article 5(1)(e)",
    },
    "ART5.1.F": {
        "name": "Integrity and confidentiality",
        "description": "Personal data processed securely including protection against unauthorized processing",
        "article": "Article 5(1)(f)",
    },
    "ART6": {
        "name": "Lawful basis for processing",
        "description": "At least one lawful basis for processing is documented",
        "article": "Article 6",
    },
    "ART7": {
        "name": "Conditions for consent",
        "description": "Consent conditions are clearly defined and obtained",
        "article": "Article 7",
    },
    "ART8": {
        "name": "Children's consent",
        "description": "Special protection for children's data",
        "article": "Article 8",
    },
    "ART13": {
        "name": "Information to be provided",
        "description": "Privacy notice provides required information",
        "article": "Article 13",
    },
    "ART15": {
        "name": "Right of access",
        "description": "Data subjects can access their personal data",
        "article": "Article 15",
    },
    "ART16": {
        "name": "Right to rectification",
        "description": "Data subjects can correct inaccurate data",
        "article": "Article 16",
    },
    "ART17": {
        "name": "Right to erasure",
        "description": "Data subjects can request deletion of their data",
        "article": "Article 17",
    },
    "ART18": {
        "name": "Right to restriction",
        "description": "Data subjects can restrict processing",
        "article": "Article 18",
    },
    "ART20": {
        "name": "Right to data portability",
        "description": "Data subjects can receive their data in machine-readable format",
        "article": "Article 20",
    },
    "ART24": {
        "name": "Data protection by design",
        "description": "Data protection principles built into systems",
        "article": "Article 25",
    },
    "ART28": {
        "name": "Data processing agreement",
        "description": "DPA in place with all processors",
        "article": "Article 28",
    },
    "ART30": {
        "name": "Records of processing",
        "description": "Maintain records of processing activities",
        "article": "Article 30",
    },
    "ART32": {
        "name": "Security of processing",
        "description": "Appropriate technical and organizational measures",
        "article": "Article 32",
    },
    "ART33": {
        "name": "Data breach notification",
        "description": "Breaches reported within 72 hours",
        "article": "Article 33",
    },
}


def get_gdpr_controls():
    return GDPR_CONTROLS


def get_gdpr_articles():
    return list(set(control["article"] for control in GDPR_CONTROLS.values()))


def assess_gdpr_control(control_id: str, evidence: dict) -> dict:
    if control_id not in GDPR_CONTROLS:
        return {"error": "Unknown control"}

    control = GDPR_CONTROLS[control_id]
    score = 0
    max_score = 100

    if evidence.get("policy_documented"):
        score += 25
    if evidence.get("process_implemented"):
        score += 25
    if evidence.get("evidence_collected"):
        score += 25
    if evidence.get("training_completed"):
        score += 15
    if evidence.get("audit_trail"):
        score += 10

    status = "compliant" if score >= 75 else "partial" if score >= 40 else "non_compliant"

    return {
        "control_id": control_id,
        "control_name": control["name"],
        "article": control["article"],
        "description": control["description"],
        "score": score,
        "max_score": max_score,
        "status": status,
        "evidence": evidence,
    }
