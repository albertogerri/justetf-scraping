import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.justetf.com/find-etf.html?'

#CLASSES per api
ASSETCLASS={
    'Azioni':'class-equity',
    'Obbligazioni':'class-bonds',
    'Metalli preziosi':'class-preciousMetals',
    'Materie prime':'class-commodities',
    'Criptovalute':'class-currency',
    'Immobiliare':'class-realEstate',
    'Mercato monetario':'class-moneyMarket'
}

ASSETCLASS_ENG={
    "Equity":     "class-equity",
    "Bonds":     "class-bonds",
    "Precious Metals":     "class-preciousMetals",
    "Commodities":     "class-commodities",
    "Cryptocurrencies":     "class-currency",
    "Real Estate":     "class-realEstate",
    "Money Market":     "class-moneyMarket",
}

#CATEGORIES per api
CATEGORIES_API={
    'Materia prima',
    'Paese',
    'Rating dell’obbligazione',
    'Regione',
    'Scadenza',
    'Segmento',
    'Settore',
    'Strategia azionaria',
    'Strategia obbligazionaria',
    'Tema',
    'Tipo di obbligazioni',
    'Valuta'}

#CATEGORIES per api
CATEGORIES_API_ENG={
    'Bond Rating':      'bondRating',
    'Bond Strategy':    'bondStrategy',
    'Bond Type':        'bondType',
    'Commodity':        'ctype',
    'Country':          'country', #
    'Currency':         'currency',
    'Equity Strategy':  'equityStrategy',
    'Maturity':         'bm',
    'Region':           'region', #
    'Sector':           'sector', 
    'Segment':          'cf',
    'Theme':            'theme'
    }

# SUBCATEGORIE per API
# CATEGORIES_API_ENG={



def get_categories (url: str, assetClass_var: str) -> dict:
    url_new=url+'assetClass='+ASSETCLASS_ENG[assetClass_var]
    response=requests.get(url_new)

    if response.status_code == 200:
        # Parsing del contenuto HTML della pagina
        soup = BeautifulSoup(response.text, 'html.parser')
        # Trova il div con class='search_menu'
        search_menu_ul = soup.find_all('ul', attrs={"class": "sidebar_filter"})
        # Controlla se il div è stato trovato
                # Crea un dizionario per memorizzare le categorie degli etf
        categories= {}
        if search_menu_ul:
            #prendiamo il primo elemento
            search_menu_ul=search_menu_ul[0]

            # Estrai tutti gli elementi <li> all'interno di ciascun <ul>
            li_elements = search_menu_ul.find_all('li')
            # Itera su tutti gli elementi <li>
            for li_element in li_elements:
            # Aggiungi la lista di elementi alla chiave corrispondente nel dizionario
                # categories_i=[subcat.split(' (')[0] for subcat in li_element.text.strip().split('\n')]
                categories_i=[]
                categories_i.append(li_element.text.strip().split(' (')[0])
                for option in li_element.find_all('option'):
                    
                    categories_i.append(option['value'])

                # if re.search('^[Tt]utt',categories_i[1])==None:
                #eng:
                if re.search('^[Aa]ll',categories_i[2])==None:
                    categories[categories_i[0]] = categories_i[2:]
                else:
                    categories[categories_i[0]] = categories_i[3:]
    return categories


def get_classes_categories(url:str)->dict:
    # Effettua la richiesta HTTP alla pagina web
    response = requests.get(url)
    # Crea un dizionario per memorizzare le classi degli etf
    classes= {}
    # Controlla se la richiesta ha avuto successo
    if response.status_code == 200:
        # Parsing del contenuto HTML della pagina
        soup = BeautifulSoup(response.text, 'html.parser')
        # Trova il div con class='search_menu'
        search_menu_div = soup.find_all('div', attrs={"class": "search_menu"})
        # Controlla se il div è stato trovato
        if search_menu_div:
            #prendiamo il secondo elemento
            search_menu_div=search_menu_div[1]
            # Trova tutti gli elementi <ul> all'interno del div 'search_menu' (ce n'è uno)
            ul_element = search_menu_div.find_all('ul')

            ##livello classi
            # Estrai tutti gli elementi <li> all'interno di ciascun <ul>
            li_elements = ul_element[0].find_all('li')
            # Crea una lista per memorizzare gli elementi della lista corrente
            class_items = []
            # Itera su tutti gli elementi <li>
            for li_element in li_elements:
                # Aggiungi il testo dell'elemento <li> alla lista
                class_items.append(li_element.text.strip())
            ## livello category e subcateogry 
            # itera su tutte le classi trovate e assegna categorie e subcategorie
            for class_item in class_items:
                if re.search('^[Aa]ll ',class_item)==None:
                    class_i=class_item.split(' (')[0]
                    classes[class_i]=get_categories(url,class_i)
            return classes
        else:
            print("Div con class='search_menu' non trovato.")
            return classes
    else:
        print(f"Errore: {response.status_code}")
        return classes

classes=get_classes_categories(url)