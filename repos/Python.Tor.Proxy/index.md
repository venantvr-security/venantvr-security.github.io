---
layout: default
title: "Python.Tor.Proxy"
description: "Gestion des Interfaces Réseau avec Stem/TOR"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Tor.Proxy</span>
</div>

<div class="page-header">
  <h1>Python.Tor.Proxy</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Tor.Proxy" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Gestion des Interfaces Réseau avec Stem/TOR

## Introduction : Garantir l'Anonymat Total

Utiliser TOR pour naviguer anonymement ne suffit pas toujours. Si votre système dispose de plusieurs interfaces réseau (Ethernet, WiFi, VPN...), certaines applications peuvent **contourner TOR** en utilisant une autre interface, révélant ainsi votre véritable adresse IP.

Ce script Python résout ce problème en **désactivant automatiquement** toutes les interfaces réseau sauf celle utilisée par TOR. Ainsi, il devient **physiquement impossible** pour une application de fuiter votre IP réelle.

### Le problème des fuites d'IP

Imaginez que vous utilisez TOR via votre interface WiFi, mais votre navigateur décide d'utiliser l'interface Ethernet pour certaines requêtes DNS. Résultat : votre FAI voit ces requêtes et peut les corréler avec votre activité TOR.

### La solution : l'isolation réseau

En désactivant toutes les interfaces sauf celle de TOR et le loopback (nécessaire au fonctionnement du système), nous garantissons que **tout le trafic** passe par TOR.

| Objectif | Description |
|----------|-------------|
| Isolation | Désactiver les interfaces non-TOR |
| Anonymat | Forcer 100% du trafic via TOR |
| Contrôle | Gérer les interfaces dynamiquement avec Python |


## Architecture du Système

Le diagramme ci-dessous illustre le fonctionnement du script. Notez que l'interface Ethernet (eth0) est désactivée tandis que l'interface WiFi (wlan0), utilisée par TOR, reste active.

<div class="mermaid">
flowchart TB
    subgraph SYSTEM["💻 Système"]
        ETH["eth0"]
        WIFI["wlan0"]
        LO["lo (loopback)"]
    end

    subgraph TOR["🧅 TOR"]
        STEM["Stem Controller"]
        SOCKS["SOCKS :9050"]
        CTRL["Control :9051"]
    end

    subgraph SCRIPT["🐍 Python Script"]
        DETECT["Détecter interface TOR"]
        DISABLE["Désactiver autres"]
        ENABLE["Réactiver"]
    end

    STEM --> CTRL
    SCRIPT --> DETECT --> WIFI
    SCRIPT --> DISABLE --> ETH
    LO -.->|"Toujours actif"| LO

    style TOR fill:#9b59b6,fill-opacity:0.15
    style WIFI fill:#2ecc71,fill-opacity:0.15
    style ETH fill:#e74c3c,fill-opacity:0.15
    style SCRIPT fill:#808080,fill-opacity:0.15
    style SYSTEM fill:#808080,fill-opacity:0.15
</div>

**Points clés** :
- L'interface TOR (wlan0 ici) reste active
- L'interface loopback (lo) est toujours conservée (nécessaire au système)
- Toutes les autres interfaces sont désactivées


## Flux de Gestion des Interfaces

Le script fonctionne en trois phases distinctes : identification de l'interface TOR, désactivation des autres interfaces, puis réactivation à la fin des opérations.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant S as 🐍 Script
    participant T as 🧅 TOR
    participant N as 🌐 Interfaces

    S->>T: Identifier interface TOR
    T-->>S: wlan0 (via torrc)

    S->>N: Lister toutes les interfaces
    N-->>S: eth0, wlan0, lo

    rect rgb(231, 76, 60, 0.2)
        Note over S,N: Désactivation
        S->>N: ip link set eth0 down
        Note over N: eth0 désactivé
    end

    Note over S: ... Opérations anonymes ...

    rect rgb(46, 204, 113, 0.2)
        Note over S,N: Réactivation
        S->>N: ip link set eth0 up
        Note over N: eth0 réactivé
    end
</div>


## Le Script Python

