---
layout: default
title: "Python.Apache.Logs"
description: "Analyse de Logs Apache avec Machine Learning"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Apache.Logs</span>
</div>

<div class="page-header">
  <h1>Python.Apache.Logs</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Apache.Logs" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Analyse de Logs Apache avec Machine Learning

## Introduction : Quand les Règles ne Suffisent Plus

Les approches traditionnelles de détection d'intrusion reposent sur des règles : "si la requête contient `../`, c'est suspect". Mais les attaquants s'adaptent, encodent leurs payloads, et inventent de nouvelles techniques. Comment détecter ce qui n'a jamais été vu auparavant ?

Le **Machine Learning** offre une approche complémentaire : plutôt que de définir explicitement ce qui est malveillant, on apprend ce qui est "normal" et on signale tout ce qui s'en écarte. Ce projet applique plusieurs algorithmes de clustering aux logs Apache pour identifier automatiquement les comportements anormaux.

### Pourquoi le clustering ?

Le clustering est une technique de ML non supervisée : on n'a pas besoin d'étiqueter manuellement les requêtes comme "bonnes" ou "mauvaises". L'algorithme découvre lui-même les groupes naturels dans les données. Les requêtes qui ne rentrent dans aucun groupe deviennent des **anomalies** à investiguer.

### Algorithmes implémentés

| Algorithme | Usage principal | Point fort |
|------------|-----------------|------------|
| **K-Means** | Groupement par similarité | Rapide et scalable |
| **DBSCAN** | Détection d'anomalies | Isole les outliers automatiquement |
| **Hiérarchique** | Taxonomie des requêtes | Visualisation en dendrogramme |
| **Spectral** | Relations complexes | Clusters de formes arbitraires |


## Architecture du Système

Les logs passent par un pipeline de traitement : parsing, extraction de features, vectorisation, puis clustering. Les anomalies sont extraites pour analyse manuelle.

<div class="mermaid">
flowchart TB
    subgraph INPUT["📂 Logs Apache"]
        L1["access.log"]
        L2["error.log"]
    end

    subgraph PARSE["⚙️ Parsing"]
        P1["Extraction features"]
        P2["IP, URL, Status, User-Agent"]
        P3["Vectorisation TF-IDF"]
    end

    subgraph ML["🤖 Machine Learning"]
        KM["K-Means"]
        DB["DBSCAN"]
        HC["Hiérarchique"]
        SC["Spectral"]
    end

    subgraph OUTPUT["📊 Résultats"]
        C1["Clusters normaux"]
        C2["🔴 Anomalies"]
        C3["Visualisations"]
    end

    INPUT --> PARSE
    PARSE --> P1 --> P2 --> P3
    P3 --> ML
    KM & DB & HC & SC --> OUTPUT

    style C2 fill:#e74c3c,fill-opacity:0.15
    style ML fill:#3498db,fill-opacity:0.15
    style OUTPUT fill:#808080,fill-opacity:0.15
    style PARSE fill:#808080,fill-opacity:0.15
    style INPUT fill:#808080,fill-opacity:0.15
</div>


## Pipeline d'Analyse en Détail

Ce diagramme de séquence montre le flux complet de l'analyse, de la lecture des logs jusqu'à la classification en clusters.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant L as 📂 Logs
    participant P as ⚙️ Parser
    participant V as 📊 Vectorizer
    participant M as 🤖 ML Model
    participant A as 🔍 Analyzer

    L->>P: Lignes de log brutes
    P->>P: Extraction via regex
    P->>V: Features (IP, URL, Status, UA)
    V->>V: Conversion TF-IDF
    V->>M: Vecteurs numériques
    M->>M: fit_predict()
    M->>A: Labels de clusters

    alt Cluster aberrant ou label -1
        A->>A: 🔴 Marquer comme anomalie
    else Cluster normal
        A->>A: ✅ Trafic légitime
    end
</div>


## Détection d'Anomalies avec DBSCAN

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) est particulièrement adapté à la détection d'anomalies car il identifie automatiquement les points qui ne rentrent dans aucun cluster dense. Ces points reçoivent le label **-1** et sont nos anomalies.

<div class="mermaid">
flowchart LR
    subgraph Data["Données d'entrée"]
        D1["Requêtes normales<br/>(trafic légitime)"]
        D2["Requêtes suspectes<br/>(patterns inhabituels)"]
        D3["Attaques<br/>(SQLi, XSS, etc.)"]
    end

    subgraph DBSCAN["Configuration DBSCAN"]
        EPS["eps = 0.5<br/>(rayon du voisinage)"]
        MIN["min_samples = 5<br/>(densité minimale)"]
    end

    subgraph Clusters["Résultats"]
        C0["Cluster 0: Trafic normal"]
        C1["Cluster 1: Bots légitimes"]
        OUT["Label -1: 🔴 Outliers (anomalies)"]
    end

    D1 & D2 & D3 --> DBSCAN
    DBSCAN --> C0 & C1 & OUT

    style OUT fill:#e74c3c,fill-opacity:0.15
    style C0 fill:#2ecc71,fill-opacity:0.15
    style Clusters fill:#808080,fill-opacity:0.15
    style DBSCAN fill:#808080,fill-opacity:0.15
    style Data fill:#808080,fill-opacity:0.15
</div>


## Structure du Projet

```
Python.Apache.Logs/
├── kmeans/
│   ├── kmeans_scratch.py      # K-Means implémenté from scratch
│   └── kmeans_sklearn.py      # K-Means avec scikit-learn
├── dbscan/
│   └── dbscan_anomaly.py      # Détection d'anomalies
├── hierarchical-clustering/
│   └── hierarchical.py        # Clustering hiérarchique
├── spectral-clustering/
│   └── spectral.py            # Clustering spectral
├── logs/
│   ├── july_2022.log
│   ├── august_2022.log
│   └── september_2022.log
└── candles/
    └── logistic-regression.py # Classification supervisée
```


## Exemple : K-Means pour Grouper les Requêtes

```python
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re

def parse_apache_logs(filename):
    """Parse les logs Apache au format Combined"""
    pattern = r'(\S+) - - \[.*?\] "(\S+) (\S+) .*?" (\d+) (\d+)'
    logs = []

    with open(filename) as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                logs.append({
                    'ip': match.group(1),
                    'method': match.group(2),
                    'request': match.group(3),
                    'status': int(match.group(4))
                })

    return pd.DataFrame(logs)


# Charger et parser les logs
logs = parse_apache_logs('access.log')

# Vectoriser les URLs avec TF-IDF
# (transforme les chaînes en vecteurs numériques)
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(logs['request'])

# Appliquer K-Means avec 5 clusters
kmeans = KMeans(n_clusters=5, random_state=42)
logs['cluster'] = kmeans.fit_predict(X)

# Analyser chaque cluster
for i in range(5):
    cluster_logs = logs[logs['cluster'] == i]
    print(f"\\nCluster {i}: {len(cluster_logs)} requêtes")
    print(cluster_logs['request'].value_counts().head(3))
```


## Exemple : DBSCAN pour Détecter les Anomalies

```python
from sklearn.cluster import DBSCAN

# DBSCAN pour détection automatique d'outliers
dbscan = DBSCAN(eps=0.5, min_samples=5)
logs['cluster'] = dbscan.fit_predict(X)

# Les anomalies ont le label -1
anomalies = logs[logs['cluster'] == -1]
print(f"🔴 {len(anomalies)} anomalies détectées\\n")

# Afficher les requêtes suspectes
for _, row in anomalies.head(10).iterrows():
    print(f"  [{row['status']}] {row['ip']:15} {row['request'][:60]}")
```


## Pour Aller Plus Loin

- 📚 [scikit-learn Clustering](https://scikit-learn.org/stable/modules/clustering.html) - Documentation officielle
- 📄 [Apache Log Format](https://httpd.apache.org/docs/2.4/logs.html) - Formats de logs
- 🔍 [DBSCAN for Anomaly Detection](https://www.kdnuggets.com/2020/04/dbscan-clustering-algorithm-machine-learning.html) - Tutoriel approfondi


## Exploits et Vulnérabilités Connues

- **CVE-2021-44228 (Log4Shell)** : Cette vulnérabilité critique dans Log4j se manifestait dans les logs via des patterns JNDI. L'analyse de logs avec ML peut détecter ces patterns inhabituels comme des anomalies avant même que la signature soit connue.

- **CVE-2017-5638 (Apache Struts RCE)** : L'exploitation de cette faille laissait des traces caractéristiques dans les logs Apache (headers Content-Type malformés). Un modèle de clustering aurait détecté ces requêtes comme outliers.

- **CVE-2019-0211 (Apache Privilege Escalation)** : Vulnérabilité d'escalade de privilèges dans Apache 2.4. Les tentatives d'exploitation généraient des patterns d'erreurs inhabituels dans les logs d'erreur Apache.

- **CVE-2021-41773 (Apache Path Traversal)** : Les requêtes exploitant cette faille contenaient des séquences `.%2e/` distinctives. L'analyse ML sur les chemins URL aurait isolé ces requêtes comme anomalies statistiques.


## Approfondissement Théorique

L'application du Machine Learning à l'analyse de logs de sécurité s'inscrit dans le domaine plus large de l'User and Entity Behavior Analytics (UEBA). Contrairement aux systèmes de détection basés sur des signatures (IDS traditionnels), l'approche ML permet de détecter les "zero-day" comportementaux : des attaques qui n'ont jamais été vues mais qui dévient statistiquement du comportement normal. Cette approche a été popularisée par les travaux de recherche sur la détection d'anomalies réseau dans les années 2000.

Le choix de l'algorithme de clustering dépend de la nature des données et des objectifs. K-Means suppose des clusters sphériques de taille similaire, ce qui convient bien aux logs de trafic régulier. DBSCAN excelle pour isoler les outliers sans hypothèse sur la forme des clusters, idéal pour la détection d'attaques rares. Le clustering hiérarchique permet de comprendre la taxonomie des requêtes (par exemple, distinguer les crawlers légitimes des scanners malveillants). Le clustering spectral, basé sur la théorie des graphes, capture des relations non-linéaires entre les requêtes.

Les défis de l'analyse de logs en production incluent : le volume de données (des millions de lignes par jour), le déséquilibre de classes (les attaques représentent moins de 0.1% du trafic), et la dérive conceptuelle (le comportement "normal" évolue avec le temps). Les solutions modernes utilisent des techniques de streaming ML (Mini-Batch K-Means), des fenêtres temporelles glissantes, et des mécanismes de réentraînement automatique. L'intégration avec des SIEM (Security Information and Event Management) comme Elastic SIEM ou Splunk permet d'opérationnaliser ces modèles.


---

