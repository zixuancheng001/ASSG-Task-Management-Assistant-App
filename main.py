
"""
main.py - Task Management Assistant Main Application
"""
import tkinter as tk
from tkinter import messagebox #Use to pop-up message box
from assg_logic import TaskManagerLogic
from assg_gui import TaskManagementGUI

def main():
    """Main function to run the application"""
    try:
        # Create the root window
        root = tk.Tk()
        
        # Set application title
        root.title("Task Management System")
        
        # Initialize business logic
        logic = TaskManagerLogic()
        
        # Initialize GUI
        app = TaskManagementGUI(root, logic)
        
        # Center the window on screen
        center_window(root)
        
        # Start the main event loop
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Application Error", f"An error occurred:\n{str(e)}")

def center_window(window):
    """Center the window on the screen"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    main()
