class User:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.mail = []
        self.registration_date = ''
        self.status = ''
        self.publications = []
        self.date_of_birth = ''
        self.sex = ''
    def __init__(self, id, name, mail, registration_date, status, publications, date_of_birth, sex):
        self.id = id
        self.name = name
        self.mail = mail
        self.registration_date = registration_date
        self.status = status
        self.publications = publications
        self.date_of_birth = date_of_birth
        self.sex = sex
    def get_print(self):
        print(self.id)
        print(self.name)
        for each in self.mail:
            print(each, end=' ')
        print()
        print(self.registration_date)
        print(self.status)
        for each in self.publications:
            each.get_print()
        print(self.date_of_birth)
        print(self.sex)
    def get_csv_list(self):
        arr = [str(self.id), str(self.name), 'mail.csv', str(self.registration_date), str(self.status),
               'publications.csv', str(self.date_of_birth), str(self.sex)]
        return arr
    def get_mail_csv_list(self):
        arr = []
        for each in self.mail:
            arr.append(str(each))
    def get_user_id_str(self):
        return f'{self.id}'


class Publication:
    def __init__(self, id):
        self.id = id
        self.name = ''
        self.description = ''
        self.pages = 0
        self.category = ''
        self.date = ''
        self.rewiews = []
    def __init__(self, pub_id, id, name, description, pages, category, date, reviews):
        self.pub_id = pub_id
        self.id = id
        self.name = name
        self.description = description
        self.pages = pages
        self.category = category
        self.date = date
        self.reviews = reviews
    def get_print(self):
        print('\t', end='')
        print(self.id)
        print('\t', end='')
        print(self.name)
        print('\t', end='')
        print(self.description)
        print('\t', end='')
        print(self.pages)
        print('\t', end='')
        print(self.category)
        print('\t', end='')
        print(self.date)
        for each in self.reviews:
            each.get_print()
    def get_csv_list(self):
        arr = [str(self.pub_id),str(self.id), str(self.name), str(self.description), str(self.pages), str(self.category),
               str(self.date), str('reviews.csv')]
        return arr

class Review:
    def __init__(self, pub_id, id):
        self.pub_id = pub_id
        self.id = id
        self.text = ''
    def __init__(self, pub_id, id, text):
        self.pub_id = pub_id
        self.id = id
        self.text = text
    def get_print(self):
        print('\t\t', end='')
        print(self.id)
        print('\t\t', end='')
        print(self.text)
    def get_csv_list(self):
        arr = [str(self.pub_id), str(self.id), str(self.text)]
        return arr
