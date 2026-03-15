#!/usr/bin/env python3
"""
Corrige les QCM pour randomiser la position des bonnes réponses
"""

import os
import random
import json
import re
from datetime import datetime

REPOS_DIR = "repos"

def shuffle_question(question_data):
    """Mélange les options et met à jour l'index de la bonne réponse"""
    options = list(question_data["options"])
    correct_answer = options[question_data["answer"]]

    # Mélanger les options
    random.shuffle(options)

    # Trouver le nouvel index de la bonne réponse
    new_answer_idx = options.index(correct_answer)

    return {
        "question": question_data["question"],
        "options": options,
        "answer": new_answer_idx
    }

def extract_json_array(content, start_pos):
    """Extrait un tableau JSON en comptant les crochets"""
    bracket_count = 0
    in_string = False
    escape_next = False
    json_end = -1

    for i, char in enumerate(content[start_pos:], start=start_pos):
        if escape_next:
            escape_next = False
            continue
        if char == '\\':
            escape_next = True
            continue
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
            if bracket_count == 0:
                json_end = i + 1
                break

    return json_end

def process_qcm_file(filepath, repo_name):
    """Recrée complètement le fichier QCM avec des réponses randomisées"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraire la description
    desc_match = re.search(r'description:\s*"([^"]*)"', content)
    description = desc_match.group(1) if desc_match else "Quiz technique"

    # Trouver le début du JSON questions
    start_marker = 'questions: ['
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print(f"  ⚠ Marker non trouvé: {filepath}")
        return False

    json_start = start_idx + len('questions: ')
    json_end = extract_json_array(content, json_start)

    if json_end == -1:
        print(f"  ⚠ Fin du JSON non trouvée: {filepath}")
        return False

    json_str = content[json_start:json_end]

    try:
        questions = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"  ⚠ Erreur JSON: {filepath} - {e}")
        return False

    # Prendre seulement les 30 premières questions
    questions = questions[:30]

    # Randomiser chaque question
    shuffled_questions = [shuffle_question(q) for q in questions]

    # Vérifier la distribution des réponses
    answer_dist = {}
    for q in shuffled_questions:
        idx = q["answer"]
        answer_dist[idx] = answer_dist.get(idx, 0) + 1

    # Recréer le fichier entièrement
    new_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_questions_json = json.dumps(shuffled_questions, ensure_ascii=False, indent=2)

    new_content = f'''---
layout: qcm
title: "QCM - {repo_name}"
repo_name: "{repo_name}"
description: "{description}"
readme_url: "../"
generated_at: "{new_timestamp}"
questions: {new_questions_json}
---
'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✓ {repo_name} - Distribution: {dict(sorted(answer_dist.items()))}")
    return True

def main():
    print("=== Randomisation des réponses QCM ===\n")

    random.seed()

    count = 0
    for repo_name in sorted(os.listdir(REPOS_DIR)):
        qcm_path = os.path.join(REPOS_DIR, repo_name, "qcm", "index.html")
        if os.path.exists(qcm_path):
            count += 1
            print(f"[{count}/30] {repo_name}")
            process_qcm_file(qcm_path, repo_name)

    print(f"\n=== {count} QCM traités ===")

    # Vérification finale
    print("\n=== Vérification distribution globale ===")
    total_dist = {0: 0, 1: 0, 2: 0, 3: 0}
    for repo_name in os.listdir(REPOS_DIR):
        qcm_path = os.path.join(REPOS_DIR, repo_name, "qcm", "index.html")
        if os.path.exists(qcm_path):
            with open(qcm_path, 'r', encoding='utf-8') as f:
                content = f.read()
            answers = re.findall(r'"answer":\s*(\d)', content)
            for a in answers:
                total_dist[int(a)] += 1

    total = sum(total_dist.values())
    print(f"Total: {total} réponses")
    for i in range(4):
        pct = total_dist[i] / total * 100 if total > 0 else 0
        print(f"  Option {chr(65+i)}: {total_dist[i]:3d} ({pct:.1f}%)")

if __name__ == "__main__":
    main()
