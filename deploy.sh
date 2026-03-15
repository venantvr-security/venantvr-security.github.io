#!/bin/bash
# Script de déploiement vers GitHub Pages

ORG="venantvr-security"
REPO="venantvr-security.github.io"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Déploiement vers GitHub Pages ===${NC}"

# Vérifier si le repo existe
if ! gh repo view "$ORG/$REPO" &>/dev/null; then
    echo -e "${BLUE}Création du repo $ORG/$REPO...${NC}"
    gh repo create "$ORG/$REPO" --public --description "Documentation et QCM pour les outils de sécurité"
fi

# Cloner ou mettre à jour
DEPLOY_DIR="$BASE_DIR/deploy_temp"
rm -rf "$DEPLOY_DIR"

echo -e "${BLUE}Clonage du repo de déploiement...${NC}"
git clone "https://github.com/$ORG/$REPO.git" "$DEPLOY_DIR" 2>/dev/null || mkdir -p "$DEPLOY_DIR"

# Copier les fichiers
echo -e "${BLUE}Copie des fichiers...${NC}"
cp -r "$BASE_DIR/_config.yml" "$DEPLOY_DIR/"
cp -r "$BASE_DIR/_layouts" "$DEPLOY_DIR/"
cp -r "$BASE_DIR/assets" "$DEPLOY_DIR/"
cp -r "$BASE_DIR/repos" "$DEPLOY_DIR/"
cp -r "$BASE_DIR/index.md" "$DEPLOY_DIR/"
cp -r "$BASE_DIR/Gemfile" "$DEPLOY_DIR/"

# Git setup
cd "$DEPLOY_DIR"
git init 2>/dev/null
git checkout -b main 2>/dev/null || git checkout main

# Commit et push
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
git add -A
git commit -m "Update site - $TIMESTAMP

- 30 repos documentés
- 30 QCM (30 questions chacun)
- Horodatage: $TIMESTAMP

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$ORG/$REPO.git"
git push -u origin main --force

echo -e "${GREEN}=== Déploiement terminé ===${NC}"
echo "URL: https://$ORG.github.io/"
echo ""
echo "Structure des URLs:"
echo "  - Accueil: https://$ORG.github.io/"
echo "  - Repo: https://$ORG.github.io/repos/REPO_NAME/"
echo "  - QCM: https://$ORG.github.io/repos/REPO_NAME/qcm/"

# Cleanup
rm -rf "$DEPLOY_DIR"
