---
layout: default
title: "Javascript.TOR.Workflow"
description: "Visualisations Interactives de Protocoles de Sécurité"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Javascript.TOR.Workflow</span>
</div>

<div class="page-header">
  <h1>Javascript.TOR.Workflow</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Javascript.TOR.Workflow" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Visualisations Interactives de Protocoles de Sécurité

## Introduction : Comprendre par la Visualisation

Les protocoles de sécurité sont souvent expliqués avec des diagrammes statiques ou des descriptions textuelles abstraites. Pourtant, ces mécanismes sont **dynamiques** : ils impliquent des échanges de messages, des négociations, des transformations de données en temps réel.

Ce projet propose une approche différente : des **visualisations HTML/CSS/JavaScript interactives** qui vous permettent de voir ces protocoles s'exécuter étape par étape. Vous pouvez observer comment les paquets sont chiffrés couche par couche dans TOR, comment un handshake TLS s'établit, ou comment une architecture Zero Trust vérifie chaque accès.

### Les protocoles visualisés

Chaque visualisation est une page web autonome que vous pouvez ouvrir dans votre navigateur et explorer à votre rythme.

| Visualisation | Description |
|---------------|-------------|
| `tor-workflow/` | Construction du circuit TOR et "routage en oignon" |
| `https-workflow/` | Handshake TLS 1.3 avec échange Diffie-Hellman |
| `ssh-protocol/` | Authentification et échange de clés SSH |
| `ipsec-vpn/` | Établissement d'un tunnel IPSec VPN |
| `dns-over-https/` | Résolution DNS chiffrée via HTTPS |
| `webrtc/` | Signalisation et établissement de connexion WebRTC |
| `zero-trust/` | Architecture de sécurité sans confiance implicite |
| `blockchain-pow-workflow/` | Consensus Proof of Work (minage) |
| `blockchain-pos-workflow/` | Consensus Proof of Stake (validation) |


## Le Réseau TOR : L'Anonymat par les Couches

TOR (The Onion Router) est un réseau d'anonymisation qui protège l'identité des utilisateurs en acheminant leur trafic à travers plusieurs relais. Son nom "oignon" vient de l'architecture de chiffrement : chaque relais ne peut "peler" qu'une couche de chiffrement, sans jamais voir l'intégralité du chemin.

### Pourquoi plusieurs relais ?

L'idée fondamentale est qu'aucun acteur ne doit pouvoir corréler l'origine et la destination du trafic :

- Le **nœud d'entrée (Guard)** connaît votre adresse IP, mais pas votre destination
- Le **nœud intermédiaire (Middle)** ne connaît ni l'origine ni la destination
- Le **nœud de sortie (Exit)** connaît la destination, mais pas votre identité

<div class="mermaid">
flowchart LR
    C[Client] -->|"🔐🔐🔐"| G[Guard]
    G -->|"🔐🔐"| M[Middle]
    M -->|"🔐"| E[Exit]
    E -->|"📄"| S[Serveur]

    style C fill:#3498db,fill-opacity:0.15
    style G fill:#9b59b6,fill-opacity:0.15
    style M fill:#e74c3c,fill-opacity:0.15
    style E fill:#f39c12,fill-opacity:0.15
    style S fill:#2ecc71,fill-opacity:0.15
</div>

**Lecture du diagramme** : Le client chiffré ses données avec trois clés (une pour chaque nœud). À chaque étape, un nœud retire une couche de chiffrement. Seul le serveur final reçoit les données en clair.


## HTTPS/TLS 1.3 : La Sécurité du Web Moderne

Chaque fois que vous voyez le cadenas dans votre navigateur, c'est TLS qui protège vos données. La version 1.3 du protocole représente une avancée majeure : le handshake est réduit à **un seul aller-retour** (1-RTT), contre deux pour TLS 1.2.

### Comment ça marche ?

