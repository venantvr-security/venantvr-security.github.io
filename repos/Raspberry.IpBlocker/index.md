---
layout: default
title: "Raspberry.IpBlocker"
description: "Générateur de Règles iptables Géolocalisées"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Raspberry.IpBlocker</span>
</div>

<div class="page-header">
  <h1>Raspberry.IpBlocker</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Raspberry.IpBlocker" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Générateur de Règles iptables Géolocalisées

## Introduction : Bloquer le Trafic par Pays

La majorité des attaques sur Internet proviennent de quelques pays bien identifiés. Si votre service n'a pas vocation à recevoir du trafic de certaines régions du monde, pourquoi ne pas simplement bloquer ces plages d'IP au niveau du pare-feu ?

Ce projet génère automatiquement des règles **iptables** à partir de fichiers de zones IP géolocalisées. Idéal pour un Raspberry Pi faisant office de routeur/pare-feu, ou tout serveur Linux souhaitant réduire sa surface d'attaque.

### Cas d'utilisation

| Usage | Description |
|-------|-------------|
| **Blocage géographique** | Bloquer le trafic de pays spécifiques (attaques, spam) |
| **Protection serveur** | Réduire les tentatives de bruteforce SSH |
| **Conformité** | Restreindre l'accès selon les réglementations |
| **Whitelist** | Autoriser uniquement certains pays |


## Architecture du Système

Le générateur lit des fichiers de zones IP (un CIDR par ligne), puis génère un script de règles iptables optimisées.

<div class="mermaid">
flowchart TB
    subgraph INPUT["📥 Entrées"]
        ZONE["fr-aggregated.zone"]
        CONFIG["Configuration"]
    end

    subgraph GENERATOR["⚙️ Générateur Python"]
        PARSE["Parser zones IP"]
        RULES["Générer règles"]
        OPTIMIZE["Optimiser/Agréger"]
    end

    subgraph OUTPUT["📤 Sortie"]
        IPTABLES["iptables rules"]
        SCRIPT["block-ips.sh"]
    end

    subgraph FIREWALL["🛡️ iptables"]
        DROP["DROP packets"]
        ACCEPT["ACCEPT local"]
    end

    INPUT --> GENERATOR --> OUTPUT --> FIREWALL

    style DROP fill:#e74c3c,fill-opacity:0.15
    style ACCEPT fill:#2ecc71,fill-opacity:0.15
    style FIREWALL fill:#808080,fill-opacity:0.15
    style OUTPUT fill:#808080,fill-opacity:0.15
    style GENERATOR fill:#808080,fill-opacity:0.15
    style INPUT fill:#808080,fill-opacity:0.15
</div>


## Format des Fichiers Zone

Les fichiers zone contiennent une plage IP (notation CIDR) par ligne. Ces fichiers sont disponibles gratuitement sur des sites comme IPdeny ou MaxMind.

<div class="mermaid">
flowchart LR
    subgraph Zone["📄 fr-aggregated.zone"]
        Z1["1.2.3.0/24"]
        Z2["5.6.0.0/16"]
        Z3["10.20.30.0/22"]
    end

    subgraph Rules["🔥 Règles iptables"]
        R1["iptables -À INPUT -s 1.2.3.0/24 -j DROP"]
        R2["iptables -À INPUT -s 5.6.0.0/16 -j DROP"]
        R3["iptables -À INPUT -s 10.20.30.0/22 -j DROP"]
    end

    Z1 --> R1
    Z2 --> R2
    Z3 --> R3

    style Zone fill:#3498db,fill-opacity:0.15
    style Rules fill:#e74c3c,fill-opacity:0.15
</div>


## Le Script Python

