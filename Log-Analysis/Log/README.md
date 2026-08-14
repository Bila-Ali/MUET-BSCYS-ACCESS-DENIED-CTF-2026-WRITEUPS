# Logs, Play, Round 4

**Category:** Forensics
**Difficulty:** Medium–Hard
**Points:** 250
**Author:** Bilawal Ali
**Event:** AccessDenied CTF 2026

## Challenge Description

A web server's access log was pulled after a suspicious spike in traffic. Among the bots, scanners, and proxy checkers, a strange `/checkout/confirm` flow appears repeatedly.

Most of the traffic is noise, but a few requests contain encoded data that, when decoded and placed in the correct order, reveal the flag.

### Hints

> **Hint 1:** `grep` isn't enough by itself this time — several requests will match the same pattern. Decode all of them before deciding which ones matter.

> **Hint 2:** The order they appear in the file is not the order that matters.

## Provided File

```text
access.log
```

---

## Solution

### Step 1 — Identify the Suspicious Endpoint

The access log contains a large amount of generic reconnaissance traffic, including requests from scanners and bots targeting common paths such as:

* `/.env`
* `/.git/config`
* `/wp-login.php`
* `/phpmyadmin/`

However, one endpoint stands out:

```text
/checkout/confirm
```

Unlike most scanner requests, this endpoint repeatedly returns successful responses and contains query parameters.

Extract the relevant requests:

```bash
grep '/checkout/confirm' access.log
```

There are multiple matches, so simply looking at the matching lines is not enough.

Extract only the `step` and `sid` parameters:

```bash
grep -oE 'step=[0-9]+&sid=[^ &"]+' access.log
```

Example output:

```text
step=1&sid=eyJ1aWQiOiJjNDEwZSIsImRldmljZSI6Im1vYmlsZSJ9
step=2&sid=QmhpX0thaGFuaV8%3D
step=2&sid=eyJjYXJ0X2lkIjoiOTAxMiIsInByb21vIjoibm9uZSJ9
step=2&sid=eyJjYXJ0X2lkIjoiMjI5MCIsInByb21vIjoiV0VMQ09NRTEwIn0%3D
step=2&sid=eyJzZXNzaW9uIjoiZXhwaXJlZCIsInJldHJ5Ijp0cnVlfQ%3D%3D
step=3&sid=U3VuYXR5Xw%3D%3D
step=1&sid=TVVFVHtMb2dzXw%3D%3D
step=4&sid=SGFpbn0%3D
step=4&sid=eyJ1aWQiOiI3N2IzYSIsInJlZmVycmVyIjoiZGlyZWN0In0%3D
step=2&sid=eyJjYXJ0X2lkIjoiNTU2NyIsIml0ZW1zIjozfQ%3D%3D
step=3&sid=eyJ1aWQiOiJhOTFmMiIsInJlZmVycmVyIjoiZ29vZ2xlIn0%3D
step=1&sid=eyJjYXJ0X2lkIjoiODg0MSIsInByb21vIjoibm9uZSJ9
```

---

### Step 2 — Decode Every `sid`

The `sid` values are URL-encoded Base64 strings.

For example:

```text
QmhpX0thaGFuaV8%3D
```

First URL-decode:

```text
QmhpX0thaGFuaV8=
```

Then Base64-decode:

```text
Bhi_Kahani_
```

Because several entries use the same `step` value, **every candidate must be decoded** before deciding whether it contains useful information.

A convenient Python script:

```python
import re
import base64
import urllib.parse

entries = []

with open("access.log", "r") as f:
    for line in f:
        match = re.search(
            r"step=([0-9]+)&sid=([^ &\"]+)",
            line
        )

        if match:
            step = int(match.group(1))
            sid = urllib.parse.unquote(match.group(2))

            decoded = base64.b64decode(
                sid + "=="
            ).decode(errors="replace")

            entries.append((step, decoded))

for step, decoded in sorted(entries):
    print(f"step={step} -> {decoded}")
```

The decoded values are:

```text
step=1 -> {"uid":"c410e","device":"mobile"}
step=1 -> {"cart_id":"8841","promo":"none"}
step=1 -> MUET{Logs_
step=2 -> Bhi_Kahani_
step=2 -> {"cart_id":"9012","promo":"none"}
step=2 -> {"cart_id":"2290","promo":"WELCOME10"}
step=2 -> {"session":"expired","retry":true}
step=2 -> {"cart_id":"5567","items":3}
step=3 -> Sunaty_
step=3 -> {"uid":"a91f2","referrer":"google"}
step=4 -> Hain}
step=4 -> {"uid":"77b3a","referrer":"direct"}
```

---

## Step 3 — Identify the Flag Fragments

Most decoded values are JSON session data and are therefore decoys.

The useful entries are the ones that decode to plain-text fragments rather than JSON:

| Step | Decoded Value |
| ---: | ------------- |
|    1 | `MUET{Logs_`  |
|    2 | `Bhi_Kahani_` |
|    3 | `Sunaty_`     |
|    4 | `Hain}`       |

The important observation is that **the `step` parameter determines the order**.

---

## Step 4 — Reorder the Fragments

Do not use the order in which the requests appear in `access.log`.

Instead, sort the extracted values according to `step`:

```text
step=1 -> MUET{Logs_
step=2 -> Bhi_Kahani_
step=3 -> Sunaty_
step=4 -> Hain}
```

---

## Step 5 — Assemble the Flag

Concatenate the four fragments:

```text
MUET{Logs_
Bhi_Kahani_
Sunaty_
Hain}
```

Final flag:

```text
MUET{Logs_Bhi_Kahani_Sunaty_Hain}
```

---

## Flag

```text
MUET{Logs_Bhi_Kahani_Sunaty_Hain}
```

---

## Tools Used

* **grep** — isolate suspicious `/checkout/confirm` requests
* **grep -oE** — extract `step` and `sid` parameters
* **Python** — URL-decode and Base64-decode all candidate values
* **Manual triage** — distinguish flag fragments from decoy JSON
* **Sorting** — reconstruct the intended order using `step`

---

## Key Takeaways

1. **Don't assume every matching request is meaningful.**
   Multiple requests can match the same suspicious pattern, so each candidate must be investigated.

2. **Decode before filtering.**
   The `sid` values appear similar at first, but decoding reveals which values contain useful information.

3. **Don't blindly trust log order.**
   The physical order of entries in a log does not necessarily represent the logical order of the data.

4. **Look for sequencing metadata.**
   The `step=` parameter provides the intended order of the flag fragments.

5. **Inspect parameters, not just paths.**
   Suspicious data can be hidden inside otherwise ordinary-looking query parameters.


      ▼
MUET{Logs_Bhi_Kahani_Sunaty_Hain}
```

> **"Logs bhi kahani sunaty hain"** — *Even logs tell a story.*
