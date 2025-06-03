import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import pyotp
import json, os, time
import hashlib, base64
from cryptography.fernet import Fernet, InvalidToken
import argparse

SECRETS_FILE = 'authenticator_secrets.enc'

translations = {
    'nl': {
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Stel nieuw wachtwoord in:',
        'confirm_password': 'Bevestig wachtwoord:',
        'password_mismatch': 'Wachtwoorden komen niet overeen.',
        'unlock_password': 'Voer je wachtwoord in om te ontgrendelen:',
        'wrong_password': 'Onjuist wachtwoord, probeer opnieuw.',
        'no_accounts': 'Nog geen accounts toegevoegd.',
        'add_account': '➕ Toevoegen',
        'remove_account': '🗑️ Verwijderen',
        'change_password': '🔑 Wijzig wachtwoord',
        'close_app': '🚪 Afsluiten',
        'new_account': 'Nieuw account toevoegen',
        'account_name': 'Accountnaam:',
        'enter_secret': 'Secret invoeren voor:',
        'invalid_secret': 'Secret ongeldig!',
        'select_account_remove': 'Account om te verwijderen:',
        'removed': 'Account verwijderd!',
        'added': 'Account toegevoegd!',
        'password_changed': 'Wachtwoord gewijzigd!',
        'enter_old_password': 'Huidig wachtwoord invoeren:',
        'enter_new_password': 'Nieuw wachtwoord invoeren:',
        'otp_copied': 'OTP-code {code} gekopieerd!',
        'copied': 'Gekopieerd',
    },
    'en': {
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Set a new password:',
        'confirm_password': 'Confirm password:',
        'password_mismatch': 'Passwords do not match.',
        'unlock_password': 'Enter your password to unlock:',
        'wrong_password': 'Incorrect password, try again.',
        'no_accounts': 'No accounts added yet.',
        'add_account': '➕ Add',
        'remove_account': '🗑️ Remove',
        'change_password': '🔑 Change password',
        'close_app': '🚪 Close',
        'new_account': 'Add new account',
        'account_name': 'Account name:',
        'enter_secret': 'Enter secret for:',
        'invalid_secret': 'Invalid secret!',
        'select_account_remove': 'Account to remove:',
        'removed': 'Account removed!',
        'added': 'Account added!',
        'password_changed': 'Password changed!',
        'enter_old_password': 'Enter current password:',
        'enter_new_password': 'Enter new password:',
        'otp_copied': 'OTP-code {code} copied!',
        'copied': 'Copied',
    },
    "de": {
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Neues Passwort festlegen:',
        'confirm_password': 'Passwort bestätigen:',
        'password_mismatch': 'Passwörter stimmen nicht überein.',
        'unlock_password': 'Passwort zum Entsperren eingeben:',
        'wrong_password': 'Falsches Passwort, versuchen Sie es erneut.',
        'no_accounts': 'Noch keine Konten hinzugefügt.',
        'add_account': '➕ Hinzufügen',
        'remove_account': '🗑️ Entfernen',
        'change_password': '🔑 Passwort ändern',
        'close_app': '🚪 Schließen',
        'new_account': 'Neues Konto hinzufügen',
        'account_name': 'Kontoname eingeben:',
        'enter_secret': 'Secret eingeben für:',
        'invalid_secret': 'Ungültiges Secret!',
        'select_account_remove': 'Konto zum Entfernen auswählen:',
        'removed': 'Konto entfernt!',
        'added': 'Konto hinzugefügt!',
        'password_changed': 'Passwort geändert!',
        'enter_old_password': 'Aktuelles Passwort eingeben:',
        'enter_new_password': 'Neues Passwort eingeben:',
        'otp_copied': 'OTP-Code {code} kopiert!',
        'copied': 'Kopiert',
    },

    "fr": {
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Définir un nouveau mot de passe:',
        'confirm_password': 'Confirmez le mot de passe:',
        'password_mismatch': 'Les mots de passe ne correspondent pas.',
        'unlock_password': 'Entrez votre mot de passe pour déverrouiller:',
        'wrong_password': 'Mot de passe incorrect, veuillez réessayer.',
        'no_accounts': 'Aucun compte ajouté pour le moment.',
        'add_account': '➕ Ajouter',
        'remove_account': '🗑️ Supprimer',
        'change_password': '🔑 Changer le mot de passe',
        'close_app': '🚪 Fermer',
        'new_account': 'Ajouter un nouveau compte',
        'account_name': 'Nom du compte:',
        'enter_secret': 'Entrer le secret pour:',
        'invalid_secret': 'Secret invalide !',
        'select_account_remove': 'Compte à supprimer:',
        'removed': 'Compte supprimé !',
        'added': 'Compte ajouté !',
        'password_changed': 'Mot de passe modifié !',
        'enter_old_password': 'Entrer le mot de passe actuel:',
        'enter_new_password': 'Entrer le nouveau mot de passe:',
        'otp_copied': 'Code OTP {code} copié!',
        'copied': 'Copié',
    },

    "it": {
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Imposta una nuova password:',
        'confirm_password': 'Conferma password:',
        'password_mismatch': 'Le password non corrispondono.',
        'unlock_password': 'Inserisci la password per sbloccare:',
        'wrong_password': 'Password errata, riprova.',
        'no_accounts': 'Nessun account aggiunto.',
        'add_account': '➕ Aggiungi',
        'remove_account': '🗑️ Rimuovi',
        'change_password': '🔑 Cambia password',
        'close_app': '🚪 Chiudi',
        'new_account': 'Aggiungi nuovo account',
        'account_name': 'Nome account:',
        'enter_secret': 'Inserisci il codice segreto per:',
        'invalid_secret': 'Codice segreto non valido!',
        'select_account_remove': 'Account da rimuovere:',
        'removed': 'Account rimosso!',
        'added': 'Account aggiunto!',
        'password_changed': 'Password modificata!',
        'enter_old_password': 'Inserisci la password attuale:',
        'enter_new_password': 'Inserisci la nuova password:',
        'otp_copied': 'Codice OTP {code} copiato!',
        'copied': 'Copiato',
    },

    "es": {
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Establecer nueva contraseña:',
        'confirm_password': 'Confirmar contraseña:',
        'password_mismatch': 'Las contraseñas no coinciden.',
        'unlock_password': 'Ingrese su contraseña para desbloquear:',
        'wrong_password': 'Contraseña incorrecta, inténtelo de nuevo.',
        'no_accounts': 'No se han añadido cuentas todavía.',
        'add_account': '➕ Añadir',
        'remove_account': '🗑️ Eliminar',
        'change_password': '🔑 Cambiar contraseña',
        'close_app': '🚪 Cerrar',
        'new_account': 'Añadir nueva cuenta',
        'account_name': 'Nombre de la cuenta:',
        'enter_secret': 'Ingresar secreto para:',
        'invalid_secret': '¡Secreto inválido!',
        'select_account_remove': 'Cuenta a eliminar:',
        'removed': '¡Cuenta eliminada!',
        'added': '¡Cuenta añadida!',
        'password_changed': '¡Contraseña cambiada!',
        'enter_old_password': 'Ingrese la contraseña actual:',
        'enter_new_password': 'Ingrese nueva contraseña:',
        'otp_copied': 'Código OTP {code} copiado!',
        'copied': 'Copiado',
    },

    "pt": {
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Definir nova senha:',
        'confirm_password': 'Confirmar senha:',
        'password_mismatch': 'As senhas não coincidem.',
        'unlock_password': 'Digite sua senha para desbloquear:',
        'wrong_password': 'Senha incorreta, tente novamente.',
        'no_accounts': 'Ainda sem contas adicionadas.',
        'add_account': '➕ Adicionar',
        'remove_account': '🗑️ Remover',
        'change_password': '🔑 Alterar senha',
        'close_app': '🚪 Fechar',
        'new_account': 'Adicionar nova conta',
        'account_name': 'Nome da conta:',
        'enter_secret': 'Insira o código secreto para:',
        'invalid_secret': 'Código secreto inválido!',
        'select_account_remove': 'Conta para remover:',
        'removed': 'Conta removida!',
        'added': 'Conta adicionada!',
        'password_changed': 'Senha alterada!',
        'enter_old_password': 'Digite a senha atual:',
        'enter_new_password': 'Digite a nova senha:',
        'otp_copied': 'Código OTP {code} copiado!',
        'copied': 'Copiado',
    },

    "da": {
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Angiv nyt kodeord:',
        'confirm_password': 'Bekræft kodeord:',
        'password_mismatch': 'Kodeordene stemmer ikke overens.',
        'unlock_password': 'Indtast dit kodeord for at låse op:',
        'wrong_password': 'Forkert kodeord, prøv igen.',
        'no_accounts': 'Ingen konti er endnu tilføjet.',
        'add_account': '➕ Tilføj',
        'remove_account': '🗑️ Fjern',
        'change_password': '🔑 Skift kodeord',
        'close_app': '🚪 Luk',
        'new_account': 'Tilføj ny konto',
        'account_name': 'Kontonavn:',
        'enter_secret': 'Indtast hemmelig kode for:',
        'invalid_secret': 'Ugyldig hemmelig kode!',
        'select_account_remove': 'Konto der skal fjernes:',
        'removed': 'Konto fjernet!',
        'added': 'Konto tilføjet!',
        'password_changed': 'Kodeord ændret!',
        'enter_old_password': 'Indtast nuværende kodeord:',
        'enter_new_password': 'Indtast det nye kodeord:',
        'otp_copied': 'OTP-kode {code} kopieret!',
        'copied': 'Kopieret',
    },
    "sv": {  # Zweeds
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Ange nytt lösenord:',
        'confirm_password': 'Bekräfta lösenordet:',
        'password_mismatch': 'Lösenorden matchar inte.',
        'unlock_password': 'Ange ditt lösenord för att låsa upp:',
        'wrong_password': 'Fel lösenord, försök igen.',
        'no_accounts': 'Inga konton tillagda ännu.',
        'add_account': '➕ Lägg till',
        'remove_account': '🗑️ Ta bort',
        'change_password': '🔑 Ändra lösenord',
        'close_app': '🚪 Stäng',
        'new_account': 'Lägg till nytt konto',
        'account_name': 'Kontonamn:',
        'enter_secret': 'Ange hemlig nyckel för:',
        'invalid_secret': 'Ogiltig hemlig nyckel!',
        'select_account_remove': 'Konto att ta bort:',
        'removed': 'Konto borttaget!',
        'added': 'Konto tillagt!',
        'password_changed': 'Lösenord ändrat!',
        'enter_old_password': 'Ange nuvarande lösenord:',
        'enter_new_password': 'Ange nytt lösenord:',
        'otp_copied': 'OTP-kod {code} kopierad!',
        'copied': 'Kopierad',
    },

    "no": {  # Noors
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Angi nytt passord:',
        'confirm_password': 'Bekreft passord:',
        'password_mismatch': 'Passordene stemmer ikke overens.',
        'unlock_password': 'Angi passordet ditt for å låse opp:',
        'wrong_password': 'Feil passord, prøv igjen.',
        'no_accounts': 'Ingen kontoer lagt til enda.',
        'add_account': '➕ Legg til',
        'remove_account': '🗑️ Fjern',
        'change_password': '🔑 Endre passord',
        'close_app': '🚪 Lukk',
        'new_account': 'Legg til ny konto',
        'account_name': 'Kontonavn:',
        'enter_secret': 'Angi hemmelig nøkkel for:',
        'invalid_secret': 'Ugyldig hemmelig nøkkel!',
        'select_account_remove': 'Velg konto som skal fjernes:',
        'removed': 'Konto fjernet!',
        'added': 'Konto lagt til!',
        'password_changed': 'Passord endret!',
        'enter_old_password': 'Oppgi nåværende passord:',
        'enter_new_password': 'Skriv inn nytt passord:',
        'otp_copied': 'OTP-kode {code} kopiert!',
        'copied': 'Kopiert',
    },

    "fi": {  # Fins
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Aseta uusi salasana:',
        'confirm_password': 'Vahvista salasana:',
        'password_mismatch': 'Salasanat eivät täsmää.',
        'unlock_password': 'Anna salasana avataksesi:',
        'wrong_password': 'Väärä salasana, yritä uudelleen.',
        'no_accounts': 'Ei vielä tilejä lisättynä.',
        'add_account': '➕ Lisää',
        'remove_account': '🗑️ Poista',
        'change_password': '🔑 Vaihda salasana',
        'close_app': '🚪 Sulje',
        'new_account': 'Lisää uusi tili',
        'account_name': 'Tilin nimi:',
        'enter_secret': 'Anna salaisuus:',
        'invalid_secret': 'Virheellinen salaisuus!',
        'select_account_remove': 'Poistettava tili:',
        'removed': 'Tili poistettu!',
        'added': 'Tili lisätty!',
        'password_changed': 'Salasana muutettu!',
        'enter_old_password': 'Anna nykyinen salasana:',
        'enter_new_password': 'Anna uusi salasana:',
        'otp_copied': 'OTP-koodi {code} kopioitu!',
        'copied': 'Kopioitu',
    },

    "pl": {  # Pools
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Ustaw nowe hasło:',
        'confirm_password': 'Potwierdź hasło:',
        'password_mismatch': 'Hasła nie pasują do siebie.',
        'unlock_password': 'Podaj hasło, aby odblokować:',
        'wrong_password': 'Nieprawidłowe hasło, spróbuj ponownie.',
        'no_accounts': 'Brak dodanych kont.',
        'add_account': '➕ Dodaj',
        'remove_account': '🗑️ Usuń',
        'change_password': '🔑 Zmień hasło',
        'close_app': '🚪 Zamknij',
        'new_account': 'Dodaj nowe konto',
        'account_name': 'Nazwa konta:',
        'enter_secret': 'Podaj klucz tajny dla:',
        'invalid_secret': 'Nieprawidłowy klucz tajny!',
        'select_account_remove': 'Konto do usunięcia:',
        'removed': 'Konto usunięte!',
        'added': 'Konto dodane!',
        'password_changed': 'Hasło zmienione!',
        'enter_old_password': 'Wprowadź aktualne hasło:',
        'enter_new_password': 'Wprowadź nowe hasło:',
        'otp_copied': 'Kod OTP {code} skopiowany!',
        'copied': 'Skopiowano',
    },

    "hu": {  # Hongaars
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Új jelszó beállítása:',
        'confirm_password': 'Jelszó megerősítése:',
        'password_mismatch': 'A jelszavak nem egyeznek.',
        'unlock_password': 'Adja meg a jelszót a feloldáshoz:',
        'wrong_password': 'Helytelen jelszó, próbálja újra.',
        'no_accounts': 'Nincs hozzáadott fiók.',
        'add_account': '➕ Hozzáadás',
        'remove_account': '🗑️ Törlés',
        'change_password': '🔑 Jelszó módosítása',
        'close_app': '🚪 Bezárás',
        'new_account': 'Új fiók hozzáadása',
        'account_name': 'Fiók neve:',
        'enter_secret': 'Írja be a titkos kulcsot:',
        'invalid_secret': 'Érvénytelen titkos kulcs!',
        'select_account_remove': 'Eltávolítandó fiók:',
        'removed': 'A fiók eltávolítva!',
        'added': 'A fiók hozzáadva!',
        'password_changed': 'Jelszó megváltoztatva!',
        'enter_old_password': 'Adja meg a jelenlegi jelszavát:',
        'enter_new_password': 'Adja meg az új jelszót:',
        'otp_copied': 'OTP-kód ({code}) kimásolva!',
        'copied': 'Kimásolva',
    },

    "sr": {  # Servisch (Cyrillisch alfabet)
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Поставите нову лозинку:',
        'confirm_password': 'Потврдите лозинку:',
        'password_mismatch': 'Лозинке се не поклапају.',
        'unlock_password': 'Унесите лозинку за откључавање:',
        'wrong_password': 'Погрешна лозинка, покушајте поново.',
        'no_accounts': 'Још увек нема додатих налога.',
        'add_account': '➕ Додај',
        'remove_account': '🗑️ Уклони',
        'change_password': '🔑 Промени лозинку',
        'close_app': '🚪 Затвори',
        'new_account': 'Додај нови налог',
        'account_name': 'Име налога:',
        'enter_secret': 'Унесите тајни кључ за:',
        'invalid_secret': 'Неважећи тајни кључ!',
        'select_account_remove': 'Налог за уклањање:',
        'removed': 'Налог уклоњен!',
        'added': 'Налог додат!',
        'password_changed': 'Лозинка промењена!',
        'enter_old_password': 'Унесите тренутну лозинку:',
        'enter_new_password': 'Унесите нову лозинку:',
        'otp_copied': 'OTP код {code} копиран!',
        'copied': 'Копирано',
    },
    "sl": {  # Sloveens
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Nastavi novo geslo:',
        'confirm_password': 'Potrdi geslo:',
        'password_mismatch': 'Gesli se ne ujemata.',
        'unlock_password': 'Za odklepanje vnesi geslo:',
        'wrong_password': 'Napačno geslo, poskusi znova.',
        'no_accounts': 'Ni še dodanih računov.',
        'add_account': '➕ Dodaj',
        'remove_account': '🗑️ Odstrani',
        'change_password': '🔑 Spremeni geslo',
        'close_app': '🚪 Zapri',
        'new_account': 'Dodaj nov račun',
        'account_name': 'Ime računa:',
        'enter_secret': 'Vnesi skrivni ključ za:',
        'invalid_secret': 'Neveljaven skrivni ključ!',
        'select_account_remove': 'Račun za odstranitev:',
        'removed': 'Račun odstranjen!',
        'added': 'Račun dodan!',
        'password_changed': 'Geslo je spremenjeno!',
        'enter_old_password': 'Vnesi trenutno geslo:',
        'enter_new_password': 'Vnesi novo geslo:',
        'otp_copied': 'OTP koda {code} kopirana!',
        'copied': 'Kopirano',
    },

    "hr": {  # Kroatisch
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Postavi novu lozinku:',
        'confirm_password': 'Potvrdi lozinku:',
        'password_mismatch': 'Lozinke se ne podudaraju.',
        'unlock_password': 'Unesi svoju lozinku za otključavanje:',
        'wrong_password': 'Pogrešna lozinka, pokušaj ponovno.',
        'no_accounts': 'Još nema dodanih računa.',
        'add_account': '➕ Dodaj',
        'remove_account': '🗑️ Ukloni',
        'change_password': '🔑 Promijeni lozinku',
        'close_app': '🚪 Zatvori',
        'new_account': 'Dodaj novi račun',
        'account_name': 'Ime računa:',
        'enter_secret': 'Unesi tajni ključ za:',
        'invalid_secret': 'Nevažeći tajni ključ!',
        'select_account_remove': 'Račun za uklanjanje:',
        'removed': 'Račun uklonjen!',
        'added': 'Račun dodan!',
        'password_changed': 'Lozinka promijenjena!',
        'enter_old_password': 'Unesi trenutnu lozinku:',
        'enter_new_password': 'Unesi novu lozinku:',
        'otp_copied': 'OTP kod {code} kopiran!',
        'copied': 'Kopirano',
    },

    "bs": {  # Bosnisch
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Postavi novu lozinku:',
        'confirm_password': 'Potvrdi lozinku:',
        'password_mismatch': 'Lozinke se ne podudaraju.',
        'unlock_password': 'Unesite svoju lozinku za otključavanje:',
        'wrong_password': 'Pogrešna lozinka, pokušajte ponovo.',
        'no_accounts': 'Još nema dodatih računa.',
        'add_account': '➕ Dodaj',
        'remove_account': '🗑️ Ukloni',
        'change_password': '🔑 Promijeni lozinku',
        'close_app': '🚪 Zatvori',
        'new_account': 'Dodaj novi račun',
        'account_name': 'Ime računa:',
        'enter_secret': 'Unesite tajni ključ za:',
        'invalid_secret': 'Nevažeći tajni ključ!',
        'select_account_remove': 'Račun za uklanjanje:',
        'removed': 'Račun uklonjen!',
        'added': 'Račun dodan!',
        'password_changed': 'Lozinka promijenjena!',
        'enter_old_password': 'Unesite trenutnu lozinku:',
        'enter_new_password': 'Unesite novu lozinku:',
        'otp_copied': 'OTP kod {code} kopiran!',
        'copied': 'Kopirano',
    },

    "ro": {  # Roemeens
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Setați o parolă nouă:',
        'confirm_password': 'Confirmați parola:',
        'password_mismatch': 'Parolele nu coincid.',
        'unlock_password': 'Introduceți parola pentru deblocare:',
        'wrong_password': 'Parolă greșită, încercați din nou.',
        'no_accounts': 'Nu sunt conturi adăugate încă.',
        'add_account': '➕ Adaugă',
        'remove_account': '🗑️ Șterge',
        'change_password': '🔑 Schimbă parola',
        'close_app': '🚪 Închide',
        'new_account': 'Adaugă cont nou',
        'account_name': 'Numele contului:',
        'enter_secret': 'Introdu cheia secretă pentru:',
        'invalid_secret': 'Cheie secretă invalidă!',
        'select_account_remove': 'Cont de șters:',
        'removed': 'Cont șters!',
        'added': 'Cont adăugat!',
        'password_changed': 'Parolă schimbată!',
        'enter_old_password': 'Introduceți parola curentă:',
        'enter_new_password': 'Introduceți parola nouă:',
        'otp_copied': 'Codul OTP {code} a fost copiat!',
        'copied': 'Copiat',
    },

    "bg": {  # Bulgaars
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Задаване на нова парола:',
        'confirm_password': 'Потвърдете паролата:',
        'password_mismatch': 'Паролите не съвпадат.',
        'unlock_password': 'Въведете паролата за отключване:',
        'wrong_password': 'Грешна парола, опитайте отново.',
        'no_accounts': 'Все още няма добавени акаунти.',
        'add_account': '➕ Добавяне',
        'remove_account': '🗑️ Премахване',
        'change_password': '🔑 Промяна на паролата',
        'close_app': '🚪 Затваряне',
        'new_account': 'Добавяне на нов акаунт',
        'account_name': 'Име на акаунта:',
        'enter_secret': 'Въведете таен ключ за:',
        'invalid_secret': 'Невалиден таен ключ!',
        'select_account_remove': 'Акаунт за премахване:',
        'removed': 'Акаунтът е премахнат!',
        'added': 'Акаунтът е добавен!',
        'password_changed': 'Паролата е променена!',
        'enter_old_password': 'Въведете текущата парола:',
        'enter_new_password': 'Въведете нова парола:',
        'otp_copied': 'OTP кодът {code} е копиран!',
        'copied': 'Копирано',
    },

    "el": {  # Grieks
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Ορισμός νέου κωδικού:',
        'confirm_password': 'Επιβεβαίωση κωδικού:',
        'password_mismatch': 'Οι κωδικοί δεν ταιριάζουν.',
        'unlock_password': 'Εισάγετε κωδικό για ξεκλείδωμα:',
        'wrong_password': 'Λάθος κωδικός, δοκιμάστε ξανά.',
        'no_accounts': 'Δεν προστέθηκαν λογαριασμοί ακόμα.',
        'add_account': '➕ Προσθήκη',
        'remove_account': '🗑️ Διαγραφή',
        'change_password': '🔑 Αλλαγή κωδικού',
        'close_app': '🚪 Κλείσιμο',
        'new_account': 'Προσθήκη νέου λογαριασμού',
        'account_name': 'Όνομα λογαριασμού:',
        'enter_secret': 'Εισαγωγή μυστικού κλειδιού για:',
        'invalid_secret': 'Μη έγκυρο μυστικό κλειδί!',
        'select_account_remove': 'Λογαριασμός προς διαγραφή:',
        'removed': 'Ο λογαριασμός διαγράφηκε!',
        'added': 'Ο λογαριασμός προστέθηκε!',
        'password_changed': 'Ο κωδικός άλλαξε!',
        'enter_old_password': 'Εισαγάγετε τον τρέχοντα κωδικό:',
        'enter_new_password': 'Εισαγάγετε νέο κωδικό:',
        'otp_copied': 'Ο κωδικός OTP {code} αντιγράφηκε!',
        'copied': 'Αντιγράφηκε',
    },

    "tr": {  # Turks
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Yeni şifre oluştur:',
        'confirm_password': 'Şifreyi doğrula:',
        'password_mismatch': 'Şifreler eşleşmiyor.',
        'unlock_password': 'Kilidi açmak için şifreyi girin:',
        'wrong_password': 'Yanlış şifre, tekrar deneyin.',
        'no_accounts': 'Henüz hesap eklenmedi.',
        'add_account': '➕ Ekle',
        'remove_account': '🗑️ Kaldır',
        'change_password': '🔑 Şifre değiştir',
        'close_app': '🚪 Kapat',
        'new_account': 'Yeni hesap ekle',
        'account_name': 'Hesap adı:',
        'enter_secret': 'Gizli anahtarı girin:',
        'invalid_secret': 'Geçersiz gizli anahtar!',
        'select_account_remove': 'Kaldırılacak hesap:',
        'removed': 'Hesap kaldırıldı!',
        'added': 'Hesap eklendi!',
        'password_changed': 'Şifre değiştirildi!',
        'enter_old_password': 'Mevcut şifreyi girin:',
        'enter_new_password': 'Yeni şifreyi girin:',
         'otp_copied': 'OTP kodu {code} kopyalandı!',
        'copied': 'Kopyalandı',
    },

    "ar": {  # Arabisch (Marokkaans Arabisch)
        'title': '🔐 مصادق بدون شركات كبرى',
        'set_password': 'قم بتعيين كلمة مرور جديدة:',
        'confirm_password': 'أكد كلمة المرور:',
        'password_mismatch': 'كلمتا المرور لا تتطابقان.',
        'unlock_password': 'أدخل كلمة المرور لفتح القفل:',
        'wrong_password': 'كلمة المرور خاطئة، حاول مرة أخرى.',
        'no_accounts': 'لا توجد حسابات مضافة بعد.',
        'add_account': '➕ إضافة',
        'remove_account': '🗑️ حذف',
        'change_password': '🔑 تغيير كلمة المرور',
        'close_app': '🚪 إغلاق',
        'new_account': 'إضافة حساب جديد',
        'account_name': 'اسم الحساب:',
        'enter_secret': 'أدخل المفتاح السري لـ:',
        'invalid_secret': 'مفتاح سري غير صالح!',
        'select_account_remove': 'حدد الحساب للحذف:',
        'removed': 'تم حذف الحساب!',
        'added': 'تمت إضافة الحساب!',
        'password_changed': 'تم تغيير كلمة المرور!',
        'enter_old_password': 'أدخل كلمة المرور الحالية:',
        'enter_new_password': 'أدخل كلمة المرور الجديدة:',
        'otp_copied': 'تم نسخ رمز OTP {code}!',
        'copied': 'تم النسخ',
    },

    "zh": {  # Chinees (Vereenvoudigd Mandarijn)
        'title': '🔐 无大科技身份验证器',
        'set_password': '设置新密码：',
        'confirm_password': '确认密码：',
        'password_mismatch': '密码不匹配。',
        'unlock_password': '输入密码以解锁：',
        'wrong_password': '密码错误，请重试。',
        'no_accounts': '尚未添加账户。',
        'add_account': '➕ 添加',
        'remove_account': '🗑️ 删除',
        'change_password': '🔑 更改密码',
        'close_app': '🚪 退出',
        'new_account': '添加新账户',
        'account_name': '账户名称：',
        'enter_secret': '输入账户的密钥：',
        'invalid_secret': '无效的密钥！',
        'select_account_remove': '选择要删除的账户：',
        'removed': '账户已删除！',
        'added': '账户已添加！',
        'password_changed': '密码已更改！',
        'enter_old_password': '输入当前密码：',
        'enter_new_password': '输入新密码：',
        'otp_copied': 'OTP代码{code}已复制！',
        'copied': '已复制',
    },
    "ko": {  # Koreaans
        'title': '🔐 No Big Tech 인증기',
        'set_password': '새로운 암호 설정:',
        'confirm_password': '암호 확인:',
        'password_mismatch': '암호가 일치하지 않습니다.',
        'unlock_password': '잠금 해제를 위해 암호를 입력하세요:',
        'wrong_password': '잘못된 암호입니다. 다시 시도하세요.',
        'no_accounts': '추가된 계정이 없습니다.',
        'add_account': '➕ 추가',
        'remove_account': '🗑️ 삭제',
        'change_password': '🔑 암호 변경',
        'close_app': '🚪 닫기',
        'new_account': '새 계정 추가',
        'account_name': '계정 이름:',
        'enter_secret': '비밀 키 입력:',
        'invalid_secret': '유효하지 않은 비밀 키입니다!',
        'select_account_remove': '삭제할 계정 선택:',
        'removed': '계정이 삭제되었습니다!',
        'added': '계정이 추가되었습니다!',
        'password_changed': '암호가 변경되었습니다!',
        'enter_old_password': '현재 암호 입력:',
        'enter_new_password': '새로운 암호 입력:',
        'otp_copied': 'OTP 코드 {code} 복사됨!',
        'copied': '복사됨',
    },

    "id": {  # Indonesisch
        'title': '🔐 Authenticator Tanpa Big Tech',
        'set_password': 'Tetapkan kata sandi baru:',
        'confirm_password': 'Konfirmasi kata sandi:',
        'password_mismatch': 'Kata sandi tidak cocok.',
        'unlock_password': 'Masukkan kata sandi untuk membuka:',
        'wrong_password': 'Kata sandi salah, coba lagi.',
        'no_accounts': 'Belum ada akun yang ditambahkan.',
        'add_account': '➕ Tambah',
        'remove_account': '🗑️ Hapus',
        'change_password': '🔑 Ubah kata sandi',
        'close_app': '🚪 Tutup',
        'new_account': 'Tambah akun baru',
        'account_name': 'Nama akun:',
        'enter_secret': 'Masukkan kunci rahasia untuk:',
        'invalid_secret': 'Kunci rahasia tidak valid!',
        'select_account_remove': 'Pilih akun untuk dihapus:',
        'removed': 'Akun dihapus!',
        'added': 'Akun ditambahkan!',
        'password_changed': 'Kata sandi diubah!',
        'enter_old_password': 'Masukkan kata sandi saat ini:',
        'enter_new_password': 'Masukkan kata sandi baru:',
        'otp_copied': 'Kode OTP {code} disalin!',
        'copied': 'Disalin',
    },

    "ja": {  # Japans
        'title': '🔐 No Big Tech認証アプリ',
        'set_password': '新しいパスワードを設定:',
        'confirm_password': 'パスワードを再入力:',
        'password_mismatch': 'パスワードが一致しません。',
        'unlock_password': 'ロック解除のためにパスワードを入力:',
        'wrong_password': 'パスワードが間違っています。',
        'no_accounts': 'まだアカウントが追加されていません。',
        'add_account': '➕ 追加',
        'remove_account': '🗑️ 削除',
        'change_password': '🔑 パスワードを変更',
        'close_app': '🚪 閉じる',
        'new_account': '新しいアカウントを追加',
        'account_name': 'アカウント名:',
        'enter_secret': 'シークレットキーを入力:',
        'invalid_secret': '無効なシークレットキーです！',
        'select_account_remove': '削除するアカウントを選択:',
        'removed': 'アカウントを削除しました！',
        'added': 'アカウントを追加しました！',
        'password_changed': 'パスワードが変更されました！',
        'enter_old_password': '現在のパスワードを入力:',
        'enter_new_password': '新しいパスワードを入力:',
        'otp_copied': 'OTPコード{code}をコピーしました！',
        'copied': 'コピー済み',
    },

    "cs": {  # Tsjechisch
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Nastavit nové heslo:',
        'confirm_password': 'Potvrdit heslo:',
        'password_mismatch': 'Hesla se neshodují.',
        'unlock_password': 'Zadejte heslo pro odemknutí:',
        'wrong_password': 'Nesprávné heslo, zkuste to znovu.',
        'no_accounts': 'Zatím nebyly přidány žádné účty.',
        'add_account': '➕ Přidat',
        'remove_account': '🗑️ Odebrat',
        'change_password': '🔑 Změnit heslo',
        'close_app': '🚪 Zavřít',
        'new_account': 'Přidat nový účet',
        'account_name': 'Název účtu:',
        'enter_secret': 'Zadejte tajný klíč pro:',
        'invalid_secret': 'Neplatný tajný klíč!',
        'select_account_remove': 'Vyberte účet k odstranění:',
        'removed': 'Účet odebrán!',
        'added': 'Účet přidán!',
        'password_changed': 'Heslo změněno!',
        'enter_old_password': 'Zadejte stávající heslo:',
        'enter_new_password': 'Zadejte nové heslo:',
        'otp_copied': 'OTP kód {code} zkopírován!',
        'copied': 'Zkopírováno',
    },

    "sk": {  # Slowaaks
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Nastaviť nové heslo:',
        'confirm_password': 'Potvrdiť heslo:',
        'password_mismatch': 'Heslá sa nezhodujú.',
        'unlock_password': 'Zadajte heslo na odomknutie:',
        'wrong_password': 'Nesprávne heslo, skúste znova.',
        'no_accounts': 'Zatiaľ nebol pridaný žiadny účet.',
        'add_account': '➕ Pridať',
        'remove_account': '🗑️ Odstrániť',
        'change_password': '🔑 Zmeniť heslo',
        'close_app': '🚪 Zavrieť',
        'new_account': 'Pridať nový účet',
        'account_name': 'Názov účtu:',
        'enter_secret': 'Zadajte tajný kľúč pre:',
        'invalid_secret': 'Neplatný tajný kľúč!',
        'select_account_remove': 'Vyberte účet na odstránenie:',
        'removed': 'Účet odstránený!',
        'added': 'Účet pridaný!',
        'password_changed': 'Heslo bolo zmenené!',
        'enter_old_password': 'Zadajte aktuálne heslo:',
        'enter_new_password': 'Zadajte nové heslo:',
        'otp_copied': 'OTP kód {code} skopírovaný!',
        'copied': 'Skopírované',
    },

    "ru": {  # Russisch
        'title': '🔐 Аутентификатор без Big Tech',
        'set_password': 'Установите новый пароль:',
        'confirm_password': 'Подтвердите пароль:',
        'password_mismatch': 'Пароли не совпадают.',
        'unlock_password': 'Введите пароль для разблокировки:',
        'wrong_password': 'Неверный пароль, попробуйте снова.',
        'no_accounts': 'Аккаунты еще не добавлены.',
        'add_account': '➕ Добавить',
        'remove_account': '🗑️ Удалить',
        'change_password': '🔑 Сменить пароль',
        'close_app': '🚪 Закрыть',
        'new_account': 'Добавить новый аккаунт',
        'account_name': 'Имя аккаунта:',
        'enter_secret': 'Введите секретный ключ для:',
        'invalid_secret': 'Недействительный секретный ключ!',
        'select_account_remove': 'Выберите аккаунт для удаления:',
        'removed': 'Аккаунт удален!',
        'added': 'Аккаунт добавлен!',
        'password_changed': 'Пароль изменен!',
        'enter_old_password': 'Введите текущий пароль:',
        'enter_new_password': 'Введите новый пароль:',
        'otp_copied': 'OTP-код {code} скопирован!',
        'copied': 'Скопировано',
    },

    "fy": {  # Fries
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Stel nij wachtwurd yn:',
        'confirm_password': 'Befêstigje wachtwurd:',
        'password_mismatch': 'Wachtwurden komme net oerien.',
        'unlock_password': 'Fier wachtwurd yn om te ûntsluten:',
        'wrong_password': 'Ferkeard wachtwurd, probearje opnij.',
        'no_accounts': 'Noch gjin akkounts tafoege.',
        'add_account': '➕ Tafoegje',
        'remove_account': '🗑️ Fuortsmite',
        'change_password': '🔑 Wachtwurd feroarje',
        'close_app': '🚪 Ofslute',
        'new_account': 'Nij akkount tafoegje',
        'account_name': 'Akkountnamme:',
        'enter_secret': 'Fier geheime kaai yn foar:',
        'invalid_secret': 'Net jildige geheime kaai!',
        'select_account_remove': 'Selektearje akkount om fuort te smiten:',
        'removed': 'Akkount fuortsmiten!',
        'added': 'Akkount tafoege!',
        'password_changed': 'Wachtwurd feroare!',
        'enter_old_password': 'Fier hjoeddeisk wachtwurd yn:',
        'enter_new_password': 'Fier nij wachtwurd yn:',
        'otp_copied': 'OTP-koade {code} kopiearre!',
        'copied': 'Kopiearre',
    },

    "cy": {  # Welsh
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Gosod cyfrinair newydd:',
        'confirm_password': 'Cadarnhewch y cyfrinair:',
        'password_mismatch': 'Nid yw\'r cyfrineiriau yn cyfateb.',
        'unlock_password': 'Rhowch gyfrinair i ddatgloi:',
        'wrong_password': 'Cyfrinair anghywir, ceisiwch eto.',
        'no_accounts': 'Dim cyfrifon wedi’u hychwanegu eto.',
        'add_account': '➕ Ychwanegu',
        'remove_account': '🗑️ Dileu',
        'change_password': '🔑 Newid cyfrinair',
        'close_app': '🚪 Cau',
        'new_account': 'Ychwanegu cyfrif newydd',
        'account_name': 'Enw’r cyfrif:',
        'enter_secret': 'Rhowch yr allwedd gyfrinachol ar gyfer:',
        'invalid_secret': 'Allwedd gyfrinachol annilys!',
        'select_account_remove': 'Dewiswch gyfrif i’w ddileu:',
        'removed': 'Mae’r cyfrif wedi’i ddileu!',
        'added': 'Mae’r cyfrif wedi’i ychwanegu!',
        'password_changed': 'Mae’r cyfrinair wedi’i newid!',
        'enter_old_password': 'Rhowch gyfrinair cyfredol:',
        'enter_new_password': 'Rhowch gyfrinair newydd:',
        'otp_copied': 'Copïwyd cod OTP {code}!',
        'copied': 'Wedi copïo',
    },

    "ga": {  # Iers(Gaeilge)
        'title': '🔐 Fíordheimhniú Gan Big Tech',
        'set_password': 'Socraigh pasfhocal nua:',
        'confirm_password': 'Deimhnigh pasfhocal:',
        'password_mismatch': 'Ní hionann na pasfhocail.',
        'unlock_password': 'Iontráil an pasfhocal chun díghlasáil:',
        'wrong_password': 'Pasfhocal mícheart, bain triail eile as.',
        'no_accounts': 'Gan cuntais curtha leis fós.',
        'add_account': '➕ Cuir Leis',
        'remove_account': '🗑️ Bain',
        'change_password': '🔑 Athraigh pasfhocal',
        'close_app': '🚪 Dún',
        'new_account': 'Cuir cuntas nua leis',
        'account_name': 'Ainm an chuntais:',
        'enter_secret': 'Iontráil eochair rúnda do:',
        'invalid_secret': 'Eochair rúnda neamhbhailí!',
        'select_account_remove': 'Roghnaigh cuntas le baint:',
        'removed': 'Cuntas bainte amach!',
        'added': 'Tá an cuntas curtha leis!',
        'password_changed': 'Tá an pasfhocal athraithe!',
        'enter_old_password': 'Cuir isteach an pasfhocal reatha:',
        'enter_new_password': 'Cuir isteach pasfhocal nua:',
        'otp_copied': 'Cóipeáladh cód OTP {code}!',
        'copied': 'Cóipeáladh',
    },

    "gd": {  # Schots Gaelisch
        'title': '🔐 Authenticator Gun Big Tech',
        'set_password': 'Suidhich facal-faire ùr:',
        'confirm_password': 'Dearbhaich am facal-faire:',
        'password_mismatch': 'Chan eil na faclan-faire co-ionann.',
        'unlock_password': 'Cuir a-steach am facal-faire airson fhuasgladh:',
        'wrong_password': 'Facal-faire ceàrr, feuch ris a-rithist.',
        'no_accounts': 'Chan eil cunntasan air an cur ris fhathast.',
        'add_account': '➕ Cuir ris',
        'remove_account': '🗑️ Thoir air falbh',
        'change_password': '🔑 Atharraich facal-faire',
        'close_app': '🚪 Dùin',
        'new_account': 'Cuir cunntas ùr ris',
        'account_name': 'Ainm a\' chunntais:',
        'enter_secret': 'Cuir a-steach an iuchair dhìomhair airson:',
        'invalid_secret': 'Iuchair dhìomhair mì-dhligheach!',
        'select_account_remove': 'Tagh cunntas airson a thoirt air falbh:',
        'removed': 'Chaidh an cunntas a thoirt air falbh!',
        'added': 'Chaidh an cunntas a chur ris!',
        'password_changed': 'Facal-faire air atharrachadh!',
        'enter_old_password': 'Cuir a-steach am facal-faire làithreach:',
        'enter_new_password': 'Cuir a-steach am facal-faire ùr:',
        'otp_copied': 'Chaidh an còd OTP {code} a chopaigeadh!',
        'copied': 'Air a chopaigeadh',
    },

    "is": {  # IJslands
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Setja nýtt lykilorð:',
        'confirm_password': 'Staðfesta lykilorð:',
        'password_mismatch': 'Lykilorðin passa ekki saman.',
        'unlock_password': 'Sláðu inn lykilorð til að aflæsa:',
        'wrong_password': 'Rangt lykilorð, reyndu aftur.',
        'no_accounts': 'Engir reikningar hafa verið bætt við ennþá.',
        'add_account': '➕ Bæta við',
        'remove_account': '🗑️ Fjarlægja',
        'change_password': '🔑 Breyta lykilorði',
        'close_app': '🚪 Loka',
        'new_account': 'Bæta við nýjum reikningi',
        'account_name': 'Nafn reiknings:',
        'enter_secret': 'Sláðu inn leyndarlykil fyrir:',
        'invalid_secret': 'Ógildur leyndarlykill!',
        'select_account_remove': 'Veldu reikning til að fjarlægja:',
        'removed': 'Reikningur fjarlægður!',
        'added': 'Reikningi bætt við!',
        'password_changed': 'Lykilorði breytt!',
        'enter_old_password': 'Sláðu inn núverandi lykilorð:',
        'enter_new_password': 'Sláðu inn nýtt lykilorð:',
        'otp_copied': 'OTP kóði {code} afritaður!',
        'copied': 'Afritað',
    },

    "mt": {  # Maltees
        'title': '🔐 No Big Tech Authenticator',
        'set_password': 'Issettja password ġdida:',
        'confirm_password': 'Ikkonferma il-password:',
        'password_mismatch': 'Il-passwords ma jaqblux.',
        'unlock_password': 'Daħħal il-password biex tiftaħ:',
        'wrong_password': 'Password ħażina, erġa\' pprova.',
        'no_accounts': 'Ma ġewx miżjuda kontijiet għadhom.',
        'add_account': '➕ Żid',
        'remove_account': '🗑️ Neħħi',
        'change_password': '🔑 Ibdel il-password',
        'close_app': '🚪 Agħlaq',
        'new_account': 'Żid kont ġdid',
        'account_name': 'Isem tal-kont:',
        'enter_secret': 'Daħħal iċ-ċavetta sigrieta għal:',
        'invalid_secret': 'Ċavetta sigrieta mhux valida!',
        'select_account_remove': 'Agħżel kont biex tneħħi:',
        'removed': 'Il-kont ġie mneħħija!',
        'added': 'Il-kont ġie miżjud!',
        'password_changed': 'Il-password inbidlet!',
        'enter_old_password': 'Daħħal il-password kurrenti:',
        'enter_new_password': 'Daħħal il-password il-ġdida:',
        'otp_copied': 'Kodiċi OTP {code} ikkupjat!',
        'copied': 'Ikkupjat',
    },
}

