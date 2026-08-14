# Vault (Easy)

**Category:** Reverse Engineering
**Difficulty:** Easy
**Points:** 50
**Author:** Bilawal Ali
**Event:** AccessDenied CTF 2026
**Tools:** `file`, `strings`, ROT13
**Flag:** `MUET{Bhai_Pehle_Strings_To_Dekh}`

---

## Challenge Description

A small program was found on an old server. Running it does not reveal much, but binaries often contain useful information even when their normal execution path does not expose it.

The objective is to inspect the binary and recover the hidden flag.

### Hint

> `strings` is your friend.

### Provided File

```text
vault_easy
```

The provided file is an ELF 64-bit executable.

---

# Solution

## Step 1 — Execute the Binary

First, make the binary executable:

```bash
chmod +x vault_easy
```

Then run it:

```bash
./vault_easy
```

The program displays:

```text
=====================================
   AccessDenied Vault v1.0 (demo)
=====================================
Sorry, this feature requires a license.
Contact support for access.
```

The program exits without revealing the flag.

This suggests that dynamic execution is not the intended solution path. Since the challenge specifically hints at `strings`, the next step is static inspection.

---

## Step 2 — Identify the File Type

Use the `file` command:

```bash
file vault_easy
```

Output:

```text
vault_easy: ELF 64-bit LSB executable, x86-64, dynamically linked, not stripped
```

This confirms that the file is a standard 64-bit Linux ELF executable.

The binary is also **not stripped**, meaning useful symbols and metadata may still be present.

---

## Step 3 — Extract Strings

The challenge hint points directly toward the `strings` utility.

Run:

```bash
strings vault_easy
```

There will be various normal program strings, including the banner and license message.

To search for the suspicious flag-like value:

```bash
strings vault_easy | grep -i zhrg
```

The relevant output is:

```text
ZHRG{Ounv_Cruyr_Fgevatf_Gb_Qrxu}
```

At first glance, this resembles a flag but uses:

```text
ZHRG{...}
```

instead of the expected:

```text
MUET{...}
```

This strongly suggests that the value has been transformed using a simple substitution cipher.

---

## Step 4 — Identify ROT13

The prefix provides an immediate clue:

```text
ZHRG
```

Applying ROT13:

```text
Z → M
H → U
R → E
G → T
```

Therefore:

```text
ZHRG
```

becomes:

```text
MUET
```

This confirms that ROT13 is the correct transformation.

---

## Step 5 — Decode the Flag

The complete encoded string is:

```text
ZHRG{Ounv_Cruyr_Fgevatf_Gb_Qrxu}
```

Using CyberChef's **ROT13** operation produces:

```text
MUET{Bhai_Pehle_Strings_To_Dekh}
```

The same result can be obtained directly from the command line:

```bash
echo "ZHRG{Ounv_Cruyr_Fgevatf_Gb_Qrxu}" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Output:

```text
MUET{Bhai_Pehle_Strings_To_Dekh}
```

---

# Source Code Analysis

The accompanying source file confirms what the static analysis revealed.

The flag is stored directly in the binary as a ROT13-encoded string:

```c
static const char secret[] = "ZHRG{Ounv_Cruyr_Fgevatf_Gb_Qrxu}";
```

The source also contains the following comment:

```c
/* The flag sits right there in the binary's strings, ROT13'd.
   No decoys, no encryption, no tricks -- just look. */
```

The following line:

```c
volatile const char *p = secret;
```

ensures that the compiler does not optimize the unused string away, allowing the encoded flag to remain inside the compiled binary.

This explains why `strings` is sufficient to solve the challenge.

---

# Intended Solution Path

The complete workflow is:

```text
vault_easy
    |
    v
Run the binary
    |
    v
License message
    |
    v
Inspect file type
    |
    v
ELF 64-bit executable
    |
    v
strings vault_easy
    |
    v
ZHRG{Ounv_Cruyr_Fgevatf_Gb_Qrxu}
    |
    v
Recognize ROT13
    |
    v
MUET{Bhai_Pehle_Strings_To_Dekh}
```

---

# Flag

```text
MUET{Bhai_Pehle_Strings_To_Dekh}
```

---

# Key Takeaways

### 1. Start With Simple Static Analysis

When analyzing an unfamiliar binary, `strings` is often one of the quickest and most useful first commands.

It can reveal:

* Hardcoded flags
* URLs
* File paths
* Error messages
* Debug information
* API endpoints
* Embedded configuration
* Suspicious encoded data

### 2. Don't Depend Only on Program Execution

A binary may intentionally provide a dead-end execution path.

If running the program does not reveal anything useful, switch to static analysis rather than repeatedly interacting with the same runtime behavior.

### 3. Recognize Common Encodings and Ciphers

The value:

```text
ZHRG{...}
```

closely resembles the expected flag structure.

Recognizing that:

```text
ZHRG → MUET
```

is a ROT13 transformation makes the rest of the decoding straightforward.

### 4. Check the Simplest Technique First

For an easy reverse-engineering challenge, there is no need to immediately reach for advanced tools such as Ghidra, IDA, or a debugger.

A practical initial workflow is:

```bash
file binary
strings binary
strings binary | grep -i flag
strings binary | grep -Ei 'muet|zhrg|flag'
```

Only move to disassembly or debugging if simpler static inspection does not provide enough information.

---

## Conclusion

The challenge does not require complex reverse engineering. The flag is embedded directly inside the ELF binary, protected only by ROT13.

The intended solution is:

```text
strings → identify encoded flag → ROT13 → flag
```

Final flag:

```text
MUET{Bhai_Pehle_Strings_To_Dekh}
```