Ce script utilise deux bibliothèques complémentaires :
- **Stem** : bibliothèque officielle du Tor Project pour contrôler TOR via Python
- **netifaces** : bibliothèque pour lister et manipuler les interfaces réseau

```python
import subprocess
import netifaces
import time
from stem.control import Controller

def get_tor_interface():
    """
    Identifie l'interface réseau utilisée par TOR.

    La détection se fait en plusieurs étapes :
    1. Vérifier la configuration torrc pour OutboundBindInterface
    2. Si non définie, utiliser l'interface de la route par défaut
    """
    # Méthode 1: Vérifier torrc pour OutboundBindInterface
    try:
        with open('/etc/tor/torrc', 'r') as f:
            for line in f:
                if 'OutboundBindInterface' in line:
                    return line.split()[1].strip()
    except FileNotFoundError:
        pass

    # Méthode 2: Interface de la route par défaut
    default = subprocess.check_output(
        "ip route | grep default | awk '{print $5}'",
        shell=True, text=True
    ).strip()

    return default


def get_all_interfaces():
    """Liste toutes les interfaces réseau du système"""
    return netifaces.interfaces()


def disable_interface(iface):
    """Désactive une interface réseau (nécessite sudo)"""
    subprocess.run(['sudo', 'ip', 'link', 'set', iface, 'down'])
    print(f"❌ Interface {iface} désactivée")


def enable_interface(iface):
    """Réactive une interface réseau"""
    subprocess.run(['sudo', 'ip', 'link', 'set', iface, 'up'])
    print(f"✅ Interface {iface} réactivée")


def isolate_tor():
    """
    Désactive toutes les interfaces sauf TOR et loopback.

    Retourne la liste des interfaces désactivées pour
    pouvoir les réactiver plus tard.
    """
    tor_iface = get_tor_interface()
    all_ifaces = get_all_interfaces()

    disabled = []
    for iface in all_ifaces:
        # Ne jamais désactiver TOR ou loopback
        if iface == tor_iface or iface == 'lo':
            print(f"🔒 Interface {iface} conservée (TOR/loopback)")
            continue

        disable_interface(iface)
        disabled.append(iface)

    return disabled


def restore_interfaces(interfaces):
    """Réactive les interfaces précédemment désactivées"""
    for iface in interfaces:
        enable_interface(iface)
```


## Exemple d'Utilisation

Voici comment utiliser le script pour effectuer des opérations anonymes en toute sécurité :

```python
from stem.control import Controller
from stem import Signal

# 1. Isoler le trafic via TOR
disabled = isolate_tor()

try:
    # 2. Effectuer des opérations anonymes
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()

        # Afficher l'adresse IP TOR actuelle
        print(f"IP TOR: {controller.get_info('address')}")

        # Changer d'identité TOR (nouveau circuit)
        controller.signal(Signal.NEWNYM)
        print("Nouvelle identité TOR obtenue")

finally:
    # 3. Toujours restaurer les interfaces, même en cas d'erreur
    restore_interfaces(disabled)
```


## Configuration TOR Requise

Pour que le script fonctionne, TOR doit être configuré avec le port de contrôle activé. Voici la configuration minimale :

```
# /etc/tor/torrc

# Port SOCKS pour les applications (proxy)
SocksPort 9050

# Port de contrôle pour Stem (API)
ControlPort 9051

# Interface de sortie spécifique (optionnel)
OutboundBindInterface wlan0

# Authentification par cookie (recommandé)
CookieAuthentication 1
```


## État du Système Avant/Après

Ce diagramme montre l'état des interfaces réseau avant et après l'exécution du script d'isolation.

<div class="mermaid">
flowchart TB
    subgraph Before["Avant Isolation"]
        B1["eth0: UP"]
        B2["wlan0: UP"]
        B3["lo: UP"]
    end

    subgraph After["Après Isolation"]
        A1["eth0: DOWN"]
        A2["wlan0: UP (TOR)"]
        A3["lo: UP"]
    end

    subgraph Traffic["Trafic"]
        T1["Tout via TOR"]
        T2["Pas de fuite"]
    end

    Before -->|"isolate_tor()"| After
    After --> Traffic

    style A1 fill:#e74c3c,fill-opacity:0.15
    style A2 fill:#2ecc71,fill-opacity:0.15
    style T1 fill:#9b59b6,fill-opacity:0.15
    style Traffic fill:#808080,fill-opacity:0.15
    style After fill:#808080,fill-opacity:0.15
    style Before fill:#808080,fill-opacity:0.15
