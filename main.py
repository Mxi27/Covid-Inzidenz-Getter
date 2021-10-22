import requests, json
from string import Template

print("Bitte setzen sie für Landkreis ein LK vor ihren Landkreis, für Stadtkreis SK. Für Bundesländer einfach nur den Namen des Bundeslandes.")

def get_rs_id(landkreis):
    url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/rki_admunit_v/FeatureServer/0/query"
    lk_name = landkreis
    parameter = {
        'referer':'https://www.mywebapp.com',
        'user-agent':'python-requests/2.9.1',
        'where': '1=1',
        'outFields': '*',
        'returnGeometry': False,
        'f':'json',
        'cacheHint': True
    }
    result = requests.get(url=url, params=parameter)
    resultjson = json.loads(result.text)

    abfrage = resultjson["features"]
    Mittelwert = [k for k in abfrage if k["attributes"]["Name"]== lk_name]
    if Mittelwert == []:
        error = "Error"
        return error
    else:
        rs_id = Mittelwert[0]['attributes']['AdmUnitId']

    return rs_id

def get_cases7_per_100k(rs_id):
    url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/rki_key_data_v/FeatureServer/0/query?"
    lk_id = rs_id
    parameter = {
        'referer':'https://www.mywebapp.com',
        'user-agent':'python-requests/2.9.1',
        'where': f'AdmUnitId = {lk_id}',
        'outFields': '*', 
        'returnGeometry': False,
        'f':'json', 
        'cacheHint': True 
    }
    result = requests.get(url=url, params=parameter)
    resultjson = json.loads(result.text)
    inz7T = resultjson['features'][0]['attributes']['Inz7T']
    return inz7T

def run():
    k_name = input("Bitte geben sie den gewünschten Kreis ein:")
    lk_id =  get_rs_id(k_name)
    if lk_id == "Error":
        print("Fehler, der Kreis ist nicht bekannt")
    else:
        inz7T = get_cases7_per_100k(lk_id)
        print('Die Corona Inzidenz im', k_name, 'liegt bei ', inz7T, 'Fällen pro 100000 Einwohner')


while True:
    run()