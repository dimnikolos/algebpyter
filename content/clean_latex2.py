import os
import json
import re

content_dir = r"c:\Users\dniko\Documents\github\algebpyter\content"

def clean_latex2_in_notebook(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return
        
    changed = False
    
    for cell in data.get('cells', []):
        if cell.get('cell_type') == 'markdown':
            new_source = []
            for line in cell.get('source', []):
                original_line = line
                
                # Replace \sel[YY]{XX} with Σελίδα XX (Άσκηση YY)
                # re.sub uses \1 for YY and \2 for XX
                line = re.sub(r'\\sel\[([^\]]+)\]\{([^}]+)\}', r'Σελίδα \2 (Άσκηση \1)', line)
                
                # Replace \includegraphics[...]{filename} or \includegraphics{filename}
                # with ![filename](filename)
                line = re.sub(r'\\includegraphics(?:\[.*?\])?\{([^}]+)\}', r'![\1](\1)', line)
                
                if line != original_line:
                    changed = True
                new_source.append(line)
            cell['source'] = new_source
            
    if changed:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
            print(f"Updated {filepath}")
        except Exception as e:
            print(f"Error writing to {filepath}: {e}")

if __name__ == "__main__":
    print(f"Scanning directory: {content_dir}")
    for root, dirs, files in os.walk(content_dir):
        # Optional: skip checking inside .git or checkpoints
        if '.git' in root or '.ipynb_checkpoints' in root:
            continue
            
        for file in files:
            if file.endswith('.ipynb'):
                clean_latex2_in_notebook(os.path.join(root, file))
    print("Done scanning and cleaning.")
