# Emirhan Toprak 
# Hasan Efe Dinç 
# Şükrü Kaan Tetik 


import pathlib
import tkinter as tk
from tkinter import ttk

import gather_data
from gather_data import GatherData
import file_storage

#Check Internet
gather_data.GatherData.check_internet(None)

def check_settings():
    global temp_mode
    global default_city
    if pathlib.Path('settings.txt').is_file():
        setting_obj = file_storage.StoreSetting()
        dict = setting_obj.convert_setting_to_dict()

        city = dict["City"]
        tm = dict["Scale"]
        temp_mode = tm
        default_city = city



default_city = ""
temp_mode = "Celsius"
check_default = True
check_settings()


def fahrenheit_converter(temperature):
    return "{:.1f}".format(temperature * 1.8 + 32)


setting_select = ""

def check_input(event):
    value = var.get()
    value = value.upper()
    new_values = []
    for city in cities:
        if city.upper().startswith(value):
            new_values.append(city)
    combobox['values'] = new_values


def set_default_settings():
    setting_store_obj = file_storage.StoreSetting()
    setting_store_obj.write_user_preferences(setting_select, temp_mode)


# DROP BOX
def Main(city=None):
    gather_data.GatherData.check_internet(None)#Checks Internet Everytime city selected in dropbox


    global selected_city
    selected_city = city if city else combobox.get()

    global setting_select
    setting_select = selected_city


    store_weather_obj = file_storage.StoreWeather(selected_city)
    store_weather_obj.write_current_info()
    store_weather_obj.write_daily_info()

    global image_current
    global image_today
    global image_tomorrow
    global image_day_after_tomorrow

    image_current = store_weather_obj.choose_picture_current()

    current_data_lable = ttk.Label(root,
                                   textvariable=current_data_stringvar,
                                   font=("Arial", 15),
                                   image=image_current,
                                   compound='top')

    image_today = store_weather_obj.choose_image_main_daily("Today")
    today_data_lable = ttk.Label(root,
                                 textvariable=today_data_stringVar,
                                 font=("Arial", 10),
                                 image=image_today,
                                 compound='top')
    image_tomorrow = store_weather_obj.choose_image_main_daily("Tomorrow")

    tomorrow_data_lable = ttk.Label(root,
                                    textvariable=tomorrow_data_stringVar,
                                    font=("Arial", 10),
                                    image=image_tomorrow,
                                    compound='top')
    image_day_after_tomorrow = store_weather_obj.choose_image_main_daily("Day After Tomorrow")
    day_after_tomorrow_lable = ttk.Label(root,
                                         textvariable=day_after_tomorrow_stringVar,
                                         font=("Arial", 10),
                                         image=image_day_after_tomorrow,
                                         compound='top')

    current_data_lable.configure(image=image_current)
    today_data_lable.configure(image=image_today)
    tomorrow_data_lable.configure(image=image_tomorrow)
    day_after_tomorrow_lable.configure(image=image_day_after_tomorrow)

    current_data_lable.place(relx=0.5, rely=0.35, anchor="center")
    today_data_lable.place(relx=0.2, rely=0.818, anchor="center")
    tomorrow_data_lable.place(relx=0.5, rely=0.818, anchor="center")
    day_after_tomorrow_lable.place(relx=0.8, rely=0.818, anchor="center")

    data_dict = store_weather_obj.convert_text_to_dict()
    data_dict_current = data_dict["Current"]
    if temp_mode == "Fahrenheit":
        temperature = int(data_dict_current["Temperature"][:3])
        data_dict_current["Temperature"] = fahrenheit_converter(temperature) + " F"
        feelsLike = int(data_dict_current["Feels Like"][:3])
        data_dict_current["Feels Like"] = fahrenheit_converter(feelsLike) + " F"
    current_data_text = ""
    for key in data_dict_current:
        if (key == "Temperature") or (key == "Condition"):
            current_data_text += "{:^50}\n".format(data_dict_current[key])
        else:
            current_data_text += "\n{:<5}: {:^15} ".format(key, data_dict_current[key])
    current_data_stringvar.set(current_data_text)


    if temp_mode == "Fahrenheit":
        temperature = data_dict["Today"]["Temperature"][:7]
        tmp_day = int(temperature.split(" / ")[0])
        tmp_night = int(temperature.split(" / ")[1])
        tmp_day = fahrenheit_converter(tmp_day)
        tmp_night = fahrenheit_converter(tmp_night)
        data_dict["Today"]["Temperature"] = tmp_day + " / " + tmp_night + " F"

        temperature = data_dict["Tomorrow"]["Temperature"][:7]
        tmp_day = int(temperature.split(" / ")[0])
        tmp_night = int(temperature.split(" / ")[1])
        tmp_day = fahrenheit_converter(tmp_day)
        tmp_night = fahrenheit_converter(tmp_night)
        data_dict["Tomorrow"]["Temperature"] = tmp_day + " / " + tmp_night + " F"

        temperature = data_dict["Day After Tomorrow"]["Temperature"][:7]
        tmp_day = int(temperature.split(" / ")[0])
        tmp_night = int(temperature.split(" / ")[1])
        tmp_day = fahrenheit_converter(tmp_day)
        tmp_night = fahrenheit_converter(tmp_night)
        data_dict["Day After Tomorrow"]["Temperature"] = tmp_day + " / " + tmp_night + " F"



    today_data_text = ""
    for key in data_dict["Today"]:
        if key == "Temperature":
            today_data_text += "\n{:^50}\n".format(data_dict["Today"]["Temperature"])
        else:
            today_data_text += "{:<5}: {:^15}\n".format(key, data_dict["Today"][key])

    tomorrow_data_text = ""
    for key in data_dict["Tomorrow"]:
        if key == "Temperature":
            tomorrow_data_text += "\n{:^50}\n".format(data_dict["Tomorrow"]["Temperature"])
        else:
            tomorrow_data_text += "{:<5}: {:^15}\n".format(key, data_dict["Tomorrow"][key])

    day_after_tomorrow_data_text = ""
    for key in data_dict["Day After Tomorrow"]:
        if key == "Temperature":
            day_after_tomorrow_data_text += "\n{:^50}\n".format(data_dict["Day After Tomorrow"]["Temperature"])
        else:
            day_after_tomorrow_data_text += "{:<5}: {:^10}\n".format(key, data_dict["Day After Tomorrow"][key])

    header_day = data_dict["Current"]["Latest Update"]
    header_month = header_day.split(" ")[1]
    header_day = int(header_day.split(" ")[0])
    Header.set(selected_city.upper())
    header_today.set(str(header_day) + " " + header_month)
    header_tomorrow.set(str(header_day + 1) + " " + header_month)
    header_day_after_tomorrow.set(str(header_day + 2) + " " + header_month)

    current_data_stringvar.set(current_data_text)
    today_data_stringVar.set(today_data_text)
    tomorrow_data_stringVar.set(tomorrow_data_text)
    day_after_tomorrow_stringVar.set(day_after_tomorrow_data_text)

