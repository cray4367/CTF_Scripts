#!/usr/bin/python3

import argparse

# ---------------- RSA CORE ----------------

def power(base, expo, m):
    res = 1
    base = base % m
    while expo > 0:
        if expo & 1:
            res = (res * base) % m
        base = (base * base) % m
        expo //= 2
    return res

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modInverse(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return None

def encrypt(m, e, n):
    return power(m, e, n)

def decrypt(c, d, n):
    return power(c, d, n)

# ---------------- STRING ENCODING ----------------

def string_to_int(s):
    return int.from_bytes(s.encode(), "big")

def int_to_string(i):
    length = (i.bit_length() + 7) // 8
    return i.to_bytes(length, "big").decode()

# ---------------- MAIN ----------------

def main():
    parser = argparse.ArgumentParser(
        description="RSA Encrypt & Decrypt with string support"
    )

    parser.add_argument("-p", type=int, required=True, help="Prime p")
    parser.add_argument("-q", type=int, required=True, help="Prime q")
    parser.add_argument("-e", type=int, required=True, help="Public exponent e")
    parser.add_argument("-m", help="Message to encrypt (string)")
    parser.add_argument("-c", type=int, help="Ciphertext to decrypt (decimal)")

    args = parser.parse_args()

    # Compute RSA values
    n = args.p * args.q
    phi = (args.p - 1) * (args.q - 1)

    if gcd(args.e, phi) != 1:
        print("[!] Error: e is not coprime with phi(n)")
        return

    d = modInverse(args.e, phi)
    if d is None:
        print("[!] Error: Failed to compute d")
        return

    print(f"[+] Public Key (e, n): ({args.e}, {n})")
    print(f"[+] Private Key (d, n): ({d}, {n})")

    # Encrypt string
    if args.m is not None:
        m_int = string_to_int(args.m)

        if m_int >= n:
            print("[!] Error: Message too large for modulus n")
            return

        c = encrypt(m_int, args.e, n)
        print("[+] Ciphertext (decimal):", c)

    # Decrypt ciphertext
    if args.c is not None:
        m_int = decrypt(args.c, d, n)
        try:
            print("[+] Decrypted Message:", int_to_string(m_int))
        except:
            print("[!] Decrypted data is not valid UTF-8")

    if args.m is None and args.c is None:
        print("[!] Error: Provide -m (encrypt) or -c (decrypt)")

if __name__ == "__main__":
    main()
