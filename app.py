import tkinter as tk
from tkinter import filedialog, messagebox
import mysql.connector
import os

class StudentFormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Form")
        self.root.geometry("400x250")

        self.selected_image = tk.StringVar(value="No file chosen")

        self.connect_db()
        self.create_form()

    def connect_db(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_db"
        )
        self.cursor = self.db.cursor()

    def create_form(self):
        form_frame = tk.Frame(self.root, padx=10, pady=10)
        form_frame.pack(fill="both", expand=True)

        fields = ["Name", "Roll", "Age", "Gender", "Address"]
        self.entries = {}

        for i, field in enumerate(fields):
            label = tk.Label(form_frame, text=field)
            label.grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(form_frame)
            entry.grid(row=i, column=1, sticky="ew", pady=5)
            self.entries[field.lower()] = entry


        img_label = tk.Label(form_frame, text="Image")
        img_label.grid(row=len(fields), column=0, sticky="w", pady=5)

        img_frame = tk.Frame(form_frame)
        img_frame.grid(row=len(fields), column=1, sticky="ew", pady=5)

        self.img_display = tk.Entry(img_frame, textvariable=self.selected_image, state="readonly")
        self.img_display.pack(side="left", fill="x", expand=True)

        choose_btn = tk.Button(img_frame, text="Choose File", command=self.choose_file)
        choose_btn.pack(side="left", padx=5)

        form_frame.columnconfigure(1, weight=1)


        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack()

        add_btn = tk.Button(btn_frame, text="Add Student", command=self.add_student)
        add_btn.grid(row=0, column=0, padx=10)

        manage_btn = tk.Button(btn_frame, text="Manage Students", command=self.open_manage_window)
        manage_btn.grid(row=0, column=1, padx=10)

    def choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            filename = os.path.basename(file_path)
            self.selected_image.set(filename)

    def add_student(self):
        name = self.entries["name"].get()
        roll = self.entries["roll"].get()
        age = self.entries["age"].get()
        gender = self.entries["gender"].get()
        address = self.entries["address"].get()
        image = self.selected_image.get()

        if not (name and roll and age and gender and address):
            messagebox.showwarning("Missing Data", "Please fill all fields.")
            return

        sql = "INSERT INTO students (name, roll, age, gender, address, image) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (name, roll, age, gender, address, image))
        self.db.commit()
        messagebox.showinfo("Success", "Student added successfully!")

        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.selected_image.set("No file chosen")

    def open_manage_window(self):
        self.manage_win = tk.Toplevel(self.root)
        self.manage_win.title("Manage Students")
        self.manage_win.geometry("1000x500")

        canvas = tk.Canvas(self.manage_win)
        scrollbar = tk.Scrollbar(self.manage_win, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        header = tk.Frame(scroll_frame, pady=5)
        header.pack(fill="x")
        headers = ["Name", "Roll", "Age", "Gender", "Address", "Image", "Edit", "Delete"]
        widths = [15, 10, 5, 10, 30, 20, 10, 10]

        for text, width in zip(headers, widths):
            tk.Label(header, text=text, width=width, anchor="center", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        self.cursor.execute("SELECT id, name, roll, age, gender, address, image FROM students")
        rows = self.cursor.fetchall()

        for student in rows:
            sid, name, roll, age, gender, address, image = student
            row_frame = tk.Frame(scroll_frame, pady=2)
            row_frame.pack(fill="x")

            values = [name, roll, age, gender, address, image]
            for val, width in zip(values, widths):
                tk.Label(row_frame, text=str(val), width=width, anchor="center").pack(side="left", padx=5)

            tk.Button(row_frame, text="Edit", width=10, command=lambda i=sid: self.edit_student(i)).pack(side="left", padx=5)
            tk.Button(row_frame, text="Delete", width=10, command=lambda i=sid: self.delete_student(i)).pack(side="left", padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def edit_student(self, student_id):
        self.cursor.execute("SELECT name, roll, age, gender, address, image FROM students WHERE id = %s", (student_id,))
        data = self.cursor.fetchone()

        if not data:
            messagebox.showerror("Error", "Student not found.")
            return

        name, roll, age, gender, address, image = data

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Student")
        edit_win.geometry("400x400")

        fields = ["Name", "Roll", "Age", "Gender", "Address"]
        entry_vars = {}

        for i, (field, val) in enumerate(zip(fields, data[:-1])):
            tk.Label(edit_win, text=field).grid(row=i, column=0, sticky="w", pady=5, padx=10)
            var = tk.StringVar(value=val)
            entry = tk.Entry(edit_win, textvariable=var)
            entry.grid(row=i, column=1, pady=5, sticky="ew", padx=10)
            entry_vars[field.lower()] = var


        tk.Label(edit_win, text="Image").grid(row=5, column=0, sticky="w", pady=5, padx=10)
        img_frame = tk.Frame(edit_win)
        img_frame.grid(row=5, column=1, sticky="ew", padx=10)

        img_var = tk.StringVar(value=image)
        img_entry = tk.Entry(img_frame, textvariable=img_var, state="readonly")
        img_entry.pack(side="left", fill="x", expand=True)

        def choose_edit_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
            if file_path:
                filename = os.path.basename(file_path)
                img_var.set(filename)

        tk.Button(img_frame, text="Choose File", command=choose_edit_image).pack(side="left", padx=5)


        btn_frame = tk.Frame(edit_win, pady=20)
        btn_frame.grid(row=6, column=0, columnspan=2)

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
            self.manage_win.destroy()
            self.open_manage_window()

        tk.Button(btn_frame, text="Save", command=save_changes).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", command=edit_win.destroy).pack(side="left", padx=10)

    def delete_student(self, student_id):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
        if confirm:
            self.cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            self.db.commit()
            messagebox.showinfo("Deleted", "Student deleted successfully.")
            self.manage_win.destroy()
            self.open_manage_window()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentFormApp(root)
    root.mainloop()
