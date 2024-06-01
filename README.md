# ARM2Intel Legacy Transfer

ARM2Intel Legacy Transfer is a tool that copies applications, preferences, documents, mail data, calendar data, and other non-hidden directories from a newer Mac with an Apple-based processor (ARM architecture) to an older Intel Mac with an older OS version. It ensures compatibility by excluding applications that are not universal binaries (compatible with both Intel and Apple Silicon architectures).

This script was created because the Apple migration assistant does not let you migrate settings from a new Operating System to an older one. This is probably because things break when you do. Expect things to break, use at your own risk, and only use this on a fresh install of OSX on a wiped drive.

## Usage

### Cloning the repo and creating an environment.

1. Clone the repository.

2. Create and activate a conda environment:
   ```
   conda create --name arm2intel_legacy_transfer python=3.9
   conda activate arm2intel_legacy_transfer
   ```
3. Open VSCode and navigate to the project directory.

### The next steps are recommended to avoid multiple prompts for a password.

4. Generate SSH keys (if not already done):
   ```
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```
   Press Enter to accept the default file location and enter a passphrase if you want (or leave it empty for no passphrase).

5. Copy the public key to your older Mac:
   ```
   ssh-copy-id username@remote_ip
   ```
   Replace `username` and `remote_ip` with your actual username and the IP address of the older Mac. This will prompt you for the password one last time.

### Running the script.

6. Run the script:
   ```
   python3 arm2intel_legacy_transfer.py
   ```

7. Enter the IP address and username of the older Mac when prompted.

8. Respond to the prompts to decide whether to copy applications, Xcode (if present), the entire Library directory, preferences, documents, mail data, calendar data, and other non-hidden directories in the user home folder.

9. The script will then proceed to copy the selected files and directories. If there are any errors, they will be logged in `rsync_errors.log`. You can check this file to diagnose any issues.

## Disclaimer

This script is provided "as is", without warranty of any kind. Use at your own risk. The authors are not responsible for any damage or data loss that may occur as a result of using this script.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
