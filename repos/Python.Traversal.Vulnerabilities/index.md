---
layout: default
title: "Python.Traversal.Vulnerabilities"
description: "DotDotSlash - Détection de Path Traversal"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Traversal.Vulnerabilities</span>
</div>

<div class="page-header">
  <h1>Python.Traversal.Vulnerabilities</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Traversal.Vulnerabilities" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# DotDotSlash - Détection de Path Traversal

> **AVERTISSEMENT** : Utilisez cet outil **uniquement** sur des systèmes autorisés.

## Introduction : La Vulnérabilité Path Traversal

Le **Path Traversal** (ou Directory Traversal) est une vulnérabilité qui permet à un attaquant de sortir du répertoire prévu par l'application pour accéder à des fichiers arbitraires sur le serveur. Le nom "DotDotSlash" vient de la technique de base : utiliser `../` pour remonter dans l'arborescence des répertoires.

### Pourquoi c'est dangereux ?

Imaginez une application web qui permet de télécharger des fichiers PDF :

```
https://example.com/download?file=report.pdf
```

Si le développeur ne valide pas correctement le paramètre `file`, un attaquant peut demander :

```
https://example.com/download?file=../../../etc/passwd
```

Et obtenir la liste des utilisateurs du système Linux !

### Plateformes de test compatibles

Cet outil a été testé avec succès sur plusieurs environnements d'entraînement :

| Plateforme | Niveaux testés |
|------------|----------------|
| DVWÀ | Low / Medium / High |
| bWAPP | Low / Medium / High |
| ZICO2-1 (VulnHub) | - |


## Anatomie d'une Attaque Path Traversal

Le diagramme ci-dessous montre comment le serveur vulnérable traite une requête malveillante. La clé est la **concaténation non sécurisée** du chemin de base avec l'entrée utilisateur.

<div class="mermaid">
flowchart TB
    subgraph Request["📤 Requête"]
        URL["GET /download?file=report.pdf"]
    end

    subgraph Attack["💥 Attaque"]
        PAYLOAD["file=../../../etc/passwd"]
    end

    subgraph Server["🖥️ Serveur Vulnérable"]
        CODE["readfile($base_path . $file)"]
        PATH["/var/www/html/../../../etc/passwd"]
        RESULT["/etc/passwd"]
    end

    subgraph Response["📥 Réponse"]
        PASSWD["root:x:0:0:root:/root:/bin/bash"]
    end

    Request --> Attack --> CODE
    CODE --> PATH --> RESULT --> Response

    style Attack fill:#e74c3c,fill-opacity:0.15
    style RESULT fill:#f39c12,fill-opacity:0.15
    style Response fill:#808080,fill-opacity:0.15
    style Server fill:#808080,fill-opacity:0.15
    style Request fill:#808080,fill-opacity:0.15
</div>

**Le problème** : Le serveur concatène `/var/www/html/` avec `../../../etc/passwd`. Les `../` remontent dans l'arborescence, et le chemin final devient `/etc/passwd`.


## Techniques d'Évasion des Filtres

Les applications modernes tentent souvent de bloquer les attaques Path Traversal en filtrant `../`. Mais il existe de nombreuses techniques pour contourner ces filtres.

<div class="mermaid">
flowchart LR
    subgraph Techniques["🔧 Payloads"]
        T1["../"]
        T2["..%2f"]
        T3["..%252f"]
        T4["....//"]
        T5["%2e%2e/"]
        T6["..%c0%af"]
    end

    subgraph Bypass["⚡ Contournement"]
        B1["Encodage URL simple"]
        B2["Double encodage"]
        B3["Bypass de filtres basiques"]
        B4["Encodage UTF-8 invalide"]
    end

    T1 --> B3
    T2 & T5 --> B1
    T3 --> B2
    T4 --> B3
    T6 --> B4

    style T1 fill:#e74c3c,fill-opacity:0.15
    style T2 fill:#f39c12,fill-opacity:0.15
    style T3 fill:#f39c12,fill-opacity:0.15
    style Bypass fill:#808080,fill-opacity:0.15
    style Techniques fill:#808080,fill-opacity:0.15