</div>


## Installation et Prérequis

```bash
# Installer les dépendances Python
pip install stem netifaces

# Le script nécessite des droits root pour manipuler les interfaces
sudo python tor_proxy.py
```

**Note de sécurité** : Ce script modifie la configuration réseau de votre système. Testez-le d'abord dans un environnement contrôlé.


## Pour Aller Plus Loin

- 📚 [Documentation Stem](https://stem.torproject.org/) - Bibliothèque officielle du Tor Project
- 🧅 [Manuel TOR](https://www.torproject.org/docs/tor-manual.html) - Configuration avancée
- 🔧 [netifaces](https://pypi.org/project/netifaces/) - Manipulation des interfaces réseau


## Exploits et Vulnérabilités Connues

Le réseau TOR et ses composants ont fait l'objet de plusieurs vulnérabilités importantes :

| CVE | Composant | Description | Score CVSS |
|-----|-----------|-------------|------------|
| **CVE-2020-15572** | Tor Browser | Fuite d'information via le header Referer permettant de corréler les sessions | 6.5 Moyen |
| **CVE-2017-16541** | Tor Browser (Firefox) | Bypass du proxy via le protocole file:// permettant de révéler l'IP réelle | 6.5 Moyen |
| **CVE-2021-38295** | Tor | Attaque de type denial-of-service via des descripteurs de services cachés malformés | 7.5 Élevé |
| **CVE-2020-10592** | Tor | Amplification d'attaque via les circuits de rendez-vous, permettant des DoS ciblés | 7.5 Élevé |
| **CVE-2019-8955** | Tor | Buffer over-read dans le parsing SOCKS5 pouvant causer des crashes | 7.5 Élevé |

Au-delà des CVE, les attaques de **corrélation de trafic** restent la principale menace contre l'anonymat TOR. Un adversaire contrôlant à la fois le noeud d'entrée et de sortie peut théoriquement désanonymiser les utilisateurs en corrélant les patterns de trafic.


## Approfondissement Théorique

### Le modèle de menace de l'isolation réseau

L'isolation des interfaces réseau abordée dans ce projet répond à un vecteur d'attaque spécifique : les **fuites de trafic**. Ces fuites peuvent survenir de plusieurs manières. Les requêtes DNS constituent le cas le plus fréquent : même si le trafic HTTP passe par TOR, les requêtes DNS peuvent être envoyées directement au résolveur du FAI, révélant les sites visités. WebRTC dans les navigateurs peut établir des connexions peer-to-peer qui contournent complètement le proxy TOR. Certaines applications peuvent ignorer les variables d'environnement de proxy et établir des connexions directes.

### Le concept de cloisonnement des identités

La gestion des identités TOR (via `NEWNYM`) est cruciale pour la sécurité opérationnelle. Chaque identité TOR utilise un circuit différent avec des noeuds intermédiaires distincts. Cependant, changer d'identité ne suffit pas toujours : si l'utilisateur maintient une session authentifiée ou des cookies persistants, la nouvelle identité reste liée à l'ancienne au niveau applicatif. Le projet **Whonix** pousse ce concept plus loin en séparant physiquement (ou virtuellement) le gateway TOR de la station de travail, garantissant qu'aucun trafic ne peut fuiter même en cas de compromission de la VM de travail.

### Les limites du modèle TOR

TOR protège contre l'analyse de trafic au niveau réseau, mais ne protège pas contre les attaques au niveau applicatif. Les fingerprints de navigateur (canvas, WebGL, fonts), les comportements de navigation, et même le timing de frappe peuvent être utilisés pour identifier un utilisateur malgré TOR. C'est pourquoi le Tor Browser modifie volontairement ces paramètres pour que tous les utilisateurs aient une empreinte identique, rendant le fingerprinting inefficace.


---

