---
layout: default
title: "Tor.Web.Capture"
description: "Capture de Pages Web via TOR en Rust"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Tor.Web.Capture</span>
</div>

<div class="page-header">
  <h1>Tor.Web.Capture</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Tor.Web.Capture" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Capture de Pages Web via TOR en Rust

## Introduction : Pourquoi Capturer des Sites Anonymement ?

Dans le domaine de la veille sécuritaire, il est souvent nécessaire de capturer des pages web sans révéler son identité. Que ce soit pour surveiller des sites de phishing, analyser des marketplaces du dark web, ou simplement archiver du contenu sensible, l'anonymat est crucial.

Ce projet propose une solution complète en **Rust** pour capturer des pages web de manière totalement anonyme via le réseau **TOR**. Contrairement aux solutions basées sur le Tor Browser, celle-ci utilise **Arti**, l'implémentation native de TOR en Rust, offrant une intégration plus fine et de meilleures performances.

### Ce que ce projet permet de faire

| Fonctionnalité        | Description                                     |
| --------------------- | ----------------------------------------------- |
| **Capture anonyme**   | Screenshots et HTML via TOR                     |
| **Dashboard HTMX**    | Interface web moderne et réactive               |
| **Planification**     | Captures programmées via cron intégré           |
| **Multi-identités**   | User-Agents de scanners connus (Shodan, Censys) |
| **Stockage cloud**    | Upload automatique vers Google Drive            |
| **Circuit isolation** | Nouveau circuit TOR par capture                 |

### Composants techniques

Le projet combine plusieurs technologies modernes :

| Composant      | Rôle                  | Technologie       |
| -------------- | --------------------- | ----------------- |
| **Client TOR** | Connexion anonyme     | Arti (Rust natif) |
| **Navigateur** | Rendu des pages       | Headless Chrome   |
| **Interface**  | Dashboard utilisateur | HTMX + HTML       |
| **Stockage**   | Persistance           | SQLite + fichiers |
| **API**        | Communication         | REST JSON         |

## Architecture du Système

L'architecture est conçue pour garantir l'anonymat à chaque étape. Le diagramme suivant illustre comment les différents composants interagissent, depuis l'interface utilisateur jusqu'à la cible, en passant par le réseau TOR.

<div class="mermaid">
flowchart TB
    subgraph UI["🖥️ Interface Utilisateur"]
        HTMX["Dashboard HTMX"]
        HTMX_note>":8080<br/><i>Interface moderne</i>"]
    end

    subgraph CORE["⚙️ Cœur Rust"]
        API["API REST"]
        API_note>"<i>Gestion des requêtes</i>"]
        SCHED["Scheduler"]
        SCHED_note>"<i>Planification cron</i>"]
        CAP["Capture Engine"]
        CAP_note>"<i>Orchestrateur principal</i>"]
    end

    subgraph TOR["🧅 Réseau TOR"]
        ARTI["Arti Client"]
        ARTI_note>"<i>TOR natif en Rust</i>"]
        G["Guard Node"]
        M["Middle Relay"]
        E["Exit Node"]
        G --> M --> E
    end

    subgraph BROWSER["🌐 Navigateur"]
        CHROME["Headless Chrome"]
        CHROME_note>"<i>Rendu et capture</i>"]
    end

    subgraph TARGET["🎯 Cible"]
        WEB["Site web cible"]
    end

    subgraph STORAGE["💾 Stockage"]
        DB[(SQLite)]
        FS["Fichiers locaux"]
        FS_note>"<i>Screenshots, HTML</i>"]
        GD["☁️ Google Drive"]
        GD_note>"<i>Backup cloud</i>"]
    end

    HTMX --> API
    API --> CAP
    SCHED --> CAP
    CAP --> ARTI
    ARTI --> G
    E --> CHROME
    CHROME --> WEB
    CAP --> DB & FS & GD

    style ARTI fill:#9b59b6,fill-opacity:0.15
    style CAP fill:#3498db,fill-opacity:0.15
    style CHROME fill:#e74c3c,fill-opacity:0.15
    style WEB fill:#2ecc71,fill-opacity:0.15
    style STORAGE fill:#808080,fill-opacity:0.15
    style TARGET fill:#808080,fill-opacity:0.15
    style BROWSER fill:#808080,fill-opacity:0.15
    style TOR fill:#808080,fill-opacity:0.15
    style CORE fill:#808080,fill-opacity:0.15
    style UI fill:#808080,fill-opacity:0.15

