import webbrowser
import os
import time
import platform
from os.path import expanduser
from time import sleep
from subprocess import run, Popen, CalledProcessError
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import re
import yaml

from datetime import datetime


def find_executable(file_path):
    try:
        # Attempt to run the variable as an executable
        run([file_path], check=True)
        return f"Variable '{file_path}' is an executable"

    except (CalledProcessError, FileNotFoundError):
        # If the variable is not an executable, try to find it in the script's directory
        script_directory = os.path.dirname(os.path.abspath(__file__))
        script_executable = os.path.join(script_directory, file_path)
        
        if os.path.isfile(script_executable) and os.access(script_executable, os.X_OK):
            print(f"Executable found in script directory: '{script_executable}'")
            return script_executable
        else:
            return f"Error"


def download_slides_as_pdf(presentation_url):
    
    # dlfile = os.path.join(downloads_dir, filename)

    # if os.path.isfile(dlfile):
    #     os.remove(dlfile)
        
    geturl= 'https://docs.google.com/presentation/d/' + presentation_url + '/export/pdf'

    # Safari on mac isn't playing well with webbrowser, so using a system call
    if platform.system() == 'Darwin':
        os.system('open -a {} {}'.format(edge_path, geturl))
    else:
        webbrowser.register('edge', None,webbrowser.BackgroundBrowser(edge_path))
        # Open the presentation URL in Microsoft Edge
        webbrowser.get('edge').open(geturl)
        # Wait for the user to manually save the presentation as PDF

def convert_images(pdf_file, output_directory):

    fdate = datetime.now().strftime("%y%m%d")
    print(fdate)
    # Define the output directory for PNG images
    output_directory = os.path.join(output_directory, fdate)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print("Directory created:", output_directory)
    else:
        print("Directory already exists:", output_directory)
        exit(1)

    # Set the resolution for the output PNG images (suitable for HDTV fullscreen display)
    resolution = (1920, 1080)

    # Convert the PDF to PNG images
    images = convert_from_path(pdf_file, dpi=300, output_folder=None, fmt='png', size=resolution)

    # Load the PDF using PdfReader
    with open(pdf_file, 'rb') as file:
        pdf_reader = PdfReader(file)

        # Iterate over the pages of the PDF
        for i, page in enumerate(pdf_reader.pages):
            # Extract the hidden word from the page's content (modify the pattern as needed)
            match = re.search(r'FILENAME: ([\w_]+)', page.extract_text())
            if match:
                word = match.group(1)
            else:
                word = f"output_{i+1}"  # Use a default name if no hidden word is found

            # Create the file name using the extracted word
            file_name = f"{word}.png"
            file_path = os.path.join(output_directory, file_name)

            # Save the image with the file name
            images[i].save(file_path, "PNG")

    print("PDF converted to PNG images successfully:")
    return output_directory
    #print(output_directory.replace(r'/', '\\'))
    return output_directory
    

def push_to_atem(imgdir, media_pool):

    for filename in os.listdir(imgdir):
        name, ext = os.path.splitext(filename)
        if name in media_pool:
            fullfile = os.path.join(imgdir, filename)
            print('Adding ' + fullfile + ' to slot ' + str(media_pool[name]))
            cmd = ' '.join([media_upload, atem_ip, str(media_pool[name]), fullfile]) 
            run(cmd)

# This is a fn to get the most recent file created in the default downloads directory
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

    return most_recent_file_path
##################################
script_directory = os.path.dirname(os.path.realpath(__file__))
output_directory = os.path.join(script_directory, 'output')

with open('config-tmp.yml', 'r') as file:
    config = yaml.safe_load(file)
atem_ip = config['atem_ip']
google_slides_id = config['google_slides_id']
media_upload = config['media_upload']
media_pool = config['media_pool']
if 'output_tdir' in config:
    output_directory = config['output_dir']

media_upload = find_executable(media_upload)


# Ensure output location exitsts
if not os.path.exists(output_directory):
    try:
        # Create the directory
        os.makedirs(output_directory)
        print(f"Directory '{output_directory}' created successfully.")
    except OSError as e:
        print(f"Directory '{output_directory}' creation failed: {e}")
else:
    print(f"Directory '{output_directory}' already exists.")

# Set up Web Browser per OS
try:
    edge_path
except:
    stype = platform.system()
    if stype == 'Darwin':
        edge_path = '/Applications/Safari.app'
    elif stype == 'Windows':
        edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"  # Replace with the path to your Edge executable
    else:
        print('What system are we on?', file=sys.stderr )
        exit(1)
    print('Autodetected platform: {}. Using browser to download: {}'.format(stype, edge_path))

download_slides_as_pdf(google_slides_id)

i=0


sleep(8)
dlfile = get_downloaded_file()
print('Looking for ' + dlfile)

if os.path.isfile(dlfile):
    print('Slides downloaded. Converting them now...')
    imgdir = convert_images(dlfile, output_directory)
    print('\n\n\nImages converted--uploading to ATEM')
    sleep(2)
    push_to_atem(imgdir, media_pool)
    
else:
    print('There was an error downloading the slides.')

