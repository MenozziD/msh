@echo off

scp ..\server\msh\msh.py pi@192.168.1.106:/home/pi/server/msh/msh.py
scp -r ..\server\msh\controller pi@192.168.1.106:/home/pi/server/msh/
scp -r ..\server\msh\module pi@192.168.1.106:/home/pi/server/msh/
scp -r ..\server\msh\webui pi@192.168.1.106:/home/pi/server/msh/