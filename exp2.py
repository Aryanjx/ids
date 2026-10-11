import math
import struct


class MD5:
    """A pure Python implementation of the MD5 hash algorithm (RFC 1321)."""

    # Per-round shift amounts
    _SHIFTS = [
        7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
        5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
        4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,
    ]

    # Precomputed sine constants: K[i] = floor(2^32 * abs(sin(i + 1)))
    _K = [int(abs(math.sin(i + 1)) * (1 << 32)) & 0xFFFFFFFF for i in range(64)]

    @staticmethod
    def _left_rotate(x: int, c: int) -> int:
        """Rotate a 32-bit integer left by c bits."""
        return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

    @classmethod
    def hash(cls, message: bytes) -> str:
        """Computes the hex digest of the given bytes message."""
        # Initial state (A, B, C, D) in little-endian format
        a0 = 0x67452301
        b0 = 0xEFCDAB89
        c0 = 0x98BADCFE
        d0 = 0x10325476

        # --- Step 1 & 2: Padding and appending length ---
        msg_len_bits = (len(message) * 8) & 0xFFFFFFFFFFFFFFFF

        # Append '1' bit followed by '0' bits until length ≡ 448 (mod 512) bits
        padded_msg = bytearray(message)
        padded_msg.append(0x80)  # 0b10000000
        while len(padded_msg) % 64 != 56:
            padded_msg.append(0x00)

        # Append original 64-bit length in little-endian
        padded_msg += struct.pack("<Q", msg_len_bits)

        # --- Step 3 & 4: Process message in 512-bit (64-byte) blocks ---
        for offset in range(0, len(padded_msg), 64):
            block = padded_msg[offset : offset + 64]
            # Unpack 64 bytes into sixteen 32-bit little-endian words
            M = list(struct.unpack("<16I", block))

            A, B, C, D = a0, b0, c0, d0

            # 64 Operations divided into 4 rounds of 16 operations each
            for i in range(64):
                if 0 <= i <= 15:
                    F = (B & C) | ((~B) & D)
                    g = i
                elif 16 <= i <= 31:
                    F = (D & B) | ((~D) & C)
                    g = (5 * i + 1) % 16
                elif 32 <= i <= 47:
                    F = B ^ C ^ D
                    g = (3 * i + 5) % 16
                elif 48 <= i <= 63:
                    F = C ^ (B | (~D))
                    g = (7 * i) % 16

                F = (F + A + cls._K[i] + M[g]) & 0xFFFFFFFF
                A = D
                D = C
                C = B
                B = (B + cls._left_rotate(F, cls._SHIFTS[i])) & 0xFFFFFFFF

            # Add block hash to result so far
            a0 = (a0 + A) & 0xFFFFFFFF
            b0 = (b0 + B) & 0xFFFFFFFF
            c0 = (c0 + C) & 0xFFFFFFFF
            d0 = (d0 + D) & 0xFFFFFFFF

        # --- Step 5: Output (convert state variables to little-endian hex) ---
        raw_hash = struct.pack("<4I", a0, b0, c0, d0)
        return raw_hash.hex()


# --- Verification Example ---
if __name__ == "__main__":
    import hashlib

    test_input = b"The quick brown fox jumps over the lazy dog"

    custom_md5 = MD5.hash(test_input)
    builtin_md5 = hashlib.md5(test_input).hexdigest()

    print(f"Custom MD5  : {custom_md5}")
    print(f"Built-in MD5: {builtin_md5}")
    print(f"Match       : {custom_md5 == builtin_md5}")