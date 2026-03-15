---
layout: default
title: "Python.PiZero.WiFi"
description: "Analyse Réseau WiFi avec PyShark et Wireshark"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.PiZero.WiFi</span>
</div>

<div class="page-header">
  <h1>Python.PiZero.WiFi</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.PiZero.WiFi" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Analyse Réseau WiFi avec PyShark et Wireshark

## Introduction : Transformer un Raspberry Pi en Analyseur Réseau

Un Raspberry Pi Zero coûte moins de 20€, mais combiné avec les bons outils, il devient un puissant analyseur de trafic réseau. Ce projet utilise **Wireshark** (via son interface Python **PyShark**) pour capturer et analyser le trafic WiFi en temps réel.

### Pourquoi analyser le trafic réseau ?

L'analyse de paquets est essentielle pour :
- **Diagnostiquer des problèmes réseau** : latence, perte de paquets, erreurs de configuration
- **Auditer la sécurité** : détecter du trafic suspect, des données non chiffrées
- **Comprendre les protocoles** : voir concrètement comment HTTP, DNS, TLS fonctionnent
- **Tester des applications** : vérifier qu'elles communiquent correctement

### Les outils utilisés

| Composant | Rôle |
|-----------|------|
| **Wireshark** | Analyseur de protocoles graphique |
| **TShark** | Version ligne de commande de Wireshark |
| **PyShark** | Interface Python pour TShark |


## Architecture du Système

Le Raspberry Pi capture le trafic brut via son interface WiFi (en mode monitor pour capturer tout le trafic, pas seulement celui qui lui est destiné). PyShark parse les paquets et les rend accessibles en Python.

<div class="mermaid">
flowchart TB
    subgraph PI["🍓 Raspberry Pi Zero"]
        WIFI["📡 Interface WiFi"]
        MON["Mode Monitor"]
    end

    subgraph CAPTURE["📦 Capture"]
        TSHARK["TShark"]
        PYSHARK["PyShark"]
    end

    subgraph ANALYSIS["🔍 Analyse"]
        PROTO["Protocoles"]
        PACKETS["Paquets"]
        STATS["Statistiques"]
    end

    subgraph OUTPUT["📊 Résultats"]
        PCAP["Fichiers .pcap"]
        JSON["Export JSON"]
        REPORT["Rapport"]
    end

    WIFI --> MON --> TSHARK
    TSHARK --> PYSHARK --> ANALYSIS
    ANALYSIS --> PROTO & PACKETS & STATS
    PROTO & PACKETS & STATS --> OUTPUT

    style WIFI fill:#2ecc71,fill-opacity:0.15
    style PYSHARK fill:#3498db,fill-opacity:0.15
    style OUTPUT fill:#808080,fill-opacity:0.15
    style ANALYSIS fill:#808080,fill-opacity:0.15
    style CAPTURE fill:#808080,fill-opacity:0.15
    style PI fill:#808080,fill-opacity:0.15
</div>


## Flux de Capture en Détail

Le diagramme de séquence suivant montre comment les paquets sont capturés, parsés, puis analysés par votre code Python.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant W as 📡 WiFi
    participant T as 🔧 TShark
    participant P as 🐍 PyShark
    participant À as 📊 Analyse

    W->>T: Paquets bruts (frames 802.11)
    T->>T: Capture en temps réel
    T->>P: Paquets parsés (objets structurés)
    P->>A: Objets Python accessibles

    loop Pour chaque paquet
        A->>A: Extraire protocole (HTTP, DNS, TLS...)
        A->>A: Analyser payload
        A->>A: Détecter anomalies
    end
</div>


## Installation

Sur Raspberry Pi OS (ou tout système Debian/Ubuntu) :

