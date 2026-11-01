#include "funciones.hpp"

#include <iostream>
#include <random>

namespace {

// Umbral práctico para evitar el costo de dividir matrices pequeñas.
// Al ser constante, no modifica la complejidad asintótica.
constexpr int UMBRAL_CASO_BASE = 64;

// Crea una matriz n x n inicializada con un valor.
Matrix crearMatriz(int n, int valor = 0) {
    return Matrix(n, std::vector<int>(n, valor));
}

// Suma dos matrices.
Matrix sumarMatrices(const Matrix& A, const Matrix& B) {
    const int n = static_cast<int>(A.size());

    Matrix C = crearMatriz(n);

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            C[i][j] = A[i][j] + B[i][j];
        }
    }

    return C;
}

// Resta dos matrices.
Matrix restarMatrices(const Matrix& A, const Matrix& B) {
    const int n = static_cast<int>(A.size());

    Matrix C = crearMatriz(n);

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            C[i][j] = A[i][j] - B[i][j];
        }
    }

    return C;
}

// Divide una matriz en cuatro submatrices.
//
// M = | M11 M12 |
//     | M21 M22 |
void dividirMatriz(
    const Matrix& M,
    Matrix& M11,
    Matrix& M12,
    Matrix& M21,
    Matrix& M22
) {
    const int n = static_cast<int>(M.size());
    const int mitad = n / 2;

    M11 = crearMatriz(mitad);
    M12 = crearMatriz(mitad);
    M21 = crearMatriz(mitad);
    M22 = crearMatriz(mitad);

    for (int i = 0; i < mitad; ++i) {
        for (int j = 0; j < mitad; ++j) {

            // Cuadrante superior izquierdo
            M11[i][j] = M[i][j];

            // Cuadrante superior derecho
            M12[i][j] = M[i][j + mitad];

            // Cuadrante inferior izquierdo
            M21[i][j] = M[i + mitad][j];

            // Cuadrante inferior derecho
            M22[i][j] = M[i + mitad][j + mitad];
        }
    }
}

// Une las cuatro submatrices para formar la matriz completa.
Matrix combinarMatrices(
    const Matrix& C11,
    const Matrix& C12,
    const Matrix& C21,
    const Matrix& C22
) {
    const int mitad = static_cast<int>(C11.size());

    Matrix C = crearMatriz(mitad * 2);

    for (int i = 0; i < mitad; ++i) {
        for (int j = 0; j < mitad; ++j) {

            C[i][j] = C11[i][j];

            C[i][j + mitad] = C12[i][j];

            C[i + mitad][j] = C21[i][j];

            C[i + mitad][j + mitad] = C22[i][j];
        }
    }

    return C;
}

}  // namespace

// ----------------------------------------------------
// GENERACIÓN DE MATRICES
// ----------------------------------------------------

Matrix generarMatrizAleatoria(int n) {

    static std::mt19937 generador(std::random_device{}());

    // Números enteros aleatorios entre 0 y 9.
    static std::uniform_int_distribution<int> distribucion(0, 9);

    Matrix M = crearMatriz(n);

    for (auto& fila : M) {
        for (auto& elemento : fila) {
            elemento = distribucion(generador);
        }
    }

    return M;
}

// Función útil para probar matrices pequeñas.
// No se utiliza al medir los tiempos.
void imprimirMatriz(const Matrix& M) {

    for (const auto& fila : M) {

        for (int elemento : fila) {
            std::cout << elemento << ' ';
        }

        std::cout << '\n';
    }
}

// ----------------------------------------------------
// ALGORITMO TRADICIONAL
// ----------------------------------------------------

