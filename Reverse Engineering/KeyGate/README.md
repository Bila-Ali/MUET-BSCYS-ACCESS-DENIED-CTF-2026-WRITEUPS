#KeyGate

**Category:** Reverse Engineering

**Difficulty:** Easy–Medium

**Author:** Bilawal Ali

**Event:** AccessDenied CTF 2026

**Tools:** `file`, `objdump`, Ghidra, Python

**Flag:** `MUET{Bhai_License_Kahan_Gaya}`

---

## Challenge Description

A protected binary implements a simple secure login mechanism. The program requires a secret key before it reveals the flag.

The key and flag are not stored in plaintext. Instead, both values are encrypted using a single-byte XOR operation. The objective is to reverse-engineer the binary, recover the XOR logic, decrypt the embedded key, and use it to obtain the flag.

### Provided File



# Solution

## Step 1 — Initial Reconnaissance

First, make the binary executable:

```bash
chmod +x keygate
```

Then identify the file type:

```bash
file keygate
```

Output:

```text
keygate: ELF 64-bit LSB executable, x86-64, dynamically linked, stripped
```

The binary is:

* 64-bit
* x86-64
* Dynamically linked
* Stripped

Because the binary is stripped, useful function names are not available. However, stripping does not remove constant data stored inside sections such as `.rodata`.

---

## Step 2 — Execute the Binary

Run the program:

```bash
./keygate
```

The binary displays:

```text
============================
       Secure Login
============================
Enter Key:
```

The program expects a key before proceeding.

A basic `strings` search does not reveal the actual flag or key because the sensitive values are stored in an encoded form.

This indicates that static inspection of the binary's data is required.

---

## Step 3 — Inspect `.rodata`

The read-only data section can be dumped using:

```bash
objdump -s -j .rodata keygate
```

Relevant output:

```text
Contents of section .rodata:
 402000 01000200 00000000 00000000 00000000  ................
 402010 67671706 160c0665 65675500 0a000000  gg.....eegU.....
 402020 18001001 2e173d34 3c0a193c 36303b26  ......=4<..<60;&
 402030 300a1e34 3d343b0a 12342c34 28550000  0..4=4;..4,4(U..
```

Two byte sequences are particularly interesting.

### Encrypted Key

```text
67 67 17 06 16 0C 06 65 65 67 55
```

### Encrypted Flag

```text
18 00 10 01 2E 17 3D 34 3C 0A 19 3C
36 30 3B 26 30 0A 1E 34 3D 34 3B 0A
12 34 2C 34 28 55
```

Both sequences terminate with:

```text
55
```

This is an important clue.

---

## Step 4 — Identify the XOR Key

The binary uses a single-byte XOR operation.

The final byte of each encrypted string is:

```text
0x55
```

If the original C string ends with a null byte:

```text
0x00
```

then:

```text
0x00 ^ 0x55 = 0x55
```

Therefore, the trailing `0x55` strongly suggests that the XOR key is:

```text
0x55
```

---

## Step 5 — Confirm the XOR Logic

The same behavior can be confirmed by opening the binary in Ghidra and examining the relevant functions.

The decompiled logic follows the pattern:

```c
void decrypt(
    const unsigned char *encrypted,
    int len,
    char *decrypted
) {
    for (int i = 0; i < len; i++) {
        decrypted[i] = encrypted[i] ^ 0x55;
    }

    decrypted[len] = '\0';
}
```

The important operation is:

```c
encrypted[i] ^ 0x55
```

The program uses this operation to decrypt both the stored key and the stored flag.

There is no complex cryptography or significant obfuscation involved. It is simply a single-byte XOR transformation.

---

# Step 6 — Decrypt the Key

The encrypted key is:

```text
67 67 17 06 16 0C 06 65 65 67 55
```

Using:

```text
decrypted_byte = encrypted_byte ^ 0x55
```

we can decrypt it with Python:

```python
enc_key = [
    0x67, 0x67, 0x17, 0x06, 0x16,
    0x0C, 0x06, 0x65, 0x65, 0x67, 0x55
]

key = ''.join(chr(b ^ 0x55) for b in enc_key)

print(key)
```

