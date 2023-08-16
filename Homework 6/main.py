import shutil
import sys
import scan
import normalize
from pathlib import Path


# обробляємо файли і переносимо їх у відповідну папку залежно від категорії
def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    
    if dist == "OTHERS":
        new_name = path.name
    else:
        new_name = normalize.normalize(path.name)

    new_path = target_folder / new_name
    path.replace(new_path)

# обробляємо архіви та переміщуємо їх у створені папки
def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize.normalize(path.name.replace(".zip", '').replace(".tar", ''))
    
    archive_folder = root_folder / "ARCHIVE" / new_name
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

# рекурсивно видаляємо порожні папки
def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

# рекурсивно видаляє порожні папки з кореневої папки
def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass
#  обробляємо та сортуємо файли в папках
def main(folder_path):
    scan.scan(folder_path)

    for file in scan.jpeg_files:
        hande_file(file, folder_path, "JPEG")
    for file in scan.jpg_files:
        hande_file(file, folder_path, "JPG")
    for file in scan.png_files:
        hande_file(file, folder_path, "PNG")
    for file in scan.txt_files:
        hande_file(file, folder_path, "TXT")
    for file in scan.docx_files:
        hande_file(file, folder_path, "DOCX")
    for file in scan.mp3_files:
        hande_file(file, folder_path, "MP3")
    for file in scan.wav_files:
        hande_file(file, folder_path, "WAV")
    for file in scan.mp4_files:
        hande_file(file, folder_path, "MP4")
    for file in scan.avi_files:
        hande_file(file, folder_path, "AVI")
    for file in scan.zip_files:
        handle_archive(file, folder_path, "ARCHIVE")
    for file in scan.tar_files:
        handle_archive(file, folder_path, "ARCHIVE")    
    for file in scan.others:
        hande_file(file, folder_path, "OTHERS")

    get_folder_objects(folder_path)

if __name__ == '__main__':
    path = sys.argv[1]
    
    arg = Path(path)
    
    main(arg.resolve())
