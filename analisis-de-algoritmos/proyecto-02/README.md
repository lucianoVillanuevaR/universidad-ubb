# Proyecto 02 — Simulador de APD

Asignatura: **Análisis de Algoritmos y Teoría de Autómatas (AATA)** — Universidad del Bío-Bío.

Implementación en Python 3 de un simulador de autómatas con pila
deterministas. Lee bloques de ocho líneas desde la entrada estándar, valida el
autómata, imprime la traza de configuraciones y termina cada cómputo con
`Aceptado` o `Rechazado`.

## Ejecución

Requiere Python 3.9 o posterior; utiliza únicamente la biblioteca estándar.
No es necesario instalar paquetes. Ejecutar desde la raíz del proyecto.

```bash
python3 main.py
```

También puede recibir un archivo redirigido:

```bash
python3 main.py < /ruta/al/archivo_de_entrada.txt
```

La entrada termina con una línea `_FIN`. No se imprimen menús ni solicitudes
adicionales.

Ejemplo mínimo con palabra vacía:

```text
q0
a
Z
q0
q0
Z
(q0,a,Z=q0,Z)
#
_FIN
```

Salida:

```text
. q0 Z
Aceptado
```

## Pruebas

Desde el directorio del proyecto:

```bash
python3 -m unittest discover -v
```

Las pruebas cubren los cuatro ejemplos del enunciado, validaciones de las ocho
líneas, determinismo, palabras y transiciones vacías, símbolos especiales,
ciclos repetidos o con crecimiento de pila, bloques incompletos, emisión
inmediata y múltiples autómatas.

## Arquitectura

Para ejecutar y entregar el programa bastan `main.py` y `dpda.py` juntos.
README, informe y tests son documentación y verificación opcionales.

Estructura de los archivos del proyecto (el directorio actual se llama
`proyecto-02`):

```text
Proyecto2/
├── main.py
├── dpda.py
├── README.md
├── docs/
│   └── INFORME_AUDITORIA.md
└── tests/
    ├── __init__.py
    └── test_dpda.py
```

`tests/__init__.py` permite descubrir las pruebas desde la raíz en versiones
de Python que requieren un paquete. Los directorios `__pycache__` son generados
por Python y no forman parte de la entrega.

- `main.py`: punto de entrada y conexión con entrada/salida estándar.
- `dpda.py`: modelos, análisis de las ocho líneas, validación, simulación y
  formato de salida.
- `tests/test_dpda.py`: pruebas automatizadas con `unittest`.

Las transiciones se indexan por `(estado, símbolo de entrada, tope)`. Se rechaza
una misma clave con resultados distintos (estado destino o palabra de pila).
También se comprueba que para un mismo `(estado, tope)` no coexista una
transición vacía con otra que consuma entrada.

La pila se representa con el tope en la primera posición, igual que en la
salida exigida. Una palabra de reemplazo se inserta de izquierda a derecha, por
lo que su primer símbolo pasa a ser el nuevo tope.

## Decisiones sobre ambigüedades del enunciado

- La tabla de ejemplos muestra visualmente `0 1` y `A L`, conforme a la
  instrucción de separar los símbolos por espacios. La extracción de texto
  del PDF puede perder esos espacios. Las transiciones partidas por el ancho
  de la celda se reúnen en una única línea 7, para respetar las ocho líneas.
  Las salidas esperadas se conservan completas, sin modificaciones.
- Se adopta la lectura literal del PDF: solo se prohíben `#`, `”`
  (U+201D), `‘` (U+2018), `,` y `.` en estados y símbolos de pila.
  Las comillas ASCII `"` (U+0022) y `'` (U+0027) están permitidas en
  estados después del primer carácter alfanumérico, y como símbolos de pila.
  Existe una posible ambigüedad tipográfica: las comillas del PDF podrían
  representar comillas ASCII, pero no se amplía la enumeración explícita,
  porque el enunciado permite todo otro carácter. Esta decisión no modifica
  el alfabeto de entrada, que exige símbolos alfanuméricos individuales.
- Se interpreta «alfanumérico» mediante `str.isalnum()`, que incluye letras
  y números Unicode; el enunciado no limita el alfabeto a ASCII.
- Se mantienen como inválidas las declaraciones vacías de estados,
  alfabetos, estados finales y transiciones. El PDF no especifica una
  representación para conjuntos vacíos. La palabra vacía se escribe `#`.
- La aceptación se evalúa al detenerse el cómputo, tal como indica el PDF.
  Si todavía hay una transición vacía aplicable, se ejecuta incluso si ya
  se cumplen las tres condiciones. Un ciclo infinito se informa como
  `Rechazado`; el PDF no fija qué prefijo de su traza debe mostrarse.
- Los espacios separan elementos y transiciones; no forman parte de nombres ni
  símbolos.
- Los alfabetos y conjuntos se almacenan como conjuntos, de modo que repetir
  un elemento en su propia declaración no altera su significado.
- Las transiciones completamente idénticas se consideran un único elemento.
  El PDF no prohíbe explícitamente su repetición; según la semántica de
  conjuntos, esta no introduce no determinismo. La regla se aplica también
  a transiciones vacías.
- En bloques completos se informa el primer error según el orden de las líneas.
  En bloques incompletos se comprueba primero la cantidad de líneas y se
  informa la siguiente línea faltante, sin validar las líneas presentes.
  Por ejemplo, `_q` seguido de `_FIN` produce `Error encontrado en 2`, aunque
  el nombre de estado de la primera línea también sea inválido.
- Se permiten todos los caracteres autorizados por el PDF en estados y
  símbolos de pila, incluidos `(`, `)` y `=`. El analizador no confunde estos
  caracteres con la sintaxis: usa las cuatro partes separadas por comas y el
  hecho de que el tope es exactamente un símbolo.
- Una línea de transiciones vacía sigue produciendo error de línea 7; se
  conserva el tratamiento existente, sin atribuir al PDF un formato para
  conjuntos vacíos que no define.
- `_FIN` sin un bloque pendiente termina normalmente. Si `_FIN` o el fin de
  archivo aparece después de una a siete líneas, se informa el número de la
  siguiente línea faltante. El PDF no define el caso truncado; esta decisión
  evita aceptar o descartar silenciosamente una entrada incompleta.
- La salida de cada autómata se escribe y se vacía al completar sus ocho
  líneas; no se espera a `_FIN` para mostrarla.

## Ciclos

El simulador registra configuraciones completas `(posición, estado, pila)` para
detectar ciclos que vuelven exactamente al mismo punto. También registra modos
`(posición, estado, tope)` junto con la altura desde la que siguen activos. Un
modo deja de estar activo cuando la pila baja de esa altura.

Si reaparece un modo todavía activo, el segmento intermedio no consumió
entrada y nunca accedió a la parte protegida de la pila. Al ser determinista,
ese segmento puede repetirse indefinidamente, incluso si cada repetición agrega
símbolos. Por ello se detiene y se informa `Rechazado`. El criterio se basa en
la estructura del APD y no utiliza un límite arbitrario de pasos.
