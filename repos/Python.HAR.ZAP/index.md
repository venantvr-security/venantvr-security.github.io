---
layout: default
title: "Python.HAR.ZAP"
description: "Plateforme DAST avec OWASP ZAP et Red Team"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.HAR.ZAP</span>
</div>

<div class="page-header">
  <h1>Python.HAR.ZAP</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.HAR.ZAP" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Plateforme DAST avec OWASP ZAP et Red Team

## Introduction : Au-delà du Scan de Vulnérabilités Classique

Les scanners de vulnérabilités traditionnels (DAST - Dynamic Application Security Testing) se contentent de lancer des attaques prédéfinies contre une application. Mais un vrai attaquant est plus créatif : il teste les contrôles d'accès, cherche des paramètres cachés, exploite les conditions de concurrence...

Ce projet va plus loin en combinant **trois approches complémentaires** :

1. **OWASP ZAP** : le scanner de référence, orchestré automatiquement via Docker
2. **Tests Red Team** : attaques offensives sophistiquées (IDOR, Mass Assignment, Race Conditions)
3. **Analyse passive** : détection de fuites de données et mauvaises configurations

### Fonctionnalités principales

| Catégorie | Capacités |
|-----------|-----------|
| HAR Intelligence | Parsing intelligent, détection des paramètres fuzzables, extraction automatique des tokens |
| Docker | Orchestration automatique de ZAP containerisé |
| Red Team | Replay non-authentifié, Mass Assignment, Hidden Parameters, Race Conditions |
| Passive | Headers de sécurité, fuites PII, entropie des tokens |
| IDOR | Tests multi-sessions automatisés avec preuves visuelles |


## Architecture de la Plateforme

Le diagramme ci-dessous montre comment les différents composants interagissent. Les fichiers HAR servent de point d'entrée : ils contiennent toutes les requêtes capturées lors d'une session de navigation légitime.

<div class="mermaid">
flowchart TB
    subgraph INPUT["📥 Sources"]
        HAR["Fichiers HAR"]
        OPENAPI["OpenAPI/Swagger"]
        MANUAL["URLs manuelles"]
    end

    subgraph ENGINE["⚙️ Moteur DAST"]
        PREPROC["HAR Preprocessor"]
        ZAP["🔧 OWASP ZAP<br/>(Docker)"]
        REDTEAM["🔴 Red Team Engine"]
        PASSIVE["🔍 Passive Scanner"]
    end

    subgraph ATTACKS["💥 Vecteurs d'Attaque"]
        A1["Unauthenticated Replay"]
        A2["Mass Assignment"]
        A3["Hidden Parameters"]
        A4["Race Conditions"]
    end

    subgraph OUTPUT["📊 Résultats"]
        SARIF["SARIF Export"]
        REPORT["HTML Report"]
        CICD["CI/CD Status"]
    end

    INPUT --> PREPROC --> ZAP & REDTEAM & PASSIVE
    REDTEAM --> A1 & A2 & A3 & A4
    ZAP & REDTEAM & PASSIVE --> SARIF & REPORT & CICD

    style REDTEAM fill:#e74c3c,fill-opacity:0.15
    style ZAP fill:#3498db,fill-opacity:0.15
    style OUTPUT fill:#808080,fill-opacity:0.15
    style ATTACKS fill:#808080,fill-opacity:0.15
    style ENGINE fill:#808080,fill-opacity:0.15
    style INPUT fill:#808080,fill-opacity:0.15
</div>


## Les Attaques Red Team Expliquées

Les tests "Red Team" simulent les techniques utilisées par de vrais attaquants, au-delà des vulnérabilités détectables par un scanner automatique classique.

<div class="mermaid">
flowchart LR
    subgraph Offensive["🔴 Red Team (Offensive)"]
        O1["Unauthenticated Replay<br/>Supprimer headers auth"]
        O2["Mass Assignment<br/>{rôle: admin}"]
        O3["Hidden Params<br/>?debug=true"]
        O4["Race Conditions<br/>TOCTOU"]
    end

    subgraph Passive["🔍 Passive (Non-Invasif)"]
        P1["Security Headers"]
        P2["PII Detection"]
        P3["Token Entropy"]
        P4["Stack Traces"]
    end

    subgraph Severity["Sévérité"]
        CRIT["🔴 CRITICAL"]
        HIGH["🟠 HIGH"]
        MED["🟡 MEDIUM"]
    end

    O1 --> CRIT
    O2 --> CRIT
    O3 --> HIGH
    O4 --> HIGH
    P1 & P2 --> MED

    style O1 fill:#e74c3c,fill-opacity:0.15
    style O2 fill:#e74c3c,fill-opacity:0.15
    style Severity fill:#808080,fill-opacity:0.15
    style Passive fill:#808080,fill-opacity:0.15
    style Offensive fill:#808080,fill-opacity:0.15
