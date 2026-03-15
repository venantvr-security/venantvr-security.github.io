---
layout: default
title: "Python.Dome.SubDomains"
description: "DOME - Outil d'Énumération de Sous-domaines"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Dome.SubDomains</span>
</div>

<div class="page-header">
  <h1>Python.Dome.SubDomains</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Dome.SubDomains" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# DOME - Outil d'Énumération de Sous-domaines

> **AVERTISSEMENT** : Utilisez cet outil **uniquement** sur des domaines autorisés (programmes bug bounty, pentests contractualisés).

## Introduction : Pourquoi Énumérer les Sous-domaines ?

La phase de **reconnaissance** est cruciale dans tout test de sécurité. Un domaine principal comme `example.com` cache souvent des dizaines de sous-domaines : `admin.example.com`, `api.example.com`, `staging.example.com`, `dev.example.com`... Chacun de ces sous-domaines peut exposer des services différents, avec des niveaux de sécurité variables.

Les sous-domaines oubliés ou mal configurés sont une mine d'or pour les attaquants :
- **Environnements de test** exposés publiquement
- **Anciennes versions** d'applications avec des vulnérabilités connues
- **Panneaux d'administration** sans protection adéquate
- **Services internes** accidentellement exposés

### DOME : L'outil de référence

**DOME** (Domain Enumeration) est un outil rapide et fiable qui combine deux approches complémentaires pour maximiser la couverture :

| Mode | Technique | Détectable par la cible ? |
|------|-----------|---------------------------|
| **Passif** | Interrogation d'APIs OSINT | ❌ Non (totalement invisible) |
| **Actif** | Résolution DNS par bruteforce | ✅ Oui (génère du trafic DNS) |


## Architecture du Système

L'énumération passive interroge des sources publiques qui ont déjà indexé les sous-domaines (certificats SSL, moteurs de recherche, bases de données de sécurité). L'énumération active teste directement l'existence de sous-domaines via des requêtes DNS.

<div class="mermaid">
flowchart TB
    subgraph INPUT["📝 Entrée"]
        DOMAIN["example.com"]
    end

    subgraph PASSIVE["🔍 Mode Passif (OSINT)"]
        P1["VirusTotal"]
        P2["SecurityTrails"]
        P3["Censys"]
        P4["Shodan"]
        P5["crt.sh"]
    end

    subgraph ACTIVE["⚡ Mode Actif"]
        A1["Pure Bruteforce<br/>a-zzz.domain.com"]
        A2["Wordlist<br/>admin, api, dev..."]
        A3["DNS Resolution"]
    end

    subgraph OUTPUT["📊 Résultats"]
        O1["Sous-domaines trouvés"]
        O2["Scan de ports (optionnel)"]
    end

    DOMAIN --> PASSIVE & ACTIVE
    PASSIVE --> P1 & P2 & P3 & P4 & P5
    ACTIVE --> A1 & A2
    A1 & A2 --> A3
    P1 & P2 & P3 & P4 & P5 & A3 --> O1
    O1 --> O2

    style PASSIVE fill:#2ecc71,fill-opacity:0.15
    style ACTIVE fill:#e74c3c,fill-opacity:0.15
    style OUTPUT fill:#808080,fill-opacity:0.15
    style INPUT fill:#808080,fill-opacity:0.15
</div>

**Points clés** :
- Le mode passif est **invisible** : aucune requête n'est envoyée à la cible
- Le mode actif est **plus complet** mais génère du trafic DNS détectable
- Les deux modes peuvent être combinés pour une couverture maximale


## Flux de Travail Détaillé

