#!/usr/bin/env python3
"""
Contact Manager Pro
A comprehensive contact management system with advanced search and organization features.

Features:
- Complete contact information management
- Advanced search and filtering
- Contact groups and tags
- Import/Export functionality (CSV, JSON)
- Backup and restore capabilities
- Contact photo support
- Data validation and deduplication

Author: Aditya Pagare
Email: adityapaagare619@gmail.com
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import json
import csv
import re
from pathlib import Path
from datetime import datetime
import uuid


class ContactDatabase:
    """Handles SQLite database operations for contacts."""

    def __init__(self, db_file="data/contacts.db"):
        self.db_file = Path(db_file)
        self.db_file.parent.mkdir(exist_ok=True)
        self.init_database()

    def init_database(self):
        """Initialize database with required tables."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Create contacts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                company TEXT,
                notes TEXT,
                tags TEXT,
                photo_path TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')

        # Create groups table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TEXT
            )
        ''')

        # Create contact_groups junction table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_groups (
                contact_id TEXT,
                group_id TEXT,
                PRIMARY KEY (contact_id, group_id),
                FOREIGN KEY (contact_id) REFERENCES contacts (id),
                FOREIGN KEY (group_id) REFERENCES groups (id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_contact(self, contact_data):
        """Add a new contact to the database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        contact_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        cursor.execute('''
            INSERT INTO contacts (id, name, phone, email, address, company, notes, tags, photo_path, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            contact_id,
            contact_data.get('name', ''),
            contact_data.get('phone', ''),
            contact_data.get('email', ''),
            contact_data.get('address', ''),
            contact_data.get('company', ''),
            contact_data.get('notes', ''),
            contact_data.get('tags', ''),
            contact_data.get('photo_path', ''),
            now,
            now
        ))

        conn.commit()
        conn.close()
        return contact_id

    def update_contact(self, contact_id, contact_data):
        """Update an existing contact."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        now = datetime.now().isoformat()

        cursor.execute('''
            UPDATE contacts SET 
                name = ?, phone = ?, email = ?, address = ?, company = ?, 
                notes = ?, tags = ?, photo_path = ?, updated_at = ?
            WHERE id = ?
        ''', (
            contact_data.get('name', ''),
            contact_data.get('phone', ''),
            contact_data.get('email', ''),
            contact_data.get('address', ''),
            contact_data.get('company', ''),
            contact_data.get('notes', ''),
            contact_data.get('tags', ''),
            contact_data.get('photo_path', ''),
            now,
            contact_id
        ))

        conn.commit()
        conn.close()

    def delete_contact(self, contact_id):
        """Delete a contact from the database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Delete from contact_groups first
        cursor.execute('DELETE FROM contact_groups WHERE contact_id = ?', (contact_id,))

        # Delete contact
        cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))

        conn.commit()
        conn.close()

    def get_all_contacts(self):
        """Get all contacts from the database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM contacts ORDER BY name')
        contacts = cursor.fetchall()

        conn.close()

        # Convert to list of dictionaries
        columns = ['id', 'name', 'phone', 'email', 'address', 'company', 'notes', 'tags', 'photo_path', 'created_at',
                   'updated_at']
        return [dict(zip(columns, contact)) for contact in contacts]

    def search_contacts(self, search_term):
        """Search contacts by name, phone, or email."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        search_pattern = f'%{search_term}%'
        cursor.execute('''
            SELECT * FROM contacts 
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? 
            ORDER BY name
        ''', (search_pattern, search_pattern, search_pattern))

        contacts = cursor.fetchall()
        conn.close()

        columns = ['id', 'name', 'phone', 'email', 'address', 'company', 'notes', 'tags', 'photo_path', 'created_at',
                   'updated_at']
        return [dict(zip(columns, contact)) for contact in contacts]

    def get_contact_by_id(self, contact_id):
        """Get a specific contact by ID."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
        contact = cursor.fetchone()

        conn.close()

        if contact:
            columns = ['id', 'name', 'phone', 'email', 'address', 'company', 'notes', 'tags', 'photo_path',
                       'created_at', 'updated_at']
            return dict(zip(columns, contact))
        return None

    def backup_database(self, backup_file):
        """Create a backup of the database."""
        conn = sqlite3.connect(self.db_file)
        backup_conn = sqlite3.connect(backup_file)
        conn.backup(backup_conn)
        backup_conn.close()
        conn.close()

    def get_statistics(self):
        """Get database statistics."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM contacts')
        total_contacts = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM contacts WHERE phone != ""')
        contacts_with_phone = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM contacts WHERE email != ""')
        contacts_with_email = cursor.fetchone()[0]

        conn.close()

        return {
            'total_contacts': total_contacts,
            'contacts_with_phone': contacts_with_phone,
            'contacts_with_email': contacts_with_email
        }


