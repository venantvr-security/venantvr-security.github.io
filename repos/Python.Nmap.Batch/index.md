---
layout: default
title: "Python.Nmap.Batch"
description: "Plateforme Avancée de Scan Réseau avec Évasion IA"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Nmap.Batch</span>
</div>

<div class="page-header">
  <h1>Python.Nmap.Batch</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Nmap.Batch" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Plateforme Avancée de Scan Réseau avec Évasion IA

> **AVERTISSEMENT** : Utilisez cet outil **uniquement** sur des systèmes autorisés.

## Introduction : Au-delà du Simple Scan

Les pare-feux de nouvelle génération (NGFW) et les systèmes de détection basés sur le machine learning deviennent de plus en plus sophistiqués. Un simple scan Nmap avec les options par défaut sera détecté et bloqué instantanément.

Cette plateforme va plus loin en intégrant des **techniques d'évasion basées sur l'IA** : mimétisme de signatures OS, timings polymorphiques, et obfuscation de protocoles. Elle combine la puissance de Nmap et Scapy avec une interface web centralisée pour orchestrer des campagnes de scan complexes.

### Ce qui rend cette plateforme unique

| Fonctionnalité | Description |
|----------------|-------------|
| **Évasion IA** | Imitation de signatures OS, timings imprévisibles |
| **Stratégies YAML** | Configuration modulaire et réutilisable |
| **Dashboard temps réel** | Logs live via Server-Sent Events |
| **Intégration TOR** | Anonymisation optionnelle des scans |
| **Workers adaptatifs** | Parallélisation intelligente |


## Architecture de la Plateforme

La plateforme se compose de trois couches : l'interface web pour le contrôle, le moteur de scan avec ses stratégies, et la couche d'anonymisation optionnelle.

<div class="mermaid">
flowchart TB
    subgraph UI["🖥️ Interface Web"]
        DASH["Dashboard :3000"]
        CONFIG["Configuration"]
        DOCS["Documentation"]
    end

    subgraph ENGINE["⚙️ Moteur de Scan"]
        STRAT["📋 Stratégies YAML"]
        NMAP["🔧 Nmap"]
        SCAPY["🐍 Scapy"]
        AI["🤖 AI Evasion"]
    end

    subgraph TOR["🧅 Anonymisation"]
        STEM["Stem Controller"]
        CIRCUIT["Circuits TOR"]
    end

    subgraph OUTPUT["📊 Résultats"]
        LOGS["Logs temps réel"]
        RESULTS["results/"]
        SSE["Server-Sent Events"]
    end

    UI --> ENGINE
    STRAT --> NMAP & SCAPY
    AI --> SCAPY
    ENGINE --> TOR
    ENGINE --> OUTPUT

    style AI fill:#9b59b6,fill-opacity:0.15
    style DASH fill:#3498db,fill-opacity:0.15
    style OUTPUT fill:#808080,fill-opacity:0.15
    style TOR fill:#808080,fill-opacity:0.15
    style ENGINE fill:#808080,fill-opacity:0.15
    style UI fill:#808080,fill-opacity:0.15
</div>


## Les Techniques d'Évasion IA

L'engine d'évasion utilise plusieurs techniques pour contourner les systèmes de détection modernes. Chaque technique cible un type spécifique de détection.

<div class="mermaid">
flowchart LR
    subgraph AI["🤖 AI Evasion Engine"]
        E1["OS Fingerprint Mimicry<br/>(imiter Windows/Linux/iOS)"]
        E2["Polymorphic Timing<br/>(délais aléatoires)"]
        E3["Protocol Obfuscation<br/>(obscurcir les patterns)"]
        E4["ML Model Bypass<br/>(tromper les classifieurs)"]
    end

    subgraph Targets["🎯 Systèmes ciblés"]
        NGFW["Next-Gen Firewall"]
        IDS["IDS/IPS"]
        ML["Détection ML"]
    end

    subgraph Result["Résultat"]
        EVADE["✅ Évasion réussie"]
        DETECT["❌ Détecté"]
    end

    E1 & E2 & E3 & E4 --> Targets
    Targets -->|"~80%"| EVADE
    Targets -->|"~20%"| DETECT

    style E1 fill:#9b59b6,fill-opacity:0.15
    style E2 fill:#9b59b6,fill-opacity:0.15
    style EVADE fill:#2ecc71,fill-opacity:0.15
    style Result fill:#808080,fill-opacity:0.15
    style Targets fill:#808080,fill-opacity:0.15
    style AI fill:#808080,fill-opacity:0.15
