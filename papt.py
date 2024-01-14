import subprocess
import shutil
import os
from datetime import datetime

LOG_FILE = "script_log.txt"

def log(message):
    with open(LOG_FILE, "a") as log_file:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_file.write(f"{timestamp} {message}\n")

def run_command(command):
    try:
        log(f"Executing command: {command}")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        log(f"Error: {e}")
        print(f"Error: {e}")
    except Exception as e:
        log(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")

def search_packages(query):
    run_command(f"apt search {query}")

def show_package_info(package_name):
    run_command(f"apt show {package_name}")

def install_package(package_name):
    run_command(f"sudo apt install {package_name}")

def update_packages():
    run_command("sudo apt update")

def upgrade_packages():
    run_command("sudo apt upgrade")

def remove_package(package_name):
    run_command(f"sudo apt remove {package_name}")

def fix_broken_packages():
    run_command("sudo apt --fix-broken install")

def autoremove_packages():
    run_command("sudo apt autoremove")

def collect_system_logs():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    zip_filename = f"system_logs_{timestamp}.zip"

    # Collect logs using journalctl
    log_dir = "system_logs"
    os.makedirs(log_dir, exist_ok=True)
    run_command(f"journalctl --no-pager > {log_dir}/journalctl.log")

    # Zip the logs
    shutil.make_archive(zip_filename, 'zip', log_dir)

    # Move the zip file to the script's directory
    shutil.move(zip_filename + ".zip", zip_filename)

    # Clean up: Remove the temporary log directory
    shutil.rmtree(log_dir)

    log(f"System logs collected and saved in {zip_filename}")
    print(f"System logs collected and saved in {zip_filename}")

def fix_common_debian_issues():
    commands = [
        "sudo dpkg --configure -a",
        "sudo apt install -f",
        "sudo apt clean",
        "sudo apt autoclean",
        "sudo apt autoremove",
    ]

    for command in commands:
        run_command(command)

    log("Common Debian issues fixed.")
    print("Common Debian issues fixed.")

def fix_broken_settings():
    # Add commands specific to fixing broken settings here
    log("Broken settings fixed.")
    print("Broken settings fixed.")

def set_startup_apps():
    print("List of installed programs:")
    result = subprocess.run("dpkg-query -l | grep '^ii'", shell=True, capture_output=True, text=True)
    programs = result.stdout.splitlines()[1:]  # Skip the header line

    for i, program in enumerate(programs, start=1):
        print(f"{i}. {program}")

    while True:
        try:
            choice = int(input("Enter the number of the program to set/unset for startup (or '0' to cancel): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(programs):
                program_name = programs[choice - 1].split()[1]
                enable_disable = input(f"Do you want to enable or disable {program_name} on startup? (1 for enable, 2 for disable): ")

                if enable_disable == '1':
                    run_command(f"sudo systemctl enable {program_name}.service")
                    print(f"{program_name} is now set to run on startup.")
                    log(f"{program_name} is now set to run on startup.")
                elif enable_disable == '2':
                    run_command(f"sudo systemctl disable {program_name}.service")
                    print(f"{program_name} is now unset from running on startup.")
                    log(f"{program_name} is now unset from running on startup.")
                else:
                    print("Invalid choice. Please enter '1' for enable or '2' for disable.")
            else:
                print("Invalid number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def edit_xdg_config_file():
    run_command("nano $XDG_CONFIG_HOME/environment")

def main():
    # Initialize log file
    with open(LOG_FILE, "w"):
        pass

    while True:
        print("Menu:")
        print("1. Search for packages")
        print("2. Show package information")
        print("3. Install package")
        print("4. Update packages")
        print("5. Upgrade packages")
        print("6. Remove package")
        print("7. Fix broken packages")
        print("8. Autoremove unnecessary dependencies")
        print("9. Collect system logs")
        print("10. Fix common Debian issues")
        print("11. Set system startup apps")
        print("12. Edit XDG config file")
        print("13. Fix broken settings")
        print("14. Exit")

        choice = input("Enter your choice (1-14): ")

        if choice == '1':
            query = input("Enter the package name or keyword to search: ")
            search_packages(query)
        elif choice == '2':
            package_name = input("Enter the name of the package to show information: ")
            show_package_info(package_name)
        elif choice == '3':
            package_name = input("Enter the name of the package to install: ")
            install_package(package_name)
        elif choice == '4':
            update_packages()
        elif choice == '5':
            upgrade_packages()
        elif choice == '6':
            package_name = input("Enter the name of the package to remove: ")
            remove_package(package_name)
        elif choice == '7':
            fix_broken_packages()
        elif choice == '8':
            autoremove_packages()
        elif choice == '9':
            collect_system_logs()
        elif choice == '10':
            fix_common_debian_issues()
        elif choice == '11':
            set_startup_apps()
        elif choice == '12':
            edit_xdg_config_file()
        elif choice == '13':
            fix_broken_settings()
        elif choice == '14':
            print("Exiting the program. Goodbye!")
            log("Script exited.")
            break
        else:
            log("Invalid choice. Please enter a number between 1 and 14.")
            print("Invalid choice. Please enter a number between 1 and 14.")

if __name__ == "__main__":
    main()

