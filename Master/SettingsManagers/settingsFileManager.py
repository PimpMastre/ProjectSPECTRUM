class SettingsFileManager:
    def __init__(self, directory, filename):
        self.__filename = filename
        self.__directory = directory

    def get_all_settings(self):
        file = open(self.__directory + '/' + self.__filename, "r")
        output = dict()
        for line in file.readlines():
            if line != '':
                data = line.split('=')
                output[data[0].strip()] = data[1].strip()

        file.close()
        return output

    def get_setting(self, name):
        file = open(self.__directory + '/' + self.__filename, "r")
        for line in file.readlines():
            if line != '':
                data = line.split('=')
                if data[0].strip() == name:
                    file.close()
                    return {data[0].strip(): data[1].strip()}

        return None

    def save_all(self, settings):
        file = open(self.__directory + '/' + self.__filename, "w")
        for setting_key in settings:
            file.write(setting_key + "=" + settings[setting_key])
            file.write('\n')

        file.close()
