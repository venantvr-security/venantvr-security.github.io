---
layout: default
title: "Python.Osint.Blackbird"
description: "Blackbird - Recherche de Comptes par Username"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Osint.Blackbird</span>
</div>

<div class="page-header">
  <h1>Python.Osint.Blackbird</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Osint.Blackbird" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Blackbird - Recherche de Comptes par Username

> **AVERTISSEMENT** : Cet outil est destiné **uniquement** à des fins éducatives et autorisées.

## Introduction : L'OSINT par le Nom d'Utilisateur

Dans le monde de l'**OSINT** (Open Source Intelligence), le nom d'utilisateur est souvent la première piste. Une personne utilise fréquemment le même pseudo sur plusieurs plateformes : réseaux sociaux, forums, sites de partage de code... En identifiant ces comptes, on peut construire un profil complet de l'activité en ligne d'une personne.

**Blackbird** automatise cette recherche en testant un nom d'utilisateur sur plus de **574 sites** simultanément. Inspiré du légendaire avion de reconnaissance SR-71 "Blackbird", il combine vitesse et discrétion.

### Cas d'usage légitimes

- **Investigation numérique** : Retrouver tous les comptes d'une personne dans le cadre d'une enquête
- **Protection de marque** : Vérifier si quelqu'un usurpe l'identité de votre entreprise
- **Audit de sécurité personnel** : Découvrir quels comptes vous avez créés et oubliés
- **Due diligence** : Vérifier la présence en ligne d'un candidat ou partenaire

### Caractéristiques techniques

| Fonctionnalité      | Description                     |
| ------------------- | ------------------------------- |
| Sites supportés     | 574+ plateformes différentes    |
| Modes d'utilisation | Interface CLI et web            |
| Formats d'export    | JSON, CSV, HTML                 |
| Performance         | Requêtes parallèles asynchrones |

## Architecture de Blackbird

Le processus de recherche est massivement parallélisé : plutôt que de tester chaque site un par un, Blackbird envoie des requêtes simultanées à tous les sites, réduisant considérablement le temps de scan.

<div class="mermaid">
flowchart TB
    subgraph INPUT["📝 Entrée"]
        USER["Username cible"]
    end

    subgraph ENGINE["⚙️ Moteur Blackbird"]
        LOADER["Sites Loader"]
        CHECKER["Account Checker"]
        PARALLEL["Parallel Requests"]
    end
    
    subgraph SITES["🌐 574+ Sites"]
        S1["Twitter"]
        S2["GitHub"]
        S3["Instagram"]
        S4["LinkedIn"]
        S5["Reddit"]
        S6["..."]
    end
    
    subgraph OUTPUT["📊 Résultats"]
        FOUND["✅ Compte trouvé"]
        NOTFOUND["❌ Non trouvé"]
        EXPORT["JSON / CSV / HTML"]
    end
    
    INPUT --> ENGINE
    ENGINE --> LOADER --> SITES
    SITES --> CHECKER --> PARALLEL
    PARALLEL --> FOUND & NOTFOUND
    FOUND --> EXPORT
    
    style FOUND fill:#2ecc71,fill-opacity:0.15
    style NOTFOUND fill:#e74c3c,fill-opacity:0.15
    style OUTPUT fill:#808080,fill-opacity:0.15
    style SITES fill:#808080,fill-opacity:0.15
    style ENGINE fill:#808080,fill-opacity:0.15
    style INPUT fill:#808080,fill-opacity:0.15

</div>

## Flux de Recherche en Détail

Ce diagramme montre comment Blackbird détermine si un compte existe sur chaque plateforme. La méthode de détection varie selon les sites : certains renvoient un code 404, d'autres un message d'erreur spécifique.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant U as 👤 Utilisateur
    participant B as 🐦 Blackbird
    participant S as 🌐 Sites (574+)

    U->>B: blackbird -u "target_user"
    
    par Requêtes parallèles
        B->>S: GET twitter.com/target_user
        B->>S: GET github.com/target_user
        B->>S: GET instagram.com/target_user
        B->>S: ...
    end
    
    alt Compte existe
        S-->>B: 200 OK
        B->>B: ✅ Marquer trouvé
    else Compte n'existe pas
        S-->>B: 404 Not Found
        B->>B: ❌ Marquer absent
    end
    
    B-->>U: Rapport des comptes trouvés

