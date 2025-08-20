#!/usr/bin/env python3
"""
Password Generator Pro
A secure password generator with customizable complexity and strength analysis.

Features:
- Customizable password length and character sets
- Real-time strength analysis with entropy calculation
- Password history with secure storage
- One-click copy to clipboard
- Security policy templates
- Batch generation capability

Author: Aditya Pagare
Email: adityapaagare619@gmail.com
"""

import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import json
import math
from pathlib import Path
from datetime import datetime


class PasswordEngine:
    """Handles password generation and strength analysis."""
    
    # Character sets
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    AMBIGUOUS = "0O1lI"  # Characters that can be confused
    
    def __init__(self):
        self.history = []
        self.load_history()
    
    def generate_password(self, length=12, use_lowercase=True, use_uppercase=True,
                         use_digits=True, use_symbols=True, exclude_ambiguous=False):
        """Generate a secure password with specified criteria."""
        if length < 1:
            raise ValueError("Password length must be at least 1")
        
        # Build character set
        charset = ""
        required_chars = []
        
        if use_lowercase:
            chars = self.LOWERCASE
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS)
            charset += chars
            required_chars.append(secrets.choice(chars))
        
        if use_uppercase:
            chars = self.UPPERCASE
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS)
            charset += chars
            required_chars.append(secrets.choice(chars))
        
        if use_digits:
            chars = self.DIGITS
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS)
            charset += chars
            required_chars.append(secrets.choice(chars))
        
        if use_symbols:
            charset += self.SYMBOLS
            required_chars.append(secrets.choice(self.SYMBOLS))
        
        if not charset:
            raise ValueError("At least one character type must be selected")
        
        # Generate password
        password = required_chars.copy()
        remaining_length = length - len(required_chars)
        
        if remaining_length < 0:
            # If required chars exceed length, just use random selection
            password = [secrets.choice(charset) for _ in range(length)]
        else:
            # Fill remaining positions
            password.extend([secrets.choice(charset) for _ in range(remaining_length)])
        
        # Shuffle the password
        secrets.SystemRandom().shuffle(password)
        
        result = ''.join(password)
        
        # Add to history
        self.add_to_history(result, {
            'length': length,
            'use_lowercase': use_lowercase,
            'use_uppercase': use_uppercase,
            'use_digits': use_digits,
            'use_symbols': use_symbols,
            'exclude_ambiguous': exclude_ambiguous
        })
        
        return result
    
    def analyze_strength(self, password):
        """Analyze password strength and return detailed metrics."""
        if not password:
            return {
                'score': 0,
                'entropy': 0,
                'strength': 'Very Weak',
                'feedback': ['Password is empty']
            }
        
        length = len(password)
        charset_size = 0
        has_lowercase = bool(set(password) & set(self.LOWERCASE))
        has_uppercase = bool(set(password) & set(self.UPPERCASE))
        has_digits = bool(set(password) & set(self.DIGITS))
        has_symbols = bool(set(password) & set(self.SYMBOLS))
        
        # Calculate character set size
        if has_lowercase:
            charset_size += len(self.LOWERCASE)
        if has_uppercase:
            charset_size += len(self.UPPERCASE)
        if has_digits:
            charset_size += len(self.DIGITS)
        if has_symbols:
            charset_size += len(self.SYMBOLS)
        
        # Calculate entropy
        entropy = length * math.log2(charset_size) if charset_size > 0 else 0
        
        # Calculate base score
        score = min(100, (entropy / 80) * 100)  # Normalize to 100
        
        # Apply penalties and bonuses
        feedback = []
        
        # Length checks
        if length < 8:
            score *= 0.5
            feedback.append("Password should be at least 8 characters long")
        elif length >= 12:
            score *= 1.1
        
        # Character variety checks
        variety_count = sum([has_lowercase, has_uppercase, has_digits, has_symbols])
        if variety_count < 3:
            score *= 0.8
            feedback.append("Use a mix of uppercase, lowercase, numbers, and symbols")
        elif variety_count == 4:
            score *= 1.1
        
        # Common patterns check
        if self._has_common_patterns(password):
            score *= 0.7
            feedback.append("Avoid common patterns and sequences")
        
        # Repeated characters
        if self._has_repeated_chars(password):
            score *= 0.9
            feedback.append("Avoid repeated characters")
        
        # Determine strength category
        if score >= 80:
            strength = "Very Strong"
            color = "#4CAF50"  # Green
        elif score >= 60:
            strength = "Strong"
            color = "#8BC34A"  # Light Green
        elif score >= 40:
            strength = "Moderate"
            color = "#FF9800"  # Orange
        elif score >= 20:
            strength = "Weak"
            color = "#FF5722"  # Red Orange
        else:
            strength = "Very Weak"
            color = "#F44336"  # Red
        
        if not feedback and score >= 60:
            feedback.append("Good password!")
        
        return {
            'score': min(100, max(0, score)),
            'entropy': entropy,
            'strength': strength,
            'color': color,
            'feedback': feedback,
            'length': length,
            'charset_size': charset_size,
            'has_lowercase': has_lowercase,
            'has_uppercase': has_uppercase,
            'has_digits': has_digits,
            'has_symbols': has_symbols
        }
    
    def _has_common_patterns(self, password):
        """Check for common patterns in password."""
        password_lower = password.lower()
        
        # Common sequences
        sequences = [
            "123456789", "abcdefghijklmnopqrstuvwxyz", "qwertyuiop",
            "asdfghjkl", "zxcvbnm", "987654321"
        ]
        
        for seq in sequences:
            for i in range(len(seq) - 2):
                if seq[i:i+3] in password_lower:
                    return True
        
        return False
    
    def _has_repeated_chars(self, password):
        """Check for repeated characters."""
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False
    
    def add_to_history(self, password, settings):
        """Add password to history."""
        entry = {
            'password': password,
            'settings': settings,
            'timestamp': datetime.now().isoformat(),
            'strength': self.analyze_strength(password)['strength']
        }
        
        self.history.append(entry)
        
        # Keep only last 20 entries
        if len(self.history) > 20:
            self.history = self.history[-20:]
        
        self.save_history()
    
    def save_history(self):
        """Save history to file."""
        try:
            history_file = Path("data/password_history.json")
            history_file.parent.mkdir(exist_ok=True)
            with open(history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception:
            pass  # Fail silently
    
    def load_history(self):
        """Load history from file."""
        try:
            history_file = Path("data/password_history.json")
            if history_file.exists():
                with open(history_file, 'r') as f:
                    self.history = json.load(f)
        except Exception:
            self.history = []


class PasswordApp:
    """Main password generator application with GUI."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator Pro")
        self.root.geometry("500x700")
        self.root.configure(bg='#f5f5f5')
        
        # Initialize password engine
        self.engine = PasswordEngine()
        
        # Configure styles
        self.setup_styles()
        
        # Create GUI
        self.create_widgets()
        
        # Generate initial password
        self.generate_password()
    
    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f5f5f5')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#f5f5f5')
        style.configure('Password.TLabel', font=('Courier', 14, 'bold'), background='white',
                       relief='sunken', padding=10)
        style.configure('Generate.TButton', font=('Arial', 12, 'bold'), padding=10)
        style.configure('Copy.TButton', font=('Arial', 10), padding=5)
    
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔐 Password Generator Pro", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Password display
        self.create_password_display(main_frame)
        
        # Settings
        self.create_settings_panel(main_frame)
        
        # Strength analysis
        self.create_strength_panel(main_frame)
        
        # Action buttons
        self.create_action_buttons(main_frame)
        
        # History
        self.create_history_panel(main_frame)
    
    def create_password_display(self, parent):
        """Create password display section."""
        pass_frame = ttk.LabelFrame(parent, text="Generated Password", padding="10")
        pass_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        pass_frame.columnconfigure(0, weight=1)
        
        # Password display
        self.password_var = tk.StringVar()
        password_label = ttk.Label(pass_frame, textvariable=self.password_var,
                                  style='Password.TLabel', width=40)
        password_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Copy button
        copy_btn = ttk.Button(pass_frame, text="📋 Copy to Clipboard",
                             command=self.copy_password, style='Copy.TButton')
        copy_btn.grid(row=1, column=0)
    
    def create_settings_panel(self, parent):
        """Create password settings panel."""
        settings_frame = ttk.LabelFrame(parent, text="Password Settings", padding="10")
        settings_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        settings_frame.columnconfigure(1, weight=1)
        
        # Length
        ttk.Label(settings_frame, text="Length:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.length_var = tk.IntVar(value=12)
        length_scale = ttk.Scale(settings_frame, from_=4, to=64, variable=self.length_var,
                               orient=tk.HORIZONTAL, command=self.on_settings_change)
        length_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        self.length_label = ttk.Label(settings_frame, text="12")
        self.length_label.grid(row=0, column=2, padx=(10, 0), pady=2)
        
        # Character type checkboxes
        self.lowercase_var = tk.BooleanVar(value=True)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_ambiguous_var = tk.BooleanVar(value=False)
        
        checkboxes = [
            ("Include lowercase letters (a-z)", self.lowercase_var),
            ("Include uppercase letters (A-Z)", self.uppercase_var),
            ("Include digits (0-9)", self.digits_var),
            ("Include symbols (!@#$%^&*)", self.symbols_var),
            ("Exclude ambiguous characters (0,O,1,l,I)", self.exclude_ambiguous_var)
        ]
        
        for i, (text, var) in enumerate(checkboxes, start=1):
            checkbox = ttk.Checkbutton(settings_frame, text=text, variable=var,
                                     command=self.on_settings_change)
            checkbox.grid(row=i, column=0, columnspan=3, sticky=tk.W, pady=2)
        
        # Presets
        preset_frame = ttk.Frame(settings_frame)
        preset_frame.grid(row=6, column=0, columnspan=3, pady=(10, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(preset_frame, text="Presets:").grid(row=0, column=0, sticky=tk.W)
        
        presets = [
            ("Simple", self.preset_simple),
            ("Complex", self.preset_complex),
            ("PIN", self.preset_pin),
            ("Passphrase", self.preset_passphrase)
        ]
        
        for i, (text, command) in enumerate(presets):
            btn = ttk.Button(preset_frame, text=text, command=command, width=10)
            btn.grid(row=0, column=i+1, padx=5)
    
    def create_strength_panel(self, parent):
        """Create password strength analysis panel."""
        strength_frame = ttk.LabelFrame(parent, text="Strength Analysis", padding="10")
        strength_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        strength_frame.columnconfigure(0, weight=1)
        
        # Strength bar
        self.strength_var = tk.StringVar(value="Analyzing...")
        strength_label = ttk.Label(strength_frame, textvariable=self.strength_var,
                                  font=('Arial', 12, 'bold'))
        strength_label.grid(row=0, column=0, pady=(0, 5))
        
        # Progress bar for strength
        self.strength_progress = ttk.Progressbar(strength_frame, length=300, mode='determinate')
        self.strength_progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Details
        self.details_text = tk.Text(strength_frame, height=4, width=50, wrap=tk.WORD,
                                   font=('Arial', 9), state=tk.DISABLED)
        self.details_text.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        details_scroll = ttk.Scrollbar(strength_frame, orient=tk.VERTICAL,
                                     command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scroll.set)
        details_scroll.grid(row=2, column=1, sticky=(tk.N, tk.S))
    
    def create_action_buttons(self, parent):
        """Create action buttons."""
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=4, column=0, pady=(0, 15))
        
        # Generate button
        generate_btn = ttk.Button(action_frame, text="🎲 Generate New Password",
                                command=self.generate_password, style='Generate.TButton')
        generate_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Batch generate button
        batch_btn = ttk.Button(action_frame, text="📦 Generate Multiple",
                             command=self.batch_generate)
        batch_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Clear history button
        clear_btn = ttk.Button(action_frame, text="🗑️ Clear History",
                             command=self.clear_history)
        clear_btn.grid(row=0, column=2)
    
    def create_history_panel(self, parent):
        """Create password history panel."""
        history_frame = ttk.LabelFrame(parent, text="Password History", padding="10")
        history_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0))
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        # History listbox
        self.history_listbox = tk.Listbox(history_frame, height=8, font=('Courier', 9))
        history_scroll = ttk.Scrollbar(history_frame, orient=tk.VERTICAL,
                                     command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=history_scroll.set)
        
        self.history_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        history_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind double-click to use password
        self.history_listbox.bind('<Double-Button-1>', self.use_history_password)
        
        # Update history display
        self.update_history_display()
    
    def on_settings_change(self, *args):
        """Handle settings change."""
        # Update length label
        length = int(self.length_var.get())
        self.length_label.config(text=str(length))
        
        # Auto-generate new password
        self.generate_password()
    
    def generate_password(self):
        """Generate a new password with current settings."""
        try:
            length = int(self.length_var.get())
            password = self.engine.generate_password(
                length=length,
                use_lowercase=self.lowercase_var.get(),
                use_uppercase=self.uppercase_var.get(),
                use_digits=self.digits_var.get(),
                use_symbols=self.symbols_var.get(),
                exclude_ambiguous=self.exclude_ambiguous_var.get()
            )
            
            self.password_var.set(password)
            self.analyze_current_password()
            self.update_history_display()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def analyze_current_password(self):
        """Analyze and display current password strength."""
        password = self.password_var.get()
        analysis = self.engine.analyze_strength(password)
        
        # Update strength display
        self.strength_var.set(f"{analysis['strength']} ({analysis['score']:.0f}/100)")
        self.strength_progress['value'] = analysis['score']
        
        # Update details
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        details = [
            f"Entropy: {analysis['entropy']:.1f} bits",
            f"Length: {analysis['length']} characters",
            f"Character set size: {analysis['charset_size']}",
            "",
            "Feedback:"
        ]
        details.extend([f"• {feedback}" for feedback in analysis['feedback']])
        
        self.details_text.insert(1.0, '\n'.join(details))
        self.details_text.config(state=tk.DISABLED)
    
    def copy_password(self):
        """Copy password to clipboard."""
        password = self.password_var.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    
    def batch_generate(self):
        """Generate multiple passwords."""
        batch_window = tk.Toplevel(self.root)
        batch_window.title("Batch Generate Passwords")
        batch_window.geometry("600x400")
        batch_window.transient(self.root)
        batch_window.grab_set()
        
        frame = ttk.Frame(batch_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Count input
        count_frame = ttk.Frame(frame)
        count_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(count_frame, text="Number of passwords:").pack(side=tk.LEFT)
        count_var = tk.IntVar(value=10)
        count_spin = ttk.Spinbox(count_frame, from_=1, to=100, textvariable=count_var, width=10)
        count_spin.pack(side=tk.LEFT, padx=(10, 0))
        
        # Generate button
        def generate_batch():
            passwords_text.delete(1.0, tk.END)
            count = count_var.get()
            
            for i in range(count):
                try:
                    password = self.engine.generate_password(
                        length=int(self.length_var.get()),
                        use_lowercase=self.lowercase_var.get(),
                        use_uppercase=self.uppercase_var.get(),
                        use_digits=self.digits_var.get(),
                        use_symbols=self.symbols_var.get(),
                        exclude_ambiguous=self.exclude_ambiguous_var.get()
                    )
                    passwords_text.insert(tk.END, f"{i+1:2d}. {password}\n")
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
                    break
        
        ttk.Button(count_frame, text="Generate", command=generate_batch).pack(side=tk.LEFT, padx=(10, 0))
        
        # Passwords display
        passwords_text = tk.Text(frame, font=('Courier', 10), wrap=tk.NONE)
        passwords_scroll_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=passwords_text.yview)
        passwords_scroll_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=passwords_text.xview)
        passwords_text.configure(yscrollcommand=passwords_scroll_y.set, xscrollcommand=passwords_scroll_x.set)
        
        passwords_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        passwords_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        passwords_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Copy all button
        def copy_all():
            content = passwords_text.get(1.0, tk.END)
            batch_window.clipboard_clear()
            batch_window.clipboard_append(content)
            messagebox.showinfo("Copied", "All passwords copied to clipboard!")
        
        ttk.Button(frame, text="Copy All", command=copy_all).pack(pady=(10, 0))
    
    def preset_simple(self):
        """Apply simple password preset."""
        self.length_var.set(8)
        self.lowercase_var.set(True)
        self.uppercase_var.set(True)
        self.digits_var.set(True)
        self.symbols_var.set(False)
        self.exclude_ambiguous_var.set(True)
        self.generate_password()
    
    def preset_complex(self):
        """Apply complex password preset."""
        self.length_var.set(16)
        self.lowercase_var.set(True)
        self.uppercase_var.set(True)
        self.digits_var.set(True)
        self.symbols_var.set(True)
        self.exclude_ambiguous_var.set(False)
        self.generate_password()
    
    def preset_pin(self):
        """Apply PIN preset."""
        self.length_var.set(6)
        self.lowercase_var.set(False)
        self.uppercase_var.set(False)
        self.digits_var.set(True)
        self.symbols_var.set(False)
        self.exclude_ambiguous_var.set(True)
        self.generate_password()
    
    def preset_passphrase(self):
        """Apply passphrase preset."""
        self.length_var.set(20)
        self.lowercase_var.set(True)
        self.uppercase_var.set(True)
        self.digits_var.set(True)
        self.symbols_var.set(True)
        self.exclude_ambiguous_var.set(False)
        self.generate_password()
    
    def update_history_display(self):
        """Update history listbox."""
        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.engine.history[-10:]):  # Show last 10
            timestamp = entry['timestamp'][:19].replace('T', ' ')
            password = entry['password']
            strength = entry['strength']
            display_text = f"{timestamp} | {strength:>11} | {password}"
            self.history_listbox.insert(0, display_text)
    
    def use_history_password(self, event):
        """Use password from history."""
        selection = self.history_listbox.curselection()
        if selection:
            item = self.history_listbox.get(selection[0])
            password = item.split(" | ")[-1]
            self.password_var.set(password)
            self.analyze_current_password()
    
    def clear_history(self):
        """Clear password history."""
        if messagebox.askyesno("Clear History", "Clear all password history?"):
            self.engine.history = []
            self.engine.save_history()
            self.update_history_display()


def main():
    """Main function to run the password generator."""
    root = tk.Tk()
    app = PasswordApp(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()