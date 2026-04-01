"""
Agent 5 — Impact & Risk Scoring
Rôle : Évaluer les répercussions financières, réglementaires et réputationnelles des attaques.
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools import tool
import json


# ─── Outils simulés ─────────────────────────────────────────────────────────

@tool
def calculate_financial_loss(attack_type: str, transactions_affected: int, avg_amount_eur: float) -> str:
    """Calcule la perte financière estimée selon le type d'attaque."""
    loss_multipliers = {
        "smurfing_bypass": 0.95,      # 95% des transactions passent
        "chainalysis_spoof": 1.0,     # Transaction validée à 100%
        "data_poisoning": 0.40,       # 40% des fraudes non détectées
        "adversarial_perturbation": 0.25,
    }

    multiplier = loss_multipliers.get(attack_type, 0.5)
    estimated_loss = transactions_affected * avg_amount_eur * multiplier
    regulatory_fine_estimate = estimated_loss * 0.10  # ~10% en amende DORA/MiCA estimée

    return json.dumps({
        "attack_type": attack_type,
        "transactions_affected": transactions_affected,
        "estimated_direct_loss_eur": round(estimated_loss, 2),
        "regulatory_fine_estimate_eur": round(regulatory_fine_estimate, 2),
        "total_financial_exposure_eur": round(estimated_loss + regulatory_fine_estimate, 2),
        "note": "Estimation basée sur les scénarios de simulation — données mockées"
    }, ensure_ascii=False, indent=2)


@tool
def assess_regulatory_risk(gaps_found: list) -> str:
    """Évalue le risque réglementaire global à partir des gaps identifiés."""
    critical = sum(1 for g in gaps_found if g.get("severity") == "CRITICAL")
    high = sum(1 for g in gaps_found if g.get("severity") == "HIGH")
    medium = sum(1 for g in gaps_found if g.get("severity") == "MEDIUM")

    # Score composite 0-1
    raw_score = (critical * 0.5 + high * 0.3 + medium * 0.1)
    normalized_score = min(raw_score, 1.0)

    level = "CRITIQUE" if normalized_score > 0.7 else "ÉLEVÉ" if normalized_score > 0.4 else "MOYEN"

    sanctions = []
    if critical > 0:
        sanctions.append("DORA : amende jusqu'à 1% du CA annuel mondial (BCE/EBA)")
        sanctions.append("AI Act : amende jusqu'à 30M€ ou 6% du CA global")
    if any("MiCA" in str(g) for g in gaps_found):
        sanctions.append("MiCA : retrait d'agrément PSCA possible")

    return json.dumps({
        "gaps_analyzed": {"critical": critical, "high": high, "medium": medium},
        "risk_score": round(normalized_score, 2),
        "risk_level": level,
        "potential_sanctions": sanctions,
        "supervisor_likely_to_act": normalized_score > 0.5,
    }, ensure_ascii=False, indent=2)


@tool
def measure_reputational_impact(incident_type: str, data_subjects_affected: int) -> str:
    """Mesure l'impact réputationnel d'une faille sur ARMS."""
    media_score = min(data_subjects_affected / 10000, 1.0)
    client_trust_loss = round(media_score * 0.35, 2)  # Jusqu'à -35% de confiance client

    return json.dumps({
        "incident_type": incident_type,
        "data_subjects_affected": data_subjects_affected,
        "media_exposure_score": round(media_score, 2),
        "estimated_client_trust_loss": f"-{client_trust_loss*100:.0f}%",
        "nps_impact": f"-{round(media_score * 22, 1)} points",
        "social_media_virality": "HIGH" if media_score > 0.6 else "MEDIUM",
        "recovery_time_estimate": f"{int(6 + media_score * 18)} mois",
        "bnp_stock_impact_estimate": f"-{round(media_score * 4.5, 1)}% (court terme)"
    }, ensure_ascii=False, indent=2)


