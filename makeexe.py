from setuptools import setup
import py2exe

# Ensure the script you want to bundle is specified correctly
script_name = "kizagan_client_building.py"

setup(
    options={
        'pyzexe': {
            'bundle_files': 1,  # Bundles everything into a single file
            'compressed': True  # Compresses the resulting executable
        }
    },
    windows=[{'script': script_name}],  # Replace with your script file name
    zipfile=None,  # Do not create a separate .zip file
)
