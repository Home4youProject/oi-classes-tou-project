class Profile:

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Admin(Profile):
    pass

class User(Profile):


    def __init__(self, username, password, email, phone_number, birth_date, name, surname, sex, languages, balance=0):
        super().__init__(username, password)
        self.email = email
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.name = name
        self.surname = surname
        self.balance = balance
        self.sex = sex
        self.languages = languages

class Owner(User):
    pass
