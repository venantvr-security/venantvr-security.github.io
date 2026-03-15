---
layout: default
title: "PHP.WordPress.Cypher"
description: "Utilitaires de Chiffrement et Hachage pour WordPress"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>PHP.WordPress.Cypher</span>
</div>

<div class="page-header">
  <h1>PHP.WordPress.Cypher</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/PHP.WordPress.Cypher" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Utilitaires de Chiffrement et Hachage pour WordPress

## Introduction : La Sécurité des Mots de Passe WordPress

WordPress propulse plus de 40% des sites web dans le monde. Cette popularité en fait une cible privilégiée des attaquants, et la sécurité des mots de passe est souvent le maillon faible. Comprendre comment WordPress stocke et vérifie les mots de passe est essentiel pour tout auditeur de sécurité.

Ce projet documente les mécanismes cryptographiques utilisés par WordPress et fournit des outils pour les auditer. Vous y trouverez une explication des algorithmes de hachage, des scripts de vérification, et des recommandations pour renforcer la sécurité.

### Ce que ce projet permet de faire

| Fonctionnalité | Description |
|----------------|-------------|
| **Comprendre** | Les mécanismes de hachage PHPass et bcrypt |
| **Auditer** | Détecter les anciens hachages MD5 vulnérables |
| **Vérifier** | Tester la solidité des mots de passe |
| **Migrer** | Mettre à niveau vers des algorithmes plus sûrs |

### Évolution historique des hachages

WordPress a fait évoluer ses méthodes de hachage au fil du temps :

| Époque | Algorithme | Sécurité actuelle |
|--------|------------|-------------------|
| **Avant 2008** | MD5 simple | 🔴 Critique (cassable en secondes) |
| **2008-2020** | PHPass ($P$) | 🟠 Acceptable (mais dépassé) |
| **Moderne** | bcrypt ($2y$) | 🟢 Fort (recommandé) |


## Architecture du Hachage WordPress

Pour comprendre comment WordPress sécurise les mots de passe, suivons le parcours d'un mot de passe depuis sa saisie jusqu'à son stockage en base de données. Le diagramme ci-dessous illustre ce processus.

<div class="mermaid">
flowchart TB
    subgraph INPUT["📝 Saisie Utilisateur"]
        PWD["Mot de passe<br/><i>ex: MonSecret123!</i>"]
    end

    subgraph WP["⚙️ Couche WordPress"]
        PHPASS["Bibliothèque PHPass<br/><i>Portable PHP Password Hashing</i>"]
        SALT["Génération du sel<br/><i>8-22 caractères aléatoires</i>"]
        ITER["Itérations<br/><i>8192 tours par défaut</i>"]
    end

    subgraph ALGO["🔐 Algorithme"]
        BCRYPT["bcrypt (moderne)<br/><i>Coût adaptatif</i>"]
        MD5["MD5 itéré (legacy)<br/><i>Moins sécurisé</i>"]
    end

    subgraph HASH["📦 Format du Hash"]
        H1["$P$B... (Portable Hash)<br/><i>34 caractères</i>"]
        H2["$2y$10$... (bcrypt)<br/><i>60 caractères</i>"]
    end

    subgraph DB["💾 Base de Données"]
        STORED["wp_users.user_pass<br/><i>Stockage sécurisé</i>"]
    end

    PWD --> PHPASS
    PHPASS --> SALT
    SALT --> ITER
    ITER --> BCRYPT & MD5
    BCRYPT --> H2
    MD5 --> H1
    H1 & H2 --> STORED

    style PWD fill:#3498db,fill-opacity:0.15
    style PHPASS fill:#9b59b6,fill-opacity:0.15
    style BCRYPT fill:#2ecc71,fill-opacity:0.15
    style MD5 fill:#e74c3c,fill-opacity:0.15
    style STORED fill:#f39c12,fill-opacity:0.15
    style DB fill:#808080,fill-opacity:0.15
    style HASH fill:#808080,fill-opacity:0.15
    style ALGO fill:#808080,fill-opacity:0.15
    style WP fill:#808080,fill-opacity:0.15
    style INPUT fill:#808080,fill-opacity:0.15
