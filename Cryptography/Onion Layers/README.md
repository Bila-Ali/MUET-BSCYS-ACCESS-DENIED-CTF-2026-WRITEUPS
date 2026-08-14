# Onion Layers

**Category:** Cryptography / Encoding

**Difficulty:** Easy

**Points:** 100

**Author:** Bilawal Ali

**Event:** AccessDenied CTF 2026
**Tool:** CyberChef
**Flag:** `MUET{Mehnat_Rang_Lai}`

---

## Challenge Description

The challenge contains multiple hidden encoding layers. Each layer uses a different encoding scheme, and the objective is to identify and decode them sequentially until the final flag is revealed.

The challenge is designed to test the ability to recognize encoding patterns, analyze character sets, and follow a layered decoding process rather than relying on a single automated solution.

### Hint

> Pay attention to the sequence and patterns behind each layer. A small detail can be the biggest clue.

### Provided File

`flag_file.txt`

```text
AUu2xw2qaXk5vLmCEe5sJQcNsq5UCgvDhSy73KpsZH3nDCdBiudsBsgHM79MoR6HB4M1FSoi8fwBEBYxX3op5mH9XZcJSTGzLrVWmxHMhQCoSc9PkyHZa2NKJfRzQvnYJb5j2jnU8j
```

---

# Solution

## Step 1 — Identify the First Encoding Layer

The provided string consists entirely of alphanumeric characters and has a character set consistent with Base58.

A useful way to identify Base58 is to check for the absence of visually ambiguous characters such as:

```text
0
O
I
l
```

The input does not contain these characters, making Base58 a strong candidate.

In CyberChef, use:

```text
From Base58
```

with the standard Bitcoin Base58 alphabet.

The result is:

```text
7E4JkQg959SBGLRdv9Dnxgr9O7AxDfCaZaa5b2CLR0lj2eee8Q1PCKiFUeP0tAGNoLk0ntaX2M0kLTb0i0VFCTozzlgputNljSt8T
```

The output is fully printable and remains composed of alphanumeric characters, indicating that another encoding layer is present.

---

## Step 2 — Identify the Second Encoding Layer

The new string is no longer valid Base58 because it contains characters that are excluded from the Base58 alphabet, such as:

```text
O
```

However, it still consists entirely of:

```text
0-9
A-Z
a-z
```

This character set is consistent with Base62.

Therefore, the next layer is Base62.

Unlike standard Base64 or Base58 operations available directly in many tools, Base62 implementations can vary. For this challenge, the layer is represented as a Base62-encoded large integer and must be decoded using the corresponding Base62 alphabet:

```text
0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
```

After decoding the Base62 layer, the resulting data contains an embedded Base64 string.

The relevant Base64 portion ends with:

```text
TVVFVHtNZWhuYXRfUmFuZ19MYWl9
```

---

## Step 3 — Extract the Base64 Layer

The decoded Base62 content contains additional text along with the Base64 payload.

The additional content is intentionally distracting and should not be treated as part of the cryptographic chain.

The important payload is:

```text
TVVFVHtNZWhuYXRfUmFuZ19MYWl9
```

This string uses the standard Base64 character set and is therefore suitable for the final decoding step.

---

## Step 4 — Decode Base64

Use CyberChef's:

```text
From Base64
```

on:

```text
TVVFVHtNZWhuYXRfUmFuZ19MYWl9
```

The result is:

```text
MUET{Mehnat_Rang_Lai}
```

This is the final flag.

---

# CyberChef Recipe

The intended decoding chain is:

```text
Input
  |
  v
From Base58
  |
  v
From Base62
  |
  v
Extract embedded Base64
  |
  v
From Base64
  |
  v
MUET{Mehnat_Rang_Lai}
```

### Operations

1. `From Base58`
2. `From Base62`
3. Extract the embedded Base64 payload
4. `From Base64`

---

# Flag

```text
MUET{Mehnat_Rang_Lai}
```

---

# Key Takeaways

## 1. Analyze the Character Set

Before attempting to decode an unknown string, inspect its character set.

For example:

| Encoding | Typical Character Set             |
| -------- | --------------------------------- |
| Base64   | `A-Z a-z 0-9 + / =`               |
| Base58   | `A-Z a-z 1-9` excluding `0 O I l` |
| Base62   | `A-Z a-z 0-9`                     |
| Base32   | `A-Z 2-7 =`                       |

Character-set analysis can significantly reduce the number of possible encoding schemes.

## 2. Decode One Layer at a Time

Layered encoding challenges should be approached systematically:

```text
Identify
    ↓
Decode
    ↓
Inspect
    ↓
Identify next layer
    ↓
Decode
    ↓
Repeat
```

Do not assume that the first successful decode is the end of the challenge.

## 3. Treat Decoded Content as Data

Decoded content may contain text that looks like instructions or commands. That content should not automatically be trusted.

In this challenge, the Base62-decoded data contains distracting text designed to resemble an instruction or prompt. It is not part of the cryptographic decoding process.

The correct approach is to distinguish between:

* Encoding payload
* Decoded data
* Challenge metadata
* Deliberate decoys

## 4. Don't Rely Entirely on Automated Detection

CyberChef's `Magic` operation can be useful for reconnaissance, but layered encoding challenges are often easier to solve by understanding why a particular encoding is likely.

The important reasoning in this challenge is:

```text
Base58 character set
        ↓
Base58 decoding
        ↓
Base62 character set
        ↓
Base62 decoding
        ↓
Embedded Base64
        ↓
Final flag
```

---

# Conclusion

The challenge uses three encoding layers:

```text
Base58 → Base62 → Base64
```

By identifying each layer from its structure and decoding them sequentially, the hidden flag can be recovered:

```text
MUET{Mehnat_Rang_Lai}
```
