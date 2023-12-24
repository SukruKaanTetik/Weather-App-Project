# Emirhan Toprak 
# Hasan Efe Dinç
# Şükrü Kaan Tetik 

from gather_data import GatherData
import tkinter
from PIL import Image, ImageTk



class StoreWeather:


    def __init__(self, city):
        self.city = city


    def __convert_current_data_str(self):
        """
        converts the dict data for current weather info to string
        to be written in text file
        :return: the string version of the data
        """

        data_getter = GatherData()
        data_getter.set_city(self.city)
        data_dict = data_getter.current_data()
        data_str = ""

        for key in data_dict:
            data_str += f"{key}: {data_dict[key]}\n"

        return data_str


    def __convert_daily_data_str(self):
        """
        converts the dict data for current weather info to string
        to be written in text file
        :return: the string version of the data
        """

        data_getter = GatherData()
        data_getter.set_city(self.city)

        data_dict = data_getter.daily_data()
        data_str = ""
        for day in data_dict:
            data_str += f"\n{day.upper()}\n"
            for key in data_dict[day]:
                data_str += f"{key}: {data_dict[day][key]}\n"

        return data_str



    def __convert_text_to_dict_current(self, read_list):
        data_dict = {}

        for i in range(5):
            line = read_list[i].split(": ")[0]
            line_data = read_list[i].split(": ")[1].split("\n")[0]
            data_dict[line] = line_data

        return data_dict

    def __convert_text_to_dict_today(self, read_list):
        data_dict = {}

        for i in range(7, 13):
            line = read_list[i].split(": ")[0]
            line_data = read_list[i].split(": ")[1].split("\n")[0]
            data_dict[line] = line_data

        return data_dict

    def __convert_text_to_dict_tomorrow(self, read_list):
        data_dict = {}

        for i in range(15, 21):
            splitted = read_list[i].split(": ")
            line = splitted[0]
            line_data = splitted[1].split("\n")[0]
            data_dict[line] = line_data

        return data_dict


    def __convert_text_to_dict_day_after_tomorrow(self, read_list):
        data_dict = {}

        for i in range(23, 29):
            splitted = read_list[i].split(": ")
            line = splitted[0]
            line_data = splitted[1].split("\n")[0]

            data_dict[line] = line_data
        return data_dict


    def convert_text_to_dict(self):
        """
        Converts the text information from the data to a dictionary to be displayed and used
        :return: dictionary that hold the data from the weather text
        """
        file = open('weather.txt', 'r', encoding='utf-8')
        read_list = file.readlines()

        data_dict = {
            "Current": self.__convert_text_to_dict_current(read_list),
            "Today": self.__convert_text_to_dict_today(read_list),
            "Tomorrow": self.__convert_text_to_dict_tomorrow(read_list),
            "Day After Tomorrow": self.__convert_text_to_dict_day_after_tomorrow(read_list)
        }

        return data_dict

    def write_current_info(self):
        """
        opens and writes the current data information to text file
        """
        file = open('weather.txt', 'w', encoding='utf-8')
        file.writelines(self.__convert_current_data_str())
        file.close()


    def write_daily_info(self):
        """
        opens and appends the current data information to the text file
        """

        file = open('weather.txt', 'a', encoding='utf-8')
        file.writelines(self.__convert_daily_data_str())
        file.close()



    def choose_picture_current(self):
        """
        Creates a PhotoImage and passes relevant image file
        considering the condition data of the weather
        :return: image object created
        """
        dict = self.convert_text_to_dict()
        weather = dict["Current"]["Condition"]
        weather = weather.lower()

        if "snow" in weather:
            image = tkinter.PhotoImage(file='image_Snowy.png')
        elif "sun" in weather or "Sunny" in weather:
            image = tkinter.PhotoImage(file='image_Sunny.png')

        elif "thunderstorms" in weather or "tstorms" in weather or "thundershowers" in weather:
            image =tkinter.PhotoImage(file='image_Thunder.png')
        elif "cloudy" in weather or "cloud" in weather or "overcast" in weather:
            image = tkinter.PhotoImage(file='image_Cloud.png')
        else:
            image = tkinter.PhotoImage(file='image_Rainy.png')

        return image


    def choose_image_main_daily(self, day_info):
        """
        :param day_info: "Today / Tomorrow / Day After Tomorrow"
        returns an edited image for the daily information considering
        the condition data for each three parameter
        :return:
        """
        dict = self.convert_text_to_dict()
        weather = dict[day_info]["Condition"]
        weather = weather.lower()
        y = 75

        if "snow" in weather:
            image = Image.open('image_Snowy.png')
        elif "sun" in weather or "Sunny" in weather:
            image = Image.open('image_Sunny.png')
            y = 100
        elif "thunderstorms" in weather or "tstorms" in weather or "thundershowers" in weather:
            image = Image.open('image_Thunder.png')
            y = 80
        elif "cloudy" in weather or "cloud" in weather or "overcast" in weather:
            image = Image.open('image_Cloud.png')
            y = 70
        else:
            image = Image.open('image_Rainy.png')


        image = image.resize((100, y))
        image = ImageTk.PhotoImage(image)
        return image






# to store the user preferences and window settings
class StoreSetting:

    def write_user_preferences(self, city="", tempertaure_scale="Celsius"):
        try:
            file = open('settings.txt', 'w', encoding='utf-8')
            prefereneces_txt = f"City: {city} \n" \
                               f"Scale: {tempertaure_scale} "
            file.writelines(prefereneces_txt)

        except FileExistsError:
            print("Error opening file")
        finally:
            file.close()


    def convert_setting_to_dict(self):
        try:
            file = open('settings.txt', 'r', encoding='utf-8')
            lines = list(file.readlines())
            city = lines[0].split(": ")[1].split("\n")[0].strip()
            scale = lines[1].split(": ")[1].strip()

            dict = {
                "City": city,
                "Scale": scale
            }

            return dict

        except FileNotFoundError:
            print("Error opening file")

        finally:
            file.close()
