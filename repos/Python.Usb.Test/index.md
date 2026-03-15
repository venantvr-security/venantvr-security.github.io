---
layout: default
title: "Python.Usb.Test"
description: "Communication Python/Android via USB"
generated_at: "2026-03-14 14:31:40"
last_update: "2026-03-14"
---

<div class="breadcrumb">
  <a href="/">Accueil</a> / <span>Python.Usb.Test</span>
</div>

<div class="page-header">
  <h1>Python.Usb.Test</h1>
  <div class="page-actions">
    <a href="qcm/" class="btn btn-secondary">QCM</a>
    <a href="https://github.com/venantvr-security/Python.Usb.Test" class="btn btn-primary" target="_blank">GitHub</a>
  </div>
</div>

# Communication Python/Android via USB

## Introduction : Contrôler Android depuis Python

La communication USB entre un PC et un appareil Android ouvre de nombreuses possibilités : automatisation de tests, extraction de données, contrôle à distance, outils de sécurité... Ce projet explore les différentes méthodes pour établir cette communication, du plus simple (ADB) au plus bas niveau (PyUSB).

### Les différentes approches

Chaque solution a ses avantages selon le cas d'usage :

| Solution | Type | Cas d'usage idéal |
|----------|------|-------------------|
| **ADB** | CLI/Scripts | Débogage, transfert de fichiers, automatisation |
| **PyUSB** | Python bas niveau | Communication brute, périphériques custom |
| **usb4a** | Python Android | Applications Pydroid sur Android |
| **Kivy** | Framework Python | Applications mobiles multi-plateformes |
| **Java** | Android natif | Contrôle total, performances optimales |


## Architecture USB

Avant de coder, il est important de comprendre comment fonctionne la communication USB. L'hôte (PC) initie toutes les communications, et le device (Android) répond.

<div class="mermaid">
flowchart LR
    subgraph HOST["🖥️ PC (Hôte)"]
        PY["Python"]
        LIB["PyUSB / ADB"]
        DRV["Driver USB"]
    end

    subgraph CABLE["🔌 Câble USB"]
        direction TB
        DP["D+ (data+)"]
        DM["D- (data-)"]
        VCC["5V (alimentation)"]
        GND["GND"]
    end

    subgraph DEVICE["📱 Android"]
        USB["USB Controller"]
        APP["Application"]
    end

    PY --> LIB --> DRV
    DRV <--> CABLE <--> USB
    USB --> APP

    style PY fill:#3498db,fill-opacity:0.15
    style USB fill:#2ecc71,fill-opacity:0.15
    style DEVICE fill:#808080,fill-opacity:0.15
    style CABLE fill:#808080,fill-opacity:0.15
    style HOST fill:#808080,fill-opacity:0.15
</div>

### Classes USB importantes

Les appareils USB sont organisés en classes qui définissent leur comportement :

| Classe | Code | Usage typique |
|--------|------|---------------|
| **CDC** | 0x02 | Port série virtuel (comme un terminal) |
| **HID** | 0x03 | Clavier, souris, manette |
| **Mass Storage** | 0x08 | Stockage (clé USB, disque) |


## Méthode 1 : ADB (Android Debug Bridge)

ADB est la méthode la plus simple et la plus utilisée. Elle ne nécessite pas de programmation bas niveau : vous envoyez des commandes shell à l'appareil Android.

### Prérequis

1. Activer le **Mode Développeur** sur Android (7 taps sur "Numéro de build")
2. Activer le **Débogage USB** dans les Options développeur
3. Installer les outils ADB sur le PC

### Commandes de base

```bash
# Vérifier que l'appareil est connecté
adb devices

# Exécuter une commande shell sur Android
adb shell ls /sdcard

# Transférer un fichier vers Android
adb push local_file.txt /sdcard/

# Récupérer un fichier depuis Android
adb pull /sdcard/file.txt ./

# Installer une application
adb install app.apk
```

### Utilisation depuis Python

```python
import subprocess

def adb(cmd):
    """Exécute une commande ADB et retourne le résultat"""
    result = subprocess.check_output(['adb'] + cmd.split(), text=True)
    return result.strip()

# Exemples d'utilisation
devices = adb('devices')
print(f"Appareils connectés:\\n{devices}")

# Lister les fichiers sur Android
files = adb('shell ls /sdcard/Download')
print(f"\\nFichiers dans Download:\\n{files}")

# Prendre un screenshot
adb('shell screencap /sdcard/screen.png')
adb('pull /sdcard/screen.png ./screenshot.png')
print("Screenshot sauvegardé !")
```


## Méthode 2 : PyUSB (Bas Niveau)

PyUSB permet une communication USB directe, sans passer par ADB. C'est utile pour les périphériques custom ou quand vous avez besoin d'un contrôle total.

<div class="mermaid">
sequenceDiagram
    autonumber
    participant P as 🐍 Python
    participant U as 🔌 PyUSB
    participant D as 📱 Android

    P->>U: find(idVendor=0x18d1)
    U->>D: Énumération des devices
    D-->>U: Device trouvé
    P->>U: set_configuration()
    P->>U: bulk_transfer(endpoint, data)
    U->>D: Données USB brutes
    D-->>U: Réponse
    U-->>P: bytes reçus
