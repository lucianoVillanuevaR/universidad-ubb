"""Auditoría reproducible: 24.000 casos, sin dependencias externas.

El oráculo recibe reglas generadas, no objetos ni funciones del analizador real.
Las familias finitas tienen cotas demostrables; agotar una cota es un fallo.
"""
import random
import signal
import subprocess
import sys
import unittest
from contextlib import contextmanager
from pathlib import Path

from dpda import procesar_bloque

SEED = 20261104
ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def plazo(segundos=45):
    # SIGALRM está disponible en el Linux de la auditoría. En otras plataformas,
    # ejecutar la suite mediante subprocess.run(..., timeout=...) externamente.
    if not hasattr(signal, 'SIGALRM'):
        yield
        return
    def expiro(*_):
        raise TimeoutError('Auditoría excedió el plazo; no cuenta como aprobada')
    anterior = signal.signal(signal.SIGALRM, expiro)
    signal.alarm(segundos)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, anterior)


def generar(rng, epsilon=False):
    n = rng.choice((2, 3, 6, 12, 24))
    estados = [f'q{i}' for i in range(n)]
    finales = set(rng.sample(estados, rng.randint(1, n)))
    reglas = []
    for i, q in enumerate(estados):
        for tope in 'ZAB':
            if epsilon and i + 1 < n and rng.random() < .45:
                reglas.append((q, '', tope, rng.choice(estados[i+1:]),
                               rng.choice(('', tope, 'AB', 'AZ', 'BAZ'))))
            else:
                for letra in 'ab':
                    if rng.random() < .7:
                        reglas.append((q, letra, tope, rng.choice(estados),
                                       rng.choice(('', tope, 'AB', 'AZ', 'BAZ'))))
    if not reglas:
        reglas.append(('q0', 'a', 'Z', 'q0', 'Z'))
    palabra = ''.join(rng.choices('ab', k=rng.randint(0, 35)))
    return estados, finales, reglas, palabra


def serializar(modelo):
    estados, finales, reglas, palabra = modelo
    transiciones = ' '.join(
        f'({q},{a or "#"},{z}={r},{w or "#"})' for q, a, z, r, w in reglas)
    return [' '.join(estados), 'a b', 'Z A B', estados[0],
            ' '.join(sorted(finales)), 'Z', transiciones, palabra or '#']


def referencia(modelo, limite, prefijo=False):
    """Intérprete por búsqueda lineal; pila mutable con tope a la derecha.

    No detecta ciclos ni importa validadores, modelos o formateadores reales.
    """
    estados, finales, reglas, palabra = modelo
    estado, cursor, pila = estados[0], 0, ['Z']
    traza = []
    for _ in range(limite + 1):
        traza.append(palabra[:cursor] + '.' + palabra[cursor:] + ' ' +
                     estado + ' ' + ''.join(reversed(pila)))
        disponibles = [regla for regla in reglas
                       if pila and regla[0] == estado and regla[2] == pila[-1]
                       and (regla[1] == '' or
                            (cursor < len(palabra) and regla[1] == palabra[cursor]))]
        if not disponibles:
            aceptado = cursor == len(palabra) and estado in finales and pila == ['Z']
            return traza + ['Aceptado' if aceptado else 'Rechazado']
        if len(disponibles) != 1:
            raise AssertionError('Generador produjo no determinismo')
        _, letra, _, estado, reemplazo = disponibles[0]
        pila.pop()
        pila.extend(reversed(reemplazo))
        cursor += len(letra)
    if prefijo:
        return traza
    raise AssertionError('Oráculo no concluyente: cota agotada')


