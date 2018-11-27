from metrics import get_metrics_by_endpoint, parse_metrics, write_metrics_file, write_normalized_metrics_file
from plot import plot
from os import path
from datetime import datetime
from autoencoder import get_train_test_dataset, get_autoencoder
from tensorflow.keras.models import load_model
from pandas import DataFrame
import traceback

APIKEYS = [
    {
        "apikey": "agrotama",
        "train": {
            "start": "2018-09-02",
            "end": "2018-10-28"
        }
    },
    {
        "apikey": "animale-vtex",
        "train": {
            "start": "2018-09-16",
            "end": "2018-10-28"
        }
    },
    {
        "apikey": "apoioentrega",
        "train": {
            "start": "2018-09-20",
            "end": "2018-10-28"
        }
    },
    {
        "apikey": "arredo-ar",
        "train": {
            "start": "2018-08-20",
            "end": "2018-09-20"
        }
    },
    {
        "apikey": "arredo-uy",
        "train": {
            "start": "2018-09-01",
            "end": "2018-10-15"
        }
    }
    # "arredo-uy",
    # "artex",
    # "asus",
    # "autoline",
    # "balaroti",
    # "bazarhorizonte-test",
    # "beautybox-saraiva",
    # "beautybox-vtex",
    # "bentostore",
    # "billabong",
    # "bluegardenia",
    # "bordabordadosenxovais",
    # "boticario",
    # "bradesco",
    # "brastemp",
    # "brutalkill",
    # "buscape",
    # "camicado",
    # "camicado-v7",
    # "cantodochef",
    # "carrefour",
    # "casaevideo",
    # "casasbahia",
    # "casashow",
    # "cea",
    # "cec",
    # "centauro-v5",
    # "chillibeans",
    # "cobasi",
    # "compracerta",
    # "comprafoodservice",
    # "compraunilever",
    # "compreipontuei",
    # "connectparts",
    # "consul",
    # "corello",
    # "cursoslivresead",
    # "cursoslivresead-teste",
    # "deliverysupermuffato",
    # "dentalcremer",
    # "dentalspeedgraph",
    # "dia",
    # "dressto",
    # "drogariaaraujo",
    # "drogariavenancio",
    # "dutramaquinas",
    # "dwz",
    # "dzarm",
    # "efacil",
    # "electrolux",
    # "element",
    # "elo7",
    # "emporiumbrazil",
    # "epocacosmeticos",
    # "eudora-vtex",
    # "extra",
    # "farmagora",
    # "farmrio",
    # "farmrio-vtex",
    # "fastshop-v6",
    # "ferramentaskennedy",
    # "futfanatics",
    # "gandhi",
    # "gaston",
    # "gcmgames",
    # "geelbe",
    # "hering-v5",
    # "heringkids",
    # "honeybe",
    # "imaginarium-vtex",
    # "ingressorapido",
    # "jeitocerto",
    # "jorgebischoff",
    # "jumbocol",
    # "karsten",
    # "kidsbrasil",
    # "kitchenaid",
    # "lebes",
    # "lfg",
    # "livrariascuritiba",
    # "lojadomecanico",
    # "lojaflamengo",
    # "lojaiplace",
    # "lojasmelissa",
    # "lojasrede",
    # "lojasrede-v7",
    # "lojasrenner",
    # "madeiramadeira",
    # "madeiramadeira_test",
    # "magazinedoinox",
    # "magazineluiza",
    # "malwee",
    # "mambo",
    # "marabraz",
    # "marisa",
    # "mmartan",
    # "mmm-v5",
    # "mobly-v5",
    # "movidaseminovos",
    # "mpbrinquedos",
    # "myft",
    # "natue",
    # "natura",
    # "natura-v6",
    # "netfarma-v6",
    # "netshoes-ar",
    # "netshoes-br",
    # "netshoes-mx",
    # "ns-allianzparque",
    # "ns-azaleia",
    # "ns-cazadosport",
    # "ns-chapecoense",
    # "ns-coritiba",
    # "ns-cruzeiro",
    # "ns-freelace",
    # "ns-gigantedacolina",
    # "ns-internacional",
    # "ns-kappa",
    # "ns-lojanba",
    # "ns-olympikus",
    # "ns-puma",
    # "ns-santosshop",
    # "ns-santosstore",
    # "ns-saopaulomania",
    # "ns-shoestock",
    # "ns-shoptimao",
    # "ns-soycuervo",
    # "ns-tiendachivas",
    # "ns-tiendacruzazulonline",
    # "ns-tiendaoficialamerica",
    # "ns-tiendapumas",
    # "ns-zattini",
    # "offcorss",
    # "offpremium",
    # "offpremium-vtex",
    # "onofrefarma-v6",
    # "oppa-v5",
    # "oppa-v6",
    # "oqvestir",
    # "outletespacociahering",
    # "padovani",
    # "palaciodasferramentas",
    # "panvel-v5",
    # "paqueta",
    # "paquetaesportes",
    # "parceiroambev",
    # "pariscl",
    # "petz",
    # "polishop",
    # "polishop-vc",
    # "pontofrio",
    # "portaleducacao",
    # "portaleducacao-vtex",
    # "portalpos",
    # "prospin",
    # "pucwebstore",
    # "qab2cerp",
    # "qdb",
    # "qdb-vtex",
    # "renner-teste",
    # "rihappy",
    # "ripcurl",
    # "rrmaquinas",
    # "rvca",
    # "salcobrand",
    # "santistadecora",
    # "saraiva-v5",
    # "savegnago",
    # "sephora",
    # "sephora-v6",
    # "shopfacil",
    # "shopfisio",
    # "shopmelissa-eu",
    # "shopmelissa-it",
    # "shopmelissa-uk",
    # "shopmelissa-us",
    # "sondadelivery",
    # "sonoma",
    # "sportline",
    # "studiozcalcados",
    # "tannino",
    # "taqi",
    # "telhanorte",
    # "tenda",
    # "tiendasjumbofood",
    # "tng",
    # "tokstok",
    # "tudoforte",
    # "umbrale-cl",
    # "undefined",
    # "unicpharma",
    # "upfy",
    # "velez",
    # "vivara",
    # "webcontinental",
    # "webmotors",
    # "youcom",
    # "zonacriativa",
    # "zonasulatende"
]

