from PIL import Image
sha256 = str(input("sha256sum: "))

if len(sha256) != 64: 
	print("Error: Input must be 64 characters long.")
	exit()

hex_allowed = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f"]
valid_string = [i in hex_allowed for i in sha256]
if not all(valid_string): 
	print("Error: Invalid SHA256 hashsum character in string.")
	for i in range(len(valid_string)):
		if not valid_string[i]: print(f"index: {i}\ncharacter: {sha256[i]}")
	exit()

num_value = [int(i, 16) for i in sha256]

print(num_value)

# img = Image.new("")








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