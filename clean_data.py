import os


def remove_files_and_folders(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            os.rmdir(folder_path)
