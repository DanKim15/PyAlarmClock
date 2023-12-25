import customtkinter as ctk
import winsound
from widgets import SlidePanel
from alarm_clock import AlarmClock
from weather_widget import Weather

height = 480
ctk.set_appearance_mode("Dark")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Alarm Clock")
        self.geometry(f"800x{height}")
        self.resizable(False, False)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.columnconfigure((0, 1, 2, 3, 4), weight=1)

        clock = AlarmClock(self, height)

        weather = Weather(self, height)

        menu = SlidePanel(self, 0.00, 0.1, height)
        button = ctk.CTkButton(
            self, text="Menu",
            command=menu.animate,
            width=height//10,
            font=("Segoe UI", height//30))
        menu.change_alarm_btn.configure(
            command=clock.change_alarm,
            textvariable=clock.btn_text)
        menu.celc_btn.configure(command=weather.change_celc)
        menu.faren_btn.configure(command=weather.change_faren)
        menu.location_options.configure(
            command=lambda x: weather.change_location(menu.location_choice.get()))

        clock.grid(row=2, column=2, sticky="nesw")
        weather.grid(row=3, column=2, sticky="n")
        button.place(relx=0.01, rely=0.02)
        menu.place(relx=-0.02, rely=0.1, relwidth=0.1,
                   relheight=0.5, anchor="ne")


if __name__ == "__main__":
    root = App()
    root.mainloop()
