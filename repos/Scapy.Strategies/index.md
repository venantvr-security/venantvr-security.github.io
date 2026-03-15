---
layout: default
title: "Scapy.Strategies"
description: "Manipulation de Paquets IP pour Tests IDS"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Scapy.Strategies</span>
</div>

<div class="page-header">
  <h1>Scapy.Strategies</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Scapy.Strategies" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Manipulation de Paquets IP pour Tests IDS

> **AVERTISSEMENT** : Utilisez ces scripts **uniquement** sur des systèmes autorisés. L'utilisation non autorisée est illégale.

## Introduction : Pourquoi Tester les IDS ?

Les systèmes de détection d'intrusion (IDS) comme Snort ou Suricata sont essentiels pour la sécurité réseau. Mais comment savoir s'ils détectent vraiment toutes les menaces ? Les attaquants sophistiqués utilisent des techniques d'**évasion** pour contourner ces systèmes, et il est crucial de tester leur efficacité.

**Scapy** est une bibliothèque Python puissante qui permet de créer, manipuler et envoyer des paquets réseau à bas niveau. Contrairement aux outils classiques qui génèrent des paquets "normaux", Scapy permet de créer des paquets **malformés**, **fragmentés** ou avec des **flags inhabituels** - exactement ce dont nous avons besoin pour tester la robustesse d'un IDS.

### Ce que ce projet permet de faire

Ce projet est une collection de scripts Scapy documentés, organisés par technique d'évasion. Chaque script est annoté avec son niveau de risque et son efficacité attendue contre différents IDS. L'objectif n'est pas l'attaque, mais l'**amélioration des capacités de détection**.

### Système de classification des risques

Pour vous aider à utiliser ces scripts de manière responsable, nous utilisons un système de flags :

| Flag | Niveau | Description | Utilisation |
|------|--------|-------------|-------------|
| 🟢 | Safe | Reconnaissance passive | Peut être utilisé sans risque |
| 🟠 | Prudence | Manipulation active | Autorisation écrite requise |
| 🔴 | Dangereux | Techniques d'attaque | Environnement contrôlé uniquement |


## Organisation du Projet

Le projet est structuré par catégorie de technique. Chaque dossier contient des scripts ciblant un aspect spécifique de l'évasion IDS. Le diagramme ci-dessous montre l'arborescence complète avec les niveaux de risque associés.

<div class="mermaid">
flowchart TB
    subgraph FRAG["📦 fragmentation/"]
        F1["🟠 ip_fragment.py"]
        F2["🟠 overlapping.py"]
        F3["🟠 tiny_fragments.py"]
    end

    subgraph FLAGS["🚩 flags/"]
        FL1["🟠 tcp_flags.py"]
        FL2["🟠 invalid_combinations.py"]
        FL3["🟠 christmas_tree.py"]
    end

    subgraph TIMING["⏱️ timing/"]
        T1["🟠 slow_scan.py"]
        T2["🟢 jitter.py"]
        T3["🟠 burst.py"]
    end

    subgraph PROTO["📡 protocol/"]
        P1["🟠 icmp_tunnel.py"]
        P2["🔴 dns_exfil.py"]
        P3["🟠 protocol_switch.py"]
    end

    subgraph ADV["🎯 advanced/"]
        A1["🟠 ttl_manipulation.py"]
        A2["🟠 ip_options.py"]
        A3["🔴 covert_channel.py"]
    end

    style F1 fill:#f39c12,fill-opacity:0.15
    style F2 fill:#f39c12,fill-opacity:0.15
    style F3 fill:#f39c12,fill-opacity:0.15
    style FL1 fill:#f39c12,fill-opacity:0.15
    style FL2 fill:#f39c12,fill-opacity:0.15
    style FL3 fill:#f39c12,fill-opacity:0.15
    style T1 fill:#f39c12,fill-opacity:0.15
    style T2 fill:#2ecc71,fill-opacity:0.15
    style T3 fill:#f39c12,fill-opacity:0.15
    style P1 fill:#f39c12,fill-opacity:0.15
    style P2 fill:#e74c3c,fill-opacity:0.15
    style P3 fill:#f39c12,fill-opacity:0.15
    style A1 fill:#f39c12,fill-opacity:0.15
    style A2 fill:#f39c12,fill-opacity:0.15
    style A3 fill:#e74c3c,fill-opacity:0.15
    style ADV fill:#808080,fill-opacity:0.15
    style PROTO fill:#808080,fill-opacity:0.15
    style TIMING fill:#808080,fill-opacity:0.15
    style FLAGS fill:#808080,fill-opacity:0.15
    style FRAG fill:#808080,fill-opacity:0.15
</div>


## Les Techniques d'Évasion Expliquées

Chaque catégorie de scripts cible une faiblesse potentielle des IDS. Comprendre ces techniques permet de mieux configurer vos systèmes de détection.

