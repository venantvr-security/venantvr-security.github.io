---
layout: default
title: "Python.Sqli.Détection"
description: "Détection d'Injection SQL par Fuzzing de Paramètres"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Sqli.Détection</span>
</div>

<div class="page-header">
  <h1>Python.Sqli.Détection</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Sqli.Détection" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Détection d'Injection SQL par Fuzzing de Paramètres

> **AVERTISSEMENT** : Ce projet est **strictement éducatif**. Testez uniquement sur vos propres applications.

## Introduction : L'Injection SQL, Fléau du Web

L'injection SQL reste l'une des vulnérabilités les plus critiques et les plus répandues. Elle figure systématiquement dans le Top 10 OWASP depuis sa création. Le principe est simple : un attaquant insère du code SQL malveillant dans un paramètre d'entrée, et l'application l'exécute aveuglément contre sa base de données.

Les conséquences peuvent être catastrophiques : vol de données sensibles, contournement d'authentification, modification ou destruction de données, voire prise de contrôle complète du serveur.

### Ce que ce projet permet de faire

Ce projet propose un **détecteur d'injection SQL par fuzzing**. Au lieu de chercher manuellement les vulnérabilités, le script teste automatiquement chaque paramètre avec des centaines de payloads connus, puis analyse les réponses pour identifier les points d'injection.

### Sources de payloads utilisées

Le fuzzer utilise des wordlists publiques reconnues dans la communauté de sécurité :

