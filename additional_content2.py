#!/usr/bin/env python3
"""
Contenu additionnel - Partie 2
"""

ADDITIONAL_CONTENT_2 = {
    "Python.Arping": {
        "title": "ARP Ping et Découverte Réseau",
        "intro": """
## Introduction

**ARP Ping** utilise le protocole ARP pour découvrir les hôtes sur un réseau local, contournant les firewalls qui bloquent ICMP.

### Avantages sur ICMP

- Fonctionne même si ICMP est bloqué
- Découvre les machines "silencieuses"
- Collecte les adresses MAC
- Plus rapide sur les réseaux locaux
""",
        "theory": """
## Théorie et Concepts

### Fonctionnement ARP

```
┌──────────────┐                    ┌──────────────┐
│   Scanner    │                    │    Cible     │
│ 192.168.1.10 │                    │ 192.168.1.20 │
└──────┬───────┘                    └──────┬───────┘
       │                                   │
       │  ARP Request (broadcast)          │
       │  "Who has 192.168.1.20?"          │
       │──────────────────────────────────►│
       │                                   │
       │  ARP Reply (unicast)              │
       │  "192.168.1.20 is at AA:BB:CC..." │
       │◄──────────────────────────────────│
```

### Table ARP

```bash
# Afficher la table ARP
arp -a
ip neigh show

# Format
IP              MAC                 Interface
192.168.1.1     aa:bb:cc:dd:ee:ff   eth0
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. ARP Ping avec Scapy

```python
from scapy.all import *

def arp_ping(ip):
    # Créer la requête ARP
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    # Envoyer et recevoir
    answered, _ = srp(packet, timeout=2, verbose=False)

    if answered:
        for sent, received in answered:
            return {
                'ip': received.psrc,
                'mac': received.hwsrc
            }
    return None

# Test
result = arp_ping("192.168.1.1")
if result:
    print(f"Host up: {result['ip']} ({result['mac']})")
```

### 2. Scanner de réseau complet

```python
from scapy.all import *
from ipaddress import ip_network
from concurrent.futures import ThreadPoolExecutor
import time

def arp_scan(network, timeout=2):
    # Créer les paquets pour tout le réseau
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(network))

    answered, _ = srp(arp_request, timeout=timeout, verbose=False)

    hosts = []
    for sent, received in answered:
        hosts.append({
            'ip': received.psrc,
            'mac': received.hwsrc,
            'vendor': get_vendor(received.hwsrc)
        })

    return sorted(hosts, key=lambda x: ip_address(x['ip']))

def get_vendor(mac):
    # Les 3 premiers octets = OUI
    oui = mac[:8].upper().replace(':', '')
    # Lookup dans une base OUI (simplifié)
    vendors = {
        'AABBCC': 'Cisco',
        '001122': 'Apple',
        # ... base complète
    }
    return vendors.get(oui, 'Unknown')

# Scanner le réseau
hosts = arp_scan("192.168.1.0/24")
for h in hosts:
    print(f"{h['ip']:15} {h['mac']}  {h['vendor']}")
```

### 3. Monitoring continu

```python
from scapy.all import *
import time
from datetime import datetime

known_hosts = {}

def arp_monitor(interface="eth0"):
    def process_arp(pkt):
        if ARP in pkt and pkt[ARP].op == 2:  # ARP Reply
            ip = pkt[ARP].psrc
            mac = pkt[ARP].hwsrc

            if ip not in known_hosts:
                known_hosts[ip] = mac
                print(f"[NEW] {datetime.now()} - {ip} ({mac})")
            elif known_hosts[ip] != mac:
                print(f"[ALERT] MAC changed for {ip}")
                print(f"  Old: {known_hosts[ip]}")
                print(f"  New: {mac}")
                known_hosts[ip] = mac

    print(f"Monitoring ARP sur {interface}...")
    sniff(iface=interface, filter="arp", prn=process_arp, store=False)

arp_monitor()
```

### 4. Détection ARP Spoofing

```python
def detect_arp_spoof(interface="eth0"):
    gateway_ip = "192.168.1.1"  # À adapter
    gateway_mac = None

    def check_arp(pkt):
        nonlocal gateway_mac

        if ARP in pkt and pkt[ARP].op == 2:
            if pkt[ARP].psrc == gateway_ip:
                current_mac = pkt[ARP].hwsrc

                if gateway_mac is None:
                    gateway_mac = current_mac
                    print(f"Gateway MAC: {gateway_mac}")
                elif current_mac != gateway_mac:
                    print(f"[SPOOFING] Gateway MAC changed!")
                    print(f"  Expected: {gateway_mac}")
                    print(f"  Received: {current_mac}")

    sniff(iface=interface, filter="arp", prn=check_arp, store=False)
```
""",
        "best_practices": """
## Bonnes Pratiques

### Optimisation des scans

```python
# Scanner en parallèle pour les grands réseaux
def fast_arp_scan(network, workers=100):
    from concurrent.futures import ThreadPoolExecutor

    ips = [str(ip) for ip in ip_network(network).hosts()]

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(arp_ping, ips))

    return [r for r in results if r is not None]
```

### Gestion des permissions

```python
import os, sys

if os.geteuid() != 0:
    sys.exit("Ce script nécessite root (pour les raw sockets)")
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Scan trop agressif

```python
# MAUVAIS : flood le réseau
for ip in ips:
    srp(arp_request, timeout=0.01)

# BON : avec rate limiting
for ip in ips:
    srp(arp_request, timeout=1, inter=0.1)
```
""",
        "tools": """
## Outils alternatifs

```bash
# arping (Linux)
arping -c 1 192.168.1.1

# nmap ARP scan
nmap -sn -PR 192.168.1.0/24

# arp-scan
arp-scan --localnet
```
""",
        "references": """
## Références

- [RFC 826 - ARP](https://tools.ietf.org/html/rfc826)
- [Scapy ARP](https://scapy.readthedocs.io/en/latest/usage.html#arp-ping)
"""
    },

    "Python.Dome.SubDomains": {
        "title": "Enumération de Sous-domaines",
        "intro": """
## Introduction

L'**énumération de sous-domaines** est une technique de reconnaissance essentielle pour identifier la surface d'attaque d'une cible.

### Méthodes

- **Brute force** : Tester des mots communs
- **Passive** : Certificate Transparency, DNS, archives
- **Active** : DNS zone transfer, virtual hosts
""",
        "theory": """
## Théorie et Concepts

### Sources d'information

| Source | Type | Description |
|--------|------|-------------|
| DNS Brute force | Actif | Résolution de noms |
| Certificate Transparency | Passif | Logs de certificats SSL |
| VirusTotal | Passif | Base de données DNS |
| Shodan | Passif | Scans internet |
| Archive.org | Passif | Pages archivées |
| Google dorks | Passif | Indexation moteurs |

### Enregistrements DNS utiles

```
A     → IPv4
AAAA  → IPv6
CNAME → Alias
MX    → Serveurs mail
NS    → Serveurs DNS
TXT   → Informations diverses
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Brute force DNS

```python
import dns.resolver
from concurrent.futures import ThreadPoolExecutor

def check_subdomain(domain, subdomain):
    target = f"{subdomain}.{domain}"
    try:
        answers = dns.resolver.resolve(target, 'A')
        ips = [str(rdata) for rdata in answers]
        return {'subdomain': target, 'ips': ips}
    except:
        return None

def bruteforce_subdomains(domain, wordlist, workers=50):
    results = []

    with open(wordlist, 'r') as f:
        words = [w.strip() for w in f if w.strip()]

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(check_subdomain, domain, word)
            for word in words
        ]

        for future in futures:
            result = future.result()
            if result:
                results.append(result)
                print(f"[+] {result['subdomain']} → {result['ips']}")

    return results

# Utilisation
subdomains = bruteforce_subdomains("example.com", "subdomains.txt")
```

### 2. Certificate Transparency

```python
import requests

def get_ct_subdomains(domain):
    url = f"https://crt.sh/?q=%.{domain}&output=json"

    try:
        r = requests.get(url, timeout=30)
        data = r.json()

        subdomains = set()
        for entry in data:
            name = entry.get('name_value', '')
            for sub in name.split('\\n'):
                sub = sub.strip().lower()
                if sub.endswith(domain) and '*' not in sub:
                    subdomains.add(sub)

        return sorted(subdomains)

    except Exception as e:
        print(f"Erreur CT: {e}")
        return []

# Utilisation
subs = get_ct_subdomains("example.com")
for s in subs:
    print(s)
```

### 3. Combinaison de sources

```python
import requests

class SubdomainEnumerator:
    def __init__(self, domain):
        self.domain = domain
        self.subdomains = set()

    def crtsh(self):
        url = f"https://crt.sh/?q=%.{self.domain}&output=json"
        try:
            r = requests.get(url, timeout=30)
            for entry in r.json():
                for name in entry.get('name_value', '').split('\\n'):
                    name = name.strip().lower()
                    if name.endswith(self.domain):
                        self.subdomains.add(name.replace('*.', ''))
        except:
            pass

    def threatcrowd(self):
        url = f"https://threatcrowd.org/searchApi/v2/domain/report/?domain={self.domain}"
        try:
            r = requests.get(url, timeout=30)
            for sub in r.json().get('subdomains', []):
                self.subdomains.add(sub.lower())
        except:
            pass

    def hackertarget(self):
        url = f"https://api.hackertarget.com/hostsearch/?q={self.domain}"
        try:
            r = requests.get(url, timeout=30)
            for line in r.text.splitlines():
                if ',' in line:
                    subdomain = line.split(',')[0]
                    self.subdomains.add(subdomain.lower())
        except:
            pass

    def enumerate_all(self):
        print(f"[*] Enumération de {self.domain}")

        print("[*] Certificate Transparency...")
        self.crtsh()

        print("[*] ThreatCrowd...")
        self.threatcrowd()

        print("[*] HackerTarget...")
        self.hackertarget()

        print(f"[+] {len(self.subdomains)} sous-domaines trouvés")
        return sorted(self.subdomains)

# Utilisation
enum = SubdomainEnumerator("example.com")
results = enum.enumerate_all()
```

### 4. Vérification des résultats

```python
import dns.resolver
import socket

def verify_subdomains(subdomains):
    verified = []

    for sub in subdomains:
        try:
            answers = dns.resolver.resolve(sub, 'A')
            ips = [str(r) for r in answers]

            # Vérifier si le port 80/443 répond
            for ip in ips:
                try:
                    socket.create_connection((ip, 443), timeout=2)
                    https = True
                except:
                    https = False

            verified.append({
                'subdomain': sub,
                'ips': ips,
                'https': https
            })
            print(f"[LIVE] {sub} → {ips}")

        except dns.resolver.NXDOMAIN:
            pass
        except Exception as e:
            pass

    return verified
```
""",
        "best_practices": """
## Bonnes Pratiques

### Wordlists efficaces

```bash
# SecLists
/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
/usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt

# Génération custom
# Combinaisons communes
dev, staging, test, prod, api, admin, www, mail, ftp, vpn
```

### Rate limiting

```python
import time

def polite_enumerate(domain, words):
    for word in words:
        check_subdomain(domain, word)
        time.sleep(0.1)  # 10 req/sec max
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Wildcard DNS

```python
# Vérifier si wildcard existe
def check_wildcard(domain):
    random_sub = f"thissubshouldnotexist12345.{domain}"
    try:
        dns.resolver.resolve(random_sub, 'A')
        return True  # Wildcard actif
    except:
        return False
```
""",
        "tools": """
## Outils

```bash
# Subfinder
subfinder -d example.com

# Amass
amass enum -d example.com

# Sublist3r
sublist3r -d example.com
```
""",
        "references": """
## Références

- [OWASP Subdomain Enumeration](https://owasp.org/www-community/attacks/Subdomain_Enumeration)
- [Certificate Transparency](https://certificate.transparency.dev/)
"""
    },

    "Python.HAR.ZAP": {
        "title": "OWASP ZAP et Analyse HAR",
        "intro": """
## Introduction

**OWASP ZAP** (Zed Attack Proxy) est un scanner de sécurité web open source. Les fichiers **HAR** (HTTP Archive) permettent d'exporter et analyser le trafic HTTP.

### Cas d'usage

- Scan automatisé de vulnérabilités
- Analyse de trafic HTTP/HTTPS
- Tests de pénétration web
- CI/CD security testing
""",
        "theory": """
## Théorie et Concepts

### Architecture ZAP

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Browser   │────►│    ZAP      │────►│   Target    │
│             │◄────│   Proxy     │◄────│   Website   │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                    ┌─────┴─────┐
                    │  Scanners │
                    │  Spider   │
                    │  Fuzzer   │
                    └───────────┘
```

### Format HAR

```json
{
  "log": {
    "version": "1.2",
    "entries": [
      {
        "request": {
          "method": "GET",
          "url": "https://example.com/api",
          "headers": [...]
        },
        "response": {
          "status": 200,
          "content": {...}
        },
        "timings": {...}
      }
    ]
  }
}
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. API ZAP en Python

```python
from zapv2 import ZAPv2

# Connexion à ZAP (doit être lancé)
zap = ZAPv2(apikey='your-api-key',
            proxies={'http': 'http://127.0.0.1:8080'})

def scan_target(target_url):
    print(f"[*] Scanning {target_url}")

    # Spider (exploration)
    print("[*] Spidering...")
    scan_id = zap.spider.scan(target_url)
    while int(zap.spider.status(scan_id)) < 100:
        print(f"Spider progress: {zap.spider.status(scan_id)}%")
        time.sleep(5)

    # Active scan
    print("[*] Active scanning...")
    scan_id = zap.ascan.scan(target_url)
    while int(zap.ascan.status(scan_id)) < 100:
        print(f"Scan progress: {zap.ascan.status(scan_id)}%")
        time.sleep(10)

    # Récupérer les alertes
    alerts = zap.core.alerts(baseurl=target_url)
    return alerts

alerts = scan_target("https://example.com")
for alert in alerts:
    print(f"[{alert['risk']}] {alert['alert']}")
    print(f"  URL: {alert['url']}")
```

### 2. Analyse de fichier HAR

```python
import json
from collections import defaultdict

def analyze_har(har_file):
    with open(har_file, 'r') as f:
        har = json.load(f)

    entries = har['log']['entries']
    stats = {
        'total_requests': len(entries),
        'methods': defaultdict(int),
        'status_codes': defaultdict(int),
        'content_types': defaultdict(int),
        'domains': defaultdict(int),
        'slow_requests': [],
        'errors': []
    }

    for entry in entries:
        req = entry['request']
        resp = entry['response']

        # Stats
        stats['methods'][req['method']] += 1
        stats['status_codes'][resp['status']] += 1

        # Domaine
        from urllib.parse import urlparse
        domain = urlparse(req['url']).netloc
        stats['domains'][domain] += 1

        # Content-Type
        for header in resp.get('headers', []):
            if header['name'].lower() == 'content-type':
                ct = header['value'].split(';')[0]
                stats['content_types'][ct] += 1

        # Requêtes lentes (> 2s)
        time_ms = entry.get('time', 0)
        if time_ms > 2000:
            stats['slow_requests'].append({
                'url': req['url'],
                'time_ms': time_ms
            })

        # Erreurs
        if resp['status'] >= 400:
            stats['errors'].append({
                'url': req['url'],
                'status': resp['status']
            })

    return stats

# Utilisation
stats = analyze_har("traffic.har")
print(f"Total: {stats['total_requests']} requêtes")
print(f"Erreurs: {len(stats['errors'])}")
```

### 3. Détection de vulnérabilités

```python
def detect_security_issues(har_file):
    with open(har_file, 'r') as f:
        har = json.load(f)

    issues = []

    for entry in har['log']['entries']:
        url = entry['request']['url']
        headers = {h['name'].lower(): h['value']
                   for h in entry['response'].get('headers', [])}

        # Vérifier headers de sécurité manquants
        security_headers = [
            'strict-transport-security',
            'x-content-type-options',
            'x-frame-options',
            'content-security-policy'
        ]

        for header in security_headers:
            if header not in headers:
                issues.append({
                    'type': 'missing_header',
                    'header': header,
                    'url': url
                })

        # Cookies sans flags
        for header in entry['response'].get('headers', []):
            if header['name'].lower() == 'set-cookie':
                cookie = header['value'].lower()
                if 'secure' not in cookie:
                    issues.append({
                        'type': 'insecure_cookie',
                        'detail': 'Missing Secure flag',
                        'url': url
                    })
                if 'httponly' not in cookie:
                    issues.append({
                        'type': 'insecure_cookie',
                        'detail': 'Missing HttpOnly flag',
                        'url': url
                    })

    return issues
```

### 4. Export depuis ZAP

```python
def export_zap_to_har(zap, output_file):
    # Récupérer tout l'historique
    messages = zap.core.messages()

    har = {
        "log": {
            "version": "1.2",
            "creator": {"name": "ZAP", "version": "2.x"},
            "entries": []
        }
    }

    for msg in messages:
        entry = {
            "request": {
                "method": msg['requestHeader'].split()[0],
                "url": msg['requestHeader'].split()[1],
                "httpVersion": "HTTP/1.1",
                "headers": parse_headers(msg['requestHeader']),
                "postData": msg.get('requestBody', '')
            },
            "response": {
                "status": int(msg['responseHeader'].split()[1]),
                "headers": parse_headers(msg['responseHeader']),
                "content": {
                    "text": msg.get('responseBody', '')
                }
            }
        }
        har['log']['entries'].append(entry)

    with open(output_file, 'w') as f:
        json.dump(har, f, indent=2)
```
""",
        "best_practices": """
## Bonnes Pratiques

### Configuration ZAP

```python
# Désactiver les scanners bruyants
zap.ascan.disable_scanners([40012, 40014, 40016])

# Mode "safe" pour ne pas modifier les données
zap.ascan.set_option_attack_mode('Safe')
```

### CI/CD Integration

```yaml
# .gitlab-ci.yml
security_scan:
  image: owasp/zap2docker-stable
  script:
    - zap-baseline.py -t $TARGET_URL -r report.html
  artifacts:
    paths:
      - report.html
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Scanner sans contexte

```python
# Configurer l'authentification
zap.authentication.set_authentication_method(
    contextid=1,
    authmethodname='formBasedAuthentication',
    authmethodconfigparams='loginUrl=...'
)
```
""",
        "tools": """
## Outils

- **ZAP GUI** : Interface graphique complète
- **zap-cli** : CLI pour automation
- **zaproxy** : Package Python
""",
        "references": """
## Références

- [ZAP Documentation](https://www.zaproxy.org/docs/)
- [HAR 1.2 Spec](http://www.softwareishard.com/blog/har-12-spec/)
"""
    },

    "Python.Ransomware": {
        "title": "Ransomware - Analyse et Compréhension",
        "intro": """
## Introduction

**AVERTISSEMENT** : Ce contenu est strictement éducatif pour comprendre comment fonctionnent les ransomwares et mieux s'en protéger. L'utilisation malveillante est illégale.

### Objectifs éducatifs

- Comprendre les mécanismes de chiffrement
- Identifier les IOCs (Indicators of Compromise)
- Mettre en place des défenses
- Analyser des samples en sandbox
""",
        "theory": """
## Théorie et Concepts

### Fonctionnement typique

```
1. INFECTION
   │
   ├──► Phishing (email)
   ├──► Exploit (vulnérabilité)
   └──► RDP brute force

2. PERSISTENCE
   │
   ├──► Clés registre
   ├──► Tâches planifiées
   └──► WMI subscriptions

3. CHIFFREMENT
   │
   ├──► Génération clé AES (symétrique)
   ├──► Chiffrement fichiers
   └──► Chiffrement clé AES avec RSA public

4. EXTORSION
   │
   └──► Demande de rançon (Bitcoin)
```

### Types de chiffrement

| Type | Avantage | Utilisé par |
|------|----------|-------------|
| AES-256 | Rapide | La plupart |
| RSA | Asymétrique | Protection clé |
| ChaCha20 | Très rapide | Moderne |
| Hybrid | Combinaison | Standard actuel |
""",
        "tutorial": """
## Analyse Éducative

### 1. Simulation de chiffrement (LAB ONLY)

```python
# ATTENTION : Code éducatif uniquement
# NE JAMAIS exécuter hors environnement isolé

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def educational_encrypt(data, key):
    '''Montre comment fonctionne AES - NE PAS UTILISER'''
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Padding
    padding_length = 16 - (len(data) % 16)
    padded_data = data + bytes([padding_length] * padding_length)

    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted

# Ceci montre le principe - JAMAIS en production
```

### 2. Détection d'activité ransomware

```python
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RansomwareDetector(FileSystemEventHandler):
    def __init__(self):
        self.modify_count = 0
        self.rename_count = 0
        self.start_time = time.time()
        self.suspicious_extensions = {
            '.encrypted', '.locked', '.crypto',
            '.crypt', '.enc', '.pays'
        }

    def on_modified(self, event):
        if not event.is_directory:
            self.modify_count += 1
            self.check_threshold()

    def on_moved(self, event):
        if not event.is_directory:
            # Extension suspecte ?
            _, ext = os.path.splitext(event.dest_path)
            if ext.lower() in self.suspicious_extensions:
                print(f"[ALERT] Suspicious rename: {event.dest_path}")

            self.rename_count += 1
            self.check_threshold()

    def check_threshold(self):
        elapsed = time.time() - self.start_time

        # Plus de 100 fichiers modifiés en 1 minute ?
        if elapsed < 60 and self.modify_count > 100:
            print("[CRITICAL] Possible ransomware activity!")
            print(f"  {self.modify_count} files modified in {elapsed:.0f}s")
            # Ici : déclencher alerte, isoler machine, etc.

# Utilisation
observer = Observer()
observer.schedule(RansomwareDetector(), "/path/to/monitor", recursive=True)
observer.start()
```

### 3. Honeypot fichiers

```python
import os
import time
import hashlib

def create_honeypot_files(directory, count=10):
    '''Crée des fichiers leurres pour détecter les ransomwares'''
    honeypots = []

    names = [
        'budget_2024.xlsx',
        'passwords.docx',
        'bank_accounts.pdf',
        'confidential.txt'
    ]

    for i, name in enumerate(names[:count]):
        path = os.path.join(directory, name)
        content = f"Honeypot file {i} - {time.time()}"

        with open(path, 'w') as f:
            f.write(content)

        honeypots.append({
            'path': path,
            'hash': hashlib.sha256(content.encode()).hexdigest(),
            'mtime': os.path.getmtime(path)
        })

    return honeypots

def check_honeypots(honeypots):
    '''Vérifie si les fichiers leurres ont été modifiés'''
    for hp in honeypots:
        if not os.path.exists(hp['path']):
            print(f"[ALERT] Honeypot deleted: {hp['path']}")
            return True

        current_mtime = os.path.getmtime(hp['path'])
        if current_mtime != hp['mtime']:
            print(f"[ALERT] Honeypot modified: {hp['path']}")
            return True

        with open(hp['path'], 'r') as f:
            content = f.read()
            current_hash = hashlib.sha256(content.encode()).hexdigest()
            if current_hash != hp['hash']:
                print(f"[ALERT] Honeypot content changed: {hp['path']}")
                return True

    return False
```

### 4. Analyse de samples

```python
import yara
import pefile
import hashlib

def analyze_sample(filepath):
    '''Analyse basique d'un exécutable suspect'''
    results = {
        'hashes': {},
        'pe_info': {},
        'suspicious': []
    }

    # Hashes
    with open(filepath, 'rb') as f:
        data = f.read()
        results['hashes'] = {
            'md5': hashlib.md5(data).hexdigest(),
            'sha256': hashlib.sha256(data).hexdigest()
        }

    # PE analysis
    try:
        pe = pefile.PE(filepath)
        results['pe_info'] = {
            'sections': [s.Name.decode().strip('\\x00') for s in pe.sections],
            'imports': [e.dll.decode() for e in pe.DIRECTORY_ENTRY_IMPORT]
        }

        # Imports suspects
        crypto_dlls = ['advapi32.dll', 'crypt32.dll']
        for dll in results['pe_info']['imports']:
            if dll.lower() in crypto_dlls:
                results['suspicious'].append(f"Crypto DLL: {dll}")

    except Exception as e:
        results['pe_info'] = {'error': str(e)}

    return results
```
""",
        "best_practices": """
## Protection et Défense

### Sauvegardes

```bash
# Règle 3-2-1
# 3 copies des données
# 2 supports différents
# 1 copie hors-site/offline
```

### Segmentation

```
[Internet] ──► [DMZ] ──► [Firewall] ──► [LAN]
                              │
                              ▼
                    [Backup Network]
                    (isolé, offline)
```

### Monitoring

```python
# Surveillez ces indicateurs
indicators = [
    'Fichiers renommés en masse',
    'Extensions inhabituelles',
    'Accès réseau anormal',
    'Processus inconnus avec crypto',
    'Shadow copies supprimées'
]
```
""",
        "pitfalls": """
## À Éviter

### ❌ Payer la rançon

- Ne garantit pas le déchiffrement
- Finance les criminels
- Vous marque comme cible
""",
        "tools": """
## Outils d'analyse

- **Yara** : Règles de détection
- **PEStudio** : Analyse PE
- **Any.Run** : Sandbox en ligne
- **VirusTotal** : Multi-AV scan
""",
        "references": """
## Références

- [No More Ransom](https://www.nomoreransom.org/)
- [ID Ransomware](https://id-ransomware.malwarehunterteam.com/)
- [CISA Ransomware Guide](https://www.cisa.gov/stopransomware)
"""
    },

    "Python.Tor.Proxy": {
        "title": "TOR - Proxy et Anonymat Réseau",
        "intro": """
## Introduction

**TOR (The Onion Router)** est un réseau d'anonymisation qui achemine le trafic à travers plusieurs relais chiffrés.

### Cas d'usage légitimes

- Protection de la vie privée
- Contournement de la censure
- Recherche en sécurité
- Whistleblowing
""",
        "theory": """
## Théorie et Concepts

### Fonctionnement

```
┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
│ Client │───►│ Guard  │───►│ Middle │───►│  Exit  │───►│ Target │
└────────┘    └────────┘    └────────┘    └────────┘    └────────┘
     │             │             │             │
   Chiffré      Chiffré      Chiffré       Clair
   3 couches    2 couches    1 couche
```

### Couches de chiffrement

```
Client:
  Paquet = Encrypt(Exit_key,
              Encrypt(Middle_key,
                Encrypt(Guard_key, Data)))

Chaque nœud enlève une couche (comme un oignon)
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Configuration Python avec TOR

```python
import requests

# TOR doit être lancé (service tor ou Tor Browser)
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def get_via_tor(url):
    try:
        r = requests.get(url, proxies=proxies, timeout=30)
        return r.text
    except Exception as e:
        print(f"Erreur: {e}")
        return None

# Vérifier l'IP TOR
def check_tor():
    ip = get_via_tor('https://api.ipify.org')
    print(f"IP via TOR: {ip}")

    # Vérifier si c'est bien une IP TOR
    tor_check = get_via_tor('https://check.torproject.org/api/ip')
    print(tor_check)

check_tor()
```

### 2. Changer d'identité (nouveau circuit)

```python
from stem import Signal
from stem.control import Controller

def renew_tor_identity():
    '''Demande un nouveau circuit TOR'''
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='your_password')
        controller.signal(Signal.NEWNYM)
        print("Nouveau circuit TOR demandé")

# Configurer le mot de passe dans torrc:
# HashedControlPassword (généré avec: tor --hash-password "your_password")
# ControlPort 9051
```

### 3. Scraping anonyme

```python
import requests
from stem import Signal
from stem.control import Controller
import time

class TorSession:
    def __init__(self):
        self.session = requests.Session()
        self.session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def renew_identity(self):
        with Controller.from_port(port=9051) as c:
            c.authenticate(password='password')
            c.signal(Signal.NEWNYM)
        time.sleep(5)  # Attendre le nouveau circuit

    def get(self, url, new_identity=False):
        if new_identity:
            self.renew_identity()
        return self.session.get(url, timeout=30)

# Utilisation
tor = TorSession()

urls = ['https://example.com/page1', 'https://example.com/page2']
for url in urls:
    response = tor.get(url, new_identity=True)
    print(f"Fetched {url}")
    time.sleep(2)
```

### 4. Accès aux services .onion

```python
def access_onion(onion_url):
    '''Accède à un service .onion'''
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    try:
        r = requests.get(onion_url, proxies=proxies, timeout=60)
        return r.text
    except Exception as e:
        print(f"Erreur: {e}")
        return None

# Exemple avec DuckDuckGo onion
# content = access_onion('https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/')
```

### 5. Créer un service .onion (Hidden Service)

```python
# Configuration dans torrc:
'''
HiddenServiceDir /var/lib/tor/my_service/
HiddenServicePort 80 127.0.0.1:8080
'''

# Ensuite lancer un serveur web local
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Service caché fonctionnel!"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)

# L'adresse .onion sera dans:
# /var/lib/tor/my_service/hostname
```
""",
        "best_practices": """
## Bonnes Pratiques

### Éviter les fuites

```python
# TOUJOURS utiliser socks5h (pas socks5)
# Le 'h' signifie que la résolution DNS passe aussi par TOR

# MAUVAIS - DNS leak
proxies = {'http': 'socks5://127.0.0.1:9050'}

# BON - DNS via TOR
proxies = {'http': 'socks5h://127.0.0.1:9050'}
```

### Headers

```python
# Minimiser les informations identifiantes
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept-Language': 'en-US,en;q=0.5',
}
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Mélanger identités

```python
# MAUVAIS : réutiliser la même session
session.get('https://site-anonyme.com')
session.get('https://mon-vrai-site.com')  # Corrélation possible!

# BON : nouvelle identité entre les contextes
tor.renew_identity()
```
""",
        "tools": """
## Outils

- **Tor Browser** : Navigateur configuré
- **stem** : Librairie Python pour contrôler TOR
- **torsocks** : Wrapper pour applications
""",
        "references": """
## Références

- [Tor Project](https://www.torproject.org/)
- [Stem Documentation](https://stem.torproject.org/)
"""
    },
}