```python
#!/usr/bin/env python3
"""
Générateur de règles iptables depuis fichiers de zones IP géolocalisées
"""

import ipaddress
import sys

def load_zone_file(filename):
    """
    Charge un fichier de zones IP.

    Chaque ligne doit contenir une plage IP en notation CIDR.
    Les lignes vides et commentaires (#) sont ignorés.
    """
    networks = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    network = ipaddress.ip_network(line, strict=False)
                    networks.append(network)
                except ValueError:
                    print(f"Warning: Plage invalide ignorée: {line}", file=sys.stderr)
    return networks


def generate_iptables_rules(networks, action='DROP', chain='INPUT'):
    """
    Génère les règles iptables pour bloquer les réseaux.

    Args:
        networks: Liste d'objets ip_network
        action: DROP (bloquer) ou REJECT (bloquer avec notification)
        chain: INPUT (trafic entrant) ou OUTPUT (trafic sortant)
    """
    rules = []
    rules.append("#!/bin/bash")
    rules.append(f"# Règles iptables - {len(networks)} plages IP")
    rules.append(f"# Action: {action} sur chaîne {chain}")
    rules.append("")

    for network in networks:
        rule = f"iptables -À {chain} -s {network} -j {action}"
        rules.append(rule)

    return "\\n".join(rules)


def main():
    if len(sys.argv) < 2:
        print("Usage: python block-ips.py <zone_file>")
        print("Exemple: python block-ips.py fr-aggregated.zone")
        sys.exit(1)

    zone_file = sys.argv[1]

    print(f"# Chargement de {zone_file}...", file=sys.stderr)
    networks = load_zone_file(zone_file)
    print(f"# {len(networks)} plages IP chargées", file=sys.stderr)

    rules = generate_iptables_rules(networks)
    print(rules)


if __name__ == "__main__":
    main()
```


## Utilisation

### Génération et application des règles

```bash
# Générer le script de blocage
python3 block-ips.py fr-aggregated.zone > block-fr.sh

# Rendre le script exécutable
chmod +x block-fr.sh

# Appliquer les règles (nécessite root)
sudo ./block-fr.sh

# Vérifier que les règles sont en place
sudo iptables -L INPUT -n | head -20
```


## Ordre des Règles iptables

L'ordre des règles est crucial : iptables les évalue dans l'ordre et s'arrête à la première correspondance. Voici une structure recommandée :

<div class="mermaid">
flowchart TB
    subgraph Chain["🔥 Chaîne INPUT"]
        R1["1. ACCEPT established,related"]
        R2["2. ACCEPT localhost"]
        R3["3. ACCEPT SSH depuis admin"]
        R4["4. DROP 1.2.3.0/24"]
        R5["5. DROP 5.6.0.0/16"]
        R6["6. ..."]
        R7["N. Policy: ACCEPT ou DROP"]
    end

    PACKET["📦 Paquet entrant"] --> R1
    R1 -->|"non"| R2
    R2 -->|"non"| R3
    R3 -->|"non"| R4
    R4 -->|"non"| R5
    R5 -->|"non"| R6
    R6 -->|"non"| R7

    style R4 fill:#e74c3c,fill-opacity:0.15
    style R5 fill:#e74c3c,fill-opacity:0.15
    style R7 fill:#2ecc71,fill-opacity:0.15
    style Chain fill:#808080,fill-opacity:0.15
</div>


## Optimisation : Agrégation des Plages

Pour améliorer les performances, on peut agréger les plages IP contiguës :

```python
from ipaddress import ip_network, collapse_addresses

def aggregate_networks(networks):
    """
    Agrège les plages IP contiguës pour réduire le nombre de règles.

    Par exemple, 192.168.1.0/24 et 192.168.2.0/24 peuvent être
    agrégées en 192.168.0.0/22 selon les cas.
    """
    # Convertir en objets ip_network
    nets = [ip_network(n, strict=False) for n in networks]

    # Agréger les plages contiguës
    aggregated = list(collapse_addresses(nets))

    print(f"Avant agrégation: {len(networks)} plages")
    print(f"Après agrégation: {len(aggregated)} plages")

    return aggregated
```


## Sources de Zones IP

