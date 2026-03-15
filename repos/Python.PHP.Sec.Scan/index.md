---
layout: default
title: "Python.PHP.Sec.Scan"
description: "Scanner de Sécurité PHP avec Analyse Statique"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.PHP.Sec.Scan</span>
</div>

<div class="page-header">
  <h1>Python.PHP.Sec.Scan</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.PHP.Sec.Scan" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Scanner de Sécurité PHP avec Analyse Statique

## Introduction : Trouver les Vulnérabilités Avant les Attaquants

PHP reste l'un des langages les plus utilisés sur le web, mais il est aussi réputé pour la facilité avec laquelle on peut introduire des vulnérabilités. Injection SQL, XSS, exécution de code à distance... Ces failles sont souvent le résultat d'une mauvaise gestion des données utilisateur.

Ce scanner utilise l'**analyse statique** pour détecter ces vulnérabilités **sans exécuter le code**. La technique clé est le **taint tracking** : on suit le parcours des données "tainted" (potentiellement malveillantes) depuis leur source (entrées utilisateur) jusqu'à leur utilisation dans des fonctions dangereuses (sinks).

### Ce que ce scanner détecte

| Catégorie | Capacités |
|-----------|-----------|
| **Analyse** | Taint tracking, call graph, parsing AST |
| **Vulnérabilités** | SQLi, XSS, RCE, LFI, Command Injection, Path Traversal, Auth Bypass |
| **WordPress** | Sanitizers WP natifs, hooks, vérification des nonces |
| **Production** | Multi-threading, cache AST, API REST |
| **Export** | SARIF (compatible GitHub Security) |


## Architecture du Scanner

Le scanner analyse le code source PHP en construisant un arbre syntaxique abstrait (AST), puis suit le flux des données pour détecter les chemins dangereux.

<div class="mermaid">
flowchart TB
    subgraph INPUT["📂 Code PHP"]
        PHP["*.php files"]
        WP["WordPress plugins"]
    end

    subgraph ENGINE["⚙️ Analyse Engine"]
        AST["AST Parser"]
        TAINT["Taint Tracker"]
        CALL["Call Graph"]
        RULES["YAML Rules"]
    end

    subgraph DETECTION["🔍 Détection"]
        SQLi["SQL Injection"]
        XSS["Cross-Site Scripting"]
        RCE["Remote Code Execution"]
        LFI["Local File Inclusion"]
        CMDi["Command Injection"]
        PATH["Path Traversal"]
        AUTH["Auth Bypass"]
    end

    subgraph OUTPUT["📊 Résultats"]
        SARIF["SARIF Export"]
        HTML["HTML Report"]
        DB["SQLite/PostgreSQL"]
    end

    INPUT --> ENGINE
    AST --> TAINT --> CALL
    RULES --> DETECTION
    ENGINE --> DETECTION --> OUTPUT

    style SQLi fill:#e74c3c,fill-opacity:0.15
    style XSS fill:#e74c3c,fill-opacity:0.15
    style RCE fill:#e74c3c,fill-opacity:0.15
    style OUTPUT fill:#808080,fill-opacity:0.15
    style DETECTION fill:#808080,fill-opacity:0.15
    style ENGINE fill:#808080,fill-opacity:0.15
    style INPUT fill:#808080,fill-opacity:0.15
</div>


## Le Taint Tracking Expliqué

Le taint tracking est au cœur du scanner. Le principe : toute donnée provenant de l'utilisateur est "tainted" (contaminée). Si cette donnée atteint une fonction dangèreuse sans être nettoyée, c'est une vulnérabilité.

