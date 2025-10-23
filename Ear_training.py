import simpleaudio as sa
import time
import random
import numpy as np

class Ear_training:

    def __init__(self,octave=3):
        

        self.notes={
            "C":130.81,
            "C#":138.59,
            "D":146.83,
            "D#":155.56,
            "E":164.81,
            "F":174.61,
            "F#":185,
            "G":196,
            "G#":207.65,
            "A":220,
            "A#":233.08,
            "B":246.94,
            "Ċ": 261.63,
            "Ċ#": 277.18,
            "Ḋ": 293.66,
            "Ḋ#": 311.13,
            "Ė": 329.63,
            "Ḟ": 349.23,
            "Ḟ#": 369.99,
            "Ġ": 392.00,
            "Ġ#": 415.30,
            "Ȧ": 440.00,
            "Ȧ#": 466.16,
            "Ḃ": 493.88
        }

        self.sargam=["S","Rk","R","Gk","G","M","Mt","P","Dk","D","Nk","N","Ṡ"]
        self.n=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B","Ċ", "Ċ#", "Ḋ", "Ḋ#", "Ė", "Ḟ", "Ḟ#", "Ġ", "Ġ#", "Ȧ", "Ȧ#", "Ḃ"]
        self.octave=octave
    def sargam_to_note(self,scale,note):
        print(note)
        idx=self.sargam.index(note)
        pos=self.n.index(scale)
        n_pos=pos+idx
        print(self.n[n_pos])
        return self.notes[self.n[n_pos]]*(self.octave-2)

    def play_note(self,frequency,duration,sample_rate=44100,volume=0.7):

        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(frequency * t * 2 * np.pi)
        audio = (wave * 32767 * volume).astype(np.int16)
        play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
        play_obj.wait_done() 


    def play_tanpura(self,scale):
        sa.stop_all()
        wave_obj = sa.WaveObject.from_wave_file(f"tanpura/{scale}.wav")  
        play_obj = wave_obj.play()  

    def start(self,scale,dur,allowed_notes,speed,notes_per_check):
        # scale="D"
        # dur=0.5
        # allowed_notes=["S","G","P","N","Ṡ"]
        # notes_per_check=5
        self.play_tanpura(scale)
        time.sleep(3)
        speed=100
        while True:
            notes=random.choices(allowed_notes,k=notes_per_check)
            for note in notes:
                freq=self.sargam_to_note(scale,note)
                self.play_note(freq,dur)
                time.sleep(10/speed)
            answers=list(input().split())
            if answers==notes:
                print("correct answer")
            else:
                print("incorrect, it was "+ " ".join(notes))
            time.sleep(1)


def main():
    node=Ear_training()
    try:
        node.start(scale="D",dur=0.5,allowed_notes=["S","G","P","N","Ṡ"],speed=100,notes_per_check=5)
    except KeyboardInterrupt:
        print("ending")
    finally:
        sa.stop_all()


        
  


if __name__=="__main__":
    main()