from __future__ import annotations

import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import main
from dpda import ejecutar, procesar_bloque, procesar_entrada


ACEPTADO = [
    "q1 q2",
    "0 1",
    "A L",
    "q1",
    "q2",
    "L",
    "(q1,0,L=q1,AL) (q1,0,A=q1,AA) (q1,1,A=q2,#) (q2,1,A=q2,#)",
    "000111",
]


class EjemplosDelPdf(unittest.TestCase):
    def test_ejemplo_aceptado(self) -> None:
        self.assertEqual(
            procesar_bloque(ACEPTADO),
            [
                ".000111 q1 L",
                "0.00111 q1 AL",
                "00.0111 q1 AAL",
                "000.111 q1 AAAL",
                "0001.11 q2 AAL",
                "00011.1 q2 AL",
                "000111. q2 L",
                "Aceptado",
            ],
        )

    def test_ejemplo_rechazado(self) -> None:
        lineas = ACEPTADO.copy()
        lineas[7] = "00011"
        self.assertEqual(
            procesar_bloque(lineas),
            [
                ".00011 q1 L",
                "0.0011 q1 AL",
                "00.011 q1 AAL",
                "000.11 q1 AAAL",
                "0001.1 q2 AAL",
                "00011. q2 AL",
                "Rechazado",
            ],
        )

    def test_ejemplo_no_determinista(self) -> None:
        lineas = ACEPTADO.copy()
        lineas[6] = "(q1,0,L=q1,AL) (q1,0,A=q1,AA) (q1,0,A=q2,AA) (q2,1,A=q2,#)"
        self.assertEqual(procesar_bloque(lineas), ["Error encontrado en 7"])

    def test_ejemplo_fondo_invalido(self) -> None:
        lineas = ACEPTADO.copy()
        lineas[5] = "T"
        self.assertEqual(procesar_bloque(lineas), ["Error encontrado en 6"])


class Validacion(unittest.TestCase):
    def assert_error(self, numero: int, indice: int, valor: str) -> None:
        lineas = ACEPTADO.copy()
        lineas[indice] = valor
        self.assertEqual(procesar_bloque(lineas), [f"Error encontrado en {numero}"])

    def test_estado_debe_comenzar_con_alfanumerico(self) -> None:
        self.assert_error(1, 0, "_q q2")

    def test_caracter_invalido_en_estado(self) -> None:
        self.assert_error(1, 0, "q.1 q2")

    def test_comilla_u201d_prohibida_en_estado(self) -> None:
        self.assert_error(1, 0, "q” q2")

    def test_comilla_u2018_prohibida_en_estado(self) -> None:
        self.assert_error(1, 0, "q‘ q2")

    def test_comilla_u201d_prohibida_en_pila(self) -> None:
        self.assert_error(3, 2, "A L ”")

    def test_comilla_u2018_prohibida_en_pila(self) -> None:
        self.assert_error(3, 2, "A L ‘")

    def test_otras_comillas_tipograficas_siguen_permitidas(self) -> None:
        for simbolo in ("“", "’", "«", "»"):
            with self.subTest(simbolo=simbolo):
                estado = "q" + simbolo
                lineas = [
                    estado, "a", simbolo, estado, estado, simbolo,
                    f"({estado},a,{simbolo}={estado},{simbolo})", "a",
                ]
                self.assertEqual(
                    procesar_bloque(lineas),
                    [f".a {estado} {simbolo}", f"a. {estado} {simbolo}", "Aceptado"],
                )

    def test_alfabetos_compactos_siguen_rechazados(self) -> None:
        for numero, indice, valor in ((2, 1, "01"), (3, 2, "AL")):
            with self.subTest(linea=numero):
                self.assert_error(numero, indice, valor)

    def test_simbolo_invalido_en_alfabeto_entrada(self) -> None:
        self.assert_error(2, 1, "0 +")

    def test_simbolo_invalido_en_alfabeto_pila(self) -> None:
        self.assert_error(3, 2, "A # L")

    def test_estado_inicial_inexistente(self) -> None:
        self.assert_error(4, 3, "q3")

    def test_estado_final_inexistente(self) -> None:
        self.assert_error(5, 4, "q3")

    def test_transicion_mal_formada(self) -> None:
        self.assert_error(7, 6, "(q1,0,L-q1,AL)")

    def test_estado_inexistente_en_transicion(self) -> None:
        self.assert_error(7, 6, "(q3,0,L=q1,AL)")

    def test_transicion_duplicada(self) -> None:
        lineas = ["q0", "a", "Z", "q0", "q0", "Z",
                  "(q0,a,Z=q0,Z) (q0,a,Z=q0,Z)", "a"]
        self.assertEqual(procesar_bloque(lineas),
                         [".a q0 Z", "a. q0 Z", "Aceptado"])

    def test_epsilon_conflicta_con_transicion_que_consume(self) -> None:
        self.assert_error(7, 6, "(q1,#,L=q1,L) (q1,0,L=q2,L)")

    def test_simbolo_invalido_en_palabra(self) -> None:
        self.assert_error(8, 7, "0012")


