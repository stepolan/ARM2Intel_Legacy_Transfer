# ARM2Intel Legacy Transfer

![Logo](ARM2Intel_Legacy_Transfer_Logo.png)

ARM2Intel Legacy Transfer is a tool that copies applications, preferences, documents, mail data, calendar data, and other non-hidden directories from a newer Mac with an Apple-based processor (ARM architecture) to an older Intel Mac with an older OS version. It ensures compatibility by excluding applications that are not universal binaries (compatible with both Intel and Apple Silicon architectures).

This script was created because the Apple migration assistant does not let you migrate settings from a new Operating System to an older one. This is probably because things break when you do. Expect things to break, use at your own risk, and only use this on a fresh install of OSX on a wiped drive.

## Usage

### Cloning the Repo and Creating an Environment

1. **Clone the Repository**:
   - Open your terminal.
   - Navigate to the directory where you want to clone the repository.
   - Run the following command to clone the repository:
     ```bash
     git clone https://github.com/yourusername/arm2intel_legacy_transfer.git
     ```

2. **Navigate to the Project Directory**:
   - Change to the project directory:
     ```bash
     cd arm2intel_legacy_transfer
     ```

3. **Download and Install Miniconda**:
   - Download Miniconda from the official site: [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
   - Choose the installer for your operating system and architecture.
   - Follow the installation instructions on the site.

4. **Create and Activate a Conda Environment**:
   - Create a new conda environment with Python 3.9:
     ```bash
     conda create --name arm2intel_legacy_transfer python=3.9
     ```
   - Activate the environment:
     ```bash
     conda activate arm2intel_legacy_transfer
     ```

### Mounting the New Mac as a Disk on the Old Mac

5. **Enable Target Disk Mode on the New Mac**:
   - Restart the new Mac and hold down the `T` key while it restarts.
   - Connect the new Mac to the old Mac using a USB-C or Thunderbolt cable.
   - The new Mac will appear as an external disk on the old Mac.

6. **Verify the Disk is Mounted**:
   - Open `Finder` on the old Mac.
   - You should see the new Mac's disk mounted as an external drive.

### Running the Script

7. **Run the Script**:
   - In the terminal on the old Mac, navigate to the project directory where the script is located:
     ```bash
     cd /path/to/arm2intel_legacy_transfer
     ```
   - Run the script with the following command:
     ```bash
     python3 arm2intel_legacy_transfer.py
     ```

8. **Follow the Prompts**:
    - The script will guide you through the process of selecting which files and directories to copy.
    - Respond to the prompts to decide whether to copy applications, Xcode (if present), the entire Library directory, preferences, documents, mail data, calendar data, and other non-hidden directories in the user home folder.

9. **Check Logs**:
    - The script will log its operations to `copy_mac_apps.log`.
    - If there are any errors, they will be logged in `rsync_errors.log`. You can check this file to diagnose any issues.

## Disclaimer

This script is provided "as is", without warranty of any kind. Use at your own risk. The authors are not responsible for any damage or data loss that may occur as a result of using this script.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.