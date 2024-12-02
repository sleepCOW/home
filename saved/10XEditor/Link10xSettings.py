import os

# Get the current user's AppData folder path
appdata_dir = os.getenv("APPDATA")
if not appdata_dir:
    raise EnvironmentError("Could not find the AppData directory.")

# Define paths relative to the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
link_targets = [
    os.path.join(script_dir, "KeyMappings.10x_settings"),
    os.path.join(script_dir, "Settings.10x_settings")
]

# Define the original file locations dynamically based on AppData path
original_files = [
    os.path.join(appdata_dir, "10x", "Settings", "KeyMappings.10x_settings"),
    os.path.join(appdata_dir, "10x", "Settings", "Settings.10x_settings")
]

def create_symbolic_link(original, target):
    try:
        # Remove the original file if it exists
        if os.path.exists(original):
            os.remove(original)
            print(f"Deleted original file: {original}")
        
        # Create a symbolic link
        os.symlink(target, original)
        print(f"Created symbolic link: {original} -> {target}")
    except Exception as e:
        print(f"Error creating symbolic link for {original}: {e}")

def create_python_script_links():
    python_scripts_dir = os.path.join(script_dir, "PythonScripts")
    target_base_dir = os.path.join(appdata_dir, "10x", "PythonScripts")
    
    if not os.path.exists(python_scripts_dir):
        print(f"PythonScripts directory not found: {python_scripts_dir}")
        return

    if not os.path.exists(target_base_dir):
        os.makedirs(target_base_dir)
        print(f"Created target base directory: {target_base_dir}")

    for filename in os.listdir(python_scripts_dir):
        if filename.endswith(".py"):
            source_path = os.path.join(python_scripts_dir, filename)
            target_path = os.path.join(target_base_dir, filename)

            try:
                # Remove the original file if it exists
                if os.path.exists(target_path):
                    os.remove(target_path)
                    print(f"Deleted existing link: {target_path}")
                
                # Create a symbolic link
                os.symlink(source_path, target_path)
                print(f"Created symbolic link for script: {source_path} -> {target_path}")
            except Exception as e:
                print(f"Error creating symbolic link for script {source_path}: {e}")

if __name__ == "__main__":
    # Create symbolic links for settings files
    for original, target in zip(original_files, link_targets):
        create_symbolic_link(original, target)
    
    # Create symbolic links for Python scripts
    create_python_script_links()