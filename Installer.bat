@echo off
setlocal EnableDelayedExpansion

cd C:\

:: URLs for the installers
set GIT_URL=https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/Git-2.45.2-64-bit.exe
set PYTHON_URL=https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe
set MYSQL_URL= https://dev.mysql.com/get/Downloads/MySQL-9.0/mysql-9.0.0-winx64.msi
set GIT_REPO_URL=https://github.com/R3tr0gh057/LibraryManagementSystem.git

:: File names
set GIT_INSTALLER=Git-2.45.2-64-bit.exe
set PYTHON_INSTALLER=python-3.11.4-amd64.exe
set MYSQL_INSTALLER=mysql-9.0.0-winx64.msi

:: Download Git installer
echo Downloading Git...
powershell -Command "Invoke-WebRequest -Uri %GIT_URL% -OutFile %GIT_INSTALLER%"
if not exist %GIT_INSTALLER% (
    echo Failed to download Git installer.
)
echo Installing Git...
start /wait %GIT_INSTALLER% /VERYSILENT
if %errorlevel% neq 0 (
    echo Failed to install Git.
)

:: Add Git to PATH
set PATH=%PATH%;C:\Program Files\Git\cmd

:: Clone Git repository
echo Cloning Git repository...
git clone %GIT_REPO_URL%
if %errorlevel% neq 0 (
    echo Failed to clone Git repository.
)
cd LibraryManagementSystem

:: Download Python installer
echo Downloading Python...
powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"
if not exist %PYTHON_INSTALLER% (
    echo Failed to download Python installer.
)
echo Installing Python...
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
if %errorlevel% neq 0 (
    echo Failed to install Python.
)

:: Add Python to PATH
set PATH=%PATH%;C:\Program Files\Python311\Scripts

:: Check if pip is installed
echo Checking for pip...
pip --version
if %errorlevel% neq 0 (
    echo pip not found.
)

:: Install Python requirements
echo Installing Python requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install Python requirements.
)

:: Download MySQL installer
cd ..
echo Downloading MySQL...
powershell -Command "Invoke-WebRequest -Uri %MYSQL_URL% -OutFile %MYSQL_INSTALLER%"
if not exist %MYSQL_INSTALLER% (
    echo Failed to download MySQL installer.
)

:: Verify the installer path
if not exist "%cd%\%MYSQL_INSTALLER%" (
    echo Installer file not found at "%cd%\%MYSQL_INSTALLER%"
    pause
    exit /b 1
)

echo Installing MySQL...
msiexec /i "%cd%\%MYSQL_INSTALLER%" /quiet /norestart /log install.log
if %errorlevel% neq 0 (
    echo Failed to install MySQL.
)

:: Wait for MySQL to finish installation
timeout /t 60

:: Start MySQL service
set PATH=%PATH%;"C:\Program Files\MySQL\MySQL Server 9.0\bin"

:: Configure MySQL
echo Configuring MySQL...
echo Open MySql Configurator and set the password to tiger
pause
mysql -u root -ptiger -e "CREATE DATABASE lms;"
mysql -u root -ptiger -e "USE lms; CREATE TABLE details (uid VARCHAR(255) PRIMARY KEY NOT NULL, no VARCHAR(255) NOT NULL);"


:: Installation successful
echo Installation successful!
echo Installed Python packages:
pip list
echo Installed MySQL and set up database 'lms' with table 'details'.

endlocal
pause