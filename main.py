import sys
import scan
import shutil
import normalize
from pathlib import Path

def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize.normalize(path.name.replace(".zip", ''))

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def print_list(list):
    res_str = "\n"
    for el in list:
        res_str += f"\t{el}\n"

    return res_str
        
def write_to_file():

    with open(path+"\list.txt", 'w') as fh:
        fh.write(f"Image: {print_list(scan.Image)}\n")
        fh.write(f"Video_files: {print_list(scan.Video_files)}\n")
        fh.write(f"Documents: {print_list(scan.Documents)}\n")
        fh.write(f"Music: {print_list(scan.Music)}\n")
        fh.write(f"Archives: {print_list(scan.Archives)}\n")
        fh.write(f"Other: {print_list(scan.Unknown_extensions)}\n")

        #fh.write(f"Folder: {folders}\n")

        fh.write(f"All extensions: {print_list(scan.extensions)}\n")
        fh.write(f"Unknown extensions: {print_list(scan.unknown)}\n")


def main(folder_path):
    print(folder_path)
    scan.scan(folder_path)

    # print(f"Image: {Image}")
    # print(f"Video_files: {Video_files}")
    # print(f"Documents: {Documents}")
    # print(f"Music: {Music}")
    # print(f"Archives: {Archives}")
    # print(f"Unknown_extensions: {Unknown_extensions}")

    for file in scan.Image:
        handle_file(file, folder_path, "Image")

    for file in scan.Video_files:
        handle_file(file, folder_path, "Video_files")

    for file in scan.Documents:
        handle_file(file, folder_path, "Documents")

    for file in scan.Music:
        handle_file(file, folder_path, "Music")

    for file in scan.Unknown_extensions:
        handle_file(file, folder_path, "Unknown_extensions")

    for file in scan.Archives:
        handle_archive(file, folder_path, "Unpack_Archive")

    remove_empty_folders(folder_path)

    write_to_file()

    

if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
    main(folder.resolve())




