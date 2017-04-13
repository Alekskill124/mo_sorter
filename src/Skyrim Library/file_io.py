import configparser

def write_config(file_name, settings):
    ConfigParser = configparser.SafeConfigParser()
    ConfigParser.add_section("Main")

    with open(file_name, 'w') as ConfigFile:
        for key in settings:
            ConfigParser.set("Main", str(key), str(settings[key]))
        ConfigParser.write(ConfigFile)

def read_config(file_name, setting):
    ConfigParser = configparser.SafeConfigParser()
    ConfigParser.add_section("Main")

    ConfigParser.read(file_name)
    try:
        result = ConfigParser.get("Main", setting)
    except configparser.NoOptionError:
        result = None

    return result
