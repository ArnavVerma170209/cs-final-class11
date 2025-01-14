import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import json

# Initialize library data
library_data = {"books": {}, "issued": {}}


def save_data():
    """Save library data to a file."""
    with open("library_data.json", "w") as file:
        json.dump(library_data, file)


def load_data():
    """Load library data from a file."""
    global library_data
    try:
        with open("library_data.json", "r") as file:
            library_data = json.load(file)
    except FileNotFoundError:
        save_data()


# Functions
def add_book():
    """Add a new book to the library."""
    book_id = book_id_entry.get()
    title = title_entry.get()
    author = author_entry.get()

    if book_id and title and author:
        if book_id not in library_data["books"]:
            library_data["books"][book_id] = {"title": title, "author": author}
            save_data()
            update_book_list()
            messagebox.showinfo("Success", "Book added successfully!")
        else:
            messagebox.showwarning("Duplicate", "Book ID already exists.")
    else:
        messagebox.showwarning("Error", "All fields are required.")
    clear_entries()


def issue_book():
    """Issue a book to a user."""
    book_id = book_id_entry.get()
    user = title_entry.get()

    if book_id and user:
        if book_id in library_data["books"]:
            library_data["issued"][book_id] = library_data["books"].pop(book_id)
            library_data["issued"][book_id]["user"] = user
            save_data()
            update_book_list()
            messagebox.showinfo("Success", f"Book issued successfully to {user}!")
        else:
            messagebox.showwarning("Error", "Book ID not found or already issued.")
    else:
        messagebox.showwarning("Error", "Both fields are required.")
    clear_entries()


def return_book():
    """Return a book to the library."""
    book_id = book_id_entry.get()

    if book_id:
        if book_id in library_data["issued"]:
            library_data["books"][book_id] = library_data["issued"].pop(book_id)
            save_data()
            update_book_list()
            messagebox.showinfo("Success", f"Book {book_id} returned successfully!")
        else:
            messagebox.showwarning("Error", "Book ID not found in issued list.")
    else:
        messagebox.showwarning("Error", "Book ID is required.")
    clear_entries()

def delete__book():
    book_id = book_id_entry.get()

    if book_id:
        if book_id in library_data["books"]:
            library_data["books"].pop(book_id)
            save_data()
            update_book_list()
            messagebox.showinfo("Success", "Book deleted successfully!")
        else:
            messagebox.showwarning("Error", "Book ID not found.")
    else:
        messagebox.showwarning("Error", "Book ID is required.")
    clear_entries()

def update_book_list():
    """Update the book list display."""
    book_list.delete(*book_list.get_children())
    for book_id, book in library_data["books"].items():
        book_list.insert("", "end", values=(book_id, book["title"], book["author"], "Available"))

    for book_id, book in library_data["issued"].items():
        book_list.insert("", "end", values=(book_id, book["title"], book["author"], f"Issued to {book['user']}"))


def clear_entries():
    """Clear all input fields."""
    book_id_entry.delete(0, ttk.END)
    title_entry.delete(0, ttk.END)
    author_entry.delete(0, ttk.END)


# Load initial data
load_data()
    
# Create the main window
root = ttk.Window(themename="litera")
root.title("Library Management System")
root.geometry("1000x600")
root.resizable(False, False)

# Header
header_frame = ttk.Frame(root, padding=10)
header_frame.pack(fill=X)

ttk.Label(header_frame, text="Library Management System", font=("Helvetica", 24, "bold"), anchor=CENTER).pack()

# Frames
input_frame = ttk.Frame(root, padding=15)
input_frame.pack(side=ttk.TOP, fill=ttk.X)

book_list_frame = ttk.Frame(root, padding=15)
book_list_frame.pack(side=ttk.BOTTOM, fill=ttk.BOTH, expand=True)

# Input Fields
ttk.Label(input_frame, text="Book ID:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
book_id_entry = ttk.Entry(input_frame, width=30)
book_id_entry.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(input_frame, text="Title/User", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=W)
title_entry = ttk.Entry(input_frame, width=30)
title_entry.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(input_frame, text="Author:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky=W)
author_entry = ttk.Entry(input_frame, width=30)
author_entry.grid(row=2, column=1, padx=10, pady=10)

# Buttons
button_width = 20
ttk.Button(input_frame, text="Add Book", style="success.TButton", command=add_book, width=button_width).grid(row=0, column=2, padx=20, pady=10)
ttk.Button(input_frame, text="Issue Book", style="primary.TButton", command=issue_book, width=button_width).grid(row=1, column=2, padx=20, pady=10)
ttk.Button(input_frame, text="Return Book", style="warning.TButton", command=return_book, width=button_width).grid(row=2, column=2, padx=20, pady=10)
ttk.Button(input_frame, text="Delete Book", style="danger.TButton", command=delete__book, width=button_width).grid(row=3, column=2, padx=20, pady=10)

# Book List
columns = ("Book ID", "Title", "Author", "Status")
book_list = ttk.Treeview(book_list_frame, columns=columns, show="headings", height=15)
for col in columns:
    book_list.heading(col, text=col)
    book_list.column(col, width=200, anchor=CENTER)

# Add dark borders
style = ttk.Style()
style.configure("Treeview.Heading", bordercolor="black", borderwidth=3)

book_list.pack(fill=BOTH, expand=True, pady=10)

update_book_list()

# Run the application
root.mainloop()
