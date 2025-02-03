import os
import winreg

def add_bin_to_path():
    # Get the current user's PATH variable from the Windows Registry
    reg_key = r"Environment"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_READ) as key:
            current_path, _ = winreg.QueryValueEx(key, "Path")
    except FileNotFoundError:
        current_path = ""

    # Define the bin directory we want to add
    bin_path = os.path.join(os.path.expanduser("~"), "bin")

    # Check if the bin directory is already in PATH
    if bin_path.lower() in current_path.lower():
        print("The bin directory is already in the PATH.")
        return

    # Append bin to the PATH
    # Make sure each entry has only single ';'
    if current_path:
        if current_path[-1] != ';':
            new_path = current_path + ";" + bin_path + ";"
        else:
            new_path = current_path + bin_path + ";"
    else:
        new_path = bin_path + ";"

    # Update the registry with the new PATH
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        print(f"Successfully added {bin_path} to PATH.")
    except Exception as e:
        print(f"Error updating PATH: {e}")

if __name__ == "__main__":
    add_bin_to_path()