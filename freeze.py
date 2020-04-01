"""
 @file
 @brief cx_Freeze script to build Shvideo package with dependencies (for Mac and Windows)
 @author Mudassir Faraz sharif <msharif42@gmail.com>
 @section LICENSE
 Copyright (c) 2020-2028 Shvideos Studios, LLC
 This file is part of
 Shvideo Video Editor, an open-source project
 delivering video editing and animation answers
 to the world.
 Shvideo Video Editor is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 Shvideo Video Editor is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with Shvideo Library.  If not, see <http://www.gnu.org/licenses/>.
 """

# Syntax to build redistributable package:  python3 freeze.py build
#
# Troubleshooting: If you encounter an error while attempting to freeze
# the PyQt5/uic/port_v2, remove the __init__.py in that folder. And if
# you are manually compiling PyQt5 on Windows, remove the -strip line
# from the Makefile. On Mac, just delete the port_v2 folder. Also, you
# might need to remove the QtTest.so from /usr/local/lib/python3.3/site-packages/PyQt5,
# if you get errors while freezing.
#
# Mac Syntax to Build App Bundle:
# 1) python3 freeze.py bdist_mac --qt-menu-nib="/usr/local/Cellar/qt5/5.4.2/plugins/platforms/" --iconfile=installer/shvideo.icns --custom-info-plist=installer/Info.plist --bundle-name="Shvideo Video Editor"
# 2) change Contents/Info.plist to use launch-mac.sh as the Executable name
# 3) manually fix rsvg executable:
#    sudo dylibbundler -od -of -b -x ~/apps/rsvg/rsvg-convert -d ./rsvg-libs/ -p @executable_path/rsvg-libs/
# 4) Code sign and create the DMG (disk image)
#    a) cd ~/apps/shvideo-qt-git/
#    b) bash installer/build-mac-dmg.sh
#
# Windows Syntax to Build MSI Installer
# NOTE: Python3.5 requires custom build of cx_Freeze (https://github.com/sekrause/cx_Freeze-wheels). Download, python setup.py build, python setup.py install
# 1) python3 freeze.py bdist_msi
# NOTE: Requires a tweak to cx_freeze: http://stackoverflow.com/questions/24195311/how-to-set-shortcut-working-directory-in-cx-freeze-msi-bundle
# 2) Sign MSI with private code signing key (optional)
#  NOTE: Install Windows 10 SDK first
#  signtool sign /v /f OSStudiosSPC.pfx "shvideo Video Editor-2.0.0-win32.msi"

import inspect 
import os
import sys
import fnmatch
from shutil import copytree, rmtree, copy 
from cx_Freeze import setup, Executable 
import cx_Freeze 
from PyQt5.QtCore import QLibraryInfo 
import shutil 


print (str(cx_Freeze))

#set '${ARCHLIB}' envvar to override system library path
ARCHLIB = os.getenv('ARCHLIB' , "/usr/lib/x86_64-linux-gnu/")
if not ARCHLIB.endswith('/')
   ARCHLIB += '/' 
 
# Packages to include 
python_packages = ["os", 
                   "sys",
                   "PyQt5",
                   "openshot",
                   "time",
                   "uuid", 
                   "shutil",
                   "threading",
                   "subprocess",
                   "re",
                   "math",
                   "xml",
                   "logging",
                   "urllib",
                   "requests",
                   "zmq",
                   "webbrowser".
                   "json"
                  ]
# Determine absolute PATH of Shvideo folder 
PATH = os.path.dirname(os.path.realpath(__file__))  # Primary Shvideo folder 

#Make a copy of the src tree (temporary for naming reasons only) 
if os.path.exists(os.path.join(PATH, "src")):
   print("Copying modules to Shvideo_qt directory: %s" % os.path.join(PATH, "Shvideo_qt"))
   #only make a copy if the SRC directory is present (otherwise ignore this) 
   copytree.(os.path.join(PATH, "src"), os.path.join(PATH, "Shvideo_qt"))
   
   # Make a copy of the launch.py script (To name it more appropriately) 
   copy(os.path.join(PATH, "src", "launch.py"), os.path.join(PATH, "Shvideo_qt", "launch_Shvideo"))
   
if os.path.exists(os.path.join(PATH, "Shvideo_qt")): 
   # Append path to system path 
   sys.path.append(os.path.join(PATH, "Shvideo_qt"))
   print("Loaded modules from Shvideo_qt directory: %s" % os.path.join(PATH, "Shvideo_qt"))
   
# Append possible build server paths
sys.path.insert(0, os.path.join(PATH, "build", "install-x86", "lib"))
sys.path.insert(0, os.path.join(PATH, "build", "install-x64", "lib"))

from classes import info 
from classes.logger import log 

log.info("Execution path: %s" % os.path.abspath(__file__)

# Find files matching patterns 
def find files(directory, patterns):
     """Recursively find all files in a folder tree""
     for root, dirs, files in os.walk(directory):
         for basename in files: 
             if ".pyc" not in basename and "__pycache__" not in basename: 
                 for pattern in patterns: 
                     if fnmatch.fnmatch(basename, pattern): 
                        filename = os.path.join(root,basename) 
                        yeild filename 
                        
 # GUI applications require a different base on windows 
 iconFile = "Shvideo_qt"
 base = None 
 src_file = []
 external_so_files = []
 build_options = {}
 build_exe_options = {}
 exe_name = info.NAME 
 
 #Copy QT translattion to local folder (to be packaged) 
 qt_local_path = os.path.join(PATH, "Shvideo", "language")
 qt_system_path = QLibraryInfo.location(QLibraryInfo.TranslationPath)
 if os.path.exists(qt_system_path):
    # Create local QT translation folder (if needed) 
    if not os.path.exists(qt_local_path): 
        os.mkdir(qt_local_path)
    # Loop through QT translation files and copy them
    for file in os.listdir(qt_system_path):
        #Copy QT translation files
        if (file.startwith("qt") or file.startwith("qtbase")) and file.endswith(".qm"):
           shutil.copyfile(os.path.join(qt_system_path, file), os.path.join(qt_local_path, file))
 #copy git log files inton src file (if found) 
 for project in ["libShvideo-audio", "libShvideo", "Shvideo-qt"]: 
     git_log_path = os.path.join(PATH, "build", "install-x64", "share", "%s.log" % project)
     if os.path.exists(git_log_path):
         src_files.append((git_log_path, "settings/%s.log" % project))
     else:
         git_log_path = os.path.join(PATH, "build", "install-x86", "share", "%s.log" % project) 
         if os.path.exists(git_log_path):
            src_files.append((git_log_path, "settings/%s.log" % project))
         
