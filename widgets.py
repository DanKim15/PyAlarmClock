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

        alarm_label = ctk.CTkLabel(
            self, text="Alarm Settings", font=("Segoe UI bold", height//45))
        self.change_btn_text = ctk.StringVar(self, "Change Alarm")
        self.change_alarm_btn = ctk.CTkButton(
            self, textvariable=self.change_btn_text, font=("Segoe UI", height//50), width=height//10)

        weather_label = ctk.CTkLabel(
            self, text="Weather Settings", font=("Segoe UI bold", height//45))
        self.radio = ctk.IntVar(self, 1)
        self.celc_btn = ctk.CTkRadioButton(
            self, text="Celcius", variable=self.radio, value=1, font=("Segoe UI", height//50),
            radiobutton_height=height//30,
            radiobutton_width=height//30)
        self.faren_btn = ctk.CTkRadioButton(
            self, text="Fahrenheit", variable=self.radio, value=2, font=("Segoe UI", height//50),
            radiobutton_height=height//30,
            radiobutton_width=height//30)
        self.location_choice = ctk.StringVar(self, value="Waterloo")
        self.location_options = ctk.CTkOptionMenu(self, values=[
            "Waterloo", "Hamilton", "Toronto", "Montreal", "Vancouver"],
            variable=self.location_choice, font=("Segoe UI", height//50), width=height//10)

        ui_label = ctk.CTkLabel(self, text="UI Settings",
                                font=("Segoe UI bold", height//45))
        change_theme_btn = ctk.CTkButton(
            self, text="Light/Dark", font=("Segoe UI", height//50), width=height//10, command=self.change_theme)

        alarm_label.pack(pady=2)
        self.change_alarm_btn.pack(pady=2)

        weather_label.pack(pady=(5, 2))
        self.celc_btn.pack(pady=1)
        self.faren_btn.pack(pady=1)
        self.location_options.pack(pady=2)

        ui_label.pack(pady=(5, 2))
        change_theme_btn.pack(pady=2)

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