<div class="mermaid">
flowchart LR
    subgraph Sources["🔴 Sources (Données Tainted)"]
        S1["$_GET"]
        S2["$_POST"]
        S3["$_REQUEST"]
        S4["$_COOKIE"]
        S5["$_FILES"]
    end

    subgraph Flow["➡️ Flux de données"]
        V1["$user = $_GET['id']"]
        V2["$query = 'SELECT * FROM users WHERE id=' . $user"]
    end

    subgraph Sinks["💀 Sinks (Fonctions Dangèreuses)"]
        K1["mysql_query()"]
        K2["mysqli_query()"]
        K3["PDO::query()"]
    end

    subgraph Sanitizers["✅ Sanitizers (Nettoyage)"]
        SAN1["mysqli_real_escape_string()"]
        SAN2["PDO::prepare()"]
        SAN3["intval()"]
    end

    S1 --> V1 --> V2 --> K1
    V2 -.->|"sanitize"| SAN1 -.-> K1

    style S1 fill:#e74c3c,fill-opacity:0.15
    style K1 fill:#e74c3c,fill-opacity:0.15
    style SAN1 fill:#2ecc71,fill-opacity:0.15
    style Sanitizers fill:#808080,fill-opacity:0.15
    style Sinks fill:#808080,fill-opacity:0.15
    style Flow fill:#808080,fill-opacity:0.15
    style Sources fill:#808080,fill-opacity:0.15
</div>

**Lecture du diagramme** :
1. `$_GET['id']` est une source tainted (entrée utilisateur)
2. La variable `$user` devient tainted par propagation
3. `$query` contient des données tainted concaténées
4. `mysql_query()` est un sink dangereux
5. **Sans sanitizer** : VULNÉRABILITÉ SQL INJECTION !


## Utilisation

```bash
# Installation des dépendances
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Initialiser la base de données des résultats
python cli.py --init-db

# Scanner un projet PHP
python cli.py scan /path/to/php/project

# Scanner avec export SARIF pour GitHub
python cli.py scan /path/to/project --output results.sarif

# Démarrer l'API REST
python cli.py serve --port 8000
```


## Règles YAML Personnalisées

Vous pouvez définir vos propres règles de détection en YAML. Cela permet d'adapter le scanner aux conventions de votre entreprise.

```yaml
# rules/custom/company-rules.yaml
rules:
  - id: CUSTOM-001
    name: Unsafe Database Query
    severity: critical
    pattern: |
      mysql_query($QUERY)
    where:
      - $QUERY.isTainted()
    message: "SQL injection vulnerability detected"
    fix: "Use prepared statements with PDO"

  - id: CUSTOM-002
    name: Missing CSRF Token
    severity: high
    pattern: |
      if ($_POST['action'] == 'delete')
    where:
      - not exists: check_admin_referer()
    message: "CSRF protection missing on destructive action"
```


## Support WordPress Avancé

WordPress a ses propres conventions de sécurité. Le scanner les comprend et vérifie leur utilisation correcte.

<div class="mermaid">
flowchart TB
    subgraph WP_Sources["🔴 Sources WordPress"]
        WS1["get_query_var()"]
        WS2["$_GET / $_POST"]
        WS3["get_option()"]
    end

    subgraph WP_Sanitizers["✅ Sanitizers WordPress"]
        WSA1["esc_html()"]
        WSA2["esc_attr()"]
        WSA3["esc_sql()"]
        WSA4["wp_kses()"]
        WSA5["sanitize_text_field()"]
    end

    subgraph WP_Security["🔐 Vérifications de Sécurité"]
        SEC1["wp_nonce_field()"]
        SEC2["check_admin_referer()"]
        SEC3["current_user_can()"]
    end

    WS1 & WS2 --> WSA1 & WSA2 & WSA3
    WP_Security --> SEC1 & SEC2 & SEC3

    style WSA1 fill:#2ecc71,fill-opacity:0.15
    style WSA2 fill:#2ecc71,fill-opacity:0.15
    style SEC1 fill:#3498db,fill-opacity:0.15
    style WP_Security fill:#808080,fill-opacity:0.15
    style WP_Sanitizers fill:#808080,fill-opacity:0.15
    style WP_Sources fill:#808080,fill-opacity:0.15
</div>

### Exemple de code WordPress sécurisé

Le scanner vérifie que ces bonnes pratiques sont respectées :

```php
<?php
// ✅ Vérification du nonce CSRF
if (!wp_verify_nonce($_POST['_wpnonce'], 'delete_action')) {
    wp_die('Security check failed');
}

// ✅ Vérification des permissions
if (!current_user_can('delete_posts')) {
    wp_die('Unauthorized');
}

// ✅ Sanitization de l'entrée utilisateur
$post_id = intval($_POST['post_id']);

// ✅ Requête préparée
$wpdb->delete('posts', ['ID' => $post_id], ['%d']);
```


