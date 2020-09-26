from cx_Freeze import setup, Executable
import sys
buildOptions = dict(packages = ["pandas","sys"]
                    ,includes = ["PyQt5"]
                    ,include_files = ["PoetTagger.ui"]
                    , excludes = [])  # 1

base = None
if sys.platform == "win32":
    base = "Win32GUI"
exe = [Executable("PoetTagger.py",base=base)]  # 2

# 3
setup(
    name='PoetTagger',
    version = '0.1',
    author = "aprilgom@gmail.com",
    options = dict(build_exe = buildOptions),
    executables = exe
)