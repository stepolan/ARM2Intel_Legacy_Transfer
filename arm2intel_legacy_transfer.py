import os
import subprocess
import logging

# Configure logging
logging.basicConfig(filename='copy_mac_apps.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ANSI escape codes for color
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
ENDC = '\033[0m'

def check_universal_binary(app_path):
    executable_path = os.path.join(app_path, "Contents", "MacOS")
    if not os.path.exists(executable_path):
        return False, "Executable not found"

    executables = os.listdir(executable_path)
    if not executables:
        return False, "No executable found in MacOS directory"

    executable_file = os.path.join(executable_path, executables[0])
    result = subprocess.run(["file", executable_file], capture_output=True, text=True)
    output = result.stdout

    if "Mach-O universal binary with 2 architectures" in output:
        return True, output
    else:
        return False, output

def check_applications_folder():
    applications_folder = "/Applications"
    app_files = os.listdir(applications_folder)
    
    results = {}
    for app in app_files:
        if app.endswith(".app"):
            app_path = os.path.join(applications_folder, app)
            is_universal, details = check_universal_binary(app_path)
            results[app] = (is_universal, details)
    
    return results

def save_results_to_file(results):
    with open("universal_binaries_report.txt", "w") as f:
        for app, (is_universal, details) in results.items():
            status = "Universal Binary" if is_universal else "Not Universal"
            f.write(f"{app}: {status}\n")
            f.write(f"Details: {details}\n\n")

def save_non_intel_apps_to_file(results):
    with open("non_intel_apps.txt", "w") as f:
        for app, (is_universal, details) in results.items():
            if not is_universal:
                f.write(f"{app}\n")

def save_universal_apps_to_file(results):
    with open("universal_apps.txt", "w") as f:
        for app, (is_universal, details) in results.items():
            if is_universal:
                f.write(f"{app}\n")

def copy_all_except_non_intel_apps(remote_ip, username, copy_xcode, transfer_method):
    with open("non_intel_apps.txt", "r") as f:
        non_intel_apps = [line.strip() for line in f]
    
    applications_folder = "/Applications"
    app_files = os.listdir(applications_folder)
    
    not_copied_apps = []

    for app in app_files:
        if app.endswith(".app"):
            app_path = os.path.join(applications_folder, app)
            if app == "Xcode.app":
                if copy_xcode:
                    destination = f"{username}@{remote_ip}:/Applications/"
                    if transfer_method == 'rsync':
                        rsync_command = ["rsync", "-avvh", app_path, destination]
                        subprocess.run(rsync_command)
                    else:
                        scp_command = ["scp", "-vr", app_path, destination]
                        subprocess.run(scp_command)
                    logging.info(f"Copied Xcode to {destination}")
                else:
                    not_copied_apps.append(app)
            elif app not in non_intel_apps:
                destination = f"{username}@{remote_ip}:/Applications/"
                if transfer_method == 'rsync':
                    rsync_command = ["rsync", "-avh", app_path, destination]
                    subprocess.run(rsync_command)
                else:
                    scp_command = ["scp", "-vr", app_path, destination]
                    subprocess.run(scp_command)
                logging.info(f"Copied {app} to {destination}")
            else:
                not_copied_apps.append(app)
    
    with open("apps_to_manually_install.txt", "w") as f:
        for app in not_copied_apps:
            f.write(f"{app}\n")
    
    if transfer_method == 'rsync':
        rsync_command = ["rsync", "-avvh", "apps_to_manually_install.txt", f"{username}@{remote_ip}:/Applications/"]
        subprocess.run(rsync_command)
    else:
        scp_command = ["scp", "-v", "apps_to_manually_install.txt", f"{username}@{remote_ip}:/Applications/"]
        subprocess.run(scp_command)
    logging.info(f"Copied apps_to_manually_install.txt to {username}@{remote_ip}:/Applications/")

def copy_additional_folder(remote_ip, username, folder, transfer_method):
    destination = f"{username}@{remote_ip}:{folder.replace('~', '')}"
    if transfer_method == 'rsync':
        rsync_command = ["rsync", "-avvh", os.path.expanduser(folder), destination]
        subprocess.run(rsync_command)
    else:
        scp_command = ["scp", "-vr", os.path.expanduser(folder), destination]
        subprocess.run(scp_command)
    logging.info(f"Copied {folder} to {destination}")

def ask_user(prompt, highlight):
    response = input(f"{prompt.replace(highlight, YELLOW + BOLD + highlight + ENDC)} ({GREEN}y{ENDC}/{RED}n{ENDC}, default {GREEN}y{ENDC}): ").strip().lower()
    if response == '' or response == 'y':
        return True
    return False

def ask_transfer_method():
    print(f"{YELLOW}{BOLD}Select transfer method:{ENDC}")
    print(f"{GREEN}1. rsync{ENDC} (Recommended for faster, incremental transfer, and resumes from interruptions)")
    print(f"{RED}2. scp{ENDC} (Simple, secure copy, but restarts the transfer from the beginning if interrupted)")
    while True:
        choice = input("Enter the number of your choice (default 1): ").strip()
        if choice == '' or choice == '1':
            return 'rsync'
        elif choice == '2':
            return 'scp'
        else:
            print(f"{RED}Invalid choice. Please enter 1 or 2.{ENDC}")

def find_non_hidden_directories():
    home_dir = os.path.expanduser("~")
    directories = [d for d in os.listdir(home_dir) if os.path.isdir(os.path.join(home_dir, d)) and not d.startswith('.')]
    return directories

def check_for_xcode():
    return os.path.exists("/Applications/Xcode.app")

if __name__ == "__main__":
    results = check_applications_folder()
    save_results_to_file(results)
    save_non_intel_apps_to_file(results)
    save_universal_apps_to_file(results)
    logging.info("Results saved to 'universal_binaries_report.txt', 'non_intel_apps.txt', and 'universal_apps.txt'")
    
    remote_ip = input(f"Please enter the {YELLOW}{BOLD}IP address{ENDC} of the older Mac: ")
    username = input(f"Please enter the {YELLOW}{BOLD}username{ENDC} of the older Mac: ")

    transfer_method = ask_transfer_method()

    copy_apps = ask_user("Do you want to copy applications?", "applications")
    copy_xcode = False
    if check_for_xcode():
        copy_xcode = ask_user("Xcode is a large application. Do you want to copy Xcode?", "Xcode")
    copy_library = ask_user("Do you want to copy the entire Library directory?", "Library")

    copy_preferences = copy_documents = copy_mail = copy_calendars = False
    if not copy_library:
        copy_preferences = ask_user("Do you want to copy preferences?", "preferences")
        copy_documents = ask_user("Do you want to copy documents?", "documents")
        copy_mail = ask_user("Do you want to copy mail data?", "mail data")
        copy_calendars = ask_user("Do you want to copy calendar data?", "calendar data")

    non_hidden_dirs = find_non_hidden_directories()
    copy_dirs = {directory: ask_user(f"Do you want to copy the {directory} directory?", directory) for directory in non_hidden_dirs if directory != "Library"}

    if copy_apps:
        copy_all_except_non_intel_apps(remote_ip, username, copy_xcode, transfer_method)
        logging.info("All applications except non-intel applications have been copied")

    if copy_library:
        copy_additional_folder(remote_ip, username, "~/Library", transfer_method)
        logging.info("Library directory has been copied")
    else:
        if copy_preferences:
            copy_additional_folder(remote_ip, username, "~/Library/Preferences", transfer_method)
            logging.info("Preferences have been copied")
            
    if copy_documents:
        copy_additional_folder(remote_ip, username, "~/Documents", transfer_method)
        logging.info("Documents have been copied")
                
    if copy_mail:
        copy_additional_folder(remote_ip, username, "~/Library/Mail", transfer_method)
        logging.info("Mail data has been copied")
                
    if copy_calendars:
        copy_additional_folder(remote_ip, username, "~/Library/Calendars", transfer_method)
        logging.info("Calendar data has been copied")

for directory, should_copy in copy_dirs.items():
    if should_copy:
        copy_additional_folder(remote_ip, username, f"~/{directory}", transfer_method)
        logging.info(f"{directory} directory has been copied")

logging.info("The list of apps that were not copied has been saved to 'apps_to_manually_install.txt' and copied to the remote Applications folder")