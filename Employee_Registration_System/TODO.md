# Employee Management System - Improvement Plan

## Tasks

- [x] 1. Fix `export.py` — implement proper CSV export (`export_to_csv`) with save dialog.
- [x] 2. Refactor `employee_form.py` — use validation from `utils.py`, add edit mode + photo preview.
- [x] 3. Add Edit Employee feature:
  - [x] 3a. Update `employee_form.py` to support Add + Edit modes.
  - [x] 3b. Add "Edit Employee" button to `dashboard.py` and display selected photo.
- [x] 4. Add photo preview in form + display selected employee photo in dashboard.
- [x] 5. Update `README.txt` to document new features.
- [x] 6. Test the application runs without errors (all modules compile successfully).
- [x] 7. Make all app windows open maximized (`root.state("zoomed")` in login.py, dashboard.py, and employee_form.py).
- [x] 8. UI/theme overhaul:
  - [x] 8a. `styles.py` — modern slate/indigo theme with hover colors, styled buttons, combobox, entry, scrollbar, treeview.
  - [x] 8b. `dashboard.py` — flat buttons with emoji icons, hover effects, hand cursor, improved photo panel.
  - [x] 8c. `login.py` — styled login button with hover effect.
  - [x] 8d. `employee_form.py` — styled Save/Cancel/Browse buttons with hover effects.
- [x] 8e. All modules compile successfully.
- [x] 9. Apply provided light modern theme (Qt QSS + CustomTkinter design) translated to Tkinter:
  - [x] 9a. `styles.py` — light palette (#F7FAFC bg, white cards, #3182CE accent), hover states, styled ttk widgets.
  - [x] 9b. Retained original Qt `APP_STYLESHEET` + `CTK_THEME` tokens for reference/future port.
  - [x] 9c. All modules compile successfully.
