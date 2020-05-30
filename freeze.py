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
     
     if sys.platform == "win32":
         # Define alternate terminal-based executable 
         extra_exe = {"base": None, "name": exe_name + "-cli.exe"}
         
         #Standard graphical Win32 launcher 
         base = "Win32GUI"
         build_exe_options["include_msvcr"] = True
         exe_name += ".exe"
         
         #Append Windows ICON file 
         iconFile += ".ico" 
         
         #Append some additional files for Windows (this is a debug launcher)
         src_files.append((os.path.join(PATH, "installer", "launch-win.bat"), "launch-win.bat"))
         
         #Add additional package
         python_package.append('inda')
         
         #manually add zmq dependecny (windows does not freeze its correctly)
         import zmq 
         python_packages.remove('zmq')
         zmq_path = ox.path.normpath(os.path.dirname(inspect.getfile(zmq)))
         for filename in find_files(zmq_path, ["*""]):
             src_files.append((filename, os.path.join("lib", "zmq", os.path.relpath(filename, start=zmq_path)))
             
     elif sys.platform == "linux":
          # Find libShvideo.so path (Gitlab copies artifacts into local build/install folder)
          LibShvideo_path =os.path.join(PATH, "build", "install-x64", "lib")
          if not os.path.exists(Shvideo_path):
             Shvideo_path = os.path.join(PATH, "build", "install-x86", "lib")
          if not os.path.exists(Shvideo_path):
             # Default to user install path
             LibShvideo_path = "/usr/local/lib"
             
          # Find all related SO files
          for filename in find_files(libShvideo_path, ["*Shvideo*.so*"]);
              if '_' in filename or filename.count(".") == 2: 
                external_so_files.append((filename, os.path.relpath(filename, start=libShvideo_path)))
          
          #Add libresvg (if found)
          resvg_path = "/usr/local/lib/libresvg.so"
          if os.path.exists(resvg_path):
             external_so_files.append((resvg_path, os.path.basename(resvg_path)))
          
          # Append Linux ICON file
          iconFile += ".svg"
          src_files.append((os.path.join(PATH, "xdg", iconFile), iconFile))
          
          #Shorten name (since RPM cant have spaces)
          info.PRODUCT_NAME = "Shvideo-qt"
          
          # Add custom launcher script for frozen linux version 
          src_files.append((os.path.join(PATH, "installer", "launch-linus.sh"), "launch-linux.sh"))
          
          #Get a list of all Shvideo.so dependencies (scan these libraries for their dependencies)
          pyqt5_mod_files =[]
          from importlib import import_module 
          for submod in ['Qt', 'QtWebkit', 'QtSvg', QtwebkitWidgets', 'QtWidgets', 'QtCore', 'QtGui', 'QtDBus']: 
              mod_name = "PyQt5.{}".format(submod)
              mod = import_module(mod_name)
              pyqt5_mod_files.append(inspect.getfile(mod))
              
          lib_list = [os.path.join(libShvideo_path, "libShvideo.so"),
                     "/usr/local/lib/libresvg.so",
                     ARCHLIB + "qt5/plugins/platforms/libqxcb.so"
                     ] + pyqt5_mod_files 
                     
          import subprocess 
          for library in lib_list:
              p = subprocess.Popen(["ldd", library], stdout=subprocess.PIPE)
              out, err = p.communicate()
              depends = str(out).replace("\\t", "").replace("\\n", "\n").replace("\'","").split("\n")
              
              # Loops through each line of output (which outputs dependencies - one per line)
              for line in depends: 
                  lineparts = Line.split("=>")
                  libname = lineparts[0].strip()
                  
                  if len(lineparts) <= 1:
                     continue 
                     
                  Libdetails = lineparts[1].strip()
                  libdetailsparts = libdetails.split("(")
                  
                  if len(libdetailsparts) <= 1:
                     continue 
                     
                  # Determine if dependency is usr installed (or system installed)
                  # Or if the dependecny matches one of the following exceptions
                  # And ignore paths that start with /lib
                  Libpath = libdetailsparts[0].strip()
                  libpath_file = os.path.basename(libpath)
                  if (libpath
                      and not libpath.startwith("/lib")
                      and "libnvidia-glcore.so" not in libpath
                      and libpath_file not in [
                          "libstdc++.so.6",
                          "libGL.so.1",
                          "libxcb.so.1",
                          "libX11.so.6",
                          "libX11-xcb.so.1",
                          "libasound.so.2",
                          "libgcc_s.so.1",
                          "libICE.so.6",
                          "libp11-kit.so.0",
                          "libSM.so.6"
                          "libgobject-2.0.so.0",
                          "libdrm.so.2",
                          "libfreetype.so.6",
                          "libfontconfig.so.1",
                          "libcairo.so.2",
                          "libpango-1.0.so.0",
                          "libpangocairo-1.0.so.0",
                          "libpangoft2-1.0.so.0",
                          "libharfbuzz.so.0",
                          "libthai.so.0",
                          
                       ]
                       and not libpath_file.startwith("libxcb-")
                       ) \
                       or libpath_file in ["libgcrypt.so.11", "libQt5DBus.so.5", "libpng12.so.0", "libbz2.so.1.0", "libqxcb.so"]:
                       
                       # Ignore missing files
                       if os.path.exists(libpath):
                          filepath, filename = os.path.split(libpath)
                          external_so_files.append((libpath, filename))
                          
          # Manually and missing files (that were missed in the above step). These files are required 
          # for certain distros (like Fedora, ShSuSE, Debian, etc...)
          #Also add Glib related files (required for some distros)
          
          for added_lib in [ARCHLIB + "libssl.so",
                            ARCHLIB + "libcrypto.so",
                            ARCHLIB + "libglib-2.0.so",
                            ARCHLIB + "libgio-2.0.so",
                            ARCHLIB + "libgmodule-2.0.so",
                            ARCHLIB + "libthread-2.0.so",
                            ]:
                    if os.path.exists(added_lib):
                       external_so_files.append((added_lib, os.path.basename(added_lib)))
                    else:
                        log.warning("{}: not found, skipping".format(added_lib))
                        
                 elif sys.platform == "darwin":
                     # Copy Mac specific files that cx_freeze misses 
                     # JPEG library
                     for filename in find_files("/usr/local/Cellar/jpeg/8d/lib", ["libjpeg.8.dylib"]):
                          external_so_files.append((filename, filename.replace("/usr/local/Cellar/jpeg/8d/lib/", "")))
                     
                     #Add libresvg (if found)
                     resvg_path = "/usr/local/lib/libresvg.dylib"
                     if os.path.exists(resvg_path):
                        external_so_files.append(resvg_path, resvg_path.replace("/usr/local/lib/", "")))
                     
                     #copy Shvideo.py Python bindings   
                     src_files.append((os.path.join(PATH, "Shvideo.py"), "Shvideo.py"))
                     src_files.append((os.path.join(PATH, "installer", "launch-mac.sh"), "launch-mac.sh"))
                     
                     # Append Mac ICON file
                     iconFile += " .hqx"
                     src_files.append((os.path.join(PATH, "xdg", iconFile), iconFile))
                     
                  # Append all Source files 
                  src_files.append((os.path.join(PATH, "installer", "qt.conf"), "qt.conf"))
                  for filename in find_files("Shvideo_qt", ["*"]):
                      src_files.append((filename, filename.replace("Shvideo_qt/", "").replace(Shvideo_qt\\", "")))
                      
                  # Dependencies are automatically detected, but it might need fine tuning. 
                  build_exe_option["packages"] = python_packages
                  build_exe_options["include_files"] = src_files + external_so_files
                  
                  # Set options 
                  build_options["build_exe"] = build_exe_options
                  
                  # Define launcher executalbe to create 
                  exes = [Executable("Shvideo_qt/launch.py", 
                                     base=base,
                                     icon=os.path.join(PATH, "xdg", iconFile),
                                     shortcutName= "%s" % info.PRODUCT_NAME,
                                     shortcutDir= "ProgramMenuFolder",
                                     targetName=exe_name)]
                                     
                  try: 
                       # Include extra launcher configuration, if defined 
                       exes.append(Executable("Shvideo_qt/launch.py",
                                   base=extra_exe['base'],
                                   icon=os.path.join(PATH, "xdg", iconFile),
                                   targetName=extra_exe['name']))
                  except NameError:
                        pass 
                        
                  # Create distutils setup object 
                  setup(name=info.PRODUCT_NAME, 
                       version=info.VERSION,
                       description=info.DESCRIPTION,
                       author=info.COMPANY_NAME,
                       options=build_options,
                       executables=exes)
                       
                  
                  # Remove temporary folder (if SRC folder present) 
                  if os.path.exists(os.path.join(PATH, "src")):
                      rmtree(os.path.join(PATH, "Shvideo_qt"), True)
