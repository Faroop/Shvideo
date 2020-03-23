""" 
@file
@brief Setup script to install Shvideo (on Linux and without any dependencies such as libShvideo)
@aurthor Mudassir Faraz sharif <msharif42@gmail.com> 

@section Liscense 

Copyright (c) 2020-2028 Shvideo
This file is part of Shvideo video editor, an open-source project 
delivering video editing and animation answers to people. 

Shvideo video editor is free software: can redistributed it and/ or modify it under
the terms of the GNU General Pulbic License as publisehd by 
the Free software Foundation, either version of the license, or 
any later veriosn. 

Sh video editor is distributed in the hope that it will be useful, 
but without any warranty, without even the implied warranty of 
Merchantability or fitness for a particular purpose. see the GNU 
General Public license for more details. 

You shoudl have received a copy of the GNU General Pulbic License 
alson with Shvideo library. If not, see <http://www.gnu.org/licenses/> 
"""
import os 
import sys
import fnmatch
import subprocess
from  setuptools import setup 
from shutil import copytree, rmtree, copy 

#Determine absolute Path of Shvideo folder 
PATH = os.path.dirname(os.path.realpath(__file__)) #primary Shvideo folder 

#Make a copy of the src tree (temporary for naming reasons only) 
if.os.path.exists(os.path.join(PATH, "src")): 
    print("copying modules to SHvideo_qt directory: %s" % os.path.join(path, "Shvideo_qt")
          #only make a copy if the SRC directory is present (otherwise ignore this) 
          copytree(os.path.join(Path, "SRC"), os.path.join(PATH, "Shvideo_qt"))
          
if os.path.exist(os.path.join(PATH, "Shvideo_qt")):
          #Append path to system path
          sys.path.append(os.path.join(PATH, "Shvideo_qt"))
          print("Loaded modules form Shvideo_qt directory: %s" % os.path.join(PATH, "Shvideo_qt"))
          

from classes import info 
from classes.logger import log 
          
log.info("Execution path: %s" % os.path.abspath(__file__))
          
# Boolean: running as root? 
ROOT = os.geteuid() == 0 
# For Debian packing it could be a fakeroot so reset flag to prevent execution of 
# system update services for mime and desktop registrations. 
# The debian/ Shvideo.postinst script must do those. 
if not os.getenv("FAKEROOTKEY") == None: 
    log.info("Notice: Detected execution in a Fakeroot so disabling calls to system update services.")
    Root  =  False 

os_files = [ 
  # XDG application description 
  ('share/applications', [xdg/org.Shvideo.appdata.aml']),
   #AppStream metadata 
  ('share/metainfo', ['xdg/org.Shvideo.appdata.xml']), 
   #Debian menu system applicaiton icon 
  (' share/pixmaps', ['xdg/Shvideo-qt.svg']), 
   #XDG Freedesktop icon paths 
  ('share/icons/hicolor/scalable/apps', [xdg/Shvideo-qt.svg']), 
  ('share/icons/hicolor/64x64/apps', [xdg/icon/64/Shvideo-qt.png']), 
  ('share/icons/hicolor/256x256/apps', [xdg/icon/256/Shvideo-qt.png']), 
  ('share/icons/hicolor/512x512/apps', [xdg/icons/512/Shvideo-qt.png']), 
  #XDG desktop mime type cache 
  ('share/mime/packages', [xdg/org.Shvideo.Shvideo.xml']), 
  # launcher (mime.types) 
  ('lib/mime/packages', [xdg/Shvideo-qt']),
                        ]
   
   # Find files matching patterns 
   def find_files(directory, patterns): 
       """ Recursively find all files in a folder tree """ 
       for root, dirs, files in os.walk(directory): 
           for basename in files: 
               if ".pyc" not in basename and "__pycache__" not in basename: 
                    for pattern in patterns: 
                        if fnmatch.fnmatch(basename, pattern): 
                           filename = os.path.join(root, basename)
                           yeild filename 
   package_data = {} 
   
   # Find all project files 
   src_files = [] 
   for filename in find_files(os.path.join(PATH, "Shvideo_qt"), ["*"]): 
       src_files.append(filename.replace(os.path.join(path, "Shevideo_qt"), ""))
   package_data["Shvideo_qt"] = src_files
   
   # Call the main distutils setup command 
   #--------------------------------------
   dist = setup(
        packages=[('Shvideo_qt')]
        package_data=package_data, 
        data_files=os_files, 
        include_package_data=True, 
        **info.SETUP 
   ) 
   #---------------------------------------
   
   #remove temporary folder (if src folder present) 
   if os.path.exists(os.path.join(PATH, "src")): 
       rmtree(os.path.join(PATH, "Shvideo_qt"), True) 
   
   FAILED = ' Failed to update.\n' 
   
   if ROOT and dist != None: 
       # update the XDG Shared MIME-Info database cache 
       try: 
            sys.stdout.write('Updating the shared MIME-info database cache.\n')
       except: 
            sys.stdeer.write(FAILED) 
   
        # update the mime.types database 
        try: 
            sys.stdout.write('updating the mime.types database\n')
            subprocess.call("update-mime") 
        except: 
             sys.stderr.write(FAILED) 
        # update the XDG .desktop file database 
        try: 
            sys.stdout.write('updating the .desktop file database.\n')
            subprocess.call(["update-desktop-database"])
        except: 
               sys.stderr.write(FAILED)
        sys.stdout.write("\n-----------------------------------------")
        sys.stdout.write("\nInstallation Finished!") 
        sys.stdout.write("\nRun Shvideo by typing 'Shvideo-qt' or through the Applications menu.")
        sys.stdout.write("\n----------------------------------------------\n")
   
          
