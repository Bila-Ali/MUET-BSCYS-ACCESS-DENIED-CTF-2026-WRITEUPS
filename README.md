# MUET BSCYS — ACCESS~DENIED CTF 2026 Writeups

> Official challenge writeups and technical solutions from the **MUET BSCYS CTF Hackathon 2026**, organized by **Team ACCESS~DENIED**.

This repository contains structured writeups for selected challenges from the MUET BSCYS CTF Hackathon 2026. Each writeup documents the investigation process, techniques used, tools involved, and the reasoning required to reach the final flag.

---

## About the CTF

**MUET BSCYS CTF Hackathon 2026** was a cybersecurity Capture The Flag competition organized for students of the **BS Cyber Security Department, Mehran University of Engineering and Technology (MUET), Jamshoro**.

The event was designed to provide hands-on experience across multiple areas of cybersecurity, including digital forensics, cryptography, reverse engineering, and log analysis.

### Event Information

| Detail          | Information                                     |
| --------------- | ----------------------------------------------- |
| **Event**       | MUET BSCYS CTF Hackathon 2026                   |
| **Organizer**   | Team ACCESS~DENIED                              |
| **Institution** | Mehran University of Engineering and Technology |
| **Department**  | BS Cyber Security                               |
| **Year**        | 2026                                            |
| **Format**      | Capture The Flag                                |
| **Focus**       | Practical Cybersecurity                         |

---

## Repository Structure

The repository is organized by challenge category to make the writeups easy to navigate.

```text
MUET-BSCYS-ACCESS-DENIED-CTF-2026-WRITEUPS/
│
├── Cryptography/
│   └── Layers/
│       └── README.md
│
├── Forensic/
│   └── ...
│
├── Log-Analysis/
│   └── Log/
│       └── README.md
│
├── Reverse Engineering/
│   ├── Vault/
│   │   └── README.md
│   │
│   └── KeyGate/
│       └── README.md
│
└── README.md
```

> Directory names may evolve as additional challenge writeups are added.

---

# Challenge Categories

## Cryptography

Challenges involving encoding, encryption, classical ciphers, and cryptographic analysis.

### Layers

**Difficulty:** Easy
**Points:** 100

A multi-layer encoding challenge requiring the solver to identify and decode a sequence of:

```text
Base58 → Base62 → Base64
```

**Techniques:**

* Character-set analysis
* Base58 decoding
* Base62 decoding
* Base64 decoding
* Layered encoding analysis

**Flag:**

```text
MUET{Mehnat_Rang_Lai}
```

---

## Forensics

Challenges involving investigation and analysis of digital artifacts such as files, logs, and other evidence.

Writeups in this category document practical forensic workflows, artifact analysis, filtering, decoding, and evidence reconstruction.

---

## Log Analysis

Challenges focused on extracting meaningful information from noisy logs and reconstructing activity from application or server events.

### Logs, Play, Round 4

**Category:** Forensics / Log Analysis
**Difficulty:** Medium–Hard
**Points:** 250

A noisy web server access log contains scanner traffic mixed with suspicious `/checkout/confirm` requests.

The solution involves:

```text
Identify suspicious endpoint
        ↓
Extract step + sid parameters
        ↓
URL-decode
        ↓
Base64-decode
        ↓
Separate decoys from flag fragments
        ↓
Sort by step
        ↓
Reconstruct flag
```

**Flag:**

```text
MUET{Logs_Bhi_Kahani_Sunaty_Hain}
```

---

## Reverse Engineering

Challenges involving binary analysis, static analysis, debugging, disassembly, and recovering hidden program logic.

### Vault — Easy

**Difficulty:** Easy
**Points:** 50

A small ELF binary appears to provide only a license-related message during normal execution. Static analysis reveals that the flag is embedded in the binary and protected using ROT13.

**Primary tools:**

```text
file
strings
CyberChef / tr
```

**Solution path:**

```text
ELF binary
    ↓
strings
    ↓
ROT13-encoded flag
    ↓
ROT13
    ↓
MUET{Bhai_Pehle_Strings_To_Dekh}
```

**Flag:**

```text
MUET{Bhai_Pehle_Strings_To_Dekh}
```

---

### KeyGate

**Difficulty:** Easy–Medium

A stripped ELF binary implements a simple key validation mechanism. Both the expected key and the flag are protected using single-byte XOR.

**Primary tools:**

```text
file
objdump
Ghidra
Python
```

**Solution path:**

```text
Inspect ELF
    ↓
Analyze .rodata
    ↓
Identify encrypted byte arrays
    ↓
Recover XOR key: 0x55
    ↓
Decrypt authentication key
    ↓
22BSCYS002
    ↓
Decrypt flag
    ↓
MUET{Bhai_License_Kahan_Gaya}
```

**Flag:**

```text
MUET{Bhai_License_Kahan_Gaya}
```

---

# Writeup Format

Each challenge writeup aims to follow a consistent structure:

```text
Challenge Information
        ↓
Challenge Description
        ↓
Provided Files
        ↓
Initial Reconnaissance
        ↓
Investigation / Analysis
        ↓
Step-by-Step Solution
        ↓
Tools Used
        ↓
Flag
        ↓
Key Takeaways
```

The goal is not only to document the final flag, but also to explain **why each step works** and how the same methodology can be applied to similar challenges.

---

# Tools & Techniques

The repository covers a range of commonly used cybersecurity tools and techniques, including:

### General

* Linux command line
* `file`
* `grep`
* `strings`
* Python

### Digital Forensics

* Log analysis
* Artifact filtering
* Encoding identification
* Data reconstruction

### Cryptography & Encoding

* Base58
* Base62
* Base64
* ROT13
* XOR

### Reverse Engineering

* ELF analysis
* `.rodata` inspection
* `objdump`
* Ghidra
* Static analysis
* Basic binary decryption

---

# Learning Objectives

These writeups are intended to demonstrate practical approaches to common CTF problems.

By studying the solutions, players can develop skills in:

* Identifying suspicious artifacts
* Performing structured reconnaissance
* Recognizing common encoding schemes
* Analyzing binary files
* Extracting embedded data
* Understanding simple obfuscation techniques
* Writing small scripts for repetitive analysis
* Separating useful data from decoys
* Reconstructing information from logs
* Validating findings against the original artifact

---

# Disclaimer

These writeups are published for **educational and cybersecurity learning purposes**.

The techniques demonstrated here are intended for use in:

* CTF competitions
* Authorized security labs
* Educational environments
* Defensive security research
* Systems for which you have explicit permission to test

Do not use these techniques against systems or data without proper authorization.

---

# Acknowledgments

Special thanks to everyone who contributed to the **MUET BSCYS CTF Hackathon 2026** and helped make the event possible.

The challenges were designed to encourage practical cybersecurity learning and give participants an opportunity to apply concepts beyond the classroom.

---

# Author

**Bilawal Ali**
BS Cyber Security
Mehran University of Engineering and Technology (MUET)

**LinkedIn:** [@Bilawal Ali](https://www.linkedin.com/in/bilawal-ali-0b0211245/) 

**Porfolio:** [Bilawal Ali](https://bila-ali.github.io/)

**GitHub:** [@Bilawal Ali](https://github.com/Bila-Ali) 

---

# Repository

**MUET BSCYS — ACCESS~DENIED CTF 2026 Writeups**

This repository will continue to be updated with additional challenge solutions and technical documentation.

If you find these writeups useful, consider starring the repository and following the project for future updates.

---

## License

Unless otherwise specified, the challenge writeups and accompanying documentation in this repository are provided for educational purposes.
