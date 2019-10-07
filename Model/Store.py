import json, os
class Store:
    
    def __init__(self):

        self.users_path = os.getcwd() + '/Model/data/users.json'
        self.knownUsers = self.loadJSON()
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

        self.availableItems = ['chocolate', 'beverages', 'fruit', 'beverages', 'pods', 'mars', 'mars pods', 'apple', 'pepsi', 'cola', 'soft drink', 'drink']

    def loadJSON(self):
        with open(self.users_path, 'r') as f:
            try:
                return json.load(f)
            except IOError as err:
                print('err: {0}'.format(err))
                return False

    def saveUser(self, user, features):
        if os.path.exists(self.users_path):
            with open(self.users_path, 'w') as f:
                try:
                    self.knownUsers[user] = features
                    json.dump(self.knownUsers, f, ensure_ascii=False)
                    return True
                except:
                    return False

    def getItem(self, query):
        for item in self.products:
            if query in item['similarItems']:
                return item


if __name__ == "__main__":
    store = Store()
    store.saveUser('test', '3123')
    print store.knownUsers