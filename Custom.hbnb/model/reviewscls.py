import uuid


class Reviews:
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
