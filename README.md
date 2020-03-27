
1. Create virtualenv
2. Activate that
3. pip install --no-deps psychopy
4. Run exp, figuring out deps
5. pip install pyinstaller
6. pyinstaller main.py --onedir --noconsole (to generate initial spec)
7. Set pathex to [], add data files
8. pyinstaller main.spec
9. 