Le secret réside dans l'échange **Diffie-Hellman éphémère** : le client et le serveur envoient simultanément leurs paramètres cryptographiques dès le premier message. Ils peuvent ainsi calculer un secret partagé sans avoir besoin d'un échange supplémentaire.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant C as 🖥️ Client
    participant S as 🌐 Serveur

    C->>S: ClientHello + KeyShare
    S->>C: ServerHello + KeyShare
    S->>C: Certificate + Verify + Finished
    C->>S: Finished

    rect rgb(46, 204, 113, 0.3)
        Note over C,S: 🔒 Connexion chiffrée établie
    end
</div>

**Points clés** :
1. Le client propose ses paramètres cryptographiques dans le premier message
2. Le serveur répond immédiatement avec les siens
3. Dès le message 4, la connexion est sécurisée et les données peuvent circuler


## Architecture Zero Trust : Ne Faire Confiance à Personne

Le modèle de sécurité traditionnel distingue l'intérieur (réseau d'entreprise, sûr) de l'extérieur (Internet, dangereux). Mais que se passe-t-il si un attaquant est déjà à l'intérieur ? Ou si vos employés travaillent de chez eux ?

L'architecture **Zero Trust** ("Confiance Zéro") abandonne cette distinction. Chaque accès, même depuis le réseau interne, doit être **explicitement autorisé** après vérification de l'identité, du contexte et de la politique de sécurité.

<div class="mermaid">
flowchart TB
    subgraph Utilisateurs
        U1[👤 Employé]
        U2[👤 Externe]
    end

    subgraph PDP["Policy Decision Point"]
        ID[🔑 Identity]
        CTX[📊 Context]
        POL[📋 Policy]
    end

    subgraph Ressources
        R1[💾 Base de données]
        R2[📁 Fichiers]
        R3[🔧 API]
    end

    U1 & U2 --> PEP[🛡️ Policy Enforcement]
    PEP <--> PDP
    PEP --> R1 & R2 & R3

    style PEP fill:#e74c3c,fill-opacity:0.15
    style PDP fill:#3498db,fill-opacity:0.15
</div>

**Les composants clés** :
- **Policy Enforcement Point (PEP)** : Le gardien qui bloque ou autorise chaque requête
- **Policy Decision Point (PDP)** : Le cerveau qui prend la décision en fonction de l'identité, du contexte et des règles


## DNS-over-HTTPS : Protéger les Requêtes DNS

Les requêtes DNS traditionnelles sont envoyées en clair : votre FAI (et tout acteur sur le réseau) peut voir quels sites vous visitez. **DNS-over-HTTPS (DoH)** résout ce problème en encapsulant les requêtes DNS dans du trafic HTTPS chiffré.

<div class="mermaid">
sequenceDiagram
    participant B as 🌐 Navigateur
    participant R as 🔒 Resolver DoH
    participant D as 📡 DNS Autoritaire

    B->>R: HTTPS: /dns-query?name=example.com
    R->>D: DNS standard
    D->>R: Réponse IP
    R->>B: HTTPS: IP chiffrée

    Note over B,R: Trafic chiffré
    Note over R,D: Trafic DNS classique
</div>

**Ce qui est protégé** : Le chemin entre votre navigateur et le résolveur DoH est chiffré. Votre FAI ne voit plus vos requêtes DNS.

**Ce qui ne l'est pas** : Le résolveur DoH voit toujours vos requêtes. Le choix du résolveur (Cloudflare, Google, NextDNS...) est donc une décision de confiance importante.


## Structure du Projet

Chaque visualisation est une page web autonome avec son propre CSS et JavaScript. Vous pouvez les modifier et les étendre facilement.

```
Javascript.TOR.Workflow/
├── TOR-01.md, TOR-02.md, TOR-03.md  # Documentation théorique
├── tor-workflow/                     # Visualisation du circuit TOR
│   ├── index.html
│   ├── style.css
│   └── script.js
├── https-workflow/                   # Visualisation du handshake TLS
├── ssh-protocol/                     # Visualisation de l'échange SSH
├── ipsec-vpn/                        # Visualisation du tunnel IPSec
├── dns-over-https/                   # Visualisation DoH
├── webrtc/                           # Visualisation signalisation WebRTC
├── zero-trust/                       # Visualisation architecture ZT
├── blockchain-pow-workflow/          # Visualisation Proof of Work
└── blockchain-pos-workflow/          # Visualisation Proof of Stake
```