```bash
# Mise à jour du système
sudo apt-get update

# Installation de Wireshark et TShark
sudo apt-get install -y libcap2-bin wireshark tshark

# Permettre l'utilisation sans root (optionnel mais recommandé)
sudo dpkg-reconfigure wireshark-common
# Choisir "Yes" pour permettre aux utilisateurs non-root de capturer

# Ajouter votre utilisateur au groupe wireshark
sudo usermod -aG wireshark $USER

# Installation des bibliothèques Python
pip install pyshark
```


## Capture en Temps Réel avec PyShark

Ce script montre comment capturer et analyser le trafic en temps réel :

```python
import pyshark

# Créer une capture en temps réel sur l'interface WiFi
capture = pyshark.LiveCapture(interface='wlan0')

print("🔍 Démarrage de la capture...")
print("-" * 50)

# Capturer 100 paquets en continu
for packet in capture.sniff_continuously(packet_count=100):
    try:
        # Informations de base disponibles pour tous les paquets
        print(f"📦 Protocole: {packet.highest_layer}")
        print(f"   Temps: {packet.sniff_time}")

        # Si c'est du HTTP, afficher les détails de la requête
        if 'HTTP' in packet:
            print(f"   🌐 URL: {packet.http.request_full_uri}")
            print(f"   📝 Méthode: {packet.http.request_method}")

        # Si c'est du DNS, afficher la requête
        if 'DNS' in packet:
            print(f"   🔎 Query DNS: {packet.dns.qry_name}")

        print("-" * 50)

    except AttributeError:
        # Certains paquets n'ont pas tous les champs
        pass
```


## Analyse de Fichiers PCAP

Vous pouvez aussi analyser des captures existantes :

```python
import pyshark

# Lire un fichier de capture existant
cap = pyshark.FileCapture('capture.pcap')

# Statistiques par protocole
protocols = {}
for packet in cap:
    proto = packet.highest_layer
    protocols[proto] = protocols.get(proto, 0) + 1

print("📊 Statistiques par protocole:")
print("-" * 30)
for proto, count in sorted(protocols.items(), key=lambda x: -x[1]):
    bar = "█" * min(count // 10, 30)
    print(f"  {proto:15} {count:5}  {bar}")
```


## Filtres de Capture

PyShark supporte les filtres Wireshark pour cibler des types de trafic spécifiques :

<div class="mermaid">
flowchart LR
    subgraph Filters["🔍 Types de Filtres"]
        F1["display_filter<br/>(filtre Wireshark)"]
        F2["bpf_filter<br/>(filtre BPF bas niveau)"]
    end

    subgraph Examples["Exemples"]
        E1["http.request.method == GET"]
        E2["tcp.port == 80"]
        E3["ip.addr == 192.168.1.1"]
        E4["dns"]
    end

    F1 --> E1 & E3 & E4
    F2 --> E2

    style F1 fill:#3498db,fill-opacity:0.15
    style F2 fill:#2ecc71,fill-opacity:0.15
    style Examples fill:#808080,fill-opacity:0.15
    style Filters fill:#808080,fill-opacity:0.15
</div>

```python
# Capturer uniquement les requêtes HTTP POST
capture = pyshark.LiveCapture(
    interface='wlan0',
    display_filter='http.request.method == POST'
)

# Ou avec un filtre BPF pour les performances
capture = pyshark.LiveCapture(
    interface='wlan0',
    bpf_filter='tcp port 443'  # Tout le trafic HTTPS
)
```


## Mode Monitor : Capturer Tout le Trafic WiFi

Par défaut, une interface WiFi ne voit que le trafic qui lui est destiné. Le **mode monitor** permet de capturer **tout** le trafic WiFi environnant (y compris celui des autres appareils).

```bash
# Vérifier si l'interface supporte le mode monitor
iw list | grep "monitor"

# Activer le mode monitor avec airmon-ng
sudo airmon-ng start wlan0

# L'interface devient wlan0mon
```