Output:

```text
22BSCYS002
```

The final byte represents the decoded null terminator.

### Recovered Key

```text
22BSCYS002
```

---

# Step 7 — Decrypt the Flag

The encrypted flag bytes are:

```text
18 00 10 01 2E 17 3D 34 3C 0A 19 3C
36 30 3B 26 30 0A 1E 34 3D 34 3B 0A
12 34 2C 34 28 55
```

Decrypt them using the same XOR key:

```python
enc_flag = [
    0x18, 0x00, 0x10, 0x01, 0x2E, 0x17,
    0x3D, 0x34, 0x3C, 0x0A, 0x19, 0x3C,
    0x36, 0x30, 0x3B, 0x26, 0x30, 0x0A,
    0x1E, 0x34, 0x3D, 0x34, 0x3B, 0x0A,
    0x12, 0x34, 0x2C, 0x34, 0x28, 0x55
]

flag = ''.join(chr(b ^ 0x55) for b in enc_flag)

print(flag)
```

Output:

```text
MUET{Bhai_License_Kahan_Gaya}
```

The final decoded byte is the null terminator.

---

# Step 8 — Verify the Recovered Key

The recovered key can be tested against the original binary:

```bash
./keygate
```

Enter:

```text
22BSCYS002
```

The program responds:

```text
============================
       Secure Login
============================
Enter Key: 22BSCYS002
Access Granted!
Flag: MUET{Bhai_License_Kahan_Gaya}
```

This confirms the recovered key and flag.

---

# Intended Solution Path

The complete investigation can be summarized as:

```text
keygate
   |
   v
file
   |
   v
ELF 64-bit, stripped
   |
   v
Run binary
   |
   v
Secure Login
   |
   v
Inspect .rodata
   |
   v
Identify encrypted byte arrays
   |
   v
Notice trailing 0x55
   |
   v
Identify XOR key = 0x55
   |
   +-------------------+
   |                   |
   v                   v
Encrypted Key      Encrypted Flag
   |                   |
   v                   v
XOR 0x55           XOR 0x55
   |                   |
   v                   v
22BSCYS002         MUET{Bhai_License_Kahan_Gaya}
   |
   v
Verify against binary
```

---

# Flag

```text
MUET{Bhai_License_Kahan_Gaya}
```

---

# Key Takeaways

### 1. Stripped Does Not Mean Empty

A stripped binary loses useful symbol names, but important constants and embedded data remain.

When reversing a stripped binary, inspect:

* `.rodata`
* `.data`
* Embedded strings
* Constant byte arrays
* References from code to those regions

### 2. Look for XOR Patterns

Single-byte XOR is common in beginner reverse-engineering challenges because it is simple to implement but easy to reverse.

The same operation decrypts the data:

```text
C = P XOR K
P = C XOR K
```

Therefore, once the XOR key is known, no separate decryption algorithm is required.

### 3. Null Terminators Can Reveal the XOR Key

The encrypted strings end with:

```text
0x55
```

A normal C string ends with:

```text
0x00
```

Since:

```text
0x00 XOR 0x55 = 0x55
```

the terminator itself provides a useful clue about the XOR key.

### 4. Verify Static Findings Dynamically

Recovering a key from static analysis is only part of the investigation.

Whenever possible, use the recovered value against the original binary to confirm that:

* The key is correct
* The decryption logic is correct
* The recovered flag is correct
* No length or termination issues were overlooked

---

## Conclusion

The challenge uses a simple single-byte XOR scheme to hide both the authentication key and the flag.

The essential workflow is:

```text
Inspect binary
    ↓
Find encrypted data
    ↓
Identify XOR 0x55
    ↓
Decrypt key
    ↓
22BSCYS002
    ↓
Decrypt flag
    ↓
MUET{Bhai_License_Kahan_Gaya}
```

Final flag:

```text
MUET{Bhai_License_Kahan_Gaya}
```
