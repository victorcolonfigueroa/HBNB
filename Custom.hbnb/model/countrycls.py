from base_model import BaseModel
import pycountry #type: ignore


class Country(BaseModel):
    def __init__(self, country_name, area_code):
        super().__init__()
        self.country_name = country_name
        self.country_code = None

    def country_name(self, country_name):
        if country_name is None:
            raise ValueError("Please enter a Country.")
        self.country_name = country_name
        print(f'The name of the country is {self.country_name}')

    def set_country_code(self, country_code):
        if len(country_code) != 2 or not country_code.isalpha():
            raise ValueError("Invalid country code. It must be a 2-letter alpha code according to ISO 3166-1 alpha-2.")

        try:
            pycountry.countries.get(alpha_2=country_code.upper())
        except KeyError:
            raise ValueError("Invalid country code. It must be a valid ISO 3166-1 alpha-2 country code.")

        self.country_code = country_code.upper()
        print(f'The country code is {self.country_code}')

class City(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.city_name = name
        self.country_code = None

    def city_name(self, city_name):
        if city_name is None:
            raise ValueError("please provide a city")
        self.city_name = city_name
        print(f'Your city name is: {self.city_name}')

    def set_country_code(self):
        code = Country.self.country_code
        self.country_code = code
