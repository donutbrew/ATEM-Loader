import webbrowser
import os
from os.path import expanduser
import time
import zipfile
import platform


atemlibzip = 'https://github.com/mintopia/atemlib/releases/download/v2.0.2/atemlib-2.0.2.zip'
exe_path = os.path.dirname(os.path.realpath(__file__))
print('#' * 80)
print(f"This doesn't work yet. just go download {atemlibzip}\nThen extract it to a directory here: {exe_path}, and modify yout config.yml to match." )
print('#' * 80)
exit(0)      

def download_file(url):
    browser_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
    # Safari on mac isn't playing well with webbrowser, so using a system call
    if platform.system() == 'Darwin':
        browser_path = '/Applications/Safari.app'
        os.system('open -a {} {}'.format(browser_path, url))
    else:
        webbrowser.register('edge', None,webbrowser.BackgroundBrowser(browser_path))
        # Open the presentation URL in Microsoft Edge
        webbrowser.get('edge').open(url)
        # Wait for the user to manually save the presentation as PDF
def get_downloaded_file():
    if os.name == 'nt':
        directory_path = os.path.join(expanduser("~"), "Downloads")
    elif os.name == 'posix':
        directory_path = os.path.join(expanduser("~"), "Downloads")
    else:
        directory_path = os.path.join(expanduser("~"), "Downloads")
    
    all_files = os.listdir(directory_path)

    # Filter out only files (excluding directories) and exclude dotfiles
    files = [f for f in all_files if os.path.isfile(os.path.join(directory_path, f)) and not f.startswith('.')]

    # Filter files created in the last 30 seconds
    recent_files = []
    current_time = time.time()
    for file in files:
        file_path = os.path.join(directory_path, file)
        file_creation_time = os.path.getctime(file_path)
        if current_time - file_creation_time <= 30:
            recent_files.append(file_path)  # Append full path

    if recent_files:
        # Sort the recent files based on their creation time
        recent_files.sort(key=lambda x: os.path.getctime(x), reverse=True)
        most_recent_file_path = recent_files[0]
        print("The most recent file created in the last 30 seconds (excluding dotfiles) is:", most_recent_file_path)
    else:

        exit(1)

download_file(atemlibzip)
time.sleep(8)

try:
    zip_file_path = get_downloaded_file()

    # Replace 'extraction_path' with the directory where you want to extract the contents
    extraction_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), atemlib)


    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)
except: 
        try:
            os.rename(source_directory, os.path.join(destination_directory, os.path.basename(source_directory)))
            print(f"The directory '{source_directory}' has been moved to '{destination_directory}'.")
        except Exception as e:
            print(f"Error: Failed to move directory - {e}") 

print(f"Files extracted to '{extraction_path}'")