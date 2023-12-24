# Emirhan Toprak 20210601060
# Hasan Efe Dinç 20200601110
# Şükrü Kaan Tetik 20200601052


import requests
from bs4 import BeautifulSoup


class GatherData:

    __chosen_city = ""
    __html_text = None
    __soup = None

    # time and date forecast website link to be attached from the "cities_url"
    __url = "https://www.timeanddate.com/weather/"


    def check_internet(self):
        url = "https://www.timeanddate.com/weather/"
        timeout = 5

        try:
            _ = requests.get(url, timeout=timeout)
            print("Internet Connection is working")

        except requests.ConnectionError:
            print("Internet connection is not available.")






    # private url attachments for different cities
    __cities_url = {
        "Adana": "turkey/adana",
        "Amasya": "turkey/amasya",
        "Ankara": "turkey/ankara",
        "Antalya": "turkey/antalya",
        "Batman": "turkey/batman",
        "Bursa": "turkey/bursa",
        "Çanakkale": "turkey/canakkale",
        "Denizli": "turkey/denizli",
        "Diyarbakır": "turkey/diyarbakir",
        "Erzurum": "turkey/erzurum",
        "Eskişehir": "turkey/eskisehir",
        "Gaziantep": "turkey/gaziantep",
        "Istanbul": "turkey/istanbul",
        "Izmir": "turkey/izmir",
        "Kahramanmaraş": "turkey/kahramanmaras",
        "Kayseri": "turkey/kayseri",
        "Kocaeli": "turkey/izmit",
        "Konya": "turkey/konya",
        "Malatya": "turkey/malatya",
        "Samsun": "turkey/samsun",
        "Trabzon": "turkey/trabzon",
    }

    def get_cities_url(self):
        return self.__cities_url


    def set_city(self, city):
        self.__chosen_city = city


    def __start_procedure_current(self):
        """
        Sets the url for the current forecast report considering city selected
        Request info and create new Beautiful Object to parse
        """

        add = self.__cities_url[self.__chosen_city]
        url = self.__url + add

        self.__html_text = requests.get(url).text
        self.__soup = BeautifulSoup(self.__html_text, 'lxml')



    def __start_procedure_daily(self):
        """
        Sets the url for the daily forecast report considering city selected
        Request info and create new Beautiful Object to parse
        """
        add = self.__cities_url[self.__chosen_city] + "/ext"
        url = self.__url + add

        self.__html_text = requests.get(url).text
        self.__soup = BeautifulSoup(self.__html_text, 'lxml')


    def __data_today(self, conditions):
        """
        :param conditions: list of the data part for daily forecasting report
        :return: data gathered in dictionary form
        """
        today_data_dict = {
            "Temperature": conditions[1].text,
            "Condition": conditions[2].text,
            "Wind Speed": conditions[4].text,
            "Humidity": conditions[6].text,
            "Sunrise": conditions[10].text,
            "Sunset": conditions[11].text
        }


        return today_data_dict


    def __data_tomorrow(self, conditions):
        """
        :param conditions: list of the data part for daily forecasting report
        :return: data gathered in dictionary form
        """

        tomorrow_data_dict = {
            "Temperature": conditions[13].text,
            "Condition": conditions[14].text,
            "Wind Speed": conditions[16].text,
            "Humidity": conditions[18].text,
            "Sunrise": conditions[22].text,
            "Sunset": conditions[23].text
        }
        return tomorrow_data_dict


    def __data_day_after_tomorrow(self, conditions):
        """
        :param conditions: list of the data part for daily forecasting report
        :return: data gathered in dictionary form
        """
        day_after_dict = {
            "Temperature": conditions[25].text,
            "Condition": conditions[26].text,
            "Wind Speed": conditions[28].text,
            "Humidity": conditions[30].text,
            "Sunrise": conditions[34].text,
            "Sunset": conditions[35].text
        }
        return day_after_dict



    def daily_data(self):
        """
        starts the procedure for getting information from daily forecasting page
        then calls the function that are defined by three days of data separately
        :return: returns all the data comes from the methods
        """

        self.__start_procedure_daily()
        conditions = list(self.__soup.findAll('td'))

        daily_data_dict = {
            "Today": self.__data_today(conditions=conditions),
            "Tomorrow: ": self.__data_tomorrow(conditions=conditions),
            "Day After Tomorrow: ": self.__data_day_after_tomorrow(conditions=conditions)
        }

        return daily_data_dict


    def current_data(self):
        """
        gets all the necessary information from the html text for the current forecasting report
        :return: all data gathered in dictionary form
        """

        self.__start_procedure_current()
        temperature = self.__soup.find('div', class_='h2').text
        conditions = self.__soup.find_all('p')
        condition = conditions[0].text.split(".")
        feels_like_list = conditions[1].text.split("Wind: ")
        feels_like = feels_like_list[0].split("Forecast")
        feels_like = feels_like[0]

        location_hour = list(self.__soup.find_all('td'))

        current_data_dict = {
            "Temperature": temperature,
            "Condition": condition[0],
            "Feels Like": feels_like[12:],
            "Wind Speed": feels_like_list[1][:7] + feels_like_list[1][9:],
            "Latest Update": location_hour[2].text
        }
        return current_data_dict