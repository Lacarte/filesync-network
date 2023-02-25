# File Synchronization Program

This program synchronizes files between a local folder and a remote folder on a LAN shared directory. It uses the SHA-1 hash of the files to check for changes and only transfers files that have been modified or are missing in the remote folder. The program displays the progress of the file transfer and checks for hash mismatches to ensure that the files have been transferred correctly.

## How to Use

1. Set the `src_folder` variable to the path of the local folder you want to synchronize.
2. Set the `ip` variable to the IP address or hostname of the remote LAN shared directory.
3. Set the `dest_folder` variable to the path of the remote folder you want to synchronize to.
4. Run the program using a Python interpreter.

## Dependencies

This program requires the following dependencies:

- `os`
- `time`
- `hashlib`
- `subprocess`
- `datetime`

## How it Works

The program runs in an infinite loop, pinging the remote LAN shared directory to check for connectivity. If the directory is reachable, the program walks through the local folder and compares the SHA-1 hash of each file to the corresponding file in the remote folder. If the hashes are different or the file does not exist in the remote folder, the program transfers the file using a custom function called `copy_with_progress()`, which displays the progress of the file transfer.

If the hash of the transferred file does not match the hash of the original file, the program attempts to transfer the file again. If the remote directory is not reachable, the program waits for 5 seconds before retrying the connection.