</div>

## Utilisation

### Installation et Mode CLI

```bash
# Cloner le dépôt original
git clone https://github.com/p1ngul1n0/blackbird
cd blackbird
pip install -r requirements.txt

# Recherche simple par username
python blackbird.py -u johndoe

# Avec export JSON pour traitement ultérieur
python blackbird.py -u johndoe --json results.json

# Export CSV pour Excel/Google Sheets
python blackbird.py -u johndoe --csv results.csv
```

### Mode Web (Interface Graphique)

Pour une utilisation plus conviviale, Blackbird propose une interface web :

```bash
# Démarrer le serveur web
python blackbird.py --web

# Accéder à l'interface
# Ouvrez http://127.0.0.1:9797 dans votre navigateur
```

## Exemple de Sortie

Voici ce que vous verrez lors d'une recherche :

```
 ██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗ ██╗██████╗ ██████╗
 ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██║██╔══██╗██╔══██╗
 ██████╔╝██║     ███████║██║     █████╔╝ ██████╔╝██║██████╔╝██║  ██║
 ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██╔══██╗██║██╔══██╗██║  ██║
 ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗██████╔╝██║██║  ██║██████╔╝
 ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═════╝

[*] Searching for: johndoe
[*] Checking 574 sites...

[+] Twitter: https://twitter.com/johndoe
[+] GitHub: https://github.com/johndoe
[+] Instagram: https://instagram.com/johndoe
[-] LinkedIn: Not found
[+] Reddit: https://reddit.com/user/johndoe
[+] Steam: https://steamcommunity.com/id/johndoe
[-] TikTok: Not found
[+] Twitch: https://twitch.tv/johndoe
...

[*] Search completed in 12.3 seconds
[*] Found: 42 accounts
[*] Not found: 532 sites
```

## Catégories de Sites Couverts

Blackbird couvre un large éventail de plateformes, organisées par catégorie :

<div class="mermaid">
flowchart LR
    subgraph Categories["📂 Catégories"]
        C1["🐦 Social Media"]
        C2["💻 Tech/Dev"]
        C3["🎮 Gaming"]
        C4["🎵 Music"]
        C5["📸 Photo/Video"]
        C6["💼 Professional"]
    end

    subgraph Count["Nombre de sites"]
        N1["150+ sites"]
        N2["80+ sites"]
        N3["60+ sites"]
        N4["40+ sites"]
        N5["70+ sites"]
        N6["50+ sites"]
    end
    
    C1 --> N1
    C2 --> N2
    C3 --> N3
    C4 --> N4
    C5 --> N5
    C6 --> N6
    
    style C1 fill:#3498db,fill-opacity:0.15
    style C2 fill:#2ecc71,fill-opacity:0.15
    style C3 fill:#9b59b6,fill-opacity:0.15
    style Count fill:#808080,fill-opacity:0.15
    style Categories fill:#808080,fill-opacity:0.15

</div>

**Exemples par catégorie** :

- **Social Media** : Twitter, Instagram, Facebook, TikTok, Snapchat...
- **Tech/Dev** : GitHub, GitLab, Stack Overflow, HackerNews, CodePen...
- **Gaming** : Steam, Xbox, PlayStation, Twitch, Discord...
- **Professional** : LinkedIn, AngelList, Behance, Dribbble...

## Ajouter un Site Personnalisé

Blackbird utilise un fichier JSON pour définir les sites à scanner. Vous pouvez ajouter vos propres sites :

```python
# Structure d'un site dans le fichier de configuration
{
    "name": "CustomSite",
    "url": "https://customsite.com/users/{}",
    "errorType": "status_code",  # ou "message"
    "errorCode": 404,            # Code HTTP si compte inexistant
    "headers": {
        "User-Agent": "Mozilla/5.0"
    }
}
```