<div class="mermaid">
flowchart LR
    subgraph Techniques["🔧 Catégories"]
        direction TB
        FRAG["Fragmentation IP"]
        FLAGS["Flags TCP"]
        TIMING["Temporisation"]
        PROTO["Protocole"]
        ADV["Avancé"]
    end

    subgraph IDS["🛡️ Détection IDS"]
        SNORT["Snort"]
        SURI["Suricata"]
        ZEEK["Zeek"]
    end

    subgraph Result["Efficacité"]
        HARD["🔴 Difficile"]
        MED["🟡 Moyen"]
        EASY["🟢 Facile"]
    end

    FRAG --> HARD
    FLAGS --> MED
    TIMING --> HARD
    PROTO --> HARD
    ADV --> HARD

    style FRAG fill:#3498db,fill-opacity:0.15
    style FLAGS fill:#9b59b6,fill-opacity:0.15
    style TIMING fill:#e74c3c,fill-opacity:0.15
    style PROTO fill:#f39c12,fill-opacity:0.15
    style ADV fill:#2c3e50,fill-opacity:0.15
    style Result fill:#808080,fill-opacity:0.15
    style IDS fill:#808080,fill-opacity:0.15
    style Techniques fill:#808080,fill-opacity:0.15
</div>

### 1. Fragmentation IP : Diviser pour mieux régner

Lorsqu'un paquet IP est trop grand, il est **fragmenté** en plusieurs morceaux. Le problème : certains IDS analysent chaque fragment séparément et peuvent rater la signature de l'attaque qui n'apparaît que dans le paquet réassemblé.

```python
from scapy.all import *

def fragment_packet(target, payload):
    """
    Fragmente un paquet en micro-fragments.

    Stratégie : L'en-tête TCP se retrouve dans un fragment,
    et le payload malveillant dans un autre. Un IDS qui ne
    réassemble pas correctement ratera la signature.
    """
    ip = IP(dst=target, flags="MF")  # MF = More Fragments

    # Fragment 1: En-tête TCP seulement (pas de payload suspect)
    frag1 = ip/TCP(dport=80, flags="S")
    frag1[IP].frag = 0

    # Fragment 2: Suite des données (contient le payload)
    frag2 = ip/Raw(payload[:8])
    frag2[IP].frag = 1

    send([frag1, frag2])
```

### 2. Le Christmas Tree Scan : Allumer tous les voyants

Le "Christmas Tree Scan" tire son nom du fait qu'il active **tous les flags TCP** simultanément, comme un sapin de Noël illuminé. Cette combinaison est illégale selon les spécifications TCP, mais certaines implémentations réseau y répondent de manière prévisible, révélant des informations sur les ports ouverts.

```python
from scapy.all import *

def xmas_scan(target, port):
    """
    Scan avec tous les flags TCP activés.

    Le paquet résultant est clairement anormal et devrait
    être détecté par tout IDS correctement configuré.
    Si ce n'est pas le cas, c'est une faille à corriger.
    """
    pkt = IP(dst=target)/TCP(
        dport=port,
        flags="FSRPAUEC"  # FIN, SYN, RST, PSH, ACK, URG, ECE, CWR
    )
    resp = sr1(pkt, timeout=2)
    return resp
```

### 3. Timing avec Jitter : La patience de l'attaquant

Les IDS détectent souvent les scans par leur **régularité**. Un scan qui envoie exactement un paquet par seconde est suspect. En ajoutant un délai aléatoire (jitter), le trafic devient plus difficile à distinguer du bruit normal.

```python
import random
import time
from scapy.all import *

def slow_scan_jitter(target, ports):
    """
    Scan lent avec variation aléatoire du timing.

    Un IDS qui corrèle les évènements dans une fenêtre de temps
    fixe peut rater ce type de scan étalé sur plusieurs minutes.
    """
    for port in ports:
        pkt = IP(dst=target)/TCP(dport=port, flags="S")
        send(pkt, verbose=0)

        # Jitter: délai aléatoire entre 1 et 10 secondes
        delay = random.uniform(1, 10)
        time.sleep(delay)
```


## Intégration avec un Laboratoire IDS

Ces scripts prennent tout leur sens lorsqu'ils sont utilisés dans un environnement de test avec un véritable IDS. Le projet **Rust.Nmap.Network** fournit un laboratoire Docker complet avec Snort et Suricata.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant S as 🐍 Scapy Script
    participant L as 🔬 IDS Lab
    participant IDS as 🛡️ Snort/Suricata
    participant E as 📊 EveBox

    S->>L: sudo python3 ip_fragment.py 172.29.0.100
    L->>IDS: Paquets fragmentés

    alt Détecté
        IDS->>E: Alerte générée
        E->>E: Afficher alerte
    else Non détecté
        IDS->>IDS: Pas d'alerte
        Note over S: Évasion réussie
    end
</div>

### Mise en pratique

Voici comment tester vos scripts contre le laboratoire IDS :

