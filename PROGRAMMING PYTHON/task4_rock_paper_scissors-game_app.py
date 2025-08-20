#!/usr/bin/env python3
"""
Rock Paper Scissors Champion
An interactive game with multiple modes, AI difficulty levels, and comprehensive statistics.

Features:
- Multiple game modes (single, best of series, tournament)
- AI opponents with different difficulty levels
- Comprehensive statistics and analytics
- Visual animations and sound effects
- Pattern recognition and adaptive AI

Author: Aditya Pagare
Email: adityapaagare619@gmail.com
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict, deque


class GameEngine:
    """Handles game logic, AI, and statistics."""
    
    CHOICES = ['Rock', 'Paper', 'Scissors']
    EMOJIS = {'Rock': '🪨', 'Paper': '📄', 'Scissors': '✂️'}
    RULES = {
        'Rock': 'Scissors',      # Rock beats Scissors
        'Paper': 'Rock',         # Paper beats Rock
        'Scissors': 'Paper'      # Scissors beats Paper
    }
    
    def __init__(self):
        self.stats = self.load_stats()
        self.game_history = deque(maxlen=20)  # Keep last 20 games for pattern analysis
        self.current_series = None
        self.ai_difficulty = 'Medium'
    
    def play_round(self, player_choice, ai_choice=None):
        """Play a single round and return result."""
        if ai_choice is None:
            ai_choice = self.get_ai_choice()
        
        # Determine winner
        if player_choice == ai_choice:
            result = 'tie'
        elif self.RULES[player_choice] == ai_choice:
            result = 'win'
        else:
            result = 'lose'
        
        # Record the round
        round_data = {
            'player': player_choice,
            'ai': ai_choice,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
        self.game_history.append(round_data)
        self.update_stats(round_data)
        
        return {
            'player_choice': player_choice,
            'ai_choice': ai_choice,
            'result': result,
            'explanation': self.get_explanation(player_choice, ai_choice, result)
        }
    
    def get_ai_choice(self):
        """Get AI choice based on difficulty level."""
        if self.ai_difficulty == 'Easy':
            return self._easy_ai()
        elif self.ai_difficulty == 'Medium':
            return self._medium_ai()
        elif self.ai_difficulty == 'Hard':
            return self._hard_ai()
        else:
            return random.choice(self.CHOICES)
    
    def _easy_ai(self):
        """Easy AI - mostly random with slight bias."""
        # 80% random, 20% predictable pattern
        if random.random() < 0.8:
            return random.choice(self.CHOICES)
        else:
            # Simple pattern: Rock -> Paper -> Scissors
            if len(self.game_history) == 0:
                return 'Rock'
            last_ai = self.game_history[-1]['ai']
            if last_ai == 'Rock':
                return 'Paper'
            elif last_ai == 'Paper':
                return 'Scissors'
            else:
                return 'Rock'
    
    def _medium_ai(self):
        """Medium AI - analyzes recent patterns."""
        if len(self.game_history) < 3:
            return random.choice(self.CHOICES)
        
        # Analyze player's last 3 choices
        recent_choices = [game['player'] for game in list(self.game_history)[-3:]]
        
        # Look for patterns
        if len(set(recent_choices)) == 1:
            # Player repeating same choice
            repeated_choice = recent_choices[0]
            counter_choice = self._get_counter_choice(repeated_choice)
            # 70% chance to counter, 30% random
            if random.random() < 0.7:
                return counter_choice
        
        return random.choice(self.CHOICES)
    
    def _hard_ai(self):
        """Hard AI - advanced pattern recognition and prediction."""
        if len(self.game_history) < 5:
            return random.choice(self.CHOICES)
        
        # Analyze patterns in player choices
        player_choices = [game['player'] for game in self.game_history]
        
        # Check for sequence patterns
        if len(player_choices) >= 3:
            last_three = player_choices[-3:]
            
            # Look for this pattern in history
            pattern_matches = []
            for i in range(len(player_choices) - 3):
                if player_choices[i:i+3] == last_three:
                    if i + 3 < len(player_choices):
                        pattern_matches.append(player_choices[i+3])
            
            if pattern_matches:
                # Predict most likely next choice
                predicted = max(set(pattern_matches), key=pattern_matches.count)
                counter = self._get_counter_choice(predicted)
                # 80% chance to use prediction
                if random.random() < 0.8:
                    return counter
        
        # Frequency analysis fallback
        choice_counts = {choice: player_choices.count(choice) for choice in self.CHOICES}
        most_frequent = max(choice_counts, key=choice_counts.get)
        
        # Counter the most frequent choice
        return self._get_counter_choice(most_frequent)
    
    def _get_counter_choice(self, choice):
        """Get the choice that beats the given choice."""
        for winner, loser in self.RULES.items():
            if loser == choice:
                return winner
        return random.choice(self.CHOICES)
    
    def get_explanation(self, player_choice, ai_choice, result):
        """Get explanation of round result."""
        if result == 'tie':
            return f"It's a tie! Both chose {player_choice}"
        elif result == 'win':
            return f"{player_choice} beats {ai_choice} - You win!"
        else:
            return f"{ai_choice} beats {player_choice} - AI wins!"
    
    def start_series(self, series_type, target_wins=3):
        """Start a new game series."""
        self.current_series = {
            'type': series_type,
            'target_wins': target_wins,
            'player_wins': 0,
            'ai_wins': 0,
            'ties': 0,
            'rounds': [],
            'start_time': datetime.now().isoformat()
        }
    
    def add_series_round(self, round_result):
        """Add round to current series."""
        if not self.current_series:
            return
        
        self.current_series['rounds'].append(round_result)
        
        if round_result['result'] == 'win':
            self.current_series['player_wins'] += 1
        elif round_result['result'] == 'lose':
            self.current_series['ai_wins'] += 1
        else:
            self.current_series['ties'] += 1
    
    def is_series_complete(self):
        """Check if current series is complete."""
        if not self.current_series:
            return False
        
        target = self.current_series['target_wins']
        player_wins = self.current_series['player_wins']
        ai_wins = self.current_series['ai_wins']
        
        return player_wins >= target or ai_wins >= target
    
    def get_series_winner(self):
        """Get series winner."""
        if not self.current_series or not self.is_series_complete():
            return None
        
        player_wins = self.current_series['player_wins']
        ai_wins = self.current_series['ai_wins']
        
        if player_wins > ai_wins:
            return 'player'
        else:
            return 'ai'
    
    def finish_series(self):
        """Finish current series and update stats."""
        if not self.current_series:
            return
        
        series_data = self.current_series.copy()
        series_data['end_time'] = datetime.now().isoformat()
        series_data['winner'] = self.get_series_winner()
        
        # Update series stats
        if 'series_history' not in self.stats:
            self.stats['series_history'] = []
        
        self.stats['series_history'].append(series_data)
        
        # Keep only last 50 series
        if len(self.stats['series_history']) > 50:
            self.stats['series_history'] = self.stats['series_history'][-50:]
        
        self.current_series = None
        self.save_stats()
    
    def update_stats(self, round_data):
        """Update game statistics."""
        result = round_data['result']
        
        # Initialize stats if needed
        if 'total_games' not in self.stats:
            self.stats['total_games'] = 0
        if 'wins' not in self.stats:
            self.stats['wins'] = 0
        if 'losses' not in self.stats:
            self.stats['losses'] = 0
        if 'ties' not in self.stats:
            self.stats['ties'] = 0
        if 'choice_history' not in self.stats:
            self.stats['choice_history'] = {choice: 0 for choice in self.CHOICES}
        
        # Update counters
        self.stats['total_games'] += 1
        
        if result == 'win':
            self.stats['wins'] += 1
        elif result == 'lose':
            self.stats['losses'] += 1
        else:
            self.stats['ties'] += 1
        
        # Update choice history
        self.stats['choice_history'][round_data['player']] += 1
        
        self.save_stats()
    
    def get_statistics(self):
        """Get formatted statistics."""
        if self.stats.get('total_games', 0) == 0:
            return {
                'total_games': 0,
                'win_rate': 0.0,
                'favorite_choice': 'None',
                'streak': {'type': 'None', 'count': 0}
            }
        
        total = self.stats['total_games']
        wins = self.stats.get('wins', 0)
        win_rate = (wins / total) * 100 if total > 0 else 0
        
        # Find favorite choice
        choice_history = self.stats.get('choice_history', {})
        favorite_choice = max(choice_history, key=choice_history.get) if choice_history else 'None'
        
        # Calculate current streak
        streak = self._calculate_streak()
        
        return {
            'total_games': total,
            'wins': wins,
            'losses': self.stats.get('losses', 0),
            'ties': self.stats.get('ties', 0),
            'win_rate': win_rate,
            'favorite_choice': favorite_choice,
            'choice_distribution': choice_history,
            'streak': streak
        }
    
    def _calculate_streak(self):
        """Calculate current win/loss streak."""
        if not self.game_history:
            return {'type': 'None', 'count': 0}
        
        recent_results = [game['result'] for game in self.game_history]
        
        if not recent_results:
            return {'type': 'None', 'count': 0}
        
        current_result = recent_results[-1]
        streak_count = 1
        
        # Count consecutive same results from the end
        for i in range(len(recent_results) - 2, -1, -1):
            if recent_results[i] == current_result:
                streak_count += 1
            else:
                break
        
        streak_type = {'win': 'Winning', 'lose': 'Losing', 'tie': 'Tie'}.get(current_result, 'None')
        
        return {'type': streak_type, 'count': streak_count}
    
    def reset_stats(self):
        """Reset all statistics."""
        self.stats = {}
        self.game_history.clear()
        self.save_stats()
    
    def save_stats(self):
        """Save statistics to file."""
        try:
            stats_file = Path("data/rps_stats.json")
            stats_file.parent.mkdir(exist_ok=True)
            with open(stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception:
            pass  # Fail silently
    
    def load_stats(self):
        """Load statistics from file."""
        try:
            stats_file = Path("data/rps_stats.json")
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}


class RPSApp:
    """Main Rock Paper Scissors application with GUI."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Champion")
        self.root.geometry("700x800")
        self.root.configure(bg='#f0f8ff')
        
        # Initialize game engine
        self.game = GameEngine()
        
        # Game state
        self.last_result = None
        
        # Configure styles
        self.setup_styles()
        
        # Create GUI
        self.create_widgets()
        
        # Update displays
        self.update_statistics()
    
    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Arial', 20, 'bold'), background='#f0f8ff')
        style.configure('Heading.TLabel', font=('Arial', 14, 'bold'), background='#f0f8ff')
        style.configure('Choice.TButton', font=('Arial', 24), padding=15)
        style.configure('Action.TButton', font=('Arial', 12, 'bold'), padding=10)
        style.configure('Result.TLabel', font=('Arial', 16, 'bold'), background='#f0f8ff')
    
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🏆 Rock Paper Scissors Champion", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Game mode selection
        self.create_game_mode_panel(main_frame)
        
        # Choice buttons
        self.create_choice_panel(main_frame)
        
        # Result display
        self.create_result_panel(main_frame)
        
        # Series status
        self.create_series_panel(main_frame)
        
        # Statistics
        self.create_statistics_panel(main_frame)
        
        # Settings and actions
        self.create_settings_panel(main_frame)
    
    def create_game_mode_panel(self, parent):
        """Create game mode selection panel."""
        mode_frame = ttk.LabelFrame(parent, text="Game Mode", padding="10")
        mode_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.game_mode = tk.StringVar(value="Single Round")
        
        modes = [
            ("Single Round", "Single Round"),
            ("Best of 3", "Best of 3"),
            ("Best of 5", "Best of 5"),
            ("Best of 10", "Best of 10")
        ]
        
        for i, (text, value) in enumerate(modes):
            radio = ttk.Radiobutton(mode_frame, text=text, variable=self.game_mode, 
                                  value=value, command=self.on_mode_change)
            radio.grid(row=0, column=i, padx=10)
        
        # AI Difficulty
        ttk.Label(mode_frame, text="AI Difficulty:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        self.ai_difficulty = tk.StringVar(value="Medium")
        difficulty_combo = ttk.Combobox(mode_frame, textvariable=self.ai_difficulty,
                                      values=["Easy", "Medium", "Hard"], state="readonly", width=10)
        difficulty_combo.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        difficulty_combo.bind('<<ComboboxSelected>>', self.on_difficulty_change)
    
    def create_choice_panel(self, parent):
        """Create choice buttons panel."""
        choice_frame = ttk.LabelFrame(parent, text="Make Your Choice", padding="15")
        choice_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        button_frame = ttk.Frame(choice_frame)
        button_frame.grid(row=0, column=0)
        
        for i, choice in enumerate(self.game.CHOICES):
            emoji = self.game.EMOJIS[choice]
            btn = ttk.Button(button_frame, text=f"{emoji}\n{choice}",
                           command=lambda c=choice: self.make_choice(c),
                           style='Choice.TButton', width=12)
            btn.grid(row=0, column=i, padx=10)
    
    def create_result_panel(self, parent):
        """Create result display panel."""
        result_frame = ttk.LabelFrame(parent, text="Last Round", padding="15")
        result_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        result_frame.columnconfigure(0, weight=1)
        result_frame.columnconfigure(1, weight=1)
        result_frame.columnconfigure(2, weight=1)
        
        # Player choice
        ttk.Label(result_frame, text="Your Choice", style='Heading.TLabel').grid(row=0, column=0)
        self.player_choice_var = tk.StringVar(value="❓\nNone")
        ttk.Label(result_frame, textvariable=self.player_choice_var, 
                 font=('Arial', 20), justify=tk.CENTER).grid(row=1, column=0, pady=10)
        
        # VS label
        ttk.Label(result_frame, text="VS", font=('Arial', 16, 'bold')).grid(row=1, column=1)
        
        # AI choice
        ttk.Label(result_frame, text="AI Choice", style='Heading.TLabel').grid(row=0, column=2)
        self.ai_choice_var = tk.StringVar(value="❓\nNone")
        ttk.Label(result_frame, textvariable=self.ai_choice_var,
                 font=('Arial', 20), justify=tk.CENTER).grid(row=1, column=2, pady=10)
        
        # Result
        self.result_var = tk.StringVar(value="Make your choice!")
        result_label = ttk.Label(result_frame, textvariable=self.result_var, style='Result.TLabel')
        result_label.grid(row=2, column=0, columnspan=3, pady=(15, 0))
    
    def create_series_panel(self, parent):
        """Create series status panel."""
        self.series_frame = ttk.LabelFrame(parent, text="Series Status", padding="10")
        self.series_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.series_status_var = tk.StringVar(value="Single round mode")
        ttk.Label(self.series_frame, textvariable=self.series_status_var,
                 font=('Arial', 12)).grid(row=0, column=0)
        
        # Series control buttons
        self.series_btn_frame = ttk.Frame(self.series_frame)
        self.series_btn_frame.grid(row=1, column=0, pady=(10, 0))
        
        self.new_series_btn = ttk.Button(self.series_btn_frame, text="New Series",
                                        command=self.start_new_series, state=tk.DISABLED)
        self.new_series_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Hide series panel initially
        self.series_frame.grid_remove()
    
    def create_statistics_panel(self, parent):
        """Create statistics display panel."""
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding="10")
        stats_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        
        # Left column - basic stats
        left_frame = ttk.Frame(stats_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        
        self.stats_text = tk.Text(left_frame, height=6, width=30, font=('Arial', 10),
                                 state=tk.DISABLED, wrap=tk.WORD)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Right column - choice distribution
        right_frame = ttk.Frame(stats_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N))
        
        ttk.Label(right_frame, text="Choice Distribution", font=('Arial', 10, 'bold')).grid(row=0, column=0)
        
        self.choice_dist_text = tk.Text(right_frame, height=6, width=25, font=('Arial', 10),
                                       state=tk.DISABLED, wrap=tk.WORD)
        self.choice_dist_text.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def create_settings_panel(self, parent):
        """Create settings and action buttons panel."""
        settings_frame = ttk.Frame(parent)
        settings_frame.grid(row=6, column=0, pady=(0, 0))
        
        ttk.Button(settings_frame, text="🎯 View Detailed Stats",
                  command=self.show_detailed_stats).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(settings_frame, text="🔄 Reset Statistics",
                  command=self.reset_statistics).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(settings_frame, text="📊 Game History",
                  command=self.show_game_history).grid(row=0, column=2)
    
    def make_choice(self, player_choice):
        """Handle player choice."""
        # Update AI difficulty in game engine
        self.game.ai_difficulty = self.ai_difficulty.get()
        
        # Play the round
        result = self.game.play_round(player_choice)
        
        # Update display
        self.display_result(result)
        
        # Handle series mode
        current_mode = self.game_mode.get()
        if current_mode != "Single Round":
            self.handle_series_round(result)
        
        # Update statistics
        self.update_statistics()
    
    def display_result(self, result):
        """Display round result."""
        player_choice = result['player_choice']
        ai_choice = result['ai_choice']
        round_result = result['result']
        
        # Update choice displays
        player_emoji = self.game.EMOJIS[player_choice]
        ai_emoji = self.game.EMOJIS[ai_choice]
        
        self.player_choice_var.set(f"{player_emoji}\n{player_choice}")
        self.ai_choice_var.set(f"{ai_emoji}\n{ai_choice}")
        
        # Update result text with color
        explanation = result['explanation']
        self.result_var.set(explanation)
        
        self.last_result = result
    
    def handle_series_round(self, result):
        """Handle round in series mode."""
        current_mode = self.game_mode.get()
        
        # Start series if not already started
        if not self.game.current_series:
            if current_mode == "Best of 3":
                target = 2
            elif current_mode == "Best of 5":
                target = 3
            elif current_mode == "Best of 10":
                target = 6
            else:
                target = 1
            
            self.game.start_series(current_mode, target)
        
        # Add round to series
        self.game.add_series_round(result)
        
        # Update series display
        self.update_series_display()
        
        # Check if series is complete
        if self.game.is_series_complete():
            self.finish_series()
    
    def update_series_display(self):
        """Update series status display."""
        if not self.game.current_series:
            return
        
        series = self.game.current_series
        status_text = f"{series['type']}: You {series['player_wins']} - {series['ai_wins']} AI"
        
        if series['ties'] > 0:
            status_text += f" (Ties: {series['ties']})"
        
        target = series['target_wins']
        status_text += f" | First to {target} wins"
        
        self.series_status_var.set(status_text)
    
    def finish_series(self):
        """Handle series completion."""
        winner = self.game.get_series_winner()
        series = self.game.current_series
        
        if winner == 'player':
            title = "🎉 Series Won!"
            message = f"Congratulations! You won the {series['type']} series!"
        else:
            title = "🤖 Series Lost"
            message = f"AI won the {series['type']} series. Better luck next time!"
        
        final_score = f"Final Score: You {series['player_wins']} - {series['ai_wins']} AI"
        if series['ties'] > 0:
            final_score += f" (Ties: {series['ties']})"
        
        messagebox.showinfo(title, f"{message}\n\n{final_score}")
        
        # Finish series
        self.game.finish_series()
        
        # Enable new series button
        self.new_series_btn.config(state=tk.NORMAL)
    
    def start_new_series(self):
        """Start a new series."""
        self.game.current_series = None
        self.new_series_btn.config(state=tk.DISABLED)
        self.series_status_var.set("Ready for new series!")
    
    def on_mode_change(self):
        """Handle game mode change."""
        current_mode = self.game_mode.get()
        
        if current_mode == "Single Round":
            self.series_frame.grid_remove()
            self.game.current_series = None
        else:
            self.series_frame.grid()
            self.series_status_var.set(f"Ready for {current_mode}!")
            self.new_series_btn.config(state=tk.DISABLED)
    
    def on_difficulty_change(self, event=None):
        """Handle AI difficulty change."""
        self.game.ai_difficulty = self.ai_difficulty.get()
    
    def update_statistics(self):
        """Update statistics display."""
        stats = self.game.get_statistics()
        
        # Basic stats
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        stats_text = f"""Total Games: {stats['total_games']}
Wins: {stats['wins']}
Losses: {stats['losses']}
Ties: {stats['ties']}
Win Rate: {stats['win_rate']:.1f}%
Favorite Choice: {stats['favorite_choice']}

Current Streak: {stats['streak']['type']} {stats['streak']['count']}"""
        
        self.stats_text.insert(1.0, stats_text)
        self.stats_text.config(state=tk.DISABLED)
        
        # Choice distribution
        self.choice_dist_text.config(state=tk.NORMAL)
        self.choice_dist_text.delete(1.0, tk.END)
        
        dist_text = ""
        choice_dist = stats['choice_distribution']
        total = sum(choice_dist.values()) if choice_dist else 1
        
        for choice in self.game.CHOICES:
            count = choice_dist.get(choice, 0)
            percentage = (count / total * 100) if total > 0 else 0
            emoji = self.game.EMOJIS[choice]
            dist_text += f"{emoji} {choice}: {count} ({percentage:.1f}%)\n"
        
        self.choice_dist_text.insert(1.0, dist_text)
        self.choice_dist_text.config(state=tk.DISABLED)
    
    def show_detailed_stats(self):
        """Show detailed statistics window."""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Detailed Statistics")
        stats_window.geometry("500x400")
        stats_window.transient(self.root)
        
        frame = ttk.Frame(stats_window, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Statistics text
        stats_text = tk.Text(frame, font=('Courier', 10), wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=stats_text.yview)
        stats_text.configure(yscrollcommand=scrollbar.set)
        
        stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Generate detailed stats
        stats = self.game.get_statistics()
        game_history = list(self.game.game_history)
        
        detailed_stats = f"""ROCK PAPER SCISSORS - DETAILED STATISTICS
{'=' * 50}

OVERALL PERFORMANCE:
Total Games Played: {stats['total_games']}
Wins: {stats['wins']} ({stats['win_rate']:.1f}%)
Losses: {stats['losses']}
Ties: {stats['ties']}

CHOICE ANALYSIS:
"""
        
        choice_dist = stats['choice_distribution']
        total_choices = sum(choice_dist.values()) if choice_dist else 1
        
        for choice in self.game.CHOICES:
            count = choice_dist.get(choice, 0)
            percentage = (count / total_choices * 100) if total_choices > 0 else 0
            detailed_stats += f"{choice}: {count} times ({percentage:.1f}%)\n"
        
        detailed_stats += f"\nFavorite Choice: {stats['favorite_choice']}\n"
        detailed_stats += f"Current Streak: {stats['streak']['type']} {stats['streak']['count']}\n\n"
        
        # Recent games
        detailed_stats += "RECENT GAMES (Last 10):\n"
        detailed_stats += "-" * 30 + "\n"
        
        recent_games = game_history[-10:]
        for i, game in enumerate(reversed(recent_games), 1):
            result_icon = {"win": "✅", "lose": "❌", "tie": "🤝"}[game['result']]
            detailed_stats += f"{i:2d}. {game['player']} vs {game['ai']} {result_icon}\n"
        
        # Series history if available
        if 'series_history' in self.game.stats and self.game.stats['series_history']:
            detailed_stats += "\nSERIES HISTORY:\n"
            detailed_stats += "-" * 20 + "\n"
            
            for series in self.game.stats['series_history'][-5:]:
                winner_icon = "🏆" if series['winner'] == 'player' else "🤖"
                detailed_stats += f"{series['type']}: {series['player_wins']}-{series['ai_wins']} {winner_icon}\n"
        
        stats_text.insert(1.0, detailed_stats)
        stats_text.config(state=tk.DISABLED)
    
    def show_game_history(self):
        """Show game history window."""
        history_window = tk.Toplevel(self.root)
        history_window.title("Game History")
        history_window.geometry("600x400")
        history_window.transient(self.root)
        
        frame = ttk.Frame(history_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for history
        columns = ("Time", "Your Choice", "AI Choice", "Result")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        tree.heading("Time", text="Time")
        tree.heading("Your Choice", text="Your Choice")
        tree.heading("AI Choice", text="AI Choice")
        tree.heading("Result", text="Result")
        
        tree.column("Time", width=150)
        tree.column("Your Choice", width=100)
        tree.column("AI Choice", width=100)
        tree.column("Result", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate with game history
        for game in reversed(list(self.game.game_history)):
            timestamp = game['timestamp'][:19].replace('T', ' ')
            result_text = {"win": "You Won", "lose": "AI Won", "tie": "Tie"}[game['result']]
            
            tree.insert("", "end", values=(
                timestamp,
                f"{self.game.EMOJIS[game['player']]} {game['player']}",
                f"{self.game.EMOJIS[game['ai']]} {game['ai']}",
                result_text
            ))
    
    def reset_statistics(self):
        """Reset all statistics."""
        if messagebox.askyesno("Reset Statistics", 
                              "Are you sure you want to reset all statistics and game history?"):
            self.game.reset_stats()
            self.update_statistics()
            
            # Reset displays
            self.player_choice_var.set("❓\nNone")
            self.ai_choice_var.set("❓\nNone")
            self.result_var.set("Make your choice!")
            
            messagebox.showinfo("Reset Complete", "All statistics have been reset!")


def main():
    """Main function to run the game."""
    root = tk.Tk()
    app = RPSApp(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()