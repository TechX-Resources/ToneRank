# Data utility class for storing emails
# @author Rylan Ahmadi (Ry305)
# Last updated 07/06/2025

class Email:
    """ Represents an email and all of its fields.
        fields: subject, sender, date, body """
    
    def __init__(self, subject, sender, date, body):
        """ Creates a new email object with specified parameters. Urgency score (uscore) is instantiated
         at -1. """
        self.subject = subject
        self.sender = sender
        self.date = date
        self.body = body
        self.uscore = -1.0 # the urgency score will be set later, in toneRank

    def __repr__(self):
        return f"{self.sender}: {self.subject!r} | uscore: {self.uscore!r}"
    
    def __eq__(self, other):
        return self.uscore == other.uscore
    
    def __gt__(self, other):
        return self.uscore < other.uscore
    
    def __lt__(self, other):
        return self.uscore > other.uscore
