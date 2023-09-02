import os
import sys
import multiprocessing
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_chunk(key, chunk, output_queue):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(chunk)
    output_queue.put((nonce, ciphertext, tag))

def decrypt_chunk(key, nonce, ciphertext, tag, output_queue):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    output_queue.put(plaintext)

def parallel_encrypt(input_file, output_file, key):
    chunk_size = 64 * 1024  # Adjust as needed
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    # Create worker processes for encryption
    num_processes = multiprocessing.cpu_count()
    processes = []
    for _ in range(num_processes):
        process = multiprocessing.Process(target=encrypt_chunk, args=(key, input_queue.get(), output_queue))
        processes.append(process)
        process.start()

    # Read and split the input file into chunks and put them in the input queue
    with open(input_file, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            input_queue.put(chunk)

    # Close the input queue to signal workers to finish
    for _ in range(num_processes):
        input_queue.put(None)

    # Wait for encryption processes to finish
    for process in processes:
        process.join()

    # Write encrypted data to the output file
    with open(output_file, 'wb') as f:
        while not output_queue.empty():
            nonce, ciphertext, tag = output_queue.get()
            f.write(nonce + ciphertext + tag)

def parallel_decrypt(input_file, output_file, key):
    chunk_size = 64 * 1024  # Adjust as needed
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    # Create worker processes for decryption
    num_processes = multiprocessing.cpu_count()
    processes = []
    for _ in range(num_processes):
        process = multiprocessing.Process(target=decrypt_chunk, args=(key, *input_queue.get(), output_queue))
        processes.append(process)
        process.start()

    # Read and split the input file into chunks and put them in the input queue
    with open(input_file, 'rb') as f:
        while True:
            nonce = f.read(16)
            ciphertext = f.read(chunk_size - 16 - 16)  # Nonce + Ciphertext + Tag
            tag = f.read(16)
            if not ciphertext:
                break
            input_queue.put((nonce, ciphertext, tag))

    # Close the input queue to signal workers to finish
    for _ in range(num_processes):
        input_queue.put(None)

    # Wait for decryption processes to finish
    for process in processes:
        process.join()

    # Write decrypted data to the output file
    with open(output_file, 'wb') as f:
        while not output_queue.empty():
            plaintext = output_queue.get()
            f.write(plaintext)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python parallel_aes.py <encrypt/decrypt> <input_file> <output_file> <key>")
        sys.exit(1)

    operation = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    key = sys.argv[4]

    if len(key) != 32:
        print("AES key must be 32 bytes (256 bits) long.")
        sys.exit(1)

    key = bytes.fromhex(key)

    if operation == 'encrypt':
        parallel_encrypt(input_file, output_file, key)
        print("Encryption complete.")
    elif operation == 'decrypt':
        parallel_decrypt(input_file, output_file, key)
        print("Decryption complete.")
    else:
        print("Invalid operation. Use 'encrypt' or 'decrypt'.")
        sys.exit(1)
