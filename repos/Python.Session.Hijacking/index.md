---
layout: default
title: "Python.Session.Hijacking"
description: "Démonstration de Session Hijacking avec Flask"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Session.Hijacking</span>
</div>

<div class="page-header">
  <h1>Python.Session.Hijacking</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Session.Hijacking" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Démonstration de Session Hijacking avec Flask

> **AVERTISSEMENT** : Ce projet est **strictement éducatif**. Le vol de session est un délit pénal puni par la loi.

## Introduction : Qu'est-ce que le Session Hijacking ?

Imaginez que vous vous connectez à votre banque en ligne. Le serveur vous donne un "badge d'accès" temporaire (le cookie de session) qui prouve que vous êtes bien authentifié. Maintenant, imaginez qu'un attaquant vole ce badge : il peut accéder à votre compte sans connaître votre mot de passe !

C'est exactement ce qu'est le **Session Hijacking** (détournement de session) : l'attaquant récupère le cookie de session d'un utilisateur légitime et l'utilise pour usurper son identité.

### Ce projet vous permettra de comprendre

Ce laboratoire Flask reproduit une attaque de session hijacking dans un environnement contrôlé. Vous allez :

- **Observer** comment les sessions web fonctionnent concrètement
- **Reproduire** une attaque de vol de session étape par étape
- **Identifier** les failles qui rendent cette attaque possible
- **Implémenter** les protections qui l'auraient empêchée


## Le Scénario : Alice et Mallory

Pour rendre les choses concrètes, suivons l'histoire de deux personnages :

- **Alice** : une utilisatrice légitime qui se connecte à une application web
- **Mallory** : une attaquante qui veut accéder au compte d'Alice sans connaître son mot de passe

Le diagramme ci-dessous illustre le déroulement de l'attaque. Observez comment Mallory n'a besoin que du cookie de session (étapes 4-5) pour usurper l'identité d'Alice.

<div class="mermaid">
flowchart TB
    subgraph LEGIT["👤 Alice (Utilisatrice légitime)"]
        U1["Alice"]
        B1["🌐 Son navigateur"]
    end

    subgraph SERVER["🖥️ Serveur Flask"]
        APP["Application web<br/>localhost:5000"]
        SESS["Gestionnaire de sessions"]
    end

    subgraph ATTACKER["🔴 Mallory (Attaquante)"]
        A1["Mallory"]
        B2["🌐 Son navigateur"]
    end

    U1 -->|"1. Se connecte avec alice/password123"| B1
    B1 -->|"2. POST /login"| APP
    APP -->|"3. Set-Cookie: session=.eJwl..."| B1
    B1 -.->|"4. Cookie visible quelque part<br/>(XSS, réseau non chiffré, etc.)"| A1
    A1 -->|"5. Copie le cookie"| B2
    B2 -->|"6. GET /secret avec le cookie volé"| APP
    APP -->|"7. 'Bienvenue Alice !'"| B2

    style U1 fill:#2ecc71,fill-opacity:0.15
    style A1 fill:#e74c3c,fill-opacity:0.15
    style APP fill:#3498db,fill-opacity:0.15
    style ATTACKER fill:#808080,fill-opacity:0.15
    style SERVER fill:#808080,fill-opacity:0.15
    style LEGIT fill:#808080,fill-opacity:0.15
</div>

**Le point crucial** : à l'étape 7, le serveur ne peut pas distinguer Mallory d'Alice. Pour lui, quiconque présente le bon cookie **est** Alice.


## Déroulement Technique de l'Attaque

Maintenant que vous comprenez le concept, voyons les détails techniques. Le diagramme de séquence suivant montre les échanges HTTP exacts entre les différents acteurs.

Nous avons coloré les trois phases distinctes :
- **Vert** : Session légitime d'Alice
- **Rouge** : Vol du cookie (la faille exploitée)
- **Jaune** : Utilisation frauduleuse par Mallory

