#!/bin/bash
# Script de génération du site GitHub Pages pour venantvr-security
# Avec horodatage pour faciliter les mises à jour

ORG="venantvr-security"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
REPOS_DIR="$BASE_DIR/repos"
TEMP_DIR="$BASE_DIR/temp_repos"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DATE_ISO=$(date '+%Y-%m-%d')

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Génération du site GitHub Pages pour $ORG ===${NC}"
echo -e "${BLUE}Horodatage: $TIMESTAMP${NC}"

# Créer les répertoires
mkdir -p "$REPOS_DIR" "$TEMP_DIR"

# Liste des repos (format: name|description)
REPOS=$(gh repo list "$ORG" --limit 100 --json name,description -q '.[] | "\(.name)|\(.description // "No description")"')

COUNT=0
TOTAL=$(echo "$REPOS" | wc -l)

while IFS='|' read -r REPO_NAME REPO_DESC; do
    # Ignorer .github et les lignes vides
    if [[ -z "$REPO_NAME" || "$REPO_NAME" == ".github" ]]; then
        continue
    fi

    COUNT=$((COUNT + 1))
    echo -e "${GREEN}[$COUNT/$TOTAL] Processing: $REPO_NAME${NC}"

    # Créer le dossier pour ce repo
    mkdir -p "$REPOS_DIR/$REPO_NAME/qcm"

    # Cloner le repo (shallow)
    CLONE_DIR="$TEMP_DIR/$REPO_NAME"
    if [[ ! -d "$CLONE_DIR" ]]; then
        git clone --depth 1 "https://github.com/$ORG/$REPO_NAME.git" "$CLONE_DIR" 2>/dev/null
    fi

    # Récupérer le dernier commit du repo
    LAST_COMMIT=""
    if [[ -d "$CLONE_DIR/.git" ]]; then
        LAST_COMMIT=$(cd "$CLONE_DIR" && git log -1 --format="%h - %s (%ci)" 2>/dev/null)
    fi

    # Copier le README
    if [[ -f "$CLONE_DIR/README.md" ]]; then
        # Créer la page index avec front matter et horodatage
        cat > "$REPOS_DIR/$REPO_NAME/index.md" <<EOFREADME
---
layout: default
title: "$REPO_NAME"
description: "$REPO_DESC"
generated_at: "$TIMESTAMP"
last_update: "$DATE_ISO"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>$REPO_NAME</span>
</div>

<div class="page-header">
  <h1>$REPO_NAME</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/$ORG/$REPO_NAME" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

<div class="page-meta">
  <small>
    <strong>Page générée le:</strong> $TIMESTAMP |
    <strong>Dernier commit:</strong> $LAST_COMMIT
  </small>
</div>

---

EOFREADME
        # Append README content
        cat "$CLONE_DIR/README.md" >> "$REPOS_DIR/$REPO_NAME/index.md"

        echo "  ✓ README copié"
    else
        # Créer une page basique si pas de README
        cat > "$REPOS_DIR/$REPO_NAME/index.md" <<EOFNOREADME
---
layout: default
title: "$REPO_NAME"
description: "$REPO_DESC"
generated_at: "$TIMESTAMP"
last_update: "$DATE_ISO"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>$REPO_NAME</span>
</div>

<div class="page-meta">
  <small><strong>Page générée le:</strong> $TIMESTAMP</small>
</div>

# $REPO_NAME

$REPO_DESC

Ce repository n'a pas de README disponible.

[Voir sur GitHub](https://github.com/$ORG/$REPO_NAME)
EOFNOREADME
        echo "  ⚠ Pas de README trouvé"
    fi

done <<< "$REPOS"

# Créer un fichier de manifest pour le suivi des mises à jour
cat > "$BASE_DIR/manifest.json" <<MANIFEST
{
  "organization": "$ORG",
  "generated_at": "$TIMESTAMP",
  "total_repos": $COUNT,
  "repos": [
$(gh repo list "$ORG" --limit 100 --json name,description,updatedAt -q '.[] | select(.name != ".github") | "    {\"name\": \"\(.name)\", \"description\": \"\(.description // \"\")\", \"updated_at\": \"\(.updatedAt)\"}"' | paste -sd ',\n')
  ]
}
MANIFEST

echo -e "${GREEN}=== Terminé ! ===${NC}"
echo "Les fichiers ont été générés dans: $REPOS_DIR"
echo "Manifest créé: $BASE_DIR/manifest.json"
echo "Horodatage: $TIMESTAMP"
