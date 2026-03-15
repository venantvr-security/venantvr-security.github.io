---
layout: default
title: "Python.Ransomware"
description: "Tutoriel Éducatif - Fonctionnement d'un Ransomware"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Ransomware</span>
</div>

<div class="page-header">
  <h1>Python.Ransomware</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Ransomware" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Tutoriel Éducatif - Fonctionnement d'un Ransomware

> **AVERTISSEMENT** : Ce projet est **strictement éducatif**. L'utilisation malveillante est illégale et passible de poursuites pénales.

## Introduction

Les ransomwares représentent l'une des menaces les plus dévastatrices dans le paysage de la cybersécurité actuel. Pour mieux s'en protéger, il est essentiel de comprendre leur fonctionnement interne. Ce projet, accompagné d'un [tutoriel YouTube détaillé](https://www.youtube.com/watch?v=ScL07VJJOX4), décortique les mécanismes d'un ransomware utilisant le **chiffrement hybride RSA + Fernet (AES)**.

L'objectif n'est pas de créer des outils malveillants, mais de former les professionnels de la sécurité à reconnaître, analyser et contrer ces menaces. En comprenant comment un attaquant procède, vous serez mieux armé pour protéger vos systèmes.

### Ce que vous allez apprendre

À travers ce tutoriel, vous découvrirez :

- **Le chiffrement hybride** : pourquoi les ransomwares combinent RSA et AES plutôt que d'utiliser un seul algorithme
- **Les mécanismes de persistance** : comment le malware s'assure de survivre aux redémarrages
- **Les IOCs (Indicateurs de Compromission)** : les traces laissées par un ransomware que vous pouvez surveiller
- **Les stratégies de défense** : les bonnes pratiques pour se protéger efficacement


## Théorie : Comprendre le Chiffrement Hybride

Avant de plonger dans le code, il est crucial de comprendre pourquoi les ransomwares utilisent une approche hybride plutôt qu'un simple algorithme de chiffrement.

### Le problème du chiffrement asymétrique seul

RSA est un algorithme de chiffrement asymétrique très sécurisé, mais il présente un inconvénient majeur : **il est extrêmement lent** pour chiffrer de grandes quantités de données. Chiffrer des gigaoctets de fichiers avec RSA prendrait des heures, voire des jours.

### La solution : combiner RSA et AES (Fernet)

Les ransomwares modernes résolvent ce problème en combinant deux algorithmes complémentaires :

| Algorithme | Type | Vitesse | Utilisation dans le ransomware |
|------------|------|---------|-------------------------------|
| **RSA** | Asymétrique | Lent | Chiffre uniquement la petite clé Fernet (quelques octets) |
| **Fernet (AES)** | Symétrique | Très rapide | Chiffre tous les fichiers de la victime |

Cette approche offre le meilleur des deux mondes : la **sécurité de RSA** (seul l'attaquant possède la clé privée) et la **rapidité de AES** (chiffrement quasi-instantané des fichiers).

### Visualisation du processus

Le diagramme ci-dessous illustre comment les deux clés interagissent entre l'attaquant et la victime. Remarquez que la clé privée RSA (en rouge) ne quitte jamais l'environnement de l'attaquant, ce qui rend le déchiffrement impossible sans payer la rançon.

<div class="mermaid">
flowchart TB
    subgraph ATTACKER["👤 Attaquant"]
        RSA_PRIV["🔑 RSA Private Key<br/><i>Gardée secrète</i>"]
        RSA_PUB["🔓 RSA Public Key<br/><i>Distribuée avec le malware</i>"]
    end

    subgraph VICTIM["🎯 Machine Victime"]
        subgraph ENCRYPT["Phase 1 : Chiffrement"]
            F1["1. Générer clé Fernet aléatoire"]
            F2["2. Chiffrer tous les fichiers .txt"]
            F3["3. Chiffrer la clé Fernet avec RSA_PUB"]
            F4["4. Créer EMAIL_ME.txt"]
        end

        subgraph DECRYPT["Phase 2 : Déchiffrement"]
            D1["1. Récupérer clé Fernet déchiffrée"]
            D2["2. Déchiffrer tous les fichiers"]
        end
    end

    RSA_PUB -->|"Intégrée au malware"| F3
    F1 --> F2 --> F3 --> F4
    F4 -->|"Envoyé par la victime"| RSA_PRIV
    RSA_PRIV -->|"Clé Fernet déchiffrée"| D1 --> D2

    style RSA_PRIV fill:#e74c3c,fill-opacity:0.15
    style RSA_PUB fill:#2ecc71,fill-opacity:0.15
    style F4 fill:#f39c12,fill-opacity:0.15
    style DECRYPT fill:#808080,fill-opacity:0.15
    style ENCRYPT fill:#808080,fill-opacity:0.15
    style VICTIM fill:#808080,fill-opacity:0.15
    style ATTACKER fill:#808080,fill-opacity:0.15
</div>


## Déroulement d'une Attaque : Étape par Étape

Maintenant que vous comprenez la théorie, voyons concrètement comment se déroule une attaque ransomware, de la préparation par l'attaquant jusqu'au (potentiel) déchiffrement des fichiers.

### Vue d'ensemble du scénario

Le diagramme de séquence ci-dessous montre les trois phases distinctes d'une attaque ransomware. Chaque phase est colorée différemment pour faciliter la compréhension :
- **Rouge** : Préparation de l'attaquant (avant l'infection)
- **Bleu** : Infection et chiffrement (exécution du malware)
- **Vert** : Négociation et déchiffrement (après paiement)