</div>

## Flux de Capture en Détail

Voyons maintenant comment se déroule une capture, étape par étape. Ce diagramme de séquence montre les interactions entre tous les composants, depuis la demande de l'utilisateur jusqu'à l'affichage du résultat.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant U as 👤 Utilisateur
    participant W as 🖥️ Dashboard
    participant À as ⚙️ API Rust
    participant T as 🧅 Arti (TOR)
    participant C as 📸 Chrome
    participant S as 🎯 Site cible

    Note over U,S: Phase 1 : Configuration de la cible
    U->>W: Ajouter URL cible
    W->>A: POST /api/targets
    A-->>W: Cible enregistrée
    
    Note over U,S: Phase 2 : Lancement de la capture
    U->>W: Cliquer "Capture"
    W->>A: POST /api/capture/{id}
    A->>T: Demander nouveau circuit
    T->>T: Établir Guard → Middle → Exit
    
    Note over U,S: Phase 3 : Capture anonyme
    T->>C: Connexion via SOCKS5
    C->>S: GET / (via TOR)
    S-->>C: HTML + ressources
    C->>C: Rendu de la page
    C->>A: Screenshot PNG + HTML
    
    Note over U,S: Phase 4 : Stockage et affichage
    A->>A: Sauvegarder fichiers
    A-->>W: Capture terminée
    W-->>U: Afficher résultat

</div>

### Points clés du processus

1. **Nouveau circuit par capture** : Chaque capture utilise un circuit TOR différent, empêchant la corrélation entre les requêtes
2. **Pas de fuite DNS** : Toutes les résolutions DNS passent par TOR
3. **Rendu complet** : Chrome exécute le JavaScript, capturant la page telle que vue par un visiteur

## Installation et Configuration

Le projet nécessite Rust 1.75 ou supérieur, ainsi qu'une installation de Chrome ou Chromium.

```bash
# Cloner le dépôt
git clone https://github.com/venantvr-security/Tor.Web.Capture.git
cd Tor.Web.Capture

# Compiler en mode release (optimisé)
cargo build --release

# Lancer l'application
cargo run --release
# Le dashboard sera accessible sur http://localhost:8080
```

### Fichier de configuration

Le fichier `config/default.toml` permet de personnaliser le comportement :

```toml
# config/default.toml

[tor]
# Activer/désactiver TOR (utile pour le debug)
enabled = true

# Créer un nouveau circuit pour chaque capture
# Recommandé pour un maximum d'anonymat
new_circuit_per_capture = true

# Timeout de connexion au réseau TOR (secondes)
connection_timeout = 30

[capture]
# Nombre maximum de captures simultanées
max_concurrent_captures = 3

# Dimensions de la fenêtre du navigateur
default_viewport_width = 1920
default_viewport_height = 1080

# Délai avant la capture (pour laisser le JS se charger)
page_load_delay_ms = 3000

[storage]
# Répertoire de stockage des captures
output_directory = "./captures"

# Activer l'upload Google Drive (nécessite OAuth)
google_drive_enabled = false
```

## Mesures de Sécurité

L'anonymat est garanti par plusieurs mécanismes complémentaires :

| Mesure                 | Description                          | Importance |
| ---------------------- | ------------------------------------ | ---------- |
| **DNS via TOR**        | Résolution de noms via le réseau TOR | Critique   |
| **WebRTC désactivé**   | Empêche les fuites d'IP locale       | Critique   |
| **Circuit isolation**  | Nouveau chemin TOR par capture       | Élevée     |
| **User-Agent rotatif** | Imite différents scanners connus     | Moyenne    |
| **Pas de cookies**     | Profil vierge à chaque capture       | Moyenne    |

### User-Agents disponibles

Pour imiter des scanners légitimes et éviter d'être bloqué :

| Scanner    | Usage typique                 |
| ---------- | ----------------------------- |
| **Shodan** | Reconnaissance infrastructure |
| **Censys** | Analyse de certificats        |
| **ZGrab**  | Scans automatisés             |
| **Nmap**   | Tests de sécurité             |

