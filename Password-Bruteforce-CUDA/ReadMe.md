# CUDA Password Bruteforce

This is a simple CUDA-based password cracking simulator that demonstrates parallel processing for brute-force password cracking. It utilizes CUDA for GPU acceleration and a simplified hashing algorithm (SHA-256) for demonstration purposes.

## Prerequisites

Before you can compile and run this code, you'll need the following:

- A CUDA-compatible GPU.
- CUDA toolkit and drivers installed.
- C++ compiler with CUDA support (e.g., nvcc).
- OpenSSL library for SHA-256 hashing.

## Compilation

1. Navigate to the project directory:

   ```sh
   cd cuda-password-cracker
   ```

2. Compile the code using `nvcc` (NVIDIA CUDA Compiler):

   ```sh
   nvcc -o password_cracker password_cracker.cu -lcrypto
   ```

## Usage

1. After successful compilation, you can run the CUDA password cracking simulator using the following command:

   ```sh
   ./password_cracker
   ```

2. The program will attempt to crack a predefined target hash (specified in the code). If it successfully finds the password, it will print the cracked password to the console.

## Functionality

This CUDA-based password cracking simulator works as follows:

- It uses a brute-force approach to generate and test possible passwords.
- The character set for passwords is predefined as lowercase and uppercase letters and digits.
- It calculates the SHA-256 hash of each generated password.
- It compares the generated hash with a predefined target hash.
- If a match is found, the program prints the cracked password to the console.


