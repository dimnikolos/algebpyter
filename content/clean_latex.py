import os
import json
import re

content_dir = r"c:\Users\dniko\Documents\github\algebpyter\content"

def clean_latex_in_notebook(filepath):
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
                
                # Replace \ldots with ...
                line = line.replace(r'\ldots', '...')
                
                # Replace \sel{XX} with Σελίδα XX
                # In JSON strings, the backslash is physical, so in Python raw string r'\\sel\{([^}]+)\}' 
                # matches the literal string "\sel{...}"
                line = re.sub(r'\\sel\{([^}]+)\}', r'Σελίδα \1', line)
                
                # Handling itemize and item
                line = line.replace(r'\begin{itemize}', '')
                line = line.replace(r'\end{itemize}', '')
                # replace \item with Markdown list item format "- "
                line = line.replace(r'\item', '- ')
                
                # also handle potential cases with newline
                line = line.replace(r'\begin{itemize}' + '\n', '')
                line = line.replace(r'\end{itemize}' + '\n', '')
                
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
        # Optional: skip checking inside node_modules or .git if any
        if '.git' in root or '.ipynb_checkpoints' in root:
            continue
            
        for file in files:
            if file.endswith('.ipynb'):
                clean_latex_in_notebook(os.path.join(root, file))
    print("Done scanning and cleaning.")
