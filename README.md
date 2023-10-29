#ATEM-Loader

This script allows you to use Google Slides to create overlay graphics for your ATEM Swticher, pull them, convert them to PNG, and upload them to the ATEM (using the  [atemlib MediaUpload.exe](https://github.com/mintopia/atemlib) executable), all with one click.

Make sure your slides are set to 1080

##Requirements
- webbrowser
- os
- time import sleep
- subprocess import run, Popen
- pdf2image import convert_from_path
- PyPDF2 import PdfReader
- re
- yaml

##Setup
1. Download this repository
2. Run setup.py to set up the environment
3. Copy config_example.yml to config.yml
4. Open config.yml and change settings 
5. Prepare slides in [Google Slides](https://slides.google.com)
6. Run!


##Usage

###Prepare Slides
WHen you create your slides, in order to set the desired filenames, create a text box, where the text color matches the background (black on black in most cases), and type:

   FILENAME: MyFilename

Where "MyFilename" is what you want this slide to be called on the ATEM. It's a good idea to put this in the notes section too so you can tell which slide this is supposed to be without having to change the text color.


###Get slides
1. Open ATEM Software and ensure the ATEM is reachable
2. Double click LoadItUp.py (or run `python LoadItUp.py` from command line)

