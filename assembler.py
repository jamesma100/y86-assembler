#!/usr/bin/env python3

import argparse
import bitstring
from enum import Enum

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
    "halt": 0x00,
    "nop": 0x10,
    "call": 0x80,
    "ret": 0x90,
    "pushq": 0xA0,
    "popq": 0xB0,
}


class CC(Enum):
    ZF = 0
    SF = 1
    OF = 2


HEXBASE = 16
CC = 0
RSP = 0x100


def encode_word(word: str) -> int:
    """Given a hex word (without the 0x prefix) as a string, returns
    the little endian byte representation as an integer.
    """
    ba = bytearray.fromhex(word)
    ba.reverse()
    s = "".join(format(x, "02x") for x in ba)
    return int(s, HEXBASE)


def update_encoding(encoding: int, shift: int, val: int) -> int:
    """Updates encoding given a value and hex shift (0 means 1 left shift)"""
    return encoding * (HEXBASE**HEXBASE**shift) + val


def parse_contents(filename: str, out: str):
    """Compile contents of y86_64 assembly into its byte encoding"""
    global RSP
    loop_addr = 0x100
    with open(filename, "r") as f:
        encodings = []
        for line in f.readlines():
            line = line.strip()
            split0 = line.split(" ")
            instr = split0[0]
            operand0, operand1 = None, None
            if len(split0) == 2:
                operands = split0[1].split(",")
                operand0 = operands[0]
                if len(operands) == 2:
                    operand1 = operands[1]

            if instr == "loop":
                loop_addr = RSP
                encodings.append((hex(RSP), ""))
                continue
            encoding = OP[instr]

            if instr in ["halt", "nop", "ret"]:
                pass
            elif instr == "irmovq":
                encoding = encoding * HEXBASE + int(f"{REG[operand1]:#0{4}x}", HEXBASE)
                operand0 = operand0[1:]
                hex_word = f"{int(operand0):#0{HEXBASE + 2}x}"
                encoding = encoding * HEXBASE**16 + encode_word(hex_word[2:])
            elif instr in ["rrmovq", "addq", "subq", "andq", "xorq"]:
                encoding = encoding * HEXBASE + REG[operand0]
                encoding = encoding * HEXBASE + REG[operand1]
            elif instr == "rmmovq":
                operand1 = operand1.split("(")
                word, operand1 = int(operand1[0]), operand1[1][:-1]
                encoding = encoding * HEXBASE + REG[operand0]
                encoding = encoding * HEXBASE + REG[operand1]
                hex_word = bitstring.BitArray(f"int:64={word}").hex
                encoding = encoding * HEXBASE**16 + encode_word(hex_word)
            elif instr == "mrmovq":
                operand0 = operand0.split("(")
                word, operand0 = int(operand0[0]), operand0[1][:-1]
                encoding = encoding * HEXBASE + REG[operand0]
                encoding = encoding * HEXBASE + REG[operand1]
                hex_word = bitstring.BitArray(f"int:64={word}").hex
                encoding = encoding * HEXBASE**16 + encode_word(hex_word)
            elif instr in ["pushq", "popq"]:
                encoding = encoding * HEXBASE**2 + REG[operand0] * HEXBASE + 0xF
            elif instr == "jmp":
                word = f"{loop_addr:#0{16 + 2}x}"
                encoding = encoding * HEXBASE**16 + encode_word(word[2:])

            encodings.append((hex(RSP), hex(encoding)))
            RSP += (len(hex(encoding)) - 2) // 2

        with open(out, "w") as f:
            for addr, encoding in encodings:
                f.write(addr + ": " + encoding[2:] + "\n")


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