</div>

### Explication des techniques

1. **OS Fingerprint Mimicry** : Les IDS utilisent les valeurs TTL, taille de fenêtre TCP, et options pour identifier l'OS source. Cette technique modifie ces valeurs pour imiter un OS "innocent" (comme un iPhone).

2. **Polymorphic Timing** : Les IDS détectent les scans par leur régularité. Cette technique introduit des délais aléatoires imprévisibles.

3. **Protocol Obfuscation** : Fragmentation des paquets, injection de données aléatoires, utilisation de ports source inhabituels.


## Flux de Scan avec Évasion

Ce diagramme montre le parcours complet d'un scan, de la sélection de la stratégie jusqu'à la réception des résultats.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant U as 👤 Utilisateur
    participant W as 🖥️ Dashboard
    participant E as ⚙️ Engine
    participant T as 🧅 TOR
    participant C as 🎯 Cible

    U->>W: Sélectionner scanner + stratégie
    W->>E: POST /api/scan

    rect rgb(155, 89, 182, 0.2)
        Note over E: AI Evasion Mode
        E->>E: Générer OS fingerprint (ex: Windows 10)
        E->>E: Calculer timing polymorphique
    end

    E->>T: Établir circuit TOR
    T->>C: Scan via exit node anonyme
    C-->>T: Réponses
    T-->>E: Résultats

    loop Mise à jour temps réel
        E-->>W: SSE: logs + progression
    end

    E->>E: Sauvegarder dans results/
</div>


## Configuration

### Fichier config.toml

La configuration générale de la plateforme :

```toml
[paths]
docs_dir = "docs"
stratégies_dir = "stratégies"
results_dir = "results"

[scan]
max_workers = 8        # Workers parallèles
timeout = 300          # Timeout par scan (secondes)

[tor]
enabled = true         # Activer l'anonymisation
control_port = 9051
socks_port = 9050
```

### Stratégies YAML

Les stratégies définissent les paramètres de scan de manière modulaire et réutilisable :

```yaml
# stratégies/nmap/stealth.yaml
name: stealth_scan
description: Scan furtif avec évasion IDS
tool: nmap

command: |
  nmap -sS -T2 -f --data-length 50
  --randomize-hosts --source-port 53
  -p {ports} {target}

options:
  ports: "22,80,443,8080"
  timing: "paranoid"

evasion:
  os_mimicry: "windows10"
  fragment_size: 8
  decoys: "RND:5"
```


## Préréglages d'Évasion

La plateforme inclut des préréglages optimisés pour différents scénarios de défense.

<div class="mermaid">
flowchart TB
    subgraph Presets["🎯 Préréglages"]
        P1["China GFW Bypass"]
        P2["Corporate NGFW"]
        P3["ML IDS Evasion"]
        P4["Stealth Recon"]
    end

    subgraph Techniques["🔧 Techniques Activées"]
        T1["Timing: Paranoid"]
        T2["Fragment: 8 bytes"]
        T3["Decoys: RND:10"]
        T4["Source Port: 53"]
        T5["OS Mimicry: Windows"]
    end

    P1 --> T1 & T2 & T5
    P2 --> T2 & T3 & T4
    P3 --> T1 & T3 & T5
    P4 --> T1 & T4

    style P1 fill:#e74c3c,fill-opacity:0.15
    style P2 fill:#f39c12,fill-opacity:0.15
    style P3 fill:#9b59b6,fill-opacity:0.15
    style P4 fill:#3498db,fill-opacity:0.15
    style Techniques fill:#808080,fill-opacity:0.15
    style Presets fill:#808080,fill-opacity:0.15
</div>


## Utilisation

### Démarrage de la plateforme

