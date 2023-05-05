from io import StringIO


def download_url(url: str, save_path: str, chunk_size: int=128) -> None:
    try:
        import requests
    except Exception as e:
        print(e)
        exit()

    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def run_main(user: str, host: str, nameOfKey: str, startAFresh: bool = False) -> None:
    try:
        import os
        import sys
        import shutil
        import subprocess
    except Exception as e:
        print(e)
        exit()
    print("***ENVIRONMENT:")
    print("Python: "+ str(sys.version # type: ignore
))
  
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
    print("Current working directory: "+cwd)

    save_path = os.path.join(cwd+"/download.zip")
    print("Will save to: "+url)

    pathToKey = os.path.join(cwd + "/" + nameOfKey)
    print("Checking that key is in place: "+ pathToKey)
    try: 
        os.path.exists(pathToKey)
        print("Key is in correct destination.")
    except Exception as e:
        print(e)
        exit()

    print("Ensuring key permissions: "+ pathToKey)
    try: 
        print("Trying to set key file permissionss to 400 (read-only).")
        os.chmod(pathToKey, 0o400)
    except Exception as e:
        print(e)
        exit()

    if(os.access(pathToKey, os.R_OK) and not (os.access(pathToKey, os.W_OK) or os.access(pathToKey, os.X_OK))):
        print("Key file permissions set correctly.")
    else:
        print("Couldn't automatically set key file permissions using method 1. Trying next method...")
        try:
            chmodProcess = subprocess.Popen(["chmod",'400',pathToKey], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            chmodProcess.communicate()
            if(os.access(pathToKey, os.R_OK) and not (os.access(pathToKey, os.W_OK) or os.access(pathToKey, os.X_OK))):
                print("File permissions set successfully.")
            else:
                raise

        except Exception as e:
            print(e)
            print("ERROR: Could not automatically sort file permissions. Please manually set the permissions of the following file to 600 (read-only) by running this command: ")
            print("chmod 400 "+pathToKey)
            exit()

    print("Downloading scripts...")
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
    print("Copying awsconfig file to project folder")
    try: 
        shutil.copyfile(src="awsconfig", dst=os.path.join(unpackedDir + '/awsconfig'))
        print("Extracted successfully.")
    except Exception as e:
        print(e)
        exit()
        
    print("Moving into folder: "+ unpackedDir)
    try: 
        venvPath = os.path.join(cwd + "/.venv")
        #if(os.path.exists(venvPath)): shutil.rmtree(path=venvPath, ignore_errors=True)
        os.chdir(unpackedDir)
        print("Moved into folder successfully.")

              
        print("Attempting to set-up virtual environment: "+venvPath)
        pOpenVenv = subprocess.Popen([sys.executable, "-m", "venv", venvPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pOpenVenv.communicate()
        if(os.path.exists(os.path.join(venvPath + "/bin/activate"))):
            print("Virtual environment created successfully.")
        else:
            print("Error creating the virtual environment. Could not find .venv/bin/activate file for activation.")
            exit()

        print("Installing the PIP requirements of the main project")
        try:
            import sys
            pathOfRequirements = os.path.join(unpackedDir + "/requirements.txt")
            with subprocess.Popen([f"source {venvPath}/bin/activate; pip3 install -vvv -r {pathOfRequirements} --require-virtualenv"], shell=True, executable="/bin/bash", bufsize=1,
           universal_newlines=True, stderr=subprocess.PIPE) as p, StringIO() as buf:
                if(p.stdout is not None):
                    for line in p.stdout:
                        print(line, end='')
                        buf.write(line)
            os.chdir(unpackedDir)
            print("Successfully ran `"+ "source ", venvPath + "/bin/activate; "+ "pip3 ", "install ", "-r ", pathOfRequirements +"`")
            print(".*.*.*.*.*.*.*")
            print("Installation successful.")
        except Exception as e:
            print(e)
            os.chdir(cwd)
            exit()
            
        print("Installing the requirements of dependencies")
        try:
            import subprocess
            import sys
            ibc_public = os.path.join(unpackedDir + "/scripts/src/public_analysis_code")
            os.chdir(ibc_public)
            pathOfDepRequirements = os.path.join(ibc_public + "/requirements.txt")
            with subprocess.Popen([f"source {venvPath}/bin/activate; pip3 install -vvv -r {pathOfDepRequirements}  --require-virtualenv"], shell=True, executable="/bin/bash", bufsize=1, universal_newlines=True, stderr=subprocess.PIPE) as p, StringIO() as buf:
                if(p.stdout is not None):
                    for line in p.stdout:
                        print(line, end='')
                        buf.write(line)

            os.chdir(unpackedDir)
            
            popen1 = subprocess.Popen([f"source {venvPath}/bin/activate; which pip3; pip3 list"], shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            popen1.communicate()
            print("Successfully ran `"+ "pip3 ", "install ", "-r ", pathOfDepRequirements +"`")
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
            print("User: " + user)
            print("Host: " + host)
            print("NOTE: Passwordless authentication will be used, reading the key file from: ")
            print("pathToKey: " + pathToKey)
            mainFilePath = os.path.join(scriptRoot + "/__main__.py")
            mainFile = subprocess.Popen([f". {venvPath}/bin/activate; {sys.executable} {mainFilePath} -U {user} -H {host} -K {pathToKey}"], shell=True)
            mainFile.communicate()
            print("Reached end of __main__.py.")
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
            parser.add_argument("-S", "--startAFresh", type=bool, default=False)
            args = parser.parse_args()
            user = args.user
            host = args.host
            nameOfKey = args.nameOfKey
            startAFresh = args.startAFresh
        else:
            import os
            from dotenv import load_dotenv
            k = load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__))+"/.env"))
            user = os.getenv('DEFAULT_USER') or "ENV_ERROR"
            host = os.getenv('DEFAULT_HOST') or "ENV_ERROR"
            nameOfKey = os.getenv('DEFAULT_NAME_OF_KEY') or "ENV_ERROR"
            startAFresh = bool(os.getenv('DEFAULT_START_A_FRESH')) or False

        print("Launching runner using: ")
        print("User: "+user)
        print("Host: "+host)
        print("nameOfKey: "+nameOfKey)
        run_main(user, host, nameOfKey, startAFresh)
    except Exception as e:
        raise