</div>


## Anatomie des Formats de Hachage

Chaque type de hash a une structure spécifique. Savoir les reconnaître permet d'identifier rapidement le niveau de sécurité d'une installation WordPress. Le diagramme suivant décompose les deux formats principaux.

<div class="mermaid">
flowchart LR
    subgraph Portable["Format PHPass (Portable Hash)"]
        P1["$P$<br/><i>Identifiant</i>"]
        P2["B<br/><i>Indicateur itérations<br/>(8192 tours)</i>"]
        P3["xxxxxxxx<br/><i>Sel (8 chars)</i>"]
        P4["xxxxxxxxxxxxxxxxxxxxx<br/><i>Hash (22 chars)</i>"]
    end

    subgraph Bcrypt["Format bcrypt (Moderne)"]
        B1["$2y$<br/><i>Identifiant</i>"]
        B2["10<br/><i>Coût (2^10 tours)</i>"]
        B3["xxxxxxxxxxxxxxxxxxxxxx<br/><i>Sel (22 chars)</i>"]
        B4["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/><i>Hash (31 chars)</i>"]
    end

    P1 --> P2 --> P3 --> P4
    B1 --> B2 --> B3 --> B4

    style P1 fill:#e74c3c,fill-opacity:0.15
    style B1 fill:#2ecc71,fill-opacity:0.15
    style Bcrypt fill:#808080,fill-opacity:0.15
    style Portable fill:#808080,fill-opacity:0.15
</div>

### Tableau comparatif des formats

| Format | Préfixe | Algorithme | Longueur | Sécurité |
|--------|---------|------------|----------|----------|
| **PHPass Portable** | `$P$` | MD5 itéré | 34 chars | 🟠 Moyen |
| **Bcrypt** | `$2y$` | bcrypt | 60 chars | 🟢 Fort |
| **MD5 simple** | (aucun) | MD5 | 32 chars | 🔴 Critique |


## Processus de Vérification

Lorsqu'un utilisateur se connecte, WordPress doit vérifier que le mot de passe saisi correspond au hash stocké. Ce processus est illustré ci-dessous.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant U as 👤 Utilisateur
    participant WP as ⚙️ WordPress
    participant DB as 💾 Database

    Note over U,DB: Tentative de connexion
    U->>WP: Login (username, password)
    WP->>DB: SELECT user_pass FROM wp_users WHERE user_login = ?
    DB-->>WP: Hash stocké ($P$BxxxxHash...)

    Note over WP: WordPress extrait le sel et l'algorithme du hash
    WP->>WP: wp_check_password(password_saisi, hash_stocké)
    WP->>WP: Recalcule le hash avec le même sel

    alt Les hashes correspondent
        WP-->>U: ✅ Connexion réussie
        Note over WP: Session créée
    else Les hashes différent
        WP-->>U: ❌ Mot de passe incorrect
        Note over WP: Tentative loggée
    end
</div>

### Point important sur la vérification

Le mot de passe en clair n'est **jamais** stocké. WordPress stocke uniquement le hash, et lors de la vérification, il recalcule le hash du mot de passe saisi pour le comparer au hash stocké. C'est une opération à sens unique.


## Fonctions PHP WordPress

Voici les principales fonctions utilisées par WordPress pour gérer les mots de passe.

