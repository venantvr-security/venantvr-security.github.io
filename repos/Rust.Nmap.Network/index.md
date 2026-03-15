---
layout: default
title: "Rust.Nmap.Network"
description: "IDS Lab Commander - Test d'Évasion IDS"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Rust.Nmap.Network</span>
</div>

<div class="page-header">
  <h1>Rust.Nmap.Network</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Rust.Nmap.Network" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# IDS Lab Commander - Test d'Évasion IDS

## Introduction : Comprendre les Systèmes de Détection d'Intrusion

Les **systèmes de détection d'intrusion** (IDS) sont les gardiens silencieux de nos réseaux. Ils analysent le trafic en permanence, à la recherche de signatures d'attaques connues ou de comportements suspects. Mais comment s'assurer qu'un IDS fonctionne correctement ? Comment tester sa capacité à détecter les attaques les plus sophistiquées ?

Ce projet répond à ces questions en créant un **laboratoire de test complet** avec trois des IDS les plus populaires : Snort, Suricata et Zeek. Une interface de pilotage en Rust permet de lancer des scans et de comparer instantanément les capacités de détection de chaque système.

### Ce que ce projet permet de faire

| Fonctionnalité | Description |
|----------------|-------------|
| **Comparaison IDS** | Tester le même scan contre Snort, Suricata et Zeek |
| **Dashboard Rust** | Interface web pour piloter les tests |
| **Techniques d'évasion** | Fragmenter, ralentir, masquer les scans |
| **Visualisation** | EveBox pour analyser les alertes Suricata |

### Les trois IDS comparés

Chaque IDS a sa philosophie et ses forces. Le tableau suivant résume leurs caractéristiques principales :

| Caractéristique | Snort | Suricata | Zeek |
|-----------------|-------|----------|------|
| **Approche** | Signatures | Signatures | Comportemental |
| **Multi-threading** | Non (v2) | Oui | Oui |
| **Format logs** | Unified2 | EVE JSON | Logs structurés |
| **Point fort** | Maturité, règles | Performance | Analyse réseau |


## Architecture du Laboratoire

Le laboratoire est conçu pour reproduire un environnement réaliste où un attaquant tente de scanner des serveurs protégés par différents IDS. Le schéma ci-dessous illustre cette architecture : un poste d'attaque équipé du Commander Rust peut cibler trois environnements distincts, chacun protégé par un IDS différent.

<div class="mermaid">
flowchart TB
    subgraph ATK["🖥️ POSTE ATTAQUANT"]
        CMD["Commander Rust<br/>Dashboard :3000"]
        TOOLS["Outils de scan<br/>Nmap / Scapy"]
    end

    subgraph SNORT["🔴 ENVIRONNEMENT SNORT"]
        S_IDS["Snort IDS<br/><i>Détection par signatures</i>"]
        S_TGT["Serveur nginx :80"]
        S_IDS -.->|"analyse le trafic"| S_TGT
    end

    subgraph SURI["🟠 ENVIRONNEMENT SURICATA"]
        SU_IDS["Suricata IDS<br/><i>Multi-threaded</i>"]
        SU_TGT["Serveur nginx :80"]
        EVE["EveBox :5636<br/><i>Visualisation</i>"]
        SU_IDS -.->|"analyse le trafic"| SU_TGT
        SU_IDS -->|"logs JSON"| EVE
    end

    subgraph ZEEK["🟢 ENVIRONNEMENT ZEEK"]
        Z_IDS["Zeek IDS<br/><i>Analyse comportementale</i>"]
        Z_TGT["Serveur nginx :80"]
        Z_IDS -.->|"analyse le trafic"| Z_TGT
    end

    CMD -->|"pilote les tests"| SNORT & SURI & ZEEK
    TOOLS -->|"scans d'évasion"| S_TGT & SU_TGT & Z_TGT

    style CMD fill:#3498db,fill-opacity:0.15
    style S_IDS fill:#e74c3c,fill-opacity:0.15
    style SU_IDS fill:#f39c12,fill-opacity:0.15
    style Z_IDS fill:#2ecc71,fill-opacity:0.15
    style ZEEK fill:#808080,fill-opacity:0.15
    style SURI fill:#808080,fill-opacity:0.15
    style SNORT fill:#808080,fill-opacity:0.15
    style ATK fill:#808080,fill-opacity:0.15
