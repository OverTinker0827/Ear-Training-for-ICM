import tkinter as tk
from tkinter import ttk
import threading
import random
import simpleaudio as sa
from Ear_training import Ear_training
import time

class EarTrainingGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Ear Training GUI")
        self.node = Ear_training()
        self.running = False
        self.current_quiz = []

        # --- Controls ---
        control_frame = tk.Frame(master)
        control_frame.pack(pady=10)
        self.replay_btn = tk.Button(master, text="Replay", command=self.replay_quiz)
        self.replay_btn.pack(pady=5)

        # Scale selection
        tk.Label(control_frame, text="Scale:").grid(row=0, column=0)
        self.scale_var = tk.StringVar(value="D")
        self.scale_box = ttk.Combobox(control_frame, textvariable=self.scale_var, values=self.node.n)
        self.scale_box.grid(row=0, column=1)

        # Speed slider (limit 200)
        tk.Label(control_frame, text="Speed (%):").grid(row=1, column=0)
        self.speed_var = tk.IntVar(value=100)
        self.speed_slider = tk.Scale(control_frame, from_=50, to=200, orient=tk.HORIZONTAL, variable=self.speed_var)
        self.speed_slider.grid(row=1, column=1)

        # Notes per check slider
        tk.Label(control_frame, text="Notes per check:").grid(row=2, column=0)
        self.npc_var = tk.IntVar(value=1)
        self.npc_slider = tk.Scale(control_frame, from_=1, to=12, orient=tk.HORIZONTAL, variable=self.npc_var)
        self.npc_slider.grid(row=2, column=1)

        # Allowed notes checkboxes
        tk.Label(control_frame, text="Allowed Notes:").grid(row=3, column=0, sticky="n")
        self.allowed_frame = tk.Frame(control_frame)
        self.allowed_frame.grid(row=3, column=1)
        self.allowed_vars = {}
        for note in self.node.sargam:
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self.allowed_frame, text=note, variable=var)
            cb.pack(side=tk.LEFT)
            self.allowed_vars[note] = var

        # Start / Stop buttons
        self.start_btn = tk.Button(control_frame, text="Start", command=self.start_quiz)
        self.start_btn.grid(row=4, column=0, pady=5)
        self.stop_btn = tk.Button(control_frame, text="Stop", command=self.stop_quiz)
        self.stop_btn.grid(row=4, column=1, pady=5)

        # --- Quiz area ---
        self.quiz_frame = tk.Frame(master)
        self.quiz_frame.pack(pady=10)

        tk.Label(self.quiz_frame, text="Click the notes in order:").pack()
        self.user_selected_frame = tk.Frame(self.quiz_frame)
        self.user_selected_frame.pack(pady=5)
        self.user_selected_labels = []

        # Frame for answer buttons
        self.answer_buttons_frame = tk.Frame(self.quiz_frame)
        self.answer_buttons_frame.pack()
        self.answer_buttons = {}

        # Submit button
        self.submit_btn = tk.Button(master, text="Submit", command=self.submit_answers)
        self.submit_btn.pack(pady=5)

        # Backspace button
        self.backspace_btn = tk.Button(master, text="Backspace", command=self.backspace)
        self.backspace_btn.pack(pady=5)

        # Result label
        self.result_label = tk.Label(master, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.user_answers = []
        self.awaiting_submission = False
    def replay_quiz(self):
        if not self.running or not self.current_quiz:
            return
        scale = self.scale_var.get()
        dur = 0.5
        speed = min(self.speed_var.get(), 200)
        for note in self.current_quiz:
            freq = self.node.sargam_to_note(scale, note)
            self.node.play_note(freq, dur)
            time.sleep(10/speed)

    def start_quiz(self):
        if self.running:
            return
        self.running = True
        self.scale_box.config(state="disabled")  # lock scale
        self.user_answers = []
        self.result_label.config(text="")
        self.thread = threading.Thread(target=self.quiz_loop, daemon=True)
        self.thread.start()

    def stop_quiz(self):
        self.running = False
        sa.stop_all()
        self.scale_box.config(state="normal")  # unlock scale
        self.result_label.config(text="Quiz stopped.")
        self.clear_user_selection()

    def backspace(self):
        if self.user_answers:
            self.user_answers.pop()
            label = self.user_selected_labels.pop()
            label.destroy()

    def note_click(self, note):
        if not self.running :
            return
        self.user_answers.append(note)
        lbl = tk.Label(self.user_selected_frame, text=note, borderwidth=1, relief="solid", padx=5)
        lbl.pack(side=tk.LEFT, padx=2)
        self.user_selected_labels.append(lbl)

    def submit_answers(self):
        if not self.running or not self.awaiting_submission:
            return
        if self.user_answers == self.current_quiz:
            self.result_label.config(text="Correct!")
        else:
            self.result_label.config(text="Incorrect! It was : " + " ".join(self.current_quiz))
        self.awaiting_submission = False
        self.user_answers = []
        self.clear_user_selection()
        time.sleep(0.5)  # short pause before next round

    def clear_user_selection(self):
        for lbl in self.user_selected_labels:
            lbl.destroy()
        self.user_selected_labels = []

    def update_answer_buttons(self, allowed_notes):
        # Destroy previous buttons
        for btn in self.answer_buttons.values():
            btn.destroy()
        self.answer_buttons = {}
        # Create new buttons for allowed notes only
        for note in allowed_notes:
            btn = tk.Button(self.answer_buttons_frame, text=note, command=lambda n=note: self.note_click(n))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.answer_buttons[note] = btn

    def quiz_loop(self):
        # Play tanpura
        scale = self.scale_var.get()
        self.node.play_tanpura(scale)
        time.sleep(1)

        while self.running:
            allowed_notes = [note for note, var in self.allowed_vars.items() if var.get()]
            if not allowed_notes:
                self.result_label.config(text="Select at least one allowed note!")
                break
            self.update_answer_buttons(allowed_notes)
            notes_per_check = self.npc_var.get()
            self.current_quiz = random.choices(allowed_notes, k=notes_per_check)
            dur = 0.5
            speed = self.speed_var.get()
            time.sleep(1)
       
            for note in self.current_quiz:
                freq = self.node.sargam_to_note(scale, note)
                self.node.play_note(freq, dur)
                time.sleep(1/speed)
           
            self.awaiting_submission = True
            while self.awaiting_submission and self.running:
                time.sleep(0.1)



