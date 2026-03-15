---
layout: default
title: "Python.QueryStringsFromPhp"
description: "Extracteur de Query Strings et SQL depuis PHP"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.QueryStringsFromPhp</span>
</div>

<div class="page-header">
  <h1>Python.QueryStringsFromPhp</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.QueryStringsFromPhp" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Extracteur de Query Strings et SQL depuis PHP

## Introduction : Cartographier la Surface d'Attaque

Avant de tester une application web pour des vulnérabilités, il faut d'abord savoir **quels paramètres elle accepte**. Chaque `$_GET['param']`, `$_POST['field']`, ou variable dans une requête SQL est un point d'entrée potentiel pour une injection.

Cet outil analyse statiquement le code source PHP pour extraire automatiquement :
- Tous les **paramètres d'entrée utilisateur** (`$_GET`, `$_POST`, `$_REQUEST`, `$_COOKIE`)
- Toutes les **requêtes SQL** avec leur risque potentiel d'injection

Le résultat est exporté en JSON, prêt à être utilisé pour le fuzzing ou la documentation.

### Cas d'utilisation

| Usage | Description |
|-------|-------------|
| **Audit de sécurité** | Identifier tous les points d'entrée utilisateur |
| **Fuzzing** | Générer des wordlists de paramètres à tester |
| **Documentation** | Inventorier les endpoints d'une API |
| **Préparation SQLi** | Localiser les requêtes SQL potentiellement vulnérables |


## Architecture de l'Extracteur

L'outil parcourt récursivement tous les fichiers PHP du projet, applique des expressions régulières pour détecter les patterns recherchés, puis exporte les résultats dédupliqués en JSON.

<div class="mermaid">
flowchart TB
    subgraph INPUT["📂 Code PHP"]
        PHP["*.php files"]
        DIR["Répertoire projet"]
    end

    subgraph ENGINE["⚙️ Extracteur"]
        PARSE["Parser PHP"]
        REGEX["Regex Extraction"]
        SQL["SQL Détection"]
        QS["Query String Détection"]
    end

    subgraph OUTPUT["📊 Résultats JSON"]
        O1["query-strings.json"]
        O2["sql-queries.json"]
        O3["paramètres.json"]
    end

    INPUT --> ENGINE
    PARSE --> REGEX --> SQL & QS
    SQL & QS --> OUTPUT

    style ENGINE fill:#3498db,fill-opacity:0.15
    style OUTPUT fill:#2ecc71,fill-opacity:0.15
    style INPUT fill:#808080,fill-opacity:0.15
</div>


## Flux d'Extraction en Détail

<div class="mermaid">
sequenceDiagram
    autonumber
    participant P as 📂 PHP Files
    participant E as ⚙️ Extractor
    participant Q as 🔍 Query Analyzer
    participant J as 📄 JSON

    E->>P: Parcourir fichiers PHP
    P-->>E: Contenu source

    loop Pour chaque fichier
        E->>E: Regex $_GET, $_POST, $_REQUEST
        E->>E: Regex requêtes SQL
        E->>Q: Paramètres extraits
    end

    Q->>Q: Dédupliquer les résultats
    Q->>Q: Classifier par type/risque
    Q->>J: Export JSON structuré
</div>


## Patterns Détectés

L'extracteur reconnaît les différentes sources de données utilisateur en PHP, ainsi que les requêtes SQL qui pourraient être vulnérables.

<div class="mermaid">
flowchart LR
    subgraph Sources["🔴 Sources de Données Utilisateur"]
        S1["$_GET['param']"]
        S2["$_POST['param']"]
        S3["$_REQUEST['param']"]
        S4["$_COOKIE['param']"]
        S5["$_SERVER['QUERY_STRING']"]
    end

    subgraph SQL["📊 Requêtes SQL"]
        Q1["SELECT ... FROM"]
        Q2["INSERT INTO"]
        Q3["UPDATE ... SET"]
        Q4["DELETE FROM"]
    end

    subgraph Output["📄 Export JSON"]
        JSON["results/*.json"]
    end

    Sources --> Output
    SQL --> Output

    style S1 fill:#e74c3c,fill-opacity:0.15
    style S2 fill:#e74c3c,fill-opacity:0.15
    style Q1 fill:#f39c12,fill-opacity:0.15
    style Output fill:#808080,fill-opacity:0.15
    style SQL fill:#808080,fill-opacity:0.15
    style Sources fill:#808080,fill-opacity:0.15