```php
<?php
/**
 * Génération d'un hash WordPress
 * Cette fonction choisit automatiquement le meilleur algorithme disponible
 */
$hash = wp_hash_password('mon_mot_de_passé_secret');
// Résultat typique: $P$BDkPFe... (34 caractères)

/**
 * Vérification d'un mot de passe
 * Compare le mot de passe saisi au hash stocké en base
 *
 * @param string $password     Le mot de passe à vérifier
 * @param string $hash         Le hash stocké en base de données
 * @param int    $user_id      L'ID de l'utilisateur (optionnel)
 * @return bool                True si le mot de passe est correct
 */
$is_valid = wp_check_password(
    'mot_de_passé_saisi',
    $hash_stocke,
    $user_id
);

if ($is_valid) {
    echo "Mot de passe correct !";
} else {
    echo "Mot de passe incorrect.";
}

/**
 * Utilisation directe de PHPass (pour comprendre le mécanisme)
 */
require_once ABSPATH . 'wp-includes/class-phpass.php';

// Paramètres: 8 = log2(iterations), true = portable
$hasher = new PasswordHash(8, true);

// Créer un hash
$hash = $hasher->HashPassword('password');

// Vérifier un hash
$valid = $hasher->CheckPassword('password', $hash);
```


## Script d'Audit de Sécurité

Ce script permet d'analyser la base de données WordPress pour identifier les comptes utilisant des algorithmes de hachage obsolètes.

```php
<?php
/**
 * Audit des hachages de mots de passe WordPress
 *
 * Ce script analyse tous les comptes utilisateurs et identifie
 * ceux qui utilisent des algorithmes de hachage obsolètes.
 *
 * USAGE: Exécuter depuis le répertoire WordPress
 *        php audit_passwords.php
 */

// Charger WordPress
require_once 'wp-load.php';

global $wpdb;

/**
 * Analyse les hachages de tous les utilisateurs
 * et génère un rapport de sécurité
 */
function audit_password_hashes($wpdb) {
    // Récupérer tous les utilisateurs
    $users = $wpdb->get_results(
        "SELECT ID, user_login, user_pass, user_email FROM {$wpdb->users}"
    );

    // Compteurs pour le rapport
    $stats = [
        'md5' => 0,
        'phpass' => 0,
        'bcrypt' => 0,
        'unknown' => 0
    ];

    echo "=== AUDIT DES MOTS DE PASSE WORDPRESS ===\n\n";

    foreach ($users as $user) {
        $hash = $user->user_pass;

        // Détecter le type de hash
        if (strlen($hash) == 32 && ctype_xdigit($hash)) {
            // Hash MD5 simple (32 caractères hexadécimaux)
            echo "🔴 CRITIQUE - MD5 simple: {$user->user_login}\n";
            echo "   Email: {$user->user_email}\n";
            echo "   Action: Forcer le changement de mot de passe\n\n";
            $stats['md5']++;

        } elseif (strpos($hash, '$P$') === 0) {
            // Hash PHPass (acceptable mais à surveiller)
            echo "🟠 MOYEN - PHPass: {$user->user_login}\n";
            $stats['phpass']++;

        } elseif (strpos($hash, '$2y$') === 0 || strpos($hash, '$2a$') === 0) {
            // Hash bcrypt (sécurisé)
            echo "✅ FORT - Bcrypt: {$user->user_login}\n";
            $stats['bcrypt']++;

        } else {
            // Format inconnu
            echo "❓ INCONNU: {$user->user_login}\n";
            echo "   Hash: " . substr($hash, 0, 10) . "...\n";
            $stats['unknown']++;
        }
    }

    // Rapport final
    echo "\n=== RÉSUMÉ ===\n";
    echo "MD5 (critique):  {$stats['md5']}\n";
    echo "PHPass (moyen):  {$stats['phpass']}\n";
    echo "Bcrypt (fort):   {$stats['bcrypt']}\n";
    echo "Inconnu:         {$stats['unknown']}\n";

    return $stats;
}

// Exécuter l'audit
audit_password_hashes($wpdb);
```


## Recommandations de Sécurité

Après avoir compris le fonctionnement et audité votre installation, voici les actions recommandées :

### Actions immédiates

