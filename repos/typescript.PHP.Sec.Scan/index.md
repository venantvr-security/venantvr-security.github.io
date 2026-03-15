---
layout: default
title: "typescript.PHP.Sec.Scan"
description: "Extension VS Code - Scanner de Sécurité PHP"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>typescript.PHP.Sec.Scan</span>
</div>

<div class="page-header">
  <h1>typescript.PHP.Sec.Scan</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/typescript.PHP.Sec.Scan" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Extension VS Code - Scanner de Sécurité PHP

## Introduction : Détecter les Vulnérabilités Dès l'Écriture du Code

Les vulnérabilités de sécurité les plus courantes — injections SQL, XSS, RCE — sont souvent introduites par inadvertance lors du développement. Et si votre éditeur de code pouvait les détecter en temps réel, avant même que vous ne sauvegardiez le fichier ?

Cette extension **Visual Studio Code** analyse votre code PHP pendant que vous l'écrivez. Elle utilise le **taint tracking** (suivi de contamination) pour tracer le flux des données utilisateur depuis leur source (`$_GET`, `$_POST`) jusqu'aux fonctions dangereuses (`mysql_query`, `echo`, `eval`).

### Ce que cette extension permet de faire

| Fonctionnalité | Description |
|----------------|-------------|
| **Détection temps réel** | Analyse pendant la frappe |
| **Taint tracking** | Suivi des données utilisateur |
| **Quick Fixes** | Corrections automatiques proposées |
| **Règles YAML** | Configuration personnalisable |
| **AST Analysis** | Parsing précis avec tree-sitter |

### Vulnérabilités détectées

L'extension couvre les principales vulnérabilités OWASP :

| Type | Sévérité | Exemple de code vulnérable |
|------|----------|---------------------------|
| **SQL Injection** | 🔴 Critique | `mysql_query($_GET['id'])` |
| **XSS** | 🔴 Critique | `echo $_POST['name']` |
| **RCE** | 🔴 Critique | `eval($_REQUEST['code'])` |
| **File Inclusion** | 🟠 Élevé | `include $_GET['page']` |
| **Auth Bypass** | 🟠 Élevé | `if ($pass == $input)` |
| **Session Fixation** | 🟡 Moyen | Sans `session_regenerate_id()` |


## Architecture de l'Extension

L'extension s'intègre profondément dans VS Code pour offrir une expérience fluide. Le diagramme ci-dessous illustre comment les différents composants interagissent pour analyser votre code en temps réel.

<div class="mermaid">
flowchart TB
    subgraph VSCODE["📝 VS Code"]
        EDITOR["Éditeur PHP<br/><i>Votre code</i>"]
        DIAG["Panneau Problèmes<br/><i>Liste des erreurs</i>"]
        QUICK["Quick Fixes<br/><i>Corrections suggérées</i>"]
    end

    subgraph EXTENSION["🔌 Extension TypeScript"]
        PARSER["tree-sitter-php<br/><i>Parser AST</i>"]
        TAINT["Taint Tracker<br/><i>Analyse du flux de données</i>"]
        RULES["rules.yaml<br/><i>Définition des patterns</i>"]
    end

    subgraph OUTPUT["📊 Résultats"]
        WARN["⚠️ Warnings<br/><i>Risques potentiels</i>"]
        ERR["❌ Errors<br/><i>Vulnérabilités confirmées</i>"]
        FIX["💡 Corrections<br/><i>Code sécurisé</i>"]
    end

    EDITOR -->|"onChange"| PARSER
    PARSER -->|"AST"| TAINT
    RULES -->|"patterns"| TAINT
    TAINT --> WARN & ERR
    WARN & ERR --> DIAG
    FIX --> QUICK

    style ERR fill:#e74c3c,fill-opacity:0.15
    style WARN fill:#f39c12,fill-opacity:0.15
    style FIX fill:#2ecc71,fill-opacity:0.15
    style TAINT fill:#3498db,fill-opacity:0.15
    style OUTPUT fill:#808080,fill-opacity:0.15
    style EXTENSION fill:#808080,fill-opacity:0.15
    style VSCODE fill:#808080,fill-opacity:0.15
</div>


## Flux d'Analyse en Détail

