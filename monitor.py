import time
import os

def monitor_file(filename):
    print(f"--- Monitoring started on: {filename} ---")
    
    # Open the file and go to the very end
    with open(filename, 'r') as f:
        f.seek(0, os.SEEK_END)
        
        while True:
            line = f.readline()
            if not line:
                # No new data, wait a tiny bit and try again
                time.sleep(0.1)
                continue
            
            # A new line was found!
            print(f"NEW ENTRY DETECTED: {line.strip()}")
            
            # Simple Rule Check
            if "Failed password" in line:
                print("!!! ALERT: Suspicious login activity detected !!!")

if __name__ == "__main__":
    # Make sure this matches your filename exactly
    monitor_file("sample.log")