
import argparse
import zipfile


def crack_zip(archive):
    with zipfile.ZipFile(archive) as z:
        for i in range(1000):
            password = f"{i:03d}".encode()

            try:
                data = z.read("flag.txt", pwd=password)

                print(f"[+] Password found: {i:03d}")
                print(data.decode().strip())
                return

            except (RuntimeError, zipfile.BadZipFile):
                continue

    print("[-] Password not found.")


def main():
    parser = argparse.ArgumentParser(
        description="Brute-force a ZIP archive protected by a three-digit password."
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Path to the password-protected ZIP archive"
    )

    args = parser.parse_args()

    crack_zip(args.file)


if __name__ == "__main__":
    main()