ENDPOINTS = [
    "/raas/v2/pageview",
    "/raas/v2/cartview",
    "/raas/v2/search",
    "/raas/v2/views",
    "/raas/v2/transactions"
]

START = 1532646933
END = 1540422933
GRAFANA_SESSION = "fa2b89fe41eda196"

X_train = DataFrame()
X_test = DataFrame()

for client in APIKEYS:
    try:
        features = []
        values = {}
        days = (datetime.fromtimestamp(END) - datetime.fromtimestamp(START)).days
        apikey = client["apikey"]
        apikey_data_file = "metrics/raw/{apikey}_{days}d.csv".format(apikey=apikey, days=days)
        apikey_normalized_data_file = "metrics/normalized/{apikey}_{days}d.csv".format(apikey=apikey, days=days)
        apikey_figure_file = "figures/raw/{apikey}_{days}d.png".format(apikey=apikey, days=days)
        apikey_normalized_figure_file = "figures/normalized/{apikey}_{days}d.png".format(apikey=apikey, days=days)
        print("Processing \"{apikey}\"...".format(apikey=apikey))

        if not path.isfile(apikey_data_file):
            for endpoint in ENDPOINTS:
                parse_metrics(get_metrics_by_endpoint(GRAFANA_SESSION, apikey, endpoint, START, END), features, values)
            write_metrics_file(apikey_data_file, features, values)

        write_normalized_metrics_file(apikey_data_file, apikey_normalized_data_file, 50)
        train, test = get_train_test_dataset(apikey_normalized_data_file, client)
        
        X_train = X_train.append(train)
        X_test = X_test.append(test)

        # plot(apikey, apikey_data_file, apikey_figure_file)
        # plot(apikey, apikey_normalized_data_file, apikey_normalized_figure_file)

    except Exception as e:
        traceback.print_exc()

try:
    autoencoder = load_model('autoencoder.h5')
except Exception as ex:
    autoencoder = get_autoencoder(X_train.shape[1])
    print(X_train.shape)
    autoencoder.fit(X_train.values, X_train.values, epochs = 500, batch_size = 32, shuffle = False, validation_data=(X_test.values, X_test.values)) 
    reconstructed_values = autoencoder.predict(test.values)
    print(reconstructed_values)
    autoencoder.save('autoencoder.h5') 