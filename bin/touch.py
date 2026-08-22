import sys
from pathlib import Path

def main():
    import pdb
    pdb.set_trace()
    for file in sys.argv[1:]:
        Path(file).touch()


if __name__ == "__main__":
    main()