```python
import pyshark

# Capture sur l'interface en mode monitor
cap = pyshark.LiveCapture(interface='wlan0mon')

for packet in cap.sniff_continuously():
    if 'WLAN' in packet:
        # Informations spécifiques au WiFi
        print(f"📡 BSSID: {packet.wlan.bssid}")
        print(f"📶 Signal: {packet.radiotap.dbm_antsignal} dBm")
```

**Attention** : Le mode monitor est soumis à des réglementations légales. Utilisez-le uniquement sur vos propres réseaux.


## Pour Aller Plus Loin

- 📚 [Documentation PyShark](https://kiminewt.github.io/pyshark/) - API complète
- 🦈 [Wireshark](https://www.wireshark.org/) - Analyseur graphique
- 📖 [Manuel TShark](https://www.wireshark.org/docs/man-pages/tshark.html) - Référence CLI


## Exploits et Vulnérabilités Connues

L'analyse WiFi permet de détecter et comprendre de nombreuses vulnérabilités dans les protocoles sans fil :

- **CVE-2017-13077 à CVE-2017-13088 (KRACK)** : Key Reinstallation Attacks contre WPA2. Cette série de vulnérabilités permet à un attaquant de forcer la réinstallation de clés de chiffrement déjà utilisées, permettant le déchiffrement du trafic. L'analyse de trames WiFi avec Wireshark/PyShark permet de détecter ces attaques via l'observation de messages EAPOL anormaux.

- **CVE-2019-9494 (Dragonblood)** : Vulnérabilités dans WPA3-SAE permettant des attaques par dictionnaire et side-channel. L'analyse des handshakes SAE via capture WiFi peut révéler des tentatives d'exploitation.

- **CVE-2020-24588 (FragAttacks)** : Ensemble de vulnérabilités dans l'implementation de la fragmentation 802.11. Permettent l'injection de trames et l'exfiltration de données. Détectables par analyse de trames fragmentées anormales.

- **CVE-2017-9417 (Broadpwn)** : Vulnérabilité dans les chipsets WiFi Broadcom permettant RCE via trames malformées. L'analyse de trafic peut révéler des patterns de trames anormaux caractéristiques de l'exploitation.

- **CVE-2021-28372 (Kr00k successor)** : Vulnérabilité dans certains chipsets WiFi permettant le déchiffrement partiel de trames. Les analyseurs détectent les trames chiffrées avec des clés nulles ou faibles.


## Approfondissement Théorique

Le protocole 802.11 (WiFi) opère sur les couches 1 (physique) et 2 (liaison) du modèle OSI. La capture en mode monitor permet d'accéder aux trames 802.11 brutes, incluant les informations de gestion (beacons, probe requests/responses, authentication, association) et les données. Contrairement au mode "managed" standard où l'adaptateur filtre automatiquement les trames non destinées à la machine, le mode monitor capture tout le trafic radio détectable sur le canal configuré.

L'analyse de trafic WiFi révélé de nombreuses informations de sécurité. Les probe requests émis par les appareils mobiles exposent l'historique des réseaux auxquels ils se sont connectés, permettant le tracking et le profilage. Les beacons des points d'accès révèlent leurs configurations de sécurité (WPA2, WPA3, PMF). L'analyse des handshakes d'authentification (4-way handshake EAPOL pour WPA2/WPA3) est fondamentale pour les audits de sécurité : une capture du handshake permet des attaques par dictionnaire offline contre la clé pré-partagée.

PyShark, en tant que wrapper Python autour de TShark, hérite de toute la puissance de dissection de Wireshark. Les dissecteurs supportent des centaines de protocoles, permettant l'analyse automatisée à grande échelle. Pour les performances, les filtrès BPF (Berkeley Packet Filter) opèrent au niveau du noyau, filtrant les paquets avant qu'ils ne remontent en espace utilisateur. L'utilisation d'un Raspberry Pi Zero comme sonde d'analyse présente l'avantage de la discrétion et de la portabilité, permettant des audits in-situ sans attirer l'attention. La consommation électrique minimale permet une autonomie prolongée sur batterie.


---

