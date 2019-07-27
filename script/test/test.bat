@ECHO OFF
SET PATH_DIR="C:\\Progetti\\msh\\server\\msh\\"
SET WINSCPCMD="C:\\Program Files (x86)\\WinSCP\\WinSCP.com"
SET RASPBERRY_SERVER="RASP_LOCAL"
%WINSCPCMD% /script=script_test.txt /parameter %RASPBERRY_SERVER% %CD% %PATH_DIR%
python convert.py %PATH_DIR%
cd %PATH_DIR%
coverage xml -i
sonar-scanner && del .coverage && del coverage.xml && del test-report.xml
exit 0