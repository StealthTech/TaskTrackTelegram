class Event:
    def __init__(self, title, date, is_important=False, repeat=None):
        self.title = title
        self.date = date  # Datetime
        self.is_important = is_important
        self.repeat = repeat  # Секунды


class Task:
    def __init__(self, title, setup_date, until_date, is_important=False):
        self.title = title
        self.setup_date = setup_date
        self.until_date = until_date
        self.is_important = is_important
