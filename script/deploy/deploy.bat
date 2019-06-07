@ECHO OFF
SET WINSCPCMD="C:\\Program Files (x86)\\WinSCP\\WinSCP.com"
SET ZIPCMD="C:\\Program Files (x86)\\7zip\\7z.exe"
SET RASPBERRY_SERVER="Raspberry Pi0"
SET PATH_DIR="C:\\Users\\Simone.simone\\Documents\\Repository\\msh\\server\\msh\\*"
%ZIPCMD% a msh.zip %PATH_DIR% 1> nul 2> nul
%WINSCPCMD% /script=script_raspberry.txt /parameter %RASPBERRY_SERVER% %CD% 1> nul 2> nul
del msh.zip
exit