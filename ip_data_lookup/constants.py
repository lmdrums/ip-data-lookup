import os

# Main
FILES_PATH = os.path.join("ip_data_lookup", "files")
ASSETS_FOLDER_PATH = os.path.join("ip_data_lookup", "assets")

# App
MAIN_TITLE = "IP Data Lookup"
MAIN_GEOMETRY = "960x540+480+270"
THEME_PATH = os.path.join(ASSETS_FOLDER_PATH, "theme.json")
IMAGES_PATH = os.path.join("ip_data_lookup", "images")
WINDOW_ICON_PATH = os.path.join(IMAGES_PATH, "logo.ico")

# Settings
SETTINGS_INI_PATH = os.path.join(FILES_PATH, "settings.ini")
CHECKBOXES_SETTING_SECTION_NAME = "CHECKBOXES"
COUNTRY_SETTING_LOCATOR = (CHECKBOXES_SETTING_SECTION_NAME, "country")
COUNTRY_CODE_SETTING_LOCATOR = (CHECKBOXES_SETTING_SECTION_NAME, "countryCode")
REGION_SETTING_LOCATOR = (CHECKBOXES_SETTING_SECTION_NAME, "region")
REGION_NAME_SETTING_LOCATOR = (CHECKBOXES_SETTING_SECTION_NAME, "regionName")
CITY_SETTING_LOCATOR = (CHECKBOXES_SETTING_SECTION_NAME, "city")
ZIP_CODE_SETTING_LOCATOR = (CHECKBOXES_SETTING_SECTION_NAME, "zip")
LATITUDE_SETTING_LOCATOR = (CHECKBOXES_SETTING_SECTION_NAME, "lat")
LONGITUDE_SETTING_LOCATOR = (CHECKBOXES_SETTING_SECTION_NAME, "lon")
TIMEZONE_SETTING_LOCATOR = (CHECKBOXES_SETTING_SECTION_NAME, "timezone")
ISP_SETTING_LOCATOR = (CHECKBOXES_SETTING_SECTION_NAME, "isp")
ORG_SETTING_LOCATOR = (CHECKBOXES_SETTING_SECTION_NAME, "org")
AS_SETTING_LOCATOR = (CHECKBOXES_SETTING_SECTION_NAME, "as")

DEFAULT_SETTINGS = {
    CHECKBOXES_SETTING_SECTION_NAME: {
        COUNTRY_SETTING_LOCATOR[1]: False,
        COUNTRY_CODE_SETTING_LOCATOR[1]: False,
        REGION_SETTING_LOCATOR[1]: False,
        REGION_NAME_SETTING_LOCATOR[1]: False,
        CITY_SETTING_LOCATOR[1]: False,
        ZIP_CODE_SETTING_LOCATOR[1]: False,
        LATITUDE_SETTING_LOCATOR[1]: False,
        LONGITUDE_SETTING_LOCATOR[1]: False,
        TIMEZONE_SETTING_LOCATOR[1]: False,
        ISP_SETTING_LOCATOR[1]: False,
        ORG_SETTING_LOCATOR[1]: False,
        AS_SETTING_LOCATOR[1]: False
    }
}

SETTINGS_DICT_LABELS = {
    'country': "Country:",
    'countryCode': "Country Code:", 
    'region': "Region:",
    'regionName': "Region Name:", 
    'city': "City:",
    'zip': "Zip:", 
    'lat': "Latitude:", 
    'lon': "Longitude:",
    'timezone': "Timezone:",
    'isp': "Internet Service Provider (ISP):",
    'org': "Organisation (Org):",
    'as': "Autonomous System (AS):"
}

# Images
BANNER_IMAGE = os.path.join(IMAGES_PATH, "banner.png")
BANNER_IMAGE_DARK = os.path.join(IMAGES_PATH, "banner_dark.png")
LOGO_CTK_IMAGE = os.path.join(IMAGES_PATH, "globe_logo.png")
SETTINGS_IMAGE = os.path.join(IMAGES_PATH, "settings.png")

# Map
MAP_TITLE = "IP Map"
MAP_GEOMETRY = "960x540+580+370"