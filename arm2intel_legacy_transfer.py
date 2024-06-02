import os
import subprocess
import logging

# Configure logging
logging.basicConfig(
    filename='copy_mac_apps.log',
    level=logging.DEBUG,  # Set to DEBUG to enable verbose logging
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ANSI escape codes for color
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
DARK_MAGENTA = '\033[35m'
BOLD = '\033[1m'
ENDC = '\033[0m'

# Section: Check if Application is Universal Binary
def check_universal_binary(app_path):
    logging.debug(f"Checking if {app_path} is a universal binary.")
    executable_path = os.path.join(app_path, "Contents", "MacOS")
    if not os.path.exists(executable_path):
        return False, "Executable not found"

    executables = os.listdir(executable_path)
    if not executables:
        return False, "No executable found in MacOS directory"

    executable_file = os.path.join(executable_path, executables[0])
    result = subprocess.run(["file", executable_file], capture_output=True, text=True)
    output = result.stdout
    logging.debug(f"file command output for {executable_file}: {output}")

    if "Mach-O universal binary with 2 architectures" in output:
        return True, output
    else:
        return False, output

# Section: Check Applications Folder
def check_applications_folder(mount_point):
    logging.debug(f"Checking applications in {mount_point}/Applications.")
    applications_folder = os.path.join(mount_point, "Applications")
    app_files = os.listdir(applications_folder)
    
    results = {}
    for app in app_files:
        if app.endswith(".app"):
            app_path = os.path.join(applications_folder, app)
            is_universal, details = check_universal_binary(app_path)
            results[app] = (is_universal, details)
            logging.debug(f"Checked {app}: Universal={is_universal}, Details={details}")
    
    return results

# Section: Save Results to File
def save_results_to_file(results):
    logging.debug("Saving results to universal_binaries_report.txt.")
    with open("universal_binaries_report.txt", "w") as f:
        for app, (is_universal, details) in results.items():
            status = "Universal Binary" if is_universal else "Not Universal"
            f.write(f"{app}: {status}\n")
            f.write(f"Details: {details}\n\n")

# Section: Save Non-Intel Apps to File
def save_non_intel_apps_to_file(results):
    logging.debug("Saving non-intel apps to non_intel_apps.txt.")
    with open("non_intel_apps.txt", "w") as f:
        for app, (is_universal, details) in results.items():
            if not is_universal:
                f.write(f"{app}\n")

# Section: Save Universal Apps to File
def save_universal_apps_to_file(results):
    logging.debug("Saving universal apps to universal_apps.txt.")
    with open("universal_apps.txt", "w") as f:
        for app, (is_universal, details) in results.items():
            if is_universal:
                f.write(f"{app}\n")

# Section: Copy All Applications Except Non-Intel Apps
def copy_all_except_non_intel_apps(mount_point, username, copy_xcode):
    logging.debug("Copying all applications except non-intel apps.")
    with open("non_intel_apps.txt", "r") as f:
        non_intel_apps = [line.strip() for line in f]
    
    applications_folder = os.path.join(mount_point, "Applications")
    app_files = os.listdir(applications_folder)
    
    not_copied_apps = []

    for app in app_files:
        if app.endswith(".app"):
            app_path = os.path.join(applications_folder, app)
            logging.debug(f"Preparing to copy {app}.")
            if app == "Xcode.app":
                if copy_xcode:
                    destination = os.path.expanduser("~/Applications/")
                    rsync_command = f"sudo rsync -avvh --rsync-path='sudo rsync' '{app_path}/' '{destination}' 2> rsync_errors.log"
                    result = subprocess.run(rsync_command, shell=True)
                    if result.returncode == 0:
                        logging.info(f"Copied Xcode to {destination} successfully")
                    else:
                        logging.error(f"Failed to copy Xcode to {destination}. Check rsync_errors.log for details.")
                else:
                    not_copied_apps.append(app)
            elif app not in non_intel_apps:
                destination = os.path.expanduser("~/Applications/")
                rsync_command = f"sudo rsync -avvh --rsync-path='sudo rsync' '{app_path}/' '{destination}' 2> rsync_errors.log"
                result = subprocess.run(rsync_command, shell=True)
                if result.returncode == 0:
                    logging.info(f"Copied {app} to {destination} successfully")
                else:
                    logging.error(f"Failed to copy {app} to {destination}. Check rsync_errors.log for details.")
            else:
                not_copied_apps.append(app)
    
    with open("apps_to_manually_install.txt", "w") as f:
        for app in not_copied_apps:
            f.write(f"{app}\n")
    
    destination = os.path.expanduser("~/Applications/")
    rsync_command = f"sudo rsync -avvh --rsync-path='sudo rsync' 'apps_to_manually_install.txt' '{destination}' 2> rsync_errors.log"
    result = subprocess.run(rsync_command, shell=True)
    
    if result.returncode == 0:
        logging.info(f"Copied apps_to_manually_install.txt to {destination} successfully")
    else:
        logging.error(f"Failed to copy apps_to_manually_install.txt to {destination}. Check rsync_errors.log for details.")

# Section: Copy Additional Folder
def copy_additional_folder(mount_point, username, folder):
    logging.debug(f"Copying additional folder {folder}.")
    source = os.path.join(mount_point, "Users", username, folder.lstrip("~/"))
    destination = os.path.expanduser(f"~/{os.path.basename(folder)}")
    
    rsync_command = f"sudo rsync -avvh --rsync-path='sudo rsync' '{source}/' '{destination}' 2> rsync_errors.log"
    result = subprocess.run(rsync_command, shell=True)
    
    if result.returncode == 0:
        logging.info(f"Copied {folder} to {destination} successfully")
    else:
        logging.error(f"Failed to copy {folder} to {destination}")

# Section: Ask User for Input with Highlighted Default Value
def ask_user(prompt, highlight, default='y'):
    response = input(f"{prompt.replace(highlight, YELLOW + BOLD + highlight + ENDC)} ({GREEN}y{ENDC}/{RED}n{ENDC}, default {GREEN}{default}{ENDC}): ").strip().lower()
    if response == '':
        return default == 'y'
    return response == 'y'

# Section: Find Non-Hidden Directories in Home Folder
def find_non_hidden_directories(mount_point, username):
    logging.debug(f"Finding non-hidden directories in {mount_point}/Users/{username}.")
    home_dir = os.path.join(mount_point, "Users", username)
    directories = [d for d in os.listdir(home_dir) if os.path.isdir(os.path.join(home_dir, d)) and not d.startswith('.')]
    return directories

# Section: Check if Xcode is Installed
def check_for_xcode(mount_point):
    logging.debug(f"Checking if Xcode is installed in {mount_point}/Applications.")
    return os.path.exists(os.path.join(mount_point, "Applications/Xcode.app"))

# Section: Center Text Within a Fixed Width
def center_within_width(text, width):
    text_width = len(text)
    padding = (width - text_width) // 2
    return ' ' * padding + text

# Section: Generate Summary of Applications Not Copied
def generate_summary(not_copied_apps):
    logging.debug("Generating summary of applications not copied.")
    summary = "\nSummary of Applications Not Copied:\n"
    summary += "=" * 50 + "\n"
    for app in not_copied_apps:
        summary += f"{app}: Not copied because it is not a universal binary or user opted out.\n"
    summary += "\nPlease manually install these applications on your older Mac as needed.\n"
    return summary

# Section: Save Summary to File
def save_summary_to_file(summary):
    logging.debug("Saving summary of applications not copied to not_copied_summary.txt.")
    with open("not_copied_summary.txt", "w") as f:
        f.write(summary)

if __name__ == "__main__":
    # Section: Get Mount Point and User Info
    logging.info("*** STARTING A NEW RUN OF THE SCRIPT ****")
    mount_point = input(f"Please enter the {YELLOW}{BOLD}mount point{ENDC} of the new Mac (e.g., /Volumes/Macintosh\\ HD): ")
    if not mount_point:
        mount_point = "/Volumes/Macintosh HD"
    
    while not os.path.ismount(mount_point.replace("\\", "")):
        mount_point = input(f"{RED}Mount point is not accessible. Please enter a valid mount point: {ENDC}")

    print(f"Contents of {mount_point}/Users:")
    users = os.listdir(os.path.join(mount_point, "Users"))
    for user in users:
        print(user)

    username = input(f"Please enter the {YELLOW}{BOLD}username{ENDC} of the new Mac: ")
    while not os.path.exists(os.path.join(mount_point, "Users", username)):
        username = input(f"{RED}User directory is not accessible. Please enter a valid username: {ENDC}")

    print(f"Contents of {mount_point}/Users/{username}:")
    user_dirs = os.listdir(os.path.join(mount_point, "Users", username))
    for directory in user_dirs:
        print(directory)

    # Section: Check Applications
    results = check_applications_folder(mount_point)
    save_results_to_file(results)
    save_non_intel_apps_to_file(results)
    save_universal_apps_to_file(results)
    logging.info("Results saved to 'universal_binaries_report.txt', 'non_intel_apps.txt', and 'universal_apps.txt'")

    # Section: Recommended to Copy
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{DARK_MAGENTA}{'='*50}{ENDC}\n\n{BOLD}{MAGENTA}{center_within_width('Recommended to Copy (default is Yes)', 50)}{ENDC}\n\n{DARK_MAGENTA}{'='*50}{ENDC}\n")
    copy_apps = ask_user("Do you want to copy applications?", "applications")
    print("")
    copy_xcode = False
    if check_for_xcode(mount_point):
        copy_xcode = ask_user("Xcode is a large application. Do you want to copy Xcode?", "Xcode")
        print("")
    copy_preferences = ask_user("Do you want to copy preferences?", "preferences")
    print("")
    copy_documents = ask_user("Do you want to copy documents?", "documents")
    print("")
    copy_mail = ask_user("Do you want to copy mail data?", "mail data")
    print("")
    copy_calendars = ask_user("Do you want to copy calendar data?", "calendar data")
    print("")
    copy_desktop = ask_user("Do you want to copy the Desktop directory?", "Desktop")
    print("")
    copy_pictures = ask_user("Do you want to copy the Pictures directory?", "Pictures")
    print("")
    copy_music = ask_user("Do you want to copy the Music directory?", "Music")
    print("")
    copy_movies = ask_user("Do you want to copy the Movies directory?", "Movies")
    print("")
    copy_public = ask_user("Do you want to copy the Public directory?", "Public")
    print("")
    copy_fonts = ask_user("Do you want to copy the Fonts directory?", "Fonts")
    print("")
    copy_dotfiles = ask_user("Do you want to copy dotfiles (like .bash_profile, .zshrc, .gitconfig)?", "dotfiles")
    print(f"{DARK_MAGENTA}{'='*50}{ENDC}\n")

    # Section: Optional to Copy
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{DARK_MAGENTA}{'='*50}{ENDC}\n\n{BOLD}{MAGENTA}{center_within_width('Optional to Copy (default is No)', 50)}{ENDC}\n\n{DARK_MAGENTA}{'='*50}{ENDC}\n")
    copy_library = ask_user("Do you want to copy the entire Library directory?", "Library", default='n')
    print("")
    copy_downloads = ask_user("Do you want to copy the Downloads directory?", "Downloads", default='n')
    print("")

    non_hidden_dirs = find_non_hidden_directories(mount_point, username)
    copy_dirs = {}
    for directory in non_hidden_dirs:
        if directory not in ["Library", "Desktop", "Pictures", "Music", "Movies", "Public", "Documents", "Downloads"]:
            copy_dirs[directory] = ask_user(f"Do you want to copy the {directory} directory?", directory, default='n')
            print("")
    print(f"{DARK_MAGENTA}{'='*50}{ENDC}\n")

    # Section: Copy Selected Items
    os.system('cls' if os.name == 'nt' else 'clear')
    not_copied_apps = []  # Initialize the list here to avoid undefined variable error

    if copy_apps:
        copy_all_except_non_intel_apps(mount_point, username, copy_xcode)
        logging.info("All applications except non-intel applications have been copied")

    if copy_library:
        copy_additional_folder(mount_point, username, "~/Library")
        logging.info("Library directory has been copied")

    if copy_preferences:
        copy_additional_folder(mount_point, username, "~/Library/Preferences")
        logging.info("Preferences have been copied")

    if copy_documents:
        copy_additional_folder(mount_point, username, "~/Documents")
        logging.info("Documents have been copied")

    if copy_mail:
        copy_additional_folder(mount_point, username, "~/Library/Mail")
        logging.info("Mail data has been copied")

    if copy_calendars:
        copy_additional_folder(mount_point, username, "~/Library/Calendars")
        logging.info("Calendar data has been copied")
    
    if copy_desktop:
        copy_additional_folder(mount_point, username, "~/Desktop")
        logging.info("Desktop directory has been copied")

    if copy_downloads:
        copy_additional_folder(mount_point, username, "~/Downloads")
        logging.info("Downloads directory has been copied")

    if copy_pictures:
        copy_additional_folder(mount_point, username, "~/Pictures")
        logging.info("Pictures directory has been copied")

    if copy_music:
        copy_additional_folder(mount_point, username, "~/Music")
        logging.info("Music directory has been copied")

    if copy_movies:
        copy_additional_folder(mount_point, username, "~/Movies")
        logging.info("Movies directory has been copied")

    if copy_public:
        copy_additional_folder(mount_point, username, "~/Public")
        logging.info("Public directory has been copied")

    if copy_fonts:
        copy_additional_folder(mount_point, username, "~/Library/Fonts")
        logging.info("Fonts directory has been copied")

    if copy_dotfiles:
        dotfiles = ['.bash_profile', '.zshrc', '.gitconfig']
        for dotfile in dotfiles:
            if os.path.exists(os.path.expanduser(f"~/{dotfile}")):
                copy_additional_folder(mount_point, username, f"~/{dotfile}")
                logging.info(f"{dotfile} has been copied")

    for directory, should_copy in copy_dirs.items():
        if should_copy:
            copy_additional_folder(mount_point, username, f"~/{directory}")
            logging.info(f"{directory} directory has been copied")

    # Generate and display summary
    summary = generate_summary(not_copied_apps)
    print("These Application were not copied since they do not have the binaries required for Intel. You will likely want to install this apps the standard way.")
    print(summary)
    save_summary_to_file(summary)
    logging.info("Summary of applications not copied has been saved to 'not_copied_summary.txt'")