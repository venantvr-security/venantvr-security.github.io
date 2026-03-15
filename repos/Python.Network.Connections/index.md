---
layout: default
title: "Python.Network.Connections"
description: "Scanner de Réseau ARP avec Scapy"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Network.Connections</span>
</div>

<div class="page-header">
  <h1>Python.Network.Connections</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Network.Connections" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Scanner de Réseau ARP avec Scapy

> **AVERTISSEMENT** : Utilisez ce script de manière responsable sur vos propres réseaux uniquement.

## Introduction : Cartographier votre Réseau Local

Lorsque vous administrez un réseau, la première question est souvent : "Quels appareils sont connectés ?". Les smartphones, ordinateurs, imprimantes, objets connectés... tous ces appareils sont invisibles jusqu'à ce qu'on les cherche activement.

Ce script Python utilise le protocole **ARP** (Address Resolution Protocol) pour découvrir tous les hôtes actifs sur votre réseau local. Contrairement au ping (ICMP), qui peut être bloqué par les pare-feux, ARP fonctionne au niveau de la couche liaison et ne peut pas être filtré sur un réseau local.

### Pourquoi utiliser ARP ?

| Avantage | Explication |
|----------|-------------|
| **Fiabilité** | ARP ne peut pas être bloqué sur un réseau local |
| **Rapidité** | Scan d'un réseau /24 en quelques secondes |
| **Informations** | Révèle l'adresse MAC en plus de l'IP |
| **Discrétion** | Trafic normal sur un réseau local |


## Architecture du Scanner

Le scanner envoie une requête ARP broadcast à toutes les adresses IP de la plage spécifiée. Seuls les hôtes actifs répondent avec leur adresse MAC.

<div class="mermaid">
flowchart TB
    subgraph Scanner["🖥️ Scanner Python"]
        SCAPY["Scapy"]
        ARP_REQ["Paquet ARP Request"]
    end

    subgraph Network["🌐 Réseau Local"]
        BC["📡 Broadcast<br/>ff:ff:ff:ff:ff:ff"]
        H1["💻 Host 1"]
        H2["📱 Host 2"]
        H3["🖨️ Host 3"]
        H4["📺 Host 4"]
    end

    subgraph Response["📊 Réponses"]
        R1["192.168.1.10 → AA:BB:CC:DD:EE:01"]
        R2["192.168.1.20 → AA:BB:CC:DD:EE:02"]
        R3["192.168.1.30 → AA:BB:CC:DD:EE:03"]
    end

    Scanner --> ARP_REQ --> BC
    BC --> H1 & H2 & H3 & H4
    H1 & H2 & H3 -->|"ARP Reply"| Response

    style BC fill:#f39c12,fill-opacity:0.15
    style Response fill:#2ecc71,fill-opacity:0.15
    style Network fill:#808080,fill-opacity:0.15
    style Scanner fill:#808080,fill-opacity:0.15
</div>


## Le Protocole ARP en Action

Le protocole ARP permet de traduire une adresse IP en adresse MAC. Sans cette traduction, la communication Ethernet serait impossible. Voici le déroulement d'une requête ARP :

<div class="mermaid">
sequenceDiagram
    autonumber
    participant S as 🖥️ Scanner
    participant N as 🌐 Réseau
    participant H as 💻 Hôte cible

    S->>N: ARP Request (broadcast)<br/>"Qui à 192.168.1.x ?"
    N->>H: Relaye la requête

    alt Hôte actif
        H-->>S: ARP Reply<br/>"Je suis 192.168.1.x à MAC AA:BB:CC"
        Note over S: ✅ Hôte détecté
    else Hôte inactif ou inexistant
        Note over S: ❌ Pas de réponse (timeout)
    end
</div>

**Point clé** : Les hôtes inactifs ne répondent simplement pas. Le scanner attend un délai (timeout) avant de considérer qu'une IP n'est pas utilisée.


## Le Script Python

Le code utilisé Scapy pour créer et envoyer les paquets ARP. La fonction `srp` (send and receive packets) gère automatiquement l'envoi et la collecte des réponses.

```python
from scapy.all import ARP, Ether, srp

def scan_network(ip_range):
    """
    Scanne une plage d'adresses IP pour détecter les machines connectées.

    Le protocole ARP est utilisé car il fonctionne au niveau de la couche
    liaison (niveau 2), ce qui signifie qu'il ne peut pas être bloqué par
    un pare-feu applicatif. Tout appareil sur le réseau local DOIT répondre
    aux requêtes ARP pour pouvoir communiquer.

    Args:
        ip_range: Plage IP au format CIDR (ex: "192.168.1.0/24")

    Returns:
        Liste de dictionnaires {ip, mac} pour chaque hôte trouvé
    """
    # Créer le paquet ARP broadcast
    # La destination Ethernet est ff:ff:ff:ff:ff:ff (tous les appareils)
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Combiner les couches Ethernet et ARP
    packet = broadcast / arp_request

    # Envoyer et recevoir les réponses
    # timeout=3 : attendre max 3 secondes pour les réponses
    # verbose=False : ne pas afficher les messages Scapy
    answèred, unanswèred = srp(packet, timeout=3, verbose=False)

    # Extraire les résultats des réponses
    devices = []
    for sent, received in answèred:
        devices.append({
            'ip': received.psrc,    # IP source de la réponse
            'mac': received.hwsrc   # MAC source de la réponse
        })

    return devices


if __name__ == "__main__":
    ip_range = "192.168.1.0/24"

    print(f"🔍 Scanning {ip_range}...")
    print("-" * 50)

    devices = scan_network(ip_range)

    print(f"\n{'IP':<20} {'MAC':<20}")
    print("-" * 40)

    for device in devices:
        print(f"{device['ip']:<20} {device['mac']:<20}")

    print(f"\n✅ {len(devices)} machines connectées trouvées.")
```