</div>


## Utilisation

```python
# main.py
from Configuration import Config
from QueryStrings import QueryStringExtractor

# Configuration : répertoire source et destination
config = Config(
    source_dir='/path/to/php/project',
    output_dir='results/'
)

# Lancer l'extraction
extractor = QueryStringExtractor(config)
results = extractor.extract()

# Afficher les statistiques
print(f"Fichiers analysés : {results.files_scanned}")
print(f"Paramètres GET : {len(results.get_params)}")
print(f"Paramètres POST : {len(results.post_params)}")
print(f"Requêtes SQL : {len(results.sql_queries)}")

# Exporter en JSON
extractor.export_json('query-strings.json')
```


## Structure du Projet

```
Python.QueryStringsFromPhp/
├── main.py                 # Point d'entrée
├── Configuration.py        # Chemins et paramètres
├── MagicStrings.py         # Constantes et patterns regex
├── QueryStrings.py         # Logique d'extraction
├── requirements.txt        # Dépendances Python
└── results/
    ├── query-strings.json  # Paramètres extraits
    ├── sql-queries.json    # Requêtes SQL trouvées
    └── paramètres.json     # Inventaire complet
```


## Exemple de Sortie JSON

Voici la structure du fichier JSON généré :

```json
{
  "project": "my-php-app",
  "extracted_at": "2026-03-14T14:30:00Z",
  "query_strings": [
    {
      "file": "api/users.php",
      "line": 15,
      "type": "GET",
      "paramètre": "user_id",
      "context": "$_GET['user_id']"
    },
    {
      "file": "api/search.php",
      "line": 23,
      "type": "POST",
      "paramètre": "query",
      "context": "$_POST['query']"
    }
  ],
  "sql_queries": [
    {
      "file": "models/User.php",
      "line": 45,
      "query": "SELECT * FROM users WHERE id = $id",
      "risk": "potential_sqli",
      "reason": "Variable non échappée dans la requête"
    }
  ],
  "statistics": {
    "files_scanned": 127,
    "get_params": 45,
    "post_params": 32,
    "sql_queries": 89
  }
}
```


## Patterns Regex Utilisés

Le fichier `MagicStrings.py` contient les expressions régulières pour la détection :

```python
# MagicStrings.py

# Patterns pour les query strings
GET_PATTERN = r"\$_GET\s*\[\s*['\"]([^'\"]+)['\"]\s*\]"
POST_PATTERN = r"\$_POST\s*\[\s*['\"]([^'\"]+)['\"]\s*\]"
REQUEST_PATTERN = r"\$_REQUEST\s*\[\s*['\"]([^'\"]+)['\"]\s*\]"
COOKIE_PATTERN = r"\$_COOKIE\s*\[\s*['\"]([^'\"]+)['\"]\s*\]"

# Patterns pour les requêtes SQL
SQL_SELECT = r"SELECT\s+.+?\s+FROM\s+\w+"
SQL_INSERT = r"INSERT\s+INTO\s+\w+"
SQL_UPDATE = r"UPDATE\s+\w+\s+SET"
SQL_DELETE = r"DELETE\s+FROM\s+\w+"
```


## Intégration avec les Tests de Sécurité

Une fois les paramètres extraits, vous pouvez les utiliser pour le fuzzing automatisé :

