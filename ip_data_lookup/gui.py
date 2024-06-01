from customtkinter import (CTk, CTkLabel, CTkFrame, CTkEntry, CTkButton, CTkOptionMenu,
                           CTkCheckBox, StringVar, CTkImage, CTkScrollableFrame, CTkToplevel,
                           set_appearance_mode, set_default_color_theme, CTkBaseClass)
from customtkinter.windows.widgets.appearance_mode import AppearanceModeTracker
from PIL import Image, ImageTk
import tkintermapview

import sys
from subprocess import Popen, PIPE
from requests import get
from tkinter import messagebox, scrolledtext, Entry
import threading

from utils.path import get_resource_path
import utils.settings as s
import ip_data_lookup.constants as c

set_appearance_mode("system")
set_default_color_theme(c.THEME_PATH)

get_pillow_image = lambda relative_path: Image.open(get_resource_path(relative_path))

globe_image = CTkImage(light_image=get_pillow_image(c.LOGO_CTK_IMAGE),
                dark_image=get_pillow_image(c.LOGO_CTK_IMAGE))
settings_image = CTkImage(light_image=get_pillow_image(c.SETTINGS_IMAGE),
                dark_image=get_pillow_image(c.SETTINGS_IMAGE))

class App(CTk):
    """Main application class for this program"""

    def __init__(self):
        super().__init__()

        if sys.platform.startswith("win"): # 'iconbitmap' only work for Windows machines
            self.iconbitmap(c.WINDOW_ICON_PATH)
        self.title(c.MAIN_TITLE)
        self.geometry(c.MAIN_GEOMETRY)
        
        # Set up grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.navigation_frame = CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        """Navigation Section"""

        tk_image = self.get_banner_image()

        self.ip_logo = CTkLabel(self.navigation_frame, text="", image=tk_image)
        self.ip_logo.grid(row=0, column=0, sticky="w")

        # Set up all navigation bar buttons
        self.home_button = CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                     text="Home",fg_color="transparent", text_color=("gray10", "gray90"),
                                     hover_color=("gray70", "gray30"),anchor="w", 
                                     command=self.home_button_event, image=globe_image)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.tracert_button = CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                        text="Traceroute", fg_color="transparent", text_color=("gray10", "gray90"),
                                        hover_color=("gray70", "gray30"), anchor="w",
                                        command=self.tracert_button_event, image=globe_image)
        self.tracert_button.grid(row=2, column=0, sticky="ew")

        self.settings_button = CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                         text="Settings", fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"), anchor="w",
                                         command=self.settings_button_event, image=settings_image)
        self.settings_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = CTkOptionMenu(self.navigation_frame, values=["System", "Light", "Dark"],
                                                  command=self.change_appearance_mode)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        """Home Section"""

        self.labels = []
        self.home_frame = CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=20)

        public_ip = get("https://checkip.amazonaws.com/").text
        self.ip_search_box = CTkEntry(self.home_frame, placeholder_text=public_ip,
                                      border_width=1.5,justify="center",
                                      corner_radius=18, height=35, width=130)
        self.ip_search_box.grid(row=0, column=0, pady=10, columnspan=2)
        self.ip_search_box.bind("<1>", lambda _: self.in_focus(self.ip_search_box, 300)) # Animates entry when you click on it
        self.ip_search_box.bind("<Return>", lambda _: self.change_ip_info())
        self.ip_search_box.bind("<KeyRelease>", lambda _: self.check_valid_ip()) # Highlights entry border red if IP isn't valid

        """Traceroute Section"""

        self.tracert_frame = CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")

        self.enter_hostname = CTkEntry(self.tracert_frame, placeholder_text="Enter Hostname",
                                       border_width=1.5, justify="center",
                                       corner_radius=18, height=35, width=130)
        self.enter_hostname.pack(pady=10)
        self.enter_hostname.bind("<1>", lambda _: self.in_focus(self.enter_hostname, 300))
        self.enter_hostname.bind("<Return>", lambda _: self.tracert_function())

        self.tracert_output = scrolledtext.ScrolledText(self.tracert_frame, bd=1,
                                                      font=("Consolas", 9), height=25)
        self.tracert_output.pack(pady=20, padx=20, expand=True, fill="both")
        self.tracert_output.configure(state="disabled")
        
        """Settings Section"""

        self.true_settings = []
        self.settings_frame = CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        self.settings_label = CTkLabel(self.settings_frame,
                                       text="Select all information you would like to appear:",
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

        # Locators to corresponding StringVar
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

        # Places checkboxes
        self.country_tick = CTkCheckBox(self.settings_frame, text="Country", 
                                        variable=self.country_variable, onvalue="on",
                                        offvalue="off", command=self.change_settings)
        self.country_tick.grid(row=1, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.country_code_tick = CTkCheckBox(self.settings_frame, text="Country Code",
                                             variable=self.country_code_variable, onvalue="on",
                                             offvalue="off", command=self.change_settings)
        self.country_code_tick.grid(row=2, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.region_tick = CTkCheckBox(self.settings_frame, text="Region", onvalue="on",
                                       variable=self.region_variable,
                                       offvalue="off", command=self.change_settings)
        self.region_tick.grid(row=3, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.region_name_tick = CTkCheckBox(self.settings_frame, text="Region Name",
                                            variable=self.region_name_variable, onvalue="on",
                                            offvalue="off", command=self.change_settings)
        self.region_name_tick.grid(row=4, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.city_tick = CTkCheckBox(self.settings_frame, text="City", onvalue="on",
                                     variable=self.city_variable,
                                     offvalue="off", command=self.change_settings)
        self.city_tick.grid(row=5, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.zip_tick = CTkCheckBox(self.settings_frame, text="ZIP/Post Code",
                                    variable=self.zip_code_variable, onvalue="on",
                                    offvalue="off", command=self.change_settings)
        self.zip_tick.grid(row=6, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.latitude_tick = CTkCheckBox(self.settings_frame, text="Latitude",
                                         variable=self.latitude_variable, onvalue="on",
                                         offvalue="off", command=self.change_settings)
        self.latitude_tick.grid(row=7, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.longitude_tick = CTkCheckBox(self.settings_frame, text="Longitude",
                                          variable=self.longitude_variable, onvalue="on",
                                          offvalue="off", command=self.change_settings)
        self.longitude_tick.grid(row=8, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.timezone_tick = CTkCheckBox(self.settings_frame, text="Timezone",
                                         variable=self.timezone_variable, onvalue="on",
                                         offvalue="off", command=self.change_settings)
        self.timezone_tick.grid(row=9, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.isp_tick = CTkCheckBox(self.settings_frame, text="Internet Service Provider (ISP)",
                                    variable=self.isp_variable, onvalue="on",
                                    offvalue="off", command=self.change_settings)
        self.isp_tick.grid(row=10, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.org_tick = CTkCheckBox(self.settings_frame, text="Organisation (Org)",
                                    variable=self.org_variable, onvalue="on",
                                    offvalue="off", command=self.change_settings)
        self.org_tick.grid(row=11, column=0, padx=(10,0), pady=(10,0), sticky="w")
        self.as_tick = CTkCheckBox(self.settings_frame, text="Autonomous System (AS)",
                                   variable=self.as_variable, onvalue="on",
                                   offvalue="off", command=self.change_settings)
        self.as_tick.grid(row=12, column=0, padx=(10,0), pady=(10,0), sticky="w")
        
        self.load_settings()
        self.select_frame_by_name("home")

    def tracert(self, hostname: str, entry_widget: CTkEntry | scrolledtext.ScrolledText | Entry) -> None:
        """
        Executes the tracert command on all systems and inserts output into Entry widget\n
        Note: `traceroute` is installed on most Linux distros but if it's not then use the command:\n
        `sudo apt-get install traceroute` or whichever package installer you have
        """

        if sys.platform.startswith("win"):
            tracert = Popen(f"cmd /c tracert {hostname}", shell=True, stdout=PIPE, encoding='utf-8')
        else:
            tracert = Popen([f"traceroute {hostname}"], shell=True, stdout=PIPE, encoding="utf-8")
        entry_widget.config(state="normal")
        entry_widget.delete(1.0, "end")
        entry_widget.insert("end", "Running...\n\n")
        for line in tracert.stdout:
            entry_widget.insert("end", line.rstrip("\n")+"\n")
            if "unable" in line.lower():
                entry_widget.insert("end", "\nCompleted with errors.")
                self.enter_hostname.bind("<Return>", lambda _: self.tracert_function())
                return
        
        entry_widget.insert("end", "\nCompleted successfully!")
        self.enter_hostname.bind("<Return>", lambda _: self.tracert_function())
        entry_widget.config(state="disabled")

    def tracert_function(self) -> None:
        """Runs the tracert function above"""

        self.tracert_output.delete(1.0, "end")
        self.enter_hostname.unbind("<Return>", None) # Unbinds Return key to prevent multiple commands being executed at once
        def run():
            hostname = self.enter_hostname.get()
            try:
                self.tracert(hostname, self.tracert_output)
            except Exception:
                messagebox.showerror("Error", "An error occured whilst completing the traceroute.")
        thread = threading.Thread(target=run) # Starts a thread to prevent program from crashing
        thread.start()
        
    def in_focus(self, widget: CTkBaseClass, target: int) -> None:
        """Adds animation to widget"""

        width = widget.cget("width")
        if width < target:
            # Increases widget width by 1px every 1ms until it's 300px wide
            widget.configure(width=width + 1)
            self.after(1, self.in_focus, widget, 300)

    def change_settings(self) -> None:
        """Changes settings.ini file when a checkbox value is changed"""

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

        self.true_settings = [] # Creates empty list
        # For every setting which is True, add the setting name to the list
        for checkbox, locator in self.change_settings_dict.items():
            if checkbox.get() == "on":
                s.edit_setting(*locator, True)
                self.true_settings.append(locator[1])
            elif checkbox.get() == "off":
                s.edit_setting(*locator, False)

    def load_settings(self) -> None:
        """Loads the current settings when frame is changed to Settings"""

        # For every setting, either set the checkbox value "on" or "off" due to whether it's True or False
        for locator, variable in self.settings_dict.items():
            setting = s.get_setting(*locator, boolean=True)
            variable.set("on" if setting else "off")
            if setting:
                self.true_settings.append(locator[1])
            
    def select_frame_by_name(self, name: str) -> None:
        """Changes which frame is currently visible in the application"""

        self.home_button.configure(fg_color=("gray75", "gray25")
                                   if name == "home" else "transparent")
        self.tracert_button.configure(fg_color=("gray75", "gray25")
                                      if name == "tracert" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25")
                                       if name == "settings" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "tracert":
            self.tracert_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.tracert_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")
        self.change_ip_info() # Updates the info in case any settings have changed
    
    def tracert_button_event(self):
        self.select_frame_by_name("tracert")

    def settings_button_event(self):
        self.select_frame_by_name("settings")

    def change_appearance_mode(self, mode):
        set_appearance_mode(mode)
        self.after(100, self.update_banner_image) # Makes sure banner is the correct colour

    def update_banner_image(self) -> None:
        """Updates the banner image (light or dark)"""

        image = self.get_banner_image()
        self.ip_logo.configure(image=image)
    
    def get_banner_image(self) -> ImageTk.PhotoImage:
        """Returns the correct banner image depending on the colour theme"""

        if AppearanceModeTracker.appearance_mode == 0:
            pil_image = Image.open(get_resource_path(c.BANNER_IMAGE))
            pil_image = pil_image.resize((228,84))
            return ImageTk.PhotoImage(pil_image)
        
        elif AppearanceModeTracker.appearance_mode == 1:
            pil_image = Image.open(get_resource_path(c.BANNER_IMAGE_DARK))
            pil_image = pil_image.resize((228,84))
            return ImageTk.PhotoImage(pil_image)
        
    def change_ip_info(self) -> None:
        """Changes the IP information shown due to which settings are True"""

        ip = self.ip_search_box.get().strip() # Gets the IP address entered
        for label in self.labels:
            label.destroy() # Destroys existing labels
        self.labels = [] # Clears list
        if ip:
            row = 1
            data = get(f"http://ip-api.com/json/{ip}").json()
            for setting in self.true_settings:
                label_heading = c.SETTINGS_DICT_LABELS[setting] # Gets the correct label heading
                try:
                    # Places labels
                    self.label = CTkLabel(self.home_frame, text=f"{label_heading} ", font=("Segoe UI", 13, "bold"))
                    self.label2 = CTkLabel(self.home_frame, text=data[setting])
                except KeyError:
                    messagebox.showerror("Error", "Please enter a valid Public IP address")
                    return
                else:
                    # Positions labels and adds the labels to the list
                    self.label.grid(row=row, column=0, padx=(10,0), sticky="w")
                    self.label2.grid(row=row, column=1, padx=(10,0), sticky="w")
                    self.labels.append(self.label)
                    self.labels.append(self.label2)
                    row += 1

            # Adds "Show on Map" button
            self.show_map_button = CTkButton(self.home_frame, text="Show on Map", command=self.show_map)
            self.show_map_button.grid(row=row, column=0, padx=(10,0), pady=(10,0), sticky="w")
            self.labels.append(self.show_map_button)

    def check_valid_ip(self) -> None:
        """
        Checks if the IP address entered is valid whilst the user is entering it.\n
        If it's not, it will highlight the entry border red
        """

        ip = self.ip_search_box.get()
        if not ip or '.' not in ip or len(ip.split('.')) != 4:
            self.ip_search_box.configure(border_color="red")
            return

        for part in ip.split('.'):
            if not part.isdigit() or int(part) > 255:
                self.ip_search_box.configure(border_color="red")
                return

        self.ip_search_box.configure(border_color=("#979DA2", "#565B5E"))
    
    def show_map(self) -> None:
        """Opens map in a CTkToplevel window"""

        map_class = Map(self.ip_search_box.get())
        map_class.mainloop()

class Map(CTkToplevel):
    """CTkToplevel window for the map"""

    def __init__(self, ip: str):
        super().__init__()
        self.ip = ip
        self.title(c.MAP_TITLE)
        if sys.platform.startswith("win"):
            self.after(250, lambda: self.iconbitmap(get_resource_path(c.WINDOW_ICON_PATH)))
        self.geometry(c.MAP_GEOMETRY)

        data = get(f"http://ip-api.com/json/{ip}").json()
        latitude = data["lat"]
        longitude = data["lon"]

        # Places map within window
        self.map = tkintermapview.TkinterMapView(self, corner_radius=0)
        self.map.pack(fill="both", expand=True)
        self.map.set_position(latitude, longitude)
        self.map.set_zoom(13)
        self.map.set_marker(latitude, longitude)

        self.after(200, self.lift)

def main() -> None:
    """Initiates main window"""

    app = App()
    app.mainloop()