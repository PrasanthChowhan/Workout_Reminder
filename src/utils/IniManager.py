import configparser

class IniFileManager:
    def __init__(self, file_path,defualt_file = None):
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.defualt_file = defualt_file

    def read_config(self):
        try:
            with open(self.file_path, 'r') as file:
                self.config.read_file(file)
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found. Creating a new one.")

    def write_config(self):
        with open(self.file_path, 'w') as file:
            self.config.write(file)
            print(f"Configuration written to '{self.file_path}'")

    def get_value(self, section, key):
        try: 
            self.config.read(self.file_path)
            return self.config.get(section, key)
        except :
            if self.defualt_file:
                self.config.read(self.defualt_file)
                return self.config.get(section, key)

        

    def set_value(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)

    def update_value_in_ini(self, section, key, new_value):
        self.read_config()
        self.set_value(section, key, new_value)
        self.write_config()

        
    def dict_to_ini(self,dictionary):
        for section, options in dictionary.items():
            self.config.add_section(section)
            for key, value in options.items():
                self.config.set(section, key, str(value))

        self.write_config()
    
if __name__ == '__main__':
# Example dictionary
    my_dict = {
        'Theme': {'selected theme':'','Exercise number': ''},
        'Notheme': {'last muscle': 'chest'}
    }

    # Convert dictionary to INI file
    ini = IniFileManager('example_config.ini')
    ini.dict_to_ini(my_dict)


# print("Configuration written to 'example_config.ini'")