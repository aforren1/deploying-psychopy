
Locally:
1. Create a new virtual environment (`python -m venv env`)
2. Activate the environment (`.\env\Scripts\activate.bat`)
3. Install known dependencies (e.g. `pip install --no-deps psychopy`)
    - `--no-deps`, and then iteratively figuring out dependencies, allows us to keep the bundled size down
4. Run the experiment to figure out missing dependencies
5. Install pyinstaller (`pip install pyinstaller`)
6. Generate an initial spec file (`pyinstaller <main>.py --onedir --noconsole`)
7. Tweak the spec file
    - e.g. set pathex to `[]`, make sure data files are included
8. Re-run pyinstaller (`pyinstaller <main>.spec --noconfirm`)
9. Make sure the launcher (`Exp.cs`) has the name you want (and the paths in `Path.Combine` are correct)

These are optional locally (though nice for testing)
9. Copy the .cs file into dist/
10. Compile via `csc.exe /target:winexe <name>.cs`
11. Remove the defunct .cs file (`rm <name>.cs`)
12. Test (`<name>.exe`)

For remote build:
1. Tweak the [build_win.bat](https://github.com/aforren1/deploying-psychopy/blob/master/build_win.bat) and [appveyor.yml](https://github.com/aforren1/deploying-psychopy/blob/master/.appveyor.yml) to meet your specific needs (note the Python version in Appveyor, the bundled exe name, etc.).
2. Make sure your Appveyor account is hooked up to build your repository
