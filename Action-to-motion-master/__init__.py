bl_info = {
    'name': 'Action2Motion - Progetto 6',
    'category': 'All',
    "version": (1, 0),
    "blender": (2, 92, 0),
}

modulesNames = ['animazione']
 
import sys
import importlib
import bpy
from bpy.utils import register_class, unregister_class
import os

try: #Prova ad importare la libreria, altrimenti la installa
    import pandas as pd
except ImportError:
    import subprocess
    import bpy 
    try:
        import ensurepip
        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)
    except ImportError:
        pass    
    pybin = bpy.app.binary_path_python
    subprocess.check_call([pybin,'-m','pip','install','pandas'])
    import pandas as pd  


try:
    import torch
except ImportError:
    import subprocess
    import bpy 
    try:
        import ensurepip
        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)
    except ImportError:
        pass    
    pybin = bpy.app.binary_path_python
    subprocess.check_call([pybin,'-m','pip','install','torch==1.8.1+cu111', '-f', 'https://download.pytorch.org/whl/torch_stable.html'])
    import torch


try:
    import scipy.io as sio
except ImportError:
    import subprocess
    import bpy 
    try:
        import ensurepip
        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)
    except ImportError:
        pass    
    pybin = bpy.app.binary_path_python
    subprocess.check_call([pybin,'-m','pip','install','scipy'])
    import scipy.io as sio 

try:
    import joblib
except ImportError:
    import subprocess
    import bpy 
    try:
        import ensurepip
        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)
    except ImportError:
        pass    
    pybin = bpy.app.binary_path_python
    subprocess.check_call([pybin,'-m','pip','install','joblib'])
    import joblib
    



modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
 
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)
 
def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()
 
def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":
    register()
