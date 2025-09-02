import nbformat

# List of notebooks to merge in order
notebooks = [
    "01_data_loading.ipynb",
    "02_data_preprocessing.ipynb",
    "03_EDA_on_price.ipynb",
    "04_model_selection_cross_validation.ipynb",
    "05_shap_analysis.ipynb"
]
merged_nb = nbformat.v4.new_notebook()
merged_cells = []

for nb_file in notebooks:
    with open(nb_file, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        merged_cells.extend(nb.cells)
        # Optional: Add a markdown separator between notebooks
        merged_cells.append(nbformat.v4.new_markdown_cell(f"---\n# End of {nb_file}\n---"))

merged_nb.cells = merged_cells

# Save the result
with open("merged_notebook.ipynb", 'w', encoding='utf-8') as f:
    nbformat.write(merged_nb, f)

print("✅ Merged notebook created: merged_notebook.ipynb")