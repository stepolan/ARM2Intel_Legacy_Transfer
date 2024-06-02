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
     ``` bash
     git clone https://github.com/yourusername/arm2intel_legacy_transfer.git
     ```

2. **Navigate to the Project Directory**:
   - Change to the project directory:
     ``` bash
     cd arm2intel_legacy_transfer
     ```

3. **Download and Install Miniconda**:
   - Download Miniconda from the official site: [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
   - Choose the installer for your operating system and architecture.
   - Follow the installation instructions on the site.

4. **Create and Activate a Conda Environment**:
   - Create a new conda environment with Python 3.9:
     ``` bash
     conda create --name arm2intel_legacy_transfer python=3.9
     ```
   - Activate the environment:
     ``` bash
     conda activate arm2intel_legacy_transfer
     ```
     
### Mounting the ARM Mac as a Disk on the Intel Mac

6. **Mount the ARM Mac on the Intel Mac**:
   - Connect the two computers using a USB, USB-C, or Thunderbolt cable.
   - On the Mac with Apple silicon, choose Apple menu  > Shut Down.
   - Press and hold the power button until “Loading startup options” appears.
   - Click Options, then click Continue.
   - Select a startup disk, then click Next.
   - If requested, enter the password for an administrator account.
   - Your Mac opens in Recovery mode.
   - Choose Utilities > Share Disk.
   - Select the disk or volume that you want to share, then click Start Sharing.
   - On the other Mac, open a Finder window, then click Network (below Locations) in the sidebar.
   - In the Network window, double-click the Mac that has the shared disk or volume, click Connect As, select Guest in the Connect As window, then click Connect.
   - On the Intel Mac, the ARM Mac should appear as an external disk. Note the mount point (e.g., `/Volumes/Macintosh HD`).

### Running the Script

7. **Run the Script**:
   - Run the script with the following command:
     ``` bash
     python3 arm2intel_legacy_transfer.py
     ```

8. **Follow the Prompts**:
    - Enter the mount point and username of the ARM Mac when prompted. The default mount point is `/Volumes/Macintosh HD`.
    - Respond to the prompts to decide whether to copy applications, Xcode (if present), the entire Library directory, preferences, documents, mail data, calendar data, and other non-hidden directories in the user home folder.

9. **Check Logs**:
    - The script will log its operations to `copy_mac_apps.log`.
    - If there are any errors, they will be logged in `rsync_errors.log`. You can check this file to diagnose any issues.

## Disclaimer

This script is provided "as is", without warranty of any kind. Use at your own risk. The authors are not responsible for any damage or data loss that may occur as a result of using this script.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
