@echo off
setlocal

:: URLs for the installers
set PYTHON_URL=https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe
set MYSQL_URL=https://dev.mysql.com/get/mysql-installer-web-community-8.0.28.0.msi
set GIT_REPO_URL=https://github.com/R3tr0gh057/LibraryManagementSystem.git

:: File names
set PYTHON_INSTALLER=python-3.11.4-amd64.exe
set MYSQL_INSTALLER=mysql-installer-web-community-8.0.28.0.msi

:: Clone Git repository
echo Cloning Git repository...
git clone %GIT_REPO_URL%
cd LibraryManagementSystem

:: Download Python installer
echo Downloading Python...
powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"
echo Installing Python...
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
del %PYTHON_INSTALLER%

:: Install Python requirements
echo Installing Python requirements...
@REM pip install --upgrade pip
pip install -r requirements.txt

:: Download MySQL installer
cd ..
echo Downloading MySQL...
powershell -Command "Invoke-WebRequest -Uri %MYSQL_URL% -OutFile %MYSQL_INSTALLER%"
echo Installing MySQL...
start /wait msiexec /i %MYSQL_INSTALLER% /quiet
del %MYSQL_INSTALLER%

:: Wait for MySQL to finish installation
timeout /t 60

:: Configure MySQL
echo Configuring MySQL...
mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'tiger';"
mysql -u root -ptiger -e "CREATE DATABASE lms;"
mysql -u root -ptiger -e "USE lms; CREATE TABLE details (uid VARCHAR(255) PRIMARY KEY NOT NULL, no VARCHAR(255) NOT NULL);"

:: Cleanup
echo Cleaning up...
@REM del %PYTHON_INSTALLER%
del %MYSQL_INSTALLER%

:: Installation successful
echo Installation successful!
echo Installed Python packages:
pip list
echo Installed MySQL and set up database 'lms' with table 'details'.

endlocal
pause
