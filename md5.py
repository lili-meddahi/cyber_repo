import math
import struct

# Original message
plTxt = "Alright, but apart from the sanitation, the medicine, education, wine, public order, irrigation, roads, the fresh-water system, and public health, what have the Romans ever done for us?"
plTxtBytes = bytes(plTxt, "utf-8")

# Add a single '1' bit and calculate padding
plTxtBytes += b'\x80'  # Append 0b10000000
msgLen = len(plTxtBytes) * 8  # Length of message in bits
tmp = msgLen % 512
padLen = (448 - tmp) % 512  # Calculate padding to reach 448 bits mod 512
plTxtBytes += b'\x00' * (padLen // 8)  # Add zero bytes

# Append original message length as a 64-bit big-endian integer
plTxtBytes += msgLen.to_bytes(8, "big")

# Verify the padded message
print(f"Padded message length (bits): {len(plTxtBytes) * 8}")

# Constants for the hash (MD5 example)
A = 0x67452301
B = 0xefcdab89
C = 0x98badcfe
D = 0x10325476

# Define basic functions
def F(x, y, z):
    return (x & y) | (~x & z)

# Rotate left (cyclic shift)
def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

# Process each 512-bit block
block_size = 64 
for i in range(0, len(plTxtBytes), block_size):
    block = plTxtBytes[i:i + block_size]
    
    # Break block into 16 32-bit words
    M = [int.from_bytes(block[j:j + 4], "little") for j in range(0, block_size, 4)]
    
    # Initialize hash value for this block
    a, b, c, d = A, B, C, D
    
    # Perform one round (example for first 16 operations)
    for j in range(16):
        k = j  
        s = [7, 12, 17, 22][j % 4]  
        t = int((2**32) * abs(math.sin(j + 1))) & 0xFFFFFFFF  
        f = F(b, c, d)
        temp = (a + f + M[k] + t) & 0xFFFFFFFF
        a, b, c, d = d, (b + left_rotate(temp, s)) & 0xFFFFFFFF, b, c
    
    # Update hash values (this would continue for all rounds)
    A = (A + a) & 0xFFFFFFFF
    B = (B + b) & 0xFFFFFFFF
    C = (C + c) & 0xFFFFFFFF
    D = (D + d) & 0xFFFFFFFF

# Final hash value (concatenate results)
digest = struct.pack("<4I", A, B, C, D)
print(f"Hash (MD5-like): {digest.hex()}")
