---
layout: default
title: "Python.CSRF.Demo"
description: "Démonstration de CSRF et Analyse de Cookies HttpOnly"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.CSRF.Demo</span>
</div>

<div class="page-header">
  <h1>Python.CSRF.Demo</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.CSRF.Demo" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Démonstration de CSRF et Analyse de Cookies HttpOnly

> **AVERTISSEMENT** : Ce projet est **strictement éducatif**. Les attaques CSRF sont illégales sans autorisation.

## Introduction : Qu'est-ce qu'une attaque CSRF ?

Imaginez que vous êtes connecté à votre banque en ligne. Pendant que vous naviguez, vous visitez innocemment un site piégé. Sans rien faire, un virement est effectué depuis votre compte vers celui de l'attaquant. Comment est-ce possible ?

C'est le principe du **CSRF** (Cross-Site Request Forgery, ou "Falsification de requête inter-sites"). L'attaquant ne vole pas vos identifiants : il exploite le fait que votre navigateur envoie **automatiquement** vos cookies de session à chaque requête vers la banque. Si l'attaquant vous fait visiter une page qui contient un formulaire caché pointant vers votre banque, le navigateur exécuterà la requête **avec vos droits**.

### Ce que ce projet vous permet de comprendre

Ce laboratoire combine deux aspects complémentaires de la sécurité web :

1. **L'analyse des cookies** : Comment vérifier si un cookie est correctement protégé (flags HttpOnly, Secure, SameSite) via les DevTools du navigateur ou l'analyse de fichiers HAR
2. **La démonstration d'attaque CSRF** : Comment fonctionne concrètement cette attaque et comment s'en protéger

À la fin de ce tutoriel, vous saurez identifier les applications vulnérables et mettre en place les protections adéquates.


## Partie 1 : Vérifier la Protection des Cookies

Avant de pouvoir exploiter une vulnérabilité, un attaquant doit d'abord vérifier si le cookie de session est correctement protégé. Voici les méthodes utilisées.

### Inspection via les DevTools du navigateur

Chaque navigateur moderne dispose d'outils de développement permettant d'inspecter les cookies. Le diagramme ci-dessous montre les deux méthodes principales : l'interface graphique (Application > Cookies) et le test JavaScript via la console.

<div class="mermaid">
flowchart TB
    subgraph Browser["🌐 Navigateur"]
        DT["DevTools (F12)"]

        subgraph Chrome["Chrome"]
            C1["Application"]
            C2["Cookies"]
            C3["Colonne HttpOnly ✓"]
        end

        subgraph Firefox["Firefox"]
            F1["Stockage"]
            F2["Cookies"]
            F3["Colonne HttpOnly ✓"]
        end
    end

    subgraph Test["🧪 Test JavaScript"]
        JS["document.cookie"]
        RES1["'' (vide) → HttpOnly actif"]
        RES2["'session=abc' → Pas HttpOnly"]
    end

    DT --> Chrome & Firefox
    JS --> RES1 & RES2

    style C3 fill:#2ecc71,fill-opacity:0.15
    style F3 fill:#2ecc71,fill-opacity:0.15
    style RES1 fill:#2ecc71,fill-opacity:0.15
    style RES2 fill:#e74c3c,fill-opacity:0.15
    style Test fill:#808080,fill-opacity:0.15
    style Firefox fill:#808080,fill-opacity:0.15
    style Chrome fill:#808080,fill-opacity:0.15
    style Browser fill:#808080,fill-opacity:0.15
</div>

**Le test JavaScript est particulièrement révélateur** : si `document.cookie` dans la console renvoie le cookie de session, cela signifie qu'il n'est pas protégé par HttpOnly et qu'un script malveillant (XSS) pourrait le voler.


## Partie 2 : Analyse Automatisée des Fichiers HAR

Pour les audits de sécurité à plus grande échelle, il est fastidieux de vérifier manuellement chaque cookie. Ce projet propose un script Python qui analyse les fichiers HAR (HTTP Archive), un format standard d'export des échanges HTTP depuis les DevTools.

### Comment ça fonctionne

Le processus est simple : vous exportez un fichier HAR depuis les DevTools de votre navigateur (onglet Network > clic droit > "Save all as HAR"), puis le script parcourt toutes les réponses HTTP pour extraire les cookies et vérifier leurs attributs de sécurité.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant B as 🌐 Browser
    participant H as 📄 HAR File
    participant P as 🐍 Python

    B->>H: Export HAR (DevTools)
    P->>H: json.load()
    P->>P: Parcourir entries
    P->>P: Extraire cookies
    P->>P: Vérifier httpOnly flag
    P-->>P: Rapport des cookies vulnérables
</div>

### Script d'Analyse HAR

Ce script parcourt un fichier HAR et identifie tous les cookies, en indiquant clairement lesquels sont protégés et lesquels sont vulnérables.

