class Tablet:

    def __init__(self, session):
        self.session = session
        self.magic_tablet = session.service("MagicTablet")
    
    def show(self, animation=[], line1=[], line2=[]):
        self.magic_tablet.show(self.animation(animation) if len(animation) else animation, line1, line2)

    def animation(self, key):
        self.magic_tablet.animation(key)

    def ask(self, *line):
        btns = []

        # create a tuple array of the same value
        for i, text in enumerate(line):
            btns.append((text, text))

        return self.magic_tablet.ask(btns)
        
    def htmlDisplay(self, html, options={}):
        self.magic_tablet.html(html_code, options)
