import urllib.request
import requests
from dotenv import load_dotenv
import os
import customtkinter as ctk
from PIL import Image
import PIL.ImageOps

load_dotenv()


class Weather(ctk.CTkFrame):
    def __init__(self, parent, height):
        super().__init__(parent, fg_color="transparent", bg_color="transparent")
        self.location = "Waterloo"
        self.condition = ctk.StringVar(self, "Unavailable")
        self.temp = ctk.StringVar(self, "N/A")
        self.feel_temp = ctk.StringVar(self, "N/A")
        self.location_info = ctk.StringVar(self, "Unavailable")
        self.is_celc = True

        self.update_weather()

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0, 1), weight=1)

        location_label = ctk.CTkLabel(self, textvariable=self.location_info, font=(
            "Segoe UI", height//30))
        self.icon_label = ctk.CTkLabel(self, image=self.icon_img, text="")
        condition_label = ctk.CTkLabel(self, textvariable=self.condition, font=(
            "Segoe UI", height//25))
        temp_label = ctk.CTkLabel(self, textvariable=self.temp, font=(
            "Segoe UI", height//10))
        feel_temp_label = ctk.CTkLabel(self, textvariable=self.feel_temp, font=(
            "Segoe UI", height//25))

        location_label.grid(row=0, column=0, columnspan=2, sticky="s")
        self.icon_label.grid(row=1, column=0, padx=10)
        condition_label.grid(row=2, column=0, padx=10)
        temp_label.grid(row=1, column=1, padx=10)
        feel_temp_label.grid(row=2, column=1, padx=10)

    def update_weather(self):
        self.fetch()
        self.update_icon()
        self.icon_label = ctk.CTkLabel(self, image=self.icon_img, text="")
        self.icon_label.grid_forget()
        self.icon_label.grid(row=1, column=0, padx=10)
        self.condition.set(self.get_current_data("condition").get("text"))
        if self.is_celc:
            self.temp.set(f'{str(self.get_current_data("temp_c"))}°C')
            self.feel_temp.set(
                f'Feels like {str(self.get_current_data("feelslike_c"))}°C')
        else:
            self.temp.set(f'{str(self.get_current_data("temp_f"))}°F')
            self.feel_temp.set(
                f'Feels like {str(self.get_current_data("feelslike_f"))}°F')
        self.location_info.set(
            f'{self.get_location_data("name")}, {self.get_location_data("region")}')
        self.job = self.after(300000, self.update_weather)  # every 5 mins

    def update_icon(self):
        urllib.request.urlretrieve(
            f"https:{self.get_current_data('condition').get('icon')}", "icon.png")
        self.icon = Image.open("icon.png")
        self.invert()
        inverted_icon = Image.open("inverted_icon.png")
        self.icon_img = ctk.CTkImage(
            dark_image=self.icon, light_image=inverted_icon, size=(64, 64))

    def invert(self):
        if self.icon.mode == "RGBA":
            r, g, b, a = self.icon.split()
            rgb_image = Image.merge("RGB", (r, g, b))
            inverted_image = PIL.ImageOps.invert(rgb_image)
            r2, g2, b2 = inverted_image.split()
            final_transparent_image = Image.merge("RGBA", (r2, g2, b2, a))
            final_transparent_image.save("inverted_icon.png")
        else:
            inverted_image = PIL.ImageOps.invert(self.icon)
            inverted_image.save("inverted_icon.png")

    def get_location_data(self, name):
        return str(self.weather_data["location"][name])

    def get_current_data(self, name):
        return self.weather_data["current"][name]

    def fetch(self):
        try:
            url = f"http://api.weatherapi.com/v1/current.json?key={os.getenv('WEATHER_API_KEY')}&q={self.location}&aqi=no"
            self.weather_data = requests.get(url).json()
        except:
            self.weather_data = {"error"}

    def change_celc(self):
        self.is_celc = True
        self.reload_weather()

    def change_faren(self):
        self.is_celc = False
        self.reload_weather()

    def change_location(self, choice):
        print(choice)
        self.location = choice
        self.reload_weather()

    def reload_weather(self):
        if self.job is not None:
            self.after_cancel(self.job)
            self.job = None
        self.update_weather()