| Priorité | Action | Impact |
|----------|--------|--------|
| 🔴 **Critique** | Forcer le changement des mots de passe MD5 | Élimine la vulnérabilité majeure |
| 🟠 **Haute** | Activer bcrypt si disponible | Renforce tous les nouveaux hashes |
| 🟡 **Moyenne** | Implémenter une politique de mots de passe | Prévient les mots de passe faibles |

### Migration vers bcrypt

Pour forcer l'utilisation de bcrypt sur les nouvelles installations :

```php
<?php
// Dans wp-config.php ou un plugin personnalisé

// Forcer l'utilisation de password_hash() natif PHP
add_filter('wp_hash_password_options', function($options) {
    return [
        'cost' => 12,  // Augmenter le coût pour plus de sécurité
    ];
});
```


## Pour Aller Plus Loin

La sécurité des mots de passe est un domaine vaste. Voici des ressources pour approfondir :

- 📚 [WordPress Password Hashing](https://developer.wordpress.org/reference/functions/wp_hash_password/) - Documentation officielle
- 🔐 [PHPass Library](https://www.openwall.com/phpass/) - La bibliothèque utilisée par WordPress
- 🛡️ [PHP password_hash()](https://www.php.net/manual/en/function.password-hash.php) - Fonction native PHP moderne
- 📖 [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) - Meilleures pratiques


## Exploits et Vulnérabilités Connues

- **CVE-2023-2745** : Vulnérabilité de traversée de répertoire dans WordPress permettant à un attaquant non authentifié d'accéder à des fichiers arbitraires, potentiellement exposant wp-config.php et les secrets cryptographiques.

- **CVE-2021-44223** : Faille dans le mécanisme de réinitialisation de mot de passe WordPress. Un attaquant pouvait exploiter une condition de concurrence pour intercepter les tokens de réinitialisation.

- **CVE-2019-8943** : Path Traversal dans WordPress permettant la lecture de fichiers sensibles via le crop d'images. Cette faille pouvait exposer les clés de hachage stockées dans wp-config.php.

- **CVE-2017-5487** : Fuite d'informations utilisateur via l'API REST WordPress. Les noms d'utilisateurs pouvaient être énumérés, facilitant les attaques par bruteforce sur les mots de passe.

- **CVE-2012-3414 (PHPass)** : Vulnérabilité dans certaines implémentations de PHPass où le générateur de nombres aléatoires était prévisible, affaiblissant la génération des sels cryptographiques.


## Approfondissement Théorique

L'évolution des algorithmes de hachage de mots de passe reflète la course permanente entre puissance de calcul et sécurité cryptographique. MD5, conçu en 1991, était considéré sûr jusqu'aux années 2000. Aujourd'hui, des attaques par tables arc-en-ciel ou GPU permettent de casser des milliards de hashes MD5 par seconde. PHPass a introduit le concept de "key stretching" avec des milliers d'itérations, mais reste basé sur MD5. Bcrypt, développé en 1999, utilise un algorithme Blowfish modifié avec un coût adaptatif : le paramètre "cost" peut être augmenté au fil du temps pour maintenir la sécurité face à l'évolution du matériel.

Les recommandations OWASP pour le stockage des mots de passe ont considérablement évolué. Le document ASVS (Application Security Verification Standard) niveau 2 exige désormais l'utilisation de fonctions de dérivation de clé adaptatives (bcrypt, scrypt, Argon2). La recommandation actuelle est d'utiliser Argon2id avec des paramètres mémoire et temps ajustés pour que le hachage prenne au minimum 1 seconde sur le serveur de production. WordPress n'a pas encore adopté Argon2 par défaut, mais des plugins comme "WP Password Argon Two" permettent cette migration.

La protection des mots de passe ne se limite pas au hachage. Une défense en profondeur inclut : limitation du nombre de tentatives de connexion (protection anti-bruteforce), authentification multi-facteurs (2FA), détection des mots de passe compromis via les bases Have I Been Pwned, et rotation régulière des clés de hachage WordPress (AUTH_KEY, SECURE_AUTH_KEY, etc.) stockées dans wp-config.php.


---

