from bs4 import BeautifulSoup
import requests
from Product import Product


def get_html(url):
    _err = True
    cnt = 0
    page_obj = None
    while _err and cnt < 3:
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            r.encoding = "utf-8"
            page = r.text
            page_obj = BeautifulSoup(page, "lxml")
            _err = False
        except:
            page_obj = None
            _err = True
            cnt += 1

    return page_obj

def parse_websites(src, page_obj, min_products, max_products, base_url, cnf_prdct, cnf_dtl):
    all_products_list = []
    cnf_prdct_tmp = cnf_prdct.split("|")
    cnf_dtl_tmp = cnf_dtl.split("|")

    for x in range(0, len(cnf_prdct_tmp)):
        cnf_prdct_tmp[x] = cnf_prdct_tmp[x].split("=")
    #cnf_prdct_tmp[1] = cnf_prdct_tmp[1].split("=")

    for x in range(0, len(cnf_dtl_tmp)):
        cnf_dtl_tmp[x] = cnf_dtl_tmp[x].split("=")
    #cnf_dtl_tmp[1] = cnf_dtl_tmp[1].split("=")
    #cnf_dtl_tmp[2] = cnf_dtl_tmp[2].split("=")
    #cnf_dtl_tmp[3] = cnf_dtl_tmp[3].split("=")
    try:
        main_div = page_obj.findAll(cnf_prdct_tmp[0][0], attrs={cnf_prdct_tmp[0][1]:cnf_prdct_tmp[0][-1]})[0]
        if src == "strawberry":
            selector = cnf_prdct_tmp[1][0] +'['+ cnf_prdct_tmp[1][1]+'*='+cnf_prdct_tmp[1][-1]+']'
            product_list = main_div.select(selector)
        else:
            product_list = main_div.findAll(cnf_prdct_tmp[1][0], attrs={cnf_prdct_tmp[1][1]:cnf_prdct_tmp[1][-1]})
    except:
        product_list = []
    prdct_cntr = 0

    for prdct in product_list:
        try:
            product = dict()
            if cnf_dtl_tmp[0][0] == "img":
                try:
                    if src != "ounass":
                        img = prdct.find(cnf_dtl_tmp[0][0], attrs={cnf_dtl_tmp[0][1]:cnf_dtl_tmp[0][-1]}).attrs["src"]
                    else:
                        img = prdct.find(cnf_dtl_tmp[0][0], attrs={cnf_dtl_tmp[0][1]:cnf_dtl_tmp[0][-1]}).attrs["data-src"]
                except:
                    img = prdct.find(cnf_dtl_tmp[0][0], attrs={cnf_dtl_tmp[0][1]:cnf_dtl_tmp[0][-1]}).attrs["data-src"]
            else:
                try:
                    img = prdct.find(cnf_dtl_tmp[0][0], attrs={cnf_dtl_tmp[0][1]: cnf_dtl_tmp[0][-1]}).find("img").attrs["src"]
                except:
                    img = prdct.find(cnf_dtl_tmp[0][0], attrs={cnf_dtl_tmp[0][1]: cnf_dtl_tmp[0][-1]}).find("img").attrs["data-url"]
            title = prdct.find(cnf_dtl_tmp[1][0], attrs={cnf_dtl_tmp[1][1]:cnf_dtl_tmp[1][-1]}).text.replace("\n", "").strip()
            if cnf_dtl_tmp[2][0] == "a":
                prdct_link = prdct.find(cnf_dtl_tmp[2][0], attrs={cnf_dtl_tmp[2][1]:cnf_dtl_tmp[2][-1]}).attrs["href"]
            else:
                prdct_link = prdct.find(cnf_dtl_tmp[2][0], attrs={cnf_dtl_tmp[2][1]:cnf_dtl_tmp[2][-1]}).find("a").attrs["href"]

            if prdct_link.startswith('//'):
                prdct_link = "https:" + prdct_link
            if prdct_link.startswith('/'):
                prdct_link = base_url + prdct_link

            if img.startswith('//'):
                img = "https:" + img
            if img.startswith('/'):
                img = base_url + img
            price = prdct.find(cnf_dtl_tmp[3][0], attrs={cnf_dtl_tmp[3][1]:cnf_dtl_tmp[3][-1]}).text.replace("\n", "").strip()

            product["img_url"] = img
            product["title"] = title
            product["url"] = prdct_link
            product["price"] = price
            product["src_website"] = base_url
            all_products_list.append(product)
            prdct_cntr = prdct_cntr + 1
            if prdct_cntr >= max_products:
                break
        except Exception as e:
            print(e)
            pass
    if len(all_products_list) < min_products:
        all_products_list.clear()
    return all_products_list

def scrape_search_websites(query, websites_search_urls, min_products, max_products, base_urls, products_conf, details_conf):
    query = query.replace(" ", "+")
    list_all_products = []
    min_products = int(min_products.decode("utf-8"))
    max_products = int(max_products.decode("utf-8"))
    for src in websites_search_urls:
        search_url = websites_search_urls[src].decode("utf-8")
        base_url = base_urls[src].decode("utf-8")
        cnf_prdct = products_conf[src].decode("utf-8")
        cnf_dtl = details_conf[src].decode("utf-8")
        if src == "strawberry":
            tmp = search_url.split("|")
            search_url = tmp[0] + query + tmp[1] + query + tmp[-1]
        else:
            search_url = search_url + query
        page_obj = get_html(search_url)
        tmp_prdct_lst = parse_websites(src, page_obj, min_products, max_products, base_url, cnf_prdct, cnf_dtl)
        list_all_products.extend(tmp_prdct_lst)

    return list_all_products
