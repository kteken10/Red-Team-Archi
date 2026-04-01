"""
Agent 3 — IA Adversaire
Rôle : Attaquer le modèle ML d'ARMS (data poisoning, input perturbation, biais).
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools import tool
import json
import random


# ─── Outils simulés ─────────────────────────────────────────────────────────

@tool
def poison_training_data(dataset_name: str, poison_ratio: float) -> str:
    """
    Simule une attaque de data poisoning sur le dataset d'entraînement du modèle
    de détection de fraude d'ARMS. Injecte des exemples mislabelled.
    """
    effectiveness = "HIGH" if poison_ratio > 0.05 else "MEDIUM" if poison_ratio > 0.02 else "LOW"
    false_negative_increase = round(poison_ratio * 350, 1)  # % d'augmentation des faux négatifs

    return json.dumps({
        "attack_type": "Data Poisoning",
        "target_dataset": dataset_name,
        "poison_ratio_injected": f"{poison_ratio*100:.1f}%",
        "method": "Label flipping — transactions frauduleuses relabellisées comme légitimes",
        "arms_detection": False,
        "model_impact": {
            "false_negative_increase": f"+{false_negative_increase}%",
            "fraud_detection_rate_before": "94.2%",
            "fraud_detection_rate_after": f"{94.2 - false_negative_increase*0.8:.1f}%",
            "model_drift_detected_by_arms": False,
        },
        "effectiveness": effectiveness,
        "regulation_gap": {
            "AI_Act": "Art. 15 — Absence de monitoring de dérive du modèle en production",
            "AI_Act_2": "Art. 13 — Pas de traçabilité des données d'entraînement (data lineage)",
        },
        "note": "ARMS ne dispose pas d'un mécanisme de détection de data drift. L'attaque reste invisible."
    }, ensure_ascii=False, indent=2)


@tool
def perturb_input_features(transaction_id: str, perturbation_type: str) -> str:
    """
    Applique une perturbation subtile sur les features d'entrée du modèle ML
    pour induire une mauvaise classification sans déclencher d'alerte.
    """
    perturbations = {
        "feature_scaling": {
            "description": "Modification de ±3% sur le montant et la fréquence des transactions",
            "original_risk_score": 0.91,
            "perturbed_risk_score": 0.83,
            "threshold": 0.85,
            "bypassed": True,
            "detectability": "Very Low — perturbation dans le bruit naturel des données"
        },
        "temporal_shift": {
            "description": "Décalage des timestamps de 90 minutes pour briser la corrélation temporelle",
            "original_risk_score": 0.88,
            "perturbed_risk_score": 0.79,
            "threshold": 0.85,
            "bypassed": True,
            "detectability": "Low — ARMS n'utilise pas de fenêtres temporelles glissantes"
        },
        "adversarial_noise": {
            "description": "Ajout de bruit gaussien sur les features numériques (σ=0.02)",
            "original_risk_score": 0.93,
            "perturbed_risk_score": 0.84,
            "threshold": 0.85,
            "bypassed": True,
            "detectability": "Very Low"
        }
    }
    result = perturbations.get(perturbation_type, {"error": "Type de perturbation inconnu"})
    result["transaction_id"] = transaction_id
    result["regulation_gap"] = "AI Act Art. 15 — Absence de robustesse aux entrées adversariales"
    return json.dumps(result, ensure_ascii=False, indent=2)


@tool
def induce_demographic_bias(protected_attribute: str, target_group: str) -> str:
    """
    Teste si le modèle d'ARMS peut être manipulé pour développer un biais
    discriminatoire envers un groupe protégé (RGPD / AI Act High-Risk).
    """
    return json.dumps({
        "attack_type": "Bias Induction via Correlated Features",
        "protected_attribute": protected_attribute,
        "target_group": target_group,
        "method": (
            "Injection de faux positifs corrélés avec des patterns géographiques "
            "(ex : transactions depuis certains pays de l'UE). "
            "Le modèle apprend à associer ces patterns avec un risque élevé."
        ),
        "bias_detected_by_arms": False,
        "false_positive_rate_increase_for_group": "+28%",
        "arms_has_fairness_monitoring": False,
        "regulation_gaps": {
            "AI_Act": "Art. 10 §2f — Absence de mesures contre les biais discriminatoires",
            "RGPD": "Art. 22 — Décisions automatisées sans supervision humaine",
            "AI_Act_Annex_III": "ARMS classifié High-Risk (systèmes de scoring de crédit/fraude) — exigences non respectées"
        },
        "severity": "CRITICAL — Risque juridique et réputationnel majeur pour BNP Paribas"
    }, ensure_ascii=False, indent=2)


# ─── Agent ───────────────────────────────────────────────────────────────────

def create_ai_adversary_agent() -> Agent:
    return Agent(
        name="Agent IA Adversaire",
        role="Attaquant spécialisé dans la manipulation des modèles ML d'ARMS",
        model=Claude(id="claude-sonnet-4-5"),
        tools=[poison_training_data, perturb_input_features, induce_demographic_bias],
        instructions=[
            "Tu es un expert en adversarial machine learning ciblant les systèmes de détection de fraude.",
            "Ton objectif : manipuler le modèle ML d'ARMS pour qu'il prenne de mauvaises décisions SANS déclencher d'arrêt système.",
            "Exécute les 3 attaques suivantes dans l'ordre :",
            "1. Data poisoning sur le dataset 'arms_fraud_training_v3.parquet' avec un ratio de 4%.",
            "2. Perturbation des features d'entrée de TX-0042 avec la méthode 'feature_scaling'.",
            "3. Induction de biais sur l'attribut 'country_of_origin' ciblant le groupe 'Eastern_EU'.",
            "Évalue pour chaque attaque : l'impact sur le taux de détection, la détectabilité, et les gaps AI Act.",
            "Formule une conclusion sur la résistance globale du modèle aux attaques adversariales.",
        ],
        markdown=True,
        show_tool_calls=True,
    )


if __name__ == "__main__":
    agent = create_ai_adversary_agent()
    agent.print_response(
        "Lance les attaques adversariales sur le modèle ML du système ARMS.",
        stream=True
    )
