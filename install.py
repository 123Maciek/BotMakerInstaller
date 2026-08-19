"""BotMaker installer.

Replaces the old install.py, which: (a) pip-installed its ~10 dependencies one
subprocess call at a time (and installer.bat *also* pip-installed the same
list before calling this script — a redundant double install), and (b)
unconditionally shutil.rmtree()'d the whole target folder before cloning fresh,
wiping any existing install (including, hypothetically, real user data) on
every run with no rollback if the clone then failed.

This version: installs from a single requirements.txt (the installer's own
pywin32/winshell dependencies, plus whatever BotMaker's own requirements.txt
asks for once it's been cloned), and never deletes an existing install until a
fresh, verified copy is confirmed good.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

BOTMAKER_REPO_URL = "https://github.com/123Maciek/BotMaker"
INSTALLER_REQUIREMENTS = Path(__file__).with_name("requirements-installer.txt")


class InstallError(Exception):
    pass


def pip_install(requirements_path):
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise InstallError(f"pip install failed for {requirements_path}")


def clone_botmaker(destination):
    import git
    try:
        git.Repo.clone_from(BOTMAKER_REPO_URL, str(destination))
    except Exception as e:
        raise InstallError(f"Failed to download BotMaker: {e}") from e


def verify_botmaker(folder):
    if not (folder / "main.py").is_file():
        raise InstallError(f"Downloaded copy at {folder} is missing main.py.")
    if not (folder / "version.txt").is_file():
        raise InstallError(f"Downloaded copy at {folder} is missing version.txt.")
    if not (folder / "requirements.txt").is_file():
        raise InstallError(f"Downloaded copy at {folder} is missing requirements.txt.")


def install_or_update(target_dir: Path):
    """Clone BotMaker into target_dir. If target_dir already exists, stage the
    download alongside it and atomically swap it in, so a failed download or
    an interrupted swap never leaves an existing install half-deleted."""
    if not target_dir.exists():
        print(f"Installing BotMaker into {target_dir} ...")
        clone_botmaker(target_dir)
        verify_botmaker(target_dir)
        return

    print(f"Existing install found at {target_dir} — staging an update ...")
    staging = target_dir.with_name(target_dir.name + ".staging")
    if staging.exists():
        shutil.rmtree(staging, ignore_errors=True)
    clone_botmaker(staging)
    verify_botmaker(staging)

    old = target_dir.with_name(target_dir.name + ".old")
    if old.exists():
        shutil.rmtree(old, ignore_errors=True)
    try:
        os.rename(target_dir, old)
    except OSError as e:
        raise InstallError(f"Could not move the existing install aside: {e}. "
                            "Your existing installation was not modified.") from e
    try:
        os.rename(staging, target_dir)
    except OSError as e:
        os.rename(old, target_dir)  # roll back
        raise InstallError(f"Could not move the update into place: {e}. "
                            "Rolled back — your existing installation is unchanged.") from e
    shutil.rmtree(old, ignore_errors=True)


def write_start_script(target_dir: Path):
    start_bat = target_dir / "start.bat"
    start_bat.write_text(
        "@echo off\n"
        f'cd /d "{target_dir}"\n'
        f'"{sys.executable}" "{target_dir / "main.py"}"\n',
        encoding="utf-8",
    )


def create_desktop_shortcut(target_dir: Path):
    try:
        import winshell
        from win32com.client import Dispatch
    except ImportError as e:
        print(f"Skipping desktop shortcut: {e}")
        return

    try:
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "BotMaker.lnk")
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.TargetPath = str(target_dir / "window.vbs")
        shortcut.WorkingDirectory = str(target_dir)
        icon_path = target_dir / "icon.ico"
        if icon_path.is_file():
            shortcut.IconLocation = str(icon_path)
        shortcut.save()
        print(f"Desktop shortcut created: {shortcut_path}")
    except Exception as e:
        print(f"Could not create desktop shortcut: {e}")


def main():
    print("BOTMAKER INSTALLER\n")

    try:
        print("Installing installer dependencies (pywin32, winshell) ...")
        pip_install(INSTALLER_REQUIREMENTS)

        documents = Path(os.getenv("USERPROFILE", str(Path.home()))) / "Documents"
        target_dir = documents / "BotMakerFiles"

        install_or_update(target_dir)

        print("Installing BotMaker's own dependencies ...")
        pip_install(target_dir / "requirements.txt")

        write_start_script(target_dir)
        create_desktop_shortcut(target_dir)
    except InstallError as e:
        print(f"\nInstallation failed: {e}")
        sys.exit(1)

    print("\nInstallation finished successfully :)")


if __name__ == "__main__":
    main()
