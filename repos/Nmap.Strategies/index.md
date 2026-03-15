---
layout: default
title: "Nmap.Strategies"
description: "Scripts NSE pour Tests IDS/IPS"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Nmap.Strategies</span>
</div>

<div class="page-header">
  <h1>Nmap.Strategies</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Nmap.Strategies" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Scripts NSE pour Tests IDS/IPS

> **AVERTISSEMENT** : Utilisez ces scripts **uniquement** sur des systèmes autorisés. L'utilisation non autorisée est illégale.

## Introduction : Le Nmap Scripting Engine

Nmap est bien plus qu'un simple scanner de ports. Son **Nmap Scripting Engine (NSE)** permet d'exécuter des scripts Luà personnalisés pour automatiser des tâches complexes : détection de vulnérabilités, énumération de services, tests d'authentification, et bien plus.

Ce projet est une collection de scripts NSE organisés par catégorie, spécialement conçus pour **tester les systèmes de détection et prévention d'intrusion (IDS/IPS)**. L'objectif est double : vérifier que vos défenses détectent bien les attaques connues, et identifier les techniques d'évasion qui pourraient passer inaperçues.

### Système de classification des risques

Chaque script est accompagné d'un flag de risque pour vous aider à l'utiliser de manière appropriée :

| Flag | Signification | Quand l'utiliser |
|------|---------------|------------------|
| 🟢 | **Safe** | Reconnaissance passive, aucun impact |
| 🟠 | **Prudence** | Peut déclencher des alertes IDS |
| 🔴 | **Dangereux** | Peut causer des dommages, autorisation écrite obligatoire |


## Organisation du Projet

Le projet est structuré en cinq catégories, chacune ciblant un aspect différent des tests de sécurité. Le diagramme ci-dessous montre l'arborescence complète avec les niveaux de risque de chaque script.

<div class="mermaid">
flowchart TB
    subgraph RECON["🔍 reconnaissance/"]
        R1["🟢 port-scan.nse"]
        R2["🟢 version-détection.nse"]
        R3["🟠 service-enum.nse"]
    end

    subgraph EVASION["🥷 evasion/"]
        E1["🟠 tcp-fragmentation.nse"]
        E2["🟠 tcp-options-malformed.nse"]
        E3["🟠 timing-evasion.nse"]
        E4["🟠 decoy-scan.nse"]
    end

    subgraph BRUTE["🔓 bruteforce/"]
        B1["🔴 ssh-brute.nse"]
        B2["🔴 http-auth-brute.nse"]
        B3["🔴 wp-login-brute.nse"]
    end

    subgraph FUZZ["💥 fuzzing/"]
        F1["🟠 http-fuzz.nse"]
        F2["🟠 url-length-fuzz.nse"]
        F3["🔴 header-injection.nse"]
    end

    subgraph DOS["⚠️ dos/"]
        D1["🔴 slowloris.nse"]
        D2["🔴 syn-flood.nse"]
        D3["🔴 resource-exhaustion.nse"]
    end

    style R1 fill:#2ecc71,fill-opacity:0.15
    style R2 fill:#2ecc71,fill-opacity:0.15
    style R3 fill:#f39c12,fill-opacity:0.15
    style E1 fill:#f39c12,fill-opacity:0.15
    style E2 fill:#f39c12,fill-opacity:0.15
    style E3 fill:#f39c12,fill-opacity:0.15
    style E4 fill:#f39c12,fill-opacity:0.15
    style B1 fill:#e74c3c,fill-opacity:0.15
    style B2 fill:#e74c3c,fill-opacity:0.15
    style B3 fill:#e74c3c,fill-opacity:0.15
    style F1 fill:#f39c12,fill-opacity:0.15
    style F2 fill:#f39c12,fill-opacity:0.15
    style F3 fill:#e74c3c,fill-opacity:0.15
    style D1 fill:#e74c3c,fill-opacity:0.15
    style D2 fill:#e74c3c,fill-opacity:0.15
    style D3 fill:#e74c3c,fill-opacity:0.15
    style DOS fill:#808080,fill-opacity:0.15
    style FUZZ fill:#808080,fill-opacity:0.15
    style BRUTE fill:#808080,fill-opacity:0.15
    style EVASION fill:#808080,fill-opacity:0.15
    style RECON fill:#808080,fill-opacity:0.15
</div>


