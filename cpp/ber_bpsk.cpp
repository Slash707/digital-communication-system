// BPSK BER Monte Carlo reference implementation.
// Compile: g++ -std=c++17 -O2 -Wall -Wextra -pedantic cpp/ber_bpsk.cpp -o ber_bpsk
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

int main() {
    constexpr std::uint64_t kBits = 1'000'000;
    const std::vector<double> ebn0_db_values{0, 2, 4, 6, 8, 10, 12, 14};
    std::mt19937_64 generator(20261124);
    std::bernoulli_distribution bit_source(0.5);

    std::cout << "modulation,ebn0_db,errors,tested_bits,ber\n";
    for (const double ebn0_db : ebn0_db_values) {
        const double ebn0_linear = std::pow(10.0, ebn0_db / 10.0);
        // For BPSK, k = 1 and Es = Eb = 1. Real noise variance is N0/2.
        const double n0 = 1.0 / ebn0_linear;
        const double sigma = std::sqrt(n0 / 2.0);
        std::normal_distribution<double> noise(0.0, sigma);

        std::uint64_t errors = 0;
        for (std::uint64_t n = 0; n < kBits; ++n) {
            const int bit = bit_source(generator);
            const double transmitted = (bit == 0) ? 1.0 : -1.0;
            const double received = transmitted + noise(generator);
            const int detected = (received >= 0.0) ? 0 : 1;
            if (detected != bit) {
                ++errors;
            }
        }

        const double ber = static_cast<double>(errors) /
                           static_cast<double>(kBits);
        std::cout << "BPSK," << ebn0_db << ',' << errors << ','
                  << kBits << ',' << std::setprecision(10) << ber << '\n';
    }
    return 0;
}
