REM Make a fresh virtual environment
rm -rf env
python -m venv env
call .\env\Scripts\activate.bat
python -m pip install --upgrade pip

REM Install dependencies (--no-deps + manual specification helps keep install size down)
python -m pip install --no-deps psychopy
python -m pip install -r requirements.txt

REM Use pre-baked spec file
python -m pip install pyinstaller
pyinstaller main.spec

REM Compile a launcher (so the user doesn't need to find the "real" executable)
cp Exp.cs dist/Exp.cs
cd dist

REM More for local testing-- I think there's a csc.exe on the path already in Appveyor
call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat"
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\Tools\VsDevCmd.bat"
csc.exe /target:winexe Exp.cs
dir
rm Exp.cs
cd ..
