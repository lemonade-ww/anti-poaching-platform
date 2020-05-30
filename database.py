import json
import pymysql


db = pymysql.connect("localhost", "root",
                     "ANTIPOACHINGplatform", "anti_poaching_platform")

cursor = db.cursor()

# cursor.execute("SHOW TABLES;")
# data = cursor.fetchone()

sql = '''CREATE TABLE DATA (
    NUMBER VARCHAR(50),
    LOCATION VARCHAR(50),
    TITLE VARCHAR(255),
    DEFENDANT VARCHAR(50),
    DEFENDANT_INFO TEXT,
    SPECIES_INFO TEXT,
    SENTENCE TEXT);'''

cursor.execute(sql)


with open('./opt.json', 'r') as file:
    data = json.load(file)

# i = 0
for item in data:
    info = data[item]
    if not info:
        continue

    number = info['number']
    location = info['location']
    title = info['title']
    defendant = str(info['defendant'])
    defendant_info = str(info['defendant_info'])
    species_info = str(info['species_info'])
    sentence = str(info['sentence'])

    sql = 'INSERT INTO DATA (NUMBER, LOCATION, TITLE, DEFENDANT, DEFENDANT_INFO, SPECIES_INFO, SENTENCE) VALUES (\"' + \
        number + '\", \"' + location + '\", \"' + title + '\", \"' + defendant + '\", \"' + \
        defendant_info + '\", \"' + species_info + '\", \"' + sentence + '\");'

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    # i += 1

# print(i)

db.close()
