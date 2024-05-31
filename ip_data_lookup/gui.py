from customtkinter import (CTk, CTkLabel, CTkFrame, CTkEntry, CTkButton, CTkOptionMenu,
                           CTkCheckBox, StringVar, CTkImage, CTkScrollableFrame,
                           set_appearance_mode, set_default_color_theme)
import utils.settings as s
import ip_data_lookup.constants as c
import sys
from PIL import Image, ImageTk
from utils.path import get_resource_path
from customtkinter.windows.widgets.appearance_mode import AppearanceModeTracker
from requests import get

set_appearance_mode("system")
set_default_color_theme(c.THEME_PATH)

get_pillow_image = lambda relative_path: Image.open(get_resource_path(relative_path))

class App(CTk):
    def __init__(self):
        super().__init__()

        if sys.platform.startswith("win"):
            self.title(c.MAIN_TITLE)
        self.geometry(c.MAIN_GEOMETRY)
        self.iconbitmap(c.WINDOW_ICON_PATH)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.navigation_frame = CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        """Navigation Section"""

        self.home_button = CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")


        self.settings_button = CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.settings_button_event)
        self.settings_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = CTkOptionMenu(self.navigation_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        """Home Section"""

        self.labels = []
        self.home_frame = CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.ip_search_box = CTkEntry(self.home_frame, placeholder_text="Enter IP (1.1.1.1)", border_width=1.5,
                                      justify="center", corner_radius=18, height=35, width=180)
        self.ip_search_box.grid(row=0, column=0, padx=(10,0), pady=(10,0))
        self.ip_search_box.bind("<Return>", lambda _: self.change_ip_info())

        self.search_button = CTkButton(self.home_frame, text="Search", command=self.change_ip_info)
        self.search_button.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="e")

        tk_image = self.get_banner_image()

        self.ip_logo = CTkLabel(self.home_frame, text="", image=tk_image)
        self.ip_logo.grid(row=0, column=0, sticky="w")

        """Settings Section"""

        self.true_settings = []
        self.settings_frame = CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        self.settings_label = CTkLabel(self.settings_frame, text="Select all information you would like to appear:",
                                       font=("Segoe UI", 16, "bold"))
        self.settings_label.grid(row=0, column=0, padx=(10,0), pady=(10,0), sticky="w")

        self.country_variable = StringVar(value="")
        self.country_code_variable = StringVar(value="")
        self.region_variable = StringVar(value="")
        self.region_name_variable = StringVar(value="")
        self.city_variable = StringVar(value="")
        self.zip_code_variable = StringVar(value="")
        self.latitude_variable = StringVar(value="")
        self.longitude_variable = StringVar(value="")
        self.timezone_variable = StringVar(value="")
        self.isp_variable = StringVar(value="")
        self.org_variable = StringVar(value="")
        self.as_variable = StringVar(value="")

        self.settings_dict = {
            c.COUNTRY_SETTING_LOCATOR: self.country_variable,
            c.COUNTRY_CODE_SETTING_LOCATOR: self.country_code_variable,
            c.REGION_SETTING_LOCATOR: self.region_variable,
            c.REGION_NAME_SETTING_LOCATOR: self.region_name_variable,
            c.CITY_SETTING_LOCATOR: self.city_variable,
            c.ZIP_CODE_SETTING_LOCATOR: self.zip_code_variable,
            c.LATITUDE_SETTING_LOCATOR: self.latitude_variable,
            c.LONGITUDE_SETTING_LOCATOR: self.longitude_variable,
            c.TIMEZONE_SETTING_LOCATOR: self.timezone_variable,
            c.ISP_SETTING_LOCATOR: self.isp_variable,
            c.ORG_SETTING_LOCATOR: self.org_variable,
            c.AS_SETTING_LOCATOR: self.as_variable,
        }

        self.country_tick = CTkCheckBox(self.settings_frame, text="Country", variable=self.country_variable, onvalue="on", offvalue="off", command=self.change_settings)
        self.country_tick.grid(row=1, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.country_code_tick = CTkCheckBox(self.settings_frame, text="Country Code", variable=self.country_code_variable, onvalue="on", offvalue="off", command=self.change_settings)
        self.country_code_tick.grid(row=2, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.region_tick = CTkCheckBox(self.settings_frame, text="Region", onvalue="on", variable=self.region_variable, offvalue="off", command=self.change_settings)
        self.region_tick.grid(row=3, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.region_name_tick = CTkCheckBox(self.settings_frame, text="Region Name", variable=self.region_name_variable, onvalue="on", offvalue="off", command=self.change_settings)
        self.region_name_tick.grid(row=4, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.city_tick = CTkCheckBox(self.settings_frame, text="City", onvalue="on", variable=self.city_variable, offvalue="off", command=self.change_settings)
        self.city_tick.grid(row=5, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.zip_tick = CTkCheckBox(self.settings_frame, text="ZIP/Post Code", variable=self.zip_code_variable, onvalue="on", offvalue="off", command=self.change_settings)
        self.zip_tick.grid(row=6, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.latitude_tick = CTkCheckBox(self.settings_frame, text="Latitude", variable=self.latitude_variable, onvalue="on", offvalue="off", command=self.change_settings)
        self.latitude_tick.grid(row=7, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.longitude_tick = CTkCheckBox(self.settings_frame, text="Longitude", variable=self.longitude_variable, onvalue="on", offvalue="off", command=self.change_settings)
        self.longitude_tick.grid(row=8, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.timezone_tick = CTkCheckBox(self.settings_frame, text="Timezone", variable=self.timezone_variable, onvalue="on", offvalue="off", command=self.change_settings)
        self.timezone_tick.grid(row=9, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.isp_tick = CTkCheckBox(self.settings_frame, text="Internet Service Provider (ISP)", variable=self.isp_variable, onvalue="on", offvalue="off", command=self.change_settings)
        self.isp_tick.grid(row=10, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.org_tick = CTkCheckBox(self.settings_frame, text="Organisation (Org)", variable=self.org_variable, onvalue="on", offvalue="off", command=self.change_settings)
        self.org_tick.grid(row=11, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.as_tick = CTkCheckBox(self.settings_frame, text="Autonomous System (AS)", variable=self.as_variable, onvalue="on", offvalue="off", command=self.change_settings)
        self.as_tick.grid(row=12, column=0, padx=(10,0), pady=(10,0), sticky="w")
        
        self.select_frame_by_name("home")

    def change_settings(self):
        self.change_settings_dict = {
            self.country_tick: c.COUNTRY_SETTING_LOCATOR,
            self.country_code_tick: c.COUNTRY_CODE_SETTING_LOCATOR,
            self.region_tick: c.REGION_SETTING_LOCATOR,
            self.region_name_tick: c.REGION_NAME_SETTING_LOCATOR,
            self.city_tick: c.CITY_SETTING_LOCATOR,
            self.zip_tick: c.ZIP_CODE_SETTING_LOCATOR,
            self.latitude_tick: c.LATITUDE_SETTING_LOCATOR,
            self.longitude_tick: c.LONGITUDE_SETTING_LOCATOR,
            self.timezone_tick: c.TIMEZONE_SETTING_LOCATOR,
            self.isp_tick: c.ISP_SETTING_LOCATOR,
            self.org_tick: c.ORG_SETTING_LOCATOR,
            self.as_tick: c.AS_SETTING_LOCATOR
        }

        self.true_settings = []
        for checkbox, locator in self.change_settings_dict.items():
            if checkbox.get() == "on":
                s.edit_setting(*locator, True)
                self.true_settings.append(locator[1])
            elif checkbox.get() == "off":
                s.edit_setting(*locator, False)

    def load_settings(self):
        for locator, variable in self.settings_dict.items():
            setting = s.get_setting(*locator, boolean=True)
            variable.set("on" if setting else "off")
            if setting:
                self.true_settings.append(locator[1])
            
    def select_frame_by_name(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def settings_button_event(self):
        self.select_frame_by_name("settings")
        self.load_settings()

    def change_appearance_mode(self, mode):
        set_appearance_mode(mode)
        self.after(100, self.update_banner_image)

    def update_banner_image(self):
        image = self.get_banner_image()
        self.ip_logo.configure(image=image)
    
    def get_banner_image(self):
        if AppearanceModeTracker.appearance_mode == 0:
            pil_image = Image.open(get_resource_path(c.BANNER_IMAGE))
            pil_image = pil_image.resize((228,84))
            return ImageTk.PhotoImage(pil_image)
        
        elif AppearanceModeTracker.appearance_mode == 1:
            pil_image = Image.open(get_resource_path(c.BANNER_IMAGE_DARK))
            pil_image = pil_image.resize((228,84))
            return ImageTk.PhotoImage(pil_image)
        
    def change_ip_info(self):
        ip = self.ip_search_box.get().strip()
        for label in self.labels:
            label.destroy()
        self.labels = []
        if ip:
            row = 1
            data = get(f"http://ip-api.com/json/{ip}").json()
            for setting in self.true_settings:
                label_heading = c.SETTINGS_DICT_LABELS[setting]
                self.label = CTkLabel(self.home_frame, text=f"{label_heading} {data[setting]}")
                self.label.grid(row=row, column=0, sticky="w")
                self.labels.append(self.label)
                row += 1

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()