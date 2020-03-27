REM Make a fresh virtual environment
python -m venv env
call .\env\Scripts\activate.bat
python -m pip install --upgrade pip

REM Install dependencies (--no-deps + manual specification helps keep install size down)
pip install --no-deps psychopy
pip install pyglet==1.3.2 pillow psychtoolbox numpy six scipy json_tricks python-bidi pandas

REM Use pre-baked spec file
pip install pyinstaller
pyinstaller main.spec

REM Compile a launcher (so the user doesn't need to find the "real" executable)
cp Exp.cs dist/Exp.cs
cd dist
call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat"
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\Tools\VsDevCmd.bat"
csc.exe /target:winexe Exp.cs
dir
rm Exp.cs
cd ..
