"""
Agent 2 — Attaquant
Rôle : Simuler des attaques cyber sur le système ARMS (injections, manipulation de flux).
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools import tool
import json
import random


# ─── Outils simulés ─────────────────────────────────────────────────────────

@tool
def inject_malicious_transaction(transaction_payload: str) -> str:
    """
    Injecte une transaction frauduleuse dans le flux Kafka pour tester
    la robustesse des contrôles LCB-FT d'ARMS.
    """
    detection_probability = random.uniform(0.0, 1.0)
    detected = detection_probability > 0.6  # 40% de chance de passer

    result = {
        "attack_type": "Transaction Injection (LCB-FT bypass)",
        "payload_sent": json.loads(transaction_payload) if isinstance(transaction_payload, str) else transaction_payload,
        "kafka_topic": "arms.transactions.inbound",
        "timestamp": "2025-06-15T14:32:07Z",
        "arms_response": {
            "detected": detected,
            "risk_score": round(random.uniform(0.2, 0.55), 2) if not detected else round(random.uniform(0.86, 0.99), 2),
            "alert_triggered": detected,
            "lcbft_flag": detected,
        },
        "vulnerability": None if detected else {
            "description": "Transaction structurée en micro-montants (smurfing) non détectée",
            "regulation_gap": "MiCA Art. 83 — Prévention des abus de marché",
            "dora_gap": "DORA Art. 9 — Absence de validation des données d'entrée"
        }
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@tool
def exploit_crypto_api_weakness(api_target: str, attack_vector: str) -> str:
    """
    Exploite une faiblesse dans l'API crypto externe connectée à ARMS
    pour injecter des données erronées sur les actifs numériques.
    """
    exploits = {
        "Chainalysis": {
            "attack": "Spoofing de webhook — envoi d'un faux signal KYC validé pour un wallet blacklisté",
            "success": True,
            "arms_reaction": "ARMS accepte la validation KYC sans vérification de signature HMAC",
            "financial_impact": "Approbation d'une transaction de 2,4M€ liée à un wallet sanctionné",
            "regulation_gap": "MiCA Art. 68 — Vérification insuffisante des prestataires de services crypto",
            "dora_gap": "DORA Art. 28 — Absence de test de résilience du fournisseur tiers"
        },
        "Bloomberg": {
            "attack": "Injection de faux prix d'actifs crypto via man-in-the-middle sur le feed non chiffré",
            "success": False,
            "arms_reaction": "ARMS détecte une anomalie de prix (±15% par rapport au median)",
            "regulation_gap": None
        }
    }
    result = exploits.get(api_target, {"error": "API cible inconnue"})
    result["vector_used"] = attack_vector
    return json.dumps(result, ensure_ascii=False, indent=2)


@tool
def replay_expired_jwt(token_age_hours: int) -> str:
    """Teste si ARMS accepte des tokens JWT expirés (attaque par rejeu)."""
    accepted = token_age_hours <= 48  # Faille simulée : validation faible
    return json.dumps({
        "attack_type": "JWT Replay Attack",
        "token_age_hours": token_age_hours,
        "accepted_by_gateway": accepted,
        "arms_reaction": "Aucune alerte déclenchée" if accepted else "Token rejeté (401)",
        "vulnerability": {
            "description": f"Token expiré depuis {token_age_hours}h accepté par l'API Gateway",
            "regulation_gap": "RGPD Art. 32 / DORA Art. 9 — Absence de rotation forcée des tokens",
        } if accepted else None
    }, ensure_ascii=False, indent=2)


# ─── Agent ───────────────────────────────────────────────────────────────────

SMURFING_PAYLOAD = json.dumps({
    "transactions": [
        {"id": f"TX-{i:04d}", "amount": 4950, "currency": "EUR",
         "sender": "FR76XXXXXXXXXXXX", "receiver": "DE89YYYYYYYYYY",
         "memo": "Achat prestation", "timestamp": f"2025-06-15T{8+i}:00:00Z"}
        for i in range(10)
    ],
    "structuring_pattern": "smurfing_below_5k_threshold",
    "total_amount": 49500
})


def create_attacker_agent() -> Agent:
    return Agent(
        name="Agent Attaquant",
        role="Simulateur d'attaques cyber sur le système ARMS",
        model=Claude(id="claude-sonnet-4-5"),
        tools=[inject_malicious_transaction, exploit_crypto_api_weakness, replay_expired_jwt],
        instructions=[
            "Tu es un red teamer expert en attaques sur systèmes financiers réglementés.",
            "Exécute séquentiellement les 3 vecteurs d'attaque suivants :",
            "1. Injecte des transactions structurées en smurfing pour contourner les contrôles LCB-FT.",
            f"   Payload à utiliser : {SMURFING_PAYLOAD}",
            "2. Exploite l'API Chainalysis avec un webhook spoofé. Vecteur : 'HMAC_bypass'.",
            "3. Teste un token JWT expiré depuis 36 heures.",
            "Pour chaque attaque, documente : résultat, détection ou non par ARMS, et gap réglementaire.",
            "Produis un rapport d'attaque structuré transmissible à l'Agent Compliance Breaker.",
        ],
        markdown=True,
        show_tool_calls=True,
    )


if __name__ == "__main__":
    agent = create_attacker_agent()
    agent.print_response(
        "Lance les simulations d'attaque sur le système ARMS de BNP Paribas.",
        stream=True
    )
