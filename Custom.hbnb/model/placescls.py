import uuid
'''fix the selfname variable'''

class Places:
    def __init__(self, name, description, price, direction):
        self.name = name
        self.description = description
        self.price = price
        self.direction = direction
        self.id = uuid.uuid4()
#review why its not recognizing the variables
    def new_place(self, new_place):
        self.name = new_place
        print(f'Your new place has been saved to {self.new_place}')

    def new_descrition(self, new_descrition):
        self.description = new_descrition
        print(f'Description: {self.description}')

    def new_price(self, new_price):
        self.price = new_price
        print(f'This will be the new price {self.price}')

    def new_direction(self, new_direction):
        self.direction = new_direction
        print(f'This is how to get there: {self.direction}')

class Amenities(Places):
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

