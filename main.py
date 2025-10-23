from Ear_training import Ear_training
from ui import EarTrainingGUI
import simpleaudio as sa
import tkinter as tk
from tkinter import ttk
def main():
    try:
        root = tk.Tk()
        gui = EarTrainingGUI(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("ending")
        
    finally:
        sa.stop_all()

     
if __name__=="__main__":
    main()