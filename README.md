# No Big Tech Authenticator

## English

### Description

A little less dependent on Big Tech with this open source Authenticator for Two-Factor Authentication (2FA) or Multi-Factor Authentication (MFA).

### Features

- Open source and independent of big tech companies.
- Supports 2FA and MFA.
- Data is securely stored in an encrypted file.

### Installation Instructions

You can run it with Python 3.

1. Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/);
2. Run **pip install customtkinter pyotp cryptography**;
3. Start the authenticator with **python3 NBTauth.py** or with **python3 NBTauth.py --language [land code]**.

supported languages [land codes]: "ar bg bs cs cy da de el en es fi fr fy ga gd hr hu id is it ja ko mt nl no pl pt ro ru sk sl sr sv tr zh"

### Security

The secrets file **authenticator_secrets.enc** is encrypted and should be protected with the Linux command **chmod 600**.

### Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.

### License

This project is licensed under the MIT License - see the **LICENSE.txt** file for details.


---

## Nederlands

### Beschrijving

Een beetje minder afhankelijk van Big Tech met deze opensource Authenticator voor tweefactorauthenticatie (2FA) of Multi-Factor Authentication (MFA).

### Kenmerken

- Open source en onafhankelijk van grote technologiebedrijven.
- Ondersteunt 2FA en MFA.
- Gegevens worden veilig opgeslagen in een versleuteld bestand.

### Installatie-instructies

Je kunt het programma met Python 3 uitvoeren.

1. Installeer Python van [https://www.python.org/downloads/](https://www.python.org/downloads/);
2. Voer na installatie dit commando uit: **pip install customtkinter pyotp cryptography**;
3. Vanaf nu start je de authenticator als volgt: **python3 NBTauth.py**.

### Veiligheid

Het bestand **authenticator_secrets.enc** bevat de geheimen/secrets en is versleuteld. Onder Linux kun je dit bestand met het commando **chmod 600** nog beter afschermen.

### Contributie

Bijdragen zijn welkom! Voel je vrij om een probleem te openen of een pull-verzoek in te dienen.

### Licentie

Dit project is gelicenseerd onder de MIT-licentie - zie het **LICENTIE.txt** bestand voor details.
