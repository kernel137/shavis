<h1 align="center">Etherium private key to BPM image</h1>
A proof-of-concept C++ CLI tool that takes an Ethereum private key as input and generates a BMP image.

Made using libbmp by marc-q: https://github.com/marc-q/libbmp/

## Installation

### On Linux

Compile by running `g++ libbmp.cpp epktobmp.cpp -o filename.out` in the ./source/ directory.

### On Windows

Compile by running `g++ libbmp.cpp epktobmp.cpp -o filename.exe` ./source/ directory in PowerShell.

## Usage

After running the compiled executable by `./filename.out` or `.\filename.exe`, first, input the private key.
Second choose your resolution, 16x16 is the lowest possible and is an exactly 1:1 ratio between pixel and binary.  

The gray option makes it so that instead of full black and white, the pixels are gray with a value difference between white and black pixels of 1, making it impossible to extract the key from a picture taken of a screen displaying the image.
