# ARM2Intel Legacy Transfer

ARM2Intel Legacy Transfer is a tool that copies applications, preferences, documents, mail data, calendar data, and other non-hidden directories from a newer Mac with an Apple-based processor (ARM architecture) to an older Intel Mac with an older OS version. It ensures compatibility by excluding applications that are not universal binaries (compatible with both Intel and Apple Silicon architectures).

## Usage

1. Clone the repository.
2. Create and activate a conda environment:
   ```bash
   conda create --name arm2intel_legacy_transfer python=3.9
   conda activate arm2intel_legacy_transfer
   ```
3. Open VSCode and navigate to the project directory.
4. Generate SSH keys (if not already done):
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```
   Press Enter to accept the default file location and enter a passphrase if you want (or leave it empty for no passphrase).
5. Copy the public key to your older Mac:
   ```bash
   ssh-copy-id username@remote_ip
   ```
   Replace `username` and `remote_ip` with your actual username and the IP address of the older Mac. This will prompt you for the password one last time.
6. Run the script:
   ```bash
   python3 arm2intel_legacy_transfer.py
   ```
7. Enter the IP address and username of the older Mac when prompted.
8. Select the transfer method (rsync or scp). 
   - rsync: Recommended for faster, incremental transfers, and can resume from interruptions.
   - scp: Simple, secure copy, but restarts the transfer from the beginning if interrupted.
9. Respond to the prompts to decide whether to copy applications, Xcode (if present), the entire Library directory, preferences, documents, mail data, calendar data, and other non-hidden directories in the user home folder.
10. The script will then proceed to copy the selected files and directories.

## Disclaimer

This script is provided "as is", without warranty of any kind. Use at your own risk. The authors are not responsible for any damage or data loss that may occur as a result of using this script.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.