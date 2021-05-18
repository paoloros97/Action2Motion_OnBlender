bl_info = {
    'name': 'Action2Motion - Progetto 6',
    'category': 'All',
    "version": (1, 0),
    "blender": (2, 92, 0),
}

modulesNames = ['animazione']
 
import sys
import importlib
import subprocess
import bpy
from bpy.utils import register_class, unregister_class
import os

try: #Prova ad importare la libreria, altrimenti la installa
    import pandas as pd
except ImportError:
 
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

    try:
        sp = subprocess.Popen(['nvidia-smi', '-q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out_str = sp.communicate()
        out_list = out_str[0].decode("utf-8").split('\n')

        out_dict = {}

        for item in out_list:
            try:
                key, val = item.split(':')
                key, val = key.strip(), val.strip()
                out_dict[key] = val
            except:
                pass
        has_CUDA = False
        try:
            has_CUDA = 'CUDA Version' in out_dict
        except:
            pass
        if has_CUDA:
            try:
                import ensurepip
                ensurepip.bootstrap()
                os.environ.pop("PIP_REQ_TRACKER", None)
            except ImportError:
                pass    
            pybin = bpy.app.binary_path_python
            
            if float(out_dict['CUDA Version']) < 11.0 and float(out_dict['CUDA Version']) >= 10.0:
                print('Installazione PyTorch con CUDA v10')
                subprocess.check_call([pybin,'-m','pip','install','torch==1.8.1+cu102', '-f', 'https://download.pytorch.org/whl/torch_stable.html'])
            elif float(out_dict['CUDA Version']) >= 11.0:
                print('Installazione PyTorch con CUDA v11')
                subprocess.check_call([pybin,'-m','pip','install','torch==1.8.1+cu111', '-f', 'https://download.pytorch.org/whl/torch_stable.html'])
            else:
                print('Installazione PyTorch CPU (CUDA presente ma con versione non disponibile)')
                subprocess.check_call([pybin,'-m','pip','install','torch==1.8.1+cpu', '-f', 'https://download.pytorch.org/whl/torch_stable.html'])

            import torch
        else:
            raise Exception()
 
    except:
        try:
            import ensurepip
            ensurepip.bootstrap()
            os.environ.pop("PIP_REQ_TRACKER", None)
        except ImportError:
            pass    
        pybin = bpy.app.binary_path_python
        print('Installazione PyTorch CPU')
        subprocess.check_call([pybin,'-m','pip','install','torch==1.8.1+cpu', '-f', 'https://download.pytorch.org/whl/torch_stable.html'])
        import torch


try:
    import scipy.io as sio
except ImportError:

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
