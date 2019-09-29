SCAN_ITEM = ['take picture', 'scan item', 'scan picture', 'scan', 'picture', 'pic', 'take pic']
LOOKING = 'looking for'

items = {
    'chocolate': {
        "productName":"Mars Pods",
        "productPrice":4.99,
        "aisleNumber":5,
        "productStock":75
    },
    
    'beverage': {
        "productName":"Pepsi",
        "productPrice":3.99,
        "aisleNumber":3,
        "productStock":150
    },

    'fruit': {
        "productName":"Apple",
        "productPrice":0.99,
        "aisleNumber":1,
        "productStock":200
    }
}

synonyms = { 
    'chocolateSynonyms': ['chocolate', 'mars', 'pods', 'mars pod'], 
    'beverageSynonyms': ['beverage', 'beverages', 'drink', 'pepsi', 'cola', 'soft drink'],
    'fruitSynonyms': ['fruit', 'apple']
}
