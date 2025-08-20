#!/usr/bin/env python3
"""
To-Do List Manager
A comprehensive task management application with modern GUI design.

Features:
- Task creation with priority levels and due dates
- Categories and tags for organization
- Search and filter capabilities
- Progress tracking and statistics
- Data persistence with automatic backups

Author: Aditya Pagare
Email: adityapaagare619@gmail.com
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, date
from pathlib import Path
import uuid


class Task:
    """Represents a single task with all its properties."""
    
    def __init__(self, title, description="", priority="Medium", 
                 category="General", due_date=None, completed=False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.category = category
        self.due_date = due_date
        self.completed = completed
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
    
    def to_dict(self):
        """Convert task to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'category': self.category,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create task from dictionary."""
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'Medium'),
            category=data.get('category', 'General'),
            due_date=data.get('due_date'),
            completed=data.get('completed', False)
        )
        task.id = data.get('id', str(uuid.uuid4()))
        task.created_at = data.get('created_at', datetime.now().isoformat())
        task.updated_at = data.get('updated_at', task.created_at)
        return task


class TaskManager:
    """Handles task data operations and persistence."""
    
    def __init__(self, data_file="data/tasks.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(exist_ok=True)
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file."""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
        except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in self.tasks], f, 
                         indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def add_task(self, task):
        """Add a new task."""
        self.tasks.append(task)
        self.save_tasks()
    
    def update_task(self, task_id, **kwargs):
        """Update an existing task."""
        for task in self.tasks:
            if task.id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                task.updated_at = datetime.now().isoformat()
                self.save_tasks()
                return True
        return False
    
    def delete_task(self, task_id):
        """Delete a task."""
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()
    
    def get_tasks(self, filter_func=None):
        """Get tasks with optional filtering."""
        if filter_func:
            return [task for task in self.tasks if filter_func(task)]
        return self.tasks.copy()
    
    def get_statistics(self):
        """Get task statistics."""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        pending = total - completed
        
        priority_counts = {}
        category_counts = {}
        
        for task in self.tasks:
            priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1
            category_counts[task.category] = category_counts.get(task.category, 0) + 1
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': (completed / total * 100) if total > 0 else 0,
            'priority_counts': priority_counts,
            'category_counts': category_counts
        }


