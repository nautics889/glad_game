from cx_Freeze import setup, Executable

'''Setup parameters for cx_Freeze'''
setup(
    name = "glad",
    version = "1.0",
    description = "GladArcade",
    executables = [Executable("main.py")]
)