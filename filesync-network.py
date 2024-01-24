import os
import time
import hashlib
import subprocess
from datetime import datetime
import json
from dotenv import load_dotenv
load_dotenv()
# import playsound
from colorama import init, Fore, Style
init()

# Environment variables
dest_target_ips = os.getenv("DEST_TARGET_IPS")
enable_sound = os.getenv("ENABLE_SOUND")
foundmp3 = os.getenv("FOUNDMP3")
src_folder = os.getenv("SRC_FOLDER")

if dest_target_ips is None:
    print("ERROR: Environment variable dest_target_ips not set.")
    exit(1)

try:
    dest_ips = json.loads(dest_target_ips)
except json.JSONDecodeError as e:
    print(f"ERROR: Invalid JSON format in DEST_TARGET_IPS: {e}")
    exit(1)


def hash_file(filename):
    """Return the SHA-1 hash of the file"""
    with open(filename, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()

def copy_with_progress(src_file, dst_file):
    # Get the size of the source file
    total_size = os.stat(src_file).st_size
    # Open the source and destination files
    with open(src_file, 'rb') as src, open(dst_file, 'wb') as dst:
        copied_size = 0
        while True:
            # Read 16 KB at a time
            buf = src.read(16 * 1024)
            if not buf:
                break
            # Write the data to the destination file
            dst.write(buf)
            # Update the copied size and display the progress
            copied_size += len(buf)
            progress = round(copied_size / total_size * 100, 2)
            print(f"\r{Fore.GREEN}>{Style.RESET_ALL} Progress: {progress}%", end='')
    print(f"\n{Fore.LIGHTBLACK_EX}SOURCE:{Style.RESET_ALL} {src_file}\n{Fore.LIGHTBLACK_EX}DESTINATION:{Style.RESET_ALL} {dst_file}\n{Fore.LIGHTBLACK_EX}FILE:{Style.RESET_ALL} {os.path.basename(src_file)}\n{Fore.LIGHTBLACK_EX}STATUS:{Style.RESET_ALL} Transfered Successful\n\n")
    #         print(f"\r> Progress: {progress}%", end='')
    # print(f"\nSOURCE: {src_file}\nDESTINATION: {dst_file}\nFILE: {os.path.basename(src_file)}\nSTATUS: Transfered Successful\n\n")

while True:
    for ip in dest_ips:
        dest_folder = r'\\'+ip+'\\@Sync'
        
        try:
            if not os.path.exists(dest_folder):
                # print(f"IP: \\\\{ip} [NOT YET DISCOVERED+]")
                print(f"{Fore.YELLOW}IP: \\\\{ip} [NOT YET DISCOVERED]{Style.RESET_ALL}")

                continue

            # Ping the remote LAN shared directory
            response = subprocess.run(["ping", "-n", "1", "-w", "1000", ip], stdout=subprocess.DEVNULL)
            if response.returncode == 0:
                if enable_sound and foundmp3:
                    # playsound.play
                    # sound(foundmp3)
                    pass
                print(f"IP: \\\\{ip} [READY TO SYNC]")
                
                for root, dirs, files in os.walk(src_folder):
                    for file in files:
                        src_file = os.path.join(root, file)
                        dest_file = src_file.replace(src_folder, dest_folder)
                        
                        if not os.path.exists(dest_file) or hash_file(src_file) != hash_file(dest_file):
                            copy_with_progress(src_file, dest_file)
            else:
                print(f"{Fore.YELLOW}IP: \\\\{ip} [NOT YET DISCOVERED]{Style.RESET_ALL}")
                print(f"IP: \\\\{ip} [NOT YET DISCOVERED]")
        except Exception as e:
            print(f"ERROR: {e}")

    time.sleep(30)  # Wait for 30 seconds before rechecking
