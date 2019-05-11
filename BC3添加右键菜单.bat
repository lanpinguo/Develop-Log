@ECHO OFF
rem 请将此脚本放在BC的目录执行，例如 F:\Software\Beyond Compare

REM 将当前路径设为变量
SET BC3PATH=%~DP0
REM 创建用户配置文件，关闭初次启动程序时的设置向导
if exist "%USERPROFILE%\Application Data\Scooter Software\Beyond Compare 3" RD /q /s "%USERPROFILE%\Application Data\Scooter Software\Beyond Compare 3"
IF NOT EXIST "%USERPROFILE%\Application Data\Scooter Software\Beyond Compare 3" MD "%USERPROFILE%\Application Data\Scooter Software\Beyond Compare 3"
COPY /Y NUL "%USERPROFILE%\Application Data\Scooter Software\Beyond Compare 3\BCState.xml"
(
ECHO ^<?xml version="1.0" encoding="UTF-8"?^>
ECHO ^<!-- Produced by Beyond Compare 3 from Scooter Software --^>
ECHO ^<BCState^>
ECHO ^<TBcState^>
ECHO ^<FirstStartup Value="False"/^>
ECHO ^<FormPosStr Value="110;111;980;737"/^>
ECHO ^</TBcState^>
ECHO ^</BCState^>
) >> "%USERPROFILE%\Application Data\Scooter Software\Beyond Compare 3\BCState.xml"

REM 注册右键
reg add "HKLM\Software\Scooter Software\Beyond Compare 3" /v "ExePath" /t REG_SZ /d "%cd%\BCompare.exe" /f
rem reg add "HKLM\Software\Scooter Software\Beyond Compare 3" /v "Version" /t REG_SZ /d "3.1.7.10865" /f
reg add "HKCU\Software\Scooter Software\Beyond Compare 3" /v "ExePath" /t REG_SZ /d "%cd%\BCompare.exe" /f
rem reg add "HKCU\Software\Scooter Software\Beyond Compare 3" /v "Version" /t REG_SZ /d "3.1.7.10865" /f
reg add "HKCR\.bcpkg" /ve /t REG_SZ /d "BeyondCompare.SettingsPackage" /f
reg add "HKCR\BeyondCompare.SettingsPackage" /ve /t REG_SZ /d "Beyond Compare Settings Package" /f
reg add "HKCR\BeyondCompare.SettingsPackage\DefaultIcon" /ve /t REG_SZ /d "%cd%\BCompare.exe,0" /f
reg add "HKCR\BeyondCompare.SettingsPackage\shell\open\command" /ve /t REG_SZ /d "\"%cd%\BCompare.exe\" \"%%1\"" /f
reg add "HKCR\.bcss" /ve /t REG_SZ /d "BeyondCompare.Snapshot" /f
reg add "HKCR\BeyondCompare.Snapshot" /ve /t REG_SZ /d "Beyond Compare Snapshot" /f
reg add "HKCR\BeyondCompare.Snapshot\DefaultIcon" /ve /t REG_SZ /d "%cd%\BCompare.exe,0" /f
reg add "HKCR\BeyondCompare.Snapshot\shell\open\command" /ve /t REG_SZ /d "\"%cd%\BCompare.exe\" \"%%1\"" /f
reg add "HKLM\System\CurrentControlSet\Services\EventLog\Application\Beyond Compare 3" /v "EventMessageFile" /t REG_SZ /d "%cd%\BCompare.exe" /f
reg add "HKLM\System\CurrentControlSet\Services\EventLog\Application\Beyond Compare 3" /v "TypesSupported" /t REG_DWORD /d 7 /f