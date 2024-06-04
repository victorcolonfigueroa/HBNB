import uuid

class user:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.id = uuid.uuid4()
   
    def new_name(self, new_name):
        self.name = new_name
    print(f'New name has been saved as {self.name}')
   
    def new_email(self, new_email):
        self.email = new_email
    print(f'New email has been saved as {self.email}')
    
    def new_password(self, new_password):
        self.password = new_password
    print(f'New password has been saved')
    
class places:
    def __init__(self, name, description, price, direction):
        self.name = name
        self.description = description
        self.price = price
        self.direction = direction
        self.id = uuid.uuid4()
    
    def new_place(self, new_place):
        self.name = new_place
    print(f'Your new place has been saved to {self.place}')
    
    def new_descrition(self, new_descrition):
        self.description = new_descrition
    print(f'Description: {self.description}')
    
    def new_price(self, new_price):
        self.price = new_price
    print(f'This will be the new price {self.price}')
    
    def new_direction(self, new_direction):
        self.direction = new_direction
    print(f'This is how to get there: {self.direction}')
    
class country:
    def __init__(self, name, area_code):
        self.name = name
        self.area_code = area_code
        self.id = uuid.uuid4()
        
    def country_name(self, country_name):
        self.name = country_name
    print(f'The name of the country is {self.name}')
    
    def new_acode(self, new_acode):
        self.area_code = new_acode
    print(f'Your area code is {self.area_code}')

class city:
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()
    
    def city_name(self, city_name):
        self.name = city_name
    print(f'Your city name is: {self.name}')
    
class amenities:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.id = uuid.uuid4()
        
    def new_amenitie(self, new_amenitie):
        self.name = new_amenitie
    print(f'This is your new amenitie{self.name}')
    
    def new_description(self, new_desciption):
        self.description = new_desciption
    print(f'This is your amenities description: {self.decription}')
    
class reviews:
    def __init__(self, text, clasification):
        self.text = text
        self.clasification = clasification
        self.id = uuid.uuid4()
    
    def new_review(self, new_review):
        self.text = new_review
    print(f'This is your new text {self.text}')
    
    def new_clasification(self, new_clasification):
        self.clasification = new_clasification
    print(f'The clasification is: {self.clasification}')
