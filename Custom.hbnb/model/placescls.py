from base_model import BaseModel
'''from persistence.data_manager import'''


class Places(BaseModel):
    def __init__(self, name, description, price, direction, user_id, creator):
        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.direction = direction
        self.user_id = user_id
        self.creator = creator

    def verify_user(self, user_id):
        if self.user_id == user_id:
            return True
        else:
            return False

    def new_place(self, new_place, user):
        if user != self.creator:
            raise PermissionError("Only the owner can change the place")
        self.name = new_place
        print(f'Your new place has been saved to {self.new_place}')

    def new_descrition(self, new_descrition, user):
        if user != self.creator:
            raise PermissionError ("Only the owner can edit this.")
        self.description = new_descrition
        print(f'Description: {self.description}')

    def new_price(self, new_price, user):
        if user != self.creator:
            raise PermissionError ("Only the owner can edit this.")
        if new_price <= 0:
            raise ValueError("price should have a greater value than 0")
        self.price = new_price
        print(f'This will be the new price {self.price}')

    def new_direction(self, new_direction, user):
        if user != self.creator:
            raise PermissionError ("Only the owner can edit this.")
        self.direction = new_direction
        print(f'This is how to get there: {self.direction}')

class Amenities(BaseModel):
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

    def new_amenity(self, new_amenity):
        self.name = new_amenity
        print(f'This is your new amenitie{self.name}')

    def new_description(self, new_desciption):
        self.description = new_desciption
        print(f'This is your amenities description: {self.decription}')

