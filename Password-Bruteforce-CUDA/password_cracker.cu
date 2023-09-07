#include <iostream>
#include <cstring>
#include <cstdint>
#include <cstdlib>
#include <ctime>
#include <cuda_runtime.h>
#include <openssl/sha.h>

#define NUM_BLOCKS 256
#define THREADS_PER_BLOCK 256
#define TARGET_HASH "7461aafc4225e5d33b72e07e71abf5f8df35d7c8892e83fc2e44172607b48983"

__global__ void crackPasswordKernel(char* charset, int charsetLen, char* targetHash) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int charsetIdx[4] = {0, 0, 0, 0};
    char hash[SHA256_DIGEST_LENGTH];

    while (charsetIdx[0] < charsetLen) {
        // Generate a candidate password based on the current charset indices
        char candidate[5];
        candidate[0] = charset[charsetIdx[0]];
        candidate[1] = charset[charsetIdx[1]];
        candidate[2] = charset[charsetIdx[2]];
        candidate[3] = charset[charsetIdx[3]];
        candidate[4] = '\0';

        // Calculate the hash of the candidate password
        SHA256((const unsigned char*)candidate, strlen(candidate), (unsigned char*)hash);

        // Compare the generated hash with the target hash
        if (strcmp(targetHash, hash) == 0) {
            printf("Password found: %s\n", candidate);
            return;
        }

        // Increment charset indices
        charsetIdx[0]++;
        for (int i = 0; i < 4; i++) {
            if (charsetIdx[i] == charsetLen) {
                charsetIdx[i] = 0;
                charsetIdx[i + 1]++;
            }
        }
    }
}

int main() {
    char* charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    int charsetLen = strlen(charset);

    // Target hash to crack (e.g., a SHA-256 hash)
    char targetHash[65]; // 64-character hash + null terminator
    strcpy(targetHash, TARGET_HASH);

    char* d_charset;
    char* d_targetHash;

    // Allocate memory on the GPU
    cudaMalloc((void**)&d_charset, charsetLen);
    cudaMalloc((void**)&d_targetHash, 65);

    // Copy data from host to GPU
    cudaMemcpy(d_charset, charset, charsetLen, cudaMemcpyHostToDevice);
    cudaMemcpy(d_targetHash, targetHash, 65, cudaMemcpyHostToDevice);

    // Launch the kernel
    crackPasswordKernel<<<NUM_BLOCKS, THREADS_PER_BLOCK>>>(d_charset, charsetLen, d_targetHash);
    cudaDeviceSynchronize();

    // Free GPU memory
    cudaFree(d_charset);
    cudaFree(d_targetHash);

    return 0;
}
