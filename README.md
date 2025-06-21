# No Big Tech Authenticator (nbtauth)

## English

### Description

A little less dependent on Big Tech with this open source Authenticator for Two-Factor Authentication (2FA) or Multi-Factor Authentication (MFA).

### Features

- Open source and independent of big tech companies.
- Supports 2FA and MFA.
- Data is securely stored in an encrypted file.

### Installation Instructions option 1 using it like a python 3 script

You can run it with Python 3.

1. Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/);
2. Run **pip install customtkinter CTKMessagebox pyotp cryptography**;
3. Start the authenticator with **python3 nbtauth.py** or with **python3 nbtauth.py --language [land code]**.

### Installation Instructions option 2 as pip package


1. Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/) and git;
2. Go to your command prompt enter **pip install git+https://github.com/JohnGuyver117/nbtauth.git**;
3. Start the authenticator with **nbtauth** or **nbtauth --language [land code]**.


### Language support

Supported languages [land codes]: "ar bg bs cs cy da de el en es fi fr fy ga gd hr hu id is it ja ko mt nl no pl pt ro ru sk sl sr sv tr zh"

### Security

The secrets file **authenticator_secrets.enc** is encrypted and should be protected with the Linux command **chmod 600**.

### Next steps: How to use it

When you start the application enter a password to protect secrets you are going to enter.
Make sure you **remember** this password very well, because if you can't remember it, the only way to access the sored secrets is by brute forcing it.

Next is to enter a secret from for example your Microsoft account, although all other parties will use the same way.
Log into your Microsoft portal, i.e. https://onedrive.live.com.

Go to your **My Microsoft account** and go to **Security**.
From there you go to **Ways to ptove who you are** and go to **Add a new way to sign in or verify**.
Select **Use an app** option.
You will see a Microsoft attempt to push their Authenticator app, but don't fall for it.
Click on **setp up a different Authenticator app**.
A new page will appear with a QR-code, which **nbtauth** can't process (yet?).
Lukely you can view the secret in human readale form.
That's something nbtauth can proces.
Enter this code in nbtauth and use the generated code to confirm that the authenticator is working.
And now you are done setting up your first OTP in nbtauth!

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
2. Voer na installatie dit commando uit: **pip install customtkinter CTKMessageboxpyotp cryptography**;
3. Vanaf nu start je de authenticator als volgt: **python3 nbtauth.py**.

### Veiligheid

Het bestand **authenticator_secrets.enc** bevat de geheimen/secrets en is versleuteld. Onder Linux kun je dit bestand met het commando **chmod 600** nog beter afschermen.

### Volgende stappen: Hoe gebruik je het?

Bij het starten van deze applicatie voer je eerst een wachtwoord in. Dit wachtwoord beveiligt de geheime sleutels (secrets) die je straks gaat invoeren.

Zorg dat je dit wachtwoord **goed onthoudt**, want als je het vergeet, bestaat er géén mogelijkheid meer om toegang te krijgen tot je opgeslagen secrets, behalve proberen het wachtwoord met brute kracht te achterhalen.

De volgende stap is het invoeren van een geheime sleutel. We gebruiken hier als voorbeeld je Microsoft-account, maar dezelfde stappen gelden over het algemeen ook voor andere aanbieders.

Log eerst in op je Microsoft-portaal, bijvoorbeeld op: https://onedrive.live.com.

Ga naar **Mijn Microsoft-account** en navigeer naar **Beveiliging**.

Binnen "Beveiliging" klik je op **Aanmeldmethoden** en kies vervolgens **een nieuwe aanmeld- of verificatiemethode toevoegen**.

Kies vervolgens de optie **Een app gebruiken**.

Microsoft probeert je nu waarschijnlijk hun eigen Authenticator-app op te dringen, maar daar trappen we natuurlijk niet in. Kies duidelijk de optie **Een andere Authenticator-app instellen**.

Er verschijnt nu een nieuwe pagina met een QR-code. Helaas kan **nbtauth** (nog?) geen QR-codes verwerken.

Gelukkig kun je op de pagina ook de "geheime sleutel" weergeven in leesbare vorm.

Kopieer deze geheime sleutel zorgvuldig en voer hem in bij nbtauth. Gebruik vervolgens de OTP-code die nbtauth genereert duidelijk om te controleren en bevestigen dat alles goed werkt.

Gefeliciteerd, je hebt nu met succes je eerste OTP-code ingesteld in nbtauth!

### Contributie

Bijdragen zijn welkom! Voel je vrij om een probleem te openen of een pull-verzoek in te dienen.

### Licentie

Dit project is gelicenseerd onder de MIT-licentie - zie het **LICENTIE.txt** bestand voor details.
