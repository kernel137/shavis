<h1 align="center">sha256vis</h1>
A proof-of-concept C++ CLI tool that takes an SHA256 hash as input and generates an image.
Made using Pillow (forked from PIL).

Hash of previous commit:
<p align="center">
  <img src="hash_of_prev_commit.png">
</p>

Currently working on packaging and distributing to PyPI.

- You can directly pipe the output of `git rev-parse HEAD` into `sha256vis -g` to 
visualize the hash of the previous commit in your current local git repository.
```sh
git rev-parse HEAD | sha256vis -g
```