```bash
# 1. Démarrer le laboratoire Suricata
cd ../Rust.Nmap.Network/suricata-lab
docker compose up -d

# 2. Lancer un script de test d'évasion
cd ../Scapy.Strategies
sudo python3 fragmentation/ip_fragment.py 172.29.0.100

# 3. Observer les résultats dans EveBox
# Ouvrez http://localhost:5636 dans votre navigateur
# Si aucune alerte n'apparaît, l'évasion a réussi !
```


## Installation et Prérequis

Scapy nécessite des privilèges root car il crée des "raw sockets" pour envoyer des paquets arbitraires. Voici comment l'installer et le configurer :

```bash
# Installation de Scapy
pip install scapy

# Méthode 1: Exécution avec sudo (recommandé)
sudo python3 script.py

# Méthode 2: Ajouter les capabilities (évite sudo à chaque fois)
sudo setcap cap_net_raw+ep $(which python3)
```


## Pour Aller Plus Loin

La manipulation de paquets est un domaine vaste. Voici quelques ressources pour approfondir :

- 📚 [Documentation Scapy](https://scapy.readthedocs.io/) - La référence officielle
- 🔓 [Techniques d'évasion IDS (Nmap)](https://nmap.org/book/firewall-subversion.html) - Guide détaillé
- 🛡️ [MITRE ATT&CK - Defense Evasion](https://attack.mitre.org/tactics/TA0005/) - Framework de classification


## Exploits et Vulnérabilités Connues

La manipulation de paquets a été utilisée dans de nombreuses attaques historiques exploitant des failles de pile réseau :

| CVE | Produit | Description | Score CVSS |
|-----|---------|-------------|------------|
| **CVE-2020-16898** | Windows TCP/IP (Bad Neighbor) | Execution de code via paquets ICMPv6 malformés, exploitable avec Scapy | 9.8 Critique |
| **CVE-2021-24086** | Windows TCP/IP | DoS via fragmentation IPv4/IPv6 crafted packets | 7.5 Élevé |
| **CVE-2019-11477** | Linux Kernel (SACK Panic) | Panic kernel via séquence TCP SACK crafted, reproductible avec Scapy | 7.5 Élevé |
| **CVE-2008-4609** | TCP/IP Stacks (multiples) | Sockstress - DoS via manipulation des fenêtres TCP | 7.8 Élevé |
| **CVE-1999-0016** | TCP/IP (Land Attack) | Paquet TCP avec source = destination causant une boucle infinie | 5.0 Moyen |

La vulnérabilité **Bad Neighbor** (CVE-2020-16898) est particulièrement notable car elle permet l'exécution de code à distance sur Windows 10 et Server 2019 via un simple paquet ICMPv6. Des PoC utilisant Scapy ont été publiés peu après la divulgation.


## Approfondissement Théorique

### L'anatomie des paquets et les points d'injection

Chaque couche du modèle OSI offre des opportunités de manipulation. Au niveau **IP** (couche 3), les options IP rarement utilisées (source routing, record route) peuvent confondre les équipements réseau. Le champ **TTL** peut être manipulé pour créer des "TTL bombs" qui atteignent un IDS mais pas la cible finale. Au niveau **TCP** (couche 4), les numéros de séquence, les flags, et les options (MSS, Window Scale, SACK) peuvent être modifiés pour créer des comportements inattendus. La beauté de Scapy est qu'il permet de construire des paquets totalement arbitraires, sans les contraintes imposées par les piles TCP/IP standard.

### La fragmentation IP : un problème fondamental

La fragmentation IP est l'une des techniques d'évasion les plus efficaces car elle exploite une ambiguïté inhérente au protocole. Quand un paquet est fragmenté, chaque fragment peut prendre un chemin différent à travers le réseau, arrivant dans n'importe quel ordre. L'hôte de destination réassemble les fragments, mais un IDS interceptant le trafic doit faire de même. Les **fragments chevauchants** (overlapping fragments) posent un problème particulier : si le fragment 2 réécrit partiellement le fragment 1, quelle version l'hôte final utilisera-t-il ? Windows et Linux font des choix différents, permettant des attaques de type "IDS evasion". Les **micro-fragments** (fragments de 8 octets) répartissent l'en-tête TCP sur plusieurs fragments, rendant impossible la lecture des ports source/destination sans réassemblage.

### Les covert channels et l'exfiltration de données

Au-delà de l'évasion IDS, Scapy permet de créer des **canaux cachés** (covert channels) pour exfiltrer des données discrètement. Les données peuvent être encodées dans des champs normalement inutilisés (IP ID, TCP séquence numbers, ICMP payload), dans le timing entre paquets, ou dans les réponses DNS. Le protocole **ICMP** est particulièrement intéressant : le ping-pong requête/réponse est généralement autorisé par les pare-feux, et le payload ICMP peut contenir des données arbitraires. Des outils comme **ptunnel** et **iodine** exploitent ces techniques pour tunneler du trafic TCP sur DNS ou ICMP, contournant les restrictions réseau les plus strictes.


---