</div>

### Explication des techniques

| Payload | Technique | Contourne |
|---------|-----------|-----------|
| `../` | Basique | Aucun filtre |
| `..%2f` | Encodage URL (`/` = `%2f`) | Filtres sur `../` littéral |
| `..%252f` | Double encodage | Filtres qui décodent une seule fois |
| `....//` | Duplication | Filtres qui suppriment `../` une fois |
| `%2e%2e/` | Encodage des points | Filtres sur `..` littéral |


## Flux de Détection Automatisé

L'outil DotDotSlash automatise la recherche de vulnérabilités Path Traversal en testant systématiquement toutes les techniques connues à différentes profondeurs.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant U as 🔧 DotDotSlash
    participant T as 🎯 Cible

    U->>T: GET /page?file=document.pdf (baseline)
    T-->>U: 200 OK (normal)

    loop Pour chaque profondeur (1-10)
        loop Pour chaque technique d'évasion
            U->>T: GET /page?file=../../../etc/passwd
            alt Vulnérable
                T-->>U: 200 OK + "root:x:0:0"
                U->>U: 🔴 VULNERABLE!
            else Protégé
                T-->>U: 403/404/Filtèred
                U->>U: Essayer technique suivante
            end
        end
    end
</div>

**Points clés** :
1. L'outil établit d'abord une "baseline" avec une requête normale
2. Il teste ensuite chaque technique d'évasion
3. Il augmente progressivement la profondeur (nombre de `../`)
4. La détection se fait par analyse du contenu de la réponse


## Utilisation de DotDotSlash

### Installation

```bash
# Cloner le dépôt original
git clone https://github.com/jcesarstef/dotdotslash/
cd dotdotslash
```

### Exemples de commandes

```bash
# Usage basique : tester un paramètre vulnérable
python3 dotdotslash.py \
    --url "http://target.com/download?file=document.pdf" \
    --string "document.pdf"

# Avec cookie de session (pour applications authentifiées)
python3 dotdotslash.py \
    --url "http://target.com/download?file=document.pdf" \
    --string "document.pdf" \
    --cookie "PHPSESSID=abc123"

# Profondeur personnalisée et mode verbeux
python3 dotdotslash.py \
    --url "http://target.com/download?file=document.pdf" \
    --string "document.pdf" \
    --depth 15 \
    --verbose
```

### Arguments disponibles

| Argument | Description |
|----------|-------------|
| `--url, -u` | URL complète à tester |
| `--string, -s` | Chaîne à remplacer par les payloads |
| `--cookie, -c` | Cookie de session (optionnel) |
| `--depth` | Profondeur maximale des `../` (défaut: 10) |
| `--verbose` | Afficher les détails de chaque requête |


## Exemple de Sortie

Voici ce que vous verrez lorsqu'une vulnérabilité est détectée :

```
 ____        _   ____        _   ____  _           _
|  _ \  ___ | |_|  _ \  ___ | |_/ ___|| | __ _ ___| |__
| | | |/ _ \| __| | | |/ _ \| __\___ \| |/ _` / __| '_ \
| |_| | (_) | |_| |_| | (_) | |_ ___) | | (_| \__ \ | | |
|____/ \___/ \__|____/ \___/ \__|____/|_|\__,_|___/_| |_|

[*] Target: http://target.com/download?file=document.pdf
[*] Testing parameter: document.pdf
[*] Depth: 10

[+] Testing: ../etc/passwd
[-] Not vulnérable

[+] Testing: ../../etc/passwd
[-] Not vulnérable

[+] Testing: ../../../etc/passwd
[!] VULNERABLE! Status: 200, Length: 1847
[!] Content preview:
    root:x:0:0:root:/root:/bin/bash
    daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
    ...
