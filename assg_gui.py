import tkinter as tk
import json
from tkinter import messagebox, simpledialog

class BaseGUI:
    def __init__(self, root):
        # Window settings
        self.root = root
        self.root.title("Task Management Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

    def create_menus(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.destroy)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def show_about(self):
        messagebox.showinfo("About", "Task Management Assistant\nVersion 2.0")

    # ==============================================================================================================================================================================================================
    # TaskManagementGUI
    # ==============================================================================================================================================================================================================        

class TaskManagementGUI(BaseGUI):
    def __init__(self, root, logic):
        # Main window reference
        super().__init__(root)
        self.logic = logic
        
        # Store the ID of the task being edited
        self.editing_task_id = None
        
        # create menu widgets
        self.create_menus()
        
        # create tab system
        self.create_tab_system()
        
        # create reminders checking
        self.check_reminders()
        
    # ==============================================================================================================================================================================================================
    # Menu
    # ==============================================================================================================================================================================================================

    def create_menus(self):
        """Create the top Menu Widgets"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Task", command=self.focus_create_task)
        file_menu.add_separator() #Add Seprator Line
        file_menu.add_command(label="Exit", command=self.root.destroy)#Change quit command cause check_reminders() will block it
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    # ==============================================================================================================================================================================================================
    # Button
    # ==============================================================================================================================================================================================================

    def create_tab_system(self):
        """Create the tab button system"""
        # Frame for tab buttons (Frame Widgets）
        tab_frame = tk.Frame(self.root, bg="#3498db", height=50)
        tab_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # Frame for tab content
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab button（Button Widgets）
        self.tab_buttons = []
        tab_names = ["Task Tracker", "Task Manager", "Reminders", "Category"]
        
        for i, name in enumerate(tab_names):
            btn = tk.Button(tab_frame, text=name,
                          font=("Arial", 11, "bold"),
                          bg="#3498db" if i == 0 else "#7f8c8d",
                          fg="white",
                          relief="flat",
                          padx=20,
                          pady=10,
                          command=lambda n=name: self.switch_tab(n))
            btn.pack(side="left", padx=2)
            self.tab_buttons.append(btn)
        
        # Create all tab contents
        self.create_task_tracker_tab()
        self.create_task_manager_tab()
        self.create_reminders_tab()
        self.create_category_tab()
        
        # Show default tab
        self.switch_tab("Task Tracker")

    # ==============================================================================================================================================================================================================
    # Switch tab
    # ==============================================================================================================================================================================================================

    def switch_tab(self, tab_name):
        """Switch between tabs"""
        # Update button color
        tab_names = ["Task Tracker", "Task Manager", "Reminders","Category"]
        for i, name in enumerate(tab_names):
            if name == tab_name:
                self.tab_buttons[i].config(bg="#3498db", relief="flat")
            else:
                self.tab_buttons[i].config(bg="#7f8c8d", relief="raised")
        
        # Hide content
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()
        
        # Show selected content
        if tab_name == "Task Tracker":
            self.task_tracker_frame.pack(fill="both", expand=True)
            self.view_all_tasks()
        elif tab_name == "Task Manager":
            self.task_manager_frame.pack(fill="both", expand=True)
        elif tab_name == "Reminders":
            self.reminders_frame.pack(fill="both", expand=True)
        elif tab_name == "Category":
            self.category_frame.pack(fill="both", expand=True)

    # ==============================================================================================================================================================================================================
    # Task Tracker Interface
    # ==============================================================================================================================================================================================================

    def create_task_tracker_tab(self):
        """Create Task Tracker tab"""
        self.task_tracker_frame = tk.Frame(self.content_frame, bg="white")
        
        # Title label（Use Label Widget）
        title_label = tk.Label(self.task_tracker_frame, 
                text="Task Tracker",
                font=("Arial", 16, "bold"),
                bg="white",
                fg="#2c3e50")
        title_label.pack(pady=(20, 10))
        
        # Control button frame
        control_frame = tk.Frame(self.task_tracker_frame, bg="white")
        control_frame.pack(pady=10)
        
        # View tasks button Use Grid layout manager
        view_btn = tk.Button(control_frame, 
                 text="View All Tasks",
                 font=("Arial", 11),
                 bg="#3498db",
                 fg="white",
                 relief="raised",
                 width=15,
                 height=1,
                 command=self.view_all_tasks)
        view_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Edit task button
        edit_btn = tk.Button(control_frame,
                 text="Edit Task",
                 font=("Arial", 11),
                 bg="#f39c12",
                 fg="white",
                 relief="raised",
                 width=15,
                 height=1,
                 command=self.edit_selected_task)
        edit_btn.grid(row=0, column=1, padx=5, pady=5)

        # Delete task button
        delete_btn = tk.Button(control_frame,
                 text="Delete Task",
                 font=("Arial", 11),
                 bg="#e74c3c",
                 fg="white",
                 relief="raised",
                 width=15,
                 height=1,
                 command=self.delete_task_gui)
        delete_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Task list frame
        list_frame = tk.Frame(self.task_tracker_frame, bg="white")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox to show tasks
        self.task_listbox = tk.Listbox(list_frame,
                                      font=("Arial", 10),
                                      yscrollcommand=scrollbar.set,
                                      bg="white",
                                      fg="#2c3e50",
                                      relief="solid",
                                      bd=1,
                                      selectbackground="#3498db",
                                      selectforeground="white",
                                      height=15,
                                      width=80)
        self.task_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # statistical information frame
        stats_frame = tk.Frame(self.task_tracker_frame,
                              bg="#ecf0f1",
                              relief="groove",
                              bd=2)
        stats_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        self.total_label = tk.Label(stats_frame, text="Total Tasks: 0", font=("Arial", 11), bg="#ecf0f1", fg="#2c3e50")
        self.total_label.pack(side="left", padx=20, pady=10)
        
        self.completed_label = tk.Label(stats_frame, text="Completed: 0", font=("Arial", 11), bg="#ecf0f1", fg="#27ae60")
        self.completed_label.pack(side="left", padx=20, pady=10)
        
        self.pending_label = tk.Label(stats_frame, text="Pending: 0", font=("Arial", 11), bg="#ecf0f1", fg="#e67e22")
        self.pending_label.pack(side="left", padx=20, pady=10)
        
        self.overdue_label = tk.Label(stats_frame, text="Overdue: 0", font=("Arial", 11), bg="#ecf0f1", fg="#e74c3c")
        self.overdue_label.pack(side="left", padx=20, pady=10)


    # ==============================================================================================================================================================================================================
    # Task Manager Interface
    # ==============================================================================================================================================================================================================

    def create_task_manager_tab(self):
        """Create Task Manager tab (add / edit tasks)"""
        self.task_manager_frame = tk.Frame(self.content_frame, bg="white")
        
        title_label = tk.Label(self.task_manager_frame, text="Task Manager", font=("Arial", 16, "bold"), bg="white", fg="#2c3e50")
        title_label.pack(pady=(20, 30))
        
        container = tk.Frame(self.task_manager_frame, bg="white")
        container.pack(expand=True)
        
        form_frame = tk.Frame(container, bg="white", width=600)
        form_frame.pack()
        
        for i in range(8): 
            form_frame.grid_rowconfigure(i, minsize=50)
        
        form_frame.grid_columnconfigure(0, minsize=150)
        form_frame.grid_columnconfigure(1, minsize=300)
        
        # Title
        tk.Label(form_frame, text="Title:", bg="white", font=("Arial", 11), anchor="e").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.title_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.title_var, font=("Arial", 11), width=40, relief="solid", bd=1).grid(row=0, column=1, sticky="w", padx=10)
        
        # Description
        tk.Label(form_frame, text="Description:", bg="white", font=("Arial", 11), anchor="e").grid(row=1, column=0, sticky="ne", padx=10, pady=5)
        self.desc_text = tk.Text(form_frame, height=4, width=40, font=("Arial", 11), relief="solid", bd=1)
        self.desc_text.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Due Date
        tk.Label(form_frame, text="Due Date:", bg="white", font=("Arial", 11), anchor="e").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        date_frame = tk.Frame(form_frame, bg="white")
        date_frame.grid(row=2, column=1, sticky="w", padx=10)
        self.due_date_var = tk.StringVar()
        tk.Entry(date_frame, textvariable=self.due_date_var, font=("Arial", 11), width=15, relief="solid", bd=1).pack(side="left")
        tk.Label(date_frame, text="(YYYY-MM-DD)", bg="white", font=("Arial", 9), fg="gray").pack(side="left", padx=5)
        
        # Due Time
        tk.Label(form_frame, text="Due Time:", bg="white", font=("Arial", 11), anchor="e").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        time_frame = tk.Frame(form_frame, bg="white")
        time_frame.grid(row=3, column=1, sticky="w", padx=10)
        self.due_time_var = tk.StringVar(value="00:00")
        tk.Entry(time_frame, textvariable=self.due_time_var, font=("Arial", 11), width=10, relief="solid", bd=1).pack(side="left")
        tk.Label(time_frame, text="(HH:MM, 24-hour)", bg="white", font=("Arial", 9), fg="gray").pack(side="left", padx=5)
        
        # Priority
        tk.Label(form_frame, text="Priority:", bg="white", font=("Arial", 11), anchor="e").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        priority_frame = tk.Frame(form_frame, bg="white")
        priority_frame.grid(row=4, column=1, sticky="w", padx=10)
        self.priority_var = tk.StringVar(value="Medium")
        for text, value in [("High", "High"), ("Medium", "Medium"), ("Low", "Low")]:
            tk.Radiobutton(priority_frame, text=text, value=value, variable=self.priority_var, bg="white", font=("Arial", 11)).pack(side="left", padx=15)

        # Category
        tk.Label(form_frame, text="Category:", bg="white", font=("Arial", 11), anchor="e").grid(row=5, column=0, sticky="e", padx=10, pady=5)
        self.category_var = tk.StringVar(value="Others")
        category_names = list(self.logic.categories.values())
        self.category_menu = tk.OptionMenu(form_frame, self.category_var, *category_names)
        self.category_menu.config(width=20)
        self.category_menu.grid(row=5, column=1, sticky="w", padx=10)

        # Status
        tk.Label(form_frame, text="Status:", bg="white", font=("Arial", 11), anchor="e").grid(row=6, column=0, sticky="e", padx=10, pady=5)
        status_frame = tk.Frame(form_frame, bg="white")
        status_frame.grid(row=6, column=1, sticky="w", padx=10)
        self.status_var = tk.StringVar(value="To Do")
        for text, value in [("To Do", "To Do"), ("In Progress", "In Progress"), ("Completed", "Completed")]:
            tk.Radiobutton(status_frame, text=text, value=value, variable=self.status_var, bg="white").pack(side="left", padx=10)

        # Buttons
        button_frame = tk.Frame(self.task_manager_frame, bg="white")
        button_frame.pack(pady=30)
        
        tk.Button(button_frame, text="Create Task", font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", width=15, height=2, command=self.create_task_gui).pack(side="left", padx=15)
        tk.Button(button_frame, text="Update Task", font=("Arial", 11), bg="#3498db", fg="white", width=15, height=2, command=self.update_task_gui).pack(side="left", padx=15)
        tk.Button(button_frame, text="Clear Form", font=("Arial", 11), bg="#95a5a6", fg="white", width=15, height=2, command=self.clear_form).pack(side="left", padx=15)

    # ==============================================================================================================================================================================================================
    # Reminders Interface
    # ==============================================================================================================================================================================================================

    def create_reminders_tab(self):
        """Create Reminders tab"""
        self.reminders_frame = tk.Frame(self.content_frame, bg="white")
        tk.Label(self.reminders_frame, text="Reminders & Notifications", font=("Arial", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=(20, 10))
        
        settings_frame = tk.Frame(self.reminders_frame, bg="#ecf0f1", relief="groove", bd=2)
        settings_frame.pack(fill="x", padx=50, pady=20)
        
        # Notification toggle
        status_frame = tk.Frame(settings_frame, bg="#ecf0f1")
        status_frame.pack(pady=15)
        tk.Label(status_frame, text="Notifications:", bg="#ecf0f1", font=("Arial", 12)).pack(side="left", padx=10)
        self.notification_var = tk.StringVar(value=self.logic.reminder_status)
        tk.Radiobutton(status_frame, text="On", value="On", variable=self.notification_var, bg="#ecf0f1", font=("Arial", 12), command=self.update_notification_status).pack(side="left", padx=10)
        tk.Radiobutton(status_frame, text="Off", value="Off", variable=self.notification_var, bg="#ecf0f1", font=("Arial", 12), command=self.update_notification_status).pack(side="left", padx=10)
        
        # Reminder time
        time_frame = tk.Frame(settings_frame, bg="#ecf0f1")
        time_frame.pack(pady=15)
        tk.Label(time_frame, text="Reminder Time:", bg="#ecf0f1", font=("Arial", 12)).pack(side="left", padx=10)
        self.time_var = tk.StringVar(value=self.logic.reminder_time)
        tk.Entry(time_frame, textvariable=self.time_var, font=("Arial", 12), width=10, relief="solid", bd=1).pack(side="left", padx=5)
        tk.Button(time_frame, text="Update Time", font=("Arial", 11), bg="#3498db", fg="white", command=self.update_reminder_time).pack(side="left", padx=10)
        
        upcoming_frame = tk.Frame(self.reminders_frame, bg="#ecf0f1", relief="groove", bd=2)
        upcoming_frame.pack(fill="both", expand=True, padx=50, pady=10)
        tk.Label(upcoming_frame, text="Upcoming Tasks (Next 3 days):", font=("Arial", 12, "bold"), bg="#ecf0f1").pack(pady=10)
        
        scrollbar = tk.Scrollbar(upcoming_frame)
        scrollbar.pack(side="right", fill="y")
        self.upcoming_listbox = tk.Listbox(upcoming_frame, font=("Arial", 10), yscrollcommand=scrollbar.set, bg="white", height=8)
        self.upcoming_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.config(command=self.upcoming_listbox.yview)
        self.update_upcoming_tasks()
        

    # ==============================================================================================================================================================================================================
    # Category Interface
    # ==============================================================================================================================================================================================================

    def create_category_tab(self):
        """Create Category Management tab"""
        self.category_frame = tk.Frame(self.content_frame, bg="white")

        tk.Label(self.category_frame, text="Category Management", font=("Arial", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=(20,10))

        list_frame = tk.Frame(self.category_frame, bg="white")
        list_frame.pack(padx=20, pady=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.category_listbox = tk.Listbox(list_frame, font=("Arial", 11), yscrollcommand=scrollbar.set, bg="white", fg="#2c3e50", selectbackground="#3498db", selectforeground="white")
        self.category_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.category_listbox.yview)

        self.category_listbox.bind("<<ListboxSelect>>", self.show_category_tasks)

        self.category_task_listbox = tk.Listbox(self.category_frame, font=("Arial", 10), bg="#ecf0f1", height=10)
        self.category_task_listbox.pack(fill="both", expand=True, padx=20, pady=10)


        btn_frame = tk.Frame(self.category_frame, bg="white")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Add Category", font=("Arial", 11), bg="#2ecc71", fg="white", width=15, command=self.add_category_gui).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Edit Category", font=("Arial", 11), bg="#f39c12", fg="white", width=15, command=self.edit_category_gui).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Delete Category", font=("Arial", 11), bg="#e74c3c", fg="white", width=15, command=self.delete_category_gui).pack(side="left", padx=10)

        self.update_category_listbox()


    # ==============================================================================================================================================================================================================
    # Task Manager Function
    # ==============================================================================================================================================================================================================

    def create_task_gui(self):
        """Create Task"""
        title = self.title_var.get().strip()
        description = self.desc_text.get("1.0", "end-1c").strip()
        due_date = self.due_date_var.get().strip()
        due_time = self.due_time_var.get().strip()
        priority = self.priority_var.get()
        status = self.status_var.get()
        category_name = self.category_var.get()        
        category_id = 1
        for cid, name in self.logic.categories.items():
          if name == category_name:
              category_id = cid
              break
            
        success, message = self.logic.create_task(title, description, due_date, due_time, priority, status, category_id)
        if success:
            self.clear_form()
            self.view_all_tasks()
            self.update_statistics()
            self.update_upcoming_tasks()
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
    
    def update_task_gui(self):
        """Update Task"""
        if self.editing_task_id is None:
            messagebox.showwarning("No Task", "Please edit a task first.")
            return
        
        category_name = self.category_var.get()
        category_id = 1
        for cid, name in self.logic.categories.items():
          if name == category_name:
              category_id = cid
              break
            
        new_data = {
            'title': self.title_var.get().strip(),
            'description': self.desc_text.get("1.0", "end-1c").strip(),
            'due_date': self.due_date_var.get().strip(),
            'due_time': self.due_time_var.get().strip(),
            'priority': self.priority_var.get(),
            'status': self.status_var.get(),
            'category_id': category_id
        }
        for i, task in enumerate(self.logic.tasks):
            if task['id'] == self.editing_task_id:
                success, message = self.logic.edit_task(i, new_data)
                if success:
                    self.clear_form()
                    self.editing_task_id = None
                    self.view_all_tasks()
                    self.update_statistics()
                    self.update_upcoming_tasks()
                    messagebox.showinfo("Success", message)
                else:
                    messagebox.showerror("Error", message)
                return
            
        messagebox.showerror("Error", "Task not found.")

        
    def clear_form(self):
        """Clear all input fields"""
        self.title_var.set("")
        self.desc_text.delete("1.0", "end")
        self.due_date_var.set("")
        self.due_time_var.set("00:00")
        self.priority_var.set("Medium")
        self.status_var.set("To Do")
        self.category_var.set("Others")
        self.editing_task_id = None


    # ==============================================================================================================================================================================================================
    # Task Tacker Function
    # ==============================================================================================================================================================================================================
    
    def view_all_tasks(self):
        """View All Task"""
        self.task_listbox.delete(0, "end")
        sorted_tasks = self.logic.get_sorted_tasks()
        
        if not sorted_tasks:
            self.task_listbox.insert("end", "No tasks available. Create some tasks first!")
            return
        
        for i, task in enumerate(sorted_tasks, 1):
            due_str = task['due_date'] if task['due_date'] != "N/A" else "No due date"
            status_icon = "✓" if task['status'] == "Completed" else "⏳"
            
            # Definition priority_color
            priority_color = {
                "High": "🔴",
                "Medium": "🟡", 
                "Low": "🟢"
            }.get(task['priority'], "⚪")
            
            description = task['description']
            desc_display = "(No desc)" if not description or description == "NULL" else (description[:17] + "..." if len(description) > 20 else description)
            category = self.logic.categories.get(task.get("category_id", 1), "Others")
            
            task_text = (
                f"{i:3d}. {status_icon} {priority_color} {task['title']} "
                f"| {category} | Desc: {desc_display} | Due: {due_str} | Priority: {task['priority']}"
            )
            self.task_listbox.insert("end", task_text)
        self.update_statistics()
    
    def delete_task_gui(self):
        """Delete Task"""
        selected = self.task_listbox.curselection() #Use curselection()get index of the selected task
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
            return
        
        task_index = selected[0]
        sorted_tasks = self.logic.get_sorted_tasks() #Use logic to sorting tasks
        if 0 <= task_index < len(sorted_tasks):
            task_to_delete = sorted_tasks[task_index]
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete:\n'{task_to_delete['title']}'?"):
                for i, task in enumerate(self.logic.tasks):
                    if task['id'] == task_to_delete['id']:
                        success, message = self.logic.delete_task(i)
                        if success:#Update View Task List
                            self.view_all_tasks()
                            self.update_upcoming_tasks()
                            messagebox.showinfo("Success", message)
                        else:
                            messagebox.showerror("Error", message)
                        break
    
    def edit_selected_task(self):
        """Edit Task"""
        selected = self.task_listbox.curselection() #Use curselection()get index of the selected task
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to edit.")
            return
        
        task_index = selected[0]
        sorted_tasks = self.logic.get_sorted_tasks() #Use logic to sorting tasks
        if 0 <= task_index < len(sorted_tasks):
            task = sorted_tasks[task_index]
            self.editing_task_id = task['id']
            self.title_var.set(task['title'])
            self.desc_text.delete("1.0", "end")
            self.desc_text.insert("1.0", task['description'])
            if task['due_date'] != "N/A":
                date_part, time_part = self.logic.parse_datetime_string(task['due_date'])
                if date_part: self.due_date_var.set(date_part)
                if time_part: self.due_time_var.set(time_part)
            else:
                self.due_date_var.set("")
                self.due_time_var.set("00:00")
            cat_id = task.get("category_id", 1)

            if cat_id in self.logic.categories:
                cat_name = self.logic.categories[cat_id]
            else:
                cat_name = "Others"
            
            self.priority_var.set(task['priority'])
            self.status_var.set(task['status'])
            self.category_var.set(cat_name)
            self.switch_tab("Task Manager")

    def update_statistics(self):
        """Update Statistics"""
        stats = self.logic.get_task_statistics()
        self.total_label.config(text=f"Total Tasks: {stats['total']}")
        self.completed_label.config(text=f"Completed: {stats['completed']}")
        self.pending_label.config(text=f"Pending: {stats['pending']}")
        self.overdue_label.config(text=f"Overdue: {stats['overdue']}")
        

    # ==============================================================================================================================================================================================================
    # Reminders Function
    # ==============================================================================================================================================================================================================
    
    def update_upcoming_tasks(self):
        """Update Upcoming Task"""
        self.upcoming_listbox.delete(0, "end")
        upcoming = self.logic.get_upcoming_tasks()
        if not upcoming:
            self.upcoming_listbox.insert("end", "No tasks due in the next 3 days")
        else:
            for task in upcoming:
                self.upcoming_listbox.insert("end", f"{task['title']} - Due: {task['due_date']}")
    
    def update_notification_status(self):
        """Update Notification Status"""
        status = self.notification_var.get()
        success, message = self.logic.set_notification_status(status)
        if not success: messagebox.showerror("Error", message)
    
    def update_reminder_time(self):
        """Update Reminder Time"""
        new_time = self.time_var.get().strip()
        success, message = self.logic.set_reminder_time(new_time)
        if success: messagebox.showinfo("Success", message)
        else: messagebox.showerror("Error", message)
    
    def check_reminders(self):
        """Check reminders every 60 seconds"""
        should_trigger, message = self.logic.check_reminder_trigger()
        if should_trigger: messagebox.showwarning("Reminder", message)
        self.root.after(60000, self.check_reminders)


    
    # ==============================================================================================================================================================================================================
    # Category Function
    # ==============================================================================================================================================================================================================
    

    def show_category_tasks(self, event):
        """Show The Selected Category Task"""
        selected = self.category_listbox.curselection()#Use curselection()get index of the selected category
        self.category_task_listbox.delete(0, "end")
        if not selected:
            return

        idx = selected[0]
        cid = list(self.logic.categories.keys())[idx]

        tasks_in_cat = [t for t in self.logic.tasks if t.get("category_id", 1) == cid]

        if not tasks_in_cat:
            self.category_task_listbox.insert("end", "No tasks in this category")
        else:
            for i, task in enumerate(tasks_in_cat, 1):
                status_icon = "✓" if task['status'] == "Completed" else "⏳"
                due_str = task['due_date'] if task['due_date'] != "N/A" else "No due date"
                self.category_task_listbox.insert("end", f"{i}. {status_icon} {task['title']} | Due: {due_str} | Status: {task['status']}")

    def update_category_listbox(self):
        """Update Category Listbox"""
        self.category_listbox.delete(0, "end")
        for cid, name in self.logic.categories.items():
            self.category_listbox.insert("end", f"{cid}: {name}")

    def add_category_gui(self):
        """Add New Category"""
        new_cat = tk.simpledialog.askstring("Add Category", "Enter new category name:")
        if new_cat:
            cid = max(self.logic.categories.keys(), default=0) + 1
            self.logic.categories[cid] = new_cat
            self.update_category_listbox()
            self.update_category_menu()

    def edit_category_gui(self):
        """Edit Category(Change Category Name)"""
        selected = self.category_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a category to edit.")
            return
        idx = selected[0]
        cid = list(self.logic.categories.keys())[idx]
        old_name = self.logic.categories[cid]
        new_name = tk.simpledialog.askstring("Edit Category", f"Edit category '{old_name}':")
        if new_name:
            self.logic.categories[cid] = new_name
            self.update_category_listbox()
            self.update_category_menu()

    def delete_category_gui(self):
        """Delete Category"""
        selected = self.category_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a category to delete.")
            return
        idx = selected[0]
        cid = list(self.logic.categories.keys())[idx]
        if messagebox.askyesno("Confirm Delete", f"Delete category '{self.logic.categories[cid]}'?"):
            del self.logic.categories[cid]
            self.update_category_listbox()
            self.update_category_menu()

    def update_category_menu(self):
        """Update Category Menu"""
        menu = self.category_menu['menu']
        menu.delete(0, 'end')
        for name in self.logic.categories.values():
            menu.add_command(label=name, command=lambda v=name: self.category_var.set(v))
    
    def focus_create_task(self):
        self.switch_tab("Task Manager")
        self.clear_form()
    
    def show_about(self):
        """Show program information"""
        messagebox.showinfo("About Task Assistant", "Task Management Assistant\nVersion 2.0\nBuilt with tkinter")

