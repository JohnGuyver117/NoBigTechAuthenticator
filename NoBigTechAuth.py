import customtkinter as ctk
from tkinter import messagebox, simpledialog
import pyotp, json, os, time
from cryptography.fernet import Fernet, InvalidToken
import base64, hashlib

SECRETS_FILE = 'authenticator_secrets.enc'

class AuthenticatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🔐 No Big Tech Authenticator")
        self.geometry("500x420")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.secrets = {}
        self.labels = {}
        
        if not os.path.exists(SECRETS_FILE):
            self.create_initial_password()
        elif not self.prompt_and_load_data():
            self.destroy()
            exit()

        self.create_widgets()
        self.update_gui()
        self.update_codes()

    def create_initial_password(self):
        while True:
            pwd1 = simpledialog.askstring("Nieuw wachtwoord aanmaken", "Stel een wachtwoord in:", show='●')
            if pwd1 is None:
                messagebox.showerror("Verplicht", "Een wachtwoord is verplicht. Probeer opnieuw.")
                continue
            pwd2 = simpledialog.askstring("Bevestig wachtwoord", "Bevestig je wachtwoord:", show='●')
            if pwd1 != pwd2:
                messagebox.showerror("Mismatch", "Wachtwoorden komen niet overeen, probeer opnieuw.")
            elif len(pwd1.strip()) < 4:
                messagebox.showerror("Te kort", "Wachtwoord minimaal 4 tekens.")
            else:
                break
        self.key = self.derive_key(pwd1)
        self.secrets = {}
        self.save_secrets()
        messagebox.showinfo("Succes", "Wachtwoord ingesteld!")

    def derive_key(self, password: str) -> bytes:
        salt = b'unieke_vaste_salt'
        dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return base64.urlsafe_b64encode(dk)

    def prompt_and_load_data(self) -> bool:
        for _ in range(3):
            pwd = simpledialog.askstring("Wachtwoord vereist", "Geef wachtwoord op:", show='●')
            if pwd is None:
                return False
            self.key = self.derive_key(pwd)
            try:
                with open(SECRETS_FILE, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = Fernet(self.key).decrypt(encrypted_data)
                self.secrets = json.loads(decrypted_data.decode())
                return True
            except (InvalidToken, json.JSONDecodeError):
                messagebox.showerror("Fout", "Incorrect wachtwoord.")
        return False

    def save_secrets(self):
        data = json.dumps(self.secrets).encode()
        encrypted_data = Fernet(self.key).encrypt(data)
        with open(SECRETS_FILE, 'wb') as f:
            f.write(encrypted_data)

    def create_widgets(self):
#        ctk.CTkLabel(self, text="🔑 No Big Tech Authenticator", font=("Helvetica", 18, "bold")).pack(pady=12)
        
        self.codes_frame = ctk.CTkScrollableFrame(self, height=200)
        self.codes_frame.pack(pady=5, padx=10, fill='both', expand=True)
        
        self.timer_label = ctk.CTkLabel(self, text="")
        self.timer_label.pack(pady=5)

        # Frame voor eerste rij knoppen
        btn_frame_top = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame_top.pack(pady=(15,5))

        ctk.CTkButton(btn_frame_top, text="➕ Account toevoegen", command=self.add_account).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(btn_frame_top, text="🗑️ Account verwijderen", command=self.remove_account).grid(row=0, column=1, padx=5, pady=5)

        # Frame voor tweede rij knoppen
        btn_frame_bottom = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame_bottom.pack(pady=5)

        ctk.CTkButton(btn_frame_bottom, text="🔑 Wijzig wachtwoord", fg_color='green', command=self.change_password).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(btn_frame_bottom, text="🔒 Afsluiten", fg_color='firebrick', command=self.destroy).grid(row=0, column=1, padx=5, pady=5)

    def update_gui(self):
        for w in self.codes_frame.winfo_children():
            w.destroy()
        self.labels.clear()

        if not self.secrets:
            ctk.CTkLabel(self.codes_frame, text="Geen accounts gevonden. ➕ Voeg er één toe.", text_color='gray').pack(pady=15)
            return

        for account in self.secrets:
            frm = ctk.CTkFrame(self.codes_frame)
            frm.pack(fill='x', padx=5, pady=2)
            ctk.CTkLabel(frm, text=account, font=("Arial",12)).pack(side='left', padx=10)
            lbl_code = ctk.CTkLabel(frm, text="------", font=("Courier",14,"bold"), text_color="cyan")
            lbl_code.pack(side='right', padx=10)
            self.labels[account] = lbl_code

    def update_codes(self):
        for name, secret in self.secrets.items():
            if name in self.labels:
                try:
                    code = pyotp.TOTP(secret).now()
                    self.labels[name].configure(text=code)
                except Exception as e:
                    self.labels[name].configure(text='INVALID')
        remain = 30 - int(time.time()) % 30
        self.timer_label.configure(text=f"Vernieuwd over {remain} sec")
        self.after(1000, self.update_codes)

    def add_account(self):
        naam = simpledialog.askstring("Account naam", "Naam van het account:")
        if not naam: return
        secret = simpledialog.askstring("Secret invoeren", f"Secret voor '{naam}':")
        if not secret: return

        try:
            pyotp.TOTP(secret.strip().replace(' ','').upper()).now()
            self.secrets[naam] = secret.strip().replace(' ','').upper()
            self.save_secrets()
            self.update_gui()
        except:
            messagebox.showerror("Fout","Ongeldig secret.")

    def remove_account(self):
        naam = simpledialog.askstring("Verwijderen","Account naam om te verwijderen:\n" + ", ".join(self.secrets))
        if naam in self.secrets:
            del self.secrets[naam]
            self.save_secrets()
            self.update_gui()
        else:
            messagebox.showerror("Fout","Account niet gevonden.")

    def change_password(self):
        old_pwd = simpledialog.askstring("Controle","Voer huidig wachtwoord in:", show='●')
        if self.derive_key(old_pwd) != self.key:
            messagebox.showerror("Fout","Huidig wachtwoord incorrect.")
            return
        new_pwd = simpledialog.askstring("Nieuw wachtwoord","Nieuw wachtwoord:", show='●')
        conf_pwd = simpledialog.askstring("Bevestigen","Bevestig nieuw wachtwoord:", show='●')
        if new_pwd != conf_pwd or not new_pwd.strip():
            messagebox.showerror("Fout","Wachtwoorden ongeldig of komen niet overeen.")
            return
        self.key = self.derive_key(new_pwd)
        self.save_secrets()
        messagebox.showinfo("Succes","Wachtwoord aangepast.")

if __name__ == "__main__":
    AuthenticatorApp().mainloop()
