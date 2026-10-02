import tkinter as tk
from tkinter import filedialog, messagebox
import os


class TextEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Untitled - Python Text Editor")
        self.master.geometry("800x600")

        self.current_file = None
        self.text_changed = False

        # Create menu bar
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_editor)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.find_text, accelerator="Ctrl+F")
        self.edit_menu.add_command(label="Replace", command=self.replace_text)

        # Text area with scrollbar
        self.text_frame = tk.Frame(self.master)
        self.text_frame.pack(fill=tk.BOTH, expand=1)

        self.text_edit = tk.Text(
            self.text_frame,
            wrap=tk.WORD,
            undo=True,
            font=("Consolas", 11)
        )
        self.text_edit.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollbar = tk.Scrollbar(self.text_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_edit.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_edit.yview)

        # Status bar
        self.status_bar = tk.Label(self.master, text="Line: 1 | Column: 1 | Characters: 0", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind events
        self.text_edit.bind("<<Modified>>", self.on_text_modified)
        self.text_edit.bind("<KeyRelease>", self.update_status_bar)
        self.text_edit.bind("<ButtonRelease-1>", self.update_status_bar)

        # Keyboard shortcuts
        self.master.bind("<Control-n>", lambda _: self.new_file())
        self.master.bind("<Control-o>", lambda _: self.open_file())
        self.master.bind("<Control-s>", lambda _: self.save_file())
        self.master.bind("<Control-Shift-S>", lambda _: self.save_as_file())
        self.master.bind("<Control-z>", lambda _: self.undo())
        self.master.bind("<Control-y>", lambda _: self.redo())
        self.master.bind("<Control-x>", lambda _: self.cut())
        self.master.bind("<Control-c>", lambda _: self.copy())
        self.master.bind("<Control-v>", lambda _: self.paste())
        self.master.bind("<Control-a>", lambda _: self.select_all())
        self.master.bind("<Control-f>", lambda _: self.find_text())

        # Initialize status bar
        self.update_status_bar()

    def set_window_title(self):
        if self.current_file:
            base_name = os.path.basename(self.current_file)
        else:
            base_name = "Untitled"
        if self.text_changed:
            self.master.title(f"{base_name}* - Python Text Editor")
        else:
            self.master.title(f"{base_name} - Python Text Editor")

    def on_text_modified(self, _=None):
        if self.text_edit.edit_modified():
            self.text_changed = True
            self.set_window_title()
            self.text_edit.edit_modified(False)

    def new_file(self):
        if self.text_changed:
            if messagebox.askyesno("Save changes?", "Do you want to save changes to the current file?"):
                self.save_file()
        self.text_edit.delete(1.0, tk.END)
        self.current_file = None
        self.text_changed = False
        self.set_window_title()
        self.update_status_bar()

    def open_file(self):
        if self.text_changed:
            if messagebox.askyesno("Save changes?", "Do you want to save changes to the current file?"):
                self.save_file()
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("JavaScript Files", "*.js"),
                ("Markdown Files", "*.md"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                self.text_edit.delete(1.0, tk.END)
                self.text_edit.insert(1.0, content)
                self.current_file = file_path
                self.text_changed = False
                self.set_window_title()
                self.update_status_bar()
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{e}")

    def save_file(self):
        if self.current_file:
            try:
                content = self.text_edit.get(1.0, tk.END)
                with open(self.current_file, "w") as file:
                    file.write(content)
                self.text_changed = False
                self.set_window_title()
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("JavaScript Files", "*.js"),
                ("Markdown Files", "*.md"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            try:
                content = self.text_edit.get(1.0, tk.END)
                with open(file_path, "w") as file:
                    file.write(content)
                self.current_file = file_path
                self.text_changed = False
                self.set_window_title()
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")

    def exit_editor(self):
        if self.text_changed:
            if messagebox.askyesno("Save changes?", "Do you want to save changes before exiting?"):
                self.save_file()
        self.master.quit()

    def undo(self):
        try:
            self.text_edit.edit_undo()
        except tk.TclError:
            pass  # Nothing to undo

    def redo(self):
        try:
            self.text_edit.edit_redo()
        except tk.TclError:
            pass  # Nothing to redo

    def cut(self):
        self.text_edit.event_generate("<<Cut>>")

    def copy(self):
        self.text_edit.event_generate("<<Copy>>")

    def paste(self):
        self.text_edit.event_generate("<<Paste>>")

    def select_all(self):
        self.text_edit.tag_add(tk.SEL, "1.0", tk.END)
        self.text_edit.mark_set(tk.INSERT, "1.0")
        self.text_edit.see(tk.INSERT)

    def find_text(self):
        find_dialog = tk.Toplevel(self.master)
        find_dialog.title("Find")
        find_dialog.geometry("300x100")
        find_dialog.resizable(False, False)

        tk.Label(find_dialog, text="Find:").grid(row=0, column=0, padx=5, pady=5)
        find_entry = tk.Entry(find_dialog, width=20)
        find_entry.grid(row=0, column=1, padx=5, pady=5)
        find_entry.focus()

        def search():
            query = find_entry.get()
            if not query:
                return
            # Remove previous highlights
            self.text_edit.tag_remove("found", "1.0", tk.END)
            # Start search from the beginning
            start_pos = "1.0"
            while True:
                start_pos = self.text_edit.search(query, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(query)}c"
                self.text_edit.tag_add("found", start_pos, end_pos)
                start_pos = end_pos
            self.text_edit.tag_config("found", background="yellow")

        tk.Button(find_dialog, text="Find Next", command=search).grid(row=0, column=2, padx=5, pady=5)
        find_dialog.bind("<Return>", lambda _: search())

    def replace_text(self):
        replace_dialog = tk.Toplevel(self.master)
        replace_dialog.title("Replace")
        replace_dialog.geometry("350x120")
        replace_dialog.resizable(False, False)

        tk.Label(replace_dialog, text="Find:").grid(row=0, column=0, padx=5, pady=5)
        find_entry = tk.Entry(replace_dialog, width=20)
        find_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(replace_dialog, text="Replace with:").grid(row=1, column=0, padx=5, pady=5)
        replace_entry = tk.Entry(replace_dialog, width=20)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        def replace_one():
            query = find_entry.get()
            replacement = replace_entry.get()
            if not query:
                return
            # Remove previous highlights
            self.text_edit.tag_remove("found", "1.0", tk.END)
            # Search from the current cursor position
            start_pos = self.text_edit.index(tk.INSERT)
            pos = self.text_edit.search(query, start_pos, stopindex=tk.END)
            if pos:
                end_pos = f"{pos}+{len(query)}c"
                self.text_edit.delete(pos, end_pos)
                self.text_edit.insert(pos, replacement)
                # Move cursor after the inserted text
                self.text_edit.mark_set(tk.INSERT, f"{pos}+{len(replacement)}c")
                self.text_edit.see(tk.INSERT)
                self.on_text_modified()  # Mark as changed

        def replace_all():
            query = find_entry.get()
            replacement = replace_entry.get()
            if not query:
                return
            # Remove previous highlights
            self.text_edit.tag_remove("found", "1.0", tk.END)
            content = self.text_edit.get(1.0, tk.END)
            new_content = content.replace(query, replacement)
            self.text_edit.delete(1.0, tk.END)
            self.text_edit.insert(1.0, new_content)
            self.on_text_modified()  # Mark as changed

        tk.Button(replace_dialog, text="Replace", command=replace_one).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(replace_dialog, text="Replace All", command=replace_all).grid(row=1, column=2, padx=5, pady=5)
        replace_dialog.bind("<Return>", lambda _: replace_one())

    def update_status_bar(self, _=None):
        # Get current cursor position
        cursor_pos = self.text_edit.index(tk.INSERT)
        line, column = cursor_pos.split('.')
        # Get total character count (including newlines)
        content = self.text_edit.get(1.0, tk.END)
        char_count = len(content) - 1  # Subtract 1 because Text widget adds a trailing newline
        self.status_bar.config(text=f"Line: {int(line)} | Column: {int(column)} | Characters: {char_count}")


def main():
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()