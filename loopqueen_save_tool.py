#!/usr/bin/env python3
"""
LoopQueen (Escape Dungeon 3) save file decrypt/encrypt tool.

Algorithm (extracted from Assembly-CSharp.dll, EncryptTools class):
    Cipher:  AES-256 (RijndaelManaged, 256-bit key)
    Mode:    ECB  (no IV)
    Padding: PKCS7
    Key:     UTF-8 bytes of the literal string
             "07872189057434672257123328872369"
    Wrapper: standard Base64 (Convert.ToBase64String / FromBase64String)

Install dependency first:
    pip install pycryptodome
    pip install Crypto

Usage:
    python3 loopqueen_save_tool.py decrypt <in.json> [out.json]
    python3 loopqueen_save_tool.py encrypt <in.json> [out.json]

decrypt: reads an encrypted save file, writes pretty-printed JSON.
encrypt: reads pretty-printed (or minified) JSON, writes an encrypted
         save file in the game's format -- use this to write edited
         values back so the game will load them.

Always back up your original save files before overwriting them.
"""
import sys
import base64
import json
from Crypto.Cipher import AES

KEY = "07872189057434672257123328872369".encode("utf-8")


def decrypt_text(blob: str) -> str:
    ct = base64.b64decode(blob.strip())
    cipher = AES.new(KEY, AES.MODE_ECB)
    raw = cipher.decrypt(ct)
    pad = raw[-1]
    if 0 < pad <= 16 and raw[-pad:] == bytes([pad]) * pad:
        raw = raw[:-pad]
    return raw.decode("utf-8")


def encrypt_text(text: str) -> str:
    data = text.encode("utf-8")
    pad = 16 - (len(data) % 16)
    data += bytes([pad]) * pad
    cipher = AES.new(KEY, AES.MODE_ECB)
    ct = cipher.encrypt(data)
    return base64.b64encode(ct).decode("ascii")


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("decrypt", "encrypt"):
        print(__doc__)
        sys.exit(1)

    mode, in_path = sys.argv[1], sys.argv[2]
    out_path = sys.argv[3] if len(sys.argv) > 3 else None

    with open(in_path, "r", encoding="utf-8") as f:
        content = f.read()

    if mode == "decrypt":
        text = decrypt_text(content)
        parsed = json.loads(text)  # validates + lets us pretty-print
        result = json.dumps(parsed, indent=2, ensure_ascii=False)
    else:
        # Re-minify isn't required, but keeping it close to what the
        # game itself writes (CRLF line endings) avoids surprises.
        parsed = json.loads(content)
        text = json.dumps(parsed, indent=4)
        result = encrypt_text(text)

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Wrote {out_path}")
    else:
        print(result)


if __name__ == "__main__":
    main()