## Les Catégories en Détail

Chaque catégorie de scripts répond à un besoin spécifique dans le cycle de test de sécurité. Comprendre leur rôle vous aidera à choisir les bons outils pour chaque situation.

<div class="mermaid">
flowchart LR
    subgraph Categories["📂 Catégories"]
        direction TB
        RECON["🔍 Reconnaissance"]
        EVASION["🥷 Évasion"]
        BRUTE["🔓 Bruteforce"]
        FUZZ["💥 Fuzzing"]
        DOS["⚠️ DoS"]
    end

    subgraph Usage["🎯 Cas d'usage"]
        U1["Découverte d'actifs"]
        U2["Contournement IDS"]
        U3["Test d'authentification"]
        U4["Recherche de vulnérabilités"]
        U5["Test de résilience"]
    end

    RECON --> U1
    EVASION --> U2
    BRUTE --> U3
    FUZZ --> U4
    DOS --> U5

    style RECON fill:#2ecc71,fill-opacity:0.15
    style EVASION fill:#3498db,fill-opacity:0.15
    style BRUTE fill:#e74c3c,fill-opacity:0.15
    style FUZZ fill:#f39c12,fill-opacity:0.15
    style DOS fill:#9b59b6,fill-opacity:0.15
    style Usage fill:#808080,fill-opacity:0.15
    style Categories fill:#808080,fill-opacity:0.15
</div>


## Installation

Les scripts NSE doivent être placés dans le répertoire approprié pour que Nmap les reconnaisse. Voici la procédure :

```bash
# Cloner le projet
git clone https://github.com/venantvr-security/Nmap.Strategies ~/nmap-stratégies

# Copier les scripts dans le répertoire Nmap
sudo cp -r ~/nmap-stratégies/* /usr/share/nmap/scripts/

# Mettre à jour la base de données de scripts
# (nécessaire pour que Nmap indexe les nouveaux scripts)
sudo nmap --script-updatedb
```


## Utilisation des Scripts

### Exécution d'un script unique

Pour lancer un script spécifique contre une cible :

```bash
nmap --script=/path/to/script.nse <target>
```

### Exécution d'une catégorie entière

Pour tester tous les scripts d'une catégorie (par exemple, tous les scripts d'évasion) :

```bash
nmap --script=/path/to/evasion/*.nse <target>
```

### Avec des options avancées

Certains scripts acceptent des arguments pour personnaliser leur comportement :

```bash
nmap -sS -p 80,443 \
  --script=http-fuzz.nse \
  --script-args="fuzz.payloads=100" \
  <target>
```


## Techniques d'Évasion IDS : Exemples Concrets

Les scripts de la catégorie "evasion" sont particulièrement intéressants pour tester les capacités de détection de vos IDS. Voici deux techniques classiques et leur fonctionnement.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant N as 🔧 Nmap
    participant IDS as 🛡️ IDS
    participant T as 🎯 Target

    rect rgb(52, 152, 219, 0.2)
        Note over N,T: Fragmentation TCP
        N->>T: Fragment 1 (8 bytes)
        N->>T: Fragment 2 (8 bytes)
        N->>T: Fragment 3 (8 bytes)
        IDS-->>IDS: Réassemblage difficile
    end

    rect rgb(241, 196, 15, 0.2)
        Note over N,T: Timing Evasion
        N->>T: Packet 1
        Note over N: Wait 5s
        N->>T: Packet 2
        Note over N: Wait 3s
        N->>T: Packet 3
        IDS-->>IDS: Timeout détection
    end
</div>

### Fragmentation TCP

La fragmentation divise les paquets en morceaux si petits que l'IDS peut avoir du mal à les réassembler correctement :

```bash
# Double fragmentation (fragments de 8 bytes)
nmap -f -f --script=tcp-fragmentation.nse target
```

### Évasion temporelle

En ralentissant le scan, on espère que l'IDS ne corrélera pas les paquets entre eux :

```bash
# Mode "paranoid" : un paquet toutes les 5 minutes
nmap -T0 --script=timing-evasion.nse target
```

### Scans leurres (Decoys)

Les decoys envoient des paquets depuis des adresses IP falsifiées, noyant la vraie source dans le bruit :

```bash
# 5 adresses IP aléatoires comme leurres
nmap -D RND:5 --script=decoy-scan.nse target
```


