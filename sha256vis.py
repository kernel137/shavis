from PIL import Image
import sys
import os
import hashlib
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

image = Image.new("RGB", (8, 8))
# [==================================================]
# sha256 = "c02fa35ab353e05d657513b89ec14ef838cf60dc" # <==
# sha256 = "94be53125e66d7713f5545a92857666ff456f1bd7ca65edb57d0c0a43dfffe37"
sha256 = "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069".replace(" ", "")
# [=================[Check for pipe]=================]
if not os.isatty(0):
	hashedpipe = hashlib.sha256(sys.stdin.buffer.read()).hexdigest()
	sha256 = str(hashedpipe)
# [====================[Functions]===================]
def nextargument(argv, opt): # return list member next to opt
	return argv[argv.index(str(opt))+1:argv.index(str(opt))+2]

def updateconf(config): # config - configparser object -> modify config.ini 
	with open("config.ini", "w") as conf:
		config.write(conf)
# [=================[Hash functions]=================]
def hashfile(filename): # return file sha256sum hash in hex string
	sha256hash = hashlib.sha256()
	with open(filename, 'rb') as file:
	    while True:
	        stack = file.read(2**16) # 64kb
	        if not stack: break
	        sha256hash.update(stack)
	return str(sha256hash.hexdigest())

def hashtext(text): # return text sha256sum hash in hex string
	return hashlib.sha256(bytes(str(text), "UTF-8")).hexdigest()
# [===================[Parameters]===================]
output_to_file_flag = False
output_filename = "output.txt"
#-----------------------------
filename = ""
#------------
theme = str(config["options"]["theme"])
size_select = int(config["options"]["size"])
color = config.getboolean("options", "color")
git = config.getboolean("options", "git")
#----------
# auto theme option idea
# take every pair of hex in hash
# (works for both SHA-1 and SHA-256)
# and generate color
#-------------------
allowed_themes = ["blue", "red", "gold", "natur", "dim", "dark", "cyan", "soft-fall"]
allowed_sizes = [*range(1, 11)]
#------------------------------



# [======================[Help]======================]
# len(sys.argv) == 1 or 
if len(sys.argv) == 2:
	if(sys.argv[1] == "-h" or sys.argv[1] == "--help"):
		helpPage = f"""Usage: sha256vis --hash 
Visualize SHA256 hash sum of a file or 

With no flags, first and only argument is used as file input and the 
visualization is shown in default image viewer.

  --config
        Change configuration for resolution and theme with persistence
		[--config theme NAME] [--config size N]
  -f, --file         Hash file and visualize hash
  [-f filename.ext] [--file filename.ext]
  -s, --hash         Input hash directly as argument
  [-s HASH] [--hash HASH] (HASH has to be SHA256)
  -r, --resolution
        Pick resolution size, options:
       [N]  SHA256      SHA1 (Git)
        1 - 8x8       - 8x5
        2 - 16x16     - 16x10
        3 - 32x32     - 32x20
        4 - 64x64     - 64x40
        5 - 128x128   - 128x80
        6 - 256x256   - 256x160
        7 - 512x512   - 512x320
        8 - 1024x1024 - 1024x640
        9 - 2048x2048 - 2048x1280
       10 - 4096x4096 - 4096x2560
    [-r N] [--resolution N]
  -t, --theme       Change theme, currently available themes:
        blue, red, gold, natur, dim, dark, cyan, soft-fall.
  [-t red] [--theme gold]
  -o, --output      Output to file and (optionally) choose file name
  [-o] [--output] or [-o "output.png"] [--output "output.png"] 
  -m, --mono       Black and white output.
  -g, --git         Use a git commit hash to generate 8x5 image
  [-g HASH] [--git HASH] (HASH has to be SHA-1)
  -h, --help        Display this help and exit

Default output image filename is [7 characters from the hash].png 
By default the image is colored and the default theme is {theme}.

Examples:
  sha256vis filename.ext              Hashes file and visualizes hashsum.
  
"""
		print(helpPage)
		exit()
# [===============[Options Processing]===============]

