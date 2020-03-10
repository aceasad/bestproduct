class Product:

    def __init__(self):
        self.product_name = ""
        self.product_url = ""
        self.brand_name = ""
        self.brand_url = ""
        self.product_image_url = ""
        self.product_price = ""
        self.product_id = ""
        self.source_website_url = ""

    # Setters

    def set_product_name(self, name):
        self.product_name = name

    def set_product_url(self, name):
        self.product_url = name

    def set_product_image_url(self, name):
        self.product_image_url = name

    def set_product_price(self, name):
        self.product_price = name

    def set_product_id(self, name):
        self.product_id = name

    def set_brand_name(self, name):
        self.brand_name = name

    def set_brand_url(self, name):
        self.brand_url = name

    def set_source_website_url(self, name):
        self.source_website_url = name

    # Getters

    def get_product_name(self):
        return self.product_name

    def get_product_url(self):
        return self.product_url

    def get_product_price(self):
        return self.product_price

    def get_product_image_url(self):
        return self.product_image_url

    def get_product_id(self):
        return self.product_id

    def get_brand_name(self):
        return self.brand_name

    def get_brand_url(self):
        return self.brand_url

    def get_source_website_url(self):
        return self.source_website_url