<div class="mermaid">
sequenceDiagram
    autonumber
    participant À as 👤 Attaquant
    participant V as 🎯 Victime

    rect rgb(231, 76, 60, 0.2)
        Note over A: Phase 1 : Préparation
        A->>A: Générer paire de clés RSA
        Note right of A: La clé privée reste<br/>chez l'attaquant
        A->>V: Intégrer RSA public key dans le malware
    end

    rect rgb(52, 152, 219, 0.2)
        Note over V: Phase 2 : Infection
        V->>V: Générer clé Fernet unique
        V->>V: Parcourir et chiffrer tous les .txt
        V->>V: Chiffrer la clé Fernet avec RSA
        V->>V: Sauvegarder dans EMAIL_ME.txt
        Note right of V: La clé Fernet originale<br/>est détruite de la mémoire
    end

    rect rgb(46, 204, 113, 0.2)
        Note over A,V: Phase 3 : Rançon
        V->>A: Envoyer EMAIL_ME.txt
        A->>A: Déchiffrer avec clé privée RSA
        Note right of A: Récupère la clé Fernet
        A->>V: Envoyer PUT_ME_ON_DESKTOP.txt
        V->>V: Utiliser la clé pour déchiffrer
    end
</div>

### Points clés à retenir

1. **La clé privée RSA ne transite jamais** : c'est ce qui rend le ransomware si efficace. Sans elle, le déchiffrement est mathématiquement impossible.

2. **Une clé Fernet unique par victime** : chaque infection génère une nouvelle clé aléatoire, empêchant l'utilisation d'un décrypteur universel.

3. **Le fichier EMAIL_ME.txt est la "rançon"** : il contient la clé Fernet chiffrée que seul l'attaquant peut décoder.


## Mise en Pratique (Environnement de Test Isolé)

> ⚠️ **ATTENTION** : N'exécutez JAMAIS ces scripts sur une machine de production ou contenant des données importantes. Utilisez uniquement une machine virtuelle isolée avec des fichiers de test.

Pour expérimenter en toute sécurité, voici les commandes à exécuter dans l'ordre. Chaque étape correspond à un acteur différent (attaquant ou victime).

```bash
# ═══════════════════════════════════════════════════════
# ÉTAPE 1 : L'attaquant prépare ses clés
# ═══════════════════════════════════════════════════════
python rsa_key_generator.py
# Génère : private_key.pem (secret) et public_key.pem

# ═══════════════════════════════════════════════════════
# ÉTAPE 2 : Le ransomware s'exécute sur la machine victime
# ═══════════════════════════════════════════════════════
# ⚠️ UNIQUEMENT dans un dossier de test (localRoot)
python ransomware.py
# Résultat : fichiers .txt chiffrés + EMAIL_ME.txt créé

# ═══════════════════════════════════════════════════════
# ÉTAPE 3 : L'attaquant déchiffré la clé Fernet
# ═══════════════════════════════════════════════════════
python fernet_decryptor.py EMAIL_ME.txt
# Génère : PUT_ME_ON_DESKTOP.txt contenant la clé Fernet

# ═══════════════════════════════════════════════════════
# ÉTAPE 4 : La victime récupère ses fichiers
# ═══════════════════════════════════════════════════════
# Placer PUT_ME_ON_DESKTOP.txt sur le bureau
# Le script de déchiffrement utilisé cette clé
```


## Se Défendre : Détection et Protection

Comprendre l'attaque, c'est bien. Savoir s'en protéger, c'est mieux ! Cette section présente les deux approches complémentaires : **détecter** une infection en cours et **prévenir** les attaques futures.

### Stratégies de défense

Le diagramme ci-dessous résume les principales mesures de sécurité. À gauche, les techniques de détection permettent d'identifier une attaque rapidement. À droite, les mesures préventives réduisent les risques d'infection.

<div class="mermaid">
flowchart LR
    subgraph Détéction["🔍 Détection (pendant l'attaque)"]
        D1["📁 Monitoring des fichiers<br/><i>Alertes sur modifications massives</i>"]
        D2["📛 Extensions suspectes<br/><i>.encrypted, .locked, .crypto</i>"]
        D3["⚡ Activité crypto élevée<br/><i>CPU à 100% sans raison</i>"]
    end

    subgraph Defense["🛡️ Prévention (avant l'attaque)"]
        F1["💾 Sauvegardes 3-2-1<br/><i>3 copies, 2 supports, 1 hors-site</i>"]
        F2["🔒 Segmentation réseau<br/><i>Limiter la propagation</i>"]
        F3["🛡️ EDR/Antivirus<br/><i>Détection comportementale</i>"]
    end

    Détéction -->|"Alerte immédiate"| Response["🚨 Réponse à incident"]
    Defense -->|"Réduction des risques"| Safe["✅ Système protégé"]

    style Détéction fill:#e74c3c,fill-opacity:0.15
    style Defense fill:#2ecc71,fill-opacity:0.15
    style Response fill:#f39c12,fill-opacity:0.15
