from flask import Flask, Response, request, app
import json

import queries

app = Flask(__name__)

@app.route('/find_roster/<trainer_name>', methods=['GET'])
def find_roster(trainer_name):
    poke_names=queries.find_roster(trainer_name)
    return Response(json.dumps(poke_names))

@app.route('/add_poke', methods=['POST'])
def add_poke():
    pokemon=request.get_json()
    queries.add_poke(pokemon)
    return Response()
@app.route('/find_by_type/<type>', methods=['GET'])
def find_by_type(type):
    poke_names=queries.find_by_type(type)
    return Response(json.dumps(poke_names))

@app.route('/evolve_pokemon/<poke_name>/<poke_tranier>', methods=['PATCH'])
def evolve_pokemon(poke_name,poke_tranier):
     res=queries.evolve_pokemon(poke_name,poke_tranier)
     if res=="I am the last chain":
         return Response(res,status=500)
     if res == "No such an owner to that pokemon":
         return Response(res, status=400)
     return Response(res,status=200)

@app.route('/update_types/<poke_name>', methods=['GET'])
def update_type(poke_name):
    res = queries.update_types(poke_name)
    if res == "Can't re-add existing key":
        return Response(res, status=400)
    return Response(res, status=200)

if __name__ == '__main__':
    app.run(port=3000)