</div>

### Composants du laboratoire

| Composant | Rôle | Port d'accès |
|-----------|------|--------------|
| **Commander (Rust)** | Dashboard de pilotage centralisé | 3000 |
| **Snort IDS** | Détection par signatures (le plus ancien) | - |
| **Suricata IDS** | Détection multi-threadée haute performance | - |
| **Zeek IDS** | Analyse comportementale et logs riches | - |
| **EveBox** | Visualisation des alertes Suricata | 5636 |


## Installation et Démarrage

Le laboratoire utilise Docker Compose pour orchestrer tous les conteneurs. L'installation est simple et automatisée.

```bash
# Prérequis : ajouter votre utilisateur au groupe docker
# (nécessaire pour éviter d'utiliser sudo)
sudo usermod -aG docker $USER

# Se déconnecter/reconnecter pour appliquer le changement de groupe

# Cloner le projet
git clone https://github.com/venantvr-security/Rust.Nmap.Network
cd Rust.Nmap.Network

# Démarrer tous les environnements de test
# Ce script lance les conteneurs pour Snort, Suricata et Zeek
./start_all_labs.sh

# Vérifier que tout fonctionne
docker ps  # Vous devriez voir 7+ conteneurs actifs
```

Une fois démarré, accédez au dashboard sur `http://localhost:3000`.


## Les Techniques d'Évasion

Les attaquants utilisent diverses techniques pour échapper à la détection des IDS. Ce projet permet de les tester méthodiquement. Le diagramme suivant montre le niveau de difficulté de détection pour chaque technique.

<div class="mermaid">
flowchart LR
    subgraph Techniques["🔧 Techniques d'évasion Nmap"]
        F["-f<br/>Fragmentation IP"]
        T["-T0<br/>Timing paranoid"]
        D["-D<br/>Decoys (leurres)"]
        P["--source-port 53<br/>Port DNS"]
    end

    subgraph Détéction["📊 Difficulté de détection"]
        EASY["🟢 Facile à détecter"]
        MEDIUM["🟡 Détection moyenne"]
        HARD["🔴 Difficile à détecter"]
    end

    F --> HARD
    T --> HARD
    D --> HARD
    P --> MEDIUM

    style F fill:#9b59b6,fill-opacity:0.15
    style T fill:#9b59b6,fill-opacity:0.15
    style D fill:#9b59b6,fill-opacity:0.15
    style HARD fill:#e74c3c,fill-opacity:0.15
    style Détéction fill:#808080,fill-opacity:0.15
    style Techniques fill:#808080,fill-opacity:0.15
</div>

### Explication des techniques

**Fragmentation (-f)** : Découpe les paquets en fragments si petits que les IDS ont du mal à reconstituer les signatures d'attaque.

**Timing paranoid (-T0)** : Ralentit considérablement le scan pour passer sous le seuil de détection temporel des IDS.

**Decoys (-D)** : Génère du trafic de leurre depuis des IP fictives pour noyer la vraie source d'attaque.

**Source port 53** : Utilise le port DNS comme source, souvent autorisé sans inspection par les pare-feux.


## Exemples de Commandes de Test

Voici comment utiliser ces techniques avec Nmap pour tester vos IDS.

```bash
# Test 1 : Scan basique (devrait être détecté facilement)
nmap -sS -p 80 target

# Test 2 : Fragmentation double
# Les paquets sont fragmentés en morceaux de 8 octets
nmap -f -f target

# Test 3 : Timing ultra-lent (paranoid)
# Un paquet toutes les 5 minutes environ
nmap -T0 -p 80 target

# Test 4 : Combinaison avancée
# Fragmentation + timing modéré + 5 leurres aléatoires + source port DNS
nmap -f -T2 -D RND:5 --source-port 53 target

# Test 5 : Scan de version masqué
nmap -sV -f -T1 --data-length 50 target
```

Après chaque test, consultez les logs de chaque IDS pour voir lequel a détecté l'attaque.


## Analyse des Résultats

Le Commander affiche les alertes de chaque IDS en temps réel. Pour Suricata, EveBox offre une interface graphique riche accessible sur le port 5636.

