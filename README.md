# Crazcalm

The goal of this repo it to see what I can build while only using the standard library. For reasons that I do not feel like explaining, I now program on a computer where I am not allowed to install and third party packages. As annoying as that is, I do not want that to limit my ability to customize my machine!

## Tests

I am using a python package file structure, so you much install the package (please use edit mode) in order to run the tests.

```
python -m pip install -e .
```

### Test command

```
python -m unittest discover .\tests\
```
## Bin

### Making windows commands

This still seems like magic to me, but added my bin directory to my PATH environment variable, I set the default application to open python files to my python.exe and then I created a `touch.cmd` file to wrap my `touch.py` file.

```
@py "%~dp0touch.py" %*
```

I had chatgpt make me a bash to windows cmd document that I put in the docs folder than kind of explains it. Essentially, this allows me to call `py` my `touch.py` file and the `%~d0` expands the path while the `%*` allows me to pass arugments to my python script.

This means that I can write `touch hellworld.txt` in powershell and a file is now created!!!

## Notes:
### Min Python Version
As of right now, the self referencing type hinting is forcing this to be python 3.14.