#!/usr/bin/env python3
"""Punto de entrada del simulador de APD."""

import sys

from dpda import ejecutar


def main() -> None:
    try:
        ejecutar(sys.stdin, sys.stdout)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
