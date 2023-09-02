import os
import sys
import multiprocessing
from Crypto.Cipher import AES
import secrets
from Crypto.Random import get_random_bytes
from multiprocessing import Pool
from functools import partial

def encrypt_chunk(key, chunk, nonce):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(chunk)
    return (nonce, ciphertext, tag)

def decrypt_chunk(key, ciphertext, nonce, tag):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

def parallel_encrypt(input_file, output_file, key):
    chunk_size = 64 * 1024  # Adjust as needed

    # Generate a random nonce for each chunk
    nonces = [get_random_bytes(16) for _ in range(multiprocessing.cpu_count())]

    # Create a pool of worker processes for encryption
    num_processes = multiprocessing.cpu_count()
    pool = Pool(processes=num_processes)

    # Read and split the input file into chunks
    with open(input_file, 'rb') as f:
        chunks = []
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunks.append(chunk)

    # Use functools.partial to pass key to encrypt_chunk
    encrypt_chunk_with_key = partial(encrypt_chunk, key)

    # Encrypt chunks in parallel
    encrypted_chunks = pool.starmap(encrypt_chunk_with_key, [(chunk, nonce) for chunk, nonce in zip(chunks, nonces)])

    # Write encrypted data to the output file
    with open(output_file, 'wb') as f:
        for nonce, ciphertext, tag in encrypted_chunks:
            f.write(nonce + ciphertext + tag)

    pool.close()
    pool.join()

def parallel_decrypt(input_file, output_file, key):
    chunk_size = 64 * 1024  # Adjust as needed

    # Create a pool of worker processes for decryption
    num_processes = multiprocessing.cpu_count()
    pool = Pool(processes=num_processes)

    # Read the input file
    with open(input_file, 'rb') as f:
        data = f.read()

    # Extract nonces, ciphertexts, and tags
    nonces = [data[i:i+16] for i in range(0, len(data), chunk_size)]
    ciphertexts = [data[i+16:i+chunk_size-16] for i in range(0, len(data), chunk_size)]
    tags = [data[i+chunk_size-16:i+chunk_size] for i in range(0, len(data), chunk_size)]

    # Use functools.partial to pass key to decrypt_chunk
    decrypt_chunk_with_key = partial(decrypt_chunk, key)

    # Decrypt chunks in parallel
    plaintext_chunks = pool.starmap(decrypt_chunk_with_key, zip(ciphertexts, nonces, tags))

    # Write decrypted data to the output file
    with open(output_file, 'wb') as f:
        for plaintext_chunk in plaintext_chunks:
            f.write(plaintext_chunk)

    pool.close()
    pool.join()

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python parallel_aes.py <encrypt/decrypt> <input_file> <output_file> <key>")
        sys.exit(1)

    operation = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    key_hex = sys.argv[4]

    if len(key_hex) != 64:
        print("AES key must be 32 bytes (256 bits) long in hexadecimal format.")
        sys.exit(1)

    key = bytes.fromhex(key_hex)

    if operation == 'encrypt':
        parallel_encrypt(input_file, output_file, key)
        print("Encryption complete.")
    elif operation == 'decrypt':
        parallel_decrypt(input_file, output_file, key)
        print("Decryption complete.")
    else:
        print("Invalid operation. Use 'encrypt' or 'decrypt'.")
        sys.exit(1)
