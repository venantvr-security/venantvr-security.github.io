#!/usr/bin/env python3
"""
Générateur de QCM pour les repos venantvr-security
Génère 30 questions techniques par repo basées sur le contenu et le domaine
"""

import os
import json
from datetime import datetime

TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPOS_DIR = os.path.join(BASE_DIR, "repos")

# QCM par repo avec 30 questions techniques
QCM_DATA = {
    "Python.HAR.ZAP": {
        "description": "DAST Security Platform avec OWASP ZAP",
        "questions": [
            {"question": "Que signifie DAST dans le contexte de la sécurité applicative ?", "options": ["Dynamic Application Security Testing", "Data Analysis Security Tool", "Database Application Security Test", "Direct Access Security Testing"], "answer": 0},
            {"question": "Quel est le port par défaut de OWASP ZAP en mode proxy ?", "options": ["8080", "8443", "9090", "3128"], "answer": 0},
            {"question": "Qu'est-ce qu'un fichier HAR ?", "options": ["HTTP Archive Record", "HTML Archive Resource", "Hypertext Application Response", "Header Analysis Report"], "answer": 0},
            {"question": "Quelle attaque Red Team teste si les endpoints sont accessibles sans authentification ?", "options": ["Unauthenticated Replay", "Mass Assignment", "CSRF Attack", "XSS Injection"], "answer": 0},
            {"question": "Quel payload est typiquement utilisé pour le Mass Assignment ?", "options": ["{\"role\": \"admin\"}", "{\"password\": \"test\"}", "{\"debug\": true}", "{\"token\": null}"], "answer": 0},
            {"question": "Quelle métrique est utilisée pour évaluer la prévisibilité des tokens de session ?", "options": ["Entropie de Shannon", "Indice de Gini", "Coefficient de Pearson", "Score Z"], "answer": 0},
            {"question": "Quel header HTTP protège contre le clickjacking ?", "options": ["X-Frame-Options", "X-XSS-Protection", "Content-Type", "Cache-Control"], "answer": 0},
            {"question": "Que signifie IDOR ?", "options": ["Insecure Direct Object Reference", "Internal Data Object Request", "Indirect Directory Object Reference", "Input Data Override Request"], "answer": 0},
            {"question": "Quel format d'export est compatible avec GitHub Security ?", "options": ["SARIF", "JUnit", "CSV", "TXT"], "answer": 0},
            {"question": "Quelle directive CSP est considérée comme dangereuse ?", "options": ["unsafe-inline", "default-src", "script-src", "img-src"], "answer": 0},
            {"question": "Combien de sessions HAR sont nécessaires pour la détection IDOR ?", "options": ["2", "1", "3", "4"], "answer": 0},
            {"question": "Quel attribut de cookie empêche l'accès JavaScript ?", "options": ["HttpOnly", "Secure", "SameSite", "Path"], "answer": 0},
            {"question": "Quelle vulnérabilité Race Condition cible-t-elle principalement ?", "options": ["TOCTOU", "Buffer Overflow", "SQL Injection", "XSS"], "answer": 0},
            {"question": "Quel outil est utilisé pour l'orchestration Docker de ZAP ?", "options": ["docker_manager.py", "zap_manager.py", "container_handler.py", "docker_zap.py"], "answer": 0},
            {"question": "Quelle interface web utilise Streamlit ?", "options": ["localhost:8501", "localhost:8080", "localhost:3000", "localhost:5000"], "answer": 0},
            {"question": "Quel paramètre CLI échoue le build si des alertes critiques sont trouvées ?", "options": ["--fail-fast", "--strict", "--error-on-high", "--abort"], "answer": 0},
            {"question": "Quel type de scan ne modifie pas l'application cible ?", "options": ["Scan passif", "Scan actif", "Fuzzing", "Injection"], "answer": 0},
            {"question": "Quelle technique détecte les paramètres cachés comme ?debug=true ?", "options": ["Hidden Parameter Discovery", "Parameter Mining", "Debug Injection", "Path Traversal"], "answer": 0},
            {"question": "Quel header indique l'utilisation de HTTPS strict ?", "options": ["Strict-Transport-Security", "X-HTTPS-Only", "Secure-Connection", "TLS-Required"], "answer": 0},
            {"question": "Quel regex pattern détecte les clés AWS ?", "options": ["AKIA[0-9A-Z]{16}", "aws_[a-z]{20}", "AWS-KEY-*", "arn:aws:*"], "answer": 0},
            {"question": "Quelle bibliothèque Python est utilisée pour le parallélisme des attaques ?", "options": ["ThreadPoolExecutor", "multiprocessing", "asyncio", "celery"], "answer": 0},
            {"question": "Quel seuil de content-length ratio indique un bypass d'authentification ?", "options": ["> 50%", "> 25%", "> 75%", "> 90%"], "answer": 0},
            {"question": "Quel format est utilisé pour Jenkins/GitLab CI ?", "options": ["JUnit XML", "SARIF", "JSON", "HTML"], "answer": 0},
            {"question": "Quelle méthode HTTP est typiquement ciblée par Mass Assignment ?", "options": ["POST/PUT/PATCH", "GET", "DELETE", "OPTIONS"], "answer": 0},
            {"question": "Quel onglet Streamlit gère les critères de pass/fail CI/CD ?", "options": ["Acceptance", "Results", "Config", "Settings"], "answer": 0},
            {"question": "Combien d'onglets possède l'interface Streamlit de l'outil ?", "options": ["9", "7", "5", "12"], "answer": 0},
            {"question": "Quelle entropie minimale est recommandée pour les tokens de session ?", "options": ["4.0 bits", "2.0 bits", "6.0 bits", "8.0 bits"], "answer": 0},
            {"question": "Quel module gère l'import OpenAPI/Swagger ?", "options": ["openapi_importer.py", "swagger_parser.py", "api_loader.py", "spec_reader.py"], "answer": 0},
            {"question": "Quelle attaque exploite les différences de timing entre requêtes ?", "options": ["Race Condition", "Time-based SQLi", "Slow DoS", "Timing Attack"], "answer": 0},
            {"question": "Quel est l'objectif principal du PayloadReconstructor ?", "options": ["Génération de payloads d'attaque", "Reconstruction de requêtes", "Parsing de réponses", "Validation de schémas"], "answer": 0}
        ]
    },
    "Python.HAR.Scanner": {
        "description": "Analyseur de fichiers HAR pour la sécurité",
        "questions": [
            {"question": "Quelle bibliothèque Python est utilisée pour parser les fichiers HAR ?", "options": ["haralyzer", "harparser", "httparchive", "har-python"], "answer": 0},
            {"question": "Quel est le format d'un fichier HAR ?", "options": ["JSON", "XML", "YAML", "Binary"], "answer": 0},
            {"question": "Quelle section du HAR contient les informations de requête ?", "options": ["entries[].request", "requests[]", "data.request", "log.request"], "answer": 0},
            {"question": "Comment accéder aux cookies dans une réponse HAR ?", "options": ["entry['response']['cookies']", "entry['cookies']", "response.getCookies()", "har.cookies"], "answer": 0},
            {"question": "Quel attribut indique qu'un cookie est accessible uniquement via HTTP ?", "options": ["httpOnly", "secureOnly", "httpAccess", "noScript"], "answer": 0},
            {"question": "Comment vérifier si une requête utilise HTTPS dans un HAR ?", "options": ["url.startswith('https')", "request.secure == True", "protocol == 'https'", "entry.isSecure()"], "answer": 0},
            {"question": "Quelle bibliothèque est recommandée pour l'analyse avancée des données HAR ?", "options": ["pandas", "numpy", "scipy", "matplotlib"], "answer": 0},
            {"question": "Quel header de sécurité protège contre le MIME sniffing ?", "options": ["X-Content-Type-Options", "Content-Type", "X-MIME-Secure", "Accept"], "answer": 0},
            {"question": "Quelle valeur du header X-Content-Type-Options empêche le sniffing ?", "options": ["nosniff", "disable", "strict", "none"], "answer": 0},
            {"question": "Comment identifier une fuite de stack trace dans une réponse ?", "options": ["Recherche de patterns d'erreur dans le body", "Vérification du status code", "Analyse des headers", "Calcul du checksum"], "answer": 0},
            {"question": "Quel module Python charge un fichier JSON ?", "options": ["json", "pickle", "yaml", "csv"], "answer": 0},
            {"question": "Comment itérer sur toutes les entrées d'un fichier HAR ?", "options": ["for entry in har_data['log']['entries']", "for entry in har_data['entries']", "for entry in har_data.entries()", "har_data.forEach()"], "answer": 0},
            {"question": "Quel attribut de cookie garantit la transmission uniquement sur HTTPS ?", "options": ["Secure", "HttpOnly", "Encrypted", "TLS"], "answer": 0},
            {"question": "Quelle méthode Python ouvre un fichier en lecture ?", "options": ["open(path, 'r')", "read(path)", "File.open(path)", "load(path)"], "answer": 0},
            {"question": "Quel header indique le type de contenu d'une réponse ?", "options": ["Content-Type", "Accept", "Content-Encoding", "Transfer-Encoding"], "answer": 0},
            {"question": "Comment détecter une politique CSP dans les headers ?", "options": ["Rechercher 'Content-Security-Policy'", "Vérifier 'X-CSP'", "Analyser 'Security-Policy'", "Parser 'CSP-Header'"], "answer": 0},
            {"question": "Quelle information le champ 'timings' du HAR contient-il ?", "options": ["Métriques de performance réseau", "Timestamps absolus", "Durée de session", "TTL des cookies"], "answer": 0},
            {"question": "Comment identifier les requêtes POST dans un HAR ?", "options": ["entry['request']['method'] == 'POST'", "entry.isPost()", "request.type == 'POST'", "method.equals('POST')"], "answer": 0},
            {"question": "Quel champ contient le corps de la requête POST ?", "options": ["request['postData']", "request['body']", "request['content']", "request['payload']"], "answer": 0},
            {"question": "Comment détecter les tokens JWT dans les réponses ?", "options": ["Regex pattern eyJ...", "Header 'JWT-Token'", "Cookie 'jwt'", "Field 'token_type'"], "answer": 0},
            {"question": "Quel outil génère des fichiers HAR depuis le navigateur ?", "options": ["Chrome DevTools", "Wireshark", "tcpdump", "curl"], "answer": 0},
            {"question": "Quelle est la structure racine d'un fichier HAR ?", "options": ["log", "har", "data", "archive"], "answer": 0},
            {"question": "Comment obtenir le status code d'une réponse ?", "options": ["entry['response']['status']", "entry['status']", "response.code", "entry.getStatus()"], "answer": 0},
            {"question": "Quel champ contient la taille de la réponse ?", "options": ["response['content']['size']", "response['size']", "response['length']", "content['bytes']"], "answer": 0},
            {"question": "Comment détecter les endpoints API dans un HAR ?", "options": ["Analyser les URLs avec patterns /api/", "Vérifier le Content-Type application/json", "Les deux méthodes ci-dessus", "Compter les requêtes GET"], "answer": 2},
            {"question": "Quelle version de HAR est la plus courante ?", "options": ["1.2", "1.0", "2.0", "1.1"], "answer": 0},
            {"question": "Comment extraire tous les domaines uniques d'un HAR ?", "options": ["Parser l'URL de chaque entry et extraire le hostname", "Utiliser le champ 'domains'", "Lire les headers 'Host'", "Utiliser entry.domain"], "answer": 0},
            {"question": "Quel champ indique si la requête provient du cache ?", "options": ["cache", "fromCache", "cached", "cacheHit"], "answer": 0},
            {"question": "Comment calculer le temps total d'une requête ?", "options": ["Sommer les champs dans 'timings'", "Lire 'totalTime'", "entry['duration']", "response['time']"], "answer": 0},
            {"question": "Quelle information 'creator' contient-elle dans un HAR ?", "options": ["Nom et version de l'outil qui a généré le HAR", "Auteur du site web", "User-Agent", "Timestamp de création"], "answer": 0}
        ]
    },
    "Rust.Nmap.Network": {
        "description": "Laboratoire IDS avec Snort, Suricata et Zeek",
        "questions": [
            {"question": "Quels sont les trois IDS testés dans ce laboratoire ?", "options": ["Snort, Suricata, Zeek", "Snort, Ossec, Fail2ban", "Suricata, Tripwire, AIDE", "Zeek, Snort, ModSecurity"], "answer": 0},
            {"question": "Quel langage est utilisé pour développer le Commander ?", "options": ["Rust", "Python", "Go", "C++"], "answer": 0},
            {"question": "Combien de niveaux de sécurité sont disponibles ?", "options": ["5", "3", "4", "6"], "answer": 0},
            {"question": "Quel niveau détecte uniquement les attaques évidentes ?", "options": ["Minimal (1)", "Basic (2)", "Moderate (3)", "Strict (4)"], "answer": 0},
            {"question": "Quel port utilise le dashboard Commander ?", "options": ["3000", "8080", "5000", "9000"], "answer": 0},
            {"question": "Quel port utilise EveBox pour Suricata ?", "options": ["5636", "8080", "9200", "5601"], "answer": 0},
            {"question": "Quelle technique Nmap utilise -f pour l'évasion ?", "options": ["Fragmentation IP", "Timing lent", "Decoys", "Source port"], "answer": 0},
            {"question": "Quelle option Nmap utilise des leurres aléatoires ?", "options": ["-D RND:10", "-f", "-T0", "--source-port"], "answer": 0},
            {"question": "Quel timing Nmap est le plus lent ?", "options": ["-T0", "-T1", "-T2", "-T5"], "answer": 0},
            {"question": "Quel port source est souvent autorisé par les firewalls ?", "options": ["53 (DNS)", "22 (SSH)", "443 (HTTPS)", "8080 (Proxy)"], "answer": 0},
            {"question": "Quel outil Python manipule les paquets IP ?", "options": ["Scapy", "Requests", "Socket", "Twisted"], "answer": 0},
            {"question": "Quel script démarre tous les labs ?", "options": ["start_all_labs.sh", "init_labs.sh", "run_all.sh", "launch.sh"], "answer": 0},
            {"question": "Quelle commande Docker compose démarre les conteneurs ?", "options": ["docker compose up -d", "docker-compose start", "docker run -d", "docker compose run"], "answer": 0},
            {"question": "Quel type de scan XMAS active tous les flags TCP ?", "options": ["FIN, PSH, URG", "SYN, ACK", "RST, FIN", "PSH, ACK"], "answer": 0},
            {"question": "Quel niveau de sécurité détecte la fragmentation ?", "options": ["Strict (4)", "Moderate (3)", "Basic (2)", "Minimal (1)"], "answer": 0},
            {"question": "Quel est le niveau 'Paranoid' ?", "options": ["5", "4", "3", "6"], "answer": 0},
            {"question": "Quel outil de visualisation est intégré pour Suricata ?", "options": ["EveBox", "Kibana", "Grafana", "Splunk"], "answer": 0},
            {"question": "Quel éditeur web permet de modifier les règles ?", "options": ["Filebrowser", "VSCode Web", "Theia", "Cloud9"], "answer": 0},
            {"question": "Quel script teste un lab rapidement ?", "options": ["quick_test.sh", "test.sh", "verify.sh", "check.sh"], "answer": 0},
            {"question": "Comment ajouter l'utilisateur au groupe Docker ?", "options": ["sudo usermod -aG docker $USER", "docker adduser $USER", "sudo docker group add", "useradd docker"], "answer": 0},
            {"question": "Quel scan Nmap utilise des paquets NULL ?", "options": ["-sN", "-sS", "-sT", "-sU"], "answer": 0},
            {"question": "Quel réseau Docker est créé pour Snort ?", "options": ["snort_net", "snort_network", "ids_snort", "network_snort"], "answer": 0},
            {"question": "Quel serveur web est utilisé comme cible ?", "options": ["nginx", "apache", "lighttpd", "caddy"], "answer": 0},
            {"question": "Quelle option Nmap définit le MTU ?", "options": ["--mtu", "-f", "--fragment-size", "--ip-options"], "answer": 0},
            {"question": "Quel fichier contient les règles Suricata ?", "options": ["rules/*.rules", "suricata.yaml", "config.rules", "alerts.conf"], "answer": 0},
            {"question": "Quel niveau est recommandé pour tester l'évasion ?", "options": ["Moderate (3)", "Minimal (1)", "Paranoid (5)", "Strict (4)"], "answer": 0},
            {"question": "Quel protocole Zeek analyse principalement ?", "options": ["Tous les protocoles réseau", "HTTP uniquement", "TCP uniquement", "DNS uniquement"], "answer": 0},
            {"question": "Quelle commande rafraîchit les groupes utilisateur ?", "options": ["newgrp docker", "refresh groups", "reload docker", "docker refresh"], "answer": 0},
            {"question": "Quel script scanne tous les niveaux de sécurité ?", "options": ["scan_all_levels.sh", "full_scan.sh", "level_test.sh", "multi_scan.sh"], "answer": 0},
            {"question": "Quel type de log Suricata génère-t-il ?", "options": ["EVE JSON", "Syslog", "CSV", "XML"], "answer": 0}
        ]
    },
    "Python.CSRF.Demo": {
        "description": "Démonstration de vulnérabilités CSRF",
        "questions": [
            {"question": "Que signifie CSRF ?", "options": ["Cross-Site Request Forgery", "Cross-Site Resource Failure", "Client-Side Request Forgery", "Cross-Server Request Fraud"], "answer": 0},
            {"question": "Quel mécanisme de défense principal protège contre CSRF ?", "options": ["Token anti-CSRF", "HTTPS", "CORS", "CSP"], "answer": 0},
            {"question": "Quelle méthode HTTP est généralement ciblée par CSRF ?", "options": ["POST", "GET (safe)", "OPTIONS", "HEAD"], "answer": 0},
            {"question": "Où le token CSRF est-il typiquement stocké ?", "options": ["Champ caché du formulaire + session", "URL uniquement", "LocalStorage", "Cookies uniquement"], "answer": 0},
            {"question": "Quel attribut de cookie aide à prévenir CSRF ?", "options": ["SameSite", "HttpOnly", "Secure", "Path"], "answer": 0},
            {"question": "Quelle valeur SameSite offre la meilleure protection ?", "options": ["Strict", "Lax", "None", "Default"], "answer": 0},
            {"question": "Comment un attaquant exploite-t-il CSRF ?", "options": ["Page malveillante avec formulaire auto-soumis", "Injection SQL", "XSS stocké", "Man-in-the-middle"], "answer": 0},
            {"question": "Quelle condition rend CSRF possible ?", "options": ["Cookies de session envoyés automatiquement", "Absence de HTTPS", "Serveur mal configuré", "Mots de passe faibles"], "answer": 0},
            {"question": "Quel header peut aider à détecter les requêtes cross-origin ?", "options": ["Origin", "Referer", "X-Requested-With", "Toutes les réponses ci-dessus"], "answer": 3},
            {"question": "Quelle action est typiquement ciblée par CSRF ?", "options": ["Changement de mot de passe", "Lecture de données", "Navigation", "Téléchargement"], "answer": 0},
            {"question": "Comment vérifier un token CSRF côté serveur ?", "options": ["Comparer avec la valeur en session", "Vérifier la signature", "Décoder le JWT", "Calculer le hash"], "answer": 0},
            {"question": "Quelle est la durée de vie recommandée d'un token CSRF ?", "options": ["Session utilisateur", "24 heures", "1 heure", "Permanent"], "answer": 0},
            {"question": "Quel framework Python génère automatiquement des tokens CSRF ?", "options": ["Django", "Flask (sans extension)", "Bottle", "Tornado"], "answer": 0},
            {"question": "Comment contourner une protection CSRF faible ?", "options": ["Token prévisible ou absent", "Injection XSS", "Forcer le navigateur", "Désactiver JavaScript"], "answer": 0},
            {"question": "Quelle balise HTML est souvent utilisée pour CSRF silencieux ?", "options": ["img src", "script", "link", "meta"], "answer": 0},
            {"question": "Pourquoi les API REST sont-elles souvent vulnérables à CSRF ?", "options": ["Absence de tokens dans les requêtes API", "Utilisation de GET uniquement", "CORS mal configuré", "Pas de sessions"], "answer": 0},
            {"question": "Quel en-tête personnalisé peut protéger une API contre CSRF ?", "options": ["X-Requested-With: XMLHttpRequest", "X-CSRF-Token", "Authorization", "Content-Type"], "answer": 0},
            {"question": "Comment le pattern Synchronizer Token fonctionne-t-il ?", "options": ["Token unique par session, vérifié à chaque requête", "Double soumission de cookie", "Vérification de l'Origin", "Timestamp dans la requête"], "answer": 0},
            {"question": "Quel est l'impact typique d'une attaque CSRF réussie ?", "options": ["Actions non autorisées au nom de la victime", "Vol de données", "Déni de service", "Escalade de privilèges"], "answer": 0},
            {"question": "Quelle est la différence entre CSRF et XSS ?", "options": ["CSRF exploite la confiance du serveur, XSS celle du client", "CSRF vole des données, XSS exécute des actions", "Aucune différence", "CSRF nécessite JavaScript"], "answer": 0},
            {"question": "Comment SameSite=Lax fonctionne-t-il ?", "options": ["Cookies envoyés pour navigation top-level GET", "Cookies jamais envoyés cross-site", "Comme None mais avec flag", "Bloque tous les POST"], "answer": 0},
            {"question": "Quel type de token est préférable : par requête ou par session ?", "options": ["Par session (plus pratique, sécurité suffisante)", "Par requête (plus sécurisé)", "Aucun (autre méthode)", "Dépend du contexte"], "answer": 3},
            {"question": "Pourquoi vérifier le header Referer n'est-il pas suffisant ?", "options": ["Peut être supprimé par politiques de confidentialité", "Toujours fiable", "Non supporté par les navigateurs", "Trop lent à vérifier"], "answer": 0},
            {"question": "Quelle attaque combine XSS et CSRF ?", "options": ["Extraction du token CSRF via XSS", "Double CSRF", "CSRF persistant", "Session hijacking"], "answer": 0},
            {"question": "Comment protéger un formulaire de login contre CSRF ?", "options": ["Token CSRF même avant authentification", "HTTPS suffit", "CAPTCHA uniquement", "Rate limiting"], "answer": 0},
            {"question": "Quel mécanisme JavaScript aide à prévenir CSRF ?", "options": ["Fetch avec credentials: 'same-origin'", "eval()", "document.write()", "innerHTML"], "answer": 0},
            {"question": "Comment tester une vulnérabilité CSRF ?", "options": ["Créer une page HTML avec formulaire ciblant le site", "Scanner automatique", "Fuzzing", "Analyse statique"], "answer": 0},
            {"question": "Quelle est la classification OWASP de CSRF ?", "options": ["A01:2021 Broken Access Control", "A03:2021 Injection", "A07:2021 XSS", "A05:2021 Security Misconfiguration"], "answer": 0},
            {"question": "Pourquoi les requêtes GET ne devraient pas modifier l'état ?", "options": ["Facilement exploitables via img/link tags", "Trop lentes", "Non supportées par CSRF", "Limitées en taille"], "answer": 0},
            {"question": "Quel outil peut automatiser les tests CSRF ?", "options": ["Burp Suite", "Nmap", "Wireshark", "Netcat"], "answer": 0}
        ]
    },
    "Scapy.Strategies": {
        "description": "Manipulation de paquets IP pour évasion IDS",
        "questions": [
            {"question": "Quelle bibliothèque Python est utilisée pour manipuler les paquets ?", "options": ["Scapy", "Socket", "Requests", "Twisted"], "answer": 0},
            {"question": "Pourquoi les privilèges root sont-ils nécessaires pour Scapy ?", "options": ["Pour accéder aux raw sockets", "Pour installer les dépendances", "Pour modifier les fichiers système", "Pour le logging"], "answer": 0},
            {"question": "Quelle technique utilise des fragments IP chevauchants ?", "options": ["Overlapping fragments", "Tiny fragments", "Timing evasion", "TTL manipulation"], "answer": 0},
            {"question": "Qu'est-ce qu'un scan Christmas Tree ?", "options": ["Tous les flags TCP activés", "Scan durant Noël", "Scan avec payload festif", "Scan multi-protocole"], "answer": 0},
            {"question": "Quel drapeau TCP initie une connexion ?", "options": ["SYN", "ACK", "FIN", "RST"], "answer": 0},
            {"question": "Quelle catégorie de script est marquée 'rouge' ?", "options": ["Dangereux (techniques d'attaque)", "Safe", "Prudence", "Déprécié"], "answer": 0},
            {"question": "Comment créer un tunnel ICMP avec Scapy ?", "options": ["Encapsuler des données dans des paquets ICMP Echo", "Modifier les headers IP", "Utiliser le TTL", "Fragmenter les paquets"], "answer": 0},
            {"question": "Qu'est-ce que l'exfiltration DNS ?", "options": ["Encoder des données dans des requêtes DNS", "Voler les enregistrements DNS", "Modifier le cache DNS", "DoS sur serveur DNS"], "answer": 0},
            {"question": "Quelle technique varie le délai entre les paquets ?", "options": ["Jitter", "Burst", "Slow scan", "Fragmentation"], "answer": 0},
            {"question": "Comment éviter la détection par timing ?", "options": ["Scan très lent (slow_scan)", "Scan rapide", "Scan aléatoire", "Pas d'évasion possible"], "answer": 0},
            {"question": "Quel champ IP permet de manipuler le routage ?", "options": ["TTL", "Version", "Checksum", "TOS"], "answer": 0},
            {"question": "Comment créer un paquet IP fragmenté avec Scapy ?", "options": ["IP(flags='MF')/payload", "fragment(packet)", "IP.split()", "Scapy.fragment()"], "answer": 0},
            {"question": "Quelle technique utilise plusieurs protocoles alternativement ?", "options": ["Protocol switch", "Multi-protocol scan", "Protocol hopping", "Layer mixing"], "answer": 0},
            {"question": "Comment envoyer un paquet avec Scapy ?", "options": ["send() ou sr()", "transmit()", "push()", "deliver()"], "answer": 0},
            {"question": "Quelle fonction reçoit les réponses aux paquets ?", "options": ["sr() / sr1()", "recv()", "listen()", "capture()"], "answer": 0},
            {"question": "Qu'est-ce qu'un canal caché (covert channel) ?", "options": ["Communication via champs non conventionnels", "VPN", "Tunnel SSH", "Proxy"], "answer": 0},
            {"question": "Quel champ peut cacher des données dans un paquet IP ?", "options": ["Options IP ou ID", "Version", "Header Length", "Protocol"], "answer": 0},
            {"question": "Comment installer Scapy ?", "options": ["pip install scapy", "apt install scapy", "brew install scapy", "npm install scapy"], "answer": 0},
            {"question": "Quelle combinaison de flags TCP est invalide ?", "options": ["SYN+FIN", "SYN+ACK", "FIN+ACK", "PSH+ACK"], "answer": 0},
            {"question": "Comment lancer un script Scapy avec privilèges ?", "options": ["sudo python3 script.py", "python3 script.py --root", "scapy-admin script.py", "run-as-root script.py"], "answer": 0},
            {"question": "Quel dossier contient les scripts de fragmentation ?", "options": ["fragmentation/", "fragments/", "ip_frag/", "frag_scripts/"], "answer": 0},
            {"question": "Qu'est-ce que le burst mode ?", "options": ["Envoi de paquets en rafales", "Scan continu", "Mode silencieux", "Compression des paquets"], "answer": 0},
            {"question": "Comment créer un paquet TCP avec Scapy ?", "options": ["IP()/TCP()", "TCP.create()", "Packet('TCP')", "new TCP()"], "answer": 0},
            {"question": "Quel flag de légalité indique 'Safe' ?", "options": ["🟢", "🟠", "🔴", "⚪"], "answer": 0},
            {"question": "Quelle technique manipule le Time To Live ?", "options": ["TTL manipulation", "Timing attack", "Time-based scan", "Delay injection"], "answer": 0},
            {"question": "Comment sniffer des paquets avec Scapy ?", "options": ["sniff()", "capture()", "listen()", "monitor()"], "answer": 0},
            {"question": "Quelle couche OSI Scapy manipule principalement ?", "options": ["Couches 3 et 4 (Réseau et Transport)", "Couche 7 (Application)", "Couche 2 (Liaison)", "Couche 1 (Physique)"], "answer": 0},
            {"question": "Comment afficher la structure d'un paquet Scapy ?", "options": ["packet.show()", "print(packet)", "packet.display()", "packet.info()"], "answer": 0},
            {"question": "Quelle technique envoie des micro-fragments ?", "options": ["Tiny fragments", "Nano packets", "Mini frames", "Micro segments"], "answer": 0},
            {"question": "Comment créer un paquet ICMP Echo avec Scapy ?", "options": ["IP()/ICMP()", "ICMP.echo()", "Ping()", "ICMP('echo')"], "answer": 0}
        ]
    },
    "Python.Sqli.Detection": {
        "description": "Scanner d'injections SQL",
        "questions": [
            {"question": "Que signifie SQL Injection ?", "options": ["Insertion de code SQL malveillant dans les entrées", "Optimisation SQL", "Génération automatique de SQL", "Compression de requêtes"], "answer": 0},
            {"question": "Quelle technique détecte les injections SQL aveugles ?", "options": ["Boolean-based blind", "Error-based", "Union-based", "Stacked queries"], "answer": 0},
            {"question": "Quel payload teste une injection de base ?", "options": ["' OR '1'='1", "SELECT *", "DROP TABLE", "CREATE USER"], "answer": 0},
            {"question": "Comment fonctionne le tampering ?", "options": ["Modification des payloads pour contourner les WAF", "Chiffrement des requêtes", "Compression des données", "Accélération des tests"], "answer": 0},
            {"question": "Quelle méthode compare les réponses pour détecter l'injection ?", "options": ["Différence HTTP (diff)", "Calcul de hash", "Timing", "Status code uniquement"], "answer": 0},
            {"question": "Quel outil est référencé pour les payloads SQL ?", "options": ["payloadbox/sql-injection-payload-list", "sqlmap", "burp-payloads", "sql-payloads-db"], "answer": 0},
            {"question": "Comment détecter une injection time-based ?", "options": ["Mesurer le délai de réponse avec SLEEP()", "Analyser les erreurs", "Compter les résultats", "Vérifier les redirections"], "answer": 0},
            {"question": "Quelle fonction SQL cause un délai ?", "options": ["SLEEP() ou WAITFOR", "DELAY()", "PAUSE()", "HOLD()"], "answer": 0},
            {"question": "Qu'est-ce que l'injection UNION-based ?", "options": ["Utilisation de UNION pour extraire des données", "Union de tables", "Fusion de requêtes", "Jointure automatique"], "answer": 0},
            {"question": "Comment contourner un filtre sur les guillemets ?", "options": ["Encodage hexadécimal ou double encoding", "Les supprimer", "Les doubler", "Utiliser des backticks"], "answer": 0},
            {"question": "Quel caractère commente en SQL ?", "options": ["-- ou #", "//", "/* uniquement", "%%"], "answer": 0},
            {"question": "Qu'est-ce que le stacked queries ?", "options": ["Exécution de multiples requêtes avec ;", "Requêtes imbriquées", "Sous-requêtes", "Batch processing"], "answer": 0},
            {"question": "Comment l'outil fuzze les endpoints ?", "options": ["Injection de payloads dans les query strings", "Modification des headers", "Changement de méthode HTTP", "Envoi de fichiers"], "answer": 0},
            {"question": "Quel type d'injection permet l'exécution de commandes OS ?", "options": ["xp_cmdshell (SQL Server)", "LOAD_FILE", "INTO OUTFILE", "EXEC"], "answer": 0},
            {"question": "Comment détecter le SGBD cible ?", "options": ["Analyse des messages d'erreur ou fingerprinting", "Header HTTP", "Port utilisé", "Version TLS"], "answer": 0},
            {"question": "Quelle fonction MySQL lit un fichier ?", "options": ["LOAD_FILE()", "READ_FILE()", "FILE_GET()", "GET_FILE()"], "answer": 0},
            {"question": "Comment extraire des données avec UNION ?", "options": ["UNION SELECT column FROM table--", "UNION GET data", "UNION EXTRACT", "UNION FETCH"], "answer": 0},
            {"question": "Quel est l'impact d'une injection SQL réussie ?", "options": ["Accès aux données, modification, voire contrôle du serveur", "Lenteur du site", "Affichage d'erreurs", "Redirection"], "answer": 0},
            {"question": "Comment se protéger contre SQL Injection ?", "options": ["Requêtes préparées (prepared statements)", "Filtrer les mots-clés SQL", "Limiter la longueur des entrées", "HTTPS"], "answer": 0},
            {"question": "Qu'est-ce que l'ORM ?", "options": ["Object-Relational Mapping - abstraction SQL", "Online Resource Manager", "Optimized Request Module", "Object Request Model"], "answer": 0},
            {"question": "Quelle classification OWASP concerne SQL Injection ?", "options": ["A03:2021 Injection", "A01:2021 Broken Access Control", "A07:2021 XSS", "A02:2021 Cryptographic Failures"], "answer": 0},
            {"question": "Comment tester l'injection sur une authentification ?", "options": ["admin'--", "admin OR 1=1", "'; DROP TABLE users;--", "Toutes les réponses"], "answer": 3},
            {"question": "Quel outil automatise les tests SQL injection ?", "options": ["sqlmap", "Nmap", "Burp Suite uniquement", "Wireshark"], "answer": 0},
            {"question": "Comment l'outil récupère les query strings d'applications PHP ?", "options": ["Projet Python.QueryStringsFromPhp", "Analyse statique", "Crawling", "Interception proxy"], "answer": 0},
            {"question": "Quelle méthode HTTP est la plus ciblée ?", "options": ["GET et POST", "PUT uniquement", "DELETE", "PATCH"], "answer": 0},
            {"question": "Comment fonctionne l'injection error-based ?", "options": ["Extraction de données via messages d'erreur SQL", "Génération d'erreurs HTTP", "Corruption de la base", "Denial of Service"], "answer": 0},
            {"question": "Quel payload contourne souvent les filtres basiques ?", "options": ["1' AND '1'='1' /*", "SELECT", "OR", "AND"], "answer": 0},
            {"question": "Comment encoder les payloads pour contourner les WAF ?", "options": ["URL encoding, double encoding, Unicode", "Base64", "Compression", "Chiffrement"], "answer": 0},
            {"question": "Quelle table système MySQL contient les métadonnées ?", "options": ["information_schema", "mysql.tables", "sys.tables", "metadata"], "answer": 0},
            {"question": "Quel dictionnaire est utilisé pour les noms de paramètres ?", "options": ["well-known-parameter-names-brute-force.txt", "params.txt", "common-params.lst", "fuzz-params.dic"], "answer": 0}
        ]
    },
    "Python.Tor.Proxy": {
        "description": "Proxy TOR avec interface GTK",
        "questions": [
            {"question": "Quelle bibliothèque Python contrôle Tor ?", "options": ["stem", "torpy", "tor-python", "pytorctl"], "answer": 0},
            {"question": "Quel port utilise Tor pour le contrôle ?", "options": ["9051", "9050", "9001", "9150"], "answer": 0},
            {"question": "Quel port utilise Tor pour le proxy SOCKS ?", "options": ["9050", "9051", "1080", "8080"], "answer": 0},
            {"question": "Quel module Python liste les interfaces réseau ?", "options": ["netifaces", "netinfo", "interfaces", "pynet"], "answer": 0},
            {"question": "Comment désactiver une interface réseau en Python ?", "options": ["subprocess + ip link set down", "netifaces.disable()", "os.disable_interface()", "socket.close_interface()"], "answer": 0},
            {"question": "Quel fichier configure Tor ?", "options": ["/etc/tor/torrc", "/etc/tor/config", "~/.tor/torrc", "/var/tor/config"], "answer": 0},
            {"question": "Comment changer le circuit Tor avec stem ?", "options": ["controller.signal(Signal.NEWNYM)", "controller.new_circuit()", "controller.rotate()", "tor.change_ip()"], "answer": 0},
            {"question": "Quelle interface loopback est toujours exclue ?", "options": ["lo", "eth0", "wlan0", "docker0"], "answer": 0},
            {"question": "Comment vérifier si Tor est actif ?", "options": ["Controller.from_port() + authenticate()", "ping tor", "netstat | grep tor", "ps aux | grep tor"], "answer": 0},
            {"question": "Quel GUI toolkit est mentionné ?", "options": ["GTK", "Qt", "Tkinter", "wxWidgets"], "answer": 0},
            {"question": "Comment trouver la route par défaut ?", "options": ["ip route | grep default", "netstat -r", "route -n", "Toutes les réponses"], "answer": 3},
            {"question": "Quel paramètre torrc définit l'interface sortante ?", "options": ["OutboundBindInterface", "BindAddress", "SocksBindAddress", "ExitInterface"], "answer": 0},
            {"question": "Comment obtenir l'IP actuelle via Tor ?", "options": ["Requête vers un service check IP", "controller.get_info('ip')", "tor --show-ip", "stem.get_external_ip()"], "answer": 0},
            {"question": "Quelle commande installe stem ?", "options": ["pip install stem", "apt install python3-stem", "pip install tor-stem", "pip install python-stem"], "answer": 0},
            {"question": "Comment authentifier le controller Tor ?", "options": ["controller.authenticate(password=...)", "controller.login()", "Controller.auth()", "stem.connect()"], "answer": 0},
            {"question": "Quel signal demande un nouveau circuit ?", "options": ["NEWNYM", "RELOAD", "REFRESH", "ROTATE"], "answer": 0},
            {"question": "Comment lister les circuits actifs ?", "options": ["controller.get_circuits()", "controller.list_circuits()", "tor.circuits", "stem.get_circuits()"], "answer": 0},
            {"question": "Quel système d'exploitation est ciblé principalement ?", "options": ["Linux", "Windows", "macOS", "BSD"], "answer": 0},
            {"question": "Pourquoi désactiver les interfaces non-Tor ?", "options": ["Prévenir les fuites de trafic hors Tor", "Améliorer les performances", "Libérer de la bande passante", "Simplifier la configuration"], "answer": 0},
            {"question": "Comment réactiver une interface ?", "options": ["ip link set <iface> up", "ifconfig <iface> up", "netctl start <iface>", "Toutes les réponses"], "answer": 3},
            {"question": "Quel type de proxy Tor utilise-t-il ?", "options": ["SOCKS5", "HTTP", "HTTPS", "SOCKS4"], "answer": 0},
            {"question": "Comment configurer Firefox pour Tor ?", "options": ["Proxy SOCKS5 localhost:9050", "Extension Tor", "TorBrowser uniquement", "PAC file"], "answer": 0},
            {"question": "Quelle distribution Linux intègre Tor nativement ?", "options": ["Tails", "Ubuntu", "Fedora", "Arch"], "answer": 0},
            {"question": "Comment vérifier la version de Tor ?", "options": ["tor --version", "torctl version", "stem --tor-version", "apt show tor"], "answer": 0},
            {"question": "Quel projet VM est mentionné pour Tor ?", "options": ["Whonix", "QubesOS", "VirtualBox", "VMware"], "answer": 0},
            {"question": "Comment démarrer Tor en service ?", "options": ["systemctl start tor", "tor start", "/etc/init.d/tor start", "service tor on"], "answer": 0},
            {"question": "Quelle information stem peut récupérer ?", "options": ["Circuits, bandwidth, relays", "Uniquement l'IP", "Les logs seulement", "Rien via API"], "answer": 0},
            {"question": "Comment gérer les erreurs de connexion Tor ?", "options": ["try/except avec stem.SocketError", "Ignorer les erreurs", "Retry infini", "Pas de gestion"], "answer": 0},
            {"question": "Quel est l'objectif de la rotation d'IP ?", "options": ["Anonymat renforcé", "Meilleure vitesse", "Contourner les limits", "Toutes les réponses"], "answer": 3},
            {"question": "Comment implémenter un system tray en GTK ?", "options": ["gi.repository.AppIndicator ou StatusIcon", "gtk.tray()", "systray.add()", "Notification.tray()"], "answer": 0}
        ]
    },
    "Python.Osint.Blackbird": {
        "description": "Recherche de noms d'utilisateur sur 500+ plateformes",
        "questions": [
            {"question": "Combien de sites Blackbird peut-il scanner ?", "options": ["574+", "100+", "250+", "1000+"], "answer": 0},
            {"question": "Que signifie OSINT ?", "options": ["Open Source Intelligence", "Online Security Intelligence", "Open System Internet", "Operational Security Int"], "answer": 0},
            {"question": "Comment rechercher un utilisateur avec Blackbird ?", "options": ["python blackbird.py -u username", "blackbird search username", "blackbird --find username", "python search.py username"], "answer": 0},
            {"question": "Quel format de sortie Blackbird génère-t-il ?", "options": ["JSON", "XML", "CSV", "TXT"], "answer": 0},
            {"question": "Comment lancer l'interface web ?", "options": ["python blackbird.py --web", "blackbird serve", "python web.py", "blackbird --gui"], "answer": 0},
            {"question": "Quel port utilise le serveur web ?", "options": ["9797", "8080", "5000", "3000"], "answer": 0},
            {"question": "Comment configurer un proxy ?", "options": ["--proxy http://127.0.0.1:8080", "-p proxy:port", "--use-proxy", "--tunnel"], "answer": 0},
            {"question": "Comment afficher tous les résultats ?", "options": ["--show-all", "--verbose", "--all", "-a"], "answer": 0},
            {"question": "Comment lister les sites supportés ?", "options": ["--list-sites", "--sites", "-l", "--show-sites"], "answer": 0},
            {"question": "Comment lire un fichier de résultats ?", "options": ["-f username.json", "--read file", "--input file", "-r results.json"], "answer": 0},
            {"question": "Quel projet a fourni la majorité des sites ?", "options": ["WhatsMyName", "Sherlock", "Maigret", "Social-Analyzer"], "answer": 0},
            {"question": "Comment installer les dépendances ?", "options": ["pip install -r requirements.txt", "python setup.py", "npm install", "make install"], "answer": 0},
            {"question": "Quelle bibliothèque Python gère les requêtes async ?", "options": ["aiohttp", "requests", "urllib", "httpx"], "answer": 0},
            {"question": "Comment utiliser Blackbird avec Docker ?", "options": ["docker pull p1ngul1n0/blackbird", "docker run blackbird", "docker build blackbird", "Pas de support Docker"], "answer": 0},
            {"question": "Quel type de matching Blackbird utilise-t-il ?", "options": ["Status code + contenu de page", "DNS lookup", "WHOIS", "Reverse image"], "answer": 0},
            {"question": "Comment le nom 'Blackbird' est-il inspiré ?", "options": ["Avion SR-71 Blackbird", "Oiseau", "Projet militaire", "Code secret"], "answer": 0},
            {"question": "Quels réseaux sociaux sont supportés ?", "options": ["Facebook, Twitter, Instagram, TikTok...", "Facebook uniquement", "Sites .onion", "Forums uniquement"], "answer": 0},
            {"question": "Comment Blackbird détecte-t-il un compte existant ?", "options": ["Analyse du status HTTP et contenu", "Email confirmation", "API officielle", "Captcha solving"], "answer": 0},
            {"question": "Quelle précaution légale est mentionnée ?", "options": ["Usage éducatif uniquement", "Aucune restriction", "Licence commerciale requise", "Autorisation gouvernementale"], "answer": 0},
            {"question": "Comment accélérer les recherches ?", "options": ["Requêtes asynchrones par défaut", "Multithreading manuel", "GPU acceleration", "Cluster computing"], "answer": 0},
            {"question": "Quel résultat indique un compte trouvé ?", "options": ["HTTP 200 + pattern matching positif", "HTTP 404", "Redirection", "Timeout"], "answer": 0},
            {"question": "Comment identifier les faux positifs ?", "options": ["Vérification manuelle du contenu", "100% automatisé", "Intelligence artificielle", "Crowdsourcing"], "answer": 0},
            {"question": "Quelle information est extraite par compte ?", "options": ["URL du profil, status, site name", "Mot de passe", "Email", "Adresse IP"], "answer": 0},
            {"question": "Comment contribuer au projet ?", "options": ["Ajouter des sites via PR GitHub", "Email au développeur", "Forum dédié", "Pas de contribution externe"], "answer": 0},
            {"question": "Quel pattern HTTP indique l'absence de compte ?", "options": ["HTTP 404 ou message 'not found'", "HTTP 200", "HTTP 500", "Redirection 301"], "answer": 0},
            {"question": "Comment Blackbird gère-t-il les rate limits ?", "options": ["Délais entre requêtes et retry", "Ignore les limites", "Proxy rotation automatique", "Pas de gestion"], "answer": 0},
            {"question": "Quel outil similaire existe ?", "options": ["Sherlock", "Nmap", "Burp Suite", "Wireshark"], "answer": 0},
            {"question": "Comment exporter les résultats ?", "options": ["Fichier JSON automatique", "Export manuel", "Base de données", "API externe"], "answer": 0},
            {"question": "Quelle catégorie de sites gaming est supportée ?", "options": ["Steam, Xbox, Roblox, Fortnite", "Uniquement PC", "Pas de gaming", "Console uniquement"], "answer": 0},
            {"question": "Comment utiliser Blackbird pour la sécurité d'entreprise ?", "options": ["Audit de présence en ligne des employés", "Hacking de comptes", "Suppression de comptes", "Création de faux profils"], "answer": 0}
        ]
    },
    "Nmap.Strategies": {
        "description": "Scripts NSE pour évasion IDS",
        "questions": [
            {"question": "Que signifie NSE dans Nmap ?", "options": ["Nmap Scripting Engine", "Network Security Engine", "Nmap Scan Extension", "Network Script Executor"], "answer": 0},
            {"question": "Quel langage utilise NSE ?", "options": ["Lua", "Python", "Perl", "Ruby"], "answer": 0},
            {"question": "Quelle option Nmap active la fragmentation ?", "options": ["-f", "-sF", "--fragment", "-F"], "answer": 0},
            {"question": "Quelle technique utilise des adresses IP leurres ?", "options": ["Decoys (-D)", "Spoofing (-S)", "Tunneling (-T)", "Bouncing (-B)"], "answer": 0},
            {"question": "Quel timing Nmap est 'Insane' ?", "options": ["-T5", "-T4", "-T3", "-T6"], "answer": 0},
            {"question": "Comment spécifier un port source ?", "options": ["--source-port ou -g", "--sport", "-p source:", "--from-port"], "answer": 0},
            {"question": "Quelle catégorie de scripts inclut la reconnaissance ?", "options": ["discovery", "recon", "scan", "enum"], "answer": 0},
            {"question": "Comment exécuter tous les scripts d'une catégorie ?", "options": ["--script=category", "-sC category", "--run-scripts category", "--scripts category"], "answer": 0},
            {"question": "Quelle option Nmap effectue un scan SYN ?", "options": ["-sS", "-sT", "-sU", "-sN"], "answer": 0},
            {"question": "Comment scanner en UDP ?", "options": ["-sU", "-U", "--udp", "-sP"], "answer": 0},
            {"question": "Quelle technique utilise le MTU pour fragmenter ?", "options": ["--mtu", "-f --mtu", "--fragment-mtu", "--ip-mtu"], "answer": 0},
            {"question": "Comment éviter le ping avant le scan ?", "options": ["-Pn", "--no-ping", "-P0", "-sP"], "answer": 0},
            {"question": "Quelle option randomise l'ordre des hôtes ?", "options": ["--randomize-hosts", "-r", "--shuffle", "--random"], "answer": 0},
            {"question": "Comment spécifier un fichier de sortie XML ?", "options": ["-oX", "--xml", "-x", "-output-xml"], "answer": 0},
            {"question": "Quelle catégorie NSE inclut le bruteforce ?", "options": ["brute", "attack", "crack", "auth"], "answer": 0},
            {"question": "Comment scanner les 1000 ports les plus courants ?", "options": ["Par défaut (sans option)", "-p1-1000", "--top-ports 1000", "-sV"], "answer": 0},
            {"question": "Quelle option détecte la version des services ?", "options": ["-sV", "-V", "--version", "-v"], "answer": 0},
            {"question": "Comment spécifier une plage de ports ?", "options": ["-p 1-1024", "-ports 1-1024", "--range 1-1024", "-P 1-1024"], "answer": 0},
            {"question": "Quelle option effectue une détection d'OS ?", "options": ["-O", "--os", "-sO", "--detect-os"], "answer": 0},
            {"question": "Comment utiliser un script personnalisé ?", "options": ["--script /path/script.nse", "-sC /path/script", "--custom-script", "--nse /path/script"], "answer": 0},
            {"question": "Quelle technique de scan utilise FIN ?", "options": ["-sF", "-sS", "-sT", "-sN"], "answer": 0},
            {"question": "Comment sauvegarder dans tous les formats ?", "options": ["-oA", "--all-formats", "-o*", "-oXNG"], "answer": 0},
            {"question": "Quelle option active le mode verbose ?", "options": ["-v", "--verbose", "-V", "-d"], "answer": 0},
            {"question": "Comment scanner IPv6 ?", "options": ["-6", "--ipv6", "-v6", "--ip6"], "answer": 0},
            {"question": "Quelle technique utilise des paquets NULL ?", "options": ["-sN", "-sZ", "-s0", "-sE"], "answer": 0},
            {"question": "Comment limiter le nombre de paquets par seconde ?", "options": ["--max-rate", "--rate-limit", "-r", "--pps"], "answer": 0},
            {"question": "Quelle option trace la route vers l'hôte ?", "options": ["--traceroute", "-tr", "--route", "--path"], "answer": 0},
            {"question": "Comment scanner depuis un fichier d'hôtes ?", "options": ["-iL", "--input-list", "-f", "--hosts-file"], "answer": 0},
            {"question": "Quelle catégorie NSE inclut les vulnérabilités ?", "options": ["vuln", "exploit", "security", "cve"], "answer": 0},
            {"question": "Comment exclure des hôtes du scan ?", "options": ["--exclude", "-e", "--skip", "--ignore"], "answer": 0}
        ]
    },
    "Python.Network.Pivot": {
        "description": "Lab de pivot réseau avec Docker",
        "questions": [
            {"question": "Qu'est-ce que le pivoting réseau ?", "options": ["Utiliser une machine compromise pour atteindre d'autres réseaux", "Rotation d'IP", "Load balancing", "DNS tunneling"], "answer": 0},
            {"question": "Combien de machines le lab contient-il ?", "options": ["3 (attacker + 2 victims)", "2", "5", "4"], "answer": 0},
            {"question": "Quelle technologie de conteneurisation est utilisée ?", "options": ["Docker", "LXC", "Podman", "rkt"], "answer": 0},
            {"question": "Quel framework Python est mentionné pour le networking ?", "options": ["Twisted", "Tornado", "aiohttp", "Flask"], "answer": 0},
            {"question": "Qu'est-ce qu'une backdoor dans ce contexte ?", "options": ["Point d'accès persistant sur une machine compromise", "Porte de service", "API cachée", "Vulnérabilité"], "answer": 0},
            {"question": "Comment créer un tunnel SSH pour le pivoting ?", "options": ["ssh -L ou -D pour port forwarding", "ssh tunnel", "ssh --pivot", "ssh -T"], "answer": 0},
            {"question": "Quel type de proxy permet le pivoting via SSH ?", "options": ["SOCKS proxy (-D)", "HTTP proxy", "HTTPS proxy", "FTP proxy"], "answer": 0},
            {"question": "Quelle commande Docker lance les conteneurs ?", "options": ["docker compose up", "docker run all", "docker start", "docker deploy"], "answer": 0},
            {"question": "Comment identifier le réseau interne depuis l'attaquant ?", "options": ["Scanner les routes et interfaces de la machine pivot", "DNS lookup", "WHOIS", "Traceroute internet"], "answer": 0},
            {"question": "Quel outil permet de créer des tunnels TCP ?", "options": ["socat ou netcat", "wget", "curl", "telnet"], "answer": 0},
            {"question": "Qu'est-ce que le double pivoting ?", "options": ["Pivoter à travers deux machines intermédiaires", "Deux connexions simultanées", "Backup de pivot", "Pivot bidirectionnel"], "answer": 0},
            {"question": "Comment Metasploit gère-t-il le pivoting ?", "options": ["route add et autoroute", "pivot module", "meterpreter pivot", "network add"], "answer": 0},
            {"question": "Quel protocole est souvent utilisé pour le tunneling ?", "options": ["SSH, ICMP, DNS", "HTTP uniquement", "FTP", "SMTP"], "answer": 0},
            {"question": "Comment maintenir l'accès après un pivot ?", "options": ["Backdoor persistante", "Session keep-alive", "Cookies", "Tokens"], "answer": 0},
            {"question": "Quelle commande Nmap scanne via un pivot ?", "options": ["Utiliser proxychains + nmap", "nmap --pivot", "nmap -P", "nmap --through"], "answer": 0},
            {"question": "Qu'est-ce que proxychains ?", "options": ["Outil pour router le trafic via SOCKS/HTTP proxy", "Chaîne de proxies", "VPN", "Tor wrapper"], "answer": 0},
            {"question": "Comment configurer proxychains ?", "options": ["/etc/proxychains.conf", "~/.proxychains", "proxychains.ini", "/var/proxychains"], "answer": 0},
            {"question": "Quelle technique masque l'origine de l'attaquant ?", "options": ["Pivot multi-hop", "VPN", "Tor", "Toutes les réponses"], "answer": 3},
            {"question": "Comment transférer des fichiers via un pivot ?", "options": ["scp via tunnel SSH ou HTTP server", "email", "ftp direct", "usb"], "answer": 0},
            {"question": "Quel est l'avantage du lab Docker ?", "options": ["Environnement isolé et reproductible", "Plus rapide", "Plus sécurisé", "Gratuit"], "answer": 0},
            {"question": "Comment identifier les services internes ?", "options": ["Port scanning depuis le pivot", "DNS zone transfer", "SNMP walk", "Toutes les réponses"], "answer": 3},
            {"question": "Qu'est-ce qu'un reverse shell ?", "options": ["La cible initie la connexion vers l'attaquant", "Shell inversé", "Backup shell", "Shell chiffré"], "answer": 0},
            {"question": "Comment Twisted facilite-t-il le pivoting ?", "options": ["Framework async pour serveurs/clients TCP", "GUI", "Parsing", "Logging"], "answer": 0},
            {"question": "Quelle commande netcat crée un listener ?", "options": ["nc -lvp port", "nc -c port", "nc --listen port", "nc -s port"], "answer": 0},
            {"question": "Comment encoder un reverse shell pour éviter la détection ?", "options": ["Base64, XOR, ou obfuscation", "Compression", "Chiffrement AES", "Steganographie"], "answer": 0},
            {"question": "Qu'est-ce que le port forwarding local (-L) ?", "options": ["Exposer un port distant localement", "Exposer un port local à distance", "Tunneling DNS", "NAT traversal"], "answer": 0},
            {"question": "Qu'est-ce que le port forwarding distant (-R) ?", "options": ["Exposer un port local sur la machine distante", "Exposer un port distant", "Reverse tunneling", "Port mirroring"], "answer": 0},
            {"question": "Comment tester la connectivité entre conteneurs ?", "options": ["ping ou curl entre IP internes", "traceroute internet", "DNS lookup", "nslookup"], "answer": 0},
            {"question": "Quel fichier définit les réseaux Docker ?", "options": ["docker-compose.yml", "Dockerfile", "network.conf", "docker.json"], "answer": 0},
            {"question": "Comment nettoyer le lab après utilisation ?", "options": ["docker compose down", "docker clean", "docker rm all", "docker stop"], "answer": 0}
        ]
    }
}

