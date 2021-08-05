import json
import pymysql

poke_data = []
trainers = []
pokemons = []
types = []
owned_by = []


def read_json_file():
    global poke_data
    with open('pokemon_data.json') as file:
        poke_data = json.load(file)


def arrange_data():
    global trainers
    global types
    for i in poke_data:
        for j in i['ownedBy']:
            trainers.append((j['name'], j['town']))
        types.append((i['id'], i['type']))

    types = list(set(types))
    trainers = set(trainers)

    for i in poke_data:
        pokemons.append((i['id'], i['name'], i['height'], i['weight']))
        for j in i['ownedBy']:
            owned_by.append((i['id'], j['name'], j['town']))


def connect_to_database():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        db="sql_intro",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )
    if connection.open:
        print("the connection is opened")
        return connection


def insert_to_trainer(connection):
    for i in trainers:
        try:
            with connection.cursor() as cursor:
                query = 'INSERT into trainer(name, town) values' + str(i)
                cursor.execute(query)
                connection.commit()
        except:
            print("Error")


def insert_to_type(connection):
    for i in types:
        try:
            with connection.cursor() as cursor:
                query = 'INSERT into poke_type(id, type) values' + str(i)
                cursor.execute(query)
                connection.commit()
        except:
            print("Error")


def insert_to_pokemon(connection):
    for i in pokemons:
        try:
            with connection.cursor() as cursor:
                query = 'INSERT into pokemon values' + str(i)
                cursor.execute(query)
                connection.commit()
        except:
            print("Error")


def insert_to_owned_by(connection):
    for i in owned_by:
        try:
            with connection.cursor() as cursor:
                query = 'INSERT into owned_by values' + str(i)
                cursor.execute(query)
                connection.commit()
        except:
            print("Error")


if __name__ == '__main__':
    read_json_file()
    arrange_data()
    connection = connect_to_database()

    insert_to_trainer(connection)
    insert_to_type(connection)
    insert_to_pokemon(connection)
    insert_to_owned_by(connection)