class AuthenticatorApp(ctk.CTk):
    def __init__(self, lang='nl'):
        super().__init__()
        self.lang = translations[lang]
        self.title(self.lang['title'])
        self.geometry("500x400")
        ctk.set_appearance_mode('dark')

        self.secrets, self.labels = {}, {}

        if not os.path.exists(SECRETS_FILE):
            self.create_initial_password()
        elif not self.prompt_and_load_data():
            self.destroy()
            return

        self.build_ui()
        self.update_gui()
        self.update_codes()

    def derive_key(self, pwd, salt):
        kdf = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100_000)
        return base64.urlsafe_b64encode(kdf)

    def create_initial_password(self):
        while True:
            pwd1 = self.ask_password(self.lang['set_password'])
            pwd2 = self.ask_password(self.lang['confirm_password'])
            
            if pwd1 is None or pwd2 is None:
                continue
            if pwd1 != pwd2:
                CTkMessagebox(message=self.lang['password_mismatch'], icon='cancel')
                continue

            salt = os.urandom(16)  # salt 128 bits is sufficient
            self.key = self.derive_key(pwd1, salt)
            self.save_secrets(salt)
            break

    def prompt_and_load_data(self):
        for _ in range(3):
            pwd = self.ask_password(self.lang['unlock_password'])
            if not pwd:
                return False
            try:
                with open(SECRETS_FILE, 'rb') as f:
                    file_content = f.read()
                    salt, encrypted = file_content[:16], file_content[16:]
                    self.key = self.derive_key(pwd, salt)
                    data = Fernet(self.key).decrypt(encrypted)
                    self.secrets = json.loads(data)
                return True
            except InvalidToken:
                CTkMessagebox(message=self.lang['wrong_password'], icon="cancel")
            except FileNotFoundError:
                CTkMessagebox(message="Secrets-bestand niet gevonden!", icon="cancel")
                return False
        return False

    def save_secrets(self, salt):
        data = json.dumps(self.secrets).encode()
        encrypted = Fernet(self.key).encrypt(data)
        with open(SECRETS_FILE, 'wb') as f:
            f.write(salt + encrypted)  # sla salt direct voor ciphertext op


    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
        CTkMessagebox(
            message=self.lang['otp_copied'].format(code=text),
            icon='info',
            title=self.lang['copied']
        )

    def ask_password(self, prompt):
        pwd = None

        def submit():
            nonlocal pwd
            pwd = entry.get()
            dialog.destroy()

        dialog = ctk.CTkToplevel(self)
        dialog.title(self.lang['title'])
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        
        dialog.transient(self)
        dialog.wait_visibility()  
        dialog.grab_set()         
        dialog.focus()
        dialog.attributes('-topmost', True)
        dialog.after(10, lambda: dialog.attributes('-topmost', False))

        lbl = ctk.CTkLabel(dialog, text=prompt)
        lbl.pack(pady=(20, 10), padx=10)

        entry = ctk.CTkEntry(dialog, show="●", width=250)
        entry.pack(pady=(0, 10))
        entry.focus()

        ok_btn = ctk.CTkButton(dialog, text="OK", command=submit)
        ok_btn.pack()

        self.wait_window(dialog)
        return pwd

    def build_ui(self):
        ctk.CTkLabel(self, text=self.lang['title'], font=("Helvetica", 20,"bold")).pack(pady=10)
        self.frame = ctk.CTkScrollableFrame(self, height=200)
        self.frame.pack(fill='both',expand=True,padx=10)
        self.timer_label = ctk.CTkLabel(self, text="", font=("Helvetica",14))
        self.timer_label.pack(pady=5)

        fr1 = ctk.CTkFrame(self, fg_color='transparent')
        fr1.pack(pady=5)
        ctk.CTkButton(fr1, text=self.lang['add_account'], command=self.add_account).pack(side='left', padx=5)
        ctk.CTkButton(fr1, text=self.lang['remove_account'], command=self.remove_account).pack(side='left', padx=5)

        fr2 = ctk.CTkFrame(self, fg_color='transparent')
        fr2.pack(pady=5)
        ctk.CTkButton(fr2, text=self.lang['change_password'], command=self.change_password, fg_color='green').pack(side='left', padx=5)
        ctk.CTkButton(fr2, text=self.lang['close_app'], command=self.destroy, fg_color='firebrick').pack(side='left', padx=5)

    def update_gui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.labels.clear()

        if not self.secrets:
            ctk.CTkLabel(self.frame, text=self.lang['no_accounts']).pack(pady=10)
            return

        for acc in self.secrets:
            frm = ctk.CTkFrame(self.frame)
            frm.pack(pady=3, fill='x', padx=5)

            # Account naam links
            ctk.CTkLabel(frm, text=acc).pack(side='left', padx=10)

            # OTP-code midden/rechts
            code_lbl = ctk.CTkLabel(frm, text='------', font=("Courier", 14), text_color="cyan")
            code_lbl.pack(side='left', padx=5)
            self.labels[acc] = code_lbl

            # Kopieer-knop rechts
            btn_copy = ctk.CTkButton(frm, text='📋', width=30,
                command=lambda lbl=code_lbl: self.copy_to_clipboard(lbl.cget('text')))
            btn_copy.pack(side='right', padx=5)


    def update_codes(self):
        for name, secret in self.secrets.items():
            if name in self.labels:
                self.labels[name].configure(text=pyotp.TOTP(secret).now())
        remain = 30 - int(time.time() % 30)
        self.timer_label.configure(text=f"⏳ {remain} s")
        self.after(1000, self.update_codes)

    def add_account(self):
        naam = ctk.CTkInputDialog(text=self.lang['account_name'], title=self.lang['new_account']).get_input()
        if naam:
            secret = ctk.CTkInputDialog(text=f"{self.lang['enter_secret']} {naam}", title=self.lang['new_account']).get_input()
            if secret:
                secret = secret.strip().replace(" ","").upper()
                try:
                    pyotp.TOTP(secret).now()
                    self.secrets[naam] = secret
                    self.save_secrets()
                    self.update_gui()
                    CTkMessagebox(message=self.lang['added'], icon='info')
                except:
                    CTkMessagebox(message=self.lang['invalid_secret'], icon='cancel')

    def remove_account(self):
        if not self.secrets:
            CTkMessagebox(message=self.lang['no_accounts'], icon='warning')
            return
        naam = ctk.CTkInputDialog(text=self.lang['select_account_remove'], title=self.lang['remove_account']).get_input()
        if naam in self.secrets:
            del self.secrets[naam]
            self.save_secrets()
            self.update_gui()
            CTkMessagebox(message=self.lang['removed'], icon='info')

    def change_password(self):
        old_pwd = self.ask_password(self.lang['enter_old_password'])
        if not old_pwd or self.derive_key(old_pwd) != self.key:
            CTkMessagebox(message=self.lang['wrong_password'], icon='cancel')
            return
        new_pwd1 = self.ask_password(self.lang['enter_new_password'])
        new_pwd2 = self.ask_password(self.lang['confirm_password'])
        if new_pwd1 != new_pwd2 or not new_pwd1:
            CTkMessagebox(message=self.lang['password_mismatch'], icon='cancel')
            return
        self.key = self.derive_key(new_pwd1)
        self.save_secrets()
        CTkMessagebox(message=self.lang['password_changed'], icon='info')

def main():

    parser = argparse.ArgumentParser(description='No Big Tech Authenticator - CustomTkinter version')

    parser.add_argument('-t', '--language', type=str, default='en', help='Set the language (bijvoorbeeld -t en voor Engels, -t nl voor Nederlands)')

    args = parser.parse_args()

    # supported languages as provided

    supported_languages = "ar bg bs cs cy da de el en es fi fr fy ga gd hr hu id is it ja ko mt nl no pl pt ro ru sk sl sr sv tr zh".split()
    lang = args.language if args.language in supported_languages else 'en'

    app = AuthenticatorApp(lang=lang)
    app.mainloop()

if __name__ == "__main__":
    main()
