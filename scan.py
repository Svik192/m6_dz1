import sys
from pathlib import Path

# Image('JPEG', 'PNG', 'JPG', 'SVG');
# Video_files ('AVI', 'MP4', 'MOV', 'MKV');
# Documents ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
# Music ('MP3', 'OGG', 'WAV', 'AMR');
# Archives ('ZIP', 'GZ', 'TAR');
# Other (Unknown_extensions)

Image = list()
Video_files = list()
Documents = list()
Music = list()
Archives = list()
Unknown_extensions = list()

folders = list()

unknown = set()
extensions = set()

registered_extensions = {
    'JPEG': Image,
    'PNG': Image,
    'JPG': Image,
    'SVG': Image,    

    'AVI': Video_files,
    'MP4': Video_files,
    'MOV': Video_files,
    'MKV': Video_files,  

    'DOC': Documents,
    'DOCX': Documents,
    'TXT': Documents,
    'PDF': Documents, 
    'XLSX': Documents,
    'PPTX': Documents,   

    'MP3': Music,
    'OGG': Music,
    'WAV': Music,
    'AMR': Music,   

    'ZIP': Archives,
    'GZ': Archives,
    'TAR': Archives
}

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():       
            if item.name not in ('Image', 'Video_files', 'Documents', 'Music', 'Archives', 'Other'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            Unknown_extensions.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                Unknown_extensions.append(new_name)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    folder = Path(path)

    scan(folder)

    print(f"Image: {Image}")
    print(f"Video_files: {Video_files}")
    print(f"Documents: {Documents}")
    print(f"Music: {Music}")
    print(f"Archives: {Archives}")

    print(f"Other: {Unknown_extensions}")
    print(f"Unknown extensions: {unknown}")

    print(f"Folder: {folders}")

    print(f"All extensions: {extensions}")