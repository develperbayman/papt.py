import subprocess
import shutil
import os
from datetime import datetime

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
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

    print("Common Debian issues fixed.")

def set_startup_apps():
    print("List of installed programs:")
    run_command("dpkg-query -l | grep '^ii'")

    program_name = input("Enter the name of the program to set/unset for startup (or 'exit' to cancel): ")

    if program_name.lower() == 'exit':
        return

    enable_disable = input(f"Do you want to enable or disable {program_name} on startup? (enable/disable): ").lower()

    if enable_disable == 'enable':
        run_command(f"sudo systemctl enable {program_name}.service")
        print(f"{program_name} is now set to run on startup.")
    elif enable_disable == 'disable':
        run_command(f"sudo systemctl disable {program_name}.service")
        print(f"{program_name} is now unset from running on startup.")
    else:
        print("Invalid choice. Please enter 'enable' or 'disable'.")

def edit_xdg_environment_path():
    run_command("nano $XDG_CONFIG_HOME/environment")

def main():
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
        print("12. Edit XDG environment path")
        print("13. Exit")

        choice = input("Enter your choice (1-13): ")

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
            edit_xdg_environment_path()
        elif choice == '13':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 13.")

if __name__ == "__main__":
    main()
