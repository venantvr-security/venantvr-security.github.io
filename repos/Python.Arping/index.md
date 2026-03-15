---
layout: default
title: "Python.Arping"
description: "Scanner de Réseau ARP avec Scapy"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Arping</span>
</div>

<div class="page-header">
  <h1>Python.Arping</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Arping" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Scanner de Réseau ARP avec Scapy

## Introduction : Découvrir les Appareils sur votre Réseau

Vous êtes-vous déjà demandé combien d'appareils sont connectés à votre réseau local ? Ordinateurs, téléphones, imprimantes, objets connectés... Ce script Python utilise le protocole **ARP** (Address Resolution Protocol) pour découvrir rapidement tous les hôtes actifs sur votre réseau.

### Pourquoi ARP ?

Le protocole ARP est la méthode la plus fiable pour découvrir des appareils sur un réseau local car :

- **Il fonctionne au niveau 2** (couche liaison) : même les pare-feux qui bloquent ICMP (ping) ne peuvent pas bloquer ARP
- **Il est obligatoire** : tout appareil qui veut communiquer sur Ethernet doit répondre aux requêtes ARP
- **Il révèle l'adresse MAC** : permet d'identifier le fabricant de l'appareil

### Ce que fait ce script

| Fonctionnalité     | Description                                       |
| ------------------ | ------------------------------------------------- |
| Découverte d'hôtes | Scanne une plage IP complète (ex: 192.168.1.0/24) |
| Requêtes ARP       | Envoie des paquets broadcast bas niveau           |
| Affichage IP/MAC   | Associe chaque IP à son adresse MAC physique      |
| Léger et rapide    | Utilise Scapy pour des performances optimales     |

## Comment Fonctionne ARP

Avant de plonger dans le code, comprenons le mécanisme sous-jacent. Une requête ARP est un message broadcast qui demande "Qui possède cette adresse IP ?". Tous les appareils du réseau reçoivent la question, mais seul celui qui possède l'IP répond.

<div class="mermaid">
flowchart LR
    subgraph Scanner["🖥️ Scanner"]
        S1["Python + Scapy"]
    end

    subgraph Network["🌐 Réseau Local"]
        ARP["📡 ARP Broadcast"]
        H1["📱 192.168.1.10"]
        H2["💻 192.168.1.20"]
        H3["🖨️ 192.168.1.30"]
    end
    
    subgraph Result["📊 Résultat"]
        R1["IP → MAC"]
    end
    
    S1 -->|"Who has 192.168.1.x?"| ARP
    ARP --> H1 & H2 & H3
    H1 & H2 & H3 -->|"I am 192.168.1.x at AA:BB:CC:DD:EE:FF"| S1
    S1 --> R1
    
    style ARP fill:#f39c12,fill-opacity:0.15
    style R1 fill:#2ecc71,fill-opacity:0.15
    style Result fill:#808080,fill-opacity:0.15
    style Network fill:#808080,fill-opacity:0.15
    style Scanner fill:#808080,fill-opacity:0.15

</div>

## Processus de Découverte en Détail

Le diagramme de séquence ci-dessous montre les trois étapes du scan : création du paquet ARP, envoi en broadcast, et collecte des réponses.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant S as 🖥️ Scanner
    participant N as 🌐 Réseau (Broadcast)
    participant H as 📱 Hôte actif

    rect rgb(52, 152, 219, 0.2)
        Note over S: Étape 1: Création du paquet
        S->>S: Ether(dst="ff:ff:ff:ff:ff:ff")
        S->>S: ARP(pdst="192.168.1.0/24")
    end
    
    rect rgb(46, 204, 113, 0.2)
        Note over S,N: Étape 2: Envoi et réception
        S->>N: ARP Request (broadcast)
        N->>H: Qui a cette IP?
        H-->>S: ARP Reply (IP + MAC)
    end
    
    rect rgb(155, 89, 182, 0.2)
        Note over S: Étape 3: Analyse
        S->>S: Collecter toutes les réponses
        S->>S: Construire le tableau IP/MAC
    end

</div>

## Le Script Python

Ce script utilise Scapy pour créer et envoyer des paquets ARP. La fonction `srp` (send and receive packets) gère automatiquement l'envoi et la collecte des réponses.

```python
from scapy.all import ARP, Ether, srp

def scan_network(target_ip):
    """
    Scanne le réseau et retourne les hôtes actifs.

    Le scan fonctionne en envoyant des requêtes ARP broadcast
    à toutes les adresses de la plage spécifiée. Seuls les
    appareils présents répondront avec leur adresse MAC.

    Args:
        target_ip: Plage IP au format CIDR (ex: "192.168.1.0/24")

    Returns:
        Liste de dictionnaires {ip, mac} pour chaque hôte trouvé
    """
    # Créer la trame Ethernet broadcast
    # dst="ff:ff:ff:ff:ff:ff" signifie "tous les appareils"
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Créer le paquet ARP
    # pdst = destination IP (la plage à scanner)
    arp = ARP(pdst=target_ip)

    # Combiner les deux couches
    packet = ether / arp

    # Envoyer et recevoir les réponses
    # timeout=3 : attendre 3 secondes max
    # verbose=0 : pas d'affichage Scapy
    result = srp(packet, timeout=3, verbose=0)[0]

    # Extraire les informations des réponses
    devices = []
    for sent, received in result:
        devices.append({
            'ip': received.psrc,    # IP source de la réponse
            'mac': received.hwsrc   # MAC source de la réponse
        })

    return devices


if __name__ == "__main__":
    target = "192.168.1.0/24"
    print(f"🔍 Scanning {target}...")

    devices = scan_network(target)

    print("\n📱 Available devices in the network:")
    print("IP\t\t\tMAC")
    print("-" * 40)
    for device in devices:
        print(f"{device['ip']}\t\t{device['mac']}")

    print(f"\n✅ Found {len(devices)} devices")
```

