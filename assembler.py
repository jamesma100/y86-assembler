#!/usr/bin/env python3

import argparse

REG = {
    "%rax": 0x0,
    "%rcx": 0x1,
    "%rdx": 0x2,
    "%rbx": 0x3,
    "%rsp": 0x4,
    "%rbp": 0x5,
    "%rsi": 0x6,
    "%rdi": 0x7,
    "%r8": 0x8,
    "%r9": 0x9,
    "%r10": 0xA,
    "%r11": 0xB,
    "%r12": 0xC,
    "%r13": 0xD,
    "%r14": 0xE,
}

OP = {
    # Simple operators
    "addq": 0x60,
    "subq": 0x61,
    "andq": 0x62,
    "xorq": 0x63,
    # JMP instructions
    "jmp": 0x70,
    "jle": 0x71,
    "jl": 0x72,
    "je": 0x73,
    "jne": 0x74,
    "jge": 0x75,
    "jg": 0x76,
    # MOV instructions
    "rrmovq": 0x20,
    "cmovle": 0x21,
    "cmovl": 0x22,
    "cmove": 0x23,
    "cmovne": 0x24,
    "cmovge": 0x25,
    "cmovg": 0x26,
    "irmovq": 0x30F,
    "rmmovq": 0x40,
    "mrmovq": 0x50,
}


def parse_contents(filename: str, out: str):
    with open(filename, "r") as f:
        encodings = []
        for line in f.readlines():
            line = line.strip()
            instr, reg_and_word = line.split(" ")
            word, reg = reg_and_word.split(",")

            encoding = OP[instr]

            if instr == "irmovq":
                encoding = encoding * 16 + int(f"{REG[reg]:#0{4}x}", 16)
                word = word[1:]
                hex_num = f"{int(word):#0{18}x}"
                ba = bytearray.fromhex(hex_num[2:])
                ba.reverse()
                s = "".join(format(x, "02x") for x in ba)
                encoding = encoding * 16**16 + int(s, 16)
            elif instr == "rrmovq":
                encoding = encoding * 16 + REG[word]
                encoding = encoding * 16 + REG[reg]

            encodings.append(hex(encoding))

        with open(out, "w") as f:
            for encoding in encodings:
                f.write(encoding[2:] + "\n")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="file name of assembly code input")
    parser.add_argument("-o", "--out", help="file name of binary code output")
    return parser.parse_args()


def main():
    args = parse_args()
    parse_contents(args.file, args.out)


if __name__ == "__main__":
    main()
