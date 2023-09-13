#Варианты 2, 7
import csv
import random
from random import randint
from generation_data_import import get_names_list, get_random_string, get_random_long_string, get_random_date
from Classes import User, Review, Publication
import json

#------------FUNCTIONS FOR GENERATION FAKE DATA-----------------------
def generation_data():
    # MAIN ARRS
    users = []
    # HELPER ARRS
    names = get_names_list()
    statuses = ['approved', 'waiting', 'decliened']
    sexes = ['male', 'female']
    for i in range(0, 4):
        reviews_arr = []
        publications_arr = []
        mail_arr = []
        for k in range(0, randint(2, 3)):  # for publications
            reviews_arr = []
            for j in range(0, randint(1, 2)):  # for reviews
                reviews_arr.append(Review(i,
                                          get_random_long_string()))
            publications_arr.append(Publication(i,
                                                get_random_string(),
                                                get_random_long_string(),
                                                randint(5,100),
                                                get_random_string(),
                                                get_random_date(),
                                                reviews_arr))
        for l in range(2, 4):
            mail_arr.append(f'{get_random_string()}@mail.ru')
        users.append(User(i,
                          names[randint(0, len(names)-1)],
                          mail_arr,
                          get_random_date(),
                          statuses[randint(0, len(statuses)-1)],
                          publications_arr,
                          get_random_date(),
                          sexes[randint(0, len(sexes)-1)]))
    return users

def import_csv(users):
    all_users_csv_data = []
    all_mail_csv_data = []
    all_publications_csv_data = []
    all_reviews_csv_data = []
    for user in users:
        all_users_csv_data.append(user.get_csv_list())
        tmp = user.mail
        tmp.insert(0,user.get_user_id_str())
        all_mail_csv_data.append(tmp)
        for publication in user.publications:
            all_publications_csv_data.append(publication.get_csv_list())
            for review in publication.reviews:
                all_reviews_csv_data.append(review.get_csv_list())
    f = open('users.csv', 'w')
    out = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    out.writerow(['id', 'name', 'mail', 'registration_date', 'status', 'publications', 'date_of_birth', 'sex'])
    out.writerows(all_users_csv_data)
    f.close()
    f = open('mail.csv', 'w')
    out = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    out.writerow(['id', 'mail'])
    out.writerows(all_mail_csv_data)
    f.close()
    f = open('publications.csv', 'w')
    out = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    out.writerow(['id', 'name', 'description', 'pages', 'category', 'date', 'reviews'])
    out.writerows(all_publications_csv_data)
    f.close()
    f = open('reviews.csv', 'w')
    out = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    out.writerow(['id', 'text'])
    out.writerows(all_reviews_csv_data)
    f.close()
#---------------------------------END OF GENERATION FAKE DATA-------------------------------

def export_csv_to_json():
    f = open('users.csv', newline='\n')
    csv_reader = csv.reader(f, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
        else:
            print(row)
        line_count+=1
        print(line_count)



#---------------- MAIN CODE------------------------
if __name__ == '__main__':
    #for each in generation_data():
        #import_csv(generation_data())
    export_csv_to_json()





