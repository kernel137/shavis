from PIL import Image
import sys
import os
import hashlib
import configparser
import pathlib


def start():
	p = pathlib.PurePath(__file__)
	config_dir = pathlib.Path(*list(p.parent.parts) + ["conf"] + ["config.ini"])
	theme_dir = pathlib.Path(*list(p.parent.parts) + ["conf"] + ["themes"])

	config = configparser.ConfigParser()
	config.read(config_dir)

	image = Image.new("RGB", (8, 8))
	# [==================================================]
	sha256 = ""
	# [====================[Functions]===================]
	def nextargument(argv, opt): # return list member next to opt
		return argv[argv.index(str(opt))+1:argv.index(str(opt))+2]

	def updateconf(config): # config - configparser object -> modify config.ini 
		with open(config_dir, "w") as conf:
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
	#----------------------------------------
	allowed_themes = ["blue", "red", "gold", "natur", "dim", "dark", "cyan", "soft-fall"]
	allowed_sizes = [*range(1, 11)]
	allowed_formats = ["png", "PNG", "jpg", "JPG", "jpeg", "JPEG", "bmp", "BMP", "ppm", "PPM"]
	# [======================[Help]======================]

	if(os.isatty(0) and (len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help")):
		helpPage = f"""Usage: shavis [OPTIONS]...[FILE]
Visualize SHA256 or SHA1 hash sum, either directly or of a file. 
With no flags, print this help page and exit.
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
  [-o def] [--output def] or [-o "output.png"] [--output "output.png"] 
  -g, --git         Use a git commit hash to generate 8x5 image
  [-g HASH] [--git HASH] (HASH has to be SHA-1)
  -m, --mono        Black and white output. No arguments.
  [-m] [--mono]
  -h, --help        Display this help and exit
  [-h] [--help]

If output filename is "def", the file name will be the first 7 hex digits
of the hash in a .png format.
Current config:
  theme: {theme}
  size:  {size_select}
  color: {color}
  git:   {git}

Examples:
  shavis filename.ext                
  shavis -t cyan -r 4 -o def -s HASH
  shavis -m -o commit.png -g GIT-HASH  

Piping accessibility examples: 
  cat file.ext | shavis
  git rev-parse HEAD | shavis -g

Check out the project at: https://github.com/kernel137/shavis
	"""
		print(helpPage)
		exit()
	# [===============[Options Processing]===============]

	if("--config" in sys.argv):
		config_nextarg = nextargument(sys.argv, "--config")

		if config_nextarg == []: # filter for missing option (--config option) -> exit
			print(f"Missing option: --config OPTION")
			print("Valid options: theme, size, color, git, list")
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

	if("-r" in sys.argv or "--resolution" in sys.argv):
		if "-r" in sys.argv: # filter for missing hash (-r HASH) -> exit
			if nextargument(sys.argv, "-r") == []: # filter for missing hash
				print(f"Missing number: -r N")
				print("Available resolutions: ", end="")
				for num in allowed_sizes[:-1]: print(num, end=", ")
				print(allowed_sizes[len(allowed_sizes)-1])
				print("Syntax: -r N")
				print(" N   SHA256      SHA1 (Git)")
				print(" 1 - 8x8       - 8x5")
				print(" 2 - 16x16     - 16x10")
				print(" 3 - 32x32     - 32x20")
				print(" 4 - 64x64     - 64x40")
				print(" 5 - 128x128   - 128x80")
				print(" 6 - 256x256   - 256x160")
				print(" 7 - 512x512   - 512x320")
				print(" 8 - 1024x1024 - 1024x640")
				print(" 9 - 2048x2048 - 2048x1280")
				print("10 - 4096x4096 - 4096x2560")
				exit()
			# hash - exists
		if "--resolution" in sys.argv: # filter for missing hash (--hash HASH) -> exit
			if nextargument(sys.argv, "--resolution") == []: # filter for missing hash
				print(f"Missing number: --resolution N")
				print("Available resolutions: ", end="")
				for num in allowed_sizes[:-1]: print(num, end=", ")
				print(allowed_sizes[len(allowed_sizes)-1])
				print("Syntax: --resolution N")
				print(" N   SHA256      SHA1 (Git)")
				print(" 1 - 8x8       - 8x5")
				print(" 2 - 16x16     - 16x10")
				print(" 3 - 32x32     - 32x20")
				print(" 4 - 64x64     - 64x40")
				print(" 5 - 128x128   - 128x80")
				print(" 6 - 256x256   - 256x160")
				print(" 7 - 512x512   - 512x320")
				print(" 8 - 1024x1024 - 1024x640")
				print(" 9 - 2048x2048 - 2048x1280")
				print("10 - 4096x4096 - 4096x2560")
				exit()
			# hash - exists
		# hash input - exists

		size_select = str(sys.argv[sys.argv.index("-r")+1]) if "-r" in sys.argv else str(sys.argv[sys.argv.index("--resolution")+1])

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

		# size_select updated

	if("-g" in sys.argv or "--git" in sys.argv):
		if not os.isatty(0): pass
		elif "-g" in sys.argv: # filter for missing hash (-g GIT-HASH) -> exit
			if nextargument(sys.argv, "-g") == []: # filter for missing hash
				print(f"Missing hash: -g GIT-HASH")
				print("Where GIT-HASH is a git commit SHA-1 hash of length 40")
				exit()
			# hash - exists
		elif "--git" in sys.argv: # filter for missing hash (--git GIT-HASH) -> exit
			if nextargument(sys.argv, "--git") == []: # filter for missing has
				print(f"Missing hash: --git GIT-HASH")
				print("Where GIT-HASH is a git commit SHA-1 hash of length 40")
				exit()
			# hash - exists
		# hash - exists

		git = True
		if os.isatty(0):
			sha256 = sys.argv[sys.argv.index("-g")+1] if "-g" in sys.argv else sys.argv[sys.argv.index("--git")+1]
		# output filename inserted

	if("-o" in sys.argv or "--output" in sys.argv):
		if "-o" in sys.argv: # filter for missing filename (-o filename.ext) -> exit
			if nextargument(sys.argv, "-o") == []: # filter for missing filename
				print(f"Missing filename argument: -o filename.ext")
				print("Make sure to include the extension: .png, .jpg etc etc.")
				print(f"Alternative option: --output def")
				print("This sets the name of the file to the first 7 hex values")
				print("of the hash")
				exit()
			# output - exists
		if "--output" in sys.argv: # filter for missing filename (--output filename.ext) -> exit
			if nextargument(sys.argv, "--output") == []: # filter for missing filename
				print(f"Missing filename argument: --output filename.ext")
				print("Make sure to include the extension: .png, .jpg etc etc.")
				print(f"Alternative option: --output def")
				print("This sets the name of the file to the first 7 hex values")
				print("of the hash")
				exit()
			# output - exists
		# output - exists

		output_to_file_flag = True
		output_filename = sys.argv[sys.argv.index("-o")+1] if "-o" in sys.argv else sys.argv[sys.argv.index("--output")+1]
		# output filename inserted

		if output_filename == "def":
			output_filename = sha256[:7] + ".png"

		ext = "".join(output_filename.split(".")[-1:])
		if ext not in allowed_formats:  # filter for incorrect format of .ext (--filename filename.ext) -> exit
			print(f"Incorrect output file format: .{ext}")
			print("Available formats: ", end="")
			for ext in allowed_formats[:-1]: print(f".{ext}", end=", ")
			print(allowed_formats[len(allowed_formats)-1])
			exit()

	if("-m" in sys.argv or "--mono" in sys.argv):
		color = False
	# [=================[Check for pipe]=================]
	if not os.isatty(0):
		if git: 
			sha256 = str(sys.stdin.read()).strip()
		else:
			hashedpipe = hashlib.sha256(sys.stdin.buffer.read()).hexdigest()
			sha256 = str(hashedpipe)
	# [==============[Check for empty hash]==============]
	if sha256 == "":
		ls_files = next(os.walk("./"), (None, None, []))[2]
		filename = "".join(sys.argv[-1:])
		if filename in ls_files:
			try: # opening file 
				file = open(str(filename))
			except FileNotFoundError: # filter filename.ext existing -> exit
				print(f"Invalid file name: --file {filename}")
				print("File does not exist.")
				exit()
			else:
				sha256 = hashfile(str(filename))
		else:
			print("Hash value empty")
			print("Input hash either by hashing a file:")
			print("  shavis filename.ext")
			print("  shavis -t blue -r 3 filename.ext")
			print("(Filename should always be the last argument")
			print("and in the same directory)")
			print("For files not in the same directory, use --file /dir/to/file.ext\"\"")
			print("Or inputting hash manually with:")
			print("  shavis --git GIT-HASH")
			print("  shavis --hash HASH")
			exit()

	# [==========[Manual inputs of hash checks]==========]
	# Check length
	if git and len(sha256) != 40: # filter for missing hash (-g GIT-HASH) -> exit
		print("Error: Git hash must be 40 characters long (SHA-1).")
		print(f"[{sha256}]")
		exit()
	if not git and len(sha256) != 64: # filter for missing hash -> exit
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
	theme = theme_dir / (theme + ".hex") # insert theme name
	with open(theme) as file:            # open theme file
		theme = file.readlines()         # theme is now list[16] of hex colors from theme
	for i in range(16): theme[i] = theme[i].strip() # strip '\n'
	for i in range(16): theme[i] = tuple(int(theme[i][i2:i2+2], 16) for i2 in [0, 2, 4]) # hex list[16] -> list of 16 decimal 3 tuple
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
	# [=============[Resize and output Image]============]
	if output_to_file_flag: image.resize((xsize, ysize), resample=Image.NEAREST).save(str(output_filename))
	else: image.resize((xsize, ysize), resample=Image.NEAREST).show()
	# [==================================================]

if __name__ == "__main__":
	start()