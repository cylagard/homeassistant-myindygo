# pip3 install requests beautifulsoup4
from bs4 import BeautifulSoup
import requests


class MyIndygoClient:
    """A default class to manage MyIndygo data."""

    def __init__(self) -> None:
        """Initialize the MyIndygoClient with email and password."""
        self.login_url = "https://myindygo.com/login"
        self.devices_url = "https://myindygo.com"
        self.session = requests.Session()
        self.sensorsList = []

    def authenticate(self, email: str, password: str) -> bool:
        self.email = email
        self.password = password
        """Authenticate the user with the provided email and password."""
        # the payload with your login credentials
        payload = {
            "email": self.email,
            "password": self.password,
            "rememberMe": "on",
        }
        loginResponse = self.session.post(self.login_url, data=payload, timeout=30)
        soup = BeautifulSoup(loginResponse.text, "html.parser")
        # find proper url for list of devices
        menuItems = soup.find_all(class_="menu_nav")
        if len(menuItems) == 1:
            self.devices_url = (
                self.devices_url + menuItems[0].find("a").get("href") + "/devices"
            )
        if loginResponse.status_code == 200:
            return True
        return False

    def updateSensors(self):
        """Update the list of sensors with their type, value, and time."""
        self.sensorsList.clear()
        # query url of the devices to get the data
        deviceResponse = self.session.get(self.devices_url, timeout=15)
        soup = BeautifulSoup(deviceResponse.text, "html.parser")

        # list all sensors type and value
        listSensors = soup.find_all(class_="box-sensor")
        for sensor in listSensors:
            data = {
                "Sensor type": sensor.find(class_="title-sensor").text.strip(),
                "Sensor value": sensor.find(class_="value-sensor").text.strip(),
                "Time sensor": sensor.find(class_="time-sensor").text.strip(),
            }
            self.sensorsList.append(data)
        print(self.sensorsList)
        return self.sensorsList


# print the result page title
# print(f"Page title: {page_title}")
