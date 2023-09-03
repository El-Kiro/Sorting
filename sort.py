import sys
import shutil
from pathlib import Path

EXTENSIONS = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'videos': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR'),
}


def normalize(filename):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
        'є': 'ye', 'ж': 'zh', 'з': 'z', 'и': 'i', 'і': 'i', 'ї': 'yi',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'yu', 'я': 'ya',
    }

    normalized_name = ''
    for char in filename:
        if char.isalnum() or char in ('.', '_', '-'):
            normalized_name += char
        elif char in translit_dict:
            normalized_name += translit_dict[char]
        else:
            normalized_name += '_'

    return normalized_name


def sort_folder(folder_path):
    folder_path = Path(folder_path)

    for source_file in folder_path.glob('**/*'):
        if source_file.is_file():
            filename = source_file.name
            file_extension = filename.split('.')[-1].upper()
            normalized_name = normalize(filename)

            category = 'unknown'
            for key, extensions in EXTENSIONS.items():
                if file_extension in extensions:
                    category = key
                    break

            category_dir = folder_path / category
            category_dir.mkdir(parents=True, exist_ok=True)

            destination_file = category_dir / normalized_name

            shutil.move(str(source_file), str(destination_file))

    for dir_path in folder_path.glob('**/*'):
        if dir_path.is_dir() and not any(dir_path.iterdir()):
            dir_path.rmdir()





if len(sys.argv) != 2:
    print("Usage: python sort.py <folder_path>")
else:
    folder_path = sys.argv[1]
    if Path(folder_path).exists():
        sort_folder(folder_path)
        print("Sorting complete.")
    else:
        print("Folder not found.")