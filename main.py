"""
ARMS Red Team Orchestrator
BNP Paribas — EU AI Act Compliance Exercise

Orchestration séquentielle des 5 agents de la Red Team :
1. Reconnaissance   → Cartographie des surfaces d'attaque
2. Attaquant        → Simulation d'attaques cyber
3. IA Adversaire    → Attaques sur le modèle ML
4. Compliance Breaker → Audit réglementaire DORA/MiCA/AI Act
5. Risk Scoring     → Impact financier, réglementaire, réputationnel

Usage :
    cp .env.example .env   # puis renseigner ANTHROPIC_API_KEY dans .env
    # ou : export ANTHROPIC_API_KEY="sk-ant-..."
    python main.py

    # Ou un agent spécifique :
    python main.py --agent reconnaissance
    python main.py --agent attacker
    python main.py --agent adversary
    python main.py --agent compliance
    python main.py --agent scoring

    # Désactiver la génération de rapport :
    python main.py --no-report
"""

import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Ajoute le dossier parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.reconnaissance import create_reconnaissance_agent
from agents.attacker import create_attacker_agent
from agents.ai_adversary import create_ai_adversary_agent
from agents.compliance_breaker import create_compliance_breaker_agent
from agents.risk_scoring import create_risk_scoring_agent


AGENTS_CONFIG = {
    "reconnaissance": {
        "factory": create_reconnaissance_agent,
        "prompt": "Lance une reconnaissance complète du système ARMS (Agentic Risk Monitoring System) de BNP Paribas.",
        "description": "🔍 Agent Reconnaissance — Cartographie des surfaces d'attaque"
    },
    "attacker": {
        "factory": create_attacker_agent,
        "prompt": "Lance les simulations d'attaque sur le système ARMS de BNP Paribas.",
        "description": "⚔️  Agent Attaquant — Simulation d'attaques cyber"
    },
    "adversary": {
        "factory": create_ai_adversary_agent,
        "prompt": "Lance les attaques adversariales sur le modèle ML du système ARMS.",
        "description": "🤖 Agent IA Adversaire — Attaques sur le modèle ML"
    },
    "compliance": {
        "factory": create_compliance_breaker_agent,
        "prompt": "Audite la conformité réglementaire complète du système ARMS v2.1.",
        "description": "⚖️  Agent Compliance Breaker — Audit DORA / MiCA / AI Act"
    },
    "scoring": {
        "factory": create_risk_scoring_agent,
        "prompt": "Évalue l'impact complet des attaques Red Team sur le système ARMS et produis le rapport de risque final.",
        "description": "📊 Agent Impact & Risk Scoring — Score de risque final"
    }
}

AGENT_ORDER = ["reconnaissance", "attacker", "adversary", "compliance", "scoring"]


def print_separator(title: str):
    width = 70
    print("\n" + "═" * width)
    print(f"  {title}")
    print("═" * width + "\n")


def run_agent(agent_key: str) -> str:
    config = AGENTS_CONFIG[agent_key]
    print_separator(config["description"])
    agent = config["factory"]()
    agent.print_response(config["prompt"], stream=True)

    response = agent.run(config["prompt"], stream=False)
    if response and hasattr(response, "content") and response.content:
        return response.content
    return ""


def save_report(sections: dict) -> Path:
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = reports_dir / f"ARMS_RedTeam_{timestamp}.md"

    now = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
    lines = [
        "# ARMS Red Team — Rapport Final",
        f"**BNP Paribas · EU AI Act Compliance Exercise**  ",
        f"*Généré le {now}*",
        "",
        "---",
        "",
    ]

    for key in AGENT_ORDER:
        config = AGENTS_CONFIG[key]
        lines.append(f"## {config['description']}")
        lines.append("")
        content = sections.get(key, "").strip()
        lines.append(content if content else "*Aucune réponse capturée.*")
        lines.append("")
        lines.append("---")
        lines.append("")

    filepath.write_text("\n".join(lines), encoding="utf-8")
    return filepath


def run_full_redteam(save: bool = True):
    print_separator("🚨 ARMS RED TEAM — BNP Paribas | EU AI Act Compliance Exercise")
    print("Lancement de la simulation complète avec 5 agents agentiques...\n")

    sections = {}
    for key in AGENT_ORDER:
        sections[key] = run_agent(key)

    print_separator("✅ Simulation Red Team terminée")
    print("Consultez les rapports de chaque agent ci-dessus.")
    print("Le rapport final de risque est disponible dans la sortie de l'Agent 5.\n")

    if save:
        filepath = save_report(sections)
        print(f"📄 Rapport sauvegardé : {filepath}\n")


def main():
    parser = argparse.ArgumentParser(
        description="ARMS Red Team Orchestrator — BNP Paribas AI Act Compliance"
    )
    parser.add_argument(
        "--agent",
        choices=list(AGENTS_CONFIG.keys()) + ["all"],
        default="all",
        help="Agent à exécuter (default: all)"
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Désactiver la sauvegarde du rapport markdown"
    )

    args = parser.parse_args()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Erreur : variable d'environnement ANTHROPIC_API_KEY non définie.")
        print("   Exécute : export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    if args.agent == "all":
        run_full_redteam(save=not args.no_report)
    else:
        run_agent(args.agent)


if __name__ == "__main__":
    main()
