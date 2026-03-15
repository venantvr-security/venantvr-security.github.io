#!/usr/bin/env python3
"""
Contenu additionnel - Partie 3 (derniers repos)
"""

ADDITIONAL_CONTENT_3 = {
    "Python.Osint.Blackbird": {
        "title": "OSINT - Reconnaissance Open Source",
        "intro": """
## Introduction

**OSINT (Open Source Intelligence)** désigne la collecte d'informations à partir de sources publiques. **Blackbird** est un outil de recherche d'usernames.

### Sources OSINT

- Réseaux sociaux
- Bases de données publiques
- Moteurs de recherche
- Archives web
- Metadata de fichiers
""",
        "theory": """
## Théorie et Concepts

### Workflow OSINT

```
1. DÉFINIR LA CIBLE
   └──► Nom, email, username, domaine

2. COLLECTER
   ├──► Moteurs de recherche
   ├──► Réseaux sociaux
   ├──► Bases publiques
   └──► Dark web

3. ANALYSER
   ├──► Corrélations
   ├──► Graphes relationnels
   └──► Timeline

4. DOCUMENTER
   └──► Rapport structuré
```

### Recherche par username

```
Username "johndoe123" trouvé sur:
├── Twitter: @johndoe123
├── GitHub: github.com/johndoe123
├── Reddit: u/johndoe123
└── LinkedIn: (corrélation via bio)
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Recherche de username

```python
import requests
from concurrent.futures import ThreadPoolExecutor

PLATFORMS = {
    'github': 'https://github.com/{}',
    'twitter': 'https://twitter.com/{}',
    'instagram': 'https://instagram.com/{}',
    'reddit': 'https://reddit.com/user/{}',
    'linkedin': 'https://linkedin.com/in/{}',
    'youtube': 'https://youtube.com/@{}',
    'tiktok': 'https://tiktok.com/@{}',
}

def check_username(platform, url_template, username):
    url = url_template.format(username)
    try:
        r = requests.get(url, timeout=10, allow_redirects=True)
        if r.status_code == 200:
            return {'platform': platform, 'url': url, 'found': True}
    except:
        pass
    return {'platform': platform, 'url': url, 'found': False}

def search_username(username):
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(check_username, platform, url, username)
            for platform, url in PLATFORMS.items()
        ]

        for future in futures:
            result = future.result()
            if result['found']:
                print(f"[+] {result['platform']}: {result['url']}")
                results.append(result)

    return results

# Utilisation
search_username("johndoe")
```

### 2. Recherche d'email

```python
import requests

def search_email(email):
    results = {}

    # Have I Been Pwned (nécessite API key)
    # https://haveibeenpwned.com/API/v3

    # Hunter.io (vérification domaine)
    domain = email.split('@')[1]
    hunter_url = f"https://api.hunter.io/v2/domain-search?domain={domain}"

    # Gravatar
    import hashlib
    email_hash = hashlib.md5(email.lower().encode()).hexdigest()
    gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
    try:
        r = requests.get(gravatar_url)
        if r.status_code == 200:
            results['gravatar'] = gravatar_url
    except:
        pass

    return results
```

### 3. Google Dorks

```python
def generate_dorks(target):
    dorks = [
        f'site:linkedin.com "{target}"',
        f'site:facebook.com "{target}"',
        f'site:github.com "{target}"',
        f'"{target}" filetype:pdf',
        f'"{target}" email OR contact',
        f'inurl:"{target}"',
        f'"{target}" password OR leak',
    ]
    return dorks

# Générer les recherches
for dork in generate_dorks("John Doe"):
    print(f"https://google.com/search?q={dork}")
```

### 4. Metadata d'images

```python
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract_metadata(image_path):
    img = Image.open(image_path)
    exif_data = {}

    if hasattr(img, '_getexif') and img._getexif():
        for tag_id, value in img._getexif().items():
            tag = TAGS.get(tag_id, tag_id)
            exif_data[tag] = value

    # GPS si présent
    if 'GPSInfo' in exif_data:
        gps = {}
        for key, val in exif_data['GPSInfo'].items():
            tag = GPSTAGS.get(key, key)
            gps[tag] = val
        exif_data['GPS'] = gps

    return exif_data

# Extraire les métadonnées
metadata = extract_metadata("photo.jpg")
print(f"Appareil: {metadata.get('Make')} {metadata.get('Model')}")
print(f"Date: {metadata.get('DateTime')}")
```
""",
        "best_practices": """
## Bonnes Pratiques

### Documentation

```python
# Toujours documenter les sources
finding = {
    'data': 'johndoe@example.com',
    'source': 'Twitter bio',
    'url': 'https://twitter.com/johndoe',
    'date': '2024-01-15',
    'confidence': 'high'
}
```

### Éthique

- Respecter la vie privée
- Ne collecter que le nécessaire
- Documenter l'usage légal
- Pas de harcèlement
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Homonymes

```python
# Vérifier les corrélations
# "John Doe" sur Twitter ≠ forcément le même sur LinkedIn
# Chercher des points communs (photo, bio, liens)
```
""",
        "tools": """
## Outils OSINT

- **Maltego** : Graphes relationnels
- **Shodan** : Recherche IoT/serveurs
- **Recon-ng** : Framework OSINT
- **theHarvester** : Emails et sous-domaines
- **SpiderFoot** : Automatisation OSINT
""",
        "references": """
## Références

- [OSINT Framework](https://osintframework.com/)
- [Awesome OSINT](https://github.com/jivoi/awesome-osint)
"""
    },

    "Python.Network.Pivot": {
        "title": "Pivoting Réseau - Techniques Avancées",
        "intro": """
## Introduction

Le **pivoting** permet d'utiliser une machine compromise comme relais pour accéder à des réseaux autrement inaccessibles.

### Scénario type

```
Attaquant → [Internet] → Machine A → [Réseau interne] → Machine B
                         (compromis)                    (cible finale)
```
""",
        "theory": """
## Théorie et Concepts

### Types de pivoting

| Technique | Description | Outil |
|-----------|-------------|-------|
| Port forwarding | Redirection de port | SSH, netsh |
| SOCKS proxy | Proxy dynamique | SSH, Chisel |
| VPN | Tunnel complet | Ligolo, OpenVPN |
| Meterpreter | Routes intégrées | Metasploit |

### SSH Port Forwarding

```
Local Forward (-L):
Attacker:8080 → SSH → Pivot → Target:80
"Amène le port distant vers moi"

Remote Forward (-R):
Target:80 → Pivot → SSH → Attacker:8080
"Expose mon port vers là-bas"

Dynamic (-D):
Proxy SOCKS sur le pivot
"Tout le trafic passe par là"
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. SSH Local Port Forward

```bash
# Accéder au port 80 de 10.10.10.5 via pivot
ssh -L 8080:10.10.10.5:80 user@pivot

# Maintenant sur l'attaquant:
curl http://localhost:8080
# → Accède à 10.10.10.5:80
```

### 2. SSH Dynamic SOCKS Proxy

```bash
# Créer un proxy SOCKS
ssh -D 9050 user@pivot

# Utiliser avec proxychains
# /etc/proxychains.conf:
# socks5 127.0.0.1 9050

proxychains nmap -sT -Pn 10.10.10.0/24
```

### 3. Chisel (Sans SSH)

```bash
# Sur l'attaquant (serveur)
./chisel server --reverse --port 8080

# Sur le pivot (client)
./chisel client ATTACKER:8080 R:socks

# SOCKS5 disponible sur attaquant:1080
proxychains curl http://10.10.10.5
```

### 4. Python Proxy Simple

```python
import socket
import threading

def handle_client(client, target_host, target_port):
    # Connexion à la cible
    target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target.connect((target_host, target_port))

    # Relai bidirectionnel
    def forward(src, dst):
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.send(data)

    t1 = threading.Thread(target=forward, args=(client, target))
    t2 = threading.Thread(target=forward, args=(target, client))
    t1.start()
    t2.start()

def port_forward(local_port, target_host, target_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', local_port))
    server.listen(5)

    print(f"Forwarding :{local_port} → {target_host}:{target_port}")

    while True:
        client, addr = server.accept()
        print(f"Connection from {addr}")
        t = threading.Thread(target=handle_client,
                            args=(client, target_host, target_port))
        t.start()

# Usage: Forward local 8080 vers 10.10.10.5:80
port_forward(8080, '10.10.10.5', 80)
```

### 5. Double pivot

```bash
# Pivot 1: accès au réseau 10.10.10.0/24
ssh -D 9050 user@pivot1

# Pivot 2: via pivot1, accès au réseau 192.168.1.0/24
proxychains ssh -D 9051 user@10.10.10.5

# Configurer proxychains en chaîne:
# [ProxyList]
# socks5 127.0.0.1 9050
# socks5 127.0.0.1 9051
```
""",
        "best_practices": """
## Bonnes Pratiques

### Garder les tunnels stables

```bash
# Autossh pour reconnecter automatiquement
autossh -M 0 -f -N -D 9050 \\
    -o "ServerAliveInterval 30" \\
    -o "ServerAliveCountMax 3" \\
    user@pivot
```

### Documentation

```
Pivot: 192.168.1.50 (compromis)
├── Accès: SSH avec clé
├── Réseaux accessibles:
│   ├── 10.10.10.0/24 (via eth1)
│   └── 172.16.0.0/24 (via eth2)
└── Tunnels actifs:
    └── SOCKS5 :9050 → 10.10.10.0/24
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Oublier le trafic DNS

```bash
# Avec proxychains, le DNS peut fuiter!
# Utiliser proxy_dns dans proxychains.conf
proxy_dns
```
""",
        "tools": """
## Outils

- **SSH** : Port forwarding natif
- **Chisel** : HTTP tunneling
- **Ligolo-ng** : Tunnel moderne
- **sshuttle** : VPN over SSH
- **proxychains** : Chaîner les proxies
""",
        "references": """
## Références

- [SSH Tunneling Explained](https://www.ssh.com/academy/ssh/tunneling)
- [Chisel](https://github.com/jpillora/chisel)
"""
    },

    "Python.Network.Connections": {
        "title": "Analyse des Connexions Réseau",
        "intro": """
## Introduction

Surveiller les **connexions réseau** actives permet de détecter les anomalies, backdoors, et exfiltrations de données.

### Indicateurs clés

- Connexions vers des IP inconnues
- Ports inhabituels
- Trafic à des heures anormales
- Volume de données suspect
""",
        "theory": """
## Théorie et Concepts

### États TCP

```
LISTEN      → En attente de connexions
ESTABLISHED → Connexion active
TIME_WAIT   → Fermeture en cours
CLOSE_WAIT  → Attend fermeture locale
SYN_SENT    → Connexion en cours
```

### Informations clés

```
Proto  Local            Remote           State       PID
TCP    192.168.1.10:443 8.8.8.8:80       ESTABLISHED 1234
│      │                │                │           │
└──────┴────────────────┴────────────────┴───────────┘
Quoi connecte quoi, dans quel état, quel processus
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Lister les connexions (Python)

```python
import psutil

def list_connections():
    connections = []

    for conn in psutil.net_connections(kind='inet'):
        try:
            process = psutil.Process(conn.pid)
            proc_name = process.name()
        except:
            proc_name = 'N/A'

        connections.append({
            'proto': 'TCP' if conn.type == 1 else 'UDP',
            'local': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else '-',
            'remote': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else '-',
            'status': conn.status,
            'pid': conn.pid,
            'process': proc_name
        })

    return connections

# Afficher
for c in list_connections():
    if c['status'] == 'ESTABLISHED':
        print(f"{c['process']:20} {c['local']:25} → {c['remote']:25}")
```

### 2. Détection d'anomalies

```python
import psutil
from ipaddress import ip_address
import socket

SUSPICIOUS_PORTS = {4444, 5555, 6666, 31337}  # Ports backdoor courants
SUSPICIOUS_COUNTRIES = {'CN', 'RU', 'KP'}     # À adapter

def check_suspicious_connections():
    alerts = []

    for conn in psutil.net_connections(kind='inet'):
        if conn.status != 'ESTABLISHED' or not conn.raddr:
            continue

        remote_ip = conn.raddr.ip
        remote_port = conn.raddr.port

        # Port suspect ?
        if remote_port in SUSPICIOUS_PORTS:
            alerts.append({
                'type': 'suspicious_port',
                'ip': remote_ip,
                'port': remote_port,
                'pid': conn.pid
            })

        # IP privée vers internet sur port non-standard ?
        try:
            local = ip_address(conn.laddr.ip)
            remote = ip_address(remote_ip)
            if local.is_private and not remote.is_private:
                if remote_port not in {80, 443, 53, 22}:
                    alerts.append({
                        'type': 'unusual_outbound',
                        'ip': remote_ip,
                        'port': remote_port,
                        'pid': conn.pid
                    })
        except:
            pass

    return alerts

# Vérifier
for alert in check_suspicious_connections():
    print(f"[ALERT] {alert['type']}: {alert['ip']}:{alert['port']}")
```

### 3. Monitoring continu

```python
import psutil
import time
from collections import defaultdict

class ConnectionMonitor:
    def __init__(self):
        self.known_connections = set()
        self.connection_history = defaultdict(list)

    def snapshot(self):
        current = set()

        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'ESTABLISHED' and conn.raddr:
                key = (conn.laddr, conn.raddr, conn.pid)
                current.add(key)

        # Nouvelles connexions
        new_conns = current - self.known_connections
        for conn in new_conns:
            print(f"[NEW] {conn[0]} → {conn[1]} (PID: {conn[2]})")

        # Connexions fermées
        closed_conns = self.known_connections - current
        for conn in closed_conns:
            print(f"[CLOSED] {conn[0]} → {conn[1]}")

        self.known_connections = current

    def run(self, interval=5):
        print("Monitoring connections...")
        while True:
            self.snapshot()
            time.sleep(interval)

# Lancer
monitor = ConnectionMonitor()
monitor.run()
```

### 4. Export des données

```python
import json
import csv

def export_connections(filename, format='json'):
    conns = list_connections()

    if format == 'json':
        with open(filename, 'w') as f:
            json.dump(conns, f, indent=2)

    elif format == 'csv':
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=conns[0].keys())
            writer.writeheader()
            writer.writerows(conns)

export_connections('connections.json')
```
""",
        "best_practices": """
## Bonnes Pratiques

### Baseline

```python
# Établir une baseline de connexions normales
# puis alerter sur les déviations

BASELINE = {
    'chrome.exe': {443, 80},
    'outlook.exe': {443, 993, 587},
    'ssh': {22},
}
```

### Logging

```python
import logging

logging.basicConfig(
    filename='/var/log/connections.log',
    format='%(asctime)s - %(message)s'
)
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Ignorer les connexions locales

```python
# Les backdoors peuvent utiliser localhost!
if conn.raddr.ip != '127.0.0.1':
    # Ne pas ignorer complètement localhost
```
""",
        "tools": """
## Outils CLI

```bash
# netstat
netstat -tunap

# ss (plus moderne)
ss -tunap

# lsof
lsof -i -P -n
```
""",
        "references": """
## Références

- [psutil Documentation](https://psutil.readthedocs.io/)
"""
    },

    "Python.Usb.Test": {
        "title": "Tests de Sécurité USB",
        "intro": """
## Introduction

Les **périphériques USB** représentent un vecteur d'attaque important : keyloggers, BadUSB, exfiltration de données, etc.

### Risques USB

- HID Injection (clavier malveillant)
- Malware via autorun
- Exfiltration de données
- Attaques physiques (USB Killer)
""",
        "theory": """
## Théorie et Concepts

### Classes USB

| Classe | Description | Risque |
|--------|-------------|--------|
| HID | Clavier/Souris | Injection de frappes |
| Mass Storage | Clé USB | Malware, exfiltration |
| CDC | Communication | Backdoor réseau |
| DFU | Firmware update | Modification firmware |

### BadUSB

```
Clé USB normale:
[USB Controller] → [Flash Storage]

BadUSB:
[USB Controller] → [Microcontrôleur]
                         │
                         ├──► Émule clavier
                         ├──► Exécute payload
                         └──► Parfois: stockage aussi
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Détecter les périphériques USB

```python
import usb.core
import usb.util

def list_usb_devices():
    devices = []

    for dev in usb.core.find(find_all=True):
        try:
            manufacturer = usb.util.get_string(dev, dev.iManufacturer)
            product = usb.util.get_string(dev, dev.iProduct)
        except:
            manufacturer = 'Unknown'
            product = 'Unknown'

        devices.append({
            'vendor_id': hex(dev.idVendor),
            'product_id': hex(dev.idProduct),
            'manufacturer': manufacturer,
            'product': product,
            'class': dev.bDeviceClass
        })

    return devices

for dev in list_usb_devices():
    print(f"{dev['vendor_id']}:{dev['product_id']} - {dev['product']}")
```

### 2. Monitoring des événements USB

```python
import pyudev
import time

def monitor_usb():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    print("Monitoring USB events...")

    for device in iter(monitor.poll, None):
        if device.action == 'add':
            print(f"[CONNECTED] {device.get('ID_VENDOR')} - {device.get('ID_MODEL')}")

            # Vérifier si c'est un HID
            if 'ID_USB_INTERFACES' in device.properties:
                if ':03' in device.get('ID_USB_INTERFACES'):
                    print("[WARNING] HID device detected!")

        elif device.action == 'remove':
            print(f"[DISCONNECTED] {device.sys_name}")

monitor_usb()
```

### 3. Politique de whitelist

```python
ALLOWED_DEVICES = {
    ('0x046d', '0xc52b'),  # Logitech Receiver
    ('0x8087', '0x0024'),  # Intel Hub
}

def check_device_allowed(vendor_id, product_id):
    return (vendor_id, product_id) in ALLOWED_DEVICES

def enforce_usb_policy():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    for device in iter(monitor.poll, None):
        if device.action == 'add':
            vid = device.get('ID_VENDOR_ID')
            pid = device.get('ID_MODEL_ID')

            if not check_device_allowed(vid, pid):
                print(f"[BLOCKED] Unauthorized device: {vid}:{pid}")
                # Désactiver le périphérique
                # (nécessite des droits admin et udev rules)
```

### 4. Détection d'exfiltration

```python
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class USBExfiltrationDetector(FileSystemEventHandler):
    def __init__(self, threshold_mb=100):
        self.threshold = threshold_mb * 1024 * 1024
        self.copy_size = 0
        self.start_time = time.time()

    def on_created(self, event):
        if not event.is_directory:
            try:
                size = os.path.getsize(event.src_path)
                self.copy_size += size

                elapsed = time.time() - self.start_time
                if elapsed < 60 and self.copy_size > self.threshold:
                    print(f"[ALERT] Mass copy detected: {self.copy_size/1024/1024:.1f}MB")

            except:
                pass

# Surveiller les montages USB
def monitor_usb_mounts():
    observer = Observer()
    handler = USBExfiltrationDetector()

    # Surveiller /media ou /mnt
    observer.schedule(handler, '/media', recursive=True)
    observer.start()
```
""",
        "best_practices": """
## Bonnes Pratiques

### Politique USB stricte

```bash
# Bloquer tous les USB storage
# /etc/modprobe.d/usb-storage.conf
blacklist usb-storage

# Ou via udev rules
# /etc/udev/rules.d/99-usb-block.rules
ACTION=="add", SUBSYSTEMS=="usb", ATTR{authorized}="0"
```

### Chiffrement obligatoire

```python
# Vérifier si le périphérique est chiffré
# avant d'autoriser l'accès
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Faire confiance aux VID/PID

```python
# Les VID/PID peuvent être falsifiés!
# Un Arduino peut se faire passer pour un clavier Logitech
# Utiliser des certificats ou du hardware attestation
```
""",
        "tools": """
## Outils

- **USBGuard** : Politique USB Linux
- **usbutils** : lsusb et outils
- **Rubber Ducky** : Test HID injection
""",
        "references": """
## Références

- [USBGuard](https://usbguard.github.io/)
- [BadUSB](https://srlabs.de/badusb/)
"""
    },

    "Python.HAR.Scanner": {
        "title": "Scanner de Fichiers HAR",
        "intro": """
## Introduction

Les fichiers **HAR (HTTP Archive)** capturent tout le trafic HTTP d'une session de navigation. L'analyse permet de détecter des fuites de données et problèmes de sécurité.

### Contenus sensibles à rechercher

- Tokens d'authentification
- Mots de passe
- Données personnelles
- Clés API
""",
        "theory": """
## Théorie et Concepts

### Structure HAR

```json
{
  "log": {
    "entries": [
      {
        "request": {
          "url": "...",
          "headers": [...],
          "postData": {...}
        },
        "response": {
          "status": 200,
          "headers": [...],
          "content": {...}
        }
      }
    ]
  }
}
```

### Données à risque

| Type | Pattern | Risque |
|------|---------|--------|
| JWT | eyJ... | Session hijacking |
| API Key | key=xxx | Accès non autorisé |
| Password | password= | Credential theft |
| Credit Card | \\d{16} | Fraude |
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Parser et analyser

```python
import json
import re
from urllib.parse import parse_qs, urlparse

class HARScanner:
    PATTERNS = {
        'jwt': r'eyJ[A-Za-z0-9_-]+\\.eyJ[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+',
        'api_key': r'["\\'](api[_-]?key|apikey)["\\']\s*[:=]\s*["\\']([^"\\'])+["\\']]',
        'password': r'password["\\'\\s]*[:=]["\\'\\s]*([^"\\'\n&]+)',
        'credit_card': r'\\b\\d{13,16}\\b',
        'email': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+',
        'bearer': r'Bearer\\s+[A-Za-z0-9_-]+',
    }

    def __init__(self, har_file):
        with open(har_file, 'r') as f:
            self.har = json.load(f)
        self.findings = []

    def scan(self):
        for entry in self.har['log']['entries']:
            self._scan_request(entry['request'])
            self._scan_response(entry['response'])
        return self.findings

    def _scan_request(self, request):
        url = request['url']

        # Scan URL
        self._scan_text(url, f"URL: {url[:50]}...")

        # Scan headers
        for header in request.get('headers', []):
            self._scan_text(
                header['value'],
                f"Request Header {header['name']}: {url[:30]}..."
            )

        # Scan POST data
        if 'postData' in request:
            text = request['postData'].get('text', '')
            self._scan_text(text, f"POST body: {url[:30]}...")

    def _scan_response(self, response):
        # Scan response headers
        for header in response.get('headers', []):
            self._scan_text(
                header['value'],
                f"Response Header {header['name']}"
            )

        # Scan response body
        content = response.get('content', {})
        text = content.get('text', '')
        if text:
            self._scan_text(text, "Response body")

    def _scan_text(self, text, location):
        for pattern_name, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                self.findings.append({
                    'type': pattern_name,
                    'match': match[:50] if isinstance(match, str) else str(match)[:50],
                    'location': location
                })

# Utilisation
scanner = HARScanner('capture.har')
findings = scanner.scan()

for f in findings:
    print(f"[{f['type']}] {f['match']} - {f['location']}")
```

### 2. Rapport de sécurité

```python
def generate_security_report(har_file):
    scanner = HARScanner(har_file)
    findings = scanner.scan()

    # Grouper par type
    by_type = {}
    for f in findings:
        if f['type'] not in by_type:
            by_type[f['type']] = []
        by_type[f['type']].append(f)

    # Générer rapport
    report = []
    report.append("# HAR Security Scan Report\\n")

    if not findings:
        report.append("No sensitive data found.\\n")
    else:
        report.append(f"Found {len(findings)} potential issues:\\n")

        for ftype, items in by_type.items():
            report.append(f"\\n## {ftype.upper()} ({len(items)} occurrences)\\n")
            for item in items[:5]:  # Limiter l'affichage
                report.append(f"- {item['location']}")
                report.append(f"  Match: `{item['match']}`\\n")

    return '\\n'.join(report)
```

### 3. Vérification des headers de sécurité

```python
def check_security_headers(har_file):
    with open(har_file, 'r') as f:
        har = json.load(f)

    REQUIRED_HEADERS = {
        'strict-transport-security': 'HSTS missing',
        'x-content-type-options': 'MIME sniffing possible',
        'x-frame-options': 'Clickjacking possible',
        'content-security-policy': 'XSS protection missing',
    }

    issues = []

    for entry in har['log']['entries']:
        url = entry['request']['url']
        headers = {h['name'].lower(): h['value']
                   for h in entry['response']['headers']}

        for header, message in REQUIRED_HEADERS.items():
            if header not in headers:
                issues.append({
                    'url': url,
                    'header': header,
                    'issue': message
                })

    return issues
```
""",
        "best_practices": """
## Bonnes Pratiques

### Anonymisation avant partage

```python
def anonymize_har(har_data):
    '''Supprime les données sensibles avant partage'''
    sensitive_headers = ['authorization', 'cookie', 'set-cookie']

    for entry in har_data['log']['entries']:
        # Anonymiser les headers
        for header in entry['request'].get('headers', []):
            if header['name'].lower() in sensitive_headers:
                header['value'] = '[REDACTED]'
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Faux positifs

```python
# Vérifier le contexte avant d'alerter
# "password" dans une URL de doc != mot de passe réel
```
""",
        "tools": """
## Outils

- **Chrome DevTools** : Export HAR
- **HAR Viewer** : Visualisation
- **mitmproxy** : Capture proxy
""",
        "references": """
## Références

- [HAR 1.2 Spec](http://www.softwareishard.com/blog/har-12-spec/)
"""
    },

    "Tor.Web.Capture": {
        "title": "Capture Web via TOR",
        "intro": """
## Introduction

Capturer des pages web de manière anonyme via **TOR** pour la recherche en sécurité et l'archivage.

### Cas d'usage

- Archivage de sites .onion
- Screenshots anonymes
- Collecte de preuves
- Recherche sur le dark web
""",
        "theory": """
## Théorie et Concepts

### Architecture

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Browser │────►│   TOR   │────►│  Site   │
│ Headless│     │ Network │     │ Target  │
└─────────┘     └─────────┘     └─────────┘
     │
     ▼
┌─────────┐
│ Capture │
│ Storage │
└─────────┘
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Configuration Selenium + TOR

```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

def create_tor_browser():
    options = Options()

    # Profil avec proxy TOR
    options.set_preference('network.proxy.type', 1)
    options.set_preference('network.proxy.socks', '127.0.0.1')
    options.set_preference('network.proxy.socks_port', 9050)
    options.set_preference('network.proxy.socks_remote_dns', True)

    # Sécurité
    options.set_preference('javascript.enabled', False)  # Optional
    options.set_preference('privacy.resistFingerprinting', True)

    # Headless
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)
    return driver

# Utilisation
driver = create_tor_browser()
driver.get('https://check.torproject.org')
print(driver.page_source)
driver.quit()
```

### 2. Capture de screenshots

```python
import os
from datetime import datetime

def capture_page(url, output_dir='captures'):
    os.makedirs(output_dir, exist_ok=True)

    driver = create_tor_browser()
    driver.set_window_size(1920, 1080)

    try:
        driver.get(url)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_url = url.replace('://', '_').replace('/', '_')[:50]

        # Screenshot
        screenshot_path = f"{output_dir}/{timestamp}_{safe_url}.png"
        driver.save_screenshot(screenshot_path)

        # HTML
        html_path = f"{output_dir}/{timestamp}_{safe_url}.html"
        with open(html_path, 'w') as f:
            f.write(driver.page_source)

        return {
            'url': url,
            'screenshot': screenshot_path,
            'html': html_path,
            'timestamp': timestamp
        }

    finally:
        driver.quit()
```

### 3. Crawler .onion

```python
from urllib.parse import urljoin, urlparse
import requests

class OnionCrawler:
    def __init__(self, max_depth=2):
        self.visited = set()
        self.max_depth = max_depth
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def crawl(self, start_url, depth=0):
        if depth > self.max_depth or start_url in self.visited:
            return []

        self.visited.add(start_url)
        results = []

        try:
            r = requests.get(start_url, proxies=self.proxies, timeout=30)

            results.append({
                'url': start_url,
                'status': r.status_code,
                'size': len(r.text)
            })

            # Extraire les liens
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text, 'html.parser')

            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(start_url, href)

                # Rester sur le même domaine
                if urlparse(full_url).netloc == urlparse(start_url).netloc:
                    results.extend(self.crawl(full_url, depth + 1))

        except Exception as e:
            results.append({
                'url': start_url,
                'error': str(e)
            })

        return results
```
""",
        "best_practices": """
## Bonnes Pratiques

### Sécurité OpSec

```python
# Ne pas charger JavaScript sur les sites inconnus
options.set_preference('javascript.enabled', False)

# User-Agent standard TOR Browser
options.set_preference('general.useragent.override',
    'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0')
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ DNS Leak

```python
# TOUJOURS utiliser socks5h (pas socks5)
proxies = {'http': 'socks5h://127.0.0.1:9050'}  # BON
```
""",
        "tools": """
## Outils

- **Tor Browser** : Navigation manuelle
- **Selenium** : Automation
- **requests** : Requêtes simples
""",
        "references": """
## Références

- [Tor Project](https://www.torproject.org/)
- [Selenium Docs](https://www.selenium.dev/documentation/)
"""
    },
}