## Intégration CI/CD

Intégrez le scanner dans votre pipeline pour bloquer les déploiements avec des vulnérabilités critiques :

```yaml
# .github/workflows/php-security.yml
name: PHP Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - name: PHP Security Scan
        run: |
          python cli.py scan ./src \
            --output sarif/results.sarif \
            --fail-on high

      - name: Upload SARIF to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: sarif/results.sarif
```


## Pour Aller Plus Loin

- 📚 [OWASP PHP Security](https://cheatsheetseries.owasp.org/cheatsheets/PHP_Configuration_Cheat_Sheet.html) - Bonnes pratiques
- 🔒 [WordPress Security](https://developer.wordpress.org/plugins/security/) - Guide officiel
- 📄 [Spécification SARIF](https://sarifweb.azurewebsites.net/) - Format de rapport standard


## Exploits et Vulnérabilités Connues

Les vulnérabilités PHP sont parmi les plus documentées. Voici des CVE majeures illustrant les types de failles détectables par ce scanner :

- **CVE-2024-4577 (PHP-CGI)** : Injection d'arguments via le paramètre php-cgi sous Windows permettant RCE. Cette vulnérabilité de type command injection est exactement le pattern détecté par l'analyse taint tracking sur les fonctions system/exec/passthru.

- **CVE-2019-11043 (PHP-FPM)** : Buffer underflow dans PHP-FPM permettant RCE via manipulation d'URL. Bien que côté serveur, les applications PHP appelant des URLs dynamiques avec des données utilisateur non sanitisées peuvent déclencher cette faille.

- **CVE-2021-21389 (WordPress)** : Vulnérabilité d'injection SQL dans le plugin BuddyPress. Illustre l'importance de vérifier l'utilisation correcte de $wpdb->prepare() que ce scanner détecte.

- **CVE-2022-21661 (WordPress Core)** : SQL injection dans WP_Query. Les paramètres non sanitisés passés aux fonctions WordPress peuvent mener à des injections SQL même via les APIs officielles.

- **CVE-2023-2982 (WordPress Plugin)** : Vulnérabilité d'upload de fichier dans un plugin permettant RCE. Le scanner détecte les utilisations dangereuses de move_uploaded_file() sans validation du type de fichier.


## Approfondissement Théorique

L'analyse statique de code (SAST - Static Application Security Testing) repose sur l'examen du code source sans exécution. Contrairement au fuzzing ou au pentesting (DAST), elle permet d'identifier les vulnérabilités avant même le déploiement. Le taint tracking, technique centrale de ce scanner, modélise le flux de données à travers le programme en marquant les entrées utilisateur comme "tainted" et en traçant leur propagation jusqu'aux fonctions sensibles (sinks).

La construction de l'AST (Abstract Syntax Tree) est la première étape de l'analyse. L'AST représente la structure syntaxique du code de manière indépendante de sa représentation textuelle. Pour PHP, des parseurs comme php-parser (en PHP) ou tree-sitter (multi-langage) permettent de générer cet arbre. L'analyse de flux de données (dataflow analysis) parcourt ensuite l'AST pour suivre les variables et leurs transformations. La difficulté majeure réside dans l'analyse inter-procédurale : suivre les données à travers les appels de fonctions, ce qui nécessite la construction d'un call graph.

Les faux positifs sont le défi principal de l'analyse statique. Un scanner trop sensible générera des alertes sur du code sécurisé (sanitizers non reconnus, logique de validation complexe), tandis qu'un scanner trop permissif manquera des vulnérabilités réelles. L'approche optimale combine des règles génériques avec des règles spécifiques au framework (WordPress, Laravel, Symfony) qui reconnaissent les patterns de sanitization propres à chaque écosystème. L'intégration CI/CD avec un seuil de sévérité configurable permet de bloquer uniquement les vulnérabilités critiques confirmées tout en loggant les alertes mineures pour revue manuelle.


---

