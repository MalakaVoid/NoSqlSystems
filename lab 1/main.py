#Варианты 2, 5
import csv
import datetime
import random
from random import randint
from generation_data_import import get_names_list, get_random_string, get_random_long_string, get_random_date, get_random_long_text
from Classes import User, Review, Publication
import json

#------------FUNCTIONS FOR GENERATION FAKE DATA-----------------------
def generation_data():
    # MAIN ARRS
    users = []
    # HELPER ARRS
    names = get_names_list()
    statuses = ['approved', 'decliened']
    sexes = ['male', 'female']
    for i in range(0, 1000):
        reviews_arr = []
        publications_arr = []
        mail_arr = []
        for k in range(0, randint(2, 3)):  # for publications
            reviews_arr = []
            for j in range(0, randint(1, 2)):  # for reviews
                reviews_arr.append(Review(k,
                                          i,
                                          get_random_long_string()))
            publications_arr.append(Publication(k,
                                                i,
                                                get_random_string(),
                                                get_random_long_text(),
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
        tmp.insert(0, user.get_user_id_str())
        all_mail_csv_data.append(tmp)
        for publication in user.publications:
            all_publications_csv_data.append(publication.get_csv_list())
            for review in publication.reviews:
                all_reviews_csv_data.append(review.get_csv_list())

    f = open('users.csv', 'w', newline='')
    out = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    out.writerow(['id', 'name', 'mail', 'registration_date', 'status', 'publications', 'date_of_birth', 'sex'])
    out.writerows(all_users_csv_data)
    f.close()

    f = open('mail.csv', 'w',newline='')
    out = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    out.writerow(['id', 'mail'])
    out.writerows(all_mail_csv_data)
    f.close()

    f = open('publications.csv', 'w',newline='')
    out = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
    out.writerow(['pub_id', 'id', 'name', 'description', 'pages', 'category', 'date', 'reviews'])
    out.writerows(all_publications_csv_data)
    f.close()

    f = open('reviews.csv', 'w',newline='')
    out = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    out.writerow(['pub_id', 'id', 'text'])
    out.writerows(all_reviews_csv_data)
    f.close()
#---------------------------------END OF GENERATION FAKE DATA-------------------------------

def export_csv_to_json():
    #------Get all lists of data-----------
    list_user_fields = []
    list_publications_fields = []
    list_reviews_fields = []
    list_users = []
    list_publications = []
    list_reviews = []
    list_mails = []

    f = open('users.csv', newline='\n')
    csv_reader = csv.reader(f, delimiter=',')

    flag = True
    for row in csv_reader:
        if flag:
            list_user_fields = row
            flag = False
        else:
            list_users.append(row)
    f.close()

    f = open('mail.csv', newline='\n')
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        list_mails.append(row)
    f.close()

    f = open('publications.csv', newline='\n')
    csv_reader = csv.reader(f, delimiter=',')
    flag = True
    for row in csv_reader:
        if flag:
            list_publications_fields = row
            flag = False
        else:
            list_publications.append(row)
    f.close()

    f = open('reviews.csv', newline='\n')
    csv_reader = csv.reader(f, delimiter=',')
    flag = True
    for row in csv_reader:
        if flag:
            list_reviews_fields = row
            flag = False
        else:
            list_reviews.append(row)
    f.close()
    #------------------END--------------
    result_dict = {"users": []}
    dict_user = dict()

    for user_data in list_users:
        dict_user = dict()
        dict_publication = dict()
        dict_reviews = dict()

        for i in range(0, len(list_user_fields)):
            dict_user[list_user_fields[i]] = user_data[i]
        dict_user['publications'] = []
        dict_user['mail'] = []

        #-------------- TASK 2 ----------------
        birth_date = dict_user['date_of_birth'].split('-')
        date_of_birth = datetime.date(int(birth_date[0]), int(birth_date[1]), int(birth_date[2]))
        interval = datetime.date.today() - date_of_birth
        if interval.days < 5110:
            dict_user['younger_fourteen'] = True
        else:
            dict_user['younger_fourteen'] = False
        #-----------------------------------------

        for each in list_mails:
            if each[0] == user_data[0]:
                for i in range(1, len(each)):
                    dict_user['mail'].append(each[i])

        for publication in list_publications:
            dict_publication = dict()
            if publication[1] == user_data[0]:
                for i in range(len(list_publications_fields)):
                    dict_publication[list_publications_fields[i]] = publication[i]
                dict_publication['reviews'] = []
                for review in list_reviews:
                    dict_reviews = dict()
                    if review[0] == publication[0] and review[1] == user_data[0]:
                        for i in range(len(list_reviews_fields)):
                            dict_reviews[list_reviews_fields[i]] = review[i]
                        dict_publication['reviews'].append(dict_reviews)
                dict_user['publications'].append(dict_publication)

        result_dict['users'].append(dict_user)
        f = open("data.json", "w")
        json.dump(result_dict, f, indent=4)



#---------------- MAIN CODE------------------------
if __name__ == '__main__':
    #for each in generation_data():
    #    import_csv(generation_data())
    #export_csv_to_json()