| Source | Description |
|--------|-------------|
| [payloadbox/sql-injection-payload-list](https://github.com/payloadbox/sql-injection-payload-list) | Collection exhaustive de payloads SQLi |
| [wfuzz SQL.txt](https://github.com/xmendez/wfuzz/blob/master/wordlist/Injections/SQL.txt) | Wordlist de fuzzing classique |
| [Auth_Bypass.txt](https://github.com/payloadbox/sql-injection-payload-list/blob/master/Intruder/exploit/Auth_Bypass.txt) | Payloads de contournement d'authentification |


## Architecture du Détecteur

Le détecteur fonctionne en trois phases : génération des requêtes, envoi et analyse des réponses. Le diagramme ci-dessous montre le flux complet de détection.

<div class="mermaid">
flowchart TB
    subgraph INPUT["📥 Entrées"]
        URL["URL cible"]
        PARAMS["Paramètres connus"]
        WL["📋 Wordlists"]
    end

    subgraph ENGINE["⚙️ Moteur de Fuzzing"]
        GEN["Générateur de requêtes"]
        INJECT["Injection payloads"]
        SEND["Envoi HTTP"]
    end

    subgraph ANALYSIS["🔍 Analyse"]
        RESP["Analyse réponses"]
        ERR["Détection erreurs SQL"]
        TIME["Analyse timing"]
        DIFF["Comparaison contenu"]
    end

    subgraph OUTPUT["📊 Résultats"]
        VULN["🔴 Vulnérabilités"]
        REPORT["📄 Rapport"]
    end

    URL & PARAMS --> GEN
    WL --> INJECT
    GEN --> INJECT --> SEND
    SEND --> RESP
    RESP --> ERR & TIME & DIFF
    ERR & TIME & DIFF --> VULN --> REPORT

    style VULN fill:#e74c3c,fill-opacity:0.15
    style ENGINE fill:#3498db,fill-opacity:0.15
    style ANALYSIS fill:#f39c12,fill-opacity:0.15
    style OUTPUT fill:#808080,fill-opacity:0.15
    style INPUT fill:#808080,fill-opacity:0.15
</div>

**Les trois méthodes de détection** :
1. **Erreurs SQL** : Le serveur renvoie un message d'erreur révélateur
2. **Timing** : Le serveur met plus de temps à répondre (SQLi time-based)
3. **Différence de contenu** : La page change de manière inattendue (SQLi boolean-based)


## Flux de Détection en Action

Voyons concrètement comment le fuzzer teste une URL et identifie une vulnérabilité. Ce diagramme de séquence montre les échanges entre le fuzzer et l'application cible.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant F as 🔧 Fuzzer
    participant T as 🎯 Cible
    participant À as 📊 Analyseur

    F->>T: GET /search?q=test (baseline)
    T-->>F: 200 OK (normal)

    rect rgb(231, 76, 60, 0.2)
        Note over F,T: Injection de payloads
        F->>T: GET /search?q=' OR '1'='1
        T-->>F: 200 OK (données anormales)
        F->>A: Différence détectée!

        F->>T: GET /search?q=' UNION SELECT--
        T-->>F: 500 Error SQL
        F->>A: Erreur SQL détectée!

        F->>T: GET /search?q='; WAITFOR DELAY '5'--
        T-->>F: Réponse après 5s
        F->>A: Time-based SQLi!
    end

    A->>A: Générer rapport
</div>

**Point important** : Le fuzzer commence par établir une "baseline" (réponse normale) pour pouvoir détecter les différences significatives.


## Les Types d'Injection SQL

Il existe plusieurs techniques d'injection SQL, chacune exploitant un comportement différent de l'application. Le fuzzer sait détecter les quatre types principaux.

<div class="mermaid">
flowchart LR
    subgraph Détection["Types d'Injection SQL"]
        D1["🔴 Error-based<br/>Messages d'erreur SQL"]
        D2["🟠 Boolean-based<br/>Différence de contenu"]
        D3["🟡 Time-based<br/>Délai de réponse"]
        D4["🔵 UNION-based<br/>Extraction de données"]
    end

    subgraph Payloads["Exemples de Payloads"]
        P1["' OR '1'='1"]
        P2["1' AND '1'='2"]
        P3["'; WAITFOR DELAY '5'--"]
        P4["' UNION SELECT NULL--"]
    end

    D1 --> P1
    D2 --> P2
    D3 --> P3
    D4 --> P4

    style D1 fill:#e74c3c,fill-opacity:0.15
    style D2 fill:#f39c12,fill-opacity:0.15
    style D3 fill:#f1c40f,fill-opacity:0.15
    style D4 fill:#3498db,fill-opacity:0.15
    style Payloads fill:#808080,fill-opacity:0.15
    style Détection fill:#808080,fill-opacity:0.15
</div>

### Error-based : La plus simple

L'application affiche l'erreur SQL brute. C'est le signe d'une mauvaise gestion des erreurs et d'une vulnérabilité triviale à exploiter.

### Boolean-based : La plus subtile

Le contenu de la page change selon que la condition injectée est vraie ou fausse. Nécessite une analyse comparative des réponses.

### Time-based : L'aveugle

Aucune différence visible, mais le serveur met plus de temps à répondre. Utile quand toutes les autres méthodes échouent.

### UNION-based : L'extraction directe

Permet de récupérer des données d'autres tables en les ajoutant aux résultats de la requête originale.


## Utilisation du Détecteur

### Configuration de base

```python
from sqli_detector import SQLiDetector

# Configuration du détecteur
detector = SQLiDetector(
    target_url="https://example.com/search",
    params={"q": "test", "page": "1"},
    wordlist="payloads/sql-injection.txt"
)

# Lancer le fuzzing
results = detector.fuzz()

# Afficher les vulnérabilités trouvées
for vuln in results.vulnerabilities:
    print(f"[!] Paramètre vulnérable: {vuln.param}")
    print(f"    Payload: {vuln.payload}")
    print(f"    Type: {vuln.type}")
    print(f"    Evidence: {vuln.evidence}")
```

### Intégration avec d'autrès outils

Le détecteur peut utiliser des paramètres extraits par d'autres outils du projet (comme Python.QueryStringsFromPhp) :

```python
import json

# Charger les paramètres extraits d'une application PHP
with open("results/app-query-strings.json") as f:
    known_params = json.load(f)

# Créer le détecteur avec ces paramètres
detector = SQLiDetector(
    target_url="https://myapp.com/api",
    params=known_params
)

# Le fuzzing testera tous les paramètres connus
results = detector.fuzz()
```


## Indicateurs de Vulnérabilité

Le détecteur recherche des patterns spécifiques dans les réponses pour identifier les vulnérabilités. Voici les principaux indicateurs et leur sévérité.

| Indicateur | Type | Sévérité |
|------------|------|----------|
| `SQL syntax error` | Error-based | 🔴 Critique |
| `mysql_fetch_array()` | Error-based | 🔴 Critique |
| `ORA-01756` | Error-based (Oracle) | 🔴 Critique |
| Différence de contenu > 50% | Boolean-based | 🟠 Haute |
| Délai > 5s (vs baseline < 1s) | Time-based | 🟠 Haute |
| Colonnes UNION visibles | UNION-based | 🔴 Critique |


## Préparer vos Wordlists

Le fuzzer est aussi efficace que ses wordlists. Voici comment télécharger les collections recommandées :

```bash
# Créer le dossier des payloads
mkdir payloads && cd payloads

# Payloads généraux (détection)
curl -O https://raw.githubusercontent.com/payloadbox/sql-injection-payload-list/master/Intruder/detect/Generic_SQLI.txt

# Payloads de contournement d'authentification
curl -O https://raw.githubusercontent.com/payloadbox/sql-injection-payload-list/master/Intruder/exploit/Auth_Bypass.txt

# Wordlist wfuzz (classique)
curl -O https://raw.githubusercontent.com/xmendez/wfuzz/master/wordlist/Injections/SQL.txt
```


## Pour Aller Plus Loin

L'injection SQL est un sujet vaste. Voici des ressources pour approfondir :

- 📚 [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) - Guide de référence
- 🔓 [PortSwigger SQLi Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet) - Techniques avancées
- 📦 [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection) - Collection exhaustive


## Exploits et Vulnérabilités Connues

L'injection SQL a été à l'origine de nombreuses brèches de sécurité majeures. Voici quelques CVE notables :

| CVE | Produit | Description | Score CVSS |
|-----|---------|-------------|------------|
| **CVE-2023-34362** | MOVEit Transfer | Injection SQL permettant l'exécution de code à distance, exploitée massivement par le groupe Cl0p | 9.8 Critique |
| **CVE-2021-27065** | Microsoft Exchange (ProxyLogon) | Chaine d'exploitation incluant une SQLi pour compromettre les serveurs Exchange | 7.8 Élevé |
| **CVE-2019-2725** | Oracle WebLogic | Injection SQL dans le composant Web Services permettant RCE sans authentification | 9.8 Critique |
| **CVE-2017-5638** | Apache Struts | Bien que principalement une RCE, cette vulnérabilité était souvent chaînée avec des SQLi | 10.0 Critique |
| **CVE-2012-2122** | MySQL/MariaDB | Bypass d'authentification par comparaison de mots de passe défaillante (timing attack) | 5.1 Moyen |

Ces vulnérabilités ont touché des millions de systèmes dans le monde. La CVE-2023-34362 (MOVEit) a notamment permis le vol de données de plus de 2000 organisations, incluant des agences gouvernementales et des entreprises du Fortune 500.


## Approfondissement Théorique

### Les mécanismes de protection modernes

La défense en profondeur contre les injections SQL repose sur plusieurs couches complémentaires. Les **requêtes préparées** (prepared statements) constituent la protection principale : en séparant le code SQL des données, elles rendent l'injection structurellement impossible. Les ORM modernes comme SQLAlchemy, Eloquent ou Hibernate implémentent cette protection de manière transparente, mais attention aux fonctions de requête brute qui contournent ces protections.

Les **WAF** (Web Application Firewalls) ajoutent une couche de détection en analysant les requêtes HTTP à la recherche de patterns d'injection connus. Cependant, ils peuvent être contournés par des techniques d'encodage (double URL encoding, unicode, commentaires SQL). Ils ne doivent jamais être considérés comme une protection principale, mais comme une couche supplémentaire de défense.

### La détection par analyse comportementale

Au-delà de la détection par signatures (recherche de patterns comme `' OR 1=1`), les approches modernes utilisent l'**analyse comportementale**. Le principe est de comparer le comportement de l'application face à des entrées normales versus des entrées potentiellement malveillantes. Une différence significative dans le temps de réponse, la taille de la réponse, ou les codes d'erreur peut indiquer une vulnérabilité, même si aucune erreur SQL explicite n'est retournée. Cette technique est particulièrement efficace contre les injections aveugles (blind SQLi) où l'attaquant n'a aucun retour direct de la base de données.


---

