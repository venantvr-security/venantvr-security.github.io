---
layout: default
title: "Python.HAR.Scanner"
description: "Analyseur de Fichiers HAR avec Haralyzer"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.HAR.Scanner</span>
</div>

<div class="page-header">
  <h1>Python.HAR.Scanner</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.HAR.Scanner" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Analyseur de Fichiers HAR avec Haralyzer

## Introduction : Qu'est-ce qu'un Fichier HAR ?

Lorsque vous naviguez sur un site web, votre navigateur effectue des dizaines, voire des centaines de requêtes HTTP : chargement de pages HTML, images, scripts JavaScript, appels API... Un fichier **HAR** (HTTP Archive) capture **toutes ces interactions** dans un format JSON standardisé.

### Pourquoi analyser les fichiers HAR ?

Pour un auditeur de sécurité, les fichiers HAR sont une mine d'or. Ils contiennent :

- **Les cookies** : sont-ils correctement protégés (HttpOnly, Secure, SameSite) ?
- **Les headers de sécurité** : HSTS, CSP, X-Frame-Options sont-ils présents ?
- **Les données sensibles** : des informations personnelles circulent-elles en clair ?
- **Les tokens d'authentification** : sont-ils suffisamment aléatoires ?

Ce projet utilise la bibliothèque **haralyzer** pour parser et analyser automatiquement ces fichiers, générant un rapport de sécurité détaillé.


## Architecture du Scanner

Le processus d'analyse se déroule en trois étapes : capture via les DevTools du navigateur, parsing avec haralyzer, puis vérifications de sécurité.

<div class="mermaid">
flowchart TB
    subgraph CAPTURE["📸 Capture"]
        BROWSER["🌐 Navigateur"]
        DEVTOOLS["DevTools (F12)"]
        EXPORT["Export HAR"]
    end

    subgraph ANALYSIS["🔍 Analyse"]
        HARALYZER["haralyzer"]
        PARSER["HAR Parser"]
        SECURITY["Security Checks"]
    end

    subgraph FINDINGS["📊 Résultats"]
        F1["🔴 Cookies non sécurisés"]
        F2["🟠 Headers manquants"]
        F3["🟡 Données sensibles"]
        F4["✅ Bonnes pratiques"]
    end

    BROWSER --> DEVTOOLS --> EXPORT
    EXPORT --> HARALYZER --> PARSER --> SECURITY
    SECURITY --> F1 & F2 & F3 & F4

    style F1 fill:#e74c3c,fill-opacity:0.15
    style F2 fill:#f39c12,fill-opacity:0.15
    style F4 fill:#2ecc71,fill-opacity:0.15
    style FINDINGS fill:#808080,fill-opacity:0.15
    style ANALYSIS fill:#808080,fill-opacity:0.15
    style CAPTURE fill:#808080,fill-opacity:0.15
</div>


## Flux d'Analyse Détaillé

Ce diagramme de séquence montre les interactions entre les différents composants lors de l'analyse d'un fichier HAR.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant B as 🌐 Browser
    participant H as 📄 HAR File
    participant S as 🔧 Scanner
    participant R as 📊 Report

    B->>H: Export session.har
    S->>H: haralyzer.HarParser()
    H-->>S: Parsed HAR object

    loop Pour chaque entrée HTTP
        S->>S: Analyser headers de réponse
        S->>S: Vérifier attributs des cookies
        S->>S: Scanner le corps des réponses
    end

    S->>R: Générer rapport de sécurité
</div>


## Utilisation de Base

Le code suivant montre comment charger et parcourir un fichier HAR avec haralyzer :

```python
from haralyzer import HarParser, HarPage
import json

# Charger le fichier HAR exporté depuis les DevTools
with open('session.har', 'r') as f:
    har_parser = HarParser(json.loads(f.read()))

# Parcourir toutes les pages de la session
for page in har_parser.pages:
    print(f"📄 Page: {page.title}")
    print(f"   Temps de chargement: {page.page_load_time}ms")

    # Analyser chaque requête/réponse
    for entry in page.entries:
        print(f"   {entry.request.method} {entry.request.url}")
        print(f"      Status: {entry.response.status}")
```


## Vérifications de Sécurité Automatisées

Le scanner effectue plusieurs vérifications de sécurité sur chaque entrée du fichier HAR. Le diagramme ci-dessous résume les points vérifiés et leur niveau de criticité.

<div class="mermaid">
flowchart LR
    subgraph Checks["🔐 Vérifications"]
        C1["Cookies HttpOnly"]
        C2["Cookies Secure"]
        C3["Headers HSTS"]
        C4["Headers CSP"]
        C5["Données PII"]
    end

    subgraph Status["État"]
        OK["✅ Conforme"]
        WARN["⚠️ Attention"]
        FAIL["❌ Vulnérable"]
    end

    C1 & C2 --> OK
    C3 & C4 --> WARN
    C5 --> FAIL

    style C1 fill:#2ecc71,fill-opacity:0.15
    style C5 fill:#e74c3c,fill-opacity:0.15
    style Status fill:#808080,fill-opacity:0.15
    style Checks fill:#808080,fill-opacity:0.15
</div>

### Script de Scan Complet

