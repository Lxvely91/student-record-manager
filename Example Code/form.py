import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import mysql.connector
import shutil
import os
import pandas as pd
from fpdf import FPDF

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="accountant_db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS accountants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    number VARCHAR(255),
    type VARCHAR(50),
    file_path VARCHAR(255) NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS imported_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    designation VARCHAR(255),
    salary VARCHAR(255),
    address VARCHAR(255)
)
""")
conn.commit()

# Global Variables
selected_id = None
file_path = None


# Function to Fetch Religions for Dropdown
#def fetch_religions():
   # cursor.execute("SELECT name FROM religion")
    #religions = cursor.fetchall()
    #return [r[0] for r in religions] if religions else []


def fetch_religions():
    cursor.execute("SELECT id, name FROM religion")
    religions = cursor.fetchall()
    return {str(row[0]): row[1] for row in religions}


# Function to Select a File
def select_file():
    global file_path
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("All Files", "*.*")])
    if file_path:
        file_label.config(text=os.path.basename(file_path))

# Function to Submit Form
def submit_form():
    global selected_id, file_path
    name = name_entry.get()
    number = number_entry.get()
    account_type = accounttype_var.get()
    religion = religion_var.get()

    if name == "" or number == "":
        messagebox.showwarning("Warning", "All fields are required!")
        return

    try:
        saved_path = None
        if file_path:
            upload_folder = "uploads"
            os.makedirs(upload_folder, exist_ok=True)
            saved_path = os.path.join(upload_folder, os.path.basename(file_path))
            shutil.copy(file_path, saved_path)
        else:
            saved_path = None

        if selected_id is None:
            if selected_id is None:
                cursor.execute(
                    "INSERT INTO accountants (name, number, type, religion, file_path) VALUES (%s, %s, %s, %s, %s)",
                    (name, number, account_type, religion, saved_path))
            else:
                cursor.execute(
                    "UPDATE accountants SET name=%s, number=%s, type=%s, religion=%s, file_path=%s WHERE id=%s",
                    (name, number, account_type, religion, saved_path, selected_id))
                selected_id = None

        conn.commit()
        messagebox.showinfo("Success", "Accountant data saved successfully!")
        fetch_data()
        clear_form()

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Function to Fetch Data
def fetch_data():
    cursor.execute("SELECT id, name, number, type, file_path FROM accountants")
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", "end", values=row)

# Function to Import Excel Data
def import_excel():
    file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel Files", "*.xlsx;*.xls")])
    if not file_path:
        return

    try:
        df = pd.read_excel(file_path)

        # Ensure there are at least 4 required columns
        if df.shape[1] < 4:
            messagebox.showwarning("Warning", "Excel file must have at least 4 columns: Name, Designation, Salary, Address")
            return

        # Rename columns for consistency (Modify as per your Excel structure)
        df.columns = ["name", "designation", "salary", "address"]

        # Handle missing values (replace NaN with empty string)
        df = df.fillna('')

        # Insert each row into the database
        for _, row in df.iterrows():
            cursor.execute("INSERT INTO imported_data (name, designation, salary, address) VALUES (%s, %s, %s, %s)",
                           (row["name"], row["designation"], row["salary"], row["address"]))

        conn.commit()
        messagebox.showinfo("Success", "Excel data imported successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Error importing Excel: {e}")


# Function to Select Row
def select_row(event):
    global selected_id
    selected_item = tree.selection()
    if selected_item:
        row_data = tree.item(selected_item, "values")
        selected_id = row_data[0]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, row_data[1])
        number_entry.delete(0, tk.END)
        number_entry.insert(0, row_data[2])
        accounttype_var.set(row_data[3])
        file_label.config(text=row_data[4] if row_data[4] else "No File Selected")

# Function to Clear Form
def clear_form():
    global selected_id, file_path
    selected_id = None
    file_path = None
    name_entry.delete(0, tk.END)
    number_entry.delete(0, tk.END)
    accounttype_var.set("Personal")
    file_label.config(text="No File Selected")


def export_by_account_number():
    # Prompt the user to enter an account number
    search_number = number_entry.get().strip()

    if not search_number:
        messagebox.showwarning("Warning", "Please enter an account number!")
        return

    try:
        # Fetch data based on account number
        cursor.execute("SELECT id, name, number, type, file_path,religion FROM accountants WHERE number = %s", (search_number,))
        rows = cursor.fetchall()

        if not rows:
            messagebox.showwarning("Warning", "No records found for the given account number!")
            return

        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=["ID", "Name", "Number", "Type", "File Path","Religion"])

        # Ask user for file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Save Excel File"
        )

        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", "Data exported successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to export data: {e}")





        def export_by_account_number_pdf():
            search_number = number_entry.get().strip()

            if not search_number:
                messagebox.showwarning("Warning", "Please enter an account number!")
                return

            try:
                # Fetch data based on account number
                cursor.execute("SELECT id, name, number, type, religion, file_path FROM accountants WHERE number = %s", (search_number,))
                rows = cursor.fetchall()

                if not rows:
                    messagebox.showwarning("Warning", "No records found for the given account number!")
                    return

                # Create PDF instance
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(200, 10, "Accountant Report", ln=True, align="C")

                pdf.set_font("Arial", "", 12)

                for row in rows:
                    pdf.ln(10)
                    pdf.cell(0, 10, f"ID: {row[0]}", ln=True)
                    pdf.cell(0, 10, f"Name: {row[1]}", ln=True)
                    pdf.cell(0, 10, f"Number: {row[2]}", ln=True)
                    pdf.cell(0, 10, f"Type: {row[3]}", ln=True)
                    pdf.cell(0, 10, f"Religion: {row[4]}", ln=True)

                    if row[5]:  # If a file path exists
                        pdf.cell(0, 10, f"File Path: {row[5]}", ln=True)

                # Ask user for file location
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF Files", "*.pdf")],
                    title="Save PDF File"
                )

                if file_path:
                    pdf.output(file_path)
                    messagebox.showinfo("Success", "Data exported successfully as PDF!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {e}")




def export_by_account_number_pdf():
    search_number = number_entry.get().strip()

    if not search_number:
        messagebox.showwarning("Warning", "Please enter an account number!")
        return

    try:
        # Fetch data from database
        cursor.execute("SELECT id, name, number, type, religion, file_path FROM accountants WHERE number = %s", (search_number,))
        rows = cursor.fetchall()

        if not rows:
            messagebox.showwarning("Warning", "No records found for the given account number!")
            return

        # Create PDF instance
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Accountant Report", ln=True, align="C")

        pdf.set_font("Arial", "", 12)

        for row in rows:
            pdf.ln(10)
            pdf.cell(0, 10, f"ID: {row[0]}", ln=True)
            pdf.cell(0, 10, f"Name: {row[1]}", ln=True)
            pdf.cell(0, 10, f"Number: {row[2]}", ln=True)
            pdf.cell(0, 10, f"Type: {row[3]}", ln=True)
            pdf.cell(0, 10, f"Religion: {row[4]}", ln=True)

            if row[5]:  # If file path exists
                pdf.cell(0, 10, f"File Path: {row[5]}", ln=True)

        # Ask user for file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save PDF File"
        )

        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Success", "Data exported successfully as PDF!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to export data: {e}")


# Root Window
root = tk.Tk()
root.title("Accountant Form")
root.geometry("500x600")
root.configure(bg="#f0f0f0")

# Main Frame
main_frame = tk.Frame(root, bg="white", padx=20, pady=20, relief="ridge", borderwidth=2)
main_frame.pack(pady=10, padx=10, fill="both", expand=True)


frame2 = tk.Frame(root)
frame2.pack()

# Labels and Entries
tk.Label(main_frame, text="Accountant Name:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(main_frame, font=("Arial", 12), width=25, bd=2, relief="solid")
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(main_frame, text="Accountant Number:", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
number_entry = tk.Entry(main_frame, font=("Arial", 12), width=25, bd=2, relief="solid")
number_entry.grid(row=1, column=1, padx=10, pady=5)

# Accountant Type
tk.Label(main_frame, text="Accountant Type:", font=("Arial", 12), bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
accounttype_var = tk.StringVar(value="Personal")
tk.Radiobutton(main_frame, text="Personal", variable=accounttype_var, value="Personal", font=("Arial", 12), bg="white").grid(row=2, column=1, sticky="w")
tk.Radiobutton(main_frame, text="Business", variable=accounttype_var, value="Business", font=("Arial", 12), bg="white").grid(row=2, column=1, padx=80, sticky="w")

# Religion Dropdown
#tk.Label(main_frame, text="Religion:", font=("Arial", 12), bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
#religion_var = tk.StringVar()
#religion_dropdown = ttk.Combobox(main_frame, textvariable=religion_var, values=fetch_religions(), font=("Arial", 12))
#religion_dropdown.grid(row=3, column=1, padx=10, pady=5)

# Religion Label
tk.Label(main_frame, text="Religion:", font=("Arial", 12), bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")


religions_dict = fetch_religions()

religion_var = tk.StringVar()
religion_var.set(next(iter(religions_dict.values())))

# Religion Combobox
religion_dropdown = ttk.Combobox(main_frame, textvariable=religion_var, values=list(religions_dict.values()), font=("Arial", 12))
religion_dropdown.grid(row=3, column=1, padx=10, pady=5)

religion_dropdown.config(width=17)


# File Upload
tk.Label(main_frame, text="Upload File:", font=("Arial", 12), bg="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
file_label = tk.Label(main_frame, text="No File Selected", bg="white", font=("Arial", 10), fg="red")
file_label.grid(row=4, column=1, sticky="w")
ttk.Button(main_frame, text="Browse", command=select_file).grid(row=4, column=1, padx=90, sticky="w")





# Buttons
ttk.Button(main_frame, text="Save", command=submit_form).grid(row=5, column=0, columnspan=2, pady=10)
ttk.Button(main_frame, text="Import Excel", command=import_excel).grid(row=6, column=0, columnspan=2, pady=10)


# Button to trigger export
ttk.Button(main_frame, text="Export by Account Number", command=export_by_account_number).grid(row=7, column=0, columnspan=2, pady=10)

# Add Export as PDF button
#export_pdf_btn = tk.Button(root, text="Export as PDF", command=export_by_account_number_pdf)
#export_pdf_btn.grid(row=8, column=0, padx=10, pady=10)
export_pdf_btn = tk.Button(frame2, text="Export PDF", command=export_by_account_number_pdf)
export_pdf_btn.grid(row=8, column=0, padx=10, pady=10)

# Table Frame
table_frame = tk.Frame(root, bg="white", relief="ridge", borderwidth=2)
table_frame.pack(pady=10, padx=10, fill="both", expand=True)

columns = ("id", "name", "number", "type", "file_path")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=100)
tree.pack(pady=10, padx=10, fill="both", expand=True)
tree.bind("<ButtonRelease-1>", select_row)

# Fetch Data
fetch_data()

root.mainloop()