if("--config" in sys.argv):
	config_nextarg = nextargument(sys.argv, "--config")
	
	if config_nextarg == []: # filter for missing option (--config option) -> exit
		print(f"Missing option: --config OPTION")
		print("Valid options: theme, size, list")
		exit()
	# option - exists

	option = sys.argv[sys.argv.index("--config")+1] 
	# taking option

	if option not in ["theme", "size", "color", "git", "list"]: # filter for wrong option (--config option) -> exit
		print(f"Invalid option: {option}")
		print("Valid options: theme, size, color, git, list")
		exit()
	# option = theme or size or list

	if option == "list": # list current config (--config list) -> exit
		print("[current config]")
		print("theme: " + str(config["options"]["theme"]))
		print("size: " + str(config["options"]["size"]))
		print("color: " + str(config.getboolean("options", "color")))
		print("git: " + str(config.getboolean("options", "git")))
		exit()

	if nextargument(sys.argv, option) == []: # filter for missing argument (--config option argument) -> exit
		print(f"Missing setting argument: --config {option} arg")
		if option == "theme": 
			print("Available themes: ", end="")
			for name in allowed_themes: print(name, end=" ")
		if option == "size": 
			print("Available sizes: ", end="")
			for num in allowed_sizes: print(num, end=" ")
		if option == "color": 
			print("Available values: True, False", end="")
		if option == "git": 
			print("Available values: True, False", end="")
		print()
		exit()
	# argument - exists

	if option == "size": # filter and update size config (--config size N) -> exit
		size_select = sys.argv[sys.argv.index("size")+1]
		if not size_select.isdigit(): # check if size is an integer (--config size N) -> exit
			print(f"Size invalid: {size_select}")
			print("Size needs to be an integer.")
			exit()
		if int(size_select) not in allowed_sizes: # check if size is valid (--config size N) -> exit
			print(f"Size invalid: {size_select}")
			print("Available sizes: ", end="")
			for num in allowed_sizes[:-1]: print(num, end=", ")
			print(allowed_sizes[len(allowed_sizes)-1])
			exit()
		size_select = int(size_select)
		config.set("options", "size", str(size_select))
		updateconf(config)
		exit()

	if option == "theme": # filter and update theme config (--config theme name) -> exit
		theme = sys.argv[sys.argv.index("theme")+1]
		if theme not in allowed_themes: # check if theme name is valid
			print(f"Theme name invalid: {theme}")
			print("Available themes: ", end="")
			for name in allowed_themes[:-1]: print(name, end=", ")
			print(allowed_themes[len(allowed_themes)-1])
			exit()
		config.set("options", "theme", str(theme))
		updateconf(config)
		exit()
	
	if option == "color": # filter and update color config (--config color bool) -> exit
		color = sys.argv[sys.argv.index("color")+1]
		if color.lower() in ["true", "t", "y", "yes", "yeah", "mhm", "yup"]:
			config.set("options", "color", "True")
		elif color.lower() in ["false", "f", "n", "no", "nah", "nuhuh", "nope"]:
			config.set("options", "color", "False")
		else:
			print("Invalid boolean value: --config color VALUE")
			print("Use a boolean as value for color.")
			exit()
		updateconf(config)
		exit()

	if option == "git": # filter and update git config (--config git bool) -> exit
		git = sys.argv[sys.argv.index("git")+1]
		if git.lower() in ["true", "t", "y", "yes", "yeah", "mhm", "yup"]:
			config.set("options", "git", "True")
		elif git.lower() in ["false", "f", "n", "no", "nah", "nuhuh", "nope"]:
			config.set("options", "git", "False")
		else:
			print("Invalid boolean value: --config git VALUE")
			print("Use a boolean as value for git.")
			exit()
		updateconf(config)
		exit()

if("-f" in sys.argv or "--file" in sys.argv):
	if "-f" in sys.argv: # filter for missing filename (-f filename.ext) -> exit
		if nextargument(sys.argv, "-f") == []: # filter for missing filename
			print(f"Missing file name: -f filename.ext")
			exit()
		# file name - exists
	if "--file" in sys.argv: # filter for missing filename (--file filename.ext) -> exit
		if nextargument(sys.argv, "--file") == []: # filter for missing filename
			print(f"Missing file name: --file filename.ext")
			exit()
		# file name - exists
	# file name - exists

	filename = sys.argv[sys.argv.index("-f")+1] if "-f" in sys.argv else sys.argv[sys.argv.index("--file")+1]
	# taking file name

	try: # opening file 
		file = open(str(filename))
	except FileNotFoundError: # filter filename.ext existing -> exit
		print(f"Invalid file name: --file {filename}")
		print("File does not exist.")
		exit()
	else:
		sha256 = hashfile(str(filename))
	# sha256 updated 
	
if("-t" in sys.argv or "--theme" in sys.argv):
	if "-t" in sys.argv: # filter for missing option (-t option) -> exit
		if nextargument(sys.argv, "-t") == []: # filter for missing setting
			print(f"Missing setting: -t theme_name")
			print("Available themes: ", end="")
			for name in allowed_themes[:-1]: print(name, end=", ")
			print(allowed_themes[len(allowed_themes)-1])
			exit()
		# setting - exists
	if "--theme" in sys.argv: # filter for missing option (--theme option) -> exit
		if nextargument(sys.argv, "--theme") == []: # filter for missing setting
			print(f"Missing setting: --theme theme_name")
			print("Available themes: ", end="")
			for name in allowed_themes[:-1]: print(name, end=", ")
			print(allowed_themes[len(allowed_themes)-1])
			exit()
		# setting - exists
	# setting - exists

	theme = sys.argv[sys.argv.index("-t")+1] if "-t" in sys.argv else sys.argv[sys.argv.index("--theme")+1]
	# taking setting | setting -> theme

	if theme not in allowed_themes: # filter for wrong option (--theme option) -> exit
		print(f"Theme name invalid: -t/--theme theme_name")
		print("Available themes: blue, red, gold, natur, dim, dark, cyan, soft-fall")
		exit()

	# setting theme changed for this call

