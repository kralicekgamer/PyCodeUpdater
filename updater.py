import configparser
import urllib.request
import re
import requests
import os
import zipfile

class Updater:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        
        self.version = self.config.get('project', 'version', fallback=None)
        self.beta = self.config.getboolean('project', 'beta', fallback=False)
        self.version_url = self.config.get('project', 'version_url', fallback=None)
        self.project_url = self.config.get('project', 'project_url', fallback=None)
        self.download_release = self.config.getboolean('project', 'download_release', fallback=False)
        self.project_name = self.config.get('project', 'project_name', fallback=None)
        
        if not all([self.version, self.version_url, self.project_url, self.project_name]):
            raise ValueError("Missing required configuration values.")
        
    def read_version(self, url):
        try:
            with urllib.request.urlopen(url) as response:
                html_content = response.read().decode('utf-8')
                text = re.sub('<[^<]+?>', '', html_content).strip()
                return text
        except Exception as e:
            print(f"Error fetching version from {url}: {e}")
            exit(1)
    
    def check_for_update(self):
        new_version = self.read_version(self.version_url)
        
        if self.version != new_version:
            print(f"Current version: {self.version}")
            print(f"Newest version: {new_version}")
            
            if self.beta:
                update_prompt = "Do you want to update to the newest or stable version [y/n]? "
            else:
                update_prompt = "Do you want to update to the newest version [y/n]? "
            
            update = input(update_prompt).strip().lower()
            
            if update == 'y':
                self.download_and_update(new_version)
            elif update == 'n':
                exit()
            else:
                print("Invalid input. Exiting.")
                exit(1)
        else:
            print(f"Running latest version: {self.version}")
            exit()
    
    def download_and_update(self, new_version):
        if self.download_release:
            url = f"{self.project_url}/releases/download/{new_version}/{self.project_name}.zip"
        else:
            url = f"{self.project_url}/archive/refs/heads/main.zip"
        
        zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'update.zip')
        
        try:
            response = requests.get(url)
            response.raise_for_status()  
            
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            if zipfile.is_zipfile(zip_path):
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(os.path.dirname(os.path.abspath(__file__)))
                print("Update completed successfully.")
            else:
                print(f"Downloaded file is not a valid zip file: {zip_path}")
                exit(1)
        except requests.RequestException as e:
            print(f"Error downloading update: {e}")
            exit(1)
        except zipfile.BadZipFile:
            print("Downloaded file is not a valid zip file.")
            exit(1)