class Simulacion(unittest.TestCase):
    def test_palabra_vacia_aceptada(self) -> None:
        lineas = ["q0", "a", "Z", "q0", "q0", "Z", "(q0,a,Z=q0,Z)", "#"]
        self.assertEqual(procesar_bloque(lineas), [". q0 Z", "Aceptado"])

    def test_transicion_vacia(self) -> None:
        lineas = ["q0 q1", "a", "Z", "q0", "q1", "Z", "(q0,#,Z=q1,Z)", "#"]
        self.assertEqual(
            procesar_bloque(lineas), [". q0 Z", ". q1 Z", "Aceptado"]
        )

    def test_pila_vacia_rechaza(self) -> None:
        lineas = ["q0", "a", "Z", "q0", "q0", "Z", "(q0,a,Z=q0,#)", "a"]
        self.assertEqual(procesar_bloque(lineas), [".a q0 Z", "a. q0 ", "Rechazado"])

    def test_ciclo_de_configuracion_repetida(self) -> None:
        lineas = ["q0", "a", "Z", "q0", "q0", "Z", "(q0,#,Z=q0,Z)", "#"]
        self.assertEqual(
            procesar_bloque(lineas), [". q0 Z", ". q0 Z", "Rechazado"]
        )

    def test_ciclo_vacio_con_crecimiento_de_pila(self) -> None:
        lineas = ["q0", "a", "Z", "q0", "q0", "Z", "(q0,#,Z=q0,ZZ)", "#"]
        self.assertEqual(
            procesar_bloque(lineas), [". q0 Z", ". q0 ZZ", "Rechazado"]
        )

    def test_ciclo_de_crecimiento_con_varios_estados(self) -> None:
        lineas = [
            "q0 q1",
            "a",
            "A Z",
            "q0",
            "q0",
            "Z",
            "(q0,#,Z=q1,AZ) (q1,#,A=q0,ZA)",
            "#",
        ]
        self.assertEqual(
            procesar_bloque(lineas),
            [". q0 Z", ". q1 AZ", ". q0 ZAZ", "Rechazado"],
        )

    def test_desapilar_invalida_un_posible_ciclo_de_crecimiento(self) -> None:
        lineas = [
            "q r",
            "a",
            "A Z",
            "q",
            "q",
            "Z",
            "(q,#,Z=q,AZ) (q,#,A=r,#) (r,#,Z=q,AAZ)",
            "#",
        ]
        self.assertEqual(
            procesar_bloque(lineas),
            [
                ". q Z",
                ". q AZ",
                ". r Z",
                ". q AAZ",
                ". r AZ",
                "Rechazado",
            ],
        )

    def test_caracteres_especiales_permitidos(self) -> None:
        # ')' y '=' son válidos en estados/símbolos de pila y también se
        # pueden analizar sin confundirlos con los delimitadores externos.
        lineas = ["q) r=", "a", ") =", "q)", "r=", "=", "(q),a,==r=,=)", "a"]
        self.assertEqual(
            procesar_bloque(lineas), [".a q) =", "a. r= =", "Aceptado"]
        )