| Source | Description | Accès |
|--------|-------------|-------|
| **IPdeny** | Zones par pays, mises à jour quotidiennes | Gratuit |
| **MaxMind** | Base GeoIP précise | Gratuit (inscription) |
| **RIPE NCC** | Registre européen officiel | Gratuit |
| **ipdeny.com** | Agrégation automatique | Gratuit |


## Pour Aller Plus Loin

- 📚 [Manuel iptables](https://linux.die.net/man/8/iptables) - Référence complète
- 🌍 [IPdeny](https://www.ipdeny.com/ipblocks/) - Zones IP par pays
- 📊 [MaxMind GeoIP](https://www.maxmind.com/) - Base de géolocalisation


## Exploits et Vulnérabilités Connues

Les pare-feux Linux (iptables/nftables) et les systèmes de géolocalisation IP ont connu plusieurs vulnérabilités :

| CVE | Composant | Description | Score CVSS |
|-----|-----------|-------------|------------|
| **CVE-2022-25636** | nftables (kernel) | Heap out-of-bounds write permettant une escalade de privilèges locale | 7.8 Élevé |
| **CVE-2021-22555** | Netfilter | Heap out-of-bounds write dans le module xt_ROUTE permettant LPE et container escape | 7.8 Élevé |
| **CVE-2022-32250** | nftables | Use-after-free dans le sous-système nf_tables permettant escalade de privilèges | 7.8 Élevé |
| **CVE-2023-32233** | Netfilter nf_tables | Use-after-free permettant d'obtenir les privilèges root | 7.8 Élevé |
| **CVE-2019-11477** | TCP Stack (SACK) | "SACK Panic" - DoS via paquets TCP craftes, contournable même avec iptables | 7.5 Élevé |

Les vulnérabilités dans **Netfilter** sont particulièrement critiques car elles affectent le code kernel qui traite les paquets réseau. Un attaquant local peut potentiellement les exploiter pour obtenir les privilèges root, même sur un système correctement configuré avec iptables.


## Approfondissement Théorique

### Les limites du blocage géographique

Le blocage par géolocalisation IP présente des limitations fondamentales. Premièrement, les bases de données de géolocalisation ne sont pas parfaitement précises : environ 1-5% des IPs sont mal géolocalisées, ce qui peut bloquer des utilisateurs légitimes ou laisser passer des attaquants. Deuxièmement, les attaquants utilisent fréquemment des **proxies**, **VPN** ou **machines compromises** dans des pays non bloqués pour contourner ces restrictions. Troisièmement, les **CDN** comme Cloudflare ou AWS utilisent des IPs dans de nombreux pays, rendant difficile le blocage ciblé sans effets collatéraux.

### Performance et scalabilité d'iptables

Avec un grand nombre de règles (plusieurs milliers), les performances d'iptables se dégradent car chaque paquet doit être comparé séquentiellement à chaque règle. Pour améliorer les performances, plusieurs techniques existent. Les **ipset** permettent de grouper des milliers d'IPs dans une structure de données optimisée (hash table ou arbre), réduisant la complexité de O(n) à O(1). **nftables**, le successeur moderne d'iptables, offre une meilleure performance native et une syntaxe plus cohérente. Pour les cas extrêmes, **eBPF/XDP** permet de filtrer les paquets directement dans le driver réseau, avant même qu'ils n'atteignent la pile TCP/IP.

### Considérations légales et éthiques

Le blocage géographique soulève des questions juridiques et éthiques. Dans l'Union Européenne, le **geo-blocking** est réglementé pour les services de commerce électronique (Règlement 2018/302). Bloquer des utilisateurs d'un pays entier peut être discriminatoire et violer certaines législations. Du point de vue de la sécurité, le blocage géographique est une mesure **defense-in-depth** qui réduit le bruit mais ne doit jamais être considérée comme une protection principale. Les attaques ciblées utilisent systématiquement des relais dans les pays non bloqués, rendant cette mesure inefficace contre des adversaires déterminés.


---