</div>

### La règle d'or : les sauvegardes 3-2-1

La meilleure protection contre les ransomwares reste une stratégie de sauvegarde solide :

- **3 copies** de vos données importantes
- **2 supports différents** (disque dur externe, NAS, cloud...)
- **1 copie hors-site** (géographiquement séparée ou déconnectée)

Si vous êtes infecté et que vous avez des sauvegardes récentes et intègres, vous pouvez simplement restaurer vos données sans payer la rançon.


## Pour Aller Plus Loin

Ce tutoriel n'est qu'une introduction. Pour approfondir vos connaissances sur les ransomwares et la cryptographie, consultez ces ressources :

- 🎬 [Tutoriel YouTube complet](https://www.youtube.com/watch?v=ScL07VJJOX4) - Démonstration vidéo pas à pas
- 📚 [Documentation Cryptography Python](https://cryptography.io/) - La bibliothèque utilisée pour Fernet
- 🆘 [No More Ransom](https://www.nomoreransom.org/) - Initiative proposant des décrypteurs gratuits pour certains ransomwares connus


## Exploits et Vulnérabilités Connues

Les ransomwares exploitent souvent des vulnérabilités connues pour se propager. Voici des exemples majeurs illustrant les vecteurs d'attaque :

- **CVE-2017-0144 (EternalBlue/MS17-010)** : Vulnérabilité SMBv1 exploitée par WannaCry et NotPetya. WannaCry a infecté plus de 230 000 systèmes dans 150 pays en mai 2017, causant des milliards de dollars de dégâts. Cette CVE reste exploitée aujourd'hui par des ransomwares ciblant des systèmes non patchés.

- **CVE-2019-19781 (Citrix ADC)** : Path traversal permettant RCE, exploitée par le ransomware EKANS/Snake et d'autres pour l'accès initial aux réseaux d'entreprise. Démontre l'importance du patching des appliances périmétriques.

- **CVE-2021-34527 (PrintNightmare)** : Vulnérabilité dans le spouleur d'impression Windows permettant RCE. Utilisée par plusieurs groupes ransomware (Magniber, Vice Society) pour le mouvement latéral après compromission initiale.

- **CVE-2021-21974 (VMware ESXi)** : Heap overflow dans OpenSLP exploitée par le ransomware ESXiArgs en 2023. A démontré que les infrastructures de virtualisation sont des cibles privilégiées pour maximiser l'impact.

- **CVE-2023-27350 (PaperCut)** : Vulnérabilité dans le logiciel de gestion d'impression exploitée par les groupes Cl0p et LockBit. Illustre la tendance des ransomwares à cibler des logiciels d'entreprise spécifiques.


## Approfondissement Théorique

Le chiffrement hybride utilisé par les ransomwares modernes s'appuie sur des principes cryptographiques solides. L'algorithme RSA (Rivest-Shamir-Adleman), basé sur la difficulté de factoriser de grands nombres premiers, fournit la sécurité asymétrique : même si la clé publique est connue, dériver la clé privée est computationnellement infaisable avec les tailles de clés actuelles (2048-4096 bits). Fernet, qui encapsule AES-128 en mode CBC avec authentification HMAC-SHA256, assure le chiffrement rapide et authentifié des fichiers. Cette combinaison est identique à celle utilisée en TLS/SSL pour sécuriser le web.

L'évolution des ransomwares montre une sophistication croissante. Les premières générations (CryptoLocker, 2013) utilisaient déjà le chiffrement hybride mais ciblaient des particuliers. La deuxième génération a introduit le "Ransomware-as-a-Service" (RaaS) où des opérateurs fournissent l'infrastructure et les affiliés exécutent les attaques. La troisième génération, appelée "double extortion", exfiltre les données avant chiffrement et menace de les publier, rendant les sauvegardes insuffisantes comme défense. Des groupes comme Maze, REvil, et LockBit ont perfectionné ce modèle.

Les techniques de défense doivent adresser chaque phase de l'attaque. La prévention passe par le patching, la segmentation réseau, et la formation des utilisateurs au phishing. La détection s'appuie sur les EDR (Endpoint Detection and Response) qui surveillent les comportements suspects : accès massif aux fichiers, appels aux APIs cryptographiques, modifications d'extensions. La réponse inclut l'isolement immédiat des machines infectées et l'analyse forensique pour déterminer le patient zero. La récupération repose sur les sauvegardes testées régulièrement et stockées hors-ligne ou immuables (air-gap ou WORM).


---