Comprendre comment l'extension analyse votre code vous aidera à mieux interpréter ses diagnostics. Le diagramme de séquence suivant montre le processus complet, de la modification du fichier à l'affichage de l'alerte.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant E as 📝 Éditeur
    participant P as 🌳 tree-sitter
    participant T as 🔍 Taint Tracker
    participant D as 📊 Diagnostics

    Note over E,D: L'utilisateur modifie le code PHP
    E->>P: Fichier PHP modifié
    P->>P: Construire l'AST (Abstract Syntax Tree)
    P->>T: Transmettre les nœuds AST

    Note over T: Analyse du flux de données
    loop Pour chaque source de données utilisateur
        T->>T: Identifier les sources ($_GET, $_POST...)
        T->>T: Tracer le flux de données
        T->>T: Vérifier si le flux atteint un sink dangereux
    end

    alt Vulnérabilité détectée
        T->>D: Créer un diagnostic
        D->>D: Déterminer sévérité et message
        D->>E: Afficher erreur avec soulignement rouge
        Note over E: L'utilisateur voit l'alerte immédiatement
    else Code sécurisé (sanitizer détecté)
        T->>D: Aucun problème
        Note over E: Pas d'alerte
    end
</div>

### Le concept de Taint Tracking

Le **taint tracking** (suivi de contamination) est une technique d'analyse statique qui :

1. **Identifie les sources** : Les données venant de l'utilisateur (`$_GET`, `$_POST`, `$_REQUEST`, `$_COOKIE`)
2. **Trace la propagation** : Suit ces données à travers les variables et fonctions
3. **Détecte les sinks** : Repère quand ces données atteignent une fonction dangèreuse
4. **Reconnaît les sanitizers** : Comprend que `htmlspecialchars()` neutralise les XSS


## Installation et Configuration

L'extension se compile facilement depuis les sources.

```bash
# Cloner le projet
git clone https://github.com/venantvr-security/typescript.PHP.Sec.Scan.git
cd typescript.PHP.Sec.Scan

# Installer les dépendances npm
npm install

# Compiler l'extension TypeScript
npm run compile

# Pour lancer en mode développement :
# 1. Ouvrir le projet dans VS Code
# 2. Appuyer sur F5 pour lancer une nouvelle fenêtre VS Code
#    avec l'extension chargée
```

### Configuration dans VS Code

Personnalisez le comportement de l'extension via les paramètres :

```json
// .vscode/settings.json
{
    // Activer/désactiver l'extension
    "phpSecurityScanner.enable": true,

    // Analyser automatiquement à chaque sauvegarde
    "phpSecurityScanner.autoScanOnSave": true,

    // Configurer la sévérité de chaque type de vulnérabilité
    "phpSecurityScanner.severity": {
        "sqlInjection": "error",      // Erreur bloquante
        "xss": "error",               // Erreur bloquante
        "rce": "error",               // Erreur bloquante
        "fileInclusion": "warning",   // Avertissement
        "authBypass": "warning"       // Avertissement
    },

    // Chemin vers un fichier de règles personnalisé
    "phpSecurityScanner.rulesPath": "./rules.yaml"
}
```


## Définition des Règles YAML

Les règles de détection sont définies dans un fichier YAML facilement modifiable. Cela permet d'adapter l'analyse à votre contexte spécifique.

```yaml
# rules.yaml - Définition des patterns de sécurité

# ═══════════════════════════════════════════════════════
# SOURCES : D'où viennent les données utilisateur ?
# ═══════════════════════════════════════════════════════
sources:
  - pattern: "$_GET"
    taint: user_input
    description: "Données GET (URL paramètres)"

  - pattern: "$_POST"
    taint: user_input
    description: "Données POST (formulaires)"

  - pattern: "$_REQUEST"
    taint: user_input
    description: "Combinaison GET/POST/COOKIE"

  - pattern: "$_COOKIE"
    taint: user_input
    description: "Cookies (manipulables côté client)"

# ═══════════════════════════════════════════════════════
# SINKS : Où les données deviennent-elles dangereuses ?
# ═══════════════════════════════════════════════════════
sinks:
  - pattern: "mysql_query($query)"
    vulnerability: sql_injection
    message: "Injection SQL potentielle - utilisez des requêtes préparées"
    severity: critical
    cwe: "CWE-89"

  - pattern: "echo $var"
    vulnerability: xss
    message: "XSS potentiel - échappez avec htmlspecialchars()"
    severity: critical
    cwe: "CWE-79"

  - pattern: "eval($code)"
    vulnerability: rce
    message: "Exécution de code arbitraire - jamais avec des données utilisateur"
    severity: critical
    cwe: "CWE-94"

  - pattern: "include($file)"
    vulnerability: file_inclusion
    message: "Inclusion de fichier dynamique - vérifiez la whitelist"
    severity: high
    cwe: "CWE-98"

# ═══════════════════════════════════════════════════════
# SANITIZERS : Comment neutraliser les données ?
# ═══════════════════════════════════════════════════════
sanitizers:
  # Contre XSS
  - pattern: "htmlspecialchars($var)"
    removes: xss
    description: "Échappe les caractères HTML"

  # Contre SQL Injection
  - pattern: "mysqli_real_escape_string($conn, $var)"
    removes: sql_injection
    description: "Échappe pour MySQL (préférer les prepared statements)"

  - pattern: "intval($var)"
    removes: sql_injection
    description: "Convertit en entier"

  # Validation de type
  - pattern: "is_numeric($var)"
    removes: sql_injection
    description: "Vérifie que c'est un nombre"
```