class ContactValidator:
    """Validates contact information."""

    @staticmethod
    def validate_email(email):
        """Validate email format."""
        if not email:
            return True  # Empty email is valid

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        """Validate phone number format."""
        if not phone:
            return True  # Empty phone is valid

        # Remove common separators
        clean_phone = re.sub(r'[\s\-\(\)\+\.]', '', phone)

        # Check if it contains only digits (and possibly starts with +)
        if phone.startswith('+'):
            return clean_phone[1:].isdigit() and len(clean_phone) >= 10
        else:
            return clean_phone.isdigit() and len(clean_phone) >= 10

    @staticmethod
    def validate_contact(contact_data):
        """Validate complete contact data."""
        errors = []

        # Name is required
        if not contact_data.get('name', '').strip():
            errors.append("Name is required")

        # Validate email if provided
        email = contact_data.get('email', '').strip()
        if email and not ContactValidator.validate_email(email):
            errors.append("Invalid email format")

        # Validate phone if provided
        phone = contact_data.get('phone', '').strip()
        if phone and not ContactValidator.validate_phone(phone):
            errors.append("Invalid phone number format")

        return errors


class ContactApp:
    """Main contact management application with GUI."""

    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager Pro")
        self.root.geometry("900x700")
        self.root.configure(bg='#f5f5f5')

        # Initialize database
        self.db = ContactDatabase()
        self.validator = ContactValidator()

        # Contact ID storage for treeview
        self.contact_id_map = {}  # item_id -> contact_id

        # Configure styles
        self.setup_styles()

        # Create GUI
        self.create_widgets()

        # Load initial data
        self.refresh_contact_list()

    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f5f5f5')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#f5f5f5')
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))

    def create_widgets(self):
        """Create and arrange GUI widgets."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="📇 Contact Manager Pro", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        # Left panel - Contact form
        self.create_contact_form(main_frame)

        # Right panel - Contact list
        self.create_contact_list(main_frame)

        # Bottom panel - Statistics and actions
        self.create_action_panel(main_frame)

    def create_contact_form(self, parent):
        """Create contact input form."""
        form_frame = ttk.LabelFrame(parent, text="Contact Information", padding="10")
        form_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))

        # Form fields
        fields = [
            ("Name*:", "name"),
            ("Phone:", "phone"),
            ("Email:", "email"),
            ("Company:", "company"),
            ("Address:", "address"),
            ("Tags:", "tags"),
            ("Notes:", "notes")
        ]

        self.form_vars = {}

        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(form_frame, text=label_text).grid(row=i * 2, column=0, sticky=tk.W, pady=(5, 2))

            if field_name in ["address", "notes"]:
                # Multi-line text for address and notes
                text_widget = tk.Text(form_frame, height=3, width=25, wrap=tk.WORD, font=('Arial', 10))
                text_widget.grid(row=i * 2 + 1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
                self.form_vars[field_name] = text_widget
            else:
                # Single-line entry
                var = tk.StringVar()
                entry = ttk.Entry(form_frame, textvariable=var, width=25)
                entry.grid(row=i * 2 + 1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
                self.form_vars[field_name] = var

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(fields) * 2, column=0, pady=(10, 0), sticky=(tk.W, tk.E))

        self.add_btn = ttk.Button(button_frame, text="Add Contact", command=self.add_contact, style='Action.TButton')
        self.add_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))

        self.update_btn = ttk.Button(button_frame, text="Update Contact", command=self.update_contact,
                                     state=tk.DISABLED)
        self.update_btn.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))

        self.clear_btn = ttk.Button(button_frame, text="Clear Form", command=self.clear_form)
        self.clear_btn.grid(row=0, column=2, sticky=(tk.W, tk.E))

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        form_frame.columnconfigure(0, weight=1)

        # Store for update mode
        self.current_contact_id = None

    def create_contact_list(self, parent):
        """Create contact list with treeview."""
        list_frame = ttk.LabelFrame(parent, text="Contacts", padding="10")
        list_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)

        # Search bar
        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.on_search_change)

        ttk.Button(search_frame, text="🔍", command=self.search_contacts, width=3).grid(row=0, column=2)

        # Contact tree
        columns = ("Name", "Phone", "Email", "Company")
        self.contact_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        # Configure columns
        self.contact_tree.heading("Name", text="Name")
        self.contact_tree.heading("Phone", text="Phone")
        self.contact_tree.heading("Email", text="Email")
        self.contact_tree.heading("Company", text="Company")

        self.contact_tree.column("Name", width=150)
        self.contact_tree.column("Phone", width=120)
        self.contact_tree.column("Email", width=180)
        self.contact_tree.column("Company", width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.contact_tree.yview)
        self.contact_tree.configure(yscrollcommand=scrollbar.set)

        self.contact_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))

        # Bind events
        self.contact_tree.bind('<Double-1>', self.on_contact_select)
        self.contact_tree.bind('<Button-3>', self.show_context_menu)  # Right-click

        # Action buttons
        action_frame = ttk.Frame(list_frame)
        action_frame.grid(row=2, column=0, pady=(10, 0), sticky=(tk.W, tk.E))

        ttk.Button(action_frame, text="Edit", command=self.edit_contact).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(action_frame, text="Delete", command=self.delete_contact).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(action_frame, text="View Details", command=self.view_contact_details).grid(row=0, column=2,
                                                                                              padx=(0, 5))
        ttk.Button(action_frame, text="Duplicate", command=self.duplicate_contact).grid(row=0, column=3)

    def create_action_panel(self, parent):
        """Create bottom action panel."""
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=2, column=0, columnspan=3, pady=(15, 0), sticky=(tk.W, tk.E))

        # Statistics
        stats_frame = ttk.LabelFrame(action_frame, text="Statistics", padding="5")
        stats_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        self.stats_label = ttk.Label(stats_frame, text="Loading statistics...")
        self.stats_label.grid(row=0, column=0)

        # Import/Export buttons
        io_frame = ttk.Frame(action_frame)
        io_frame.grid(row=0, column=1)

        ttk.Button(io_frame, text="📥 Import CSV", command=self.import_csv).grid(row=0, column=0, padx=2)
        ttk.Button(io_frame, text="📤 Export CSV", command=self.export_csv).grid(row=0, column=1, padx=2)
        ttk.Button(io_frame, text="💾 Backup", command=self.backup_database).grid(row=0, column=2, padx=2)
        ttk.Button(io_frame, text="🔧 Settings", command=self.show_settings).grid(row=0, column=3, padx=2)

        action_frame.columnconfigure(0, weight=1)

        # Update statistics
        self.update_statistics()

    def get_form_data(self):
        """Get data from form fields."""
        data = {}

        for field_name, widget in self.form_vars.items():
            if field_name in ["address", "notes"]:
                # Text widget
                data[field_name] = widget.get("1.0", tk.END).strip()
            else:
                # StringVar
                data[field_name] = widget.get().strip()

        return data

    def set_form_data(self, contact_data):
        """Set form fields with contact data."""
        for field_name, widget in self.form_vars.items():
            value = contact_data.get(field_name, "")

            if field_name in ["address", "notes"]:
                # Text widget
                widget.delete("1.0", tk.END)
                widget.insert("1.0", value)
            else:
                # StringVar
                widget.set(value)

    def clear_form(self):
        """Clear all form fields."""
        for field_name, widget in self.form_vars.items():
            if field_name in ["address", "notes"]:
                widget.delete("1.0", tk.END)
            else:
                widget.set("")

        self.current_contact_id = None
        self.add_btn.config(state=tk.NORMAL)
        self.update_btn.config(state=tk.DISABLED)

    def add_contact(self):
        """Add a new contact."""
        contact_data = self.get_form_data()

        # Validate data
        errors = self.validator.validate_contact(contact_data)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        # Check for duplicate
        if self.check_duplicate(contact_data):
            if not messagebox.askyesno("Duplicate Contact",
                                       "A contact with similar information already exists. Add anyway?"):
                return

        # Add to database
        try:
            self.db.add_contact(contact_data)
            self.clear_form()
            self.refresh_contact_list()
            self.update_statistics()
            messagebox.showinfo("Success", "Contact added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add contact: {str(e)}")

    def update_contact(self):
        """Update the current contact."""
        if not self.current_contact_id:
            messagebox.showerror("Error", "No contact selected for update!")
            return

        contact_data = self.get_form_data()

        # Validate data
        errors = self.validator.validate_contact(contact_data)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        # Update in database
        try:
            self.db.update_contact(self.current_contact_id, contact_data)
            self.clear_form()
            self.refresh_contact_list()
            self.update_statistics()
            messagebox.showinfo("Success", "Contact updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update contact: {str(e)}")

    def edit_contact(self):
        """Edit selected contact."""
        selected = self.contact_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to edit!")
            return

        item = selected[0]
        contact_id = self.contact_id_map.get(item)

        if contact_id:
            # Load contact data
            contact = self.db.get_contact_by_id(contact_id)
            if contact:
                self.set_form_data(contact)
                self.current_contact_id = contact_id
                self.add_btn.config(state=tk.DISABLED)
                self.update_btn.config(state=tk.NORMAL)

    def delete_contact(self):
        """Delete selected contact."""
        selected = self.contact_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete!")
            return

        item = selected[0]
        contact_name = self.contact_tree.item(item)['values'][0]

        if messagebox.askyesno("Confirm Delete", f"Delete contact '{contact_name}'?"):
            contact_id = self.contact_id_map.get(item)
            if contact_id:
                try:
                    self.db.delete_contact(contact_id)
                    self.refresh_contact_list()
                    self.update_statistics()
                    messagebox.showinfo("Success", "Contact deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete contact: {str(e)}")

    def duplicate_contact(self):
        """Duplicate selected contact."""
        selected = self.contact_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to duplicate!")
            return

        item = selected[0]
        contact_id = self.contact_id_map.get(item)

        if contact_id:
            # Load contact data
            contact = self.db.get_contact_by_id(contact_id)
            if contact:
                # Modify name to indicate copy
                contact['name'] = f"{contact['name']} (Copy)"
                self.set_form_data(contact)
                self.current_contact_id = None
                self.add_btn.config(state=tk.NORMAL)
                self.update_btn.config(state=tk.DISABLED)

    def view_contact_details(self):
        """View detailed contact information."""
        selected = self.contact_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to view!")
            return

        item = selected[0]
        contact_id = self.contact_id_map.get(item)

        if contact_id:
            contact = self.db.get_contact_by_id(contact_id)

            if not contact:
                messagebox.showerror("Error", "Contact not found!")
                return

            # Create details window
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Contact Details - {contact['name']}")
            details_window.geometry("400x500")
            details_window.transient(self.root)
            details_window.grab_set()

            frame = ttk.Frame(details_window, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)

            # Display contact information
            fields = [
                ("Name:", contact['name']),
                ("Phone:", contact['phone']),
                ("Email:", contact['email']),
                ("Company:", contact['company']),
                ("Address:", contact['address']),
                ("Tags:", contact['tags']),
                ("Notes:", contact['notes']),
                ("Created:", contact['created_at'][:19].replace('T', ' ') if contact['created_at'] else ''),
                ("Updated:", contact['updated_at'][:19].replace('T', ' ') if contact['updated_at'] else '')
            ]

            for i, (label, value) in enumerate(fields):
                ttk.Label(frame, text=label, font=('Arial', 10, 'bold')).grid(row=i * 2, column=0, sticky=tk.W,
                                                                              pady=(5, 0))

                if label in ["Address:", "Notes:"]:
                    text_widget = tk.Text(frame, height=3, width=40, wrap=tk.WORD, font=('Arial', 10))
                    text_widget.insert("1.0", value or "")
                    text_widget.config(state=tk.DISABLED)
                    text_widget.grid(row=i * 2 + 1, column=0, sticky=(tk.W, tk.E), pady=(2, 5))
                else:
                    value_label = ttk.Label(frame, text=value or "Not provided",
                                            foreground="gray" if not value else "black")
                    value_label.grid(row=i * 2 + 1, column=0, sticky=tk.W, pady=(2, 5))

            # Close button
            ttk.Button(frame, text="Close", command=details_window.destroy).grid(row=len(fields) * 2, column=0,
                                                                                 pady=(20, 0))

            frame.columnconfigure(0, weight=1)

    def refresh_contact_list(self):
        """Refresh the contact list display."""
        # Clear existing items and mapping
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)
        self.contact_id_map.clear()

        # Get contacts (search or all)
        search_term = self.search_var.get().strip()
        if search_term:
            contacts = self.db.search_contacts(search_term)
        else:
            contacts = self.db.get_all_contacts()

        # Add contacts to tree
        for contact in contacts:
            values = (
                contact['name'],
                contact['phone'] or '',
                contact['email'] or '',
                contact['company'] or ''
            )

            item_id = self.contact_tree.insert("", "end", values=values)
            # Store contact ID mapping
            self.contact_id_map[item_id] = contact['id']

    def on_contact_select(self, event):
        """Handle contact selection (double-click)."""
        self.edit_contact()

    def on_search_change(self, event):
        """Handle search field changes."""
        # Refresh list after a short delay to avoid too many searches
        self.root.after(300, self.search_contacts)

    def search_contacts(self):
        """Search contacts."""
        self.refresh_contact_list()

    def check_duplicate(self, contact_data):
        """Check if contact might be a duplicate."""
        name = contact_data.get('name', '').strip().lower()
        phone = contact_data.get('phone', '').strip()
        email = contact_data.get('email', '').strip().lower()

        all_contacts = self.db.get_all_contacts()

        for contact in all_contacts:
            existing_name = contact['name'].strip().lower()
            existing_phone = contact['phone'].strip()
            existing_email = contact['email'].strip().lower()

            # Check for exact name match
            if name and name == existing_name:
                return True

            # Check for phone match
            if phone and phone == existing_phone:
                return True

            # Check for email match
            if email and email == existing_email:
                return True

        return False

    def import_csv(self):
        """Import contacts from CSV file."""
        file_path = filedialog.askopenfilename(
            title="Import Contacts",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not file_path:
            return

        try:
            imported_count = 0
            skipped_count = 0

            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    # Map CSV columns to contact fields
                    contact_data = {
                        'name': row.get('name', '').strip(),
                        'phone': row.get('phone', '').strip(),
                        'email': row.get('email', '').strip(),
                        'company': row.get('company', '').strip(),
                        'address': row.get('address', '').strip(),
                        'tags': row.get('tags', '').strip(),
                        'notes': row.get('notes', '').strip()
                    }

                    # Validate
                    errors = self.validator.validate_contact(contact_data)
                    if errors:
                        skipped_count += 1
                        continue

                    # Check for duplicate
                    if self.check_duplicate(contact_data):
                        skipped_count += 1
                        continue

                    # Add contact
                    self.db.add_contact(contact_data)
                    imported_count += 1

            self.refresh_contact_list()
            self.update_statistics()

            messagebox.showinfo("Import Complete",
                                f"Imported {imported_count} contacts.\nSkipped {skipped_count} contacts (duplicates or invalid).")

        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import contacts: {str(e)}")

    def export_csv(self):
        """Export contacts to CSV file."""
        file_path = filedialog.asksaveasfilename(
            title="Export Contacts",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not file_path:
            return

        try:
            contacts = self.db.get_all_contacts()

            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['name', 'phone', 'email', 'company', 'address', 'tags', 'notes']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                for contact in contacts:
                    # Write only the specified fields
                    row = {field: contact.get(field, '') for field in fieldnames}
                    writer.writerow(row)

            messagebox.showinfo("Export Complete", f"Exported {len(contacts)} contacts to {file_path}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export contacts: {str(e)}")

    def backup_database(self):
        """Create a backup of the database."""
        file_path = filedialog.asksaveasfilename(
            title="Backup Database",
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )

        if not file_path:
            return

        try:
            self.db.backup_database(file_path)
            messagebox.showinfo("Backup Complete", f"Database backed up to {file_path}")
        except Exception as e:
            messagebox.showerror("Backup Error", f"Failed to backup database: {str(e)}")

    def show_settings(self):
        """Show settings window."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()

        frame = ttk.Frame(settings_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Database Settings", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        # Database path
        ttk.Label(frame, text=f"Database location: {self.db.db_file}").pack(anchor=tk.W, pady=5)

        # Statistics
        stats = self.db.get_statistics()
        ttk.Label(frame, text=f"Total contacts: {stats['total_contacts']}").pack(anchor=tk.W, pady=2)
        ttk.Label(frame, text=f"Contacts with phone: {stats['contacts_with_phone']}").pack(anchor=tk.W, pady=2)
        ttk.Label(frame, text=f"Contacts with email: {stats['contacts_with_email']}").pack(anchor=tk.W, pady=2)

        # Actions
        ttk.Label(frame, text="Actions", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(20, 10))

        def compact_database():
            try:
                conn = sqlite3.connect(self.db.db_file)
                conn.execute("VACUUM")
                conn.close()
                messagebox.showinfo("Success", "Database compacted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to compact database: {str(e)}")

        ttk.Button(frame, text="Compact Database", command=compact_database).pack(anchor=tk.W, pady=5)

        # Close button
        ttk.Button(frame, text="Close", command=settings_window.destroy).pack(pady=(20, 0))

    def show_context_menu(self, event):
        """Show context menu on right-click."""
        item = self.contact_tree.identify_row(event.y)
        if item:
            self.contact_tree.selection_set(item)

            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Edit", command=self.edit_contact)
            context_menu.add_command(label="Delete", command=self.delete_contact)
            context_menu.add_command(label="Duplicate", command=self.duplicate_contact)
            context_menu.add_separator()
            context_menu.add_command(label="View Details", command=self.view_contact_details)

            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()

    def update_statistics(self):
        """Update statistics display."""
        stats = self.db.get_statistics()
        stats_text = f"📊 Total: {stats['total_contacts']} | 📞 With Phone: {stats['contacts_with_phone']} | 📧 With Email: {stats['contacts_with_email']}"
        self.stats_label.config(text=stats_text)


def main():
    """Main function to run the contact manager."""
    root = tk.Tk()
    app = ContactApp(root)

    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit Contact Manager?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()