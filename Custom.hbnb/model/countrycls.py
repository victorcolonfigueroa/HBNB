import uuid


class Country:
    def __init__(self, country_name, area_code):
        self.country_name = country_name
        self.area_code = area_code
        self.id = uuid.uuid4()

    def country_name(self, country_name):
        self.country_name = country_name
        print(f'The name of the country is {self.country_name}')

    def new_acode(self, new_acode):
        self.area_code = new_acode
        print(f'Your area code is {self.area_code}')

class City(Country):
    def __init__(self, name):
        self.city_name = name
        self.id = uuid.uuid4()

    def city_name(self, city_name):
        self.city_name = city_name
        print(f'Your city name is: {self.city_name}')
