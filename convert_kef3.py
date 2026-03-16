import json
import re

def create_markdown_cell(source_lines):
    # join with newlines and add to a list, we just keep empty strings for newline
    source = []
    for i, line in enumerate(source_lines):
        source.append(line + ('\n' if (i < len(source_lines) - 1 or line == '') else ''))
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source
    }

def create_code_cell(source_lines):
    source = []
    for i, line in enumerate(source_lines):
        source.append(line + ('\n' if i < len(source_lines) - 1 else ''))
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source
    }

def is_python_code(lines):
    if any(l.startswith('>>>') for l in lines): return True
    code_keywords = ['import ', 'def ', 'print', '=', 'for ', 'if ', 'return']
    for l in lines:
        for kw in code_keywords:
            if kw in l: return True
    return False

def clean_code_lines(lines):
    is_repl = any(l.startswith('>>>') for l in lines)
    if is_repl:
        clean = []
        for l in lines:
            if l.startswith('>>> '):
                clean.append(l[4:])
            elif l.startswith('>>>'):
                clean.append(l[3:])
            elif l.startswith('... '):
                clean.append(l[4:])
            elif l.startswith('...'):
                clean.append(l[3:])
        return clean
    else:
        return lines

def process_tex(filepath, out_filepath):
    cells = []
    current_md = []
    
    in_listing = False
    current_code = []
    in_exercise = False
    
    in_table = False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for raw_line in lines:
        raw_line = raw_line.rstrip('\n')
        line_stripped = raw_line.strip()
        
        if line_stripped.startswith('%'):
            continue
            
        if '\\begin{table}' in line_stripped or '\\end{table}' in line_stripped:
            continue
            
        if '\\begin{tabular}' in line_stripped:
            in_table = True
            current_md.append('')
            # Add table header
            cols = line_stripped.count('c')
            header_sep = '|' + '|'.join(['---'] * cols) + '|'
            # The next lines should form the table
            # We don't append header yet, we wait for the first row to determine cols explicitly if needed
            continue
            
        if '\\end{tabular}' in line_stripped:
            in_table = False
            current_md.append('')
            continue
            
        if in_table:
            # simple transform of tabular rows to markdown table rows
            row = raw_line.replace('\\hline', '').replace('\\\\', '').strip()
            if row:
                current_md.append('| ' + row.replace('&', ' | ') + ' |')
                # If this is the first row we processed, add the header separator
                if len(current_md) >= 2 and current_md[-2] == '':
                    cols = row.count('&') + 1
                    header_sep = '|' + '|'.join(['---'] * cols) + '|'
                    current_md.append(header_sep)
            continue
            
        if '\\begin{lstlisting}' in line_stripped:
            if current_md:
                # filter out empty markdown cells
                if any(l.strip() for l in current_md):
                    cells.append(create_markdown_cell(current_md))
                current_md = []
            in_listing = True
            current_code = []
            continue
            
        if '\\end{lstlisting}' in line_stripped:
            in_listing = False
            if current_code:
                if is_python_code(current_code):
                    clean = clean_code_lines(current_code)
                    if clean:
                        cells.append(create_code_cell(clean))
                else:
                    current_md.append('```text')
                    current_md.extend(current_code)
                    current_md.append('```')
            continue
            
        if in_listing:
            current_code.append(raw_line)
            continue

        if line_stripped.startswith('\\chapter{'):
            m = re.search(r'\\chapter\{(.*?)\}', raw_line)
            if m: current_md.append('# ' + m.group(1))
            continue
            
        if line_stripped.startswith('\\section{'):
            m = re.search(r'\\section\{(.*?)\}', raw_line)
            if m: current_md.append('## ' + m.group(1))
            continue
            
        if line_stripped.startswith('\\subsection{'):
            m = re.search(r'\\subsection\{(.*?)\}', raw_line)
            if m: current_md.append('### ' + m.group(1))
            continue
            
        if '\\begin{exercise}' in raw_line:
            in_exercise = True
            raw_line = raw_line.replace('\\begin{exercise}', '> **ΑΣΚΗΣΗ:** ')
            current_md.append(raw_line)
            # if end exercise is on the same line
            if '\\end{exercise}' in raw_line:
                in_exercise = False
                current_md[-1] = current_md[-1].replace('\\end{exercise}', '')
            continue
            
        if '\\end{exercise}' in raw_line:
            in_exercise = False
            raw_line = raw_line.replace('\\end{exercise}', '')
            if raw_line.strip():
                current_md.append('> ' + raw_line)
            continue
            
        if in_exercise:
            current_md.append('> ' + raw_line)
            continue
            
        # normal line
        current_md.append(raw_line)

    if current_md and any(l.strip() for l in current_md):
        cells.append(create_markdown_cell(current_md))

    # Construct complete ipynb structure
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    with open(out_filepath, 'w', encoding='utf-8') as out_f:
        json.dump(notebook, out_f, ensure_ascii=False, indent=4)
        
    print(f"Generated {out_filepath}")

if __name__ == '__main__':
    process_tex('content/original_tex_content/Kef3.tex', 'Kef3_Interactive.ipynb')
