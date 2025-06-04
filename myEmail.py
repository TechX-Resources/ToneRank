class Email:
    """ Represents an email and all of its fields.
        fields: subject, sender, date, body """
    
    def __init__(self, subject, sender, date, body):
        self.subject = subject
        self.sender = sender
        self.date = date
        self.body = body

    def __repr__(self):
        return f"Email(subject={self.subject!r}, sender={self.sender!r}, date={self.date!r})"