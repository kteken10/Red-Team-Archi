# ARMS Red Team — BNP Paribas EU AI Act Compliance

> Atelier de conformité et finance agentique  
> Simulation **Red Team agentique** sur le système **ARMS** (Agentic Risk Monitoring System) — cadre pédagogique et d’exercice réglementaire.

## Vision du projet

Ce dépôt ne pilote **aucun système réel** de BNP Paribas : il orchestre **cinq agents IA** (via [Agno](https://docs.agno.com) et **Claude**) qui produisent des **rapports et analyses textuels** à partir de **prompts** et d’**outils simulés** (mocks). L’objectif est de **structurer un parcours Red Team** aligné sur l’**EU AI Act** et les attentes **DORA · MiCA · RGPD**, pour réfléchir à la résilience, à la traçabilité et à la conformité avant toute mise en production fictive.

- **Enchaînement** : reconnaissance → attaques cyber → attaques ML → audit compliance → scoring de risque.  
- **Prérequis runtime** : une clé API **Anthropic** uniquement (`ANTHROPIC_API_KEY`).  
- **Modèle utilisé dans le code** : `claude-sonnet-4-5`.

Les tableaux et scores illustrés plus bas (ex. risque global **0.84**) correspondent aux **scénarios simulés** intégrés aux agents, pas à un audit d’un environnement de production.

---

## Architecture des 5 agents

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
| Reconnaissance | `agents/reconnaissance.py` | Cartographie des surfaces d’attaque |
| Attaquant | `agents/attacker.py` | Simulations d’attaques (injections, flux, etc.) |
| IA adversaire | `agents/ai_adversary.py` | Scénarios adversariaux sur le modèle ML |
| Compliance Breaker | `agents/compliance_breaker.py` | Audit DORA / MiCA / AI Act (données d’audit simulées) |
| Risk Scoring | `agents/risk_scoring.py` | Impact et rapport de risque final |

---

## Installation

**Prérequis** : Python 3.10 ou supérieur recommandé.

```bash
cd "Red Team Archi"   # ou le chemin de votre clone
python -m venv .venv
# Linux / macOS : source .venv/bin/activate
# Windows PowerShell : .\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Le fichier `requirements.txt` inclut **agno**, le client **anthropic** (nécessaire pour le modèle Claude dans Agno) et **python-dotenv** (chargement d’un fichier `.env` local).

---

## Configuration

Une seule variable d’environnement est requise — **clé API Anthropic** (`ANTHROPIC_API_KEY`).

**Option recommandée — fichier `.env` (déjà ignoré par Git)**

```bash
# Linux / macOS
cp .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env
```

Puis éditer `.env` et renseigner `ANTHROPIC_API_KEY=...`.

`main.py` charge automatiquement `.env` au démarrage.

**Ou variables d’environnement classiques**

**Linux / macOS**

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Windows (PowerShell)**

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

Aucun autre fournisseur (OpenAI, Azure, etc.) n’est configuré dans ce dépôt.

---

## Utilisation

Par défaut, **tous** les agents s’exécutent **à la suite** (`--agent` omis ou `--agent all`).

```bash
# Simulation complète (5 agents)
python main.py

# Équivalent explicite
python main.py --agent all

# Un seul agent
python main.py --agent reconnaissance
python main.py --agent attacker
python main.py --agent adversary
python main.py --agent compliance
python main.py --agent scoring
```

Les sorties sont affichées dans le terminal (streaming activé dans `main.py`).

---

## Scénarios d’attaque simulés

### Scénario 1 — Attaque cyber (LCB-FT, webhooks, API)

1. **Smurfing** : injection de transactions sous le seuil de détection.  
2. **Webhook Chainalysis spoofé** : validation d’un wallet blacklisté (scénario HMAC).  
3. **JWT replay** : token expiré accepté par la passerelle API (scénario).

### Scénario 2 — Attaque IA / données

1. **Data poisoning** : corruption partielle du jeu d’entraînement (label flipping).  
2. **Perturbation des entrées** : variation des features pour abaisser le score de risque.  
3. **Biais induit** : faux positifs corrélés à des attributs sensibles (scénario).

---

## Exemple de synthèse réglementaire (sortie type)

Les lignes ci-dessous illustrent le **type de conclusions** que les agents peuvent produire dans l’exercice ; elles ne constituent pas un rapport officiel.

| Sévérité | Réglementation | Exemple de constat (scénario) |
|----------|----------------|-------------------------------|
| Critique | AI Act Art. 13 | Absence ou insuffisance d’explicabilité (XAI) |
| Critique | AI Act Art. 14 | Supervision humaine absente sur décisions à haut risque |
| Critique | MiCA Art. 83 | Scénario de smurfing crypto non détecté |
| Élevé | DORA Art. 28 | Chaîne de confiance fournisseur / intégrité des flux |
| Élevé | DORA Art. 19 | Procédures de reporting ICT (scénario délai 4 h) |

**Exemple de score global affiché dans l’exercice : ~0.84 / 1.0 — niveau critique (simulation).**  
**Recommandation narrative possible dans le rapport agent : mise en production bloquée tant que les écarts ne sont pas traités (fiction pédagogique).**

---

## Structure du projet

```
Red Team Archi/
├── main.py                 # Orchestrateur CLI
├── requirements.txt
├── .env.example            # Modèle pour ANTHROPIC_API_KEY (copier vers .env)
├── .gitignore
├── README.md
└── agents/
    ├── __init__.py
    ├── reconnaissance.py
    ├── attacker.py
    ├── ai_adversary.py
    ├── compliance_breaker.py
    └── risk_scoring.py
```

---

## Framework

Construit avec **[Agno](https://docs.agno.com)** — framework multi-agents pour Python, modèle **Claude** (Anthropic).

---

*Projet à visée pédagogique — données et système ARMS présentés comme **simulés** à des fins d’apprentissage et d’exercice de conformité.*