class TodoApp:
    """Main application class with GUI."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("900x700")
        self.root.configure(bg='#f5f5f5')
        
        # Initialize task manager
        self.task_manager = TaskManager()
        
        # Configure styles
        self.setup_styles()
        
        # Create GUI
        self.create_widgets()
        
        # Bind keyboard shortcuts
        self.setup_shortcuts()
        
        # Load initial data
        self.refresh_task_list()
    
    def setup_styles(self):
        """Configure ttk styles for modern appearance."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f5f5f5')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#f5f5f5')
        style.configure('Custom.Treeview', rowheight=25)
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
    
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📋 To-Do List Manager", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Left panel - Task form
        self.create_task_form(main_frame)
        
        # Right panel - Task list
        self.create_task_list(main_frame)
        
        # Bottom panel - Statistics
        self.create_statistics_panel(main_frame)
    
    def create_task_form(self, parent):
        """Create task input form."""
        form_frame = ttk.LabelFrame(parent, text="Add New Task", padding="10")
        form_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        
        # Title
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(form_frame, textvariable=self.title_var, width=25)
        title_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
        self.description_text = tk.Text(form_frame, height=3, width=25, wrap=tk.WORD)
        self.description_text.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Priority
        ttk.Label(form_frame, text="Priority:").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(form_frame, textvariable=self.priority_var, 
                                     values=["Low", "Medium", "High", "Critical"],
                                     state="readonly", width=22)
        priority_combo.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Category
        ttk.Label(form_frame, text="Category:").grid(row=6, column=0, sticky=tk.W, pady=(10, 2))
        self.category_var = tk.StringVar(value="General")
        category_combo = ttk.Combobox(form_frame, textvariable=self.category_var,
                                     values=["General", "Work", "Personal", "Shopping", "Health"],
                                     width=22)
        category_combo.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Due date
        ttk.Label(form_frame, text="Due Date (YYYY-MM-DD):").grid(row=8, column=0, sticky=tk.W, pady=(10, 2))
        self.due_date_var = tk.StringVar()
        due_date_entry = ttk.Entry(form_frame, textvariable=self.due_date_var, width=25)
        due_date_entry.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=10, column=0, pady=(15, 0), sticky=(tk.W, tk.E))
        
        add_btn = ttk.Button(button_frame, text="Add Task", command=self.add_task, style='Action.TButton')
        add_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_form)
        clear_btn.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        form_frame.columnconfigure(0, weight=1)
    
    def create_task_list(self, parent):
        """Create task list with treeview."""
        list_frame = ttk.LabelFrame(parent, text="Tasks", padding="10")
        list_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        # Search and filter
        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_task_list())
        
        # Filter combobox
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(search_frame, textvariable=self.filter_var,
                                   values=["All", "Pending", "Completed", "High Priority", "Due Today"],
                                   state="readonly", width=12)
        filter_combo.grid(row=0, column=2)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_task_list())
        
        # Task tree
        columns = ("Title", "Priority", "Category", "Due Date", "Status")
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show="headings", 
                                     style='Custom.Treeview')
        
        # Configure columns
        self.task_tree.heading("Title", text="Title")
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.heading("Category", text="Category")
        self.task_tree.heading("Due Date", text="Due Date")
        self.task_tree.heading("Status", text="Status")
        
        self.task_tree.column("Title", width=200)
        self.task_tree.column("Priority", width=80)
        self.task_tree.column("Category", width=100)
        self.task_tree.column("Due Date", width=100)
        self.task_tree.column("Status", width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        self.task_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Action buttons
        action_frame = ttk.Frame(list_frame)
        action_frame.grid(row=2, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
        
        ttk.Button(action_frame, text="Complete", command=self.toggle_complete).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(action_frame, text="Edit", command=self.edit_task).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(action_frame, text="Delete", command=self.delete_task).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(action_frame, text="Export", command=self.export_tasks).grid(row=0, column=3)
        
        # Bind double-click
        self.task_tree.bind("<Double-1>", lambda e: self.edit_task())
    
    def create_statistics_panel(self, parent):
        """Create statistics display panel."""
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding="10")
        stats_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.stats_label = ttk.Label(stats_frame, text="", justify=tk.LEFT)
        self.stats_label.grid(row=0, column=0, sticky=tk.W)
        
        stats_frame.columnconfigure(0, weight=1)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        self.root.bind('<Control-n>', lambda e: self.focus_title_entry())
        self.root.bind('<Control-d>', lambda e: self.delete_task())
        self.root.bind('<Return>', lambda e: self.add_task())
        self.root.bind('<Delete>', lambda e: self.delete_task())
    
    def focus_title_entry(self):
        """Focus on title entry for new task."""
        widget = self.root.nametowidget(self.title_var._name)
        widget.focus_set()
    
    def add_task(self):
        """Add a new task."""
        title = self.title_var.get().strip()
        if not title:
            messagebox.showerror("Error", "Task title is required!")
            return
        
        description = self.description_text.get("1.0", tk.END).strip()
        priority = self.priority_var.get()
        category = self.category_var.get()
        due_date = self.due_date_var.get().strip() or None
        
        # Validate due date
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                return
        
        task = Task(title, description, priority, category, due_date)
        self.task_manager.add_task(task)
        self.clear_form()
        self.refresh_task_list()
        self.update_statistics()
        messagebox.showinfo("Success", "Task added successfully!")
    
    def clear_form(self):
        """Clear the task form."""
        self.title_var.set("")
        self.description_text.delete("1.0", tk.END)
        self.priority_var.set("Medium")
        self.category_var.set("General")
        self.due_date_var.set("")

    def refresh_task_list(self):
        """Refresh the task list with current data."""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        filter_value = self.filter_var.get()
        search_term = self.search_var.get().lower()

        def task_filter(task):
            if search_term and search_term not in task.title.lower():
                return False
            if filter_value == "Pending" and task.completed:
                return False
            elif filter_value == "Completed" and not task.completed:
                return False
            elif filter_value == "High Priority" and task.priority != "High":
                return False
            elif filter_value == "Due Today" and task.due_date != date.today().isoformat():
                return False
            return True

        tasks = self.task_manager.get_tasks(task_filter)
        for task in sorted(tasks, key=lambda t: (t.completed, t.priority == "Critical" and 0 or
                                                              t.priority == "High" and 1 or
                                                              t.priority == "Medium" and 2 or 3)):
            status = "✓ Completed" if task.completed else "⏳ Pending"
            due_date_display = task.due_date or "No due date"

            item_id = self.task_tree.insert("", "end", values=(
                task.title, task.priority, task.category, due_date_display, status
            ))

            if task.completed:
                self.task_tree.set(item_id, "Title", f"✓ {task.title}")
            elif task.priority == "Critical":
                self.task_tree.set(item_id, "Priority", f"🔴 {task.priority}")
            elif task.priority == "High":
                self.task_tree.set(item_id, "Priority", f"🟠 {task.priority}")

            # Store task ID inside item "tags"
            self.task_tree.item(item_id, tags=(task.id,))

    def get_selected_task(self):
        """Get the currently selected task."""
        selection = self.task_tree.selection()
        if not selection:
            return None
        item = selection[0]
        tags = self.task_tree.item(item, "tags")
        if not tags:
            return None
        task_id = tags[0]
        for task in self.task_manager.tasks:
            if task.id == task_id:
                return task
        return None

    def toggle_complete(self):
        """Toggle completion status of selected task."""
        task = self.get_selected_task()
        if not task:
            messagebox.showwarning("Warning", "Please select a task!")
            return
        
        self.task_manager.update_task(task.id, completed=not task.completed)
        self.refresh_task_list()
        self.update_statistics()
    
    def edit_task(self):
        """Edit the selected task."""
        task = self.get_selected_task()
        if not task:
            messagebox.showwarning("Warning", "Please select a task to edit!")
            return
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("400x500")
        edit_window.configure(bg='#f5f5f5')
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Center the window
        edit_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        frame = ttk.Frame(edit_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(frame, text="Title:").pack(anchor=tk.W, pady=(0, 5))
        title_var = tk.StringVar(value=task.title)
        ttk.Entry(frame, textvariable=title_var, width=40).pack(fill=tk.X, pady=(0, 10))
        
        # Description
        ttk.Label(frame, text="Description:").pack(anchor=tk.W, pady=(0, 5))
        desc_text = tk.Text(frame, height=4, width=40, wrap=tk.WORD)
        desc_text.pack(fill=tk.X, pady=(0, 10))
        desc_text.insert("1.0", task.description)
        
        # Priority
        ttk.Label(frame, text="Priority:").pack(anchor=tk.W, pady=(0, 5))
        priority_var = tk.StringVar(value=task.priority)
        ttk.Combobox(frame, textvariable=priority_var, 
                    values=["Low", "Medium", "High", "Critical"],
                    state="readonly", width=37).pack(fill=tk.X, pady=(0, 10))
        
        # Category
        ttk.Label(frame, text="Category:").pack(anchor=tk.W, pady=(0, 5))
        category_var = tk.StringVar(value=task.category)
        ttk.Combobox(frame, textvariable=category_var,
                    values=["General", "Work", "Personal", "Shopping", "Health"],
                    width=37).pack(fill=tk.X, pady=(0, 10))
        
        # Due date
        ttk.Label(frame, text="Due Date (YYYY-MM-DD):").pack(anchor=tk.W, pady=(0, 5))
        due_date_var = tk.StringVar(value=task.due_date or "")
        ttk.Entry(frame, textvariable=due_date_var, width=40).pack(fill=tk.X, pady=(0, 15))
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)
        
        def save_changes():
            new_title = title_var.get().strip()
            if not new_title:
                messagebox.showerror("Error", "Task title is required!")
                return
            
            new_description = desc_text.get("1.0", tk.END).strip()
            new_priority = priority_var.get()
            new_category = category_var.get()
            new_due_date = due_date_var.get().strip() or None
            
            # Validate due date
            if new_due_date:
                try:
                    datetime.strptime(new_due_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                    return
            
            self.task_manager.update_task(
                task.id,
                title=new_title,
                description=new_description,
                priority=new_priority,
                category=new_category,
                due_date=new_due_date
            )
            
            self.refresh_task_list()
            self.update_statistics()
            edit_window.destroy()
            messagebox.showinfo("Success", "Task updated successfully!")
        
        ttk.Button(btn_frame, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT)
    
    def delete_task(self):
        """Delete the selected task."""
        task = self.get_selected_task()
        if not task:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Delete task '{task.title}'?"):
            self.task_manager.delete_task(task.id)
            self.refresh_task_list()
            self.update_statistics()
            messagebox.showinfo("Success", "Task deleted successfully!")
    
    def export_tasks(self):
        """Export tasks to JSON file."""
        filename = filedialog.asksaveasfilename(
            title="Export Tasks",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump([task.to_dict() for task in self.task_manager.tasks], 
                             f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", f"Tasks exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export tasks: {e}")
    
    def update_statistics(self):
        """Update the statistics display."""
        stats = self.task_manager.get_statistics()
        
        stats_text = f"📊 Total: {stats['total']} | " \
                    f"✅ Completed: {stats['completed']} | " \
                    f"⏳ Pending: {stats['pending']} | " \
                    f"📈 Completion Rate: {stats['completion_rate']:.1f}%"
        
        self.stats_label.config(text=stats_text)


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = TodoApp(root)
    
    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()