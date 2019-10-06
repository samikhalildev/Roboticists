VIRTUAL_ROBOT = True
REAL_ROBOT_IP = '192.168.1.41:9559'
VIRTUAL_ROBOT_IP = 'localhost:35633'

IMAGE_PATH = '/Model/img/item.jpg'

# Interaction
USER_GREET = ['hi', 'hello', 'hey', 'howdy', 'hey pepper', 'help', 'sup', 'how are you', 'how you doing', "what's up", "yo", "pepper"]
ROBOT_GREET = ['Hello there, what are you looking for today?', 'Hey human, how may I help you today?', 'Howdy, what would you like?', 'Hello there, I am here to help.', 'Hey friend, how may I assist you?', 'Hi, I am Pepper, your shopping buddy.']
SCAN = ['take picture', 'scan item', 'scan picture', 'scan', 'picture', 'take pic']
LOOK = ["I am looking for _*", "looking for _*"]
BYE = ['bye', 'goodbye', 'see ya', 'see ya later', 'laters', 'have a good day', 'goodnight', 'enjoy your day']
LOOK_FOR = 'looking for'
ROBOT_CONFUSED = ['Sorry, I dont understand.', 'I am not sure what you said', 'What?', 'Please repeat that', 'Sorry, I didnt get that', 'What did you just say?', 'I am unable to process that', 'I dont get it', "I am confused"]

# Robot states
HI = 'Hi!'
SCAN_ITEM = 'Scan Item'
CHOOSE_ITEM = 'Choose Item'
SCAN_ITEM_OR_TALK = 'You may use the tablet or talk to me'
ITEM_SCANNED = 'Item scanned'
ITEM_AVAILABLE = '{0} is available'
AISLE = 'You can find it in aisle {0}.\nIt is priced for {1}'
FIND_ANOTHER_ITEM = 'Find another item'
NOT_IN_STOCK = 'Sorry, {0} may be not in stock.'
OBJECT_NOT_DETECTED = "Object not detected, please try again."
THANK_YOU = 'Thank you'
FOR = 'for'

# Tablet animation
ANIMATION = {
    'BLANK': 'BLANK',
    'BLACK': 'BLACK',
    'LOGO': 'LOGO',
    'COUNTER': 'COUNTER',
    'PROGRESS': 'PROGRESS',
    'HELIX': 'HELIX',
    'TICK': 'TICK', 
    'UNCROSS_HANDS': 'UNCROSS_HANDS',
    'WAVE': 'WAVE_HELLO'
}

# Robot interaction dialog
INTERACTION_CONTENT = """
    topic: ~interact()
    language: enu

    concept:(greet) [{0}]
    concept:(look)  [{2}]
    concept:(items) [{3}]
    concept:(scan)  [{4}]
    concept:(bye)   [{5}]

    u: (_~greet) {1}
    u: (_~look) $item=$1
    u: (_~items) $item=$1
    u: (_~scan) Scanning item, please wait.
    u: (_~bye) {6}
    u: (e:Dialog/NotUnderstood) {7}
"""

# Encoded image HTML src
IMAGE_SCANNED_HTML = '<h1 style="text-align:center;">This is the picture I took, you may retake by saying "scan" again :)</h1> <img style="text-align:center;" src="data:image/png;base64,{0}"/>'