```python
def security_scan(har_parser):
    """
    Analyse un fichier HAR et retourne les problèmes de sécurité détectés.

    Vérifie :
    - Les attributs de sécurité des cookies (HttpOnly, Secure)
    - La présence des headers de sécurité (HSTS, CSP, X-Frame-Options)
    - Les fuites potentielles de données sensibles
    """
    findings = []

    for page in har_parser.pages:
        for entry in page.entries:
            # === VÉRIFICATION DES COOKIES ===
            for cookie in entry.response.cookies:
                # Cookie sans HttpOnly = vulnérable au vol via XSS
                if not cookie.get('httpOnly'):
                    findings.append({
                        'type': 'COOKIE_NOT_HTTPONLY',
                        'severity': 'HIGH',
                        'cookie': cookie['name'],
                        'url': entry.request.url,
                        'recommendation': 'Ajouter le flag HttpOnly au cookie'
                    })

                # Cookie sans Secure = peut être intercepté sur HTTP
                if not cookie.get('secure'):
                    findings.append({
                        'type': 'COOKIE_NOT_SECURE',
                        'severity': 'MEDIUM',
                        'cookie': cookie['name'],
                        'recommendation': 'Ajouter le flag Secure au cookie'
                    })

            # === VÉRIFICATION DES HEADERS ===
            headers = {h['name'].lower(): h['value']
                      for h in entry.response.headers}

            # Absence de HSTS = vulnérable aux attaques MITM
            if 'strict-transport-security' not in headers:
                findings.append({
                    'type': 'MISSING_HSTS',
                    'severity': 'MEDIUM',
                    'url': entry.request.url,
                    'recommendation': 'Ajouter Strict-Transport-Security header'
                })

            # Absence de CSP = vulnérable aux injections de scripts
            if 'content-security-policy' not in headers:
                findings.append({
                    'type': 'MISSING_CSP',
                    'severity': 'LOW',
                    'url': entry.request.url,
                    'recommendation': 'Implémenter une Content-Security-Policy'
                })

    return findings
```


## Exemple de Rapport

Voici un exemple de sortie du scanner :

```
🔍 Scanning: session.har
📊 Found 3 pages, 127 entries

Page 1: Login Page
  ❌ Cookie 'session_id' missing HttpOnly
     → Risque: Vol de session via XSS
  ⚠️ Missing HSTS header on /api/login
     → Risque: Attaque man-in-the-middle
  ✅ CSP header present

Page 2: Dashboard
  ⚠️ Potential PII in response body (email détected)
     → Risque: Exposition de données personnelles
  ✅ All cookies secure

Page 3: Settings
  ✅ All security headers present
  ✅ No sensitive data detected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
  🔴 Critical: 1
  🟠 Warning: 2
  🟢 Passed: 124
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```


## Comment Exporter un Fichier HAR

1. Ouvrez les DevTools de votre navigateur (F12)
2. Allez dans l'onglet **Network** (Réseau)
3. Naviguez sur le site à analyser
4. Clic droit dans la liste des requêtes → **Save all as HAR with content**


## Pour Aller Plus Loin

- 📚 [Documentation Haralyzer](https://haralyzer.readthedocs.io/) - API complète
- 📄 [Spécification HAR 1.2](http://www.softwareishard.com/blog/har-12-spec/) - Format officiel
- 🛡️ [OWASP Secure Headers](https://owasp.org/www-project-secure-headers/) - Best practices


## Exploits et Vulnérabilités Connues

- **CVE-2020-8161 (Rack)** : Vulnérabilité de directory traversal dans Rack, détectable via l'analyse HAR des requêtes statiques. Les patterns de chemins anormaux dans les logs révèlent les tentatives d'exploitation.

- **CVE-2019-5418 (Rails File Content Disclosure)** : Fuite de fichiers via le header Accept mal géré. L'analyse HAR permet de détecter les requêtes suspectes avec des headers Accept contenant des chemins de fichiers.

- **Missing Security Headers (OWASP Top 10)** : L'absence de headers comme X-Content-Type-Options, X-Frame-Options, ou CSP est une des vulnérabilités les plus courantes détectables par analyse HAR automatisée.

- **CVE-2020-11022 (jQuery XSS)** : L'analyse HAR peut identifier les versions vulnérables de jQuery via les chemins de scripts chargés ou les commentaires de version dans les fichiers JS.

- **PII Exposure Incidents** : Nombreuses fuites de données (Equifax, Facebook) auraient pu être détectées plus tôt par analyse automatisée des réponses API contenant des données sensibles non masquées.


## Approfondissement Théorique

Le format HAR (HTTP Archive) a été initialement développé par Jan Odvarko pour le projet Firebug et standardisé en 2012 sous la spécification HAR 1.2. Il est devenu le standard de facto pour l'export des sessions de navigation, supporté par tous les navigateurs modernes et les outils de proxy comme Fiddler, Charles Proxy, et Burp Suite.

L'analyse automatisée de fichiers HAR s'inscrit dans le domaine plus large du DAST (Dynamic Application Security Testing). Contrairement au SAST qui analyse le code source, le DAST examine le comportement de l'application en runtime. L'avantage de l'approche HAR est qu'elle capture le trafic réel, incluant les requêtes générées dynamiquement par JavaScript et les réponses complètes du serveur. C'est particulièrement utile pour détecter les fuites de données sensibles (PII, tokens, secrets) qui peuvent ne pas être visibles dans le code source.

Les headers de sécurité HTTP constituent une couche de défense en profondeur essentielle. HSTS (HTTP Strict Transport Security) prévient les attaques de downgrade SSL. CSP (Content Security Policy) atténue les risques XSS en contrôlant les sources de scripts autorisées. X-Frame-Options prévient le clickjacking. L'analyse HAR permet de vérifier systématiquement la présence et la configuration correcte de ces headers sur toutes les ressources d'une application, identifiant les endpoints qui auraient pu échapper à la configuration globale.


---

