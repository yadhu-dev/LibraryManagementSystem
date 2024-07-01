@echo off
setlocal

:: URLs for the installers
set GIT_URL=https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/Git-2.45.2-64-bit.exe
set PYTHON_URL=https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe
set MYSQL_URL=https://dev.mysql.com/get/mysql-installer-web-community-8.0.28.0.msi
set GIT_REPO_URL=https://github.com/R3tr0gh057/LibraryManagementSystem.git

:: File names
set GIT_INSTALLER=Git-2.45.2-64-bit.exe
set PYTHON_INSTALLER=python-3.11.4-amd64.exe
set MYSQL_INSTALLER=mysql-installer-web-community-8.0.28.0.msi

:: Download Git installer
echo Downloading Git...
powershell -Command "Invoke-WebRequest -Uri %GIT_URL% -OutFile %GIT_INSTALLER%"
if not exist %GIT_INSTALLER% (
    echo Failed to download Git installer. Exiting...
    exit /b 1
)
echo Installing Git...
start /wait %GIT_INSTALLER% /VERYSILENT
if %errorlevel% neq 0 (
    echo Failed to install Git. Exiting...
    exit /b %errorlevel%
)
del %GIT_INSTALLER%

:: Add Git to PATH
set PATH=%PATH%;C:\Program Files\Git\cmd

:: Clone Git repository
echo Cloning Git repository...
git clone %GIT_REPO_URL%
if %errorlevel% neq 0 (
    echo Failed to clone Git repository. Exiting...
    exit /b %errorlevel%
)
cd LibraryManagementSystem

:: Download Python installer
echo Downloading Python...
powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"
if not exist %PYTHON_INSTALLER% (
    echo Failed to download Python installer. Exiting...
    exit /b 1
)
echo Installing Python...
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
if %errorlevel% neq 0 (
    echo Failed to install Python. Exiting...
    exit /b %errorlevel%
)
del %PYTHON_INSTALLER%

:: Add Python to PATH
set PATH=%PATH%;C:\Python311;C:\Python311\Scripts

:: Check if pip is installed
echo Checking for pip...
pip --version
if %errorlevel% neq 0 (
    echo pip not found. Exiting...
    exit /b %errorlevel%
)

:: Install Python requirements
echo Installing Python requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install Python requirements. Exiting...
    exit /b %errorlevel%
)

:: Download MySQL installer
cd ..
echo Downloading MySQL...
powershell -Command "Invoke-WebRequest -Uri %MYSQL_URL% -OutFile %MYSQL_INSTALLER%"
if not exist %MYSQL_INSTALLER% (
    echo Failed to download MySQL installer. Exiting...
    exit /b 1
)
echo Installing MySQL...
start /wait msiexec /i %MYSQL_INSTALLER% /quiet
if %errorlevel% neq 0 (
    echo Failed to install MySQL. Exiting...
    exit /b %errorlevel%
)
del %MYSQL_INSTALLER%

:: Wait for MySQL to finish installation
timeout /t 60

:: Start MySQL service
net start MySQL80

:: Configure MySQL
echo Configuring MySQL...
mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'tiger';"
mysql -u root -ptiger -e "CREATE DATABASE lms;"
mysql -u root -ptiger -e "USE lms; CREATE TABLE details (uid VARCHAR(255) PRIMARY KEY NOT NULL, no VARCHAR(255) NOT NULL);"

:: Cleanup
echo Cleaning up...
del %MYSQL_INSTALLER%

:: Installation successful
echo Installation successful!
echo Installed Python packages:
pip list
echo Installed MySQL and set up database 'lms' with table 'details'.

endlocal
pause
