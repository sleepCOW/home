import os
import argparse
import sys


def create_symlink(source, target):
    """Creates a symbolic link to the source in the target directory."""
    if not os.path.exists(source):
        print(f"Error: Source '{source}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(target):
        print(f"Error: Target '{target}' is not a valid directory.")
        sys.exit(1)

    link_name = os.path.join(target, os.path.basename(source))

    try:
        os.symlink(source, link_name)
        print(f"Symlink created: {link_name} -> {source}")
    except Exception as e:
        print(f"Failed to create symlink: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Create a symbolic link to a file or directory.")
    parser.add_argument("--s", "--source", required=True, help="Path to the file or directory to create a symbolic link for")
    parser.add_argument("--t", "--target", required=True, help="Path to the folder where the symlink will be created")

    args = parser.parse_args()

    create_symlink(args.s, args.t)


if __name__ == "__main__":
    main()
