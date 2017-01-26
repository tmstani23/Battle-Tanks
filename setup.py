import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\tmstani23\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\tmstani23\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tk8.6"

executables = [cx_Freeze.Executable("Tanks.py")]

cx_Freeze.setup(
    name = "Battle Tanks",
    options = {"build_exe": {"packages": ["pygame", "os", "sys"], "include_files": ["explosion1.ogg", "explosion4.ogg", "nightsky.jpg", "tank1real.png", "tank2real.png", "gameicon.jpg"]}},
    description ="Battle Tank Game",
    executables = executables
)

#shift right click open command window in root file 
#type python setup.py build   to create a build folder with all the files or,
#type python setup.py bdist_msi in the command window to create the windows installer