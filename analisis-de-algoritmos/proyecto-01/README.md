# Proyecto 01 — Multiplicación de matrices

Asignatura: **Análisis de Algoritmos y Teoría de Autómatas (AATA)** — Universidad del Bío-Bío.

## Descripción

Implementación y comparación de tres algoritmos de multiplicación de matrices cuadradas:

- **Tradicional:** multiplicación directa de matrices.
- **DR1:** divide y vencerás mediante la Propiedad 1.
- **DR2:** divide y vencerás mediante la Propiedad 2 (algoritmo de Strassen).

Se miden tiempos de ejecución para distintos tamaños de matrices y se verifica que los tres algoritmos produzcan resultados equivalentes. El proyecto también considera el análisis del comportamiento asintótico de DR1 y DR2.

## Archivos

- `main.cpp`: programa principal, pruebas y medición de tiempos.
- `funciones.cpp`: implementación de los algoritmos.
- `funciones.hpp`: declaraciones y tipo de matriz.
- `aata.pdf`: documento de la actividad académica.

## Compilación

Desde esta carpeta, con un compilador compatible con C++17:

```bash
g++ -std=c++17 -O2 -Wall -Wextra -pedantic main.cpp funciones.cpp -o matrices
```

## Ejecución

```bash
./matrices
```

Sin argumentos, el programa recorre los tamaños indicados en `main.cpp`. Para limitar las pruebas, por ejemplo, hasta matrices de 1024 × 1024:

```bash
./matrices 1024
```

Las pruebas con matrices grandes pueden tardar bastante y consumir recursos significativos.
