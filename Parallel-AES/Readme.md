# Parallel Encryption/Decryption Tool

This Python script allows you to perform parallel encryption and decryption of files using the Advanced Encryption Standard (AES) algorithm. Parallel processing techniques are employed to enhance the speed of cryptographic operations.

## Table of Contents

- [Parallel Encryption/Decryption Tool](#parallel-encryptiondecryption-tool)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
    - [Encryption](#encryption)
    - [Decryption](#decryption)
  - [Performance Considerations](#performance-considerations)

## Features

- Parallel AES encryption and decryption.
- Easy-to-use command-line interface.
- Supports multi-core processors for enhanced performance.
- Secure file encryption and decryption using AES.

## Prerequisites

Before using this tool, ensure you have the following prerequisites installed:

- Python 3.x
- `pycryptodome` library (install with `pip install pycryptodome`)

## Usage

1. Clone or download this repository to your local machine.

2. Open a terminal and navigate to the project directory.

### Encryption

To encrypt a file, use the following command:

```shell
python parallel_aes.py encrypt <input_file> <output_file> <key>
```

- `<input_file>`: The path to the file you want to encrypt.
- `<output_file>`: The path where the encrypted file will be saved.
- `<key>`: A 32-byte (256-bit) hexadecimal key used for encryption.

Example:

```shell
python parallel_aes.py encrypt plaintext.txt encrypted.bin 00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff
```

### Decryption

To decrypt a file, use the following command:

```shell
python parallel_aes.py decrypt <input_file> <output_file> <key>
```

- `<input_file>`: The path to the encrypted file.
- `<output_file>`: The path where the decrypted file will be saved.
- `<key>`: The same 32-byte hexadecimal key used for encryption.

Example:

```shell
python parallel_aes.py decrypt encrypted.bin decrypted.txt 00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff
```

## Performance Considerations

- Adjust the `chunk_size` variable in the script to optimize performance based on your system's capabilities and available memory.

- The tool utilizes multiprocessing to take advantage of multi-core processors. The number of processes created equals the number of CPU cores available.
