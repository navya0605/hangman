
import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import platform

def start_game():
    category = category_combobox.get()
    level = level_combobox.get()

    script_map = {
        ('animals', 'easy'): 'animal_easy.py',
        ('animals', 'medium'): 'animal_medium.py',
        ('animals', 'tough'): 'animal_tough.py',
        ('birds', 'easy'): 'bird_easy.py',
        ('birds', 'medium'): 'bird_medium.py',
        ('birds', 'tough'): 'bird_tough.py',
        ('countries', 'easy'): 'country_easy.py',
        ('countries', 'medium'): 'country_medium.py',
        ('countries', 'tough'): 'country_tough.py',
        ('languages', 'easy'): 'language_easy.py',
        ('languages', 'medium'): 'language_medium.py',
        ('languages', 'tough'): 'language_tough.py',
        ('flowers', 'easy'): 'flowers_easy.py',
        ('flowers', 'medium'): 'flowers_medium.py',
        ('flowers', 'tough'): 'flowers_tough.py',
        ('professions', 'easy'): 'prof_easy.py',
        ('professions', 'medium'): 'prof_medium.py',
        ('professions', 'tough'): 'prof_tough.py',
        ('IELTS/TOEFL', 'easy'): 'word_easy.py',
        ('IELTS/TOEFL', 'medium'): 'word_medium.py',
        ('IELTS/TOEFL', 'tough'): 'word_tough.py'
    }

    script = script_map.get((category, level))
    if script:
        python_executable = sys.executable  # Get full path to Python interpreter
        subprocess.Popen([python_executable, script])  # Use full path in Popen call
        output_label.config(text=f"Starting {category} game at {level} level. Please check the game window.")
    else:
        output_label.config(text="Invalid category or level selected")

def quit_game():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("The Hangman Game")

# Change background color to beige
root.configure(bg='#f5f5dc')

# Maximize window
root.state('zoomed')

# Create a custom style for comboboxes
s = ttk.Style()
s.configure('TCombobox', font=('Arial', 20))

# Create frame to hold widgets
frame = ttk.Frame(root, padding=50)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create heading
heading_label = ttk.Label(frame, text="The Hangman Game", font=('Arial', 36, 'bold'))
heading_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

# Create subtitle
subtitle_label = ttk.Label(frame, text="Guess the word or get ready to hang", font=('Arial', 16))
subtitle_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Create category selection
category_label = ttk.Label(frame, text="Category:", font=('Arial', 24))
category_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

categories = ['animals', 'birds', 'countries', 'languages', 'flowers', 'professions', 'IELTS/TOEFL']
category_combobox = ttk.Combobox(frame, values=categories, width=30, style='TCombobox')
category_combobox.grid(row=2, column=1, padx=10, pady=5)

# Create level selection
level_label = ttk.Label(frame, text="Level:", font=('Arial', 24))
level_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

levels = ['easy', 'medium', 'tough']
level_combobox = ttk.Combobox(frame, values=levels, width=30, style='TCombobox')
level_combobox.grid(row=3, column=1, padx=10, pady=5)

# Button to start the game
start_button = ttk.Button(frame, text="Start Game", command=start_game, width=30)
start_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)
start_button.configure(style='TButton')

# Quit button
quit_button = ttk.Button(frame, text="Quit", command=quit_game, width=30)
quit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20)
quit_button.configure(style='TButton')

# Label to display output
output_label = ttk.Label(frame, text="", font=('Arial', 24))
output_label.grid(row=6, column=0, columnspan=2, pady=5)

# Create custom style for buttons
s.configure('TButton', font=('Arial', 24))

# Run the main event loop
root.mainloop()