if("-s" in sys.argv or "--hash" in sys.argv):
	if "-s" in sys.argv: # filter for missing hash (-s HASH) -> exit
		if nextargument(sys.argv, "-s") == []: # filter for missing hash
			print(f"Missing hash: -s HASH")
			exit()
		# hash - exists
	if "--hash" in sys.argv: # filter for missing hash (--hash HASH) -> exit
		if nextargument(sys.argv, "--hash") == []: # filter for missing hash
			print(f"Missing hash: --hash HASH")
			exit()
		# hash - exists
	# hash input - exists

	sha256 = str(sys.argv[sys.argv.index("-s")+1]) if "-s" in sys.argv else str(sys.argv[sys.argv.index("--hash")+1])
	# sha256 updated - checked for invalid input in code below



	

# [===================[^^^DONE^^^]===================]
	
if("-o" in sys.argv or "--output" in sys.argv):
	output_to_file_flag = True
	output_filename = sys.argv[sys.argv.index("-o")+1] if "-o" in sys.argv else sys.argv[sys.argv.index("--output")+1]

if("-e" in sys.argv or "--encrypt" in sys.argv):
	encrypt_flag = True
	decrypt_flag = False

elif("-d" in sys.argv or "--decrypt" in sys.argv):
	encrypt_flag = False
	decrypt_flag = True

if("-k" in sys.argv or "--key" in sys.argv):
	custom_key_flag = True
	key = str(sys.argv[sys.argv.index("-k")+1]) if "-k" in sys.argv else str(sys.argv[sys.argv.index("--key")+1])
	if(key.isnumeric()): key = int(key)
	else: key = int(sum([ord(letter) for letter in key]))






# [==========[Manual inputs of hash checks]==========]
# Check length
if git and len(sha256) != 40: 
	print("Error: Git hash must be 40 characters long (SHA-1).")
	exit()
if len(sha256) != 64 and not git: 
	print("Error: Input must be 64 characters long.")
	exit()

# Check for invalid characters (And point them out!!!)
hex_allowed = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f"]
valid_characters = [i in hex_allowed for i in sha256]
if not all(valid_characters): 
	print("Error: Invalid SHA256 hashsum character in string.")
	print(sha256)
	for i in range(len(valid_characters)):
		if not valid_characters[i]: print("↑", end='')
		else: print(" ", end='')
	print()
	exit()
# [==================[ Processing ]==================]
sha256_dv = [int(i, 16) for i in sha256] # dv  = Decimal Values         |   hex -> decimal -> list
sha256_dvm = []		 					 # dvm = Decimal Values Matrix  |
for i in range(0, 8): sha256_dvm.append(sha256_dv[i*8:(i+1)*8]) #       |   list[64] -> matrix[8][8]
# [==================[Theme Loader]==================]
theme = "./themes/" + theme + ".hex" # insert theme name
with open(theme) as file:            # open theme file
	theme = file.readlines()         # theme is now list[16] of hex colors from theme
for i in range(16): theme[i] = theme[i].strip() # strip '\n'
for i in range(16): theme[i] = tuple(int(theme[i][i2:i2+2], 16) for i2 in [0, 2, 4]) # hex list[16] -> list of 16 decimal 3 tuple
# [==================================================]







# [================[Rendering Image]=================]

if git: x, y = 8, 5
else: x, y = 8, 8
image = Image.new("RGB" if color else "L", (x, y))

pixels = image.load()
for v in range(x):
	for h in range(y):
		pixels[v,h] = theme[sha256_dvm[h][v]] if color else ((sha256_dvm[h][v]+1)*16)-1


size = 8 * (2**(size_select-1))
xsize, ysize = size, 5 * (2**(size_select-1)) if git else size

image.resize((xsize, ysize), resample=Image.NEAREST).show()
# [==================================================]



# ↑

# 9 4 b e 5 3 1 2
# 5 e 6 6 d 7 7 1
# 3 f 5 5 4 5 a 9
# 2 8 5 7 6 6 6 f
# f 4 5 6 f 1 b d
# 7 c a 6 5 e d b
# 5 7 d 0 c 0 a 4
# 3 d f f f e 3 4

# 94be53125e66d7713f5545a92857666ff456f1bd7ca65edb57d0c0a43dfffe34