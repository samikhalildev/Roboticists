REAL_ROBOT_IP = '192.168.1.41:9559'
VIRTUAL_ROBOT_IP = 'localhost:43823'
VIRTUAL_ROBOT = True

# Interactions
GREET = ['hi', 'hello', 'hey', 'howdy', 'hey pepper']
SCAN = ['take picture', 'scan item', 'scan picture', 'scan', 'picture', 'take pic']
LOOK_FOR = 'looking for'
BYE = ['bye', 'goodbye', 'see ya', 'see ya later', 'laters', 'have a good day', 'goodnight', 'enjoy your day']

# Robot messages
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

    concept:(greet) ["hi" "hello" "hey" howdy "hey pepper"]
    concept:(look) ["I am looking for _*" "looking for _*"]
    concept:(items) [{0}]
    concept:(scan) [scan picture "take picture" "scan item" "scan picture"]

    u: (_~greet) Hello there, what are you looking for today?
    u: (_~look) $item=$1
    u: (_~items) $item=$1
    u: (_~scan) Scanning item, please wait.
    u: (e:Dialog/NotUnderstood) Sorry, I dont understand.
"""

# Encoded image html src
IMAGE_SCANNED_HTML = '<h1 style="text-align:center;">This is the picture I took, you may retake by saying "scan" again :)</h1> <img style="text-align:center;" src="data:image/png;base64,{0}"/>'
