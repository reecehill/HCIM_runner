from io import StringIO


def download_url(url: str, save_path: str, chunk_size: int = 128) -> None:
    try:
        import requests
    except Exception as e:
        print(e)
        exit()

    r = requests.get(url, stream=True)
    with open(save_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def run_main(user: str, host: str, nameOfKey: str, startAFresh: str = "false") -> None:
    def setFilePermissions(file_path: str, file_name: str, permission: str):
        print("Checking that key is in place: " + file_path)
        try:
            os.path.exists(file_path)
            print(f"{file_name} is in correct destination.")
        except Exception as e:
            print(e)
            exit()

        print(f"Ensuring {file_name} permissions: " + file_path)
        try:
            print(
                f"Trying to set {file_name} file permissions to {permission} (read-only)."
            )
            os.chmod(file_path, int(permission, 8))
        except Exception as e:
            print(e)
            exit()

        if file_name == "Given key":
            if os.access(file_path, os.R_OK) and not (
                os.access(file_path, os.W_OK) or os.access(file_path, os.X_OK)
            ):
                print("Key file permissions set correctly.")
            else:
                print(
                    "Couldn't automatically set key file permissions using method 1. Trying next method..."
                )
                try:
                    chmodProcess = subprocess.Popen(
                        ["chmod", "400", file_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    chmodProcess.communicate()
                    if os.access(file_path, os.R_OK) and not (
                        os.access(file_path, os.W_OK) or os.access(file_path, os.X_OK)
                    ):
                        print("File permissions set successfully.")
                    else:
                        raise

                except Exception as e:
                    print(e)
                    print(
                        "ERROR: Could not automatically sort file permissions. Please manually set the permissions of the following file to 600 (read-only) by running this command: "
                    )
                    print("chmod 400 " + file_path)
                    exit()

    try:
        import os
        import sys
        import shutil
        import subprocess
    except Exception as e:
        print(e)
        exit()
    print("***ENVIRONMENT:")
    print("Python: " + str(sys.version))  # type: ignore

    if startAFresh == "true":
        print("Cleaning directory.")
        print(startAFresh)
        try:
            shutil.rmtree(
                path=os.path.join(
                    os.getcwd(), "Human-Connectome-Investigating-Modularity-version-2"
                ),
                ignore_errors=True,
            )
        except Exception as e:
            print(e)
            print(
                "Unable to delete directory. Please manually clear the folder; however,dDo NOT delete requirements.txt, run.py, or the key file."
            )
            exit()

    print("Preparing environment.")
    # Github URL .zip to download
    url = "https://github.com/reecehill/Human-Connectome-Investigating-Modularity/archive/refs/heads/version-2.zip"
    print("Will call Github at: " + url)

    cwd = os.getcwd()
    print("Current working directory: " + cwd)

    save_path = os.path.join(cwd, "download.zip")
    print("Will save to: " + url)

    pathToKey = os.path.join(cwd, nameOfKey)
    setFilePermissions(file_path=pathToKey, file_name="Given key", permission="400")
    scriptsNeedUnpacking = False
    if not os.path.exists(save_path) or startAFresh == "true":
        print("Downloading scripts...")
        try:
            download_url(url=url, save_path=save_path)
            print("Downloaded successfully.")
            scriptsNeedUnpacking = True
        except Exception as e:
            print(e)
            exit()
    else:

        print("No need to download scripts - .zip found in place.")

    if scriptsNeedUnpacking:
        print(
            "Extracting (and overwriting if existing) download.zip to current directory"
        )
        try:
            shutil.unpack_archive(filename=save_path)
            print("Extracted successfully.")
        except Exception as e:
            print(e)
            exit()
    else:
        print("No need to extract scripts.")

    unpackedDir = os.path.join(
        cwd, "Human-Connectome-Investigating-Modularity-version-2"
    )
    print("Copying awsconfig file to project folder")
    try:
        shutil.copyfile(src="awsconfig", dst=os.path.join(unpackedDir, "awsconfig"))
        print("Extracted successfully.")
    except Exception as e:
        print(e)
        exit()

    pathToCgalExe = os.path.join(
        unpackedDir, "scripts", "matlab", "toolboxes","FieldTrip","external","iso2mesh","bin","cgalmesh.mexglx"
    )
    setFilePermissions(file_path=pathToCgalExe, file_name="cgalExe", permission="751")
    pathToCgalExe = os.path.join(
        unpackedDir, "scripts","matlab","toolboxes","FieldTrip","external","iso2mesh","bin","cgalsimp2.mexglx"
    )
    setFilePermissions(file_path=pathToCgalExe, file_name="cgal2Exe", permission="751")

    print("Moving into folder: " + unpackedDir)
    try:
        venvPath = os.path.join(cwd, ".venv")
        # if(os.path.exists(venvPath)): shutil.rmtree(path=venvPath, ignore_errors=True)
        os.chdir(unpackedDir)
        print("Moved into folder successfully.")

        print("Attempting to set-up virtual environment: " + venvPath)
        pOpenVenv = subprocess.Popen(
            [sys.executable, "-m", "venv", venvPath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        pOpenVenv.communicate()

        if os.path.exists(os.path.join(venvPath, "bin", "activate")):
            print("Virtual environment created successfully.")
            pOpenVenvStart = subprocess.Popen(
                ["/bin/bash", "-c", f"source {os.path.join(venvPath, 'bin', 'activate')}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = pOpenVenvStart.communicate()

            pythonExecutableVenv = os.path.join(venvPath, "bin", "python3.10")
        else:
            print(
                "Error creating the virtual environment. Could not find .venv/bin/activate file for activation."
            )
            exit()

        print("Installing the PIP requirements of the main project")
        try:
            import sys

            pathOfRequirements = os.path.join(unpackedDir, "requirements.txt")
            with subprocess.Popen(
                [
                    f"{pythonExecutableVenv} -m pip install -vvv -r {pathOfRequirements} --require-virtualenv"
                ],
                shell=True,
                executable="/bin/bash",
                bufsize=1,
                universal_newlines=True,
                stderr=subprocess.PIPE,
            ) as p, StringIO() as buf:
                if p.stdout is not None:
                    for line in p.stdout:
                        print(line, end="")
                        buf.write(line)
            os.chdir(unpackedDir)
            print(
                "Successfully ran `" + "source ",
                venvPath + "/bin/activate; " + "{venvPath} -m pip ",
                "install ",
                "-r ",
                pathOfRequirements + "`",
            )
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

            os.chdir(unpackedDir)

            popen1 = subprocess.Popen(
                [
                    f"{pythonExecutableVenv} -m pip install -U pip; {pythonExecutableVenv} -m pip install -U setuptools; {pythonExecutableVenv} -m install boto3; {pythonExecutableVenv} -m pip list"
                ],
                shell=True,
                executable="/bin/bash",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            popen1.communicate()
            popen2 = subprocess.Popen(
                [
                    f"which {pythonExecutableVenv}"
                ],
                shell=True,
                executable="/bin/bash",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = popen2.communicate()
            print(
                "Successfully ran `" + pythonExecutableVenv + " -m pip ",
                "install ",
                "-r ",
                "`",
            )
            print(".*.*.*.*.*.*.*")
            print("Installation successful.")
        except Exception as e:
            print(e)
            os.chdir(cwd)
            exit()

        scriptRoot = os.path.join(unpackedDir, "scripts")
        print("Moving into script folder: " + scriptRoot)
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
            print(
                "NOTE: Passwordless authentication will be used, reading the key file from: "
            )
            print("pathToKey: " + pathToKey)
            mainFilePath = os.path.join(scriptRoot, "__main__.py")
            print("Ensuring __main__.py is executable.")
            try:
                chmodProcess = subprocess.Popen(
                    ["chmod", "751", mainFilePath],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                chmodProcess.communicate()
                if os.access(mainFilePath, os.X_OK):
                    print("File permissions set successfully.")
                else:
                    raise

            except Exception as e:
                print(e)
                print(
                    "ERROR: Could not automatically make __main__.py executable. Please manually set the permissions of the following file to 751 (read-only) by running this command: "
                )
                print("chmod 751 " + mainFilePath)
                exit()
            mainFile = subprocess.Popen(
                [
                    f"{pythonExecutableVenv} {mainFilePath} -U {user} -H {host} -K {pathToKey}"
                ],
                shell=True,
            )
            mainFile.communicate()
            print("Reached end of __main__.py.")
        except Exception as e:
            print(e)
            os.chdir(cwd)
            exit()

        print("Returning to root: " + cwd)
        try:
            os.chdir(cwd)
            print("Moved back to root successfully.")
        except Exception as e:
            print(e)
            exit()

        print("Deactivating venv")
        try:
            deactivateVenv = subprocess.Popen([f"deactivate"], shell=True)
            deactivateVenv.communicate()
            print("Venv deactivated.")
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

        if sys.version_info >= (3, 10):
            print("Compatible python version installed.")
        else:
            raise ValueError("Incorrect python version number. Requires >=3.11")

        if len(sys.argv) > 1:

            # TODO: Current config does NOT default to .env.
            import argparse

            parser = argparse.ArgumentParser()
            parser.add_argument(
                "-U", "--user", type=str, default="CLI_ARGUMENT_ERROR", required=True
            )
            parser.add_argument(
                "-H", "--host", type=str, default="CLI_ARGUMENT_ERROR", required=True
            )
            parser.add_argument(
                "-K",
                "--nameOfKey",
                type=str,
                default="CLI_ARGUMENT_ERROR",
                required=True,
            )
            parser.add_argument(
                "-S",
                "--startAFresh",
                type=str,
                choices=["false", "true"],
                default="CLI_ARGUMENT_ERROR",
            )
            args = parser.parse_args()
            user = args.user
            host = args.host
            nameOfKey = args.nameOfKey
            startAFresh = args.startAFresh
        else:
            import os
            from dotenv import load_dotenv

            k = load_dotenv(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
            )
            user = os.getenv("DEFAULT_USER") or "ENV_ERROR"
            host = os.getenv("DEFAULT_HOST") or "ENV_ERROR"
            nameOfKey = os.getenv("DEFAULT_NAME_OF_KEY") or "ENV_ERROR"
            startAFresh = os.getenv("DEFAULT_START_A_FRESH") or "false"

        print("Launching runner using: ")
        print("User: " + user)
        print("Host: " + host)
        print("nameOfKey: " + nameOfKey)
        run_main(user, host, nameOfKey, startAFresh)
    except Exception as e:
        raise
