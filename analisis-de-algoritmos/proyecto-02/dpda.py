"""Validacion y simulacion de automatas con pila deterministas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence, TextIO


# Lectura literal de la página 1: U+201D y U+2018, no comillas ASCII.
# Existe una posible ambigüedad tipográfica; no se amplía la lista del PDF.
CARACTERES_PROHIBIDOS = frozenset({"#", "”", "‘", ",", "."})


class ErrorValidacion(ValueError):
    """Error asociado a una de las ocho lineas del automata."""

    def __init__(self, numero_linea: int) -> None:
        super().__init__(f"Error encontrado en {numero_linea}")
        self.numero_linea = numero_linea


@dataclass(frozen=True)
class Transicion:
    estado_origen: str
    simbolo_entrada: str
    tope_pila: str
    estado_destino: str
    palabra_pila: str


@dataclass(frozen=True)
class Automata:
    estados: frozenset[str]
    alfabeto_entrada: frozenset[str]
    alfabeto_pila: frozenset[str]
    estado_inicial: str
    estados_finales: frozenset[str]
    fondo_pila: str
    transiciones: dict[tuple[str, str, str], Transicion]
    palabra: str


def _tokens(linea: str) -> list[str]:
    return linea.split()


def _contiene_caracter_prohibido(texto: str) -> bool:
    return any(caracter in CARACTERES_PROHIBIDOS for caracter in texto)


def _validar_estados(linea: str) -> frozenset[str]:
    estados = _tokens(linea)
    if not estados:
        raise ErrorValidacion(1)

    for estado in estados:
        if not estado[0].isalnum() or _contiene_caracter_prohibido(estado):
            raise ErrorValidacion(1)
    return frozenset(estados)


def _validar_alfabeto_entrada(linea: str) -> frozenset[str]:
    simbolos = _tokens(linea)
    if not simbolos or any(len(simbolo) != 1 or not simbolo.isalnum() for simbolo in simbolos):
        raise ErrorValidacion(2)
    return frozenset(simbolos)


def _validar_alfabeto_pila(linea: str) -> frozenset[str]:
    simbolos = _tokens(linea)
    if not simbolos:
        raise ErrorValidacion(3)
    if any(len(simbolo) != 1 or _contiene_caracter_prohibido(simbolo) for simbolo in simbolos):
        raise ErrorValidacion(3)
    return frozenset(simbolos)


def _validar_estado_inicial(linea: str, estados: frozenset[str]) -> str:
    valores = _tokens(linea)
    if len(valores) != 1 or valores[0] not in estados:
        raise ErrorValidacion(4)
    return valores[0]


def _validar_estados_finales(linea: str, estados: frozenset[str]) -> frozenset[str]:
    valores = _tokens(linea)
    if not valores or any(estado not in estados for estado in valores):
        raise ErrorValidacion(5)
    return frozenset(valores)


def _validar_fondo_pila(linea: str, alfabeto_pila: frozenset[str]) -> str:
    valores = _tokens(linea)
    if len(valores) != 1 or len(valores[0]) != 1 or valores[0] not in alfabeto_pila:
        raise ErrorValidacion(6)
    return valores[0]


def _analizar_transicion(
    texto: str,
    estados: frozenset[str],
    alfabeto_entrada: frozenset[str],
    alfabeto_pila: frozenset[str],
) -> Transicion:
    # Las tres comas son inequívocas: estados y símbolos de pila no pueden
    # contenerlas. El '=' separador va después del único símbolo del tope.
    if len(texto) < 2 or texto[0] != "(" or texto[-1] != ")":
        raise ErrorValidacion(7)

    partes = texto[1:-1].split(",")
    if len(partes) != 4:
        raise ErrorValidacion(7)

    estado_origen, simbolo_entrada, tope_y_destino, palabra_pila_cruda = partes
    if len(simbolo_entrada) != 1 or len(tope_y_destino) < 3 or tope_y_destino[1] != "=":
        raise ErrorValidacion(7)

    tope_pila = tope_y_destino[0]
    estado_destino = tope_y_destino[2:]
    if estado_origen not in estados or estado_destino not in estados:
        raise ErrorValidacion(7)
    if simbolo_entrada != "#" and simbolo_entrada not in alfabeto_entrada:
        raise ErrorValidacion(7)
    if tope_pila not in alfabeto_pila or not palabra_pila_cruda:
        raise ErrorValidacion(7)

    if palabra_pila_cruda == "#":
        palabra_pila = ""
    elif all(simbolo in alfabeto_pila for simbolo in palabra_pila_cruda):
        palabra_pila = palabra_pila_cruda
    else:
        raise ErrorValidacion(7)

    return Transicion(
        estado_origen,
        simbolo_entrada,
        tope_pila,
        estado_destino,
        palabra_pila,
    )


def _validar_transiciones(
    linea: str,
    estados: frozenset[str],
    alfabeto_entrada: frozenset[str],
    alfabeto_pila: frozenset[str],
) -> dict[tuple[str, str, str], Transicion]:
    textos = _tokens(linea)
    if not textos:
        raise ErrorValidacion(7)

    transiciones: dict[tuple[str, str, str], Transicion] = {}
    entradas_por_estado_y_tope: dict[tuple[str, str], set[str]] = {}

    for texto in textos:
        transicion = _analizar_transicion(texto, estados, alfabeto_entrada, alfabeto_pila)
        clave = (
            transicion.estado_origen,
            transicion.simbolo_entrada,
            transicion.tope_pila,
        )
        if clave in transiciones:
            if transiciones[clave] != transicion:
                raise ErrorValidacion(7)
            # Repetir el mismo elemento no cambia la relación de transición.
            continue
        transiciones[clave] = transicion

        grupo = (transicion.estado_origen, transicion.tope_pila)
        entradas = entradas_por_estado_y_tope.setdefault(grupo, set())
        entradas.add(transicion.simbolo_entrada)
        # Una transición epsilon excluye toda transición que consuma entrada
        # para el mismo par (estado, tope de pila).
        if "#" in entradas and len(entradas) > 1:
            raise ErrorValidacion(7)

    return transiciones


def _validar_palabra(linea: str, alfabeto_entrada: frozenset[str]) -> str:
    valor = linea.strip()
    if not valor:
        raise ErrorValidacion(8)
    if valor == "#":
        return ""
    if any(simbolo not in alfabeto_entrada for simbolo in valor):
        raise ErrorValidacion(8)
    return valor


def analizar_automata(lineas: Sequence[str]) -> Automata:
    """Valida exactamente ocho líneas y construye un APD."""
    if len(lineas) != 8:
        numero = min(len(lineas) + 1, 8)
        raise ErrorValidacion(numero)

    estados = _validar_estados(lineas[0])
    alfabeto_entrada = _validar_alfabeto_entrada(lineas[1])
    alfabeto_pila = _validar_alfabeto_pila(lineas[2])
    estado_inicial = _validar_estado_inicial(lineas[3], estados)
    estados_finales = _validar_estados_finales(lineas[4], estados)
    fondo_pila = _validar_fondo_pila(lineas[5], alfabeto_pila)
    transiciones = _validar_transiciones(
        lineas[6], estados, alfabeto_entrada, alfabeto_pila
    )
    palabra = _validar_palabra(lineas[7], alfabeto_entrada)

    return Automata(
        estados,
        alfabeto_entrada,
        alfabeto_pila,
        estado_inicial,
        estados_finales,
        fondo_pila,
        transiciones,
        palabra,
    )


def _formatear_configuracion(
    palabra: str, posicion: int, estado: str, pila: tuple[str, ...]
) -> str:
    palabra_con_punto = f"{palabra[:posicion]}.{palabra[posicion:]}"
    return f"{palabra_con_punto} {estado} {''.join(pila)}"


def simular(automata: Automata) -> list[str]:
    """Devuelve la traza completa y la decisión final del APD."""
    estado = automata.estado_inicial
    posicion = 0
    pila = (automata.fondo_pila,)

    configuracion = (posicion, estado, pila)
    visitadas = {configuracion}
    modos_activos = {(posicion, estado, pila[0]): len(pila)}
    salida = [_formatear_configuracion(automata.palabra, posicion, estado, pila)]
    ciclo = False

    while pila:
        tope = pila[0]
        transicion = None
        if posicion < len(automata.palabra):
            transicion = automata.transiciones.get(
                (estado, automata.palabra[posicion], tope)
            )
        if transicion is None:
            transicion = automata.transiciones.get((estado, "#", tope))
        if transicion is None:
            break

        pila = tuple(transicion.palabra_pila) + pila[1:]
        estado = transicion.estado_destino
        if transicion.simbolo_entrada != "#":
            posicion += 1

        salida.append(_formatear_configuracion(automata.palabra, posicion, estado, pila))
        configuracion = (posicion, estado, pila)
        if configuracion in visitadas:
            ciclo = True
            break
        visitadas.add(configuracion)

        if pila:
            altura = len(pila)
            modos_activos = {
                modo: altura_inicial
                for modo, altura_inicial in modos_activos.items()
                if altura_inicial <= altura
            }
            modo = (posicion, estado, pila[0])
            if modo in modos_activos:
                ciclo = True
                break
            modos_activos[modo] = altura

    aceptado = (
        not ciclo
        and posicion == len(automata.palabra)
        and estado in automata.estados_finales
        and pila == (automata.fondo_pila,)
    )
    salida.append("Aceptado" if aceptado else "Rechazado")
    return salida


def procesar_bloque(lineas: Sequence[str]) -> list[str]:
    try:
        return simular(analizar_automata(lineas))
    except ErrorValidacion as error:
        return [str(error)]


def _iterar_resultados(lineas: Iterable[str]) -> Iterator[list[str]]:
    """Entrega cada resultado apenas se completa su bloque de entrada."""
    bloque: list[str] = []
    for linea_cruda in lineas:
        linea = linea_cruda.rstrip("\r\n")
        if linea.strip() == "_FIN":
            if bloque:
                yield procesar_bloque(bloque)
            return
        bloque.append(linea)
        if len(bloque) == 8:
            yield procesar_bloque(bloque)
            bloque.clear()

    if bloque:
        yield procesar_bloque(bloque)


def procesar_entrada(lineas: Iterable[str]) -> list[str]:
    """Procesa bloques de ocho líneas hasta encontrar ``_FIN``."""
    salida: list[str] = []
    for resultado in _iterar_resultados(lineas):
        salida.extend(resultado)
    return salida


def ejecutar(entrada: TextIO, salida: TextIO) -> None:
    for lineas_salida in _iterar_resultados(entrada):
        salida.write("\n".join(lineas_salida) + "\n")
        salida.flush()
