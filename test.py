import configparser

config = configparser.ConfigParser()

config.add_section('options')
config.set('options', 'theme', 'cyan')
config.set('options', 'size', '7')

with open("config.ini", "w") as conf:
	config.write(conf)