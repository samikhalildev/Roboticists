import json, os
class Store:
    
    def __init__(self):

        self.users_path = os.getcwd() + '/Model/data/users.json'
        self.knownUsers = self.loadJSON()
        self.products = [
            {
                "productName":"apple",
                "productPrice":0.99,
                "aisleNumber":1,
                "productStock":200
            },
            
            {
                "productName":"banana",
                "productPrice":2.99,
                "aisleNumber":1,
                "productStock":200
            },

            {
                "productName":"orange",
                "productPrice":1.99,
                "aisleNumber":6,
                "productStock":200
            },

            {
                "productName":"broccoli",
                "productPrice":2.99,
                "aisleNumber":1,
                "productStock":200
            },

            {
                "productName":"carrot",
                "productPrice":1.99,
                "aisleNumber":1,
                "productStock":200
            },

            {
                "productName":"pizza",
                "productPrice":2.99,
                "aisleNumber":5,
                "productStock":200
            },

            {
                "productName":"laptop",
                "productPrice":2.99,
                "aisleNumber":2,
                "productStock":200
            },

            {
                "productName":"keyboard",
                "productPrice":2.99,
                "aisleNumber":1,
                "productStock":200
            },

            {
                "productName":"donut",
                "productPrice":2.99,
                "aisleNumber":3,
                "productStock":200
            },

            {
                "productName":"hot dog",
                "productPrice":2.99,
                "aisleNumber":1,
                "productStock":200
            }
        ]

        self.availableItems = ['pizza', 'apple', 'hot dog', 'donut', 'keyboard', 'laptop', 'carrot', 'apple', 'orange', 'broccoli', 'banana']

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
        if query in self.availableItems:
            for item in self.products:
                if query == item['productName']:
                    return item


if __name__ == "__main__":
    store = Store()
    store.saveUser('test', '3123')
    print store.knownUsers