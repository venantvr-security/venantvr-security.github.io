---
layout: default
title: "Python.AccèssForbiddenFiles"
description: "Scanner de Fichiers Sensibles Exposés"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.AccèssForbiddenFiles</span>
</div>

<div class="page-header">
  <h1>Python.AccèssForbiddenFiles</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.AccèssForbiddenFiles" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Scanner de Fichiers Sensibles Exposés

> **AVERTISSEMENT** : Utilisez cet outil **uniquement** sur vos propres serveurs pour vérifier votre configuration.

## Introduction : Les Fichiers Oubliés par les Développeurs

L'un des problèmes de sécurité les plus courants sur le web est l'exposition accidentelle de fichiers sensibles. Un fichier `.env` contenant les mots de passe de base de données, un répertoire `.git` révélant tout l'historique du code, une backup SQL oubliée... Ces erreurs sont triviales à exploiter mais souvent ignorées jusqu'à ce qu'un attaquant les découvre.

Ce scanner automatise la vérification de votre serveur web en testant l'accès à une liste complète de fichiers sensibles connus. L'objectif est de s'assurer que vos règles `.htaccess` ou nginx bloquent correctement ces ressources.

### Fichiers recherchés par les attaquants

| Catégorie | Exemples | Niveau de risque |
|-----------|----------|------------------|
| **Environnement** | `.env`, `.env.local`, `.env.production` | 🔴 Critique |
| **Git** | `.git/config`, `.git/HEAD`, `.gitignore` | 🔴 Critique |
| **Backups** | `backup.sql`, `database.zip`, `*.bak` | 🔴 Critique |
| **Configuration** | `config.php`, `wp-config.php`, `settings.py` | 🔴 Critique |
| **Logs** | `error.log`, `access.log`, `debug.log` | 🟠 Élevé |
| **IDE** | `.idea/`, `.vscode/settings.json` | 🟡 Moyen |


## Architecture du Scanner

Le scanner est simple mais efficace : il teste chaque chemin connu avec différentes méthodes HTTP et analyse les codes de réponse pour déterminer si le fichier est protégé ou exposé.

<div class="mermaid">
flowchart TB
    subgraph INPUT["📋 Configuration"]
        TARGETS["URLs ciblés"]
        PATHS["Chemins à tester"]
    end

    subgraph SCANNER["⚙️ Moteur de Scan"]
        REQ["Requêtes HTTP"]
        GET["GET"]
        POST["POST"]
        HEAD["HEAD"]
    end

    subgraph ANALYSIS["🔍 Analyse"]
        CODE["Code HTTP"]
        SIZE["Taille réponse"]
        CONTENT["Contenu"]
    end

    subgraph RESULT["📊 Résultats"]
        OK["✅ 403 Forbidden"]
        VULN["🔴 200 OK = Vulnérable"]
    end

    INPUT --> SCANNER
    SCANNER --> GET & POST & HEAD
    GET & POST & HEAD --> ANALYSIS
    ANALYSIS --> CODE
    CODE -->|"403/404"| OK
    CODE -->|"200"| VULN

    style VULN fill:#e74c3c,fill-opacity:0.15
    style OK fill:#2ecc71,fill-opacity:0.15
    style RESULT fill:#808080,fill-opacity:0.15
    style ANALYSIS fill:#808080,fill-opacity:0.15
    style SCANNER fill:#808080,fill-opacity:0.15
    style INPUT fill:#808080,fill-opacity:0.15
</div>


## Flux de Scan en Détail

Ce diagramme montre comment le scanner teste chaque fichier et interprète les réponses du serveur.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant S as 🔧 Scanner
    participant T as 🎯 Serveur cible

    S->>T: GET /.env
    alt Serveur correctement configuré
        T-->>S: 403 Forbidden
        Note over S: ✅ Fichier protégé
    else Fichier exposé !
        T-->>S: 200 OK + contenu
        Note over S: 🔴 VULNÉRABLE !
    end

    S->>T: GET /.git/config
    alt Répertoire caché
        T-->>S: 404 Not Found
        Note over S: ✅ Non accessible
    else Dépôt git exposé !
        T-->>S: 200 OK + config git
        Note over S: 🔴 Code source volable !
    end

    S->>T: GET /backup.sql
    T-->>S: ???
</div>


## Le Script Python