Ce diagramme montre les deux phases d'énumération. Remarquez que le mode passif ne contacte jamais directement la cible, tandis que le mode actif envoie des requêtes DNS.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant U as 👤 Utilisateur
    participant D as 🔧 DOME
    participant API as 🌐 APIs OSINT
    participant DNS as 📡 DNS

    U->>D: dome.py -m passive -d target.com

    rect rgb(46, 204, 113, 0.2)
        Note over D,API: Mode Passif (Invisible)
        D->>API: Query crt.sh (certificats SSL)
        API-->>D: Sous-domaines des certificats
        D->>API: Query VirusTotal
        API-->>D: Sous-domaines indexés
    end

    U->>D: dome.py -m active -d target.com -w wordlist.txt

    rect rgb(231, 76, 60, 0.2)
        Note over D,DNS: Mode Actif (Détectable)
        D->>DNS: admin.target.com existe ?
        DNS-->>D: 192.168.1.10 (oui)
        D->>DNS: api.target.com existe ?
        DNS-->>D: NXDOMAIN (non)
        D->>DNS: dev.target.com existe ?
        DNS-->>D: 192.168.1.20 (oui)
    end

    D-->>U: Liste des sous-domaines vivants
</div>


## Utilisation

### Mode Passif : Reconnaissance Invisible

Le mode passif est idéal pour une première reconnaissance sans risque de détection. Il interroge uniquement des sources tierces.

```bash
# Énumération passive uniquement
python dome.py -m passive -d example.com

# Avec fichier de configuration des clés API
# (certaines APIs nécessitent une authentification)
python dome.py -m passive -d example.com --config config.api
```

### Mode Actif : Bruteforce DNS

Le mode actif teste directement l'existence de sous-domaines. Il est plus complet mais génère du trafic DNS visible.

```bash
# Bruteforce avec wordlist de noms courants
python dome.py -m active -d example.com -w wordlist.txt

# Désactiver le bruteforce pur (a, b, c... aa, ab, ac...)
python dome.py -m active -d example.com -w wordlist.txt --no-bruteforce

# Avec scan de ports sur les sous-domaines trouvés
python dome.py -m active -d example.com -w wordlist.txt -p
```


## Le Pure Bruteforce : La Force Brute

En plus des wordlists, DOME peut tester toutes les combinaisons de lettres de 1 à 3 caractères. C'est exhaustif mais chronophage.

<div class="mermaid">
flowchart LR
    subgraph Bruteforce["🔤 Pure Bruteforce"]
        B1["a.domain.com"]
        B2["b.domain.com"]
        B3["..."]
        B4["aa.domain.com"]
        B5["ab.domain.com"]
        B6["..."]
        B7["aaa.domain.com"]
    end

    subgraph Count["📊 Statistiques"]
        C1["26 (1 lettre)"]
        C2["676 (2 lettres)"]
        C3["17576 (3 lettres)"]
        T["Total: 18,278 combinaisons"]
    end

    B1 & B2 & B3 --> C1
    B4 & B5 & B6 --> C2
    B7 --> C3
    C1 & C2 & C3 --> T

    style T fill:#3498db,fill-opacity:0.15
    style Count fill:#808080,fill-opacity:0.15
    style Bruteforce fill:#808080,fill-opacity:0.15
</div>

**Astuce** : Commencez par le mode passif et une wordlist pour les résultats rapides. Utilisez le pure bruteforce uniquement si vous avez le temps et que la cible le justifie.


## Configuration des APIs (config.api)

Certaines sources OSINT nécessitent une clé API pour fonctionner. Créez un fichier `config.api` avec vos clés :

```ini
[virustotal]
api_key = your_api_key_here

[securitytrails]
api_key = your_api_key_here

[censys]
api_id = your_api_id
api_secret = your_api_secret

[shodan]
api_key = your_api_key_here
```

**Où obtenir ces clés ?**
- VirusTotal : gratuit, inscrivez-vous sur virustotal.com
- SecurityTrails : offre gratuite limitée
- Censys : compte académique ou commercial
- Shodan : compte gratuit avec quota limité


## Exemple de Sortie

Voici ce que vous verrez lors d'une exécution typique :