## Considérations Éthiques et Légales

L'utilisation de cet outil doit respecter :

- **La vie privée** : Ne recherchez que des personnes pour lesquelles vous avez une raison légitime
- **Les CGU des sites** : Certaines plateformes interdisent le scraping automatisé
- **La législation locale** : L'OSINT est encadré par des lois (RGPD en Europe, etc.)

## Pour Aller Plus Loin

- 🐦 [Blackbird Original](https://github.com/p1ngul1n0/blackbird) - Dépôt source
- 🔍 [OSINT Framework](https://osintframework.com/) - Collection d'outils OSINT
- 🕵️ [Sherlock Project](https://github.com/sherlock-project/sherlock) - Alternative populaire


## Exploits et Vulnérabilités Connues

L'OSINT par username peut révéler des comptes liés à des brèches de données majeures. Voici des incidents de sécurité pertinents pour comprendre les risques d'exposition en ligne :

- **CVE-2021-22911 (Rocket.Chat)** : Fuite d'informations utilisateur permettant l'énumération de comptes. Ce type de vulnérabilité facilite directement le travail d'outils comme Blackbird en confirmant l'existence d'utilisateurs.

- **LinkedIn Datà Breach 2021** : Scraping de 700 millions de profils LinkedIn. Les données incluaient noms d'utilisateur, emails, et liens vers d'autres réseaux sociaux, illustrant comment une seule source peut mener à un graphe complet de présence en ligne.

- **CVE-2020-12720 (vBulletin)** : Injection SQL permettant l'extraction de la basé utilisateurs. Les forums compromis via cette CVE ont exposé des millions de pseudonymes et emails, alimentant les bases de données OSINT.

- **Facebook Datà Leak 2019** : 533 millions de numéros de téléphone associés à des comptes Facebook. La correlation téléphone-username permet d'enrichir les recherches OSINT avec des données de contact.

- **CVE-2022-0847 (Dirty Pipe)** : Bien que technique, cette vulnérabilité Linux a été utilisée pour compromettre des serveurs hébergéant des bases de données utilisateurs, illustrant la chaîne : vulnérabilité système vers fuite de données OSINT exploitables.


## Approfondissement Théorique

L'OSINT (Open Source Intelligence) repose sur le principe que les informations publiquement accessibles, lorsqu'elles sont agrégées et corrélées, révèlent bien plus que la somme de leurs parties. La recherche par username exploite un biais cognitif humain : la tendance à réutiliser le même pseudonyme sur plusieurs plateformes par commodité. Cette pratique, appelée "username reuse", est similaire à la réutilisation de mots de passe et présente des risques comparables pour la vie privée.

Le processus technique de Blackbird illustre plusieurs concepts fondamentaux de l'énumération web. La détection de comptes existants peut se faire par plusieurs méthodes : analyse du code de réponse HTTP (200 vs 404), recherche de patterns dans le contenu de la page (message d'erreur spécifique vs contenu de profil), et analyse des headers de réponse. Certains sites implémentent des protections anti-scraping (rate limiting, CAPTCHAs, blocage par User-Agent) que les outils OSINT doivent contourner via rotation de proxies, randomisation des délais, et spoofing de signatures navigateur.

L'aspect éthique et légal de l'OSINT est crucial. En Europe, le RGPD impose des restrictions sur la collecte et le traitement de données personnelles, même publiques. La finalité de la collecte doit être légitime et proportionnée. Les professionnels de la sécurité utilisent l'OSINT pour évaluer l'exposition d'une entreprise (digital footprint assessment), tester la résistance au social engineering, ou investiguer des incidents. Les acteurs malveillants exploitent les mêmes techniques pour le spear phishing, l'usurpation d'identité, ou la préparation d'attaques ciblées. Cette dualité d'usage souligne l'importance d'une utilisation responsable.


---
