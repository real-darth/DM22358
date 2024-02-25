#include <cmath>
#include <iostream>
#include <immintrin.h>

extern "C" {
    void neighbors(double x[], double y[], int n, int b, int R, bool res[]);
}

/**
 * Calculates the neighbors of a given point in a 2D space.
 * 
 * @param x An array of x-coordinates of the points.
 * @param y An array of y-coordinates of the points.
 * @param n The number of points in the arrays.
 * @param b The index of the point for which neighbors are to be calculated.
 * @param R The radius within which points are considered neighbors.
 * @param res An array to store the result indicating whether each point is a neighbor or not.
 */
void neighbors(double x[], double y[], int n, int b, int R, bool res[]) {
    int subtractValX = x[b];
    int subtractValY = y[b];
    int RR = R * R;

    // Vectorization
    int simdSize = sizeof(__m256d) / sizeof(double); // Calculate the size of a SIMD vector
    int numSimdVectors = n / simdSize; // Calculate the number of SIMD vectors

    __m256d subtractValXVec = _mm256_set1_pd(subtractValX); // Create a SIMD vector with all elements set to subtractValX
    __m256d subtractValYVec = _mm256_set1_pd(subtractValY); // Create a SIMD vector with all elements set to subtractValY
    __m256d RRVec = _mm256_set1_pd(RR); // Create a SIMD vector with all elements set to RR

    for (int i = 0; i < numSimdVectors * simdSize; i += simdSize) { // Loop over the SIMD vectors
        __m256d xVec = _mm256_loadu_pd(&x[i]); // Load a SIMD vector of x values
        __m256d yVec = _mm256_loadu_pd(&y[i]); // Load a SIMD vector of y values

        __m256d tempVec = _mm256_add_pd(_mm256_mul_pd(_mm256_sub_pd(xVec, subtractValXVec), _mm256_sub_pd(xVec, subtractValXVec)), // Calculate the squared Euclidean distance
                                        _mm256_mul_pd(_mm256_sub_pd(yVec, subtractValYVec), _mm256_sub_pd(yVec, subtractValYVec)));

        __m256d compareVec = _mm256_cmp_pd(tempVec, RRVec, _CMP_LT_OQ); // Compare the squared distances with RR

        int mask = _mm256_movemask_pd(compareVec); // Convert the comparison result to a bitmask
        res[i] = (mask & 0x1) != 0; // Check if the first element of the bitmask is set and store the result in res
        res[i + 1] = (mask & 0x2) != 0; // Check if the second element of the bitmask is set and store the result in res
        res[i + 2] = (mask & 0x4) != 0; // Check if the third element of the bitmask is set and store the result in res
        res[i + 3] = (mask & 0x8) != 0; // Check if the fourth element of the bitmask is set and store the result in res
    }

    // Handle remaining elements
    for (int i = numSimdVectors * simdSize; i < n; i++) { // Loop over the remaining elements
        double temp = (x[i] - subtractValX) * (x[i] - subtractValX) + (y[i] - subtractValY) * (y[i] - subtractValY); // Calculate the squared Euclidean distance
        res[i] = (temp < RR); // Check if the squared distance is less than RR and store the result in res
    }
}

int main() {
    int n = 8;
    double x[] = {1, 2, 3, 4, 5, 6, 7, 8};
    double y[] = {1, 2, 3, 4, 5, 6, 7, 8};
    int b = 4;
    int R = 2;
    bool res[n];
    neighbors(x, y, n, b, R, res);
    for (int i = 0; i < n; i++) {
        std::cout << res[i] << " ";
    }
    std::cout << std::endl;
}