<div class="mermaid">
sequenceDiagram
    autonumber
    participant Alice as 👤 Alice
    participant Server as 🖥️ Serveur Flask
    participant Mallory as 🔴 Mallory

    rect rgb(46, 204, 113, 0.2)
        Note over Alice,Server: Phase 1 : Connexion légitime d'Alice
        Alice->>Server: POST /login<br/>username=alice&password=password123
        Server->>Alice: HTTP 200 + Set-Cookie: session=.eJwl...
        Alice->>Server: GET / (cookie envoyé automatiquement)
        Server->>Alice: Page d'accueil avec "Session ID: .eJwl..."
    end

    rect rgb(231, 76, 60, 0.2)
        Note over Alice,Mallory: Phase 2 : Vol du cookie
        Note right of Alice: Mallory intercepte le cookie<br/>(XSS, sniffing WiFi, malware...)
        Alice-->>Mallory: Cookie volé: .eJwl...
    end

    rect rgb(241, 196, 15, 0.2)
        Note over Mallory,Server: Phase 3 : Usurpation d'identité
        Mallory->>Server: GET /hijack (page de démonstration)
        Server->>Mallory: Formulaire JavaScript
        Mallory->>Mallory: Injecte le cookie avec document.cookie
        Mallory->>Server: GET /secret (avec le cookie d'Alice)
        Server->>Mallory: "Secret spécial pour alice" 🎉
    end
</div>


## Le Code Vulnérable

Examinons le code Flask qui rend cette attaque possible. Dans cette démonstration, nous avons **volontairement** désactivé les protections pour illustrer les risques.

### L'application Flask

```python
from flask import Flask, request, render_template_string, session, redirect
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Clé secrète pour signer les sessions

# Base d'utilisateurs simplifiée
users = {"alice": "password123"}

@app.route('/', methods=['GET', 'POST'])
def login():
    # Si déjà connecté, afficher la page d'accueil
    if 'username' in session:
        # ⚠️ VULNÉRABILITÉ : On affiche le Session ID !
        # En production, ne JAMAIS exposer le cookie à l'utilisateur
        return f"""
            <h1>Bienvenue {session['username']}</h1>
            <p>Votre Session ID: {request.cookies.get('session')}</p>
            <a href="/secret">Accéder à vos secrets</a>
        """

    # Sinon, traiter le login
    if request.method == 'POST':
        if users.get(request.form['username']) == request.form['password']:
            session['username'] = request.form['username']
            return redirect('/')

    return '<form method="POST">...</form>'

@app.route('/secret')
def secret():
    if 'username' not in session:
        return "Accès refusé : vous devez être connecté", 401
    # Cette page ne vérifie QUE le cookie - pas de validation supplémentaire
    return f"🔒 Secret ultra-confidentiel pour {session['username']}"
```

### La page de hijacking (pour la démonstration)

Cette page permet à Mallory d'injecter le cookie volé dans son navigateur :

```html
<h1>🔴 Session Hijacking Demo</h1>
<p>Collez le cookie de session volé ci-dessous :</p>
<input type="text" id="session_id" placeholder="Collez .eJwl... ici" style="width: 400px;">
<button onclick="hijackSession()">Usurper la session</button>

<script>
function hijackSession() {
    const sessionId = document.getElementById('session_id').value;

    // Injection du cookie volé dans le navigateur de Mallory
    document.cookie = `session=${encodeURIComponent(sessionId)}; path=/`;

    // Redirection vers la page protégée
    // Le serveur croira que Mallory est Alice !
    window.location.href = '/secret';
}
</script>
```


## Les Vulnérabilités et Leurs Corrections

Maintenant que vous avez vu l'attaque, voyons comment la prévenir. Chaque vulnérabilité a une ou plusieurs corrections possibles.

<div class="mermaid">
flowchart LR
    subgraph VULN["❌ Ce qui rend l'attaque possible"]
        V1["Cookie accessible en JavaScript<br/><i>(pas de HttpOnly)</i>"]
        V2["Cookie envoyé sur HTTP<br/><i>(pas de Secure)</i>"]
        V3["Session qui ne change jamais<br/><i>(pas de rotation)</i>"]
        V4["Cookie envoyé partout<br/><i>(pas de SameSite)</i>"]
    end

    subgraph PROT["✅ Les protections à activer"]
        P1["HttpOnly=True<br/><i>Invisible pour JavaScript</i>"]
        P2["Secure=True<br/><i>HTTPS obligatoire</i>"]
        P3["Régénérer après login<br/><i>session.regenerate()</i>"]
        P4["SameSite=Strict<br/><i>Même origine uniquement</i>"]
    end

    V1 -->|"Correction"| P1
    V2 -->|"Correction"| P2
    V3 -->|"Correction"| P3
    V4 -->|"Correction"| P4

    style V1 fill:#e74c3c,fill-opacity:0.15
    style V2 fill:#e74c3c,fill-opacity:0.15
    style V3 fill:#e74c3c,fill-opacity:0.15
    style V4 fill:#e74c3c,fill-opacity:0.15
    style P1 fill:#2ecc71,fill-opacity:0.15
    style P2 fill:#2ecc71,fill-opacity:0.15
    style P3 fill:#2ecc71,fill-opacity:0.15
    style P4 fill:#2ecc71,fill-opacity:0.15
    style PROT fill:#808080,fill-opacity:0.15
    style VULN fill:#808080,fill-opacity:0.15
</div>

### Configuration sécurisée en Flask

Voici comment configurer Flask correctement en production :

```python
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,   # Invisible pour JavaScript
    SESSION_COOKIE_SECURE=True,     # HTTPS uniquement
    SESSION_COOKIE_SAMESITE='Strict' # Même origine
)
```


## Reproduire l'Attaque (Environnement de Test)

Vous voulez voir l'attaque en action ? Suivez ces étapes dans un environnement de test isolé.

### Étape 1 : Lancez le serveur

```bash
python app.py
# Serveur démarré sur http://localhost:5000
```

### Étape 2 : Alice se connecte (Navigateur 1)

1. Ouvrez `http://localhost:5000`
2. Connectez-vous avec `alice` / `password123`
3. **Copiez le Session ID affiché** (commence par `.eJwl...`)

### Étape 3 : Mallory vole la session (Navigateur 2 - fenêtre privée)

1. Ouvrez une **nouvelle fenêtre de navigation privée**
2. Allez sur `http://localhost:5000/hijack`
3. Collez le Session ID copié
4. Cliquez sur "Usurper la session"

### Résultat attendu

Mallory voit maintenant : **"Secret spécial pour alice"**

Elle a accédé au compte d'Alice sans jamais connaître son mot de passe !


## Comment Vérifier si un Cookie est Protégé ?

En tant que développeur ou auditeur de sécurité, vous devez savoir vérifier les flags de sécurité des cookies.

| Méthode | Comment faire |
|---------|---------------|
| **Chrome DevTools** | F12 → Application → Cookies → Voir colonnes HttpOnly, Secure, SameSite |
| **Firefox DevTools** | F12 → Stockage → Cookies → Mêmes colonnes |
| **Test JavaScript** | Tapez `document.cookie` dans la console. Si le cookie n'apparaît pas, HttpOnly fonctionne ! |


## Pour Aller Plus Loin

- 📚 [OWASP Session Management Cheat Sheet](https://cheatsheetséries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- 🔧 [Flask-Login](https://flask-login.readthedocs.io/) - Gestion sécurisée des sessions
- 🔒 [MDN - Cookies et sécurité](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#security)


## Exploits et Vulnérabilités Connues

Le session hijacking exploite souvent des vulnérabilités dans la gestion des sessions ou des failles XSS. Voici des CVE illustrant ces risques :

- **CVE-2022-24785 (Moment.js Path Traversal)** : Bien que principalement path traversal, cette vulnérabilité dans une bibliothèque JavaScript très répandue illustre comment une faille peut mener au vol de cookies via XSS en chaîne. Les bibliothèques tierces non mises à jour sont un vecteur courant.

- **CVE-2021-44228 (Log4Shell)** : Cette vulnérabilité critique a été utilisée pour voler des cookies de session via injection JNDI. Les payloads injectaient du code récupérant document.cookie et l'envoyant à des serveurs contrôlées par les attaquants.

- **CVE-2020-8945 (GPAC)** : Use-after-free permettant l'exécution de code et potentiellement le vol de sessions dans les applications utilisant cette bibliothèque multimédia. Illustre que les vulnérabilités mémoire peuvent mener au hijacking.

- **CVE-2019-11358 (jQuery Prototype Pollution)** : Vulnérabilité dans jQuery permettant la modification de prototypes JavaScript, potentiellement exploitable pour manipuler les cookies. A affecté des millions de sites web.

- **CVE-2023-23752 (Joomla Unauthorized Access)** : Faille permettant l'accès non authentifié à des informations sensibles incluant des tokens de session. Démontre l'importance de protéger les endpoints d'API qui exposent des données de session.


## Approfondissement Théorique

La gestion des sessions web repose sur le principe d'état dans un protocole sans état (HTTP). Chaque requête HTTP étant indépendante, le serveur doit avoir un moyen d'identifier les requêtes appartenant à la même session utilisateur. Le cookie de session, contenant un identifiant unique (session ID), est la solution standard. Ce session ID est soit un identifiant aléatoire pointant vers des données stockées côté serveur (session server-side), soit un token signé contenant les données elles-mêmes (JWT, session Flask signée).

Les vecteurs de vol de session sont multiples. Le XSS (Cross-Site Scripting) permet à un attaquant d'exécuter du JavaScript malveillant qui lit document.cookie et l'envoie à un serveur externe. Le sniffing réseau sur des connexions non chiffrées (HTTP sans TLS) permet de capturer les cookies en transit. Les attaques Man-in-the-Middle sur des réseaux WiFi publics exploitent ce vecteur. Le session fixation force la victime à utiliser un session ID connu de l'attaquant, qui peut ensuite hijacker la session une fois authentifiée.

Les défenses modernes s'appuient sur plusieurs couches. Le flag HttpOnly empêche l'accès JavaScript aux cookies, bloquant le XSS classique. Le flag Secure force l'envoi uniquement sur HTTPS, empêchant le sniffing. L'attribut SameSite (Strict ou Lax) limite l'envoi des cookies aux requêtes same-origin, contrant les attaques CSRF et certains scénarios de vol. La rotation de session ID après authentification (session régénération) invalide les session ID obtenus avant login, contrant le session fixation. L'association de l'IP et/ou du User-Agent à la session détecte les tentatives d'utilisation depuis un contexte différent, bien que ces techniques aient des limites (utilisateurs mobiles, proxies).


---

