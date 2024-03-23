<h1 align="center">shavis</h1>
A Python CLI tool that takes SHA256 or SHA1 hash as input and generates an image.
Shavis can hash files (SHA256), take input from pipe and configure the output image to a wide range of sizes.
Made using Pillow (forked from PIL).

Used to more intuitively visualize a SHA256 or SHA1 hash. 

<p align="center">Hash of previous commit:</p>
<p align="center">
  <img src="hash_of_prev_commit.png">
</p>

### Install
Install by running `pip install shavis`

```
Usage: shavis [OPTIONS]...[FILE]
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
  -l  --git-latest  Use latest git commit hash from current directory to generate 8x5 image
  [-l] [--git-latest]
  -m, --mono        Black and white output. No arguments.
  [-m] [--mono]
  -h, --help        Display this help and exit
  [-h] [--help]

If output filename is "def", the file name will be the first 7 hex digits
of the hash in a .png format.
Current config:
  theme: red
  size:  7
  color: True
  git:   False

Examples:
  shavis filename.ext                
  shavis -t cyan -r 4 -o def -s HASH
  shavis -m -o commit.png -g GIT-HASH  

Piping accessibility examples: 
  cat file.ext | shavis
  git rev-parse HEAD | shavis -g

Check out the project at: https://github.com/kernel137/shavis
```
_**I am aware of the argparse or click python modules for argument parsing**, I wanted to experiment by creating my own argument parser by hand, in  the future I'll probably move argument parsing to one of those modules for stability._
