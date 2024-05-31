import os
import subprocess
import logging

# Configure logging
logging.basicConfig(filename='copy_mac_apps.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def copy_all_except_non_intel_apps(remote_ip, username):
    with open("non_intel_apps.txt", "r") as f:
        non_intel_apps = [line.strip() for line in f]
    
    applications_folder = "/Applications"
    app_files = os.listdir(applications_folder)
    
    not_copied_apps = []

    for app in app_files:
        if app.endswith(".app"):
            app_path = os.path.join(applications_folder, app)
            if app not in non_intel_apps:
                destination = f"{username}@{remote_ip}:/Applications/"
                scp_command = ["scp", "-vr", app_path, destination]
                subprocess.run(scp_command)
                logging.info(f"Copied {app} to {destination}")
            else:
                not_copied_apps.append(app)
    
    with open("apps_to_manually_install.txt", "w") as f:
        for app in not_copied_apps:
            f.write(f"{app}\n")
    
    subprocess.run(["scp", "-v", "apps_to_manually_install.txt", f"{username}@{remote_ip}:/Applications/"])
    logging.info(f"Copied apps_to_manually_install.txt to {username}@{remote_ip}:/Applications/")

def copy_additional_folder(remote_ip, username, folder):
    destination = f"{username}@{remote_ip}:{folder.replace('~', '')}"
    scp_command = ["scp", "-vr", os.path.expanduser(folder), destination]
    subprocess.run(scp_command)
    logging.info(f"Copied {folder} to {destination}")

def ask_user(prompt):
    response = input(f"{prompt} (yes/no, default yes): ").strip().lower()
    if response == '' or response == 'yes':
        return True
    return False

if __name__ == "__main__":
    results = check_applications_folder()
    save_results_to_file(results)
    save_non_intel_apps_to_file(results)
    save_universal_apps_to_file(results)
    logging.info("Results saved to 'universal_binaries_report.txt', 'non_intel_apps.txt', and 'universal_apps.txt'")
    
    remote_ip = input("Please enter the IP address of the older Mac: ")
    username = input("Please enter the username of the older Mac: ")

    if ask_user("Do you want to copy applications?"):
        copy_all_except_non_intel_apps(remote_ip, username)
        logging.info("All applications except non-intel applications have been copied")

    if ask_user("Do you want to copy preferences?"):
        copy_additional_folder(remote_ip, username, "~/Library/Preferences")
        logging.info("Preferences have been copied")

    if ask_user("Do you want to copy documents?"):
        copy_additional_folder(remote_ip, username, "~/Documents")
        logging.info("Documents have been copied")

    if ask_user("Do you want to copy mail data?"):
        copy_additional_folder(remote_ip, username, "~/Library/Mail")
        logging.info("Mail data has been copied")

    if ask_user("Do you want to copy calendar data?"):
        copy_additional_folder(remote_ip, username, "~/Library/Calendars")
        logging.info("Calendar data has been copied")
    
    logging.info("The list of apps that were not copied has been saved to 'apps_to_manually_install.txt' and copied to the remote Applications folder")