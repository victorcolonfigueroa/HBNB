from models.base_model import BaseModel
from models.city import City

# List of valid ISO 3166-1 alpha-2 country codes
VALID_ISO_CODES = [
    "AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR", "AM", "AW", "AU",
    "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BQ",
    "BA", "BW", "BV", "BR", "IO", "BN", "BG", "BF", "BI", "CV", "KH", "CM", "CA", "KY",
    "CF", "TD", "CL", "CN", "CX", "CC", "CO", "KM", "CG", "CD", "CK", "CR", "CI", "HR",
    "CU", "CW", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "GQ", "ER", "EE",
    "SZ", "ET", "FK", "FO", "FJ", "FI", "FR", "GF", "PF", "TF", "GA", "GM", "GE", "DE",
    "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GG", "GN", "GW", "GY", "HT", "HM",
    "VA", "HN", "HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IM", "IL", "IT", "JM",
    "JP", "JE", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG", "LA", "LV", "LB", "LS",
    "LR", "LY", "LI", "LT", "LU", "MO", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ",
    "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM", "NA",
    "NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG", "NU", "NF", "MK", "MP", "NO", "OM",
    "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RO",
    "RU", "RW", "RE", "BL", "SH", "KN", "LC", "MF", "PM", "VC", "WS", "SM", "ST", "SA",
    "SN", "RS", "SC", "SL", "SG", "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES",
    "LK", "SD", "SR", "SJ", "SE", "CH", "SY", "TW", "TJ", "TZ", "TH", "TL", "TG", "TK",
    "TO", "TT", "TN", "TR", "TM", "TC", "TV", "UG", "UA", "AE", "GB", "US", "UM", "UY",
    "UZ", "VU", "VE", "VN", "VG", "VI", "WF", "EH", "YE", "ZM", "ZW"
]

class Country(BaseModel):
    """
    Represents a country with a name, ISO 3166-1 alpha-2 code, and list of cities.
    """
    def __init__(self, name, country_id, code, *args, **kwargs):
        """
        Initialize the Country with a name and ISO 3166-1 alpha-2 code.

        :param name: The name of the country
        :param code: The ISO 3166-1 alpha-2 code of the country
        :param args: Optional positional arguments
        :param kwargs: Optional keyword arguments
        """
        super().__init__(*args, **kwargs)
        if code not in VALID_ISO_CODES:
            raise ValueError(f"Invalid ISO 3166-1 alpha-2 code: {code}")
        self.name = name
        self.code = code
        self.cities = []
        self.save()

    def add_city(self, city):
        """
        Add a city to the country.

        :param city: The city to add
        """
        if isinstance(city, str):
            city = City.load(city)
        if city and city not in self.cities:
            self.cities.append(city)
            self.save()
            city.save()

    def to_dict(self):
        """
        Convert the Country to a dictionary.

        :return: The Country as a dictionary
        """
        data = super().to_dict()
        data.update({
            'name': self.name,
            'code': self.code,
            'cities': [city.to_dict() for city in self.cities if isinstance(city, City)]
        })
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Create a Country from a dictionary.

        :param data: The dictionary to create the Country from
        :return: The created Country
        """
        country = cls(
            name=data['name'],
            code=data['code'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
        country.cities = [City.from_dict(city) if isinstance(city, dict) else city for city in data.get('cities', [])]
        return country
