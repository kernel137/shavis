from PIL import Image
import sys
#-------------------
output_to_file_flag = False
#--------------------------
input_string = ""
input_filename = ""
#------------------
output_string = ""
output_filename = "output.txt"
#-----------------------------
# [===================[Parameters]===================]
# auto theme option idea
# take every pair of hex in hash
# (works for both SHA-1 and SHA-256)
# and 
theme = "cyan"
size_select = 7
color = True
git = True
# [==================================================]
sha256 = "b7d98ca9422f190ad2f8de8130ce8ba1543ee0db" # <====
# sha256 = "94be53125e66d7713f5545a92857666ff456f1bd7ca65edb57d0c0a43dfffe37"
# [==================================================]	
"""
if(len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help"):
	helpPage = \"""Usage: sha256vis --hash 
Encrypt or decrypt text utilizing collatz iteration.
Allowed input is text through command-line arguments or files.

With no flags, first and only argument is used as hash and the visualization
is shown in default image viewer.

  -s --hash         Input hash as string after flag
  [-s 94be...] [--hash 94be...]
  -o, --output      Output to file and choose file name
  [-o "output.png"] [--output "output.png"]
  -h, --help        Print this text and exit



Default output filename is "output.txt". If used twice or more times with 
the same filename, output will overwrite the file.

Use -s if you're reading from a file but want the output in the console.

Examples:
  colcipher "Test input text"         Encodes text and prints output to console.
  colcipher -d -t "448 26 14 613 123" Decodes text and prints output to console.
  colcipher -e -f "./plain.txt" -o "secret.txt"           Takes input from file 
  "plain.txt" and outputs encoded text into secret.txt in the same directory.
  colcipher -e -k 2953 -f "plain.txt" -o "encrypted.txt"  Encrypts "plain.txt"
  using custom key and outputs into "encrypted.txt".
\"""
	print(helpPage)
	exit()

"""








# [==================================================]	
# for i in range(8):
# 	for i2 in range(8):
# 		print(((sha256_dvm[i][i2]+1)*16)-1, end=' ')
# 	print()
# [==================================================]
# sha256 = str(input("sha256sum: "))
# [==================================================]
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
sha256_dv = [int(i, 16) for i in sha256] # dv  = Decimal Values
sha256_dvm = []		 					 # dvm = Decimal Values Matrix
for i in range(0, 8): sha256_dvm.append(sha256_dv[i*8:(i+1)*8])
# [==================[Theme Loader]==================]
theme = "./themes/" + theme + ".hex"
with open(theme) as file:
	theme = file.readlines()
for i in range(16): theme[i] = theme[i].strip()
for i in range(16): theme[i] = tuple(int(theme[i][i2:i2+2], 16) for i2 in [0, 2, 4])
# [==================================================]






# [ Implement size here ]

# size_select = 7
# 1 2  3  4  5   6   7   8    9    10
size = 8 * (2**(size_select-1))
# 8 16 32 64 128 256 512 1024 2048 4096 

# [================[Rendering Image]=================]
image = Image.new("L", (8, 8))
if color: 
	if git:
		image = Image.new("RGB", (8, 5))
		pixels = image.load()
		for v in range(8):
			for h in range(5):
				pixels[v,h] = theme[sha256_dvm[h][v]]
	else:
		image = Image.new("RGB", (8, 8))
		pixels = image.load()
		for v in range(8):
			for h in range(8):
				pixels[v,h] = theme[sha256_dvm[h][v]]
else:
	pixels = image.load()
	for v in range(8):
		for h in range(8):
			pixels[v,h] = ((sha256_dvm[h][v]+1)*16)-1



if git: image.resize((size, 5 * (2**(size_select-1))), resample=Image.NEAREST).show()
else: image.resize((size, size), resample=Image.NEAREST).show()





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