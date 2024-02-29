import configparser
import sys



# config = configparser.ConfigParser()

# config.add_section('options')
# config.set('options', 'theme', 'cyan')
# config.set('options', 'size', '7')

# with open("config.ini", "w") as conf:
# 	config.write(conf)

def nextargument(argv, opti):
	return argv[opti+1:opti+2]

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]



print(nextargument(sys.argv, sys.argv.index("--config")))