class EntradaCompleta(unittest.TestCase):
    def test_multiples_automatas_y_fin(self) -> None:
        segundo = ACEPTADO.copy()
        segundo[7] = "00011"
        entrada = [linea + "\n" for linea in ACEPTADO + segundo + ["_FIN", "ignorado"]]
        salida = procesar_entrada(entrada)
        self.assertEqual(
            salida,
            [
                ".000111 q1 L",
                "0.00111 q1 AL",
                "00.0111 q1 AAL",
                "000.111 q1 AAAL",
                "0001.11 q2 AAL",
                "00011.1 q2 AL",
                "000111. q2 L",
                "Aceptado",
                ".00011 q1 L",
                "0.0011 q1 AL",
                "00.011 q1 AAL",
                "000.11 q1 AAAL",
                "0001.1 q2 AAL",
                "00011. q2 AL",
                "Rechazado",
            ],
        )

    def test_fin_sin_automatas_no_imprime_nada(self) -> None:
        self.assertEqual(procesar_entrada(["_FIN\n", "ignorado\n"]), [])

    def test_fin_dentro_de_bloque_informa_linea_faltante(self) -> None:
        self.assertEqual(
            procesar_entrada(["q0\n", "a\n", "Z\n", "_FIN\n"]),
            ["Error encontrado en 4"],
        )

    def test_bloque_incompleto_prioriza_linea_faltante(self) -> None:
        for entrada in (["_q"], ["_q", "_FIN"]):
            with self.subTest(entrada=entrada):
                self.assertEqual(procesar_entrada(entrada), ["Error encontrado en 2"])

    def test_fin_de_archivo_dentro_de_bloque_informa_linea_faltante(self) -> None:
        self.assertEqual(
            procesar_entrada(["q0\n", "a\n", "Z\n", "q0\n", "q0\n", "Z\n"]),
            ["Error encontrado en 7"],
        )

    def test_fin_de_archivo_despues_de_bloque_completo_es_valido(self) -> None:
        self.assertEqual(procesar_entrada(ACEPTADO), procesar_bloque(ACEPTADO))

    def test_ejecutar_produce_salida_exacta(self) -> None:
        entrada = io.StringIO("\n".join(ACEPTADO + ["_FIN"]) + "\n")
        salida = io.StringIO()
        ejecutar(entrada, salida)
        esperado = "\n".join(
            [
                ".000111 q1 L",
                "0.00111 q1 AL",
                "00.0111 q1 AAL",
                "000.111 q1 AAAL",
                "0001.11 q2 AAL",
                "00011.1 q2 AL",
                "000111. q2 L",
                "Aceptado",
                "",
            ]
        )
        self.assertEqual(salida.getvalue(), esperado)

    def test_ejecutar_imprime_y_vacia_cada_bloque_inmediatamente(self) -> None:
        salida = io.StringIO()
        primera_salida = "\n".join(procesar_bloque(ACEPTADO)) + "\n"

        def entrada_por_etapas():
            for linea in ACEPTADO:
                yield linea + "\n"
            self.assertEqual(salida.getvalue(), primera_salida)
            yield "_FIN\n"

        ejecutar(entrada_por_etapas(), salida)
        self.assertEqual(salida.getvalue(), primera_salida)

    def test_cancelacion_interactiva_no_muestra_error(self) -> None:
        with patch.object(main, "ejecutar", side_effect=KeyboardInterrupt):
            main.main()


