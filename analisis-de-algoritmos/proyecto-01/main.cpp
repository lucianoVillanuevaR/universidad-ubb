#include <chrono>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

#include "funciones.hpp"

int main(int argc, char* argv[]) {

    // Tamaños solicitados en la tarea.
    const std::vector<int> tamanos = {
        64,
        128,
        256,
        512,
        1024,
        2048,
        4096
    };

    // Sin argumentos se ejecutan todos los tamaños. Para detener la prueba
    // en un tamaño concreto se puede usar, por ejemplo: ./matrices 1024
    int tamanoMaximo = std::numeric_limits<int>::max();

    if (argc > 2) {
        std::cerr << "Uso: " << argv[0] << " [tamano_maximo]\n";
        return 1;
    }

    if (argc == 2) {
        try {
            std::size_t caracteresLeidos = 0;
            tamanoMaximo = std::stoi(argv[1], &caracteresLeidos);

            if (caracteresLeidos != std::string(argv[1]).size()
                || tamanoMaximo <= 0) {
                throw std::invalid_argument("tamano invalido");
            }
        } catch (const std::exception&) {
            std::cerr << "ERROR: el tamaño máximo debe ser un entero positivo.\n";
            return 1;
        }
    }

    // Encabezado de la tabla.
    std::cout
        << std::left
        << std::setw(8)
        << "n"

        << std::right
        << std::setw(20)
        << "Tradicional (ms)"

        << std::setw(15)
        << "DR1 (ms)"

        << std::setw(15)
        << "DR2 (ms)"

        << std::setw(15)
        << "Verificacion"

        << '\n';

    std::cout
        << std::string(73, '-')
        << '\n';

    // Se prueba cada tamaño.
    for (int n : tamanos) {

        if (n > tamanoMaximo) {
            break;
        }

        // ------------------------------------------------
        // GENERACIÓN DE MATRICES
        // ------------------------------------------------

        Matrix A = generarMatrizAleatoria(n);
        Matrix B = generarMatrizAleatoria(n);

        // ------------------------------------------------
        // ALGORITMO TRADICIONAL
        // ------------------------------------------------

        const auto inicioTradicional =
            std::chrono::steady_clock::now();

        Matrix CTradicional =
            algoritmoTradicional(A, B);

        const auto finTradicional =
            std::chrono::steady_clock::now();

        // ------------------------------------------------
        // DR1
        // ------------------------------------------------

        const auto inicioDR1 =
            std::chrono::steady_clock::now();

        Matrix CDR1 =
            algoritmoDR1(A, B);

        const auto finDR1 =
            std::chrono::steady_clock::now();

        // ------------------------------------------------
        // DR2
        // ------------------------------------------------

        const auto inicioDR2 =
            std::chrono::steady_clock::now();

        Matrix CDR2 =
            algoritmoDR2(A, B);

        const auto finDR2 =
            std::chrono::steady_clock::now();

        // ------------------------------------------------
        // CÁLCULO DE TIEMPOS
        // ------------------------------------------------

        const double tiempoTradicional =
            std::chrono::duration<double, std::milli>(
                finTradicional - inicioTradicional
            ).count();

        const double tiempoDR1 =
            std::chrono::duration<double, std::milli>(
                finDR1 - inicioDR1
            ).count();

        const double tiempoDR2 =
            std::chrono::duration<double, std::milli>(
                finDR2 - inicioDR2
            ).count();

        // La verificación se realiza después de medir los tres algoritmos.
        const bool dr1Correcto = (CTradicional == CDR1);
        const bool dr2Correcto = (CTradicional == CDR2);

        // ------------------------------------------------
        // MOSTRAR RESULTADOS
        // ------------------------------------------------

        std::cout
            << std::left
            << std::setw(8)
            << n

            << std::right
            << std::fixed
            << std::setprecision(3)

            << std::setw(20)
            << tiempoTradicional

            << std::setw(15)
            << tiempoDR1

            << std::setw(15)
            << tiempoDR2

            << std::setw(15)
            << (
                dr1Correcto && dr2Correcto
                    ? "OK"
                    : "ERROR"
            )

            << '\n';

        // Si existe algún error, se detiene el programa.
        if (!dr1Correcto || !dr2Correcto) {

            std::cerr
                << "\nERROR: los algoritmos entregaron "
                << "resultados diferentes para n = "
                << n
                << '\n';

            return 1;
        }
    }

    return 0;
}
