import ctypes
import os
import pathlib
import sys

def is_admin() -> bool:
    """Checking, if script is running in admin rooles"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    if not is_admin():
        print("Script needed admin rooles. Restarting...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )
        sys.exit()

    program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
    install_dir = pathlib.Path(program_files) / "Mieru"

    install_dir.mkdir(parents=True, exist_ok=True)
    print(f"Dir for installing: {install_dir}")

    current_dir = pathlib.Path(__file__).parent

    src_exe = current_dir / "mieru.exe"
    dst_exe = install_dir / "mieru.exe"
    if src_exe.exists():
        dst_exe.write_bytes(src_exe.read_bytes())
        print("Coopied mieru.exe")
    else:
        print("Error: file mieru.exe not found near script")
        input("Click Enter for exit...")
        sys.exit(1)

    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
            r"System\CurrentControlSet\Control\Session Manager\Environment",
            0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
                path_val, _ = winreg.QueryValue(key, "PATH")

                paths = [p.strip() for p in path_val.split(";") if p.strip()]
                if str(install_dir) not in paths:
                    paths.append(str(install_dir))
                    new_path = ";".join(paths)
                    winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                    print("Mieru successfully added in system PATH!")
                else:
                    print("Mieru was exist in PATH.")
    except Exception as e:
        print(f"Error updating PATH: {e}")

    print("\nInstallation completed successfully!")
    input("Click Enter to close the window...")


if __name__ == "__main__":
    main()
