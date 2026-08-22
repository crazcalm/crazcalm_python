# Bash to Windows CMD Translation Guide

A practical reference for translating common Bash shell patterns into Windows CMD/batch syntax, especially when creating `.cmd` wrappers for Python programs.

## 1. Basic mental model

| Bash | Windows CMD |
|---|---|
| `script.sh` | `script.cmd` / `script.bat` |
| `$1` | `%1` |
| `$2` | `%2` |
| `$@` | `%*` |
| `$0` | `%0` |
| `$PATH` | `%PATH%` |
| `export VAR=value` | `set "VAR=value"` |
| `$VAR` | `%VAR%` |
| `"$file"` | `"%file%"` |
| `$(command)` | `for /f ...` |
| `if ...` | `if ...` |
| `&&` | `&&` |
| `||` | `||` |
| `;` | `&` |
| `command1 ; command2` | `command1 & command2` |
| `command1 \| command2` | `command1 \| command2` |

CMD is considerably more limited than Bash, so some Bash constructs do not have a direct one-to-one equivalent.

---

## 2. Script arguments

### Bash

```bash
#!/bin/bash

echo "Script: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
```

### CMD

```bat
@echo off

echo Script: %0
echo First argument: %1
echo Second argument: %2
echo All arguments: %*
```

For:

```powershell
myscript.cmd hello world
```

the arguments are:

```text
%0 = myscript.cmd
%1 = hello
%2 = world
%* = hello world
```

### Important

The closest CMD equivalent to Bash's:

```bash
"$@"
```

is:

```bat
%*
```

This is especially useful when writing a wrapper around another program:

```bat
@py "%~dp0program.py" %*
```

---

## 3. `%0` and `%~dp0`

In Bash:

```bash
$0
```

refers to the script's invocation name.

In CMD:

```bat
%0
```

refers to the batch file's path/name.

CMD provides modifiers for extracting parts of a path.

The particularly useful one is:

```bat
%~dp0
```

which means:

- `%0` — batch file
- `~` — remove surrounding quotes
- `d` — drive
- `p` — path

Therefore:

```bat
%~dp0
```

means:

> The drive and directory containing this batch file.

For example, if the batch file is:

```text
C:\Users\Marcus\bin\touch.cmd
```

then:

```bat
%~dp0
```

produces:

```text
C:\Users\Marcus\bin\
```

This allows a wrapper to locate a Python script relative to itself rather than relative to the current working directory.

### Bash equivalent

A Bash launcher might use:

```bash
SCRIPT_DIR="$(dirname "$0")"
python "$SCRIPT_DIR/touch.py" "$@"
```

The CMD equivalent is:

```bat
@py "%~dp0touch.py" %*
```

---

## 4. CMD path modifiers

Given an argument such as:

```text
C:\Users\Marcus\bin\hello.txt
```

CMD provides modifiers such as:

| Syntax | Meaning |
|---|---|
| `%~f1` | Fully qualified path |
| `%~d1` | Drive |
| `%~p1` | Path |
| `%~n1` | Filename without extension |
| `%~x1` | Extension |
| `%~dp1` | Drive + path |

These modifiers can be used with `%0`, `%1`, `%2`, etc.

For example:

```bat
%~dp0
```

means the drive and path of the batch file.

```bat
%~dp1
```

means the drive and path of the first argument.

---

## 5. Variables

### Bash

```bash
NAME="Marcus"
echo "$NAME"
```

### CMD

```bat
set "NAME=Marcus"
echo %NAME%
```

Prefer:

```bat
set "VARIABLE=value"
```

rather than:

```bat
set VARIABLE=value
```

The quoted form prevents accidental trailing spaces from becoming part of the variable's value. The quotes themselves are not stored in the variable.

---

## 6. Environment variables

### Bash

```bash
export MYAPP=/some/path
```

### CMD

```bat
set "MYAPP=C:\some\path"
```

`set` changes the variable for the current CMD process and programs it launches.

For a persistent Windows environment variable:

```cmd
setx MYAPP "C:\some\path"
```

You can also set persistent environment variables through Windows' Environment Variables GUI.

### PATH

Bash:

```bash
export PATH="$HOME/bin:$PATH"
```

CMD:

```bat
set "PATH=C:\Users\Marcus\bin;%PATH%"
```

The PATH separator is:

```text
Bash: :
CMD:  ;
```

For example:

```text
Bash:
/usr/local/bin:/usr/bin:/bin

Windows:
C:\Windows\System32;C:\Windows;C:\Python314;...
```

---

## 7. Quoting

Quoting is important in both shells, especially for paths containing spaces.

### Bash

```bash
python "$file"
```

### CMD

```bat
py "%file%"
```

If:

```text
file=C:\My Files\hello.txt
```

then:

```bat
py %file%
```

can be interpreted incorrectly because of the space.

Prefer:

```bat
py "%file%"
```

A good general rule in CMD is:

```bat
"%VARIABLE%"
```

when passing a variable containing a path to another command.

---

## 8. Command chaining

### Bash

```bash
command1; command2
```

### CMD

```bat
command1 & command2
```

For example:

```bash
mkdir output; cd output
```

becomes:

```bat
mkdir output & cd output
```

### `&&`

These are essentially the same:

Bash:

```bash
mkdir output && cd output
```

CMD:

```bat
mkdir output && cd output
```

The second command runs only if the first succeeds.

### `||`

Also similar:

```bash
command1 || command2
```

---

## 9. Pipes

Pipes work similarly:

### Bash

```bash
command1 | command2
```

### CMD

```bat
command1 | command2
```

Example:

```cmd
dir | findstr ".py"
```

---

## 10. Exit status

### Bash

```bash
$?
```

### CMD

```bat
%ERRORLEVEL%
```

Example:

```bat
somecommand

echo %ERRORLEVEL%
```

You can test it:

```bat
if %ERRORLEVEL% neq 0 (
    echo Something failed
)
```

Bash equivalent:

```bash
if [ $? -ne 0 ]; then
    echo "Something failed"
fi
```

---

## 11. `if`

### Bash

```bash
if [ "$NAME" = "Marcus" ]; then
    echo "Hello"
fi
```

### CMD

```bat
if "%NAME%"=="Marcus" (
    echo Hello
)
```

A common CMD idiom is:

```bat
if "%VARIABLE%"=="value" (
    ...
)
```

rather than:

```bat
if %VARIABLE%==value (
    ...
)
```

The quotes help when the variable is empty or contains spaces.

---

## 12. Testing for files

### Bash

```bash
if [ ! -f "$file" ]; then
    echo "File doesn't exist"
fi
```

### CMD

```bat
if not exist "%file%" (
    echo File doesn't exist
)
```

---

## 13. Loops

### Bash

```bash
for file in *.txt; do
    echo "$file"
done
```

### CMD

Inside a `.cmd` or `.bat` file:

```bat
for %%f in (*.txt) do (
    echo %%f
)
```

### Important CMD gotcha

At an interactive CMD prompt, use one `%`:

```cmd
for %f in (*.txt) do echo %f
```

Inside a batch file, use two `%` characters:

```bat
for %%f in (*.txt) do echo %%f
```

---

## 14. Reading arguments in a loop

### Bash

```bash
for file in "$@"; do
    touch "$file"
done
```

### CMD

A basic equivalent is:

```bat
for %%f in (%*) do (
    echo %%f
)
```

CMD's argument/quoting rules are more complicated than Bash's, so it is often preferable to pass the arguments to a program that already has robust argument parsing.

For example, a Python wrapper can simply forward everything:

```bat
@py "%~dp0touch.py" %*
```

---

## 15. Functions and subroutines

CMD does not have functions in quite the same way Bash does.

### Bash

```bash
function hello() {
    echo "Hello"
}

hello
```

### CMD

Labels can be used as subroutines:

```bat
@echo off

call :hello
exit /b

:hello
echo Hello
exit /b
```