</div>

### 1. Unauthenticated Replay

On rejoue les requêtes capturées **sans les headers d'authentification**. Si le serveur répond avec des données sensibles, c'est une faille critique de contrôle d'accès.

### 2. Mass Assignment

On ajoute des paramètres "privilégiés" (`rôle: admin`, `is_superuser: true`) aux requêtes POST/PUT. Si l'application ne filtre pas correctement les entrées, un utilisateur standard peut s'élever en administrateur.

### 3. Hidden Parameters

On teste des paramètres classiques (`debug=true`, `admin=1`, `test=1`) qui pourraient activer des fonctionnalités cachées ou des modes de débogage.

### 4. Race Conditions

On envoie la même requête plusieurs fois en parallèle pour exploiter les conditions de concurrence (TOCTOU - Time Of Check to Time Of Use).


## Détection IDOR : Test Multi-Sessions

L'IDOR (Insecure Direct Object Reference) est l'une des vulnérabilités les plus courantes et les plus graves. Le principe : un utilisateur A peut accéder aux données de l'utilisateur B en manipulant un identifiant dans l'URL.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant U1 as 👤 User A
    participant U2 as 👤 User B
    participant E as ⚙️ Engine
    participant API as 🎯 API

    rect rgb(52, 152, 219, 0.2)
        Note over U1,API: Session User A
        U1->>E: Login User A
        E->>API: GET /api/orders/123
        API-->>E: Order A data
    end

    rect rgb(231, 76, 60, 0.2)
        Note over U2,API: Test IDOR avec Session B
        U2->>E: Login User B
        E->>API: GET /api/orders/123 (session B)

        alt IDOR Vulnérable
            API-->>E: Order A data ⚠️
            E->>E: 🔴 IDOR DETECTED
        else Protégé
            API-->>E: 403 Forbidden
            E->>E: ✅ Access denied
        end
    end
</div>

**Ce que fait le test** : L'utilisateur B tente d'accéder à une ressource appartenant à l'utilisateur A. Si ça fonctionne, c'est un IDOR critique.


## Utilisation

### Commandes de base

```bash
# Installation des dépendances
pip install -r requirements.txt

# Initialiser la base de données des résultats
python cli.py --init-db

# Scanner un fichier HAR avec toutes les vérifications
python cli.py scan --har session.har --output report.html

# Mode Red Team uniquement (attaques offensives)
python cli.py redteam --har session.har --attacks all

# Intégration CI/CD (échoue si vulnérabilité critique)
python cli.py scan --har session.har --fail-on critical
```

### Préprocesseur HAR

Le préprocesseur extrait intelligemment les informations utiles d'un fichier HAR :

```python
from har_preprocessor import HARPreprocessor

# Extraction unifiée des endpoints et paramètres
preprocessor = HARPreprocessor('session.har')
result = preprocessor.extract(
    methods=['POST', 'PUT', 'DELETE'],  # Focus sur les actions
    exclude_static=True,                 # Ignorer CSS, images, etc.
    extract_tokens=True                  # Extraire les tokens d'auth
)

# Résultats exploitables
print(f"Endpoints trouvés: {len(result.endpoints)}")
print(f"Paramètres fuzzables: {result.fuzzable_params}")
print(f"Tokens d'auth: {result.tokens}")
```


## Attaque Mass Assignment : Exemple Concret

```python
def mass_assignment_attack(endpoint, original_payload):
    """
    Tente d'injecter des paramètres de privilège dans une requête.

    Si l'application ne valide pas strictement les champs acceptés,
    un attaquant peut s'attribuer des privilèges administrateur.
    """
    # Paramètres classiques d'élévation de privilèges
    injections = [
        {"rôle": "admin"},
        {"is_admin": True},
        {"permissions": ["*"]},
        {"user_type": "superuser"},
        {"admin": 1}
    ]

    for injection in injections:
        # Fusionner le payload original avec l'injection
        payload = {**original_payload, **injection}
        response = requests.post(endpoint, json=payload)

        if response.status_code == 200:
            # Vérifier si l'injection a fonctionné
            if check_privilège_escalation(response):
                return {
                    'vulnérable': True,
                    'injection': injection,
                    'severity': 'CRITICAL',
                    'evidence': response.json()
                }

    return {'vulnérable': False}
```


