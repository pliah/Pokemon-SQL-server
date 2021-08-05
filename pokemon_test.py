import certifi
import queries
import urllib3

# This test is for first running only, otherwise change the assertion to 200
def test_get_pokemon_by_type():
    assert "eevee" in queries.find_by_type('normal')
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    res = http.request('GET', 'http://localhost:3000/update_types/eevee')
    assert res.status == 400

def test_get_pokemons_by_owner():
    assert queries.find_roster('Drasna') == ["wartortle", "caterpie", "beedrill", "arbok", "clefairy", "wigglytuff",
                                             "persian", "growlithe", "machamp", "golem", "dodrio", "hypno", "cubone",
                                             "eevee", "kabutops"]

def test_evolve_archies_spearow():
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    res = http.request('PATCH', 'http://localhost:3000/evolve_pokemon/spearow/Archie')
    assert res.status == 400

# This test is for first running only, otherwise change the assertion to 200
def test_evolve_whitneys_pikachu():
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    res = http.request('PATCH', 'http://localhost:3000/evolve_pokemon/pikachu/Whitney')
    assert res.status == 400

    queries.add_poke({"id": 193, "name": "yanma", 'height': 12, 'weight': 380})


def test_update_pokemon_types():
    queries.update_types('venusaur')
    assert 'venusaur' in queries.find_by_type('poison')
    assert 'venusaur' in queries.find_by_type('grass')


def test_get_owners():
    assert queries.find_owners('charmander')==["Giovanni", "Jasmine", "Whitney"]


# This test is for first running only, otherwise change the assertion to 400
def test_evolve_pokemon_1():
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    res = http.request('PATCH','http://localhost:3000/evolve_pokemon/pinsir/Whitney')
    assert res.status == 500

def test_evolve_pokemon_2():
    # first & second level
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    res1 = http.request('PATCH','http://localhost:3000/evolve_pokemon/oddish/Whitney')
    res2 = http.request('PATCH', 'http://localhost:3000/evolve_pokemon/oddish/Whitney')

    assert res1.status == 200
    # This test is for first running only.
    assert res2.status == 400
    # third level
    res3 = http.request('GET','http://localhost:3000/find_roster/Whitney')
    assert 'gloom' in str(res3.data)