## Scripts de Bruteforce (🔴 Autorisation Requise)

Ces scripts tentent des connexions avec des listes de mots de passe. **Ne les utilisez jamais sans autorisation écrite explicite**.

```bash
# Bruteforce SSH
nmap --script=ssh-brute.nse \
  --script-args="userdb=users.txt,passdb=pass.txt" \
  -p 22 target

# Bruteforce HTTP Basic Auth
nmap --script=http-auth-brute.nse \
  -p 80 target

# Bruteforce WordPress
nmap --script=wp-login-brute.nse \
  --script-args="wp.users=admin" \
  -p 80 target
```


## Intégration avec le Laboratoire IDS

Ces scripts sont conçus pour fonctionner avec le laboratoire Docker du projet **Rust.Nmap.Network**, qui fournit des instances Snort et Suricata prêtes à l'emploi.

```bash
# 1. Démarrer tous les labs
cd ../Rust.Nmap.Network
./start_all_labs.sh

# 2. Tester contre Snort
nmap --script=evasion/*.nse 172.28.0.100

# 3. Tester contre Suricata
nmap --script=evasion/*.nse 172.29.0.100

# 4. Vérifier les alertes générées
# Ouvrez EveBox : http://localhost:5636
```


## Pour Aller Plus Loin

Les scripts NSE ouvrent des possibilités infinies. Voici quelques ressources pour approfondir :

- 📚 [Nmap Scripting Engine](https://nmap.org/book/nse.html) - Guide officiel
- 📖 [NSE Documentation](https://nmap.org/nsedoc/) - Référence de tous les scripts
- 🔓 [Nmap Firewall Evasion](https://nmap.org/book/firewall-subversion.html) - Techniques avancées
- 🛡️ [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) - Méthodologie de test


## Exploits et Vulnérabilités Connues

- **CVE-2021-44228 (Log4Shell)** : Vulnérabilité critique dans Apache Log4j détectable via Nmap. Les scripts NSE peuvent identifier les serveurs vulnérables en analysant les headers et les réponses des services Java exposés.

- **CVE-2017-0144 (EternalBlue/MS17-010)** : Faille SMBv1 exploitée par WannaCry. Le script `smb-vuln-ms17-010.nse` de Nmap permet de détecter cette vulnérabilité critique sur les systèmes Windows non patchés.

- **CVE-2014-0160 (Heartbleed)** : Vulnérabilité OpenSSL permettant la fuite de mémoire serveur. Le script `ssl-heartbleed.nse` détecte les serveurs encore vulnérables à cette faille historique.

- **CVE-2019-11510 (Pulse Secure VPN)** : Lecture arbitraire de fichiers sur les VPN Pulse Secure. Les scans Nmap de version permettent d'identifier les instances vulnérables via la détection de version des services SSL/TLS.

- **CVE-2020-1938 (Ghostcat/Apache Tomcat AJP)** : Lecture de fichiers via le protocole AJP. Le scan du port 8009 avec détection de version permet d'identifier les serveurs Tomcat exposant ce service vulnérable.


## Approfondissement Théorique

Le Nmap Scripting Engine représente une évolution majeure de Nmap, transformant un simple scanner de ports en une plateforme d'audit de sécurité complète. Les scripts NSE sont écrits en Lua, un langage léger et extensible, et peuvent accéder à une API riche permettant l'interaction avec les services réseau, le parsing de protocoles, et même l'exploitation contrôlée de vulnérabilités.

Les techniques d'évasion IDS implémentées dans ces scripts reposent sur des principes fondamentaux de la détection d'intrusion. La fragmentation IP exploite le fait que certains IDS ne réassemblent pas correctement les paquets fragmentés. L'évasion temporelle tire parti des timeouts de corrélation : si un IDS ne peut pas associer des paquets espacés dans le temps, il ne détectera pas le scan. Les decoys brouillent l'analyse en générant du trafic depuis de fausses adresses IP, rendant difficile l'identification de la vraie source.

La méthodologie de test IDS/IPS suit généralement le framework OWASP et les recommandations du NIST SP 800-115. L'objectif n'est pas de contourner les défenses en production, mais de valider leur efficacité. Un IDS correctement configuré devrait détecter les techniques documentées (scan SYN, détection de version agressive), tandis que les techniques d'évasion permettent d'identifier les angles morts nécessitant un renforcement des règles de détection.


---