```


## Fichiers Cibles Classiques

Selon le système d'exploitation cible, voici les fichiers les plus intéressants à rechercher :

| OS | Fichier | Contenu |
|----|---------|---------|
| Linux | `/etc/passwd` | Liste des utilisateurs |
| Linux | `/etc/shadow` | Hashes des mots de passe |
| Linux | `/etc/hosts` | Configuration DNS locale |
| Windows | `C:\Windows\win.ini` | Configuration Windows |
| Windows | `C:\boot.ini` | Configuration de démarrage |
| App | `../../../.env` | Variables d'environnement (clés API, mots de passe) |
| App | `../../../config.php` | Configuration de l'application |


## Pour Aller Plus Loin

- 📚 [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal) - Guide de référence
- 🔧 [dotdotslash Original](https://github.com/jcesarstef/dotdotslash) - Dépôt source
- 🎯 [VulnHub ZICO2](https://www.vulnhub.com/entry/zico2-1,210/) - VM d'entraînement


## Exploits et Vulnérabilités Connues

Le Path Traversal a été impliqué dans de nombreuses brèches de sécurité majeures :

| CVE | Produit | Description | Score CVSS |
|-----|---------|-------------|------------|
| **CVE-2021-41773** | Apache HTTP Server 2.4.49 | Path traversal permettant l'accès à des fichiers hors de la racine web, avec possibilité de RCE si mod_cgi est actif | 9.8 Critique |
| **CVE-2021-42013** | Apache HTTP Server 2.4.50 | Correction incomplète de CVE-2021-41773, contournable par double encodage URL | 9.8 Critique |
| **CVE-2020-5902** | F5 BIG-IP | Traversal dans l'interface TMUI permettant l'exécution de code à distance non authentifiée | 9.8 Critique |
| **CVE-2019-19781** | Citrix ADC/Gateway | Path traversal permettant l'écriture de fichiers et l'exécution de code arbitraire | 9.8 Critique |
| **CVE-2018-7600** | Drupal (Drupalgeddon2) | Combinaison de path traversal et injection permettant RCE sans authentification | 9.8 Critique |

La vulnérabilité CVE-2021-41773 d'Apache est particulièrement intéressante car elle a été corrigée de manière incomplète dans la version 2.4.50 (CVE-2021-42013), démontrant la difficulté de filtrer correctement les séquences de traversal.


## Approfondissement Théorique

### La normalisation des chemins : un problème complexe

Le coeur du problème du path traversal réside dans la **normalisation des chemins**. Un système de fichiers interprète `/var/www/../etc` comme `/var/etc`, mais l'application peut voir le chemin littéral avant résolution. Cette différence de perspective entre l'application et le système de fichiers est à l'origine de la vulnérabilité. Les langages comme Java avec `getCanonicalPath()` ou Python avec `os.path.realpath()` permettent de résoudre un chemin vers sa forme canonique, mais cette résolution doit être faite **avant** toute validation, pas après.

### Les variantes selon les systèmes de fichiers

Les systèmes de fichiers diffèrent dans leur interprétation des chemins spéciaux. Sous Windows, les **ADS** (Alternate Data Streams) permettent d'accéder à des flux de données cachés via `file.txt::$DATA`. Les **chemins UNC** (`\\server\share`) peuvent être utilisés pour forcer des connexions SMB sortantes et potentiellement capturer des hashes NTLM. Sous Linux, les liens symboliques dans `/proc` peuvent permettre d'accéder à des fichiers inattendus : `/proc/self/fd/3` peut pointer vers un fichier ouvert par le processus, même s'il a été supprimé du système de fichiers.

### Defense en profondeur contre le path traversal

La meilleure protection combine plusieurs couches. Premièrement, utiliser une **whitelist** de fichiers autorisés plutôt que de filtrer les chemins suspects. Deuxièmement, exécuter l'application dans un **chroot** ou un conteneur pour limiter physiquement les fichiers accessibles. Troisièmement, configurer les permissions du système de fichiers selon le principe du moindre privilège : le processus web ne devrait pouvoir lire que les fichiers strictement nécessaires. Enfin, les **SELinux/AppArmor** peuvent fournir une couche supplémentaire de contrôle d'accès obligatoire (MAC) indépendante des permissions UNIX traditionnelles.


---

