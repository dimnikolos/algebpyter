import os
from convert_kef3 import process_tex

def main():
    in_file = f'original_tex_content/Kef2.tex'
    out_file = f'Kef2_Interactive.ipynb'
    if os.path.exists(in_file):
        process_tex(in_file, out_file)
    else:
        print(f"File not found: {in_file}")

if __name__ == '__main__':
    main()
