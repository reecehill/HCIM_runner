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

def run_main(user: str, host: str, nameOfKey: str) -> None:
    print("Cleaning directory.")
    try:
        shutil.rmtree(path=os.path.join(os.getcwd() + "/Human-Connectome-Investigating-Modularity-version-2"), ignore_errors=True)
    except Exception as e:
        print(e)
        print("Unable to delete directory. Please manually clear the folder; however,dDo NOT delete requirements.txt, run.py, or the key file.")
        exit()

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

        pathToKey = os.path.join(cwd + "/" + nameOfKey)
        print("Checking that key is in place: "+ pathToKey)
        try: 
            os.path.exists(pathToKey)
            print("Key is in correct destination.")
        except Exception as e:
            print(e)
            os.chdir(scriptRoot)
            exit()


        print("RUNNING MAIN PYTHON FILE: __main__.py")
        try: 
            print("User: " + user)
            print("Host: " + host)
            print("NOTE: Passwordless authentication will be used, reading the key file from: ")
            print("pathToKey: " + pathToKey)
            mainFile = subprocess.Popen(['python', "__main__.py", "-U", user, "-H", host, "-K", pathToKey])
            mainFile.communicate()
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

if __name__ == "__main__":
    try:
        import sys
        if len( sys.argv ) > 1:
            import argparse
            parser = argparse.ArgumentParser()
            parser.add_argument("-U", "--user", type=str, default="CLI_ARGUMENT_ERROR")
            parser.add_argument("-H", "--host", type=str, default="CLI_ARGUMENT_ERROR")
            parser.add_argument("-K", "--nameOfKey", type=str, default="CLI_ARGUMENT_ERROR")
            args = parser.parse_args()
            user = args.user
            host = args.host
            nameOfKey = args.nameOfKey
        else:
            import os
            from dotenv import load_dotenv
            k = load_dotenv(os.getcwd()+"/../.env")
            user = os.getenv('DEFAULT_USER') or "ENV_ERROR"
            host = os.getenv('DEFAULT_HOST') or "ENV_ERROR"
            nameOfKey = os.getenv('DEFAULT_NAME_OF_KEY') or "ENV_ERROR"

        print("Launching runner using: ")
        print("User: "+user)
        print("Host: "+host)
        print("nameOfKey: "+nameOfKey)
        run_main(user, host, nameOfKey)
    except Exception as e:
        raise
    
