#!/usr/bin/python

import argparse
import string

def caesar_shift(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result

def main():
    parser = argparse.ArgumentParser(
        description="Caesar Cipher Brute Force Tool"
    )
    parser.add_argument(
        "-c", "--ciphertext",
        required=True,
        help="Ciphertext to brute force"
    )

    args = parser.parse_args()

    print("[+] Brute-forcing Caesar cipher...\n")

    for shift in range(1, 26):
        plaintext = caesar_shift(args.ciphertext, shift)
        print(f"Shift {shift:2d}: {plaintext}")

if __name__ == "__main__":
    main()
