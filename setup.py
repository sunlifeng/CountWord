from distutils.core import setup

import py2exe

import matplotlib

includes = ["encodings", "encodings.*"]  
excludes = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
            "pywin.dialogs", "pywin.dialogs.list", 
            "Tkconstants","Tkinter","tcl"
           ]


options = {"py2exe":
    {"compressed": 1,
     "optimize": 2,
     "ascii": 1,
     "includes":includes,
     "excludes":excludes,
     "bundle_files": 1 
    }}
setup(
    options = options,
    zipfile=None,
    #data_files=matplotlib.get_py2exe_datafiles(),
    windows=[{"script": "CountWord.py" }]
    )