# Ajouter les autres repos avec des questions génériques de sécurité
ADDITIONAL_REPOS = {
    "Tor.Web.Capture": {
        "description": "Capture web anonyme via TOR",
        "questions": [
            {"question": "Quel framework Rust implémente le client Tor ?", "options": ["Arti", "Tor-rs", "Rust-Tor", "TorLib"], "answer": 0},
            {"question": "Quel navigateur headless est utilisé pour les captures ?", "options": ["Chrome/Chromium", "Firefox", "Safari", "Edge"], "answer": 0},
            {"question": "Qu'est-ce qu'une capture headless ?", "options": ["Screenshot sans interface graphique", "Capture audio", "Capture réseau", "Capture mémoire"], "answer": 0},
            {"question": "Comment Tor assure-t-il l'anonymat ?", "options": ["Routage en oignon multi-hop", "VPN", "Proxy simple", "DNS over HTTPS"], "answer": 0},
            {"question": "Quel format d'archive est utilisé pour le HTML ?", "options": ["MHTML ou HTML complet", "PDF", "WARC", "ZIP"], "answer": 0},
            {"question": "Pourquoi utiliser Tor pour la capture web ?", "options": ["Anonymat de l'opérateur", "Vitesse", "Qualité d'image", "Compression"], "answer": 0},
            {"question": "Qu'est-ce qu'un nœud de sortie Tor ?", "options": ["Dernier relais avant la destination", "Premier relais", "Relais du milieu", "Serveur DNS"], "answer": 0},
            {"question": "Comment vérifier que le trafic passe par Tor ?", "options": ["check.torproject.org", "whatismyip.com", "ipinfo.io", "Toutes les réponses"], "answer": 0},
            {"question": "Quel protocole Tor utilise-t-il principalement ?", "options": ["TCP", "UDP", "ICMP", "SCTP"], "answer": 0},
            {"question": "Comment automatiser les captures en batch ?", "options": ["Script avec boucle sur URLs", "Cron job", "API REST", "Toutes les réponses"], "answer": 3},
            {"question": "Quel avantage offre Arti sur le C Tor ?", "options": ["Écrit en Rust (memory safety)", "Plus rapide", "Plus de fonctionnalités", "Compatible Windows"], "answer": 0},
            {"question": "Comment gérer les timeouts sur Tor ?", "options": ["Timeouts plus longs car latence réseau", "Ignorer", "Retry immédiat", "Réduire les timeouts"], "answer": 0},
            {"question": "Quel format de screenshot est généralement utilisé ?", "options": ["PNG", "JPEG", "BMP", "GIF"], "answer": 0},
            {"question": "Comment capturer une page complète (pas seulement le viewport) ?", "options": ["fullPage: true dans Puppeteer/Playwright", "scroll + capture", "Zoom out", "PDF export"], "answer": 0},
            {"question": "Qu'est-ce que le fingerprinting navigateur ?", "options": ["Identification unique via caractéristiques browser", "Empreinte digitale", "Biométrie", "Captcha"], "answer": 0},
            {"question": "Comment réduire le fingerprinting ?", "options": ["Tor Browser avec configs standards", "Mode incognito", "VPN", "Proxy"], "answer": 0},
            {"question": "Quel header révèle le navigateur utilisé ?", "options": ["User-Agent", "Accept", "Host", "Referer"], "answer": 0},
            {"question": "Comment archiver les ressources externes d'une page ?", "options": ["Télécharger CSS, JS, images et sauvegarder localement", "Screenshot seulement", "PDF", "Print"], "answer": 0},
            {"question": "Qu'est-ce que le DOM ?", "options": ["Document Object Model - structure de la page", "Data Object Model", "Direct Object Mapping", "Document Order Model"], "answer": 0},
            {"question": "Comment attendre le chargement complet d'une page ?", "options": ["waitUntil: 'networkidle'", "sleep()", "onload event", "DOMContentLoaded"], "answer": 0},
            {"question": "Quel format préserve les liens hypertextes ?", "options": ["HTML/MHTML", "PNG", "JPEG", "PDF (partiellement)"], "answer": 0},
            {"question": "Comment gérer les sites avec JavaScript ?", "options": ["Headless browser exécute JS", "curl suffit", "wget suffit", "Pas de JS support"], "answer": 0},
            {"question": "Qu'est-ce que Puppeteer ?", "options": ["Bibliothèque Node.js pour contrôler Chrome", "Framework web", "ORM", "Testing tool"], "answer": 0},
            {"question": "Comment gérer les CAPTCHAs ?", "options": ["Services de résolution ou intervention manuelle", "Ignorer", "Bypass automatique", "Toujours bloqué"], "answer": 0},
            {"question": "Quel est l'intérêt de l'archivage web ?", "options": ["Preuve légale, recherche, backup", "SEO", "Performance", "Accessibilité"], "answer": 0},
            {"question": "Comment compresser les captures ?", "options": ["ZIP ou tar.gz des fichiers", "JPEG quality", "PNG optimization", "Toutes les réponses"], "answer": 3},
            {"question": "Qu'est-ce que la Wayback Machine ?", "options": ["Archive web d'Internet Archive", "Time machine", "Backup service", "CDN"], "answer": 0},
            {"question": "Comment respecter robots.txt lors de captures ?", "options": ["Parser et respecter les directives", "Ignorer toujours", "Bloquer le scraping", "Demander permission"], "answer": 0},
            {"question": "Quel outil ligne de commande capture des screenshots ?", "options": ["Puppeteer CLI ou Playwright CLI", "curl", "wget", "lynx"], "answer": 0},
            {"question": "Comment horodater les captures ?", "options": ["Inclure timestamp dans nom de fichier ou métadonnées", "Fichier séparé", "Base de données", "Log file"], "answer": 0}
        ]
    },
    "PHP.WordPress.Cypher": {
        "description": "Utilitaires de chiffrement pour WordPress",
        "questions": [
            {"question": "Quel algorithme de hachage WordPress utilise par défaut ?", "options": ["bcrypt (via phpass)", "MD5", "SHA1", "SHA256"], "answer": 0},
            {"question": "Qu'est-ce que phpass ?", "options": ["Bibliothèque de hachage de mots de passe PHP", "Framework PHP", "Plugin WordPress", "Extension MySQL"], "answer": 0},
            {"question": "Comment vérifier un mot de passe WordPress ?", "options": ["wp_check_password()", "password_verify()", "check_pass()", "verify_password()"], "answer": 0},
            {"question": "Quelle fonction WordPress hashe un mot de passe ?", "options": ["wp_hash_password()", "password_hash()", "hash_password()", "wp_encrypt()"], "answer": 0},
            {"question": "Quel préfixe indique un hash bcrypt ?", "options": ["$2y$ ou $2a$", "$5$", "$6$", "$1$"], "answer": 0},
            {"question": "Qu'est-ce que le salt en cryptographie ?", "options": ["Valeur aléatoire ajoutée avant hachage", "Algorithme de chiffrement", "Clé de chiffrement", "Mode de chiffrement"], "answer": 0},
            {"question": "Où WordPress stocke-t-il les clés de chiffrement ?", "options": ["wp-config.php", "database", ".htaccess", "wp-content/"], "answer": 0},
            {"question": "Quelle constante contient la clé AUTH ?", "options": ["AUTH_KEY", "SECRET_KEY", "SECURE_KEY", "WP_KEY"], "answer": 0},
            {"question": "Comment générer des clés WordPress sécurisées ?", "options": ["api.wordpress.org/secret-key/", "openssl rand", "random_bytes()", "Toutes les réponses"], "answer": 0},
            {"question": "Quel algorithme symétrique est courant en PHP ?", "options": ["AES-256", "DES", "RC4", "Blowfish"], "answer": 0},
            {"question": "Quelle extension PHP gère le chiffrement moderne ?", "options": ["OpenSSL ou Sodium", "mcrypt", "crypt", "hash"], "answer": 0},
            {"question": "Comment chiffrer avec OpenSSL en PHP ?", "options": ["openssl_encrypt()", "encrypt()", "ssl_encrypt()", "cipher()"], "answer": 0},
            {"question": "Quel mode de chiffrement est recommandé ?", "options": ["GCM ou CBC avec HMAC", "ECB", "CFB seul", "OFB seul"], "answer": 0},
            {"question": "Qu'est-ce que l'IV (Initialization Vector) ?", "options": ["Valeur aléatoire pour le premier bloc", "Vecteur d'intégrité", "Identifiant de version", "Index vectoriel"], "answer": 0},
            {"question": "Comment stocker l'IV avec les données chiffrées ?", "options": ["Préfixer les données chiffrées avec l'IV", "Fichier séparé", "Base de données séparée", "Header HTTP"], "answer": 0},
            {"question": "Quelle fonction PHP génère des octets aléatoires ?", "options": ["random_bytes()", "rand()", "mt_rand()", "openssl_random()"], "answer": 0},
            {"question": "Comment sécuriser les cookies WordPress ?", "options": ["LOGGED_IN_KEY + LOGGED_IN_SALT", "md5() simple", "base64_encode()", "serialize()"], "answer": 0},
            {"question": "Qu'est-ce que le HMAC ?", "options": ["Hash-based Message Authentication Code", "Hybrid MAC", "HTTP MAC", "Hash MAC"], "answer": 0},
            {"question": "Quelle fonction calcule un HMAC en PHP ?", "options": ["hash_hmac()", "hmac()", "compute_hmac()", "mac()"], "answer": 0},
            {"question": "Comment valider l'intégrité des données chiffrées ?", "options": ["HMAC ou mode authentifié (GCM)", "Checksum MD5", "CRC32", "Taille du fichier"], "answer": 0},
            {"question": "Quelle attaque cible les implémentations crypto faibles ?", "options": ["Timing attack, padding oracle", "SQL injection", "XSS", "CSRF"], "answer": 0},
            {"question": "Comment comparer des hashes de manière sécurisée ?", "options": ["hash_equals()", "== ou ===", "strcmp()", "compare()"], "answer": 0},
            {"question": "Qu'est-ce que libsodium ?", "options": ["Bibliothèque crypto moderne (NaCl)", "Plugin WordPress", "Extension PHP", "Framework"], "answer": 0},
            {"question": "Quelle fonction sodium chiffre des données ?", "options": ["sodium_crypto_secretbox()", "sodium_encrypt()", "sodium_cipher()", "sodium_seal()"], "answer": 0},
            {"question": "Comment migrer de MD5 vers bcrypt pour les passwords ?", "options": ["Re-hasher à la prochaine connexion", "Convertir directement", "Double hash", "Impossible"], "answer": 0},
            {"question": "Quel cost factor bcrypt est recommandé ?", "options": ["10-12 (ajuster selon performance)", "5", "20", "1"], "answer": 0},
            {"question": "Comment protéger wp-config.php ?", "options": ["Permissions 400 et/ou hors webroot", "chmod 777", "Laisser par défaut", "Chiffrer le fichier"], "answer": 0},
            {"question": "Qu'est-ce que le key stretching ?", "options": ["Rendre le hash plus coûteux à calculer", "Allonger la clé", "Compresser la clé", "Diviser la clé"], "answer": 0},
            {"question": "Comment WordPress protège-t-il les nonces ?", "options": ["wp_create_nonce() avec timestamp", "Session ID", "Cookie", "IP"], "answer": 0},
            {"question": "Quelle durée de vie ont les nonces WordPress ?", "options": ["24 heures par défaut", "1 heure", "Session", "Permanent"], "answer": 0}
        ]
    }
}

# Fusionner les QCM
QCM_DATA.update(ADDITIONAL_REPOS)

# Template HTML pour les pages QCM
QCM_HTML_TEMPLATE = '''---
layout: qcm
title: "QCM - {repo_name}"
repo_name: "{repo_name}"
description: "{description}"
readme_url: "../"
generated_at: "{timestamp}"
questions: {questions_json}
---
'''

def generate_qcm_pages():
    """Génère les pages QCM pour chaque repo"""

    for repo_name, data in QCM_DATA.items():
        repo_dir = os.path.join(REPOS_DIR, repo_name, "qcm")
        os.makedirs(repo_dir, exist_ok=True)

        # Générer le fichier index.html pour le QCM
        qcm_file = os.path.join(repo_dir, "index.html")

        questions_json = json.dumps(data["questions"], ensure_ascii=False, indent=2)

        content = QCM_HTML_TEMPLATE.format(
            repo_name=repo_name,
            description=data["description"],
            timestamp=TIMESTAMP,
            questions_json=questions_json
        )

        with open(qcm_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ QCM généré: {repo_name}")

    print(f"\n=== {len(QCM_DATA)} QCM générés ===")

if __name__ == "__main__":
    generate_qcm_pages()
