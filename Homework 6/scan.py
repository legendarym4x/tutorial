import sys
from pathlib import Path


jpeg_files = list()
png_files = list()
jpg_files = list()
txt_files = list()
docx_files = list()
mp3_files = list()
wav_files = list()
mp4_files = list()
avi_files = list()
folders = list()
zip_files = list()
tar_files = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    "JPEG": jpeg_files,
    "PNG": png_files,
    "JPG": jpg_files,
    "TXT": txt_files,
    "DOCX": docx_files,
    "MP3": mp3_files,
    "WAV": wav_files,
    "MP4": mp4_files,
    "AVI": avi_files,
    "ZIP": zip_files,
    "TAR": tar_files,
    "OTHERS": others
}

# отримуємо ім'я файлу та повертаємо його розширення у верхньому регістрі
def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

# виконуємо рекурсивне сканування папки та групування файлів за категоріями відповідно до їх розширень
def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if get_extensions(item.name) not in registered_extensions:
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Scanning in: {path}")

    arg = Path(path)
    scan(arg)
    
    # виводимо списки файлів та розширень відповідно до категорій 
    print(f"Images: {jpeg_files, jpg_files, png_files}\n")
    print(f"Documents: {txt_files},{docx_files}\n")
    print(f"Audio: {mp3_files},{wav_files}\n")
    print(f"Video: {mp4_files},{avi_files}\n")
    print(f"Archives: {zip_files},{tar_files}\n")
    print(f"Others: {others}\n")
    print(f"All extensions: {extensions}\n")
    print(f"Unknown extensions: {unknown}\n")