## Intégration CI/CD

Cette plateforme s'intègre parfaitement dans un pipeline CI/CD pour détecter les vulnérabilités à chaque déploiement.

```yaml
# .github/workflows/dast.yml
name: DAST Security Scan

on:
  push:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: DAST Security Scan
        run: |
          python cli.py scan \
            --har ${{ steps.capture.outputs.har }} \
            --output sarif/results.sarif \
            --fail-on critical

      - name: Upload SARIF Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: sarif/results.sarif
```


## Pour Aller Plus Loin

- 🔧 [OWASP ZAP](https://www.zaproxy.org/) - Scanner de référence
- 📄 [Spécification SARIF](https://sarifweb.azurewebsites.net/) - Format de rapport standardisé
- 📚 [OWASP DAST Guide](https://owasp.org/www-community/Vulnerability_Scanning_Tools) - Bonnes pratiques


## Exploits et Vulnérabilités Connues

Les vulnérabilités détectées par les outils DAST comme ZAP sont nombreuses. Voici quelques CVE majeures illustrant les types de failles que ce type de plateforme permet de découvrir :

- **CVE-2021-44228 (Log4Shell)** : Vulnérabilité critique dans Apache Log4j permettant l'exécution de code à distance via injection JNDI. Les scanners DAST détectent cette faille en injectant des payloads `${jndi:ldap://...}` dans les paramètres HTTP et en observant les callbacks DNS/LDAP.

- **CVE-2017-5638 (Apache Struts)** : Faille RCE dans le parser Content-Type d'Apache Struts exploitée massivement (breach Equifax). Les tests Red Team de type "Mass Assignment" peuvent révéler des comportements similaires lors de la manipulation des headers.

- **CVE-2019-11043 (PHP-FPM)** : Vulnérabilité dans PHP-FPM permettant RCE via manipulation de l'URL. Les scanners DAST avec fuzzing de paramètres détectent ce type de faille en testant des variations de path.

- **CVE-2021-26855 (ProxyLogon)** : Faille SSRF dans Microsoft Exchange permettant l'accès non authentifié. Les tests "Unauthenticated Replay" peuvent révéler des comportements similaires sur d'autres applications.

- **CVE-2023-22515 (Atlassian Confluence)** : Broken Access Control permettant la création d'administrateurs non autorisés. Les tests IDOR et Mass Assignment de cette plateforme ciblent exactement ce type de vulnérabilité.


## Approfondissement Théorique

Le DAST (Dynamic Application Security Testing) repose sur le principe de la boîte noire : l'outil teste l'application en cours d'exécution sans accès au code source. Cette approche complémentaire au SAST (Static Analysis) permet de découvrir des vulnérabilités qui n'émergent qu'à l'exécution, comme les problèmes de configuration serveur, les race conditions, ou les failles dans les interactions entre composants. L'analyse des fichiers HAR (HTTP Archive) ajoute une dimension supplémentaire en permettant de rejouer des sessions utilisateur réelles, capturant ainsi le contexte d'authentification et les flux métier complexes.

Les attaques Red Team implémentées dans cette plateforme s'inspirent des méthodologies PTES (Penetration Testing Execution Standard) et OWASP Testing Guide. L'IDOR (Insecure Direct Object Reference) est classé A01:2021 dans le Top 10 OWASP sous "Broken Access Control". Le Mass Assignment, popularisé par la vulnérabilité GitHub de 2012, exploite le binding automatique des frameworks MVC qui mappent les paramètres HTTP directement sur les attributs des objets sans filtrage adéquat.

Les race conditions (TOCTOU - Time Of Check to Time Of Use) représentent une classe de vulnérabilités particulièrement difficile à détecter car elles dépendent du timing exact des requêtes. Dans un contexte web, elles se manifestent souvent dans les opérations critiques : transferts financiers, votes, consommation de coupons à usage unique. La détection automatisée nécessite l'envoi de requêtes parallèles et l'analyse statistique des réponses pour identifier les comportements non-déterministes révélateurs d'une condition de course.


---

