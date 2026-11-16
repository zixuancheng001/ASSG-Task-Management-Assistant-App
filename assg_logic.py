"""
assg_logic.py - Task Management Business Logic Module
Contains all core business logic, separated from GUI
"""
from datetime import datetime
import json
import os

class TaskManagerLogic:
    """Task management business logic class"""
    
    def __init__(self):
        """Initialize task manager"""
        self.tasks = []
        self.task_id_counter = 1
        self.reminder_time = "12:00"
        self.reminder_status = "On"
        
        # Priority weights for urgency calculation
        self.PRIORITY_WEIGHTS = {"High": 10, "Medium": 5, "Low": 1}
        self.TIME_MULTIPLIERS = {"High": 3, "Medium": 2, "Low": 1, "N/A": 0.5}
        # Category
        self.categories = {1: "Others",2: "Study",3: "Work",4: "Personal"}
        self.category_id_counter = 5

        self.data_file = "task_data.json"
        self.load_data()

    def save_data(self):
        data = {
            "tasks": self.tasks,
            "categories": self.categories,
            "task_id_counter": self.task_id_counter,
            "reminder_time": self.reminder_time,
            "reminder_status": self.reminder_status
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    saved_cats = data.get("categories", {"1": "Others"})
                    self.categories = {int(k): v for k, v in saved_cats.items()}
                    self.task_id_counter = data.get("task_id_counter", 1)
                    self.reminder_time = data.get("reminder_time", "12:00")
                    self.reminder_status = data.get("reminder_status", "On")
            except Exception as e:
                print(f"Error loading data: {e}")

    # ==============================================================================================================================================================================================================
    # Create Task
    # ==============================================================================================================================================================================================================
    
    def create_task(self, title, description, due_date, due_time, priority, status,category_id =1):
        """Create a new task"""
        # Validate input
        if not title:
            return False, "Title cannot be empty!"
        
        if not description:
            description = "NULL"
        
        # Validate date and time if provided
        due_date_str = "N/A"
        if due_date:
            # Validate date format
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
                due_datetime = datetime.strptime(due_date, "%Y-%m-%d")
                
                # Check if date is in the past
                if due_datetime.date() < datetime.now().date():
                    return False, "Due date cannot be in the past!"
                
                # Add time if provided
                if due_time:
                    # Validate time format
                    try:
                        datetime.strptime(due_time, "%H:%M")
                        due_date_str = f"{due_date} {due_time}"
                    except ValueError:
                        return False, "Invalid time format! Use HH:MM (24-hour)"
                else:
                    due_date_str = f"{due_date} 00:00"
                    
            except ValueError:
                return False, "Invalid date format! Use YYYY-MM-DD"
        else:
            due_date_str = "N/A"
        
        # Create task dictionary
        new_task = {
            "id": self.task_id_counter,
            "title": title,
            "description": description,
            "due_date": due_date_str,
            "priority": priority,
            "status": status,
            "completed_at": None,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category_id": category_id,
        }
        
        # Set completion time if task is completed
        if status == "Completed":
            new_task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        self.tasks.append(new_task)
        self.task_id_counter += 1

        self.save_data()
        return True, f"Task '{title}' created successfully!"

    # ==============================================================================================================================================================================================================
    # Delete Task
    # ==============================================================================================================================================================================================================
    
    def delete_task(self, task_index):
        """Delete a task by index"""
        if not self.tasks:
            return False, "No tasks to delete!"
        
        if 0 <= task_index < len(self.tasks):
            removed_task = self.tasks.pop(task_index)
            self.save_data()
            return True, f"Task '{removed_task['title']}' deleted successfully!"
        
        return False, "Invalid task index!"

    # ==============================================================================================================================================================================================================
    # Edit Task
    # ==============================================================================================================================================================================================================
    
    def edit_task(self, task_index, new_data):
        """Edit an existing task"""
        if not self.tasks:
            return False, "No tasks to edit!"
        
        if 0 <= task_index < len(self.tasks):
            task = self.tasks[task_index]
            
            # Update task data with provided values
            if 'title' in new_data and new_data['title']:
                task['title'] = new_data['title']
            
            if 'description' in new_data:
                task['description'] = new_data['description'] if new_data['description'] else "NULL"
            
            if 'due_date' in new_data and 'due_time' in new_data:
                if new_data['due_date']:
                    try:
                        # Validate date
                        datetime.strptime(new_data['due_date'], "%Y-%m-%d")
                        
                        # Check if date is in the past
                        due_datetime = datetime.strptime(new_data['due_date'], "%Y-%m-%d")
                        if due_datetime.date() < datetime.now().date():
                            return False, "Due date cannot be in the past!"
                        
                        # Add time if provided
                        if new_data['due_time']:
                            # Validate time
                            try:
                                datetime.strptime(new_data['due_time'], "%H:%M")
                                task['due_date'] = f"{new_data['due_date']} {new_data['due_time']}"
                            except ValueError:
                                return False, "Invalid time format! Use HH:MM (24-hour)"
                        else:
                            task['due_date'] = f"{new_data['due_date']} 00:00"
                            
                    except ValueError:
                        return False, "Invalid date format! Use YYYY-MM-DD"
                else:
                    task['due_date'] = "N/A"
            
            if 'priority' in new_data:
                task['priority'] = new_data['priority']
            
            if 'status' in new_data:
                task['status'] = new_data['status']
                if new_data['status'] == "Completed" and not task['completed_at']:
                    task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                elif new_data['status'] != "Completed":
                    task['completed_at'] = None

            if 'category_id' in new_data:
                task['category_id'] = new_data['category_id']
            
            self.save_data()
            return True, "Task updated successfully!"
        
        return False, "Invalid task index!"

    # ==============================================================================================================================================================================================================
    # Task Statistics
    # ==============================================================================================================================================================================================================
    
    def get_task_statistics(self):
        """Get statistics about tasks"""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t['status'] == "Completed"])
        pending = total - completed
        
        # Count high priority tasks
        high_priority = len([t for t in self.tasks if t['priority'] == "High" and t['status'] == "To Do"])
        
        # Count overdue tasks
        overdue = 0
        now = datetime.now()
        for task in self.tasks:
            if task['status'] == "To Do" and task['due_date'] != "N/A":
                try:
                    due_date = datetime.strptime(task['due_date'], "%Y-%m-%d %H:%M")
                    if due_date < now:
                        overdue += 1
                except ValueError:
                    continue
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "high_priority": high_priority,
            "overdue": overdue
        }
    
    # ==============================================================================================================================================================================================================
    # Sorted Task
    # ==============================================================================================================================================================================================================
    
    def get_sorted_tasks(self):
        """Get tasks sorted by urgency"""
        if not self.tasks:
            return []
        
        return sorted(self.tasks, key=self.urgency_value, reverse=True)

    # ==============================================================================================================================================================================================================
    # Upcoming Task
    # ==============================================================================================================================================================================================================
    
    def get_upcoming_tasks(self, days=3):
        """Get tasks due within specified days (default 3 days)"""
        now = datetime.now()
        upcoming_tasks = []
        
        for task in self.tasks:
            if task['status'] == "To Do" and task['due_date'] != "N/A":
                try:
                    due_date = datetime.strptime(task['due_date'], "%Y-%m-%d %H:%M")
                    days_diff = (due_date - now).days
                    if 0 <= days_diff <= days:
                        upcoming_tasks.append(task)
                except ValueError:
                    continue
        
        return upcoming_tasks

    # ==============================================================================================================================================================================================================
    # Rank Level
    # ==============================================================================================================================================================================================================
    
    def rank_level(self, due_datetime):
        """Calculate urgency level based on time remaining"""
        if not due_datetime:
            return "Medium"
        
        now = datetime.now()
        time_remaining = (due_datetime - now).total_seconds() / 3600
        
        if time_remaining <= 24:
            return "High"
        elif time_remaining <= 72:
            return "Medium"
        else:
            return "Low"

    # ==============================================================================================================================================================================================================
    # Urgency Value
    # ==============================================================================================================================================================================================================
    
    def urgency_value(self, task):
        """Calculate urgency score for a task"""
        due_date_str = task.get("due_date", "N/A")
        user_priority = task.get("priority", "Medium")
        
        base_weight = self.PRIORITY_WEIGHTS.get(user_priority, 5)
        due_datetime = None
        time_level = "N/A"
        
        if due_date_str != "N/A" and due_date_str:
            try:
                due_datetime = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
                time_level = self.rank_level(due_datetime)
            except ValueError:
                pass
        
        time_multi = self.TIME_MULTIPLIERS.get(time_level, 0.5)
        urgency_score = base_weight * time_multi
        
        if due_date_str == "N/A":
            return base_weight * 0.1
        
        return urgency_score

    # ==============================================================================================================================================================================================================
    # Check Time Format
    # ==============================================================================================================================================================================================================
    
    def validate_time_format(self, time_str):
        """Validate time format (HH:MM)"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True, "Valid time format"
        except ValueError:
            return False, "Invalid time format! Use HH:MM (24-hour)"

    # ==============================================================================================================================================================================================================
    # Reminder Time
    # ==============================================================================================================================================================================================================
    
    def set_reminder_time(self, time_str):
        """Set reminder time"""
        valid, message = self.validate_time_format(time_str)
        if valid:
            self.reminder_time = time_str
            return True, f"Reminder time updated to {time_str}"
        return False, message
    
    # ==============================================================================================================================================================================================================
    # Notification Status
    # ==============================================================================================================================================================================================================
    
    def set_notification_status(self, status):
        """Set notification status (On/Off)"""
        if status in ["On", "Off"]:
            self.reminder_status = status
            return True, f"Notification status set to {status}"
        return False, "Invalid status! Use 'On' or 'Off'"

    # ==============================================================================================================================================================================================================
    # Reminder Trigger
    # ==============================================================================================================================================================================================================
    
    def check_reminder_trigger(self):
        """Check if reminder should be triggered"""
        now = datetime.now().strftime("%H:%M")
        pending_tasks = len([t for t in self.tasks if t['status'] == "To Do"])
        
        if self.reminder_status == "On" and now == self.reminder_time and pending_tasks > 0:
            return True, f"Reminder: It's {now}\nYou have {pending_tasks} pending task(s)."
        
        return False, ""

    # ==============================================================================================================================================================================================================
    # Get Task ID
    # ==============================================================================================================================================================================================================
    
    def get_task_by_id(self, task_id):
        """Get task by ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

    # ==============================================================================================================================================================================================================
    # Update Task Category
    # ==============================================================================================================================================================================================================
    
    def update_task_category(self, task_id, category_id):
        task = self.get_task_by_id(task_id)
        if task:
            task['category_id'] = category_id
            return True, "Category updated successfully!"
        return False, "Task not found!"

    # ==============================================================================================================================================================================================================
    # Parse Datetime String
    # ==============================================================================================================================================================================================================
    
    def parse_datetime_string(self, datetime_str):
        """Parse datetime string and return date and time separately"""
        if datetime_str == "N/A":
            return None, None
        
        try:
            dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M")
        except ValueError:
            return None, None
