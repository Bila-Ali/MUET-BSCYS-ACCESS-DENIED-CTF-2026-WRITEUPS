# Crack the Vault

**Category:** Cryptography
**Difficulty:** Medium
**Author:** Bilawal Ali

## Challenge Description

A sensitive file containing the flag was encrypted and stored inside a password-protected ZIP archive. The password is short, but no direct password hint was provided.

The objective is to analyze the archive, determine the possible password space, recover the password using brute-force techniques, and extract the flag.

## Hint

> Taala chhota hai, lekin raaz bara hai.
> Password mein sirf 3 numbers hain.

## Files

| File                 | Description                                              |
| -------------------- | -------------------------------------------------------- |
| `encrypted_flag.zip` | Password-protected archive containing the flag           |
| `zip-crack.py`       | Python script for brute-forcing the three-digit password |

## Analysis

The hint indicates that the password consists of exactly three numeric digits.

Each digit can contain a value from `0` to `9`, resulting in:

```text
10 × 10 × 10 = 1,000
```

possible combinations.

The keyspace is small enough to perform an exhaustive brute-force attack. The script tests every combination from `000` through `999` until the archive is successfully decrypted.

Leading zeros are included in the search. For example:

```text
000
001
002
...
009
010
...
099
100
...
999
```

## Solution

The provided `zip-crack.py` script can be used to test all three-digit combinations.

Run:

```bash
python zip-crack.py
```

The script uses `encrypted_flag.zip` as the default input file.

A different archive can also be supplied using:

```bash
python zip-crack.py --file <archive>
```

For example:

```bash
python zip-crack.py --file encrypted_flag.zip
```

When the correct password is found, the script extracts and displays the contents of `flag.txt`.

## Result

The brute-force process successfully recovered the password:

```text
714
```

The extracted file contained:

```text
MUET{Bhai_C0mbination_Mil_Gayi}
```

## Technical Details

The brute-force script uses Python's built-in `zipfile` module to access the encrypted archive.

The password is generated as a three-character numeric string:

```python
password = f"{i:03d}".encode()
```

This ensures that values such as `7` are represented as `007`, allowing the complete three-digit keyspace to be tested.

The script also handles ZIP password validation errors and CRC failures so that invalid password attempts do not terminate the process.

## Tools and Techniques

* Python
* ZIP archive analysis
* Password brute forcing
* Keyspace analysis
* Python `zipfile` module

## Challenge Information

| Field         | Value                             |
| ------------- | --------------------------------- |
| Challenge     | Crack the Vault                   |
| Category      | Cryptography                      |
| Difficulty    | Medium                            |
| Author        | Bilawal Ali                       |
| Password Type | Three-digit numeric               |
| Keyspace      | 1,000 combinations                |
| Password      | `714`                             |
| Flag          | `MUET{Bhai_C0mbination_Mil_Gayi}` |

## Disclaimer

This writeup and brute-force script are provided for educational and CTF purposes. The techniques demonstrated here should only be used against systems and files for which you have authorization.
