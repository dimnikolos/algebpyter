import os
from convert_kef3 import process_tex

def main():
    for i in range(4, 9):
        in_file = f'content/original_tex_content/Kef{i}.tex'
        out_file = f'Kef{i}_Interactive.ipynb'
        if os.path.exists(in_file):
            process_tex(in_file, out_file)
        else:
            print(f"File not found: {in_file}")

if __name__ == '__main__':
    main()
