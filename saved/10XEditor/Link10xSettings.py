import os

# Define file paths
# TODO: Replace with search through registry for installation path, see N10X Unreal plugin for exact places
original_files = [
    r"C:\Users\fgfg1\AppData\Roaming\10x\Settings\KeyMappings.10x_settings",
    r"C:\Users\fgfg1\AppData\Roaming\10x\Settings\Settings.10x_settings"
]
link_targets = [
    r"E:\Work\Projects\home\saved\10XEditor\KeyMappings.10x_settings",
    r"E:\Work\Projects\home\saved\10XEditor\Settings.10x_settings"
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

if __name__ == "__main__":
    for original, target in zip(original_files, link_targets):
        create_symbolic_link(original, target)