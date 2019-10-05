class Store:
    
    def __init__(self):

        self.products = [
            {
                "productName":"Mars Pods",
                "similarItems": ['chocolate', 'mars', 'pods', 'mars pods'],
                "productPrice":4.99,
                "aisleNumber":5,
                "productStock":75
            },

            {
                "productName":"Pepsi",
                "similarItems": ['beverage', 'beverages', 'drink', 'pepsi', 'cola', 'soft drink'],
                "productPrice":3.99,
                "aisleNumber":3,
                "productStock":150
            },

            {
                "productName":"Apple",
                "similarItems": ['fruit', 'apple'],
                "productPrice":0.99,
                "aisleNumber":1,
                "productStock":200
            }
        ]

        self.availableItems = ['chocolate', 'beverages', 'fruit', 'beverages', 'pods', 'mars', 'mars pods' 'apple', 'pepsi', 'cola', 'soft drink', 'drink']

    def getItem(self, query):
        for item in self.products:
            if query in item['similarItems']:
                return item

    def conceptStringFormat(self):
        string = ''
        for item in self.availableItems:
            string += '"{0}" '.format(item)
        return string