## Utilisation

Pour explorer les visualisations, vous pouvez simplement ouvrir les fichiers HTML dans votre navigateur, ou lancer un serveur local pour une meilleure expérience.

```bash
# Cloner le projet
git clone https://github.com/venantvr-security/Javascript.TOR.Workflow
cd Javascript.TOR.Workflow

# Méthode 1: Ouvrir directement
open tor-workflow/index.html

# Méthode 2: Serveur local (recommandé)
python -m http.server 8000
# Puis ouvrez http://localhost:8000/tor-workflow/
```


## Pour Aller Plus Loin

Ces visualisations ne sont qu'une introduction. Pour approfondir chaque protocole :

- 🧅 [Tor Project](https://www.torproject.org/) - Documentation officielle du réseau TOR
- 🔐 [RFC 8446 - TLS 1.3](https://datatracker.ietf.org/doc/html/rfc8446) - Spécification complète
- 🌐 [RFC 8484 - DNS over HTTPS](https://datatracker.ietf.org/doc/html/rfc8484) - Standard DoH
- 🏛️ [NIST SP 800-207 - Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final) - Guide de référence


## Exploits et Vulnérabilités Connues

- **CVE-2020-8835** : Vulnérabilité dans le noyau Linux permettant une évasion de l'isolation réseau utilisée par TOR. Un attaquant local pouvait contourner les mécanismes de sandbox via une exploitation BPF.

- **CVE-2021-23961 (Firefox/Tor Browser)** : Faille dans la gestion des ports réseau permettant le fingerprinting des utilisateurs TOR via des requêtes vers des ports non-standards, compromettant l'anonymat.

- **CVE-2017-5715 (Spectre)** : Cette vulnérabilité matérielle affecte les implémentations TLS en permettant la lecture de secrets cryptographiques via des attaques par canal auxiliaire sur les processeurs.

- **CVE-2020-1971 (OpenSSL)** : Déni de service dans la vérification des certificats X.509, affectant les handshakes TLS et pouvant impacter les connexions HTTPS sécurisées.

- **CVE-2023-32784 (KeePass)** : Bien que non directement lié à TOR, cette vulnérabilité illustre l'importance du Zero Trust : même les gestionnaires de mots de passe locaux peuvent être compromis, justifiant la vérification systématique de chaque accès.


## Approfondissement Théorique

Le routage en oignon (Onion Routing) a été développé initialement par le Naval Research Laboratory américain dans les années 1990. Le concept repose sur le chiffrement en couches successives, où chaque noeud du réseau ne peut déchiffrer qu'une seule couche, révélant uniquement l'adresse du prochain saut. Cette architecture garantit qu'aucun noeud unique ne possède suffisamment d'informations pour corréler l'expéditeur et le destinataire d'un message.

L'évolution de TLS de la version 1.2 vers 1.3 représente une avancée majeure en termes de sécurité et de performance. TLS 1.3 a supprimé les algorithmes obsolètes (RSA key exchange, CBC mode ciphers, SHA-1), réduit le handshake de 2-RTT à 1-RTT, et introduit le 0-RTT pour les connexions de reprise. Le Perfect Forward Secrecy est désormais obligatoire, garantissant que la compromission d'une clé privée n'affecte pas les sessions passées.

L'architecture Zero Trust, popularisée par Google avec BeyondCorp et formalisée par le NIST SP 800-207, marque un changement de paradigme dans la sécurité réseau. Contrairement au modèle périmétrique traditionnel ("château fort"), le Zero Trust part du principe que le réseau interne est aussi hostile que l'externe. Chaque requête doit être authentifiée, autorisée et chiffrée, indépendamment de sa provenance. Cette approche s'est révélée particulièrement pertinente avec l'essor du télétravail et des architectures cloud hybrides.


---

