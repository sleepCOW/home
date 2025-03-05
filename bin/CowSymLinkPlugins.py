from CowSymLink import create_symlink
import os
import argparse
import sys


def has_uplugin(folder_path):
    if not os.path.isdir(folder_path):
        return False

    for item in os.listdir(folder_path):
        if item.endswith(".uplugin"):
            return True


def symlink_uplugin(folder_name, folder_path, target_path):
    new_folder_path = os.path.join(target_path, folder_name)

    os.makedirs(new_folder_path, exist_ok=True)

    for item in os.listdir(folder_path):
        if item in ["Binaries", "Intermediate", ".git"]:
            continue  # Skip specified directories

        symlink_source = os.path.join(folder_path, item)
        create_symlink(symlink_source, new_folder_path)
        print(f'Created symlink for {symlink_source} in {target_path}')


def main():
    parser = argparse.ArgumentParser(
        description="Create a symbolic link for all plugins in the current directory to the target directory excluding temp files.")
    parser.add_argument("--s", "--source", required=True, help="Path to the file or directory where plugins located")
    parser.add_argument("--t", "--target", required=True, help="Path to the folder where the symlink will be created")

    args = parser.parse_args()
    source = args.s
    target = args.t

    source_directory = source

    # If source directory is a plugin itself just copy it
    if has_uplugin(source_directory):
        folder_name = os.path.basename(source_directory)
        symlink_uplugin(folder_name, source_directory, target)
        return

    # Iterate over items in directory
    for item in os.listdir(source_directory):
        folder_path = os.path.join(source_directory, item)

        if os.path.isdir(folder_path):
            # Skip folder with no .uplugin
            if not has_uplugin(folder_path):
                continue

            symlink_uplugin(item, folder_path, target)


if __name__ == "__main__":
    main()
