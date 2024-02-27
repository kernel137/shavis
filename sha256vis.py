from PIL import Image

# [===================[Parameters]===================]
theme = "red"
size_select = 7
color = True
# [==================================================]

sha256 = str(input("sha256sum: "))
# [==================================================]
# Check length
if len(sha256) != 64: 
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



# for i in range(8):
# 	for i2 in range(8):
# 		print(((sha256_dvm[i][i2]+1)*16)-1, end=' ')
# 	print()


# [ Implement size here ]

# size_select = 7
# 1 2  3  4  5   6   7   8    9    10
size = 8 * (2**(size_select-1))
# 8 16 32 64 128 256 512 1024 2048 4096 

# [=====================]

image = Image.new("L", (8, 8))
if color: 
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

image.resize((size,size), resample=Image.NEAREST).show()






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