Matrix algoritmoTradicional(
    const Matrix& A,
    const Matrix& B
) {
    const int n = static_cast<int>(A.size());

    Matrix C = crearMatriz(n);

    /*
        Cij = sumatoria desde k=0 hasta n-1
              de Aik * Bkj
    */

    for (int i = 0; i < n; ++i) {

        for (int j = 0; j < n; ++j) {

            for (int k = 0; k < n; ++k) {

                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    return C;
}

// ----------------------------------------------------
// DR1 - PROPIEDAD 1
// ----------------------------------------------------

Matrix algoritmoDR1(
    const Matrix& A,
    const Matrix& B
) {
    const int n = static_cast<int>(A.size());

    // Caso base.
    if (n <= UMBRAL_CASO_BASE) {
        return algoritmoTradicional(A, B);
    }

    // Submatrices de A.
    Matrix A11;
    Matrix A12;
    Matrix A21;
    Matrix A22;

    // Submatrices de B.
    Matrix B11;
    Matrix B12;
    Matrix B21;
    Matrix B22;

    dividirMatriz(
        A,
        A11,
        A12,
        A21,
        A22
    );

    dividirMatriz(
        B,
        B11,
        B12,
        B21,
        B22
    );

    /*
        Propiedad 1:

        C11 = A11*B11 + A12*B21

        C12 = A11*B12 + A12*B22

        C21 = A21*B11 + A22*B21

        C22 = A21*B12 + A22*B22
    */

    Matrix C11 = sumarMatrices(

        algoritmoDR1(A11, B11),

        algoritmoDR1(A12, B21)
    );

    Matrix C12 = sumarMatrices(

        algoritmoDR1(A11, B12),

        algoritmoDR1(A12, B22)
    );

    Matrix C21 = sumarMatrices(

        algoritmoDR1(A21, B11),

        algoritmoDR1(A22, B21)
    );

    Matrix C22 = sumarMatrices(

        algoritmoDR1(A21, B12),

        algoritmoDR1(A22, B22)
    );

    // Se reconstruye la matriz resultado.
    return combinarMatrices(
        C11,
        C12,
        C21,
        C22
    );
}

// ----------------------------------------------------
// DR2 - PROPIEDAD 2 / STRASSEN
// ----------------------------------------------------

Matrix algoritmoDR2(
    const Matrix& A,
    const Matrix& B
) {
    const int n = static_cast<int>(A.size());

    // Caso base.
    if (n <= UMBRAL_CASO_BASE) {
        return algoritmoTradicional(A, B);
    }

    // Submatrices de A.
    Matrix A11;
    Matrix A12;
    Matrix A21;
    Matrix A22;

    // Submatrices de B.
    Matrix B11;
    Matrix B12;
    Matrix B21;
    Matrix B22;

    dividirMatriz(
        A,
        A11,
        A12,
        A21,
        A22
    );

    dividirMatriz(
        B,
        B11,
        B12,
        B21,
        B22
    );

    /*
        Propiedad 2:

        M = (A11 + A22)(B11 + B22)

        N = (A21 + A22)B11

        O = A11(B12 - B22)

        P = A22(B21 - B11)

        Q = (A11 + A12)B22

        R = (A21 - A11)(B11 + B12)

        S = (A12 - A22)(B21 + B22)
    */

    Matrix M = algoritmoDR2(

        sumarMatrices(A11, A22),

        sumarMatrices(B11, B22)
    );

    Matrix N = algoritmoDR2(

        sumarMatrices(A21, A22),

        B11
    );

    Matrix O = algoritmoDR2(

        A11,

        restarMatrices(B12, B22)
    );

    Matrix P = algoritmoDR2(

        A22,

        restarMatrices(B21, B11)
    );

    Matrix Q = algoritmoDR2(

        sumarMatrices(A11, A12),

        B22
    );

    Matrix R = algoritmoDR2(

        restarMatrices(A21, A11),

        sumarMatrices(B11, B12)
    );

    Matrix S = algoritmoDR2(

        restarMatrices(A12, A22),

        sumarMatrices(B21, B22)
    );

    /*
        Ahora se calculan las cuatro partes
        de la matriz C.

        C11 = M + P - Q + S
    */

    Matrix C11 = sumarMatrices(

        restarMatrices(
            sumarMatrices(M, P),
            Q
        ),

        S
    );

    // C12 = O + Q
    Matrix C12 = sumarMatrices(
        O,
        Q
    );

    // C21 = N + P
    Matrix C21 = sumarMatrices(
        N,
        P
    );

    // C22 = M + O - N + R
    Matrix C22 = sumarMatrices(

        restarMatrices(
            sumarMatrices(M, O),
            N
        ),

        R
    );

    // Se reconstruye la matriz final.
    return combinarMatrices(
        C11,
        C12,
        C21,
        C22
    );
}
