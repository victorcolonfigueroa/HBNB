from base_model import BaseModel


class Country(BaseModel):
    def __init__(self, country_name, area_code):
        super().__init__()
        self.country_name = country_name
        self.area_code = area_code

    def country_name(self, country_name):
        if country_name is None:
            raise ValueError("Please enter a Country.")
        self.country_name = country_name
        print(f'The name of the country is {self.country_name}')

    def new_acode(self, new_acode):
        if isinstance(new_acode, int):
            raise ValueError("Area code has to be only numbers.")
        self.area_code = new_acode
        print(f'Your area code is {self.area_code}')

class City(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.city_name = name

    def city_name(self, city_name):
        if city_name is None:
            raise ValueError("please provide a city")
        self.city_name = city_name
        print(f'Your city name is: {self.city_name}')
