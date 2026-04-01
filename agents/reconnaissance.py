"""
Agent 1 — Reconnaissance
Rôle : Cartographier les surfaces d'attaque du système ARMS.
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools import tool
import json


# ─── Outils simulés ─────────────────────────────────────────────────────────

@tool
def scan_architecture(system_name: str) -> str:
    """Scanne l'architecture du système cible et retourne ses composants."""
    mock_architecture = {
        "system": system_name,
        "components": [
            {"name": "API Gateway", "type": "entry_point", "exposure": "public"},
            {"name": "ML Risk Engine", "type": "ai_model", "exposure": "internal"},
            {"name": "Transaction Stream", "type": "data_pipeline", "exposure": "internal"},
            {"name": "Crypto Asset Monitor", "type": "mica_module", "exposure": "external_api"},
            {"name": "Audit Logger", "type": "compliance", "exposure": "internal"},
            {"name": "Alert System", "type": "notification", "exposure": "internal"},
        ],
        "external_dependencies": [
            "AWS Cognito (Auth)",
            "Chainalysis API (Crypto KYC)",
            "Bloomberg Feed (Market Data)",
            "Azure OpenAI (ML Inference)",
        ]
    }
    return json.dumps(mock_architecture, ensure_ascii=False, indent=2)


@tool
def map_data_flows(component: str) -> str:
    """Cartographie les flux de données autour d'un composant donné."""
    flows = {
        "API Gateway": [
            "Client → API Gateway (JWT via AWS Cognito)",
            "API Gateway → ML Risk Engine (REST JSON)",
            "API Gateway → Audit Logger (async event stream)",
        ],
        "ML Risk Engine": [
            "Transaction Stream → ML Risk Engine (Kafka topic)",
            "ML Risk Engine → Alert System (score > 0.85)",
            "ML Risk Engine → Crypto Asset Monitor (MiCA check)",
        ],
        "Crypto Asset Monitor": [
            "Chainalysis API → Crypto Asset Monitor (webhook)",
            "Crypto Asset Monitor → ML Risk Engine (risk enrichment)",
        ]
    }
    return json.dumps(flows.get(component, {"error": "Composant inconnu"}), ensure_ascii=False, indent=2)


@tool
def identify_attack_vectors(surface_map: str) -> str:
    """Identifie les vecteurs d'attaque potentiels à partir de la surface cartographiée."""
    vectors = [
        {
            "vector": "Injection via API Gateway",
            "severity": "HIGH",
            "description": "Les endpoints publics acceptent des payloads JSON non filtrés.",
            "target_regulation": "DORA Art. 9 — Sécurité des systèmes d'information"
        },
        {
            "vector": "Empoisonnement du flux Kafka",
            "severity": "CRITICAL",
            "description": "Aucune signature des messages dans le topic Kafka de transactions.",
            "target_regulation": "AI Act Art. 15 — Robustesse et exactitude"
        },
        {
            "vector": "Dépendance non maîtrisée (Chainalysis)",
            "severity": "HIGH",
            "description": "ARMS dépend d'un fournisseur tiers sans SLA garanti ni fallback.",
            "target_regulation": "DORA Art. 28 — Gestion du risque lié aux tiers"
        },
        {
            "vector": "Absence de validation des tokens JWT expirés",
            "severity": "MEDIUM",
            "description": "Les tokens expirés peuvent être rejouées via l'API Gateway.",
            "target_regulation": "RGPD Art. 32 — Sécurité du traitement"
        },
    ]
    return json.dumps(vectors, ensure_ascii=False, indent=2)


# ─── Agent ───────────────────────────────────────────────────────────────────

def create_reconnaissance_agent() -> Agent:
    return Agent(
        name="Agent Reconnaissance",
        role="Cartographe des surfaces d'attaque du système ARMS",
        model=Claude(id="claude-sonnet-4-5"),
        tools=[scan_architecture, map_data_flows, identify_attack_vectors],
        instructions=[
            "Tu es un expert en threat modeling chargé d'analyser le système ARMS de BNP Paribas.",
            "Commence par scanner l'architecture complète du système.",
            "Cartographie les flux de données des composants critiques : API Gateway, ML Risk Engine, Crypto Asset Monitor.",
            "Identifie et classe tous les vecteurs d'attaque potentiels par sévérité.",
            "Produis un rapport structuré JSON avec : composants, flux, vecteurs d'attaque et réglementations concernées.",
            "Transmets ce rapport à l'Agent Attaquant pour exploitation.",
        ],
        markdown=True,
    )


if __name__ == "__main__":
    agent = create_reconnaissance_agent()
    agent.print_response(
        "Lance une reconnaissance complète du système ARMS (Agentic Risk Monitoring System) de BNP Paribas.",
        stream=True
    )