def change_temp_mode():
    """
    Changes the temp mode from the settings file.
    Excepts if you directly try to change the temp mode
    """
    global temp_mode
    if temp_mode == "Celsius":
        temp_mode = "Fahrenheit"
        try:
            Main(selected_city)
        except:
            print("You did not select a city")

    else:
        temp_mode = "Celsius"
        try:
            Main(selected_city)
        except:
            print("You did not select a city")

    temp_mode_label['text'] = f"Current temperature mode: {temp_mode}"

#City List
data_getter = GatherData()
cities = data_getter.get_cities_url()
cities = list(cities)  # list of cities to be searched from the toggle list

#Frame,Title and Icon
root = tk.Tk()
root.geometry("1200x800")
icon = tk.PhotoImage(file='image_Icon.png')
root.iconphoto(True, icon)
root.title("WEATHER FORECASTING ")

# Header variable defination
global Header
Header = tk.StringVar()
global header_today
header_today = tk.StringVar()
global header_tomorrow
header_tomorrow = tk.StringVar()
global header_day_after_tomorrow
header_day_after_tomorrow = tk.StringVar()

# DROP BOX Frame
frame = ttk.Frame(root, padding="10") #Adds Little Frame
frame.grid()

# Global variable defination
global current_data_stringvar
current_data_stringvar = tk.StringVar()
global today_data_stringVar
today_data_stringVar = tk.StringVar()
global day_after_tomorrow_stringVar
day_after_tomorrow_stringVar = tk.StringVar()
global tomorrow_data_stringVar
tomorrow_data_stringVar = tk.StringVar()

#Combobox Defination
var = tk.StringVar()
combobox = ttk.Combobox(frame, textvariable=var) #Adds Dropbox into the frame
combobox['values'] = cities
combobox.grid()
combobox.bind('<KeyRelease>', check_input)


#Default City Info Writer (Calls Main function with default city)
if default_city != "":
    combobox.set(default_city)
    Main(default_city)

combobox.bind('<<ComboboxSelected>>', lambda event: Main()) #Calls main when city selected


# HEADER

Header_label = ttk.Label(root, textvariable=Header, font=("Arial", 25))
Header_label.place(relx=0.5, rely=0.1, anchor="center")

header_today_label = ttk.Label(root, textvariable=header_today, font=('Arial', 15))
header_today_label.place(relx=0.2, rely=0.65, anchor="center")

header_tomorrow_label = ttk.Label(root, textvariable=header_tomorrow, font=('Arial', 15))
header_tomorrow_label.place(relx=0.5, rely=0.65, anchor="center")

header_day_after_tomorrow_label = ttk.Label(root, textvariable=header_day_after_tomorrow, font=('Arial', 15))
header_day_after_tomorrow_label.place(relx=0.8, rely=0.65, anchor="center")

# Temp Mode
change_mode_button = ttk.Button(root, text="Change temperature mode",
                                command=change_temp_mode)  # Button Command Calls "change_temp_mode"
change_mode_button.place(relx=0.98, rely=0.02, anchor='ne')
temp_mode_label = ttk.Label(root, text=f"Current temperature mode: {temp_mode}")
temp_mode_label.place(relx=0.98, rely=0.07, anchor='ne')

# Save Settings
Settings_button = ttk.Button(root, text="Set Default Settings",
                             command=set_default_settings) # Button Command Calls "set_default_settings"
Settings_button.place(relx=0.98, rely=0.130, anchor='ne')

root.mainloop()
