# ARM2Intel Legacy Transfer

ARM2Intel Legacy Transfer is a tool that copies applications, preferences, documents, mail data, and calendar data from a newer Mac with an Apple-based processor (ARM architecture) to an older Intel Mac with an older OS version. It ensures compatibility by excluding applications that are not universal binaries (compatible with both Intel and Apple Silicon architectures).

## Usage

1. Clone the repository.
2. Create and activate a conda environment:
   ```bash
   conda create --name arm2intel_legacy_transfer python=3.9
   conda activate arm2intel_legacy_transfer
   ```
3. Open VSCode and navigate to the project directory.
4. Run the script:
   ```bash
   python3 copy_mac_apps.py
   ```
5. Enter the IP address and username of the older Mac when prompted.
6. Respond to the prompts to decide whether to copy applications, preferences, documents, mail data, and calendar data.

## Disclaimer

This script is provided "as is", without warranty of any kind. Use at your own risk. The authors are not responsible for any damage or data loss that may occur as a result of using this script.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.