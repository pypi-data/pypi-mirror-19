class LocalDataClass:

    def __init__(self):
        self.app = None
        self.db = None
        self.ModelHelpers = None
        self.redo_attrs = None
        self.reencode = None
        self.relation_to_class = None
        self.word_to_class = None

        self.MANY_TO_MANY_RELATIONS = None
        self.NON_OWNER_RELATIONS = None
        self.RELATIONS_NOT_FIELDS = None
        self.UUIDGenerator = None
        self.UUID = None
        self.VANILLA_OBJECTS = None

    def set(self, title, data):
        setattr(self, title, data)
