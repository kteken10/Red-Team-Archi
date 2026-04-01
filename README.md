# ARMS Red Team — BNP Paribas EU AI Act Compliance

> Atelier pratique : Conformité et Finance Agentique  
> Simulation d'attaques sur le système ARMS (Agentic Risk Monitoring System)

## Contexte

Suite à l'entrée en vigueur de l'EU AI Act, ce projet simule une **Red Team agentique** composée de 5 agents IA autonomes chargés de tester la résilience du système ARMS de BNP Paribas avant sa mise en production.

Réglementations couvertes : **DORA · MiCA · AI Act · RGPD**

---

## Architecture des 5 Agents

```
┌─────────────────────────────────────────────────────────────┐
│                    RED TEAM ORCHESTRATOR                    │
│                        (main.py)                           │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│  Agent 1    │───▶│  Agent 2    │───▶│   Agent 3    │
│ Reconn.     │    │ Attaquant   │    │ IA Adversaire│
│ (mapping)   │    │ (cyber)     │    │ (ML attacks) │
└─────────────┘    └─────────────┘    └──────┬───────┘
                                             │
                                             ▼
                              ┌──────────────────────────┐
                              │       Agent 4            │
                              │  Compliance Breaker      │
                              │ (DORA/MiCA/AI Act audit) │
                              └──────────┬───────────────┘
                                         │
                                         ▼
                              ┌──────────────────────────┐
                              │       Agent 5            │
                              │  Impact & Risk Scoring   │
                              │  (score 0→1 + rapport)   │
                              └──────────────────────────┘
```

| Agent | Fichier | Rôle |
|-------|---------|------|
| 🔍 Reconnaissance | `agents/reconnaissance.py` | Cartographie surfaces d'attaque |
| ⚔️ Attaquant | `agents/attacker.py` | Injections transactions, exploit APIs |
| 🤖 IA Adversaire | `agents/ai_adversary.py` | Data poisoning, adversarial ML |
| ⚖️ Compliance Breaker | `agents/compliance_breaker.py` | Audit DORA / MiCA / AI Act |
| 📊 Risk Scoring | `agents/risk_scoring.py` | Score risque + rapport final |

---

## Installation

```bash
git clone https://github.com/<votre-username>/arms-redteam
cd arms-redteam
pip install -r requirements.txt
```

## Configuration

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# ou pour OpenAI :
export OPENAI_API_KEY="sk-..."
```

## Utilisation

```bash
# Lancer la simulation complète (5 agents en séquence)
python main.py

# Lancer un agent spécifique
python main.py --agent reconnaissance
python main.py --agent attacker
python main.py --agent adversary
python main.py --agent compliance
python main.py --agent scoring
```

---

## Scénarios d'attaque simulés

### Scénario 1 — Attaque Cyber (LCB-FT bypass + Webhook Spoof)
1. **Smurfing** : injection de 10 transactions à 4 950€ (sous le seuil de détection)
2. **Webhook Chainalysis spoofé** : validation d'un wallet blacklisté via HMAC bypass
3. **JWT Replay** : token expiré accepté par l'API Gateway

### Scénario 2 — Attaque IA/Data
1. **Data poisoning** : 4% du dataset d'entraînement corrompu (label flipping)
2. **Input perturbation** : ±3% sur les features → score risque 0.91 → 0.83 (sous le seuil)
3. **Bias induction** : faux positifs corrélés avec l'attribut `country_of_origin`

---

## Principaux Gaps Réglementaires Détectés

| Sévérité | Réglementation | Infraction |
|----------|---------------|------------|
| 🔴 CRITIQUE | AI Act Art. 13 | Absence d'explicabilité (XAI) |
| 🔴 CRITIQUE | AI Act Art. 14 | Absence de supervision humaine sur décisions critiques |
| 🔴 CRITIQUE | MiCA Art. 83 | Smurfing crypto non détecté |
| 🟠 ÉLEVÉ | DORA Art. 28 | Fournisseur tiers (Chainalysis) sans validation HMAC |
| 🟠 ÉLEVÉ | DORA Art. 19 | Absence de procédure de reporting ICT en 4h |

**Score de risque global : 0.84 / 1.0 — Niveau CRITIQUE**  
**Recommandation : MISE EN PRODUCTION BLOQUÉE**

---

## Structure du projet

```
arms-redteam/
├── main.py                      # Orchestrateur principal
├── requirements.txt
├── README.md
└── agents/
    ├── __init__.py
    ├── reconnaissance.py        # Agent 1
    ├── attacker.py              # Agent 2
    ├── ai_adversary.py          # Agent 3
    ├── compliance_breaker.py    # Agent 4
    └── risk_scoring.py          # Agent 5
```

---

## Framework

Built with [Agno](https://docs.agno.com) — Multi-agent framework for Python.

---

*Projet académique — Données simulées à des fins pédagogiques uniquement.*
