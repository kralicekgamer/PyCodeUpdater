import configparser
import urllib
import re
import requests
import os
import zipfile

class Start:
    config = configparser.ConfigParser()
    config.read('config.ini')
    version = config.get('project', 'version') 
    beta = config.getboolean('project', 'beta') 
    version_url = config.get('project', 'version_url')
    project_url = config.get('project', 'project_url')
    download_relese = config.getboolean('project', 'download_relese')
    project_name = config.get('project', 'project_name')


    def read_version(url):
        try:
            with urllib.request.urlopen(url) as response:
                html_content = response.read().decode('utf-8')
                text = re.sub('<[^<]+?>', '', html_content).strip()
    
                return text
        except Exception as e:
            print(f"Error: {e}")
            exit()
    
    new_version = read_version(version_url)
    if version != new_version:
        if beta != True:
            print("Running old " + version)
            print("Newest is " + new_version)
            update = input("Do you want update to newest " + new_version + " [y/n] ")
        elif beta == True:
            print("You are running beta " + version)
            print("Newest is " + new_version)
            update = input("Do you want update to newest or stable " + new_version + " [y/n] ")
    elif version == new_version:
        print("Running stable " + version)
        exit()
    else:
        print("Error pyce")
        exit()

    if update == "y":
        if download_relese == True:
            # need to edit this
            # this is not optimized
            url = project_url + "/releases/download/" + new_version + "/" +  project_name + ".zip"
        elif download_relese == False:
            url = project_url + "/archive/refs/heads/main.zip"
        else:
            print("Error pyce")

    elif update == "n":
        exit()
    else:
        print("Invalid argument")


    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    zip_path = os.path.join(parent_dir, 'update.zip')
    response = requests.get(url)
    with open(zip_path, 'wb') as f:
        f.write(response.content)

    if zipfile.is_zipfile(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(parent_dir)
    else:
        print(f'Error with downloading: {zip_path}')
    exit()
    