## Exemples de Quick Fixes

L'extension propose des corrections automatiques. Le diagramme suivant illustre les transformations appliquées.

<div class="mermaid">
flowchart LR
    subgraph Problem["❌ Code Vulnérable"]
        P1["echo $_GET['name']"]
        P2["$pass == $input"]
        P3["mysql_query($sql)"]
    end

    subgraph Fix["✅ Code Corrigé"]
        F1["echo htmlspecialchars($_GET['name'], ENT_QUOTES, 'UTF-8')"]
        F2["$pass === $input"]
        F3["$pdo->prepare($sql)"]
    end

    P1 -->|"Quick Fix XSS"| F1
    P2 -->|"Quick Fix Auth"| F2
    P3 -->|"Quick Fix SQLi"| F3

    style P1 fill:#e74c3c,fill-opacity:0.15
    style P2 fill:#e74c3c,fill-opacity:0.15
    style P3 fill:#e74c3c,fill-opacity:0.15
    style F1 fill:#2ecc71,fill-opacity:0.15
    style F2 fill:#2ecc71,fill-opacity:0.15
    style F3 fill:#2ecc71,fill-opacity:0.15
    style Fix fill:#808080,fill-opacity:0.15
    style Problem fill:#808080,fill-opacity:0.15
</div>


## Exemples de Détection

Voici des exemples concrets de code analysé par l'extension.

```php
<?php
// ═══════════════════════════════════════════════════════
// EXEMPLE 1 : XSS (Cross-Site Scripting)
// ═══════════════════════════════════════════════════════

// ❌ VULNÉRABLE - Les données utilisateur sont affichées directement
$name = $_GET['name'];
echo "Hello, $name";
// → Diagnostic: "XSS potentiel - échappez avec htmlspecialchars()"

// ✅ SÉCURISÉ - Avec échappement HTML
$name = htmlspecialchars($_GET['name'], ENT_QUOTES, 'UTF-8');
echo "Hello, $name";
// → Pas de diagnostic (sanitizer reconnu)


// ═══════════════════════════════════════════════════════
// EXEMPLE 2 : SQL Injection
// ═══════════════════════════════════════════════════════

// ❌ VULNÉRABLE - Concaténation directe dans la requête
$id = $_GET['id'];
$result = mysql_query("SELECT * FROM users WHERE id = $id");
// → Diagnostic: "Injection SQL potentielle - utilisez des requêtes préparées"

// ✅ SÉCURISÉ - Avec prepared statement
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$_GET['id']]);
// → Pas de diagnostic (le paramètre est isolé de la requête)


// ═══════════════════════════════════════════════════════
// EXEMPLE 3 : Comparaison lâche (Type Juggling)
// ═══════════════════════════════════════════════════════

// ❌ VULNÉRABLE - Comparaison lâche peut être contournée
// En PHP: "0" == 0 == false, ce qui peut permettre des bypasses
if ($password == $user_input) {
    login();
}
// → Diagnostic: "Utilisez une comparaison stricte (===)"

// ✅ SÉCURISÉ - Comparaison stricte
if ($password === $user_input) {
    login();
}
// → Pas de diagnostic


// ═══════════════════════════════════════════════════════
// EXEMPLE 4 : Inclusion de fichier
// ═══════════════════════════════════════════════════════

// ❌ VULNÉRABLE - L'utilisateur contrôle le fichier inclus
include $_GET['page'] . '.php';
// → Diagnostic: "Inclusion de fichier dynamique - vérifiez la whitelist"
// Attaque possible: ?page=../../../etc/passwd%00

// ✅ SÉCURISÉ - Avec whitelist
$allowed = ['home', 'about', 'contact'];
$page = $_GET['page'];
if (in_array($page, $allowed)) {
    include $page . '.php';
}
// → Pas de diagnostic (la validation est détectée)
```


