import customtkinter as ctk
from PIL import Image, ImageTk
from widgets import LTime
import time
import winsound

arrow = Image.open("arrow.png")
arrow_up = ctk.CTkImage(
    light_image=arrow)
arrow_down = ctk.CTkImage(
    light_image=arrow.transpose(Image.FLIP_TOP_BOTTOM))


class AlarmClock(ctk.CTkFrame):
    def __init__(self, parent, height):
        super().__init__(master=parent, fg_color="transparent", bg_color="transparent")

        self.set_hour = 12
        self.set_min = 0
        self.set_time = ctk.StringVar(
            self, f"{self.set_hour:02}:{self.set_min:02}:00")
        self.set_ampm = ctk.StringVar(self, "AM")
        self.height = height
        self.btn_text = ctk.StringVar(self, "Change Alarm")
        self.not_changing = True
        self.blinking = True
        self.blink_off = True
        self.snoozed = False
        self.stopped = False
        self.play_sound = True

        self.rowconfigure((0, 1, 2), weight=1, uniform="a")
        self.columnconfigure((0, 1, 2, 3), weight=1)

        self.current_time = LTime(self, self.height//4, True)
        self.current_ampm = LTime(self, self.height//10, False)
        self.empty_box = ctk.CTkFrame(
            self, fg_color="transparent", bg_color="transparent")
        self.empty_box.grid(row=0, column=1, sticky="s")
        self.current_time.grid(row=1, column=0, columnspan=3, sticky="nesw")
        self.current_ampm.grid(row=1, column=3, sticky="w")

        self.set_time_label = ctk.CTkLabel(
            self, textvariable=self.set_time, font=("Segoe UI", self.height//4), padx=10)
        self.set_ampm_label = ctk.CTkLabel(
            self, textvariable=self.set_ampm, font=("Segoe UI", self.height//10), padx=10)
        self.hr_up = ctk.CTkButton(
            self, text="", image=arrow_up, command=self.increase_hour)
        self.hr_down = ctk.CTkButton(
            self, text="", image=arrow_down, command=self.decrease_hour)
        self.min_up = ctk.CTkButton(
            self, text="", image=arrow_up, command=self.increase_min)
        self.min_down = ctk.CTkButton(
            self, text="", image=arrow_down, command=self.decrease_min)
        self.ampm_up = ctk.CTkButton(
            self, text="", image=arrow_up, command=self.change_ampm)
        self.ampm_down = ctk.CTkButton(
            self, text="", image=arrow_down, command=self.change_ampm)

        self.check_alarm()

    def change_alarm(self):
        if self.not_changing:
            self.current_time.grid_remove()
            self.current_ampm.grid_remove()
            self.set_time_label.grid(
                row=1, column=0, columnspan=3, sticky="nesw")
            self.set_ampm_label.grid(row=1, column=3, sticky="w")
            self.hr_up.grid(row=0, column=0, sticky="s")
            self.hr_down.grid(row=2, column=0, sticky="n", pady=20)
            self.min_up.grid(row=0, column=1, sticky="s")
            self.min_down.grid(row=2, column=1, sticky="n", pady=20)
            self.ampm_up.grid(row=0, column=3, sticky="sw")
            self.ampm_down.grid(row=2, column=3, sticky="nw", pady=20)
            self.btn_text.set("Save")
            self.not_changing = False
        else:
            self.set_time_label.grid_forget()
            self.set_ampm_label.grid_forget()
            self.hr_up.grid_forget()
            self.hr_down.grid_forget()
            self.min_up.grid_forget()
            self.min_down.grid_forget()
            self.ampm_up.grid_forget()
            self.ampm_down.grid_forget()
            self.current_time.grid()
            self.current_ampm.grid()
            self.btn_text.set("Change Alarm")
            self.not_changing = True

    def check_alarm(self):
        hrmin, apm = LTime.current_time(self)
        if hrmin == self.set_time.get() and apm == self.set_ampm.get():
            self.play_sound = True
            self.snooze_btn = ctk.CTkButton(
                self, text="Snooze", command=self.snooze_press, font=("Segoe UI", self.height//50), width=self.height//10)
            self.stop_btn = ctk.CTkButton(
                self, text="Stop", command=self.stop_press, font=("Segoe UI", self.height//50), width=self.height//10)
            self.snooze_btn.grid(row=2, column=1)
            self.stop_btn.grid(row=2, column=2)
            self.og_theme = ctk.get_appearance_mode()
            self.blink()
            self.alarm_sounds()
        self.after(1000, self.check_alarm)

    def snooze_press(self):
        hrmin, apm = LTime.current_time(self)
        mins = int(hrmin[3:5])
        if mins > 51:
            self.increase_hour
            self.set_min = mins + 9 - 60
        else:
            self.set_min = mins + 9
        self.set_time.set(f"{self.set_hour:02}:{self.set_min:02}:00")
        self.blinking = False
        self.blink_off = True
        self.play_sound = False
        self.snooze_btn.grid_forget()
        self.stop_btn.grid_forget()

    def stop_press(self):
        self.blinking = False
        self.blink_off = True
        self.play_sound = False
        self.snooze_btn.grid_forget()
        self.stop_btn.grid_forget()

    def blink(self):
        if self.blinking:
            if ctk.get_appearance_mode() == "Dark":
                ctk.set_appearance_mode("Light")
            else:
                ctk.set_appearance_mode("Dark")
            self.after(500, self.blink)
        else:
            ctk.set_appearance_mode(self.og_theme)

    def alarm_sounds(self):
        if self.play_sound:
            winsound.PlaySound("beep-06.wav", 0)
            self.after(500, self.alarm_sounds)

    def increase_hour(self):
        if self.set_hour == 12:
            self.set_hour = 1
        else:
            self.set_hour += 1
        self.set_time.set(f"{self.set_hour:02}:{self.set_min:02}:00")

    def decrease_hour(self):
        if self.set_hour == 1:
            self.set_hour = 12
        else:
            self.set_hour -= 1
        self.set_time.set(f"{self.set_hour:02}:{self.set_min:02}:00")

    def increase_min(self):
        if self.set_min % 5 != 0:
            self.set_min = self.set_min - (self.set_min % 5)
        if self.set_min == 55:
            self.set_min = 0
        else:
            self.set_min += 5
        self.set_time.set(f"{self.set_hour:02}:{self.set_min:02}:00")

    def decrease_min(self):
        if self.set_min % 5 != 0:
            self.set_min = self.set_min - (self.set_min % 5)
        if self.set_min == 0:
            self.set_min = 55
        else:
            self.set_min -= 5
        self.set_time.set(f"{self.set_hour:02}:{self.set_min:02}:00")

    def change_ampm(self):
        if self.set_ampm.get() == "AM":
            self.set_ampm.set("PM")
        else:
            self.set_ampm.set("AM")