```bash
# Démarrer le serveur web
python3 main.py

# Accéder au dashboard
# Ouvrez http://localhost:3000
```

### Scan via API REST

```bash
curl -X POST http://localhost:3000/api/scan \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "nmap",
    "strategy": "stealth",
    "targets": ["192.168.1.0/24"],
    "ports": "22,80,443",
    "evasion": {
      "enabled": true,
      "preset": "corporate_ngfw"
    }
  }'
```


## Pour Aller Plus Loin

- 📚 [Nmap Documentation](https://nmap.org/book/) - Référence complète
- 🐍 [Scapy](https://scapy.readthedocs.io/) - Manipulation de paquets
- 🧅 [TOR Stem](https://stem.torproject.org/) - Contrôle de TOR via Python


## Exploits et Vulnérabilités Connues

Le scan réseau permet de découvrir des services vulnérables. Voici des exemples de CVE majeures détectables par Nmap et qui ont été massivement exploitées :

- **CVE-2017-0144 (EternalBlue)** : Vulnérabilité SMBv1 exploitée par WannaCry et NotPetya. Nmap détecte cette faille via le script `smb-vuln-ms17-010`. Plus de 200 000 systèmes infectés en quelques jours, illustrant l'importance du scan réseau pour identifier les services exposés.

- **CVE-2014-0160 (Heartbleed)** : Faille OpenSSL permettant la lecture de mémoire serveur. Le script Nmap `ssl-heartbleed` détecte cette vulnérabilité. A affecté environ 17% des serveurs HTTPS dans le monde à son apogée.

- **CVE-2021-41773 (Apache Path Traversal)** : Vulnérabilité dans Apache 2.4.49 permettant la lecture de fichiers et RCE. Détectable par scan de version et scripts NSE personnalisés. Exploitée dans les 24h suivant sa divulgation.

- **CVE-2019-19781 (Citrix ADC)** : Path traversal dans Citrix Gateway menant à RCE. Les scans de ports 443/80 avec détection de service Citrix ont permis aux attaquants d'identifier des milliers de cibles vulnérables.

- **CVE-2022-26134 (Confluence OGNL)** : Injection OGNL dans Atlassian Confluence permettant RCE non authentifié. Le scan de ports avec identification de service Confluence (port 8090 typiquement) est la première étape de l'exploitation.


## Approfondissement Théorique

Le scan réseau constitue la phase de reconnaissance active dans le cycle d'une attaque (ou d'un audit de sécurité). Selon le modèle Cyber Kill Chain de Lockheed Martin, cette étape fait partie de la "Reconnaissance" et de la "Weaponization". Le scan TCP SYN (-sS), dit "half-open", est privilégié car il ne complète pas la poignée de main TCP, rendant la détection plus difficile et évitant les logs applicatifs. Cependant, les IDS modernes détectent facilement ce pattern par l'analyse des ratios SYN/SYN-ACK anormaux.

Les techniques d'évasion IDS implémentées dans cette plateforme s'appuient sur plusieurs principes fondamentaux. Le TTL spoofing exploite le fait que les IDS inline voient les paquets avant leur destination finale ; en ajustant le TTL pour qu'il expire après l'IDS mais avant la cible, certains paquets malveillants peuvent être ignorés par l'IDS. La fragmentation IP divise les paquets de sorte que les signatures de détection (qui opèrent souvent paquet par paquet) ne reconnaissent pas les patterns malveillants. Les techniques de timing exploitent les timeouts des systèmes de détection : un scan suffisamment lent passe sous le seuil d'alerte.

L'utilisation de TOR pour l'anonymisation des scans présente des limitations importantes. Les exit nodes TOR sont connus et souvent bloqués par les pare-feux. De plus, le débit limité de TOR rend les scans intensifs impraticables. L'approche optimale combine TOR pour la reconnaissance initiale discrète avec des VPS jetables pour les scans plus intensifs. La rotation de circuits TOR via Stem permet de distribuer les requêtes sur plusieurs exit nodes, réduisant le risque de blocage. Cependant, les techniques d'évasion doivent être utilisées de manière éthique et uniquement dans le cadre d'audits autorisés.


---

