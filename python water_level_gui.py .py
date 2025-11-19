import tkinter as tk
from PIL import Image, ImageTk
import pygame

# Initialize sound system
pygame.mixer.init()
BUZZER_SOUND = "493163__breviceps__buzzer-sounds-wrong-answer-error.wav"

class WaterLevelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arduino Water Level Controller MADESH")
        self.root.geometry("1000x600")
        self.root.config(bg="#27C78F")  # Sky blue background 🌤️

        self.create_canvas()
        self.load_images()
        self.place_components()
        self.draw_connections()
        self.add_controls()

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=1000, height=500, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(pady=20)

    def load_images(self):
        # Load and resize all images to suitable dimensions
        self.arduino_img = Image.open("arduino.png").resize((220, 150))
        self.sensor_img = Image.open("sensor.png").resize((130, 90))
        self.buzzer_img = Image.open("buzzer.png").resize((120, 80))
        self.tank_img = Image.open("tank.png").resize((180, 180))

        # Convert them to Tkinter-compatible images
        self.arduino_photo = ImageTk.PhotoImage(self.arduino_img)
        self.sensor_photo = ImageTk.PhotoImage(self.sensor_img)
        self.buzzer_photo = ImageTk.PhotoImage(self.buzzer_img)
        self.tank_photo = ImageTk.PhotoImage(self.tank_img)

    def place_components(self):
        # Place each image in specific coordinates
        self.canvas.create_image(150, 250, image=self.arduino_photo, anchor="center")  # Arduino
        self.canvas.create_image(400, 200, image=self.sensor_photo, anchor="center")   # Sensor
        self.canvas.create_image(700, 250, image=self.buzzer_photo, anchor="center")   # Buzzer
        self.canvas.create_image(900, 320, image=self.tank_photo, anchor="center")     # Water tank

        # Add labels below each image
        self.canvas.create_text(150, 380, text="Arduino UNO", font=("Arial", 12, "bold"))
        self.canvas.create_text(400, 320, text="Ultrasonic Sensor", font=("Arial", 12, "bold"))
        self.canvas.create_text(700, 380, text="Buzzer", font=("Arial", 12, "bold"))
        self.canvas.create_text(900, 440, text="Water Tank", font=("Arial", 12, "bold"))

    def draw_connections(self):
        # ---- Arduino to Sensor connections ----
        # VCC (Red)
        self.canvas.create_line(250, 230, 330, 180, width=3, fill="red")
        self.canvas.create_text(290, 160, text="VCC", fill="red", font=("Arial", 10, "bold"))

        # GND (Black)
        self.canvas.create_line(250, 260, 330, 210, width=3, fill="black")
        self.canvas.create_text(290, 200, text="GND", fill="black", font=("Arial", 10, "bold"))

        # TRIG (Yellow)
        self.canvas.create_line(250, 270, 330, 220, width=3, fill="yellow")
        self.canvas.create_text(290, 220, text="TRIG", fill="orange", font=("Arial", 10, "bold"))

        # ECHO (Green)
        self.canvas.create_line(250, 290, 330, 240, width=3, fill="green")
        self.canvas.create_text(290, 240, text="ECHO", fill="green", font=("Arial", 10, "bold"))

        # ---- Arduino to Buzzer ----
        self.canvas.create_line(250, 250, 640, 250, width=3, fill="orange")
        self.canvas.create_text(450, 235, text="BUZZER", fill="orange", font=("Arial", 10, "bold"))

        # ---- Arduino to Tank (Motor connection) ----
        self.canvas.create_line(250, 180, 830, 180, width=3, fill="blue")
        self.canvas.create_text(550, 165, text="MOTOR PUMP", fill="blue", font=("Arial", 10, "bold"))

    def add_controls(self):
        # Control buttons (Manual, Auto, Drain)
        frame = tk.Frame(self.root, bg="#87CEEB")
        frame.pack()

        tk.Button(frame, text="Manual Fill", bg="#070707", fg="black", width=15, command=self.manual_fill).grid(row=0, column=0, padx=10)
        tk.Button(frame, text="Auto Mode", bg="#55efc4", fg="black", width=15, command=self.auto_fill).grid(row=0, column=1, padx=10)
        tk.Button(frame, text="Drain Tank", bg="#fab1a0", fg="black", width=15, command=self.drain_tank).grid(row=0, column=2, padx=10)
        tk.Button(frame, text="DONE BY: M.MADESHWARAN, T.THAMIZHVENDHAN, KISHORE ARJUNAN", bg="#fab1a0", fg="black", width=50, command=self.drain_tank).grid(row=0, column=3, padx=40)

        # Water level indicator rectangle
        self.level_rect = self.canvas.create_rectangle(880, 300, 920, 420, fill="#74b9ff")
        self.water_level = 40  # initial level
        self.update_tank_level()

    def update_tank_level(self):
        top_y = 400 - self.water_level
        self.canvas.coords(self.level_rect, 810, top_y, 990, 400)
        self.root.update_idletasks()

    def manual_fill(self):
        if self.water_level < 120:
            self.water_level += 20
            self.update_tank_level()
            if self.water_level >= 120:
                self.play_buzzer()

    def auto_fill(self):
        for _ in range(6):
            self.root.after(400)
            self.water_level += 20
            self.update_tank_level()
            if self.water_level >= 120:
                self.play_buzzer()
                break

    def drain_tank(self):
        if self.water_level > 0:
            self.water_level -= 20
            self.update_tank_level()

    def play_buzzer(self):
        pygame.mixer.music.load(BUZZER_SOUND)
        pygame.mixer.music.play()
        print("🔊 Tank Full! Buzzer Sound Played.")

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = WaterLevelGUI(root)
    root.mainloop()
    
