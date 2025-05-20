# No Big Tech Authenticator
*-english-*

A little less depenend on Big Tech with this open source Authenticator for Two-Factor Authentication (2FA) or Multi-Factor Authentication (MFA).

You can run it from the commandline and uses python 3.
Usage:

1. install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/);
2. run **pip install customtkinter pyotp cryptography**
3. run **python3 NoBigTech.py**.

The secrets file (**authenticator_secrets.enc**) is encrypted and should be protected with the Linux **chmod 600** command.

*-Nederlands / Dutch-*

Een beetje minder afhankelijk van Big Tech met deze opensource Authenticator voor twweestapsverificatie (2FA) of Multi Factor Authentication (MFA).

Je kunt het programma met python3 uitvoeren.

Werkwijze:

1. installeer Python van [https://www.python.org/downloads/](https://www.python.org/downloads/);
2. voer na installatie dit commando uit: **pip install customtkinter pyotp cryptography**
3. vanaf nu start je de auhenticator als volgt: **python3 NoBigTech.py**.

Het bestand #authenticator_secrets.enc# bevat de geheimen/secrets en is versleuteld. Onder Linux kun je dit bestand met **chmod 600** nog beter afschermen.
