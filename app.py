import json, configparser
from flask import Flask, request
from datetime import datetime
from ScrapeProducts import scrape_search_websites
from forex_python.converter import CurrencyRates
from pandas import json_normalize
import pandas as pd
import re
import regex

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
#brand_conf = confParser("brand_conf")

general_conf = confParser("general_conf")
min_products = general_conf["min_products"]
max_products = general_conf["max_products"]

@app.route('/', methods=['GET'])
def index():
    return ("<h1> Best Product Scrapper API</h1>")

def only_numerics(seq):
    seq_type= type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))

def process_string(string_sample):
    result=""
    if("." in string_sample):
        str_l=string_sample.split(".")[0]
        str_r=string_sample.split(".")[1]
        str_f_l=only_numerics(str_l)
        str_f_r=only_numerics(str_r)
        result=str_f_l+"."+str_f_r            
    else:
        result=only_numerics(string_sample)
    return result

def sorted_products_list(product,keyword):
    df= json_normalize(product)
    pound_rate=4.68
    dollar_rate=3.76
    #print("Initial Shape: ",df.shape)
    indexTodrop=[]
    for index, row in df.iterrows():
        try:
            string_sample=row['price']
            if(string_sample.find("\u00a3")):
                string_sample=process_string(string_sample)
                price=float(string_sample)*pound_rate
                row['price']=price
            elif(string_sample.find("US$") or string_sample.find("$")):
                string_sample=process_string(string_sample)
                price=float(string_sample)*dollar_rate
                row['price']=price
            elif(string_sample.find("SAR")):
                string_sample=process_string(string_sample)
                row['price']=float(string_sample)
            else:
                result = regex.sub(r'[^\p{Latin}]', u'', string_sample)
                string_sample=process_string(result)
                row['price']=float(string_sample)
        except Exception as e:
            indexTodrop.append(index)

    df= df.drop(indexTodrop)
    keylist=[]
    if(len(keyword.split(" "))==1):
        keylist=[keyword.lower(),keyword.upper()]
    else:
        l=keyword.split(" ")
        for words in l:
            keylist.extend([words.lower(),words.upper()])

    if(len(keylist)==1):
        df=df[df['title'].str.contains(keyword.lower(), na = False)]
    else:
        frames=[]
        for words in keylist:
            frames.append(df[df['title'].str.contains(words, na = False)])
        df=pd.concat(frames)
        df.sort_values("title", inplace = True) 
        df.drop_duplicates(subset ="title",keep = False, inplace = True) 

    df=df.reindex(df.price.astype(float).sort_values().index)
    df = df[df.price > 0.0]
    return df.to_json(orient='records')


@app.route('/search', methods=['GET'])
def get_product_searched():
    start = datetime.now()
    query = request.args.get("query")
    #query = data["query"]
    products_list = scrape_search_websites(query, websites_search_urls, min_products, max_products, base_urls, products_conf, details_conf)
    end = datetime.now()
    diff = end - start
    print(str(diff.seconds) + " seconds")
    products_sorted=sorted_products_list(products_list,query)
    return products_sorted

if __name__=='__main__':
    app.run()