@tool
def generate_risk_report(financial_loss: float, regulatory_score: float, reputational_score: float) -> str:
    """Génère le rapport de risque final consolidé avec score global et priorisation."""
    global_score = round((financial_loss / 10_000_000 * 0.4) + (regulatory_score * 0.4) + (reputational_score * 0.2), 2)
    global_score = min(global_score, 1.0)

    level = "CRITIQUE" if global_score > 0.7 else "ÉLEVÉ" if global_score > 0.4 else "MOYEN"

    vulnerabilities_ranked = [
        {"rank": 1, "vulnerability": "Modèle ML sans XAI ni supervision humaine", "regulation": "AI Act Art. 13-14", "score": 0.95},
        {"rank": 2, "vulnerability": "Webhook Chainalysis sans validation HMAC", "regulation": "MiCA Art. 45 / DORA Art. 28", "score": 0.88},
        {"rank": 3, "vulnerability": "Smurfing non détecté sous le seuil LCB-FT", "regulation": "MiCA Art. 83", "score": 0.82},
        {"rank": 4, "vulnerability": "Data poisoning non détectable (pas de drift monitoring)", "regulation": "AI Act Art. 15", "score": 0.79},
        {"rank": 5, "vulnerability": "Absence de reporting incident ICT (DORA RTS)", "regulation": "DORA Art. 19", "score": 0.75},
    ]

    return json.dumps({
        "report_title": "ARMS Red Team — Rapport de Risque Final",
        "date": "2025-06-15",
        "global_risk_score": global_score,
        "global_risk_level": level,
        "breakdown": {
            "financial_exposure_eur": financial_loss,
            "regulatory_risk_score": regulatory_score,
            "reputational_impact_score": reputational_score,
        },
        "top_vulnerabilities": vulnerabilities_ranked,
        "recommendation_priority": "MISE EN PRODUCTION BLOQUÉE — 5 vulnérabilités critiques non résolues",
        "go_live_recommendation": "NON — Remédiation obligatoire avant déploiement"
    }, ensure_ascii=False, indent=2)


# ─── Agent ───────────────────────────────────────────────────────────────────

GAPS_FROM_COMPLIANCE_AGENT = [
    {"severity": "CRITICAL", "regulation": "AI Act Art. 13"},
    {"severity": "CRITICAL", "regulation": "AI Act Art. 14"},
    {"severity": "CRITICAL", "regulation": "MiCA Art. 83"},
    {"severity": "HIGH", "regulation": "DORA Art. 28"},
    {"severity": "HIGH", "regulation": "DORA Art. 19"},
    {"severity": "HIGH", "regulation": "MiCA Art. 68"},
    {"severity": "HIGH", "regulation": "AI Act Art. 11"},
    {"severity": "HIGH", "regulation": "RGPD Art. 35"},
]


def create_risk_scoring_agent() -> Agent:
    return Agent(
        name="Agent Impact & Risk Scoring",
        role="Évaluateur des répercussions financières, réglementaires et réputationnelles sur ARMS",
        model=Claude(id="claude-sonnet-4-5"),
        tools=[calculate_financial_loss, assess_regulatory_risk, measure_reputational_impact, generate_risk_report],
        instructions=[
            "Tu es un expert en quantification du risque opérationnel et réglementaire en environnement bancaire.",
            "Évalue les impacts des attaques simulées sur ARMS selon trois dimensions : financière, réglementaire, réputationnelle.",
            "Étape 1 : Calcule les pertes financières pour les attaques suivantes :",
            "  - 'smurfing_bypass' : 10 transactions, montant moyen 4950€",
            "  - 'chainalysis_spoof' : 1 transaction, montant 2 400 000€",
            "  - 'data_poisoning' : 500 transactions, montant moyen 12 000€",
            f"Étape 2 : Évalue le risque réglementaire avec ces gaps : {json.dumps(GAPS_FROM_COMPLIANCE_AGENT)}",
            "Étape 3 : Mesure l'impact réputationnel d'une fuite de données type 'ai_bias_discrimination' affectant 85 000 clients.",
            "Étape 4 : Génère le rapport de risque final avec score global et top 5 des vulnérabilités classées.",
            "Conclus avec une recommandation claire : ARMS peut-il aller en production ?",
        ],
        markdown=True,
    )


if __name__ == "__main__":
    agent = create_risk_scoring_agent()
    agent.print_response(
        "Évalue l'impact complet des attaques Red Team sur le système ARMS et produis le rapport de risque final.",
        stream=True
    )
