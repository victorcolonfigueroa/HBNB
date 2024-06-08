from base_model import BaseModel
import uuid



class Reviews(BaseModel):
    def __init__(self, text, clasification, user):
        super().__init__()
        self.text = text
        self.clasification = clasification
        self.user = user
        self.id = uuid.uuid4()

    def new_review(self, new_review):
        self.text = new_review
        print(f'This is your new text {self.text}')

    def new_clasification(self, new_clasification):
        self.clasification = new_clasification
        print(f'The clasification is: {self.clasification}')
