import urllib.request
import re
import configparser
import zipfile
import os
import subprocess

# dont config this file config config.ini
def read_config(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)

    version = config.get('Settings', 'version')
    website_url = config.get('Settings', 'url')
    relese = config.get("Settings", "relese")
    project_name = config.get("Settings", "project_name")

    return version, website_url, relese, project_name


version, website_url, relese, project_name = read_config()


def read_version(url):
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode('utf-8')
            text = re.sub('<[^<]+?>', '', html_content).strip()

            return text
    except Exception as e:
        print(f"Error: {e}")
        return None


web_version = read_version(website_url)


if web_version:
    if web_version != version:
        print()
        print("Your version: " + version)
        print("Newst version: " + web_version)
        print()
        cmd_update = input("Do you want update [y/n]? ")
        if cmd_update == "y": # modify this if not work :D
            relese_link = relese + "v" + web_version + ".zip"
            print(relese_link)

            try:
                with urllib.request.urlopen(relese_link) as response:
                    data = response.read()
                    with open(project_name + "-" + web_version + ".zip", 'wb') as file:
                        file.write(data)
                    print('Download!')
            except urllib.error.URLError as e:
                print(f'Error: {e.reason}')


            def install(zip_file, extract):
                with zipfile.ZipFile(zip_file, 'r') as zip_archiv:
                    zip_archiv.extractall(extract)

            zip_file = f'{project_name}-{web_version}.zip'
            actual_directory = os.getcwd()
            file_url = actual_directory.split("\\")
            file_url.pop()
            extract = "\\".join(file_url)
            install(zip_file, extract)
            input()
            new_program_folder = "\\" + project_name + "-" + web_version
            new_program = extract + new_program_folder
            new_program_file = new_program + "\\update.py"

            subprocess.run(["start", "cmd", "/k", "python", new_program_file], shell=True)
            exit()
            # exit program

        elif cmd_update == "n":
            print("OK!")
            # exit program
        else:
            print("Invalid stagment")
            # exit program

    else:
        print("Stable " + version)
        # exit program