class CasosAdicionales(unittest.TestCase):
    def test_duplicados_con_resultados_distintos(self) -> None:
        for segunda in ("(q,a,Z=r,Z)", "(q,a,Z=q,AZ)"):
            with self.subTest(segunda=segunda):
                lineas = ["q r", "a", "A Z", "q", "r", "Z",
                          "(q,a,Z=q,Z) " + segunda, "a"]
                self.assertEqual(procesar_bloque(lineas), ["Error encontrado en 7"])

    def test_duplicados_epsilon_identicos(self) -> None:
        lineas = ["q f", "a", "Z", "q", "f", "Z",
                  "(q,#,Z=f,Z) (q,#,Z=f,Z)", "#"]
        self.assertEqual(procesar_bloque(lineas),
                         [". q Z", ". f Z", "Aceptado"])

    def test_duplicados_epsilon_conflictivos(self) -> None:
        for segunda in ("(q,#,Z=q,Z)", "(q,#,Z=f,ZZ)"):
            with self.subTest(segunda=segunda):
                lineas = ["q f", "a", "Z", "q", "f", "Z",
                          "(q,#,Z=f,Z) " + segunda, "#"]
                self.assertEqual(procesar_bloque(lineas), ["Error encontrado en 7"])

    def test_duplicados_no_ocultan_conflicto_epsilon(self) -> None:
        epsilon, consumo = "(q,#,Z=q,Z)", "(q,a,Z=q,Z)"
        for transiciones in (f"{epsilon} {epsilon} {consumo}",
                             f"{consumo} {consumo} {epsilon}"):
            with self.subTest(transiciones=transiciones):
                lineas = ["q", "a", "Z", "q", "q", "Z", transiciones, "a"]
                self.assertEqual(procesar_bloque(lineas), ["Error encontrado en 7"])

    def test_duplicados_no_consecutivos(self) -> None:
        lineas = ["q f", "a b", "Z", "q", "f", "Z",
                  "(q,a,Z=q,Z) (q,b,Z=f,Z) (q,a,Z=q,Z)", "ab"]
        self.assertEqual(procesar_bloque(lineas),
                         [".ab q Z", "a.b q Z", "ab. f Z", "Aceptado"])

    def test_epsilon_antes_y_despues_del_consumo(self) -> None:
        lineas = ["s q r f", "a", "A B Z", "s", "f", "Z",
                  "(s,#,Z=q,ABZ) (q,a,A=r,#) (r,#,B=f,#)", "a"]
        self.assertEqual(procesar_bloque(lineas),
                         [".a s Z", ".a q ABZ", "a. r BZ", "a. f Z", "Aceptado"])

    def test_reconstruccion_de_pila_termina_aceptando(self) -> None:
        lineas = ["s q r f", "a", "A B Z", "s", "f", "Z",
                  "(s,#,Z=q,AZ) (q,#,A=r,#) (r,#,Z=q,ABZ) (r,#,B=f,#)", "#"]
        self.assertEqual(procesar_bloque(lineas),
                         [". s Z", ". q AZ", ". r Z", ". q ABZ",
                          ". r BZ", ". f Z", "Aceptado"])

    def test_tres_condiciones_de_aceptacion_independientes(self) -> None:
        casos = [
            ("(q,a,Z=f,Z)", "aa", [".aa q Z", "a.a f Z", "Rechazado"]),
            ("(q,a,Z=f,AZ)", "a", [".a q Z", "a. f AZ", "Rechazado"]),
            ("(q,a,Z=q,Z)", "a", [".a q Z", "a. q Z", "Rechazado"]),
        ]
        for transiciones, palabra, esperado in casos:
            with self.subTest(transiciones=transiciones):
                lineas = ["q f", "a", "A Z", "q", "f", "Z", transiciones, palabra]
                self.assertEqual(procesar_bloque(lineas), esperado)

    def test_simbolos_especiales_en_estados_y_transiciones(self) -> None:
        for simbolo in ("(", ")", "=", "_", "+", "-", "\\", ":", "[", "]"):
            with self.subTest(simbolo=simbolo):
                q, f = "q" + simbolo, "f" + simbolo
                lineas = [f"{q} {f}", "a", simbolo, q, f, simbolo,
                          f"({q},a,{simbolo}={f},{simbolo})", "a"]
                self.assertEqual(procesar_bloque(lineas),
                                 [f".a {q} {simbolo}", f"a. {f} {simbolo}", "Aceptado"])

    def test_sintaxis_y_referencias_invalidas_en_transiciones(self) -> None:
        for texto in ("(q1,0,L=q1,)", "(q1,0,L=q1,#L)", "(q1,0,L=q1,L)basura",
                      "(q1,0,L=q1,L)(q1,1,L=q1,L)", "(q1,2,L=q1,L)",
                      "(q1,0,T=q1,L)", "(q1,0,L=q1,T)", "(q1,0,L=q3,L)"):
            with self.subTest(texto=texto):
                lineas = ACEPTADO.copy()
                lineas[6] = texto
                self.assertEqual(procesar_bloque(lineas), ["Error encontrado en 7"])

    def test_prioridad_entre_errores_de_bloque_completo(self) -> None:
        # Cada prefijo válido debe dejar como primer error la línea siguiente.
        for indice in range(8):
            with self.subTest(linea=indice + 1):
                lineas = ACEPTADO[:indice] + [""] * (8 - indice)
                self.assertEqual(procesar_bloque(lineas),
                                 [f"Error encontrado en {indice + 1}"])

    def test_palabra_larga_y_muchas_transiciones(self) -> None:
        cantidad = 1000
        estados = [f"q{i}" for i in range(cantidad + 1)]
        palabra = "a" * cantidad
        transiciones = " ".join(f"(q{i},a,Z=q{i + 1},Z)" for i in range(cantidad))
        lineas = [" ".join(estados), "a", "Z", "q0", estados[-1], "Z",
                  transiciones, palabra]
        esperado = [f"{palabra[:i]}.{palabra[i:]} q{i} Z" for i in range(cantidad + 1)]
        self.assertEqual(procesar_bloque(lineas), esperado + ["Aceptado"])

    def test_muchos_desapilados_epsilon_no_son_un_ciclo(self) -> None:
        cantidad = 1000
        lineas = ["q r f", "a", "A Z", "q", "f", "Z",
                  f"(q,#,Z=r,{'A' * cantidad}Z) (r,#,A=r,#) (r,#,Z=f,Z)", "#"]
        esperado = [". q Z"] + [f". r {'A' * n}Z" for n in range(cantidad, -1, -1)]
        self.assertEqual(procesar_bloque(lineas), esperado + [". f Z", "Aceptado"])

    def test_cli_bloques_y_salida_de_pila_vacia(self) -> None:
        bloque = ["q", "a", "Z", "q", "q", "Z", "(q,a,Z=q,#)", "a"]
        duplicado = ["q", "a", "Z", "q", "q", "Z",
                     "(q,a,Z=q,Z) (q,a,Z=q,Z)", "a"]
        entrada = "\n".join(bloque + duplicado + ["_FIN", "ignorado"]) + "\n"
        proceso = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parents[1] / "main.py")],
            input=entrada, text=True, capture_output=True, timeout=10,
        )
        self.assertEqual(proceso.returncode, 0)
        self.assertEqual(proceso.stderr, "")
        self.assertEqual(proceso.stdout,
                         ".a q Z\na. q \nRechazado\n.a q Z\na. q Z\nAceptado\n")


