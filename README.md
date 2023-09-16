# y86-assembler
Compile your y86_64 assembly code down to its byte encoding!

## Use cases
- popular languages like Java, C++, etc. don't serve your needs, so you need to write assembly
- you have a y86 computer and want to use it

## Actual use cases
- 

## Usage
```
$ python3 -m venv venv
$ pip install -r requirements.txt
$ ./assembler.py -f myfile.asm -o myfile
```
Note: address space starts at `0x100`

## Example
To produce the `example` file run the above setup then
```
$ ./assembler.py -f example.asm -o example
```
Voila
```
$ cat example
0x100: 30f30f00000000000000
0x10a: 2031
0x10c:
0x10c: 4013fdffffffffffffff
0x116: 6031
0x118: 700c01000000000000
```
