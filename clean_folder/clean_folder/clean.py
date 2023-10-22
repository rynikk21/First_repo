import sys
import shutil
import re
from pathlib import Path

# normalize.py {

CYRILLIC_SYMBOLS = 'абвгґдеєжзиіїйклмнопрстуфхцчшщюя'
TRANSLATION = ('a', 'b', 'v', 'h', 'g', 'd', 'e', 'ye', 'zh', 'z', 'y', 'i', 'yi', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', 'yu', 'ya')

TRANS = dict()

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()

def normalize(name: str) -> str:
    extension = Path(name).suffix
    name_without_extension = Path(name).stem
    translated_name = re.sub(r'\W', '_', name_without_extension.translate(TRANS))
    normalized_name = translated_name + extension
    return normalized_name

# } normalize.py

# file_parser.py {

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEOS = []
MP4_VIDEOS = []
MOV_VIDEOS = []
MKV_VIDEOS = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
MY_OTHER = []
ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []




REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEOS,
    'MP4': MP4_VIDEOS,
    'MOV': MOV_VIDEOS,
    'MKV': MKV_VIDEOS,
    'DOC': DOC_DOCUMENTS,
    'DOCX': DOCX_DOCUMENTS,
    'TXT': TXT_DOCUMENTS,
    'PDF': PDF_DOCUMENTS,
    'XLSX': XLSX_DOCUMENTS,
    'PPTX': PPTX_DOCUMENTS,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ZIP_ARCHIVES,
    'GZ': GZ_ARCHIVES,
    'TAR': TAR_ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()

def get_extention(name: str) -> str:
    return Path(name).suffix[1:].upper()

def scan(folder: Path):
    for item in folder.iterdir():
        # work with folder
        if item.is_dir(): # check if object is folder
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        # Work with file
        extension = get_extention(item.name) # take extension of file
        full_name = folder / item.name # take full path to file
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension) # .mp4, .mov, .avi
                MY_OTHER.append(full_name)

# if __name__ == '__main__':
#     folder_process = sys.argv[1]
#     scan(Path(folder_process))
#     print(f'Images jpeg: {JPEG_IMAGES}')
#     print(f'Images jpg: {JPG_IMAGES}')
#     print(f'Images png: {PNG_IMAGES}')
#     print(f'Images svg: {SVG_IMAGES}')
#     print(f'Videos avi: {AVI_VIDEOS}')
#     print(f'Videos mp4: {MP4_VIDEOS}')
#     print(f'Videos mov: {MOV_VIDEOS}')
#     print(f'Videos mkv: {MKV_VIDEOS}')
#     print(f'Documents doc: {DOC_DOCUMENTS}')
#     print(f'Documents docx: {DOCX_DOCUMENTS}')
#     print(f'Documents txt: {TXT_DOCUMENTS}')
#     print(f'Documents pdf: {PDF_DOCUMENTS}')
#     print(f'Documents xlsx: {XLSX_DOCUMENTS}')
#     print(f'Documents pptx: {PPTX_DOCUMENTS}')
#     print(f'Audio mp3: {MP3_AUDIO}')
#     print(f'Audio ogg: {OGG_AUDIO}')
#     print(f'Audio wav: {WAV_AUDIO}')
#     print(f'Audio amr: {AMR_AUDIO}')
#     print(f'Archives zip: {ZIP_ARCHIVES}')
#     print(f'Archives gz: {GZ_ARCHIVES}')
#     print(f'Archives tar: {TAR_ARCHIVES}')

#     print(f'EXTENSIONS: {EXTENSIONS}')
#     print(f'UNKNOWN: {UNKNOWN}')
#     print(f'FOLDERS: {FOLDERS}')

#  } file_parser.py

#  main.py {

def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_other(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()

# def handle_folder(folder: Path):
#     try:
#         folder.rmdir()
#     except OSError:
#         print(f'Error during remove folder {folder}')

def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
    for file in AVI_VIDEOS:
        handle_media(file, folder / 'video' / 'AVI')
    for file in MP4_VIDEOS:
        handle_media(file, folder / 'video' / 'MP4')
    for file in MOV_VIDEOS:
        handle_media(file, folder / 'video' / 'MOV')
    for file in MKV_VIDEOS:
        handle_media(file, folder / 'video' / 'MKV')
    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')        
    for file in DOC_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in DOCX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in TXT_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'TXT')
    for file in PDF_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PDF')
    for file in XLSX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in PPTX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PPTX')
    for file in MY_OTHER:
        handle_other(file, folder / 'MY_OTHER')
    for file in ZIP_ARCHIVES:
        handle_archive(file, folder / 'archives' /  'ZIP_ARCHIVES')
    for file in GZ_ARCHIVES:
        handle_archive(file, folder / 'archives' /  'GZ_ARCHIVES')
    for file in TAR_ARCHIVES:
        handle_archive(file, folder / 'archives' /  'TAR_ARCHIVES')
    
    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')

def start():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process)

#  } main.py 
