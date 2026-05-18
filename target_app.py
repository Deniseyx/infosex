import customtkinter as ctk
import json
import os
import time

class TargetApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Target Application - Auth System")
        self.geometry("400x450")
        self.db_file = "database.json"
        self.current_user = None
        self.show_login()

    def load_db(self):
        if not os.path.exists(self.db_file):
            return {}
        try:
            with open(self.db_file, "r") as f:
                return json.load(f)
        except:
            return {}

    def save_db(self, data):
        with open(self.db_file, "w") as f:
            json.dump(data, f, indent=4)

    def log_event(self, level, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("sample.log", "a") as f:
            f.write(f"{timestamp} {level} {message}\n")

    def show_login(self):
        self.clear_screen()
        ctk.CTkLabel(self, text="Member Login", font=("Roboto", 24)).pack(pady=20)
        
        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username", width=250)
        self.user_entry.pack(pady=10)
        
        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.pass_entry.pack(pady=10)
        
        ctk.CTkButton(self, text="Sign In", command=self.login, width=200).pack(pady=10)
        
        # Fixed indentation: This must be inside show_login
        ctk.CTkButton(self, text="Create Account", fg_color="transparent", 
                      text_color="#3498db", hover_color="#eeeeee", 
                      command=self.show_signup).pack()

    def show_signup(self):
        self.clear_screen()
        ctk.CTkLabel(self, text="Create Account", font=("Roboto", 24)).pack(pady=20)
        
        self.new_user = ctk.CTkEntry(self, placeholder_text="Choose Username", width=250)
        self.new_user.pack(pady=10)
        
        self.new_pass = ctk.CTkEntry(self, placeholder_text="Choose Password", show="*", width=250)
        self.new_pass.pack(pady=10)
        
        ctk.CTkButton(self, text="Register", command=self.register, fg_color="#27ae60", width=200).pack(pady=10)
        ctk.CTkButton(self, text="Back to Login", fg_color="transparent", text_color="#3498db", command=self.show_login).pack()

    def register(self):
        user = self.new_user.get()
        pw = self.new_pass.get()
        
        if user and pw:
            db = self.load_db()
            db[user] = pw
            self.save_db(db)
            self.log_event("INFO", f"New user registered: {user}")
            self.show_login()

    def login(self):
        user = self.user_entry.get()
        pw = self.pass_entry.get()
        db = self.load_db()

        if user in db and db[user] == pw:
            self.current_user = user
            self.log_event("INFO", f"User '{user}' successfully logged in.")
            self.show_welcome(user)
        elif user not in db:
            self.log_event("WARNING", f"Unknown user login attempt: '{user}' not found in database")
            self.status_msg("Unknown User", "orange")
        else:
            self.log_event("ERROR", f"Failed password attempt for user '{user}'")
            self.status_msg("Invalid Credentials", "red")

    def show_welcome(self, username):
        self.clear_screen()
        ctk.CTkLabel(self, text=f"Hello, {username}!", font=("Roboto", 28, "bold")).pack(pady=40)
        ctk.CTkLabel(self, text="Welcome to the secure area.", font=("Roboto", 16)).pack(pady=10)
        
        ctk.CTkButton(self, text="Log Out", command=lambda: self.logout(username), 
                      fg_color="#c0392b", hover_color="#a93226", width=200).pack(pady=30)

    def logout(self, username):
        self.log_event("INFO", f"User '{username}' logged out.")
        self.current_user = None
        self.show_login()

    def status_msg(self, text, color):
        lbl = ctk.CTkLabel(self, text=text, text_color=color)
        lbl.pack()
        self.after(2000, lbl.destroy)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = TargetApp()
    app.mainloop()