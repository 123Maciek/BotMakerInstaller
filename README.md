I will guide you how to install open source BotMaker

1. Download python 3.12 !!! FOLLOW INSTRUCTION TO ENSURE THAT PYTHON AND PIP IS ADDED TO THE PATH !!!
go to https://www.python.org/downloads/ and click yellow button "Download python 3.x.x (latest version)"
run the .exe file and then:
 * click "Custom Installation"
 * In the Optional Features click Next
 * In the Advanced Options click "Precompile standard library" and "Add Python to environment variables" !!!
 * click Install button and wait for python to install
2. Download git
go to https://git-scm.com/download/win and download one of this:
 * 32-bit Git for Windows Setup
 * 64-bit Git for Windows Setup (Recommended)
Open the .exe file that it downloaded and install it with deafult options
3. Check your installations
Open cmd (win + r and type cmd and click enter) and type:
 * py --version (Correct output: Python 3.x.x) (Incorrect output: )
 * git --version (Correct output: git version 2.x.x.windows.1)
4. Download my package
On the page https://www.github.com/123Maciek/BotMakerInstaller click on green button "Code" and at the bottom click download zip folder
then upack it.
5. Open installer.bat
This program will run install.py program.
install.py program install all required python libraries and will clone github repository (https://github.com/123Maciek/BotMaker)
to your folder in Documents called BotMakerFiles and in this folder will edit start.bat to be compatible with its current localization
and will create a shortcut of window.vbs on your desktop with icon called icon.ico