## Prérequis Techniques

| Composant | Version minimale | Notes |
|-----------|------------------|-------|
| **VS Code** | 1.85.0+ | Extension API v1.85+ requise |
| **Node.js** | 16.x ou 18.x | Pour la compilation |
| **TypeScript** | 5.4.5 | Langage de l'extension |
| **tree-sitter-php** | Latest | Parser AST PHP |


## Pour Aller Plus Loin

L'analyse statique de sécurité est un domaine riche. Voici des ressources pour approfondir :

- 🌳 [tree-sitter](https://tree-sitter.github.io/) - Le système de parsing utilisé
- 📦 [tree-sitter-php](https://github.com/tree-sitter/tree-sitter-php) - Grammaire PHP spécifique
- 🔌 [VS Code Extension API](https://code.visualstudio.com/api) - Documentation officielle
- 🛡️ [OWASP PHP Security](https://cheatsheetséries.owasp.org/cheatsheets/PHP_Configuration_Cheat_Sheet.html) - Bonnes pratiques PHP
- 📚 [CWE Database](https://cwe.mitre.org/) - Catalogue des faiblesses logicielles


## Exploits et Vulnérabilités Connues

PHP a été affecté par de nombreuses vulnérabilités critiques au fil des années :

| CVE | Composant | Description | Score CVSS |
|-----|-----------|-------------|------------|
| **CVE-2024-4577** | PHP CGI (Windows) | Injection d'arguments via query strings permettant RCE sur Windows avec locales chinoise/japonaise | 9.8 Critique |
| **CVE-2023-3824** | PHP phar | Buffer overflow lors du chargement de fichiers phar malformés | 9.4 Critique |
| **CVE-2022-31626** | PHP mysqlnd | Buffer overflow dans le driver MySQL natif permettant RCE | 9.8 Critique |
| **CVE-2019-11043** | PHP-FPM (NGINX) | Remote code exécution via manipulation du chemin SCRIPT_FILENAME | 9.8 Critique |
| **CVE-2012-1823** | PHP CGI | Injection de paramètres CGI permettant l'exécution de code arbitraire | 7.5 Élevé |

La vulnérabilité **CVE-2024-4577** est particulièrement notable car elle a affecté des configurations par défaut de PHP sur Windows, permettant l'exécution de code sans authentification via une simple requête HTTP.


## Approfondissement Théorique

### Les limites de l'analyse statique

L'analyse statique de sécurité, bien que puissante, présente des limitations inhérentes. Le **problème de l'arrêt** (halting problem) implique qu'il est mathématiquement impossible de prédire parfaitement le comportement de tout programme. En conséquence, les outils d'analyse statique font face à un compromis entre **faux positifs** (alertes sur du code sécurisé) et **faux négatifs** (vulnérabilités non détectées). Les constructions dynamiques de PHP comme `$$variable`, `call_user_func()`, et l'inclusion de fichiers via variables rendent le suivi du flux de données particulièrement complexe. Les frameworks modernes comme Laravel ou Symfony ajoutent des couches d'abstraction qui peuvent masquer les patterns de sécurité aux analyseurs simples.

### L'évolution des techniques d'injection en PHP

Les techniques d'injection en PHP ont considérablement évolué. Au-delà des injections SQL classiques, les attaquants exploitent maintenant la **désérialisation non sécurisée** (`unserialize()` sur des données utilisateur), les **Server-Side Template Injections** (SSTI) dans Twig ou Blade, et les **injections de type** exploitant le typage faible de PHP. La vulnérabilité de **type juggling** (`"0e123" == "0e456"` retourne true en PHP) a permis de nombreux bypasses d'authentification. Les **gadget chains** POP (Property Oriented Programming) transforment des objets apparemment inoffensifs en vecteurs d'exécution de code lors de la désérialisation.

### L'intégration dans le cycle de développement sécurisé

Un scanner de sécurité comme cette extension s'inscrit dans une approche **DevSecOps** où la sécurité est intégrée tout au long du cycle de développement. L'analyse en temps réel dans l'IDE constitue la première ligne de défense, détectant les problèmes avant même le commit. Les hooks de pre-commit peuvent enforcer des règles de sécurité minimales. L'intégration dans la CI/CD (GitHub Actions, GitLab CI) permet une analyse systématique de chaque pull request. Enfin, les outils DAST (Dynamic Application Security Testing) comme OWASP ZAP complètent l'analyse statique en testant l'application en exécution. Cette approche multicouche maximise la détection des vulnérabilités à chaque étape.


---

