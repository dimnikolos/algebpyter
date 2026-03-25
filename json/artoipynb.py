import json

def create_interactive_notebook(json_filename, output_filename):
    # Φόρτωση των δεδομένων
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cells = []

    # 1. Το "Μαγικό" CSS Κελί που μετατρέπει το Jupyter σε Ιστοσελίδα
    css_magic = """%%html
<style>
    /* Γενικό φόντο και γραμματοσειρά */
    body { background-color: #f4f7f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Κεντράρισμα και στυλ σελίδας */
    #notebook-container { 
        max-width: 900px; 
        margin: 40px auto; 
        padding: 50px; 
        background: #ffffff; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); 
        border-radius: 12px; 
    }
    
    /* Εξαφάνιση των ενοχλητικών In [ ] και Out [ ] */
    div.prompt { display: none !important; }
    
    /* Κομψός σχεδιασμός στα κελιά κώδικα */
    div.input_area { 
        border: 1px solid #e1e4e8 !important; 
        border-radius: 8px !important; 
        background-color: #fdfdfd !important; 
    }
    div.output_area pre { font-family: 'Consolas', 'Courier New', monospace; color: #2c3e50; }
    
    /* Στυλ Επικεφαλίδων */
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-bottom: 20px;}
    h2 { color: #34495e; margin-top: 40px; font-weight: 600; }
    
    /* Custom Κουτιά για Ασκήσεις και Λύσεις */
    .problem-box { 
        background: #e8f4f8; 
        padding: 20px; 
        border-left: 5px solid #3498db; 
        border-radius: 4px; 
        margin-bottom: 15px; 
        font-size: 1.1em;
    }
    .solution-box { 
        background: #fef9e7; 
        padding: 20px; 
        border-left: 5px solid #f1c40f; 
        border-radius: 4px; 
        margin-top: 10px; 
    }
    .notes-box { font-size: 0.95em; color: #7f8c8d; font-style: italic; margin-top: 10px; }
</style>
"""
    # Προσθήκη του CSS ως το πρώτο κελί κώδικα
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [css_magic]
    })

    # Προσθήκη Κεντρικού Τίτλου
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# 📘 Algebpy: Διαδραστικό Βιβλίο Άλγεβρας\n\n",
            "*Κάντε κλικ στο παραπάνω κελί και πατήστε **Shift + Enter** για να ενεργοποιήσετε τα γραφικά της ιστοσελίδας!*\n\n",
            "---"
        ]
    })

    # Προσθήκη των Ασκήσεων ανά Κατηγορία
    for category, exercises in data.items():
        # Τίτλος Κατηγορίας
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"## 📌 {category}"]
        })

        for idx, ex in enumerate(exercises):
            # Εκφώνηση με HTML/CSS
            problem_md = f"<div class='problem-box'>\n<strong>Άσκηση {idx+1}:</strong> {ex['problem']}\n</div>"
            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [problem_md]
            })

            # Python Λύση (Εκτελέσιμος Κώδικας)
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [ex['python_solution']]
            })

            # Μαθηματική Λύση & Σημειώσεις με HTML/CSS
            solution_md = (
                f"<div class='solution-box'>\n"
                f"<strong>Μαθηματική Εξήγηση:</strong> {ex['math_solution']}\n\n"
                f"<div class='notes-box'>💡 <strong>Tip:</strong> {ex['notes']}</div>\n"
                f"</div>\n<br><hr>"
            )
            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [solution_md]
            })

    # Δομή του Notebook
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
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

    # Αποθήκευση στο αρχείο .ipynb
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)

    print(f"Το διαδραστικό βιβλίο δημιουργήθηκε επιτυχώς: {output_filename}")

# Εκτέλεση της συνάρτησης
create_interactive_notebook('arranged.json', 'algebpy_interactive.ipynb')