```
[*] Starting DOME - Subdomain Enumeration Tool
[*] Target: example.com
[*] Mode: Active + Passive

[+] Passive énumération...
    [crt.sh] Found 45 subdomains from SSL certificates
    [VirusTotal] Found 23 subdomains
    [SecurityTrails] Found 67 subdomains

[+] Active bruteforce...
    [wordlist] Testing 10000 entries from subdomains.txt
    [bruteforce] Testing a-zzz (18278 combinations)

[+] Resolving DNS for all candidates...
    [DNS] 127 unique candidates to resolve

[+] Results:
    admin.example.com     -> 192.168.1.10
    api.example.com       -> 192.168.1.20
    dev.example.com       -> 192.168.1.30
    staging.example.com   -> 192.168.1.40
    mail.example.com      -> 192.168.1.50
    ...

[*] Total: 127 unique subdomains found
[*] Saved to: results/example.com.txt
```


## Pour Aller Plus Loin

- 🔗 [GitHub DOME Original](https://github.com/v4d1/Dome) - Dépôt source de l'outil
- 📚 [OWASP Enumeration Guide](https://owasp.org/www-project-web-security-testing-guide/) - Méthodologie de test
- 🎯 [Subdomain Takeover](https://www.hackerone.com/ethical-hacker/guide-subdomain-takeovers) - Exploitation des sous-domaines abandonnés


## Exploits et Vulnérabilités Connues

- **Subdomain Takeover Microsoft (2020)** : Des chercheurs ont découvert plus de 670 sous-domaines Microsoft vulnérables au takeover, pointant vers des services Azure, S3, ou GitHub Pages non revendiqués. Impact potentiel : phishing crédible sous domaine microsoft.com.

- **CVE-2021-21315 (Node.js systeminformation)** : L'énumération de sous-domaines a permis de découvrir des instances de monitoring exposant cette vulnérabilité d'injection de commandes sur des sous-domaines oubliés.

- **Uber Subdomain Takeover (2016)** : saostatic.uber.com pointait vers un bucket S3 non revendiqué. Un chercheur a pu prendre le contrôle et démontrer un risque de phishing. Bounty : 2,500 USD.

- **CVE-2020-8193 (Citrix Gateway)** : L'énumération de sous-domaines a révélé des instances Citrix ADC/Gateway vulnérables sur des sous-domaines de staging non protégés de grandes entreprises.

- **Starbucks Subdomain Takeover (2019)** : Plusieurs sous-domaines Starbucks pointaient vers des services Heroku désactivés, permettant le takeover et le potentiel vol de cookies via scope de domaine parent.


## Approfondissement Théorique

L'énumération de sous-domaines est une technique de reconnaissance fondamentale classifiée dans la phase "Information Gathering" du PTES (Penetration Testing Execution Standard) et de l'OWASP Testing Guide. Elle exploite le fait que les organisations modernes utilisent des centaines de sous-domaines pour différents services, et que la gestion de ce périmètre est souvent lacunaire.

Les sources passives comme Certificate Transparency (crt.sh) sont particulièrement puissantes car elles indexent tous les certificats SSL émis. Depuis 2018, les Certificate Authorities doivent obligatoirement publier leurs certificats dans des logs CT, ce qui signifie que tout sous-domaine ayant un certificat SSL est automatiquement révélé. Les attaquants et les défenseurs utilisent ces mêmes sources pour cartographier le périmètre d'une organisation.

Le "subdomain takeover" est une vulnérabilité critique qui survient lorsqu'un enregistrement DNS (CNAME) pointe vers un service externe (S3, Azure, Heroku, etc.) qui n'est plus actif ou n'a pas été revendiqué. Un attaquant peut alors créer une ressource sur le service ciblé et servir du contenu malveillant sous le domaine légitime de la victime. Les impacts incluent : vol de cookies (si le scope inclut le domaine parent), phishing crédible, atteinte à la réputation, et dans certains cas, compromission de l'authentification SSO.


---