class AuditoriaMasiva(unittest.TestCase):
    def test_8000_consumo(self):
        rng = random.Random(SEED)
        with plazo():
            for i in range(8000):
                modelo = generar(rng)
                bloque = serializar(modelo)
                with self.subTest(caso=i, semilla=SEED, entrada=bloque):
                    # Cada transición consume un carácter: máximo |palabra| pasos.
                    self.assertEqual(procesar_bloque(bloque),
                                     referencia(modelo, len(modelo[3]) + 1))

    def test_4000_epsilon_finitos(self):
        rng = random.Random(SEED + 1)
        with plazo():
            for i in range(4000):
                modelo = generar(rng, epsilon=True)
                bloque = serializar(modelo)
                with self.subTest(caso=i, semilla=SEED + 1, entrada=bloque):
                    # Epsilon aumenta estrictamente el índice de estado.
                    # Entre dos consumos hay menos de |Q| pasos epsilon.
                    limite = len(modelo[0]) * (len(modelo[3]) + 1) + 1
                    self.assertEqual(procesar_bloque(bloque), referencia(modelo, limite))

    def test_4000_ciclos_demostrables(self):
        rng = random.Random(SEED + 2)
        with plazo():
            for i in range(4000):
                n = rng.randint(1, 25)
                estados = [f'q{j}' for j in range(n)] + ['f']
                crecimiento = rng.randint(0, 5)
                reglas = [(estados[j], '', z, estados[(j+1) % n], 'A' * crecimiento + z)
                          for j in range(n) for z in 'ZA']
                modelo = (estados, {'f'}, reglas, rng.choice(('', 'a', 'aa')))
                bloque = serializar(modelo)
                with self.subTest(caso=i, semilla=SEED + 2, entrada=bloque):
                    # Siempre hay transición; nunca se consume, desapila ni llega a f.
                    # Sin crecimiento es un anillo; con crecimiento la pila crece sin cota.
                    obtenido = procesar_bloque(bloque)
                    self.assertEqual(obtenido[-1], 'Rechazado')
                    prefijo = referencia(modelo, 3*n + 3, prefijo=True)
                    self.assertGreaterEqual(len(obtenido), 3)
                    self.assertLessEqual(len(obtenido) - 1, len(prefijo))
                    self.assertEqual(obtenido[:-1], prefijo[:len(obtenido)-1])

    def test_8000_invalidos(self):
        rng = random.Random(SEED + 3)
        with plazo():
            for i in range(8000):
                bloque = serializar(generar(rng, epsilon=True))
                linea = i % 8
                errores = [
                    ('_q', 'q.0', 'q,0', '#'),
                    ('ab', 'a +', 'a #', 'a aa'),
                    ('ZA', 'Z #', 'Z ,', 'Z .'),
                    ('ausente', 'q0 q1', '#', ''),
                    ('ausente', 'q0 ausente', '#'),
                    ('X', 'ZZ', '#', ''),
                    ('(q0,a,Z-q0,Z)', '(q0,a,X=q0,Z)', '(q0,a,Z=ausente,Z)',
                     '(q0,a,Z=q0,X)', '(q0,c,Z=q0,Z)', '(q0,a,Z=q0,#Z)',
                     '(q0,a,Z=q0,Z) (q0,a,Z=q1,Z)',
                     '(q0,#,Z=q0,Z) (q0,a,Z=q1,Z)'),
                    ('c', 'a b', '#a', ''),
                ]
                bloque[linea] = rng.choice(errores[linea])
                with self.subTest(caso=i, semilla=SEED + 3, entrada=bloque):
                    self.assertEqual(procesar_bloque(bloque),
                                     [f'Error encontrado en {linea + 1}'])


class IntegracionAuditada(unittest.TestCase):
    def test_200_bloques_sin_site_packages(self):
        rng = random.Random(SEED + 4)
        entrada, esperado = [], []
        for _ in range(200):
            modelo = generar(rng, epsilon=True)
            entrada.extend(serializar(modelo))
            esperado.extend(referencia(modelo, len(modelo[0]) * (len(modelo[3])+1) + 1))
        proceso = subprocess.run(
            [sys.executable, '-S', 'main.py'], cwd=ROOT,
            input='\n'.join(entrada + ['_FIN', 'ignorado']) + '\n',
            text=True, capture_output=True, timeout=15)
        self.assertEqual(proceso.returncode, 0)
        self.assertEqual(proceso.stderr, '')
        self.assertEqual(proceso.stdout, '\n'.join(esperado) + '\n')


if __name__ == '__main__':
    unittest.main()
