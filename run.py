try:
    import requests
    import os
    import shutil
    import argparse
except Exception as e:
    print(e)
    exit()

def download_url(url: str, save_path: str, chunk_size: int=128) -> None:
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

parser = argparse.ArgumentParser()
parser.add_argument("user", type=str)
parser.add_argument("host", type=str)
parser.add_argument("password", type=str)
args = parser.parse_args()

print("Preparing environment.")

# Github URL .zip to download
url = 'https://github.com/reecehill/Human-Connectome-Investigating-Modularity/archive/refs/heads/version-2.zip'
print("Will call Github at: "+url)

cwd = os.getcwd()
print("Current working directory: "+url)

save_path = os.path.join(cwd+"/download.zip")
print("Will save to: "+url)

print("Downloading...")
try:
    download_url(url=url, save_path=save_path)
    print("Downloaded successfully.")
except Exception as e:
    print(e)
    exit()

print("Extracting download.zip to current directory")
try: 
    shutil.unpack_archive(filename=save_path)
    print("Extracted successfully.")
except Exception as e:
    print(e)
    exit()

unpackedDir = os.path.join(cwd + "/Human-Connectome-Investigating-Modularity-version-2")
print("Moving into folder: "+ unpackedDir)
try: 
    os.chdir(unpackedDir)
    print("Moved into folder successfully.")
    print("Install using PIP the requirements of the project")
    try:
        import subprocess
        import sys
        pathOfRequirements = os.path.join(unpackedDir + "/requirements.txt")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "-r", pathOfRequirements])
        os.chdir(unpackedDir)
        print("Successfully ran `"+ sys.executable, " -m", "pip ", "install ", "-U ", "-r ", pathOfRequirements +"`")
        print(".*.*.*.*.*.*.*")
        print("Installation successful.")
    except Exception as e:
        print(e)
        os.chdir(cwd)
        exit()

    scriptRoot = os.path.join(unpackedDir + "/scripts")
    print("Moving into script folder: "+ scriptRoot)
    try: 
        os.chdir(scriptRoot)
        print("Moved into folder successfully.")
    except Exception as e:
        print(e)
        os.chdir(scriptRoot)
        exit()

    print("RUNNING MAIN PYTHON FILE: __main__.py")
    try: 
        subprocess.Popen(['python', "__main__.py", args.user, args.host, args.password], stdout=subprocess.PIPE)
        print("Launched __main__.py successfully.")
    except Exception as e:
        print(e)
        os.chdir(cwd)
        exit()


    print("Returning to root: "+ cwd)
    try: 
        os.chdir(cwd)
        print("Moved back to root successfully.")
    except Exception as e:
        print(e)
        exit()

except Exception as e:
    print(e)
    os.chdir(cwd)
    exit()