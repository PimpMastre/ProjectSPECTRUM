class SerializableSettings(object):
    def __init__(self, settings):
        self.settings = settings

    def serialize(self):
        return {x: self.settings[x] for x in self.settings.keys()}

    def get_setting_names(self):
        return self.settings.keys()