class RegresionesDeEntrega(unittest.TestCase):
    def test_todos_los_caracteres_prohibidos(self) -> None:
        for simbolo in ("#", "”", "‘", ",", "."):
            for indice, valor in ((0, "q1" + simbolo + " q2"),
                                  (2, "A L " + simbolo)):
                with self.subTest(simbolo=simbolo, linea=indice + 1):
                    bloque = ACEPTADO.copy()
                    bloque[indice] = valor
                    self.assertEqual(procesar_bloque(bloque),
                                     [f"Error encontrado en {indice + 1}"])

    def test_comillas_ascii_en_estados_y_fondo_de_pila(self) -> None:
        for simbolo in ('"', "'"):
            with self.subTest(simbolo=simbolo):
                q, f = "q" + simbolo + "0", "f" + simbolo + "1"
                bloque = [f"{q} {f}", "a", simbolo, q, f, simbolo,
                          f"({q},a,{simbolo}={f},{simbolo})", "a"]
                self.assertEqual(procesar_bloque(bloque),
                                 [f".a {q} {simbolo}", f"a. {f} {simbolo}", "Aceptado"])

    def test_comillas_ascii_apilado_y_desapilado_en_cli(self) -> None:
        bloque = [
            "q\"0 r'1 f\"'2", "a b", "Z \" '", 'q"0', 'f\"\'2', "Z",
            "(q\"0,a,Z=r'1,\"'Z) (r'1,b,\"=r'1,#) (r'1,#,'=f\"'2,#)",
            "ab",
        ]
        esperado = b'.ab q"0 Z\na.b r\'1 "\'Z\nab. r\'1 \'Z\nab. f"\'2 Z\nAceptado\n'
        proceso = subprocess.run(
            [sys.executable, "main.py"], cwd=Path(__file__).resolve().parents[1],
            input=("\n".join(bloque + ["_FIN", "ignorado"]) + "\n").encode(),
            capture_output=True, timeout=10,
        )
        self.assertEqual(proceso.returncode, 0)
        self.assertEqual(proceso.stderr, b"")
        self.assertEqual(proceso.stdout, esperado)

    def test_especiales_no_pueden_iniciar_estados_ni_ser_entrada(self) -> None:
        for simbolo in ('"', "'", "_", "+", "-", "(", ")", "="):
            for indice, valor in ((0, simbolo + "q q2"), (1, "0 " + simbolo)):
                with self.subTest(simbolo=simbolo, linea=indice + 1):
                    bloque = ACEPTADO.copy()
                    bloque[indice] = valor
                    self.assertEqual(procesar_bloque(bloque),
                                     [f"Error encontrado en {indice + 1}"])

    def test_todos_los_bloques_incompletos(self) -> None:
        for cantidad in range(1, 8):
            for cierre in ([], ["_FIN", "ignorado"]):
                with self.subTest(cantidad=cantidad, cierre=cierre):
                    self.assertEqual(procesar_entrada(ACEPTADO[:cantidad] + cierre),
                                     [f"Error encontrado en {cantidad + 1}"])

    def test_continua_despues_de_un_bloque_invalido(self) -> None:
        invalido = ACEPTADO.copy()
        invalido[5] = "T"
        self.assertEqual(procesar_entrada(invalido + ACEPTADO + ["_FIN"]),
                         ["Error encontrado en 6"] + procesar_bloque(ACEPTADO))

    def test_no_acepta_antes_de_finalizar_el_computo(self) -> None:
        bloque = ["q r", "a", "Z", "q", "q", "Z",
                  "(q,#,Z=r,Z)", "#"]
        self.assertEqual(procesar_bloque(bloque),
                         [". q Z", ". r Z", "Rechazado"])

    def test_fin_de_linea_windows(self) -> None:
        self.assertEqual(procesar_entrada(
            [linea + "\r\n" for linea in ACEPTADO + ["_FIN"]]),
            procesar_bloque(ACEPTADO))

    def test_cuatro_ejemplos_en_cli(self) -> None:
        rechazado = ACEPTADO.copy()
        rechazado[7] = "00011"
        no_determinista = ACEPTADO.copy()
        no_determinista[6] = (
            "(q1,0,L=q1,AL) (q1,0,A=q1,AA) (q1,0,A=q2,AA) (q2,1,A=q2,#)"
        )
        fondo_invalido = ACEPTADO.copy()
        fondo_invalido[5] = "T"
        entrada = "\n".join(ACEPTADO + rechazado + no_determinista +
                            fondo_invalido + ["_FIN", "ignorado"]) + "\n"
        proceso = subprocess.run(
            [sys.executable, "main.py"],
            cwd=Path(__file__).resolve().parents[1],
            input=entrada, text=True, capture_output=True, timeout=10,
        )
        self.assertEqual(proceso.returncode, 0)
        self.assertEqual(proceso.stderr, "")
        self.assertEqual(proceso.stdout, (
            ".000111 q1 L\n0.00111 q1 AL\n00.0111 q1 AAL\n"
            "000.111 q1 AAAL\n0001.11 q2 AAL\n00011.1 q2 AL\n"
            "000111. q2 L\nAceptado\n"
            ".00011 q1 L\n0.0011 q1 AL\n00.011 q1 AAL\n"
            "000.11 q1 AAAL\n0001.1 q2 AAL\n00011. q2 AL\nRechazado\n"
            "Error encontrado en 7\nError encontrado en 6\n"
        ))


if __name__ == "__main__":
    unittest.main()
