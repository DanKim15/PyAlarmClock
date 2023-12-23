import customtkinter as ctk
from datetime import datetime
# from alarm_clock import AlarmClock


class LTime(ctk.CTkLabel):

    def __init__(self, parent, h, time_or_ampm):

        self.ctime = ctk.StringVar()
        self.hours_mins, self.ampm = self.current_time()
        self.time_or_ampm = time_or_ampm
        if time_or_ampm:
            self.ctime.set(self.hours_mins)
        else:
            self.ctime.set(self.ampm)
        self.font = ctk.CTkFont(size=h)
        super().__init__(parent, textvariable=self.ctime, font=(
            "Segoe UI", h), padx=10)
        self.update_time()

    def update_time(self):
        self.hours_mins, self.ampm = self.current_time()
        if self.time_or_ampm:
            self.ctime.set(self.hours_mins)
        else:
            self.ctime.set(self.ampm)
        self.after(10, self.update_time)

    def current_time(self):
        now = datetime.now()
        hrmin = now.strftime("%I:%M:%S")
        apm = now.strftime("%p")
        return hrmin, apm


class SlidePanel(ctk.CTkFrame):
    def __init__(self, parent, start_pos, end_pos, height):
        super().__init__(master=parent)

        self.start_pos = start_pos - 0.02
        self.end_pos = end_pos + 0.01
        self.width = abs(start_pos - end_pos)

        self.pos = self.start_pos
        self.in_start_pos = True

        self.change_btn_text = ctk.StringVar(self, "Change Alarm")
        self.change_alarm_btn = ctk.CTkButton(
            self, textvariable=self.change_btn_text, font=("Segoe UI", height//50), width=height//10)
        self.change_theme_btn = ctk.CTkButton(
            self, text="Light/Dark", font=("Segoe UI", height//50), width=height//10, command=self.change_theme)

        self.change_alarm_btn.pack(pady=5)
        self.change_theme_btn.pack(pady=5)

    def change_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    def animate(self):
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos < self.end_pos:
            self.pos += 0.008
            self.place(relx=self.pos, rely=0.1,
                       relwidth=self.width, relheight=0.9, anchor="ne")
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backwards(self):
        if self.pos > self.start_pos:
            self.pos -= 0.008
            self.place(relx=self.pos, rely=0.1,
                       relwidth=self.width, relheight=0.9, anchor="ne")
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True
