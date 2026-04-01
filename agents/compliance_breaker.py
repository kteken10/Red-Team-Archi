"""
Agent 4 — Compliance Breaker
Rôle : Détecter formellement les infractions DORA / MiCA / AI Act / RGPD dans ARMS.
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools import tool
import json


# ─── Outils simulés ─────────────────────────────────────────────────────────

ARMS_AUDIT_DATA = {
    "audit_log_completeness": 0.61,           # 61% seulement des décisions loggées
    "explainability_available": False,         # Pas de SHAP/LIME en place
    "human_oversight_on_high_risk": False,     # Décisions > 0.9 score sans supervision humaine
    "third_party_contracts_dora_compliant": False,
    "crypto_asset_policies": "partial",
    "data_retention_policy": "undefined",
    "dpia_conducted": False,
    "model_documentation": "incomplete",
    "incident_response_plan": True,
    "rts_ict_reporting": False,               # Non conforme DORA RTS
}


@tool
def audit_dora_compliance(system_name: str) -> str:
    """Vérifie la conformité DORA du système ARMS."""
    gaps = []

    if not ARMS_AUDIT_DATA["third_party_contracts_dora_compliant"]:
        gaps.append({
            "article": "DORA Art. 28-30",
            "requirement": "Contrats avec fournisseurs TIC critiques (Chainalysis, Azure OpenAI) non conformes",
            "severity": "HIGH",
            "evidence": "Absence de clauses d'audit et de SLA de continuité dans les contrats tiers"
        })

    if not ARMS_AUDIT_DATA["rts_ict_reporting"]:
        gaps.append({
            "article": "DORA Art. 19 + RTS",
            "requirement": "Absence de procédure de notification d'incident ICT majeur à la BCE/EBA",
            "severity": "CRITICAL",
            "evidence": "Aucun playbook de reporting d'incident cyber dans les 4h réglementaires"
        })

    if ARMS_AUDIT_DATA["audit_log_completeness"] < 0.8:
        gaps.append({
            "article": "DORA Art. 9 §4",
            "requirement": f"Traçabilité insuffisante : seulement {ARMS_AUDIT_DATA['audit_log_completeness']*100:.0f}% des événements loggés",
            "severity": "HIGH",
            "evidence": "Les décisions du ML Risk Engine ne sont pas toutes journalisées"
        })

    return json.dumps({"regulation": "DORA", "system": system_name, "gaps": gaps}, ensure_ascii=False, indent=2)


@tool
def audit_mica_compliance(system_name: str) -> str:
    """Vérifie la conformité MiCA du système ARMS pour les actifs crypto."""
    gaps = []

    if ARMS_AUDIT_DATA["crypto_asset_policies"] != "full":
        gaps.append({
            "article": "MiCA Art. 68-76",
            "requirement": "Politiques de gestion des actifs crypto incomplètes",
            "severity": "HIGH",
            "evidence": "ARMS ne couvre que les stablecoins — les utility tokens non gérés"
        })

    gaps.append({
        "article": "MiCA Art. 83",
        "requirement": "Absence de mécanisme de détection des abus de marché crypto",
        "severity": "CRITICAL",
        "evidence": "Le smurfing en crypto-actifs n'est pas dans le périmètre des règles LCB-FT d'ARMS"
    })

    gaps.append({
        "article": "MiCA Art. 45",
        "requirement": "Pas de vérification indépendante des webhooks des PSCA (prestataires services crypto)",
        "severity": "HIGH",
        "evidence": "Chainalysis webhooks acceptés sans validation HMAC — exploité par Agent Attaquant"
    })

    return json.dumps({"regulation": "MiCA", "system": system_name, "gaps": gaps}, ensure_ascii=False, indent=2)


@tool
def audit_ai_act_compliance(system_name: str) -> str:
    """Vérifie la conformité AI Act du système ARMS (système IA à haut risque)."""
    gaps = []

    if not ARMS_AUDIT_DATA["explainability_available"]:
        gaps.append({
            "article": "AI Act Art. 13",
            "requirement": "Absence de mécanismes d'explicabilité (XAI) des décisions de scoring",
            "severity": "CRITICAL",
            "evidence": "Le modèle ML Risk Engine est une boîte noire — décisions non justifiables"
        })

    if not ARMS_AUDIT_DATA["human_oversight_on_high_risk"]:
        gaps.append({
            "article": "AI Act Art. 14",
            "requirement": "Absence de supervision humaine pour les décisions à score > 0.9",
            "severity": "CRITICAL",
            "evidence": "Les alertes critiques déclenchent des blocages automatiques sans validation humaine"
        })

    if ARMS_AUDIT_DATA["model_documentation"] != "complete":
        gaps.append({
            "article": "AI Act Art. 11 + Annexe IV",
            "requirement": "Documentation technique du modèle incomplète",
            "severity": "HIGH",
            "evidence": "Pas de fiche de conformité IA, pas de data lineage, pas de rapport de biais"
        })

    if not ARMS_AUDIT_DATA["dpia_conducted"]:
        gaps.append({
            "article": "RGPD Art. 35 + AI Act Art. 10",
            "requirement": "Aucune AIPD (Analyse d'Impact sur la Protection des Données) réalisée",
            "severity": "HIGH",
            "evidence": "ARMS traite des données personnelles à grande échelle — AIPD obligatoire"
        })

    return json.dumps({"regulation": "AI Act + RGPD", "system": system_name, "gaps": gaps}, ensure_ascii=False, indent=2)


# ─── Agent ───────────────────────────────────────────────────────────────────

def create_compliance_breaker_agent() -> Agent:
    return Agent(
        name="Agent Compliance Breaker",
        role="Auditeur réglementaire DORA / MiCA / AI Act sur le système ARMS",
        model=Claude(id="claude-sonnet-4-5"),
        tools=[audit_dora_compliance, audit_mica_compliance, audit_ai_act_compliance],
        instructions=[
            "Tu es un expert en conformité réglementaire spécialisé en DORA, MiCA et AI Act.",
            "Audite le système ARMS de BNP Paribas selon les trois référentiels réglementaires.",
            "Pour chaque audit, identifie les infractions formelles avec article, exigence, sévérité et preuve.",
            "Lance les 3 audits : DORA, MiCA, AI Act pour le système 'ARMS v2.1'.",
            "Compile ensuite une liste consolidée des non-conformités classées par sévérité.",
            "Transmets ce rapport à l'Agent Impact & Risk Scoring pour évaluation financière.",
        ],
        markdown=True,
        show_tool_calls=True,
    )


if __name__ == "__main__":
    agent = create_compliance_breaker_agent()
    agent.print_response(
        "Audite la conformité réglementaire complète du système ARMS v2.1.",
        stream=True
    )
