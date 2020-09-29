SET mypath=%~dp0
echo %mypath:~0,-1%
cd %mypath:~0,-1%
:: Abilita risposta PING in Firewall
echo "Configurazione PC per SHUTDOWN"
netsh advfirewall firewall add rule name="All ICMP V4" protocol=icmpv4:any,any dir=in action=allow
:: Abilita WMI in Firewall
netsh advfirewall firewall set rule group="Strumentazione gestione Windows (WMI)" new enable=yes
netsh advfirewall firewall set rule group="Gestione remota registro eventi" new enable=yes
:: Configurazione per SHUTDOWN
:: The remote registry service must be enabled on each computer you want to shut down remotely – it’s disabled by default.
sc config RemoteRegistry start= auto
sc start RemoteRegistry
:: Impostare LocalAccountTokenFilterPolicy in registro
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1
::Guida per istruzioni Manuali
::https://www.groovypost.com/howto/enable-wake-on-lan-windows-10/
::echo "Abilito esecuzione script Powershell"
::PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList 'Set-ExecutionPolicy Unrestricted -Force' -Verb RunAs}"
echo "Eseguo script Microsoft per abilitare WOL-Errore"
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList 'Enable_WOL.ps1' -Verb RunAs}"
pause
