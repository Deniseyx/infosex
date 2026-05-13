import customtkinter as ctk
import threading
import time
import os
import json

class LogApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LogSentinel Dashboard")
        self.geometry("800x600")
        self.show_login()

    def show_login(self):
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(pady=40, padx=100, fill="both", expand=True)
        ctk.CTkLabel(self.login_frame, text="LogSentinel Security Login", font=("Roboto", 24, "bold")).pack(pady=20)
        self.user_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=250)
        self.user_entry.pack(pady=10)
        self.pass_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=250)
        self.pass_entry.pack(pady=10)
        ctk.CTkButton(self.login_frame, text="Access System", command=self.login, width=200).pack(pady=20)

    def login(self):
        if self.user_entry.get() == "admin" and self.pass_entry.get() == "password":
            self.login_frame.destroy()
            self.show_dashboard()

    def show_dashboard(self):
        self.status_label = ctk.CTkLabel(self, text="● SYSTEM MONITORING ACTIVE", text_color="#2ecc71", font=("Roboto", 14, "bold"))
        self.status_label.pack(pady=10)

        # state="disabled" makes it read-only
        self.log_display = ctk.CTkTextbox(self, width=700, height=350, font=("Consolas", 12), state="disabled")
        self.log_display.pack(pady=10, padx=20)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10, fill="x", padx=50)

        ctk.CTkButton(btn_frame, text="Export Security Report", command=self.export_report, fg_color="#34495e").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Clear Viewer", command=self.clear_logs, fg_color="#c0392b").pack(side="right", padx=10)

        self.alert_box = ctk.CTkLabel(self, text="SYSTEM SECURE", font=("Roboto", 12, "bold"), text_color="gray")
        self.alert_box.pack(pady=20)

        threading.Thread(target=self.run_monitor, daemon=True).start()

    def append_log(self, message):
        """Helper to insert text into a disabled textbox"""
        self.log_display.configure(state="normal")
        self.log_display.insert("end", f"{message}\n")
        self.log_display.configure(state="disabled")
        self.log_display.see("end")

    def clear_logs(self):
        self.log_display.configure(state="normal")
        self.log_display.delete("1.0", "end")
        self.log_display.configure(state="disabled")

    def export_report(self):
        content = self.log_display.get("1.0", "end")
        report_name = f"Security_Report_{int(time.time())}.txt"
        with open(report_name, "w") as f:
            f.write("--- LogSentinel Official Security Report ---\n")
            f.write(content)
        print(f"Report saved as {report_name}")

    def run_monitor(self):
            filename = "sample.log"
            try:
                with open('rules.json', 'r') as f:
                    rules = json.load(f)
                    keywords = rules.get('keywords', [])
            except: keywords = ["Failed password"]

            if not os.path.exists(filename):
                with open(filename, 'w') as f: f.write("")

            with open(filename, 'r') as f:
                # --- PHASE 1: Load History ---
                # Read everything currently in the file
                existing_lines = f.readlines()
                for line in existing_lines:
                    self.append_log(line.strip())
                
                # --- PHASE 2: Live Monitoring ---
                # We are now at the end of the file. 
                # Only lines added AFTER this point will trigger alerts.
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(0.5)
                        continue
                    
                    msg = line.strip()
                    self.append_log(msg)

                    # Trigger alert ONLY for new lines
                    if "Unknown user" in msg:
                        self.alert_box.configure(text=f"🚨 UNKNOWN USER DANGER: {msg}", text_color="#e67e22")
                    elif any(word in msg for word in keywords):
                        self.alert_box.configure(text=f"⚠️ THREAT DETECTED: {msg}", text_color="#e74c3c")

if __name__ == "__main__":
    app = LogApp()
    app.mainloop()