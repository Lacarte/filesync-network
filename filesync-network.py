import os
import time
import hashlib
import subprocess
from datetime import datetime

src_folder = r'D:\@Sync'
ip = "LCRT-A-NEW"
dest_folder = r'\\'+ip+'\\@Sync'

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
            print(f"Progress: {progress}%")
    
    print(f"{src_file} transferred successfully to {dst_file}.")

while True:
    try:
        # Ping the remote LAN shared directory
        response = subprocess.run(["ping", "-n", "1", "-w", "1", ip], stdout=subprocess.DEVNULL)
        if response.returncode == 0:
            # print("PING [OK]")
            for root, dirs, files in os.walk(src_folder):
                for file in files:
                    src_file = os.path.join(root, file)
                    dest_file = src_file.replace(src_folder, dest_folder)
                    if not os.path.exists(dest_file) or os.stat(src_file).st_mtime - os.stat(dest_file).st_mtime > 1:
                        print(f"Syncing: Hash mismatch for file {src_file}...")
                        copy_with_progress(src_file, dest_file)
                        if hash_file(src_file) != hash_file(dest_file):
                            print(f"ERROR: Hash mismatch for file {dest_file}. Resending...")
                            copy_with_progress(src_file, dest_file)
        else:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f"{current_time} ERROR: Unable to ping {dest_folder}. Retrying in 5 seconds...")
        time.sleep(1)
    except Exception as e:
        print(f"ERROR: {e}")
        time.sleep(5)
