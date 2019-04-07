from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["pygame, random, math"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "Pursuit and Evasion",
    options = options,
    version = "1",
    description = 'The algorithm for Pursuit and Evasion, using Python 3 and pygame',
    executables = executables
)
