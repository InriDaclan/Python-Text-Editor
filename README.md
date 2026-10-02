# Simple Python Text Editor

A beginner-friendly text editor application built with Python and Tkinter.

## Features

- **File Operations**: New, Open, Save, Save As, Exit
- **Editing**: Undo, Redo, Cut, Copy, Paste, Select All
- **Search**: Find text, Replace text
- **User Interface**: 
  - Menu bar with File and Edit menus
  - Large text editing area with scrollbar
  - Status bar showing current line, column, and character count
- **Keyboard Shortcuts**:
  - Ctrl + N → New
  - Ctrl + O → Open
  - Ctrl + S → Save
  - Ctrl + Shift + S → Save As
  - Ctrl + Z → Undo
  - Ctrl + Y → Redo
  - Ctrl + X → Cut
  - Ctrl + C → Copy
  - Ctrl + V → Paste
  - Ctrl + A → Select All
  - Ctrl + F → Find

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)

## How to Run

1. Make sure you have Python installed (version 3.x recommended)
2. Navigate to the directory containing `text_editor.py`
3. Run the command:
   ```bash
   python text_editor.py
   ```
   or on some systems:
   ```bash
   python3 text_editor.py
   ```

The application will launch a graphical window with the text editor interface.

## How It Works

### Main Window
The `TextEditor` class creates the main Tkinter window with a title bar, menu bar, text area, and status bar.

### Text Widget
The core editing component is a `tkinter.Text` widget with:
- Word wrapping (`wrap=tk.WORD`)
- Built-in undo/redo functionality (`undo=True`)
- Monospace font for better readability
- Vertical scrollbar for navigation

### File Handling
- **Open**: Uses `filedialog.askopenfilename` to select a file, reads content, and inserts it into the text widget
- **Save**: Gets all text content and writes it to the current file path
- **Save As**: Uses `filedialog.asksaveasfilename` to get a new file path and saves content there
- Tracks modifications with a `text_changed` flag and updates the window title with an asterisk (*) when there are unsaved changes

### Keyboard Shortcuts
Shortcuts are bound using `master.bind()` with lambda functions that call the corresponding methods (e.g., `<Control-n>` calls `new_file()`).

### Status Bar
The status bar updates on key and mouse events to show:
- Current line and column (from `text_edit.index(tk.INSERT)`)
- Character count (length of all text content, adjusting for Tkinter's trailing newline)

### Search Functionality
- **Find**: Opens a dialog to enter search text, highlights all matches with a yellow background
- **Replace**: Opens a dialog to enter find and replace text, with options to replace one occurrence or all occurrences

## Code Structure

The application is contained in a single file (`text_editor.py`) with:

1. **Imports**: tkinter, filedialog, messagebox, os
2. **TextEditor class**: Encapsulates all functionality
   - `__init__`: Sets up the window, menus, text area, scrollbar, status bar, and event bindings
   - Menu action methods: new_file, open_file, save_file, save_as_file, exit_editor
   - Editing methods: undo, redo, cut, copy, paste, select_all
   - Search methods: find_text, replace_text
   - Helper methods: set_window_title, on_text_modified, update_status_bar
3. **main function**: Creates the root window and starts the application
4. **if __name__ == "__main__"**: Standard Python entry point

## Extending the Editor

To add more features:
1. Add new menu items in the `__init__` method and create corresponding methods
2. Create new dialog windows using `tkinter.Toplevel` for complex operations
3. Use text widget methods like `search()`, `delete()`, `insert()`, `tag_add()` for text operations
4. Enhance the status bar in `update_status_bar()` to show additional metrics
5. Add more keyboard shortcuts following the existing pattern

## License

This project is open source and available for modification and distribution.