```python
import json

def find_http_only_cookies(har_file_path):
    """
    Analyse un fichier HAR pour identifier les cookies HttpOnly.

    Un cookie sans HttpOnly peut être volé via XSS (document.cookie).
    Un cookie sans Secure peut être intercepté sur HTTP.
    """
    with open(har_file_path, 'r') as f:
        har_data = json.load(f)

    cookies_info = []

    # Parcourir toutes les requêtes/réponses du fichier HAR
    for entry in har_data['log']['entries']:
        response = entry.get('response', {})
        for cookie in response.get('cookies', []):
            cookies_info.append({
                'name': cookie.get('name'),
                'httpOnly': cookie.get('httpOnly', False),
                'secure': cookie.get('secure', False),
                'url': entry['request']['url']
            })

    return cookies_info

# Exemple d'utilisation
cookies = find_http_only_cookies('session.har')
for c in cookies:
    status = "✅ Protégé" if c['httpOnly'] else "❌ Vulnérable"
    print(f"{c['name']}: {status}")
```


## Partie 3 : Anatomie d'une Attaque CSRF

Maintenant que nous comprenons comment vérifier les cookies, voyons comment fonctionne concrètement une attaque CSRF. Cette démonstration utilise l'exemple classique d'un transfert bancaire frauduleux.

### Le scénario d'attaque

L'attaque CSRF exploite la confiance aveugle du serveur dans les cookies de session. Voici le déroulement :

1. La victime est connectée à sa banque (elle a un cookie de session valide)
2. Elle visite un site malveillant (evil.com) contrôlé par l'attaquant
3. Ce site contient un formulaire invisible qui pointe vers la banque
4. Le formulaire s'envoie automatiquement, et le navigateur y ajoute le cookie de session
5. La banque reçoit une requête valide et exécute le transfert

<div class="mermaid">
flowchart TB
    subgraph Victim["👤 Victime"]
        V1["Connecté sur bank.com"]
        V2["Cookie de session actif"]
    end

    subgraph Attacker["🔴 Attaquant"]
        A1["evil.com"]
        A2["Page piégée"]
    end

    subgraph Bank["🏦 Banque"]
        B1["bank.com"]
        B2["/transfer?to=attacker&amount=1000"]
    end

    V1 -->|"1. Visite evil.com"| A1
    A2 -->|"2. Formulaire caché auto-submit"| V2
    V2 -->|"3. Requête avec cookie"| B2
    B2 -->|"4. Transfert effectué!"| B1

    style A1 fill:#e74c3c,fill-opacity:0.15
    style A2 fill:#e74c3c,fill-opacity:0.15
    style Bank fill:#808080,fill-opacity:0.15
    style Attacker fill:#808080,fill-opacity:0.15
    style Victim fill:#808080,fill-opacity:0.15
</div>

### La page malveillante

Voici à quoi ressemble la page hébergée par l'attaquant. Le piège est simple mais diablement efficace : un formulaire invisible qui s'envoie dès le chargement de la page.

```html
<!-- evil.com/csrf.html -->
<html>
<body onload="document.forms[0].submit()">
  <h1>Vous avez gagné un iPhone!</h1>

  <!-- Le formulaire est caché mais fonctionnel -->
  <form action="https://bank.com/transfer" method="POST" style="display:none">
    <input name="to" value="attacker_account">
    <input name="amount" value="10000">
  </form>
</body>
</html>
```

**Le point clé** : la victime n'a rien à faire. Le simple fait de charger la page déclenche l'attaque. Le navigateur envoie automatiquement le cookie de session de bank.com avec la requête, car c'est son comportement par défaut.


## Partie 4 : Les Protections CSRF

Heureusement, il existe plusieurs mécanismes de protection efficaces. Le choix de la protection dépend de l'architecture de votre application et de votre tolérance aux faux positifs.

<div class="mermaid">
flowchart LR
    subgraph Protection["🛡️ Protections CSRF"]
        T1["Token CSRF"]
        T2["SameSite Cookie"]
        T3["Vérification Referer"]
        T4["Double Submit"]
    end

    subgraph Impl["📝 Implémentation"]
        I1["<input type='hidden' name='csrf_token'>"]
        I2["Set-Cookie: SameSite=Strict"]
        I3["if referer != origin: reject"]
        I4["Cookie + Header match"]
    end

    T1 --> I1
    T2 --> I2
    T3 --> I3
    T4 --> I4

    style T1 fill:#2ecc71,fill-opacity:0.15
    style T2 fill:#3498db,fill-opacity:0.15
    style T3 fill:#f39c12,fill-opacity:0.15
    style T4 fill:#9b59b6,fill-opacity:0.15
    style Impl fill:#808080,fill-opacity:0.15
    style Protection fill:#808080,fill-opacity:0.15
</div>

### Le Token CSRF : la protection la plus robuste

Le principe est simple : chaque formulaire contient un token secret généré par le serveur. L'attaquant ne peut pas connaître ce token (car il ne peut pas lire le contenu des pages de la banque), donc il ne peut pas construire un formulaire valide.

### Implémentation Flask avec Flask-WTF

Flask-WTF gère automatiquement la génération et la vérification des tokens CSRF. Voici comment l'utiliser :

```python
from flask import Flask, session, request, abort
from flask_wtf.csrf import CSRFProtect
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
csrf = CSRFProtect(app)  # Active la protection CSRF globale

@app.route('/transfer', methods=['POST'])
def transfer():
    # Le token CSRF est vérifié AUTOMATIQUEMENT par Flask-WTF
    # Si le token est absent ou invalide, la requête est rejetée (400)
    to = request.form['to']
    amount = request.form['amount']
    return "Transfert effectué"
```

```html
<!-- Template avec token CSRF -->
<form method="POST" action="/transfer">
    <!-- Flask-WTF injecte automatiquement le token -->
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <input name="to" placeholder="Destinataire">
    <input name="amount" placeholder="Montant">
    <button>Transférer</button>
</form>
```


## Comparaison : Avant et Après Protection

Pour résumer, voici les différences de configuration entre une application vulnérable et une application correctement protégée :

| Attribut | Sans Protection | Avec Protection |
|----------|-----------------|-----------------|
| HttpOnly | ❌ Cookie accessible en JS | ✅ Cookie invisible pour JS |
| Secure | ❌ Envoyé sur HTTP | ✅ HTTPS uniquement |
| SameSite | None (envoyé partout) | Strict (même site uniquement) |
| Token CSRF | ❌ Aucun | ✅ Vérifié à chaque requête |


## Pour Aller Plus Loin

Ce laboratoire n'est qu'une introduction aux attaques CSRF. Pour approfondir vos connaissances :

- 📚 [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) - Le guide de référence
- 🔧 [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/en/1.2.x/csrf/) - Protection CSRF en Flask
- 🌐 [MDN Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie) - Attributs des cookies
- 📄 [Spécification HAR](http://www.softwareishard.com/blog/har-12-spec/) - Format des fichiers HAR


## Exploits et Vulnérabilités Connues

- **CVE-2019-11358 (jQuery)** : Vulnérabilité de pollution de prototype dans jQuery pouvant être combinée avec CSRF pour exécuter du code malveillant. Affectait des millions de sites utilisant jQuery < 3.4.0.

- **CVE-2008-0166 (WordPress)** : Vulnérabilité CSRF dans l'administration WordPress permettant la modification des paramètres du site et l'ajout d'administrateurs malveillants sans authentification.

- **CVE-2020-8193 (Citrix ADC/Gateway)** : Faille CSRF permettant l'exécution de commandes arbitraires sur les équipements Citrix, affectant des milliers d'entreprises mondiales.

- **CVE-2012-0394 (Apache Struts)** : Vulnérabilité CSRF dans le framework Struts permettant la modification de paramètres applicatifs via des requêtes forgées.

- **Netflix CSRF Vulnerability (2006)** : Cas historique où un attaquant pouvait modifier l'adresse de livraison et commander des DVD sur le compte de victimes simplement en leur faisant visiter une page malveillante.


## Approfondissement Théorique

Le CSRF a été formellement décrit pour la première fois par Peter Watkins en 2001 sous le nom "session riding". L'attaque exploite un problème fondamental du modèle de sécurité web : les cookies sont automatiquement attachés à toutes les requêtes vers un domaine, indépendamment de l'origine de la requête. Cette conception, qui facilite l'expérience utilisateur (rester connecté), crée une vulnérabilité inhérente.

L'attribut SameSite des cookies, introduit en 2016 et standardisé dans la RFC 6265bis, représente la défense la plus moderne contre CSRF. Trois valeurs sont possibles : Strict (le cookie n'est jamais envoyé cross-site), Lax (envoyé uniquement pour les navigations top-level GET), et None (comportement legacy, nécessite Secure). Depuis Chrome 80 (2020), SameSite=Lax est la valeur par défaut, ce qui a considérablement réduit la surface d'attaque CSRF sur le web moderne.

La défense en profondeur contre CSRF combine plusieurs mécanismes : tokens synchroniseur (state lié à la session), pattern double-submit cookie (token dans cookie et header/body), vérification de l'en-tête Origin/Referer, et interactions utilisateur explicites (re-authentification pour actions sensibles). Les APIs REST modernes utilisent souvent des tokens Bearer dans le header Authorization plutôt que des cookies, éliminant naturellement le risque CSRF car ces headers ne sont jamais envoyés automatiquement par le navigateur.


---