## Exemple de Sortie

Voici ce que vous verrez en exécutant le script sur un réseau domestique typique :

```
🔍 Scanning 192.168.1.0/24...
--------------------------------------------------

IP                   MAC
----------------------------------------
192.168.1.1          0a:1b:2c:3d:4e:5f    # Router/Box
192.168.1.10         a1:b2:c3:d4:e5:f6    # PC Bureau
192.168.1.25         10:20:30:40:50:60    # Smartphone
192.168.1.42         aa:bb:cc:dd:ee:ff    # Laptop
192.168.1.100        11:22:33:44:55:66    # Smart TV

✅ 5 machines connectées trouvées.
```

**Astuce** : Les trois premiers octets de l'adresse MAC (OUI) identifient le fabricant. Vous pouvez utiliser des bases de données en ligne pour les identifier.


## Structure du Paquet ARP

Pour comprendre ce que fait réellement le script, voici la structure des paquets envoyés :

<div class="mermaid">
flowchart TB
    subgraph Ethernet["📦 Trame Ethernet"]
        E1["dst: ff:ff:ff:ff:ff:ff (broadcast)"]
        E2["src: MAC du scanner"]
        E3["type: 0x0806 (ARP)"]
    end

    subgraph ARP["📡 Paquet ARP"]
        A1["op: 1 (request = qui à cette IP?)"]
        A2["hwsrc: MAC du scanner"]
        A3["psrc: IP du scanner"]
        A4["hwdst: 00:00:00:00:00:00 (inconnu)"]
        A5["pdst: IP ciblé à découvrir"]
    end

    Ethernet --> ARP

    style E1 fill:#e74c3c,fill-opacity:0.15
    style A5 fill:#3498db,fill-opacity:0.15
    style ARP fill:#808080,fill-opacity:0.15
    style Ethernet fill:#808080,fill-opacity:0.15
</div>


## Installation et Exécution

```bash
# Installer Scapy
pip install scapy

# Exécuter le script (privilèges root requis)
sudo python scanner_réseau.py
```

**Pourquoi sudo ?** Scapy crée des "raw sockets" pour envoyer des paquets arbitraires. Cette opération nécessite des privilèges administrateur sur la plupart des systèmes.


## Pour Aller Plus Loin

- 📚 [Documentation Scapy](https://scapy.readthedocs.io/) - Manipulation avancée de paquets
- 📄 [RFC 826 - ARP Protocol](https://tools.ietf.org/html/rfc826) - Spécification officielle
- 🔍 [OUI Lookup](https://macvendors.com/) - Identifier le fabricant d'une adresse MAC


## Exploits et Vulnérabilités Connues

Le protocole ARP, conçu sans mécanisme d'authentification, est intrinsèquement vulnérable. Voici des exemples de vulnérabilités et attaques exploitant ces faiblesses :

- **CVE-2008-2476** : Vulnérabilité dans la pile IPv6/ICMPv6 de plusieurs systèmes (FreeBSD, NetBSD) permettant une attaque de type Neighbor Discovery spoofing, équivalent IPv6 de l'ARP spoofing. Un attaquant sur le même segment réseau peut rediriger le trafic.

- **CVE-2020-8597 (pppd)** : Bien que concernant PPP, cette vulnérabilité de buffer overflow illustre les risques des protocoles réseau de couche 2. Un paquet malveillant peut provoquer l'exécution de code arbitraire.

- **CVE-2011-0997 (ISC DHCP)** : Faille permettant à un serveur DHCP malveillant d'exécuter du code via des options DHCP. Combinée avec l'ARP spoofing, elle permet des attaques en chaîne sur le réseau local.

- **ARP Cache Poisoning** : Technique d'attaque non liée à une CVE spécifique mais universellement applicable. L'outil Ettercap et Bettercap l'implémentent pour réaliser des attaques Man-in-the-Middle sur les réseaux locaux.

- **CVE-2016-1979 (libnetfilter)** : Vulnérabilité dans le traitement des messages netlink permettant un DoS. Les outils de manipulation ARP comme Scapy interagissent avec cette interface.


## Approfondissement Théorique

Le protocole ARP (Address Resolution Protocol), défini dans la RFC 826 en 1982, est un protocole essentiel de la couche liaison (couche 2 du modèle OSI). Son rôle est de faire le lien entre les adresses IP (couche 3) et les adresses MAC (couche 2). Sans ARP, les équipements d'un réseau Ethernet ne pourraient pas communiquer car les trames Ethernet nécessitent les adresses MAC source et destination. Le mécanisme est simple : une machine souhaitant connaître l'adresse MAC associée à une IP diffuse une requête ARP en broadcast, et la machine possédant cette IP répond avec son adresse MAC.

Cette simplicité est aussi la faiblesse principale d'ARP : il n'existe aucun mécanisme d'authentification. N'importe quelle machine peut répondre à une requête ARP, même si elle n'est pas le propriétaire légitime de l'adresse IP. C'est le fondement de l'ARP spoofing (ou ARP poisoning) : un attaquant envoie des réponses ARP falsifiées pour associer son adresse MAC à l'adresse IP d'une autre machine (typiquement la passerelle). Le trafic destiné à cette IP transite alors par l'attaquant, permettant une attaque Man-in-the-Middle.

Les mécanismes de défense contre l'ARP spoofing incluent : Dynamic ARP Inspection (DAI) sur les switches managés, ARP statiques pour les équipements critiques, détection d'anomalies via des outils comme arpwatch, et le chiffrement des communications (HTTPS, VPN) qui rend l'interception inutile même en cas de MITM. La segmentation réseau via VLAN limite également la portée d'une attaque ARP au segment local.


---