### Métriques à observer

| Métrique | Signification |
|----------|---------------|
| **Taux de détection** | % des scans détectés |
| **Faux positifs** | Alertes sur du trafic légitime |
| **Latence** | Temps entre le scan et l'alerte |
| **Richesse des logs** | Informations contextuelles |


## Pour Aller Plus Loin

Ce laboratoire n'est qu'une introduction au monde du test d'IDS. Pour approfondir vos connaissances :

- 📚 [Snort Rules Explanation](https://www.snort.org/rules_explanation) - Comprendre la syntaxe des règles Snort
- 🔧 [Suricata Documentation](https://suricata.readthedocs.io/) - Configuration avancée de Suricata
- 📊 [Zeek Documentation](https://docs.zeek.org/) - Scripting et analyse comportementale
- 🛡️ [MITRE ATT&CK](https://attack.mitre.org/) - Catalogue des techniques d'attaque


## Exploits et Vulnérabilités Connues

Les systèmes de détection d'intrusion et les outils de scan réseau ont été affectés par plusieurs vulnérabilités :

| CVE | Produit | Description | Score CVSS |
|-----|---------|-------------|------------|
| **CVE-2022-40674** | Suricata | Heap buffer overflow dans le parsing HTTP permettant un crash ou RCE | 9.8 Critique |
| **CVE-2021-45469** | Snort | Stack buffer overflow dans le préprocesseur Modbus | 7.5 Élevé |
| **CVE-2022-25899** | Suricata | DoS via paquets TCP craftés causant une consommation mémoire excessive | 7.5 Élevé |
| **CVE-2023-35001** | Linux Kernel (nf_tables) | Vulnérabilité dans Netfilter affectant les systèmes hébergeant des IDS | 7.8 Élevé |
| **CVE-2020-5923** | Snort (DAQ) | Fuite de mémoire dans le module Data Acquisition pouvant causer un DoS | 6.5 Moyen |

Ces vulnérabilités illustrent l'importance de maintenir les IDS à jour. Un IDS vulnérable peut devenir lui-même un vecteur d'attaque, l'attaquant exploitant les failles de parsing pour compromettre le système de sécurité.


## Approfondissement Théorique

### Les approches de détection : signatures vs comportement

Les IDS modernes utilisent principalement deux approches complémentaires. La **détection par signatures** (Snort, Suricata) compare le trafic réseau à une base de règles prédéfinies. Cette méthode est efficace contre les attaques connues mais impuissante face aux zero-days ou aux variations de payloads. La **détection comportementale** (Zeek) analyse les patterns de trafic pour identifier les anomalies, permettant de détecter des attaques inconnues mais générant plus de faux positifs. Les déploiements modernes combinent les deux approches : Suricata ou Snort en première ligne pour bloquer les menaces connues, et Zeek pour l'analyse forensique approfondie.

### Le défi de l'inspection du trafic chiffré

Avec la généralisation de TLS/HTTPS (plus de 90% du trafic web), les IDS traditionnels perdent en efficacité car ils ne peuvent pas inspecter le contenu chiffré. Plusieurs stratégies existent : le **SSL/TLS interception** (man-in-the-middle d'entreprise) permet de déchiffrer le trafic mais pose des problèmes de confidentialité et de performance. L'analyse des **métadonnées TLS** (JA3/JA3S fingerprinting) permet d'identifier les clients et serveurs sans déchiffrer. Les approches **Machine Learning** analysent les patterns de trafic chiffré (taille des paquets, timing, direction) pour détecter les communications malveillantes.

### Évasion avancée et contre-mesures

Les techniques d'évasion évoluent constamment. Au-delà de la fragmentation et du timing, les attaquants modernes utilisent des **protocoles encapsulés** (HTTP sur DNS, ICMP tunneling), des **chiffrements custom** pour masquer les payloads, et des **protocoles légitimes** comme cover channels (data hidden dans les headers HTTP, DNS TXT records). Les contre-mesures incluent la normalisation de protocole (réassemblage des fragments avant analyse), l'inspection multi-couches (corrélation entre couches réseau/transport/application), et l'analyse comportementale à long terme qui détecte les patterns suspects même si chaque paquet individuel semble légitime.


---