```python
# main.py
from configuration import Config
import requests
from concurrent.futures import ThreadPoolExecutor

# Liste exhaustive de fichiers sensibles à tester
SENSITIVE_PATHS = [
    # Fichiers d'environnement
    '.env', '.env.local', '.env.production', '.env.backup',

    # Répertoire Git (permet de cloner tout le code source !)
    '.git/config', '.git/HEAD', '.git/index', '.gitignore',

    # Backups (souvent laissées par erreur)
    'backup.sql', 'database.sql', 'dump.sql',
    'backup.zip', 'backup.tar.gz', 'site.zip',

    # Fichiers de configuration
    'config.php', 'wp-config.php', 'settings.py',
    'config.yml', 'secrets.yml', 'application.yml',

    # Logs (peuvent révéler des erreurs SQL, chemins, etc.)
    'error.log', 'debug.log', 'access.log',

    # Fichiers IDE
    '.idea/', '.vscode/settings.json',

    # Fichiers de debug
    'phpinfo.php', 'info.php', 'test.php',
    'composer.json', 'package.json'
]


def scan_sensitive_files(base_url, paths=SENSITIVE_PATHS):
    """
    Scanne une liste de chemins sensibles sur un serveur web.

    Un fichier est considéré comme exposé si le serveur répond 200 OK.
    Les codes 403, 404, 500 indiquent que le fichier est protégé ou inexistant.
    """
    results = {'vulnérable': [], 'protected': [], 'errors': []}

    for path in paths:
        url = f"{base_url.rstrip('/')}/{path}"
        try:
            resp = requests.get(url, timeout=5, allow_redirects=False)

            if resp.status_code == 200:
                # DANGER : fichier accessible !
                results['vulnérable'].append({
                    'path': path,
                    'status': resp.status_code,
                    'size': len(resp.content),
                    'preview': resp.text[:100] if resp.text else ''
                })
            else:
                # OK : fichier protégé ou inexistant
                results['protected'].append({
                    'path': path,
                    'status': resp.status_code
                })

        except Exception as e:
            results['errors'].append({'path': path, 'error': str(e)})

    return results


# Utilisation
if __name__ == "__main__":
    target = "https://example.com"
    results = scan_sensitive_files(target)

    print(f"\\n🔴 FICHIERS VULNÉRABLES ({len(results['vulnérable'])}):")
    for vuln in results['vulnérable']:
        print(f"  {vuln['path']} - {vuln['size']} bytes")

    print(f"\\n✅ Fichiers protégés: {len(results['protected'])}")
```


## Protection avec .htaccess

Si le scan révèle des fichiers exposés, voici comment les protéger dans Apache :

```apache
# Bloquer l'accès aux fichiers sensibles
<FilesMatch "^\.env|\.git|\.htaccess|\.sql$">
    Order allow,deny
    Deny from all
</FilesMatch>

# Bloquer les backups et archives
<FilesMatch "\.(bak|sql|zip|tar|gz|7z)$">
    Order allow,deny
    Deny from all
</FilesMatch>

# Bloquer les fichiers de log
<FilesMatch "\.(log)$">
    Order allow,deny
    Deny from all
</FilesMatch>
```


## Pour Aller Plus Loin

- 📚 [OWASP Sensitive Data Exposure](https://owasp.org/www-project-web-security-testing-guide/) - Guide de test
- 🔓 [Git Dumper](https://blog.netspi.com/dumping-git-data-from-misconfigured-web-servers/) - Exploitation des .git exposés


## Exploits et Vulnérabilités Connues

- **CVE-2019-11043 (PHP-FPM)** : Vulnérabilité d'exécution de code à distance dans PHP-FPM permettant d'exploiter des fichiers PHP exposés. Un fichier phpinfo.php accessible pouvait révéler la configuration vulnérable.

- **CVE-2021-41773 (Apache Path Traversal)** : Faille de traversée de chemin dans Apache 2.4.49 permettant l'accès à des fichiers arbitraires en dehors du DocumentRoot via des requêtes URL encodées.

- **CVE-2017-9841 (PHPUnit RCE)** : Exécution de code à distance via le fichier `vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php` exposé. Des milliers de sites ont été compromis via ce fichier oublié.

- **CVE-2019-11510 (Pulse Secure)** : Lecture arbitraire de fichiers permettant d'accéder aux fichiers de configuration et aux sessions utilisateur via une simple requête HTTP mal formée.

- **Breach Twitch 2021** : Fuite massive causée par un répertoire .git exposé sur un serveur interne, permettant le téléchargement de l'intégralité du code source et des revenus des streamers.


## Approfondissement Théorique

L'exposition de fichiers sensibles est classée dans le Top 10 OWASP sous la catégorie "Security Misconfiguration" (A05:2021). Cette vulnérabilité résulte généralement d'une mauvaise configuration des serveurs web plutôt que d'une faille dans le code applicatif. Les serveurs de développement sont souvent déployés en production sans durcissement, exposant des fichiers de debug, des répertoires de contrôle de version, et des sauvegardes automatiques.

Le répertoire .git est particulièrement dangereux car il contient l'intégralité de l'historique du projet. Des outils comme GitTools ou git-dumper permettent de reconstruire un dépôt complet à partir des objets git accessibles. Même si seul le fichier .git/config est lisible, il peut révéler des URLs de dépôts privés ou des credentials. La protection doit être systématique : bloquer tout accès aux répertoires commençant par un point (dotfiles).

Les bonnes pratiques de déploiement incluent : utilisation de variables d'environnement plutôt que de fichiers .env en production, exclusion des répertoires de développement (.git, .idea, node_modules) via le serveur web, configuration de règles de pare-feu applicatif (WAF) pour bloquer les patterns suspects, et audits réguliers avec des outils automatisés. Le principe du moindre privilège s'applique : seuls les fichiers strictement nécessaires au fonctionnement de l'application doivent être accessibles depuis le web.


---

