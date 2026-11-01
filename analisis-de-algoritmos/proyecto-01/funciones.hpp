#pragma once

#include <vector>

using Matrix = std::vector<std::vector<int>>;

Matrix generarMatrizAleatoria(int n);

void imprimirMatriz(const Matrix& M);

Matrix algoritmoTradicional(
    const Matrix& A,
    const Matrix& B
);

Matrix algoritmoDR1(
    const Matrix& A,
    const Matrix& B
);

Matrix algoritmoDR2(
    const Matrix& A,
    const Matrix& B
);
