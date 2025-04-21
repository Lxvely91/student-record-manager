# Import necessary modules
import tkinter as tk  # For GUI components
from tkinter import filedialog, messagebox  # For file selection and popup messages
import mysql.connector  # For connecting and working with MySQL database
import os  # For file path operations like getting filenames

# Define the main application class
class StudentFormApp:
    def __init__(self, root):
        self.root = root  # Main window
        self.root.title("Student Form")  # Window title
        self.root.geometry("400x250")  # Size of the main window

        self.selected_image = tk.StringVar(value="No file chosen")  # To store image filename

        self.connect_db()  # Call method to connect to MySQL database
        self.create_form()  # Call method to build the GUI form

    # Connect to MySQL database using mysql.connector
    def connect_db(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_db"
        )
        self.cursor = self.db.cursor()  # Create a cursor to execute SQL commands

    # Create the main input form layout
    def create_form(self):
        form_frame = tk.Frame(self.root, padx=10, pady=10)  # Main frame for inputs
        form_frame.pack(fill="both", expand=True)

        fields = ["Name", "Roll", "Age", "Gender", "Address"]  # Labels for the form
        self.entries = {}  # Dictionary to hold entry fields

        for i, field in enumerate(fields):
            label = tk.Label(form_frame, text=field)  # Create label
            label.grid(row=i, column=0, sticky="w", pady=5)  # Position label to the left
            entry = tk.Entry(form_frame)  # Create input box
            entry.grid(row=i, column=1, sticky="ew", pady=5)  # Position entry next to label
            self.entries[field.lower()] = entry  # Store entry widget with lowercase field name

        # Add image upload row
        img_label = tk.Label(form_frame, text="Image")
        img_label.grid(row=len(fields), column=0, sticky="w", pady=5)

        img_frame = tk.Frame(form_frame)
        img_frame.grid(row=len(fields), column=1, sticky="ew", pady=5)

        # Display image filename (read-only entry)
        self.img_display = tk.Entry(img_frame, textvariable=self.selected_image, state="readonly")
        self.img_display.pack(side="left", fill="x", expand=True)

        # Choose file button for selecting image
        choose_btn = tk.Button(img_frame, text="Choose File", command=self.choose_file)
        choose_btn.pack(side="left", padx=5)

        form_frame.columnconfigure(1, weight=1)  # Allow column 1 to expand

        # Buttons frame at the bottom
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack()

        # Add student button
        add_btn = tk.Button(btn_frame, text="Add Student", command=self.add_student)
        add_btn.grid(row=0, column=0, padx=10)

        # Manage students button
        manage_btn = tk.Button(btn_frame, text="Manage Students", command=self.open_manage_window)
        manage_btn.grid(row=0, column=1, padx=10)

    # Open file dialog to choose an image file
    def choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            filename = os.path.basename(file_path)  # Get just the filename, not full path
            self.selected_image.set(filename)  # Display filename in the entry box

    # Save student data to the database
    def add_student(self):
        name = self.entries["name"].get()
        roll = self.entries["roll"].get()
        age = self.entries["age"].get()
        gender = self.entries["gender"].get()
        address = self.entries["address"].get()
        image = self.selected_image.get()

        # Check if any field is empty
        if not (name and roll and age and gender and address):
            messagebox.showwarning("Missing Data", "Please fill all fields.")
            return

        # Insert student record into database
        sql = "INSERT INTO students (name, roll, age, gender, address, image) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (name, roll, age, gender, address, image))
        self.db.commit()  # Save changes to database
        messagebox.showinfo("Success", "Student added successfully!")

        # Clear form inputs
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.selected_image.set("No file chosen")

    # Open the "Manage Students" window
    def open_manage_window(self):
        self.manage_win = tk.Toplevel(self.root)  # Create a new window
        self.manage_win.title("Manage Students")
        self.manage_win.geometry("1000x500")

        canvas = tk.Canvas(self.manage_win)  # Canvas for scrolling
        scrollbar = tk.Scrollbar(self.manage_win, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        # Adjust scroll region
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Header row
        header = tk.Frame(scroll_frame, pady=5)
        header.pack(fill="x")
        headers = ["Name", "Roll", "Age", "Gender", "Address", "Image", "Edit", "Delete"]
        widths = [15, 10, 5, 10, 30, 20, 10, 10]

        # Create header labels
        for text, width in zip(headers, widths):
            tk.Label(header, text=text, width=width, anchor="center", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        # Fetch student data
        self.cursor.execute("SELECT id, name, roll, age, gender, address, image FROM students")
        rows = self.cursor.fetchall()

        # Create row for each student
        for student in rows:
            sid, name, roll, age, gender, address, image = student
            row_frame = tk.Frame(scroll_frame, pady=2)
            row_frame.pack(fill="x")

            values = [name, roll, age, gender, address, image]
            for val, width in zip(values, widths):
                tk.Label(row_frame, text=str(val), width=width, anchor="center").pack(side="left", padx=5)

            # Buttons to edit or delete
            tk.Button(row_frame, text="Edit", width=10, command=lambda i=sid: self.edit_student(i)).pack(side="left", padx=5)
            tk.Button(row_frame, text="Delete", width=10, command=lambda i=sid: self.delete_student(i)).pack(side="left", padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # Function to edit student data
    def edit_student(self, student_id):
        # Get student data from DB
        self.cursor.execute("SELECT name, roll, age, gender, address, image FROM students WHERE id = %s", (student_id,))
        data = self.cursor.fetchone()

        if not data:
            messagebox.showerror("Error", "Student not found.")
            return

        name, roll, age, gender, address, image = data

        # Create window for editing
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Student")
        edit_win.geometry("400x400")

        fields = ["Name", "Roll", "Age", "Gender", "Address"]
        entry_vars = {}

        # Create editable entries pre-filled with existing data
        for i, (field, val) in enumerate(zip(fields, data[:-1])):
            tk.Label(edit_win, text=field).grid(row=i, column=0, sticky="w", pady=5, padx=10)
            var = tk.StringVar(value=val)
            entry = tk.Entry(edit_win, textvariable=var)
            entry.grid(row=i, column=1, pady=5, sticky="ew", padx=10)
            entry_vars[field.lower()] = var

        # Image file field
        tk.Label(edit_win, text="Image").grid(row=5, column=0, sticky="w", pady=5, padx=10)
        img_frame = tk.Frame(edit_win)
        img_frame.grid(row=5, column=1, sticky="ew", padx=10)

        img_var = tk.StringVar(value=image)
        img_entry = tk.Entry(img_frame, textvariable=img_var, state="readonly")
        img_entry.pack(side="left", fill="x", expand=True)

        # Choose image button
        def choose_edit_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
            if file_path:
                filename = os.path.basename(file_path)
                img_var.set(filename)

        tk.Button(img_frame, text="Choose File", command=choose_edit_image).pack(side="left", padx=5)

        # Buttons for saving or canceling
        btn_frame = tk.Frame(edit_win, pady=20)
        btn_frame.grid(row=6, column=0, columnspan=2)

        # Save changes to DB
        def save_changes():
            updated_data = (
                entry_vars["name"].get(),
                entry_vars["roll"].get(),
                entry_vars["age"].get(),
                entry_vars["gender"].get(),
                entry_vars["address"].get(),
                img_var.get(),
                student_id
            )
            sql = """
                UPDATE students SET name=%s, roll=%s, age=%s, gender=%s, address=%s, image=%s
                WHERE id=%s
            """
            self.cursor.execute(sql, updated_data)
            self.db.commit()
            messagebox.showinfo("Success", "Student updated successfully!")
            edit_win.destroy()
            self.manage_win.destroy()  # Close and reopen window to refresh data
            self.open_manage_window()

        tk.Button(btn_frame, text="Save", command=save_changes).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", command=edit_win.destroy).pack(side="left", padx=10)

    # Function to delete a student record
    def delete_student(self, student_id):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
        if confirm:
            self.cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            self.db.commit()
            messagebox.showinfo("Deleted", "Student deleted successfully.")
            self.manage_win.destroy()
            self.open_manage_window()  # Refresh manage window

# This block runs the app
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentFormApp(root)
    root.mainloop()
