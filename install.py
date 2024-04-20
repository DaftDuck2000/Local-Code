import zipfile
import os
import subprocess

files = ["PyQt5.zip", "PyQt5_Qt5-5.15.2.dist-info.zip", "PyQt5_sip-12.13.0.dist-info.zip", "PyQt5-5.15.10.dist-info.zip", "QScintilla-2.14.1.dist-info.zip"]

def extract_zip(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

cwd = os.path.dirname(os.path.realpath(__file__))


for file in files:
    extract_zip(file, cwd)

for file in files:
    subprocess.call(["rmdir", files[file]])
