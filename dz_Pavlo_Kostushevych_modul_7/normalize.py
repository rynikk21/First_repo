import re
from pathlib import Path

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