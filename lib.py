import subprocess
import requests
import sys
import os


def get_pip():
    imported = False
    try:
        import pip

        imported = True
    except ImportError:
        try:
            print("Baixando pip...")

            script_url = "https://bootstrap.pypa.io/get-pip.py"

            response = requests.get(script_url)
            if response.status_code == 200:
                with open("get-pip.py", "wb") as f:
                    f.write(response.content)

                subprocess.check_call([sys.executable, "get-pip.py"])

                os.remove("get-pip.py")
                imported = True
        except ImportError:
            pass

    return imported


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        install(package)

def download_packages(required_packages):
    if not get_pip():
        raise ImportError("Não foi possível instalar o pip.")

    # importar pacotes necessários
    for package in required_packages:
        import_or_install(package)

# imports
download_packages(["pygame"])

import pygame
import math
import tkinter as tk
from tkinter import Canvas
from constants import *
from classes import *
# from functions import *