```python
import json
import requests

# Charger les paramètres extraits
with open('results/query-strings.json') as f:
    data = json.load(f)

# Payloads de test SQLi
sqli_payloads = ["'", "1 OR 1=1", "'; DROP TABLE--", "1' AND '1'='1"]

# Tester chaque paramètre GET
for param in data['query_strings']:
    if param['type'] == 'GET':
        for payload in sqli_payloads:
            url = f"https://target.com/api?{param['paramètre']}={payload}"
            response = requests.get(url)

            # Analyser la réponse pour détecter SQLi
            if "SQL syntax" in response.text or "mysql" in response.text.lower():
                print(f"[!] SQLi potentielle sur {param['paramètre']}")
                print(f"    Payload: {payload}")
                print(f"    Fichier: {param['file']}:{param['line']}")
```


## Pour Aller Plus Loin

- 📚 [OWASP Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) - Bonnes pratiques
- 🐘 [PHP Superglobals](https://www.php.net/manual/en/language.variables.superglobals.php) - Documentation officielle


## Exploits et Vulnérabilités Connues

L'extraction de paramètres et requêtes SQL permet d'identifier des patterns vulnérables similaires à ceux exploités dans des CVE réelles :

- **CVE-2024-2961 (GNU C Library iconv)** : Bien que non spécifique à PHP, cette vulnérabilité de buffer overflow peut être déclenchée via des paramètres utilisateur mal sanitisés passés aux fonctions de conversion d'encodage. L'extraction de paramètres permet d'identifier ces points d'entrée.

- **CVE-2023-6875 (POST SMTP WordPress)** : Injection SQL via le paramètre $_GET['log']. L'extraction automatique de tous les paramètres GET aurait révélé ce point d'entrée vulnérable, permettant une détection précoce.

- **CVE-2022-4510 (Jeecg Boot)** : Injection SQL dans plusieurs paramètres non sanitisés. Un extracteur de query strings aurait généré la liste complète des paramètres à auditer.

- **CVE-2021-29447 (WordPress XXE)** : Bien que XXE, la vulnérabilité est déclenchée via upload de fichier ($_FILES). L'extraction de toutes les sources de données utilisateur inclut ces vecteurs.

- **CVE-2020-7919 (Joomla SQLi)** : Injection SQL via le paramètre $_REQUEST['id'] dans le composant com_tags. La détection de concatenation directe de $_REQUEST dans des requêtes SQL aurait signalé ce risque.


## Approfondissement Théorique

L'extraction de paramètres et requêtes SQL constitue la première étape de l'analyse de surface d'attaque (Attack Surface Analysis). Cette méthodologie, formalisée par l'OWASP, vise à identifier tous les points d'entrée potentiels d'une application avant de procéder aux tests de pénétration. En contexte PHP, les superglobales ($_GET, $_POST, $_REQUEST, $_COOKIE, $_FILES, $_SERVER) représentent les principales sources de données non fiables (untrusted input).

L'analyse par expressions régulières (regex-based analysis) présente des avantages et limites. L'avantage principal est la rapidité : parcourir des milliers de fichiers PHP prend quelques secondes. La limite est la précision : les regex ne comprennent pas la sémantique du code. Un paramètre $_GET['id'] passé à intval() puis utilisé dans une requête préparée est sécurisé, mais l'extraction regex le signalera quand même. Cette limitation est acceptable car l'objectif est de minimiser les faux négatifs (vulnérabilités non détectées) quitte à avoir des faux positifs qui seront éliminés lors de l'analyse manuelle.

L'intégration avec les outils de fuzzing automatisé (Burp Suite, OWASP ZAP, ffuf) transforme la sortie JSON de l'extracteur en wordlist de paramètres. Le fuzzing consiste à envoyer des payloads malveillants sur chaque paramètre et à analyser les réponses pour détecter des comportements anormaux (messages d'erreur SQL, stack traces, délais de réponse). La corrélation entre les paramètres extraits du code source et leur comportement à l'exécution permet d'identifier avec précision les vulnérabilités exploitables. Cette approche hybride SAST+DAST (Static + Dynamic Analysis) maximise la couverture de détection.


---

