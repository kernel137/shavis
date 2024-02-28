colors = []
with open("full.hex", "r") as file: # output name of hex file
	colors = file.readlines()

for i in range(len(colors)): colors[i] = colors[i].strip().casefold()

for i in range(len(colors)): print(colors[i], end=" ") 
print()

with open("full.hex", "w") as file: # input name of hex file
	for color in colors[::-1]:
		file.write(color+"\n")