</div>

### Exemple de code

```python
import usb.core
import usb.util

# Trouver l'appareil Android (Google Vendor ID = 0x18d1)
device = usb.core.find(idVendor=0x18d1)

if device is None:
    raise ValueError("Appareil Android non trouvé")

# Configurer l'appareil
device.set_configuration()

# Trouver les endpoints (points de communication)
cfg = device.get_active_configuration()
interface = cfg[(0, 0)]

# Endpoint de sortie (PC -> Android)
ep_out = usb.util.find_descriptor(
    interface,
    custom_match=lambda e:
        usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
)

# Endpoint d'entrée (Android -> PC)
ep_in = usb.util.find_descriptor(
    interface,
    custom_match=lambda e:
        usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
)

# Envoyer des données
ep_out.write(b'Hello Android!')

# Recevoir des données
data = ep_in.read(64)
print(f"Reçu: {bytes(data)}")
```


## Considérations de Sécurité

La communication USB peut être exploitée de manière malveillante. Ce projet est éducatif, mais gardez en tête :

- **BadUSB** : Un appareil peut se faire passer pour un clavier et injecter des commandes
- **Juice Jacking** : Un chargeur public malveillant peut exfiltrer des données
- **ADB non sécurisé** : Toujours désactiver le débogage USB après utilisation


## Pour Aller Plus Loin

- 📚 [PyUSB Documentation](https://pyusb.github.io/pyusb/) - Communication USB bas niveau
- 📱 [Android USB Host](https://developer.android.com/guide/topics/connectivity/usb/host) - Perspective côté Android
- 🔧 [ADB Documentation](https://developer.android.com/studio/command-line/adb) - Référence officielle


## Exploits et Vulnérabilités Connues

La communication USB et ADB ont été à l'origine de nombreuses vulnérabilités de sécurité :

| CVE | Produit | Description | Score CVSS |
|-----|---------|-------------|------------|
| **CVE-2020-0069** | MediaTek Android | Escalade de privilèges via USB permettant d'obtenir un shell root sur des millions d'appareils MediaTek | 7.8 Élevé |
| **CVE-2019-2215** | Android Binder | Use-after-free exploitable via USB debug, utilisé par le spyware Pegasus | 7.8 Élevé |
| **CVE-2018-9489** | Android | Fuite d'informations via ADB permettant de récupérer des données sensibles sans autorisation | 7.5 Élevé |
| **CVE-2017-0785** | Android Bluetooth/USB | BlueBorne - vulnérabilité permettant l'exécution de code à distance via interfaces sans fil | 8.8 Élevé |
| **CVE-2014-3153** | Linux Kernel (Towelroot) | Futex vulnerability exploitable via USB pour rooter des appareils Android | 7.2 Élevé |

Les attaques **BadUSB** (CVE-2014-3566 et suivantes) sont particulièrement insidieuses car elles modifient le firmware des contrôleurs USB pour se faire passer pour d'autres types de périphériques (clavier, carte réseau), rendant la détection pratiquement impossible par les antivirus traditionnels.


## Approfondissement Théorique

### Le modèle de sécurité USB et ses faiblesses

Le protocole USB a été conçu pour la simplicité d'utilisation, pas pour la sécurité. Le modèle de confiance implicite suppose que tout périphérique connecté est légitime. Lorsqu'un appareil s'annonce comme un clavier HID, le système d'exploitation l'accepte sans vérification. Cette architecture permet les attaques **BadUSB** ou un appareil malveillant (souvent une clé USB modifiée) injecte des frappes clavier à vitesse surhumaine pour exécuter des commandes. Le projet USB Armory et les outils comme **Rubber Ducky** exploitent cette confiance aveugle.

### ADB et la surface d'attaque Android

Android Debug Bridge représente un vecteur d'attaque majeur quand il est mal configuré. Historiquement, ADB over WiFi (port 5555) a été activé par défaut sur de nombreux appareils, permettant des compromissions à distance sans accès physique. Même avec ADB USB uniquement, un attaquant ayant un accès physique bref peut activer le débogage, installer une backdoor, et désactiver le débogage - laissant peu de traces. Les clés RSA d'autorisation ADB introduites depuis Android 4.2.2 atténuent ce risque, mais l'utilisateur peut toujours accepter une clé malveillante par inattention.

### Défense contre les attaques USB

Plusieurs mécanismes de défense existent contre les attaques USB. **USBGuard** sous Linux permet de définir des politiques d'autorisation basées sur les attributs des périphériques (vendor ID, product ID, classe). Les **ports USB data-only** ou **USB Condoms** bloquent physiquement les lignes de données, permettant uniquement la charge. Android 12+ introduit un mode "charging only" qui désactive les lignes de données au niveau matériel lorsque l'appareil est verrouillé. Pour les environnements haute sécurité, la désactivation complète des ports USB via BIOS/UEFI ou politique de groupe reste la mesure la plus efficace.


---

