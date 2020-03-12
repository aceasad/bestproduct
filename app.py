import json, configparser
from flask import Flask, request
from ScrapeProducts import scrape_search_websites

app = Flask(__name__)

parser = configparser.ConfigParser()
parser.read("conf/config.ini")

def confParser(section):
    if not parser.has_section(section):
        print("No section information are available in config file for", section)
        return
    # Build dict
    tmp_dict = {}
    for option, value in parser.items(section):
        option = str(option)
        value = value.encode("utf-8")
        tmp_dict[option] = value
    return tmp_dict

websites_search_urls = confParser("websites_search_url")
base_urls = confParser("base_urls")
products_conf = confParser("products_conf")
details_conf = confParser("details_conf")
general_conf = confParser("general_conf")
min_products = general_conf["min_products"]
max_products = general_conf["max_products"]

@app.route('/search', methods=['GET'])
def get_product_searched():
    query = request.args.get("query")
    print("Search Request recieved for"+query)
    products_list = scrape_search_websites(query, websites_search_urls, min_products, max_products, base_urls, products_conf, details_conf)
    print("Search Result recieved for"+query)
    return json.dumps(products_list, indent=2, sort_keys=True)

@app.route('/')
def index():
    return "<h1>Welcome to Best Product API</h1>"    

if __name__=='__main__':
    app.run()
