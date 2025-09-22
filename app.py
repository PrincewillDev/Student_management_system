import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
import sqlite3

class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("950x600")
        self.root.config(bg="#f0f0f0")
        
        # Create database connection or connect to existing
        self.create_db()
        
        # Variables for form fields
        self.student_id = tk.StringVar()
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.phone = tk.StringVar()
        self.course = tk.StringVar()
        self.gender = tk.StringVar()
        self.search_text = tk.StringVar()

        # Title Label
        title_font = font.Font(family="Ariel", size=16, weight="bold")
        title = tk.Label(root, text="Student Management System", font=title_font, bg="#f0f0f0", fg="#333333")
        title.pack(pady=10)
        
         # Main Frame
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left Frame for Form
        form_frame = tk.LabelFrame(main_frame, text="Student Details", bg="#f0f0f0",
                                   font=("Arial", 12))
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,  padx=10, pady=10)

        #Form Widgets
        # Students ID
        label_id = tk.Label(form_frame, text="Student ID:", bg="#f0f0f0", font=("Arial", 10))
        label_id.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_id = tk.Entry(form_frame, textvariable=self.student_id, font=("Arial", 10))
        entry_id.grid(row=0, column=1, padx=10, pady=10)


         # Name
        lbl_name = tk.Label(form_frame, text="Name:", bg="#f0f0f0", font=("Arial", 10))
        lbl_name.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry_name = tk.Entry(form_frame, textvariable=self.name,  font=("Arial", 10))
        entry_name.grid(row=1, column=1, padx=10, pady=10)
        
        # Email
        lbl_email = tk.Label(form_frame, text="Email:", bg="#f0f0f0", font=("Arial", 10))
        lbl_email.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        entry_email = tk.Entry(form_frame, textvariable=self.email, font=("Arial", 10))
        entry_email.grid(row=2, column=1, padx=10, pady=10)
        
        # Phone
        lbl_phone = tk.Label(form_frame, text="Phone:", bg="#f0f0f0", font=("Arial", 10))
        lbl_phone.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        entry_phone = tk.Entry(form_frame, textvariable=self.phone, font=("Arial", 10))
        entry_phone.grid(row=3, column=1, padx=10, pady=10)
        
        # Course
        lbl_course = tk.Label(form_frame, text="Course:", bg="#f0f0f0", font=("Arial", 10))
        lbl_course.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        entry_course = tk.Entry(form_frame, textvariable=self.course, font=("Arial", 10))
        entry_course.grid(row=4, column=1, padx=10, pady=10)
        
        # Buttons Frame
        btn_frame = tk.Frame(form_frame, bg="#f0f0f0")
        btn_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=20)
        
         # Add Button
        btn_add = tk.Button(btn_frame, text="Add", width=10, command=self.add_student,
                           bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        btn_add.grid(row=0, column=0, padx=5)
        
        # Update Button
        btn_update = tk.Button(btn_frame, text="Update", width=10, command=self.update_student,
                              bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        btn_update.grid(row=0, column=1, padx=5)
        
        # Delete Button
        btn_delete = tk.Button(btn_frame, text="Delete", width=10, command=self.delete_student,
                              bg="#f44336", fg="white", font=("Arial", 10, "bold"))
        btn_delete.grid(row=0, column=2, padx=5)
        
        # Clear Button
        btn_clear = tk.Button(btn_frame, text="Clear", width=10, command=self.clear_form,
                             bg="#607D8B", fg="white", font=("Arial", 10, "bold"))
        btn_clear.grid(row=0, column=3, padx=5)
        
        
         # Right Frame for Table
        table_frame = tk.LabelFrame(main_frame, text="Student Records", bg="#f0f0f0",
                                   font=("Arial", 12))
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Search frame
        search_frame = tk.Frame(table_frame, bg="#f0f0f0")
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        lbl_search = tk.Label(search_frame, text="Search:", bg="#f0f0f0", font=("Arial", 10))
        lbl_search.pack(side=tk.LEFT, padx=5)
        
        entry_search = tk.Entry(search_frame, textvariable=self.search_text, width=25, font=("Arial", 10))
        entry_search.pack(side=tk.LEFT, padx=5)
        
        btn_search = tk.Button(search_frame, text="Search", command=self.search_student,
                              bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
        btn_search.pack(side=tk.LEFT, padx=5)
        
        btn_show_all = tk.Button(search_frame, text="Show All", command=self.fetch_data,
                                bg="#9C27B0", fg="white", font=("Arial", 10, "bold"))
        btn_show_all.pack(side=tk.LEFT, padx=5)
        
        # Table Frame
        tree_frame = tk.Frame(table_frame, bg="#f0f0f0")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        x_scroll = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        y_scroll = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Table
        self.student_table = ttk.Treeview(
            tree_frame, 
            columns=("id", "name", "email", "phone", "course", "gender"),
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set
        )
        
        x_scroll.config(command=self.student_table.xview)
        y_scroll.config(command=self.student_table.yview)
        
        # Define columns
        self.student_table.heading("id", text="ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("gender", text="Gender")
        
        self.student_table["show"] = "headings" 
        
        self.student_table.column("id", width=50)
        self.student_table.column("name", width=150)
        self.student_table.column("email", width=150)
        self.student_table.column("phone", width=100)
        self.student_table.column("course", width=120)
        self.student_table.column("gender", width=80)
        
        self.student_table.pack(fill=tk.BOTH, expand=True)
        
        # Bind select event
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)
        
        # Load initial data
        self.fetch_data()
        
    def create_db(self):
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            course TEXT,
            gender TEXT
        )
        ''')
        conn.commit()
        conn.close()
    
    def fetch_data(self):
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        
        if len(rows) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for row in rows:
                self.student_table.insert("", tk.END, values=row)
        
        conn.close()
    
    def add_student(self):
        if self.student_id.get() == "" or self.name.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                conn = sqlite3.connect('student.db')
                cursor = conn.cursor()
                
                # Check if ID already exists
                cursor.execute("SELECT * FROM students WHERE id=?", (self.student_id.get(),))
                row = cursor.fetchone()
                
                if row:
                    messagebox.showerror("Error", "Student ID already exists")
                else:
                    cursor.execute(
                        "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            self.student_id.get(),
                            self.name.get(),
                            self.email.get(),
                            self.phone.get(),
                            self.course.get(),
                            self.gender.get()
                        )
                    )
                    conn.commit()
                    messagebox.showinfo("Success", "Student added successfully")
                    self.fetch_data()
                    self.clear_form()
                
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
    
    def get_cursor(self, event):
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        row = content["values"]
        
        if row:
            self.student_id.set(row[0])
            self.name.set(row[1])
            self.email.set(row[2])
            self.phone.set(row[3])
            self.course.set(row[4])
            self.gender.set(row[5])
    
    def update_student(self):
        if self.student_id.get() == "":
            messagebox.showerror("Error", "Student ID is required")
        else:
            try:
                conn = sqlite3.connect('student.db')
                cursor = conn.cursor()
                
                cursor.execute(
                    "UPDATE students SET name=?, email=?, phone=?, course=?, gender=? WHERE id=?",
                    (
                        self.name.get(),
                        self.email.get(),
                        self.phone.get(),
                        self.course.get(),
                        self.gender.get(),
                        self.student_id.get()
                    )
                )
                conn.commit()
                self.fetch_data()
                self.clear_form()
                messagebox.showinfo("Success", "Student updated successfully")
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
    
    def delete_student(self):
        if self.student_id.get() == "":
            messagebox.showerror("Error", "Student ID is required")
        else:
            try:
                conn = sqlite3.connect('student.db')
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM students WHERE id=?", (self.student_id.get(),))
                conn.commit()
                self.fetch_data()
                self.clear_form()
                messagebox.showinfo("Success", "Student deleted successfully")
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
    
    def clear_form(self):
        self.student_id.set("")
        self.name.set("")
        self.email.set("")
        self.phone.set("")
        self.course.set("")
        self.gender.set("")
    
    def search_student(self):
        if self.search_text.get() == "":
            messagebox.showerror("Error", "Please enter search criteria")
        else:
            try:
                conn = sqlite3.connect('student.db')
                cursor = conn.cursor()
                
                search_term = f"%{self.search_text.get()}%"
                cursor.execute(
                    "SELECT * FROM students WHERE id LIKE ? OR name LIKE ? OR course LIKE ?",
                    (search_term, search_term, search_term)
                )
                rows = cursor.fetchall()
                
                if len(rows) != 0:
                    self.student_table.delete(*self.student_table.get_children())
                    for row in rows:
                        self.student_table.insert("", tk.END, values=row)
                else:
                    messagebox.showinfo("Info", "No matching records found")
                
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")

    

if __name__=="__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()