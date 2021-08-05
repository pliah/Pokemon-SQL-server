import pymysql
import requests as requests


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


connection = connect_to_database()


def find_by_type(type):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id from poke_type where TYPE='{type}'")
            type_id = cursor.fetchall()
            print(type_id)
            poke_names = []
            for i in type_id:
                cursor.execute(f"SELECT name from pokemon where id='{i['id']}'")
                sol = cursor.fetchall()
                for i in sol:
                    poke_names.append(i["name"])
            return poke_names
    except:
        print("Error")


def find_roster(trainer_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT name FROM pokemon where id IN\
            (SELECT id FROM owned_by where name ='{trainer_name}')")
            sol = cursor.fetchall()
            poke_names = []
            for i in sol:
                poke_names.append(i["name"])
            return poke_names
    except:
        print("Error")


def finds_most_owned():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM " \
                           " (SELECT id, COUNT(*) as a FROM owned_by  " \
                           " GROUP BY id) as new JOIN pokemon" \
                           " on new.id = pokemon.id " \
                           " WHERE a >= ALL(" \
                           " SELECT COUNT(*) as a" \
                           " FROM owned_by" \
                           " GROUP BY owned_by.id)")
            sol = cursor.fetchall()
            names = []
            for i in sol:
                names.append(i['name'])
            return names
    except:
        print("Error")


def add_poke(pokemon):
    print(pokemon)
    id = pokemon['id']
    name = pokemon['name']
    height = pokemon['height']
    weight = pokemon['weight']
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO pokemon VALUES" + str((id, str(name), height, weight))
            cursor.execute(query)
            connection.commit()
            update_types(name)
    except pymysql.err.IntegrityError:
        print("pokemon is already exist")


def get_id(poke_name):
    try:
        with connection.cursor() as cursor:
            query = f"SELECT id FROM pokemon WHERE name = '{poke_name}'"
            cursor.execute(query)
            poke_id = cursor.fetchone()['id']
        print(poke_id)
        if poke_id is None:
            return None
        return poke_id
    except TypeError:
        print("ID ERROR")


def update_owned_by(new_poke, old_poke, trainer):
    try:
        with connection.cursor() as cursor:
            query = f"UPDATE owned_by SET id = '{new_poke}' WHERE id = {old_poke} AND name = '{trainer}'"
            print(query)
            cursor.execute(query)
        connection.commit()

    except:
       print("Error in update")


def update_types(poke_name):
    r = requests.get(
        'https://pokeapi.co/api/v2/pokemon/' + poke_name, verify=False)
    types = r.json()['types']
    poke_id = get_id(poke_name)
    for i in types:
        try:
            with connection.cursor() as cursor:
                query = f"INSERT INTO poke_type VALUES{poke_id, i['type']['name']}"
                cursor.execute(query)
                connection.commit()
        except pymysql.err.IntegrityError:
            print("already exist")


def is_exist(name):
    if get_id(name) is not None:
        return True
    return False

def find_owners(pokemon_name):
    try:
        with connection.cursor() as cursor:
            query = f"SELECT name FROM owned_by WHERE owned_by.id IN(" \
                    f"SELECT pokemon.id FROM pokemon WHERE name = '{pokemon_name}')"
            cursor.execute(query)
            rows = cursor.fetchall()
            ans = []
            for row in rows:
                ans.append(f'{row["name"]}')
            return ans
    except:
        print("Error")

def create_poke(poke_id, poke_name, old_poke, trainer):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_name}/", verify=False)
    height = r.json()["height"]
    weight = r.json()["weight"]
    update_types(poke_name)
    add_poke({"id": poke_id, "name": poke_name, "height": height, "weight": weight})
    update_owned_by(poke_name, old_poke, trainer)

def evolve_pokemon(poke_name, poke_tranier):
    owners = find_owners(poke_name)
    print('owe',owners)
    if poke_tranier not in owners :
        return "No such an owner to that pokemon"
    poke_url = "https://pokeapi.co/api/v2/pokemon/" + poke_name
    r = requests.get(poke_url, verify=False)
    poke_species_url = r.json()['species']['url']
    s = requests.get(poke_species_url, verify=False)
    evolve_info_url = s.json()['evolution_chain']['url']
    t = requests.get(evolve_info_url, verify=False)
    chain_evolves_to_info = t.json()['chain']['evolves_to']
    if chain_evolves_to_info != []:
        evolve_name = chain_evolves_to_info[0]['species']['name']
        evolve_url = chain_evolves_to_info[0]['species']['url']
        evolve_id = evolve_url.split('/')[-2]
        if is_exist(evolve_name):
            update_owned_by(evolve_id, get_id(poke_name), poke_tranier)
        else:
            create_poke(evolve_id, evolve_name, get_id(poke_name),poke_tranier)
        return 'Successfully advanced in the evolutionary chain'
    else:
        return 'I am the last chain'