## Exemple de Sortie

Voici ce que vous verrez en exécutant le script sur un réseau domestique typique :

```
🔍 Scanning 192.168.1.0/24...

📱 Available devices in the network:
IP                 MAC
----------------------------------------
192.168.1.1        0a:1b:2c:3d:4e:5f    (Router)
192.168.1.102      a1:b2:c3:d4:e5:f6    (Phone)
192.168.1.134      10:20:30:40:50:60    (Laptop)
192.168.1.150      aa:bb:cc:dd:ee:ff    (Smart TV)

✅ Found 4 devices
```

**Astuce** : Vous pouvez identifier le fabricant de chaque appareil grâce aux trois premiers octets de l'adresse MAC (OUI - Organizationally Unique Identifier).

## Structure du Paquet ARP

Pour les curieux, voici la structure exacte des paquets envoyés par le script :

<div class="mermaid">
flowchart TB
    subgraph Ethernet["🔌 Trame Ethernet"]
        E1["dst: ff:ff:ff:ff:ff:ff (broadcast)"]
        E2["src: MAC du scanner"]
        E3["type: 0x0806 (ARP)"]
    end

    subgraph ARP["📡 Paquet ARP"]
        A1["op: 1 (request = qui a cette IP?)"]
        A2["hwsrc: MAC du scanner"]
        A3["psrc: IP du scanner"]
        A4["hwdst: 00:00:00:00:00:00 (inconnu)"]
        A5["pdst: IP cible"]
    end
    
    Ethernet --> ARP
    
    style E1 fill:#e74c3c,fill-opacity:0.15
    style A5 fill:#3498db,fill-opacity:0.15
    style ARP fill:#808080,fill-opacity:0.15
    style Ethernet fill:#808080,fill-opacity:0.15

</div>

## Installation et Exécution

```bash
# Créer un environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# Installer Scapy
pip install scapy

# Exécuter (privilèges root requis pour les raw sockets)
sudo python main.py
```

**Note importante** : Les requêtes ARP nécessitent un accès direct à la couche liaison (niveau 2), ce qui requiert des privilèges administrateur.

## Pour Aller Plus Loin

- 📚 [Documentation Scapy](https://scapy.readthedocs.io/) - Manipulation avancée de paquets
- 📄 [RFC 826 - ARP Protocol](https://tools.ietf.org/html/rfc826) - Spécification officielle
- 🔍 [Techniques de découverte réseau](https://nmap.org/book/host-discovery.html) - Guide Nmap


## Exploits et Vulnérabilités Connues

- **CVE-2020-8597 (pppd Buffer Overflow)** : Vulnérabilité dans le daemon PPP permettant une exécution de code à distance. La découverte ARP permet d'identifier les hôtes utilisant PPP pour cibler cette vulnérabilité.

- **CVE-2008-0166 (Debian OpenSSL)** : Faille critique de génération de clés prévisibles sur Debian. Le scan ARP combiné à l'identification du vendor MAC permet de cibler les systèmes Debian potentiellement vulnérables.

- **ARP Spoofing/Poisoning** : Technique d'attaque Man-in-the-Middle exploitant l'absence d'authentification dans le protocole ARP. Un attaquant peut se faire passer pour la passerelle et intercepter tout le trafic réseau.

- **CVE-2021-31440 (Linux Kernel eBPF)** : Vulnérabilité dans eBPF permettant une élévation de privilèges. Combiné au scan ARP pour découvrir les hôtes Linux, cette faille permet des mouvements latéraux sur le réseau.


## Approfondissement Théorique

Le protocole ARP, défini dans la RFC 826 en 1982, est l'un des protocoles fondamentaux d'Internet qui n'a jamais été conçu avec la sécurité en tête. Il fonctionne sur le principe de confiance : lorsqu'un hôte reçoit une réponse ARP, il l'accepte sans vérification. Cette confiance aveugle est à l'origine des attaques ARP spoofing, où un attaquant envoie de fausses réponses ARP pour associer son adresse MAC à l'IP d'un autre hôte (typiquement la passerelle).

Les mécanismes de défense contre les abus ARP incluent : Dynamic ARP Inspection (DAI) sur les switches managés, ARP Watch pour la détection d'anomalies, et les entrées ARP statiques pour les hôtes critiques. Le protocole Secure Neighbor Discovery (SEND), défini dans la RFC 3971, propose une solution cryptographique pour IPv6, mais n'a pas d'équivalent largement déployé pour IPv4.

La découverte réseau via ARP est souvent la première étape d'un test de pénétration interne. Elle permet de cartographier rapidement le réseau, identifier les systèmes actifs, et potentiellement découvrir des appareils non autorisés (shadow IT). L'analyse des OUI (trois premiers octets de l'adresse MAC) révèle le fabricant de la carte réseau, permettant d'inférer le type d'appareil : routeur, serveur, IoT, workstation. Des bases de données comme IEEE OUI Registry ou macvendors.com permettent cette identification.


---
