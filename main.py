import customtkinter as ctk
import winsound
from widgets import SlidePanel
from alarm_clock import AlarmClock

height = 480
ctk.set_appearance_mode("Dark")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Alarm Clock")
        self.geometry(f"800x{height}")
        self.resizable(False, False)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        clock = AlarmClock(self, height)
        menu = SlidePanel(self, 0.00, 0.1, height)
        button = ctk.CTkButton(
            self, text="Menu",
            command=menu.animate,
            width=height//10,
            font=("Segoe UI", height//30))
        menu.change_alarm_btn.configure(
            command=clock.change_alarm,
            textvariable=clock.btn_text)

        clock.grid(row=1, column=1, columnspan=4, rowspan=3)
        button.place(relx=0.01, rely=0.02)
        menu.place(relx=-0.02, rely=0.1, relwidth=0.1,
                   relheight=0.5, anchor="ne")


if __name__ == "__main__":
    root = App()
    root.mainloop()