## Cas d'Usage

Ce projet est utile dans plusieurs contextes légitimes :

1. **Threat Intelligence** : Surveiller des sites de phishing ciblant votre organisation
2. **Analyse forensique** : Archiver des preuves sans alerter l'attaquant
3. **Veille dark web** : Monitorer des marketplaces .onion
4. **Tests de sécurité** : Vérifier l'anonymat de vos propres systèmes

## Pour Aller Plus Loin

Le monde de l'anonymat en ligne et de la capture web offre de nombreuses pistes d'exploration :

- 🧅 [Arti - TOR en Rust](https://gitlab.torproject.org/tpo/core/arti) - L'implémentation officielle de TOR en Rust
- 🌐 [Tor Project](https://www.torproject.org/) - Documentation officielle du réseau TOR
- 📱 [HTMX](https://htmx.org/) - Framework frontend utilisé pour le dashboard
- 🔒 [Tails OS](https://tails.boum.org/) - Système d'exploitation anonyme complet


## Exploits et Vulnérabilités Connues

Les technologies de capture web et d'anonymisation ont été affectées par plusieurs vulnérabilités :

| CVE | Produit | Description | Score CVSS |
|-----|---------|-------------|------------|
| **CVE-2022-1853** | Chrome Headless | Use-after-free dans Indexed DB permettant RCE via page malveillante | 8.8 Élevé |
| **CVE-2021-21224** | Chrome V8 | Type confusion dans le moteur JavaScript, exploitable lors du rendu de pages | 8.8 Élevé |
| **CVE-2020-15572** | Tor Browser | Fuite d'information via le header Referer permettant correlation de sessions | 6.5 Moyen |
| **CVE-2023-3079** | Chrome | Type confusion dans V8 exploitée activement dans la nature | 8.8 Élevé |
| **CVE-2019-11707** | Firefox (Tor Browser base) | Type confusion permettant l'exécution de code arbitraire | 8.8 Élevé |

Les navigateurs headless comme Chrome représentent une surface d'attaque significative. Un site malveillant peut potentiellement exploiter des vulnérabilités du navigateur pour compromettre le système de capture, d'où l'importance de l'isolation (sandbox, conteneurs).


## Approfondissement Théorique

### Les vecteurs de désanonymisation

Même avec TOR, plusieurs vecteurs peuvent compromettre l'anonymat. Le **fingerprinting de navigateur** analyse des caractéristiques uniques comme la résolution d'écran, les fonts installés, les plugins, et même le comportement du moteur de rendu pour identifier un visiteur. Les **fuites WebRTC** peuvent révéler l'IP réelle via les protocoles STUN/TURN utilisés pour la communication peer-to-peer. Les **timing attacks** corrèlent le moment d'une requête avec l'activité réseau observée au niveau FAI. Pour contrer ces menaces, ce projet désactive WebRTC, utilise des viewports standardisés, et isole chaque capture dans un profil navigateur vierge.

### L'architecture des services cachés TOR

Les services .onion (v3) utilisent un système de rendez-vous cryptographique complexe. Le service publie ses descripteurs chiffrés sur une table de hachage distribuée (DHT) du réseau TOR. Un client souhaitant accéder au service récupère ces descripteurs, établit un circuit vers un point de rendez-vous, et le service fait de même depuis son côté. Les deux parties se rencontrent au point de rendez-vous sans jamais révéler leurs emplacements réels. Cette architecture garantit l'anonymat bidirectionnel mais introduit une latence significative (6 sauts au lieu de 3 pour le web classique via TOR).

### La sécurité du web scraping anonyme

Le scraping anonyme pose des défis sécuritaires particuliers. Le site ciblé peut être malveillant et tenter d'exploiter des vulnérabilités du navigateur. Les protections anti-bot (Cloudflare, Akamai) peuvent détecter les patterns de scraping automatisé même via TOR. Les **honeypots** et **canary tokens** peuvent alerter les opérateurs de sites suspects que leur infrastructure est surveillée. Une approche robuste combine l'isolation du navigateur (sandbox, VM, conteneur), la rotation des circuits TOR et des user-agents, des délais réalistes entre les requêtes, et une vérification des contenus capturés pour détecter les redirections malveillantes ou les pages de blocage.


---