Arguments can also be passed:

```bat
@echo off

call :hello Marcus
exit /b

:hello
echo Hello %1
exit /b
```

---

## 16. Comments

### Bash

```bash
# This is a comment
```

### CMD

Official comment syntax:

```bat
rem This is a comment
```

You will also frequently see:

```bat
:: This is commonly used as a comment
```

`rem` is the official mechanism; `::` is a common batch-file convention.

---

## 17. Shebang vs. Windows launcher

Bash scripts commonly use a shebang:

```bash
#!/usr/bin/env python3
```

The shebang tells Unix-like systems which interpreter should run the script.

A Windows `.cmd` file explicitly invokes the program:

```bat
@py "%~dp0touch.py" %*
```

So a Bash launcher:

```bash
#!/bin/bash
python3 "$(dirname "$0")/touch.py" "$@"
```

is conceptually similar to this CMD launcher:

```bat
@py "%~dp0touch.py" %*
```

---

# 18. Python command wrappers

This is particularly useful for maintaining a personal Windows `bin` directory.

Suppose you have:

```text
C:\Users\Marcus\bin\
    touch.cmd
    touch.py
    rename.cmd
    rename.py
```

`touch.cmd`:

```bat
@py "%~dp0touch.py" %*
```

`rename.cmd`:

```bat
@py "%~dp0rename.py" %*
```

Add the `bin` directory to your Windows `PATH`.

You can then run:

```powershell
touch foo.txt
touch foo.txt bar.txt
rename old.txt new.txt
```

The execution chain is:

```text
PowerShell
    ↓
finds touch.cmd on PATH
    ↓
Windows executes touch.cmd
    ↓
%~dp0 finds touch.py beside the wrapper
    ↓
%* forwards all arguments
    ↓
py runs touch.py
    ↓
Python receives the arguments in sys.argv
```

This is a simple and effective way to make a collection of Python scripts behave like native Windows command-line utilities.

---

# 19. The most important CMD gotchas

If you are coming from Bash, these are worth memorizing.

### Variables

Bash:

```bash
$VAR
```

CMD:

```bat
%VAR%
```

### All arguments

Bash:

```bash
"$@"
```

CMD:

```bat
%*
```

### Script location

Bash commonly uses:

```bash
dirname "$0"
```

CMD:

```bat
%~dp0
```

### Command separator

Bash:

```bash
command1; command2
```

CMD:

```bat
command1 & command2
```

### PATH separator

Bash:

```text
:
```

CMD:

```text
;
```

### Variables containing paths

Prefer:

```bat
"%FILE%"
```

rather than:

```bat
%FILE%
```

### Batch-file `for` variables

Inside a batch file:

```bat
%%f
```

At an interactive CMD prompt:

```cmd
%f
```

### Exit from a batch file

Use:

```bat
exit /b
```

or:

```bat
exit /b 0
```

---

# 20. Useful resources

### Microsoft

[Windows Commands — Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands)

The official reference for Windows CMD commands.

[Microsoft Learn — `call` / Batch parameters](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/call)

Particularly useful for `%0`, `%1`, `%*`, `%~dp0`, and the other batch-parameter modifiers.

[Microsoft Learn — `for`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/for)

Reference for CMD's `for` loops.

[Microsoft Learn — `if`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/if)

Reference for conditional execution.

### Other reference

[SS64 — Windows CMD Syntax](https://ss64.com/nt/)

A convenient reference for CMD syntax and commands.

---

# 21. What to learn first

You do not need to learn all of CMD to make useful Python command wrappers.

For a personal `bin` directory, focus on these topics in roughly this order:

1. `%1`, `%2`, `%*` — command-line arguments
2. `%~dp0` — locating files relative to a batch script
3. `set` and `%VAR%` — variables
4. Quoting paths
5. `PATH`
6. `if`
7. `for`
8. `call`
9. `exit /b`
10. `ERRORLEVEL`

Once you understand those, you can build most simple Windows command wrappers without needing to become a full-time CMD programmer.
