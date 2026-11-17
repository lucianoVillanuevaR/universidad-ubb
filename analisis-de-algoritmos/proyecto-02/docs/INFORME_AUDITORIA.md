# Informe de auditoría — Proyecto 2 AATA

## Corrección final — 17 de noviembre de 2026 (estado vigente)

Se revisaron directamente el texto y las imágenes de las dos páginas de
`/home/luciano/Escritorio/PROYECTO 2.pdf`.

**Cambio funcional único:** en `dpda.py`, `CARACTERES_PROHIBIDOS` queda como
`frozenset({"#", "”", "‘", ",", "."})`. Se retiran U+0022 y U+0027.
La página 1 permite todo carácter fuera de la lista explícita. Se adopta
esa lectura literal, reconociendo la posible ambigüedad tipográfica.
No se modificaron la simulación, el alfabeto de entrada ni `main.py`.

Se actualizó el test de caracteres prohibidos sin eliminar métodos y se
agregaron tres pruebas: comillas ASCII en nombres y fondo de pila; traza
completa por CLI con ambas comillas, apilado y desapilado; rechazo de comillas
y otros símbolos especiales al inicio de estados y en el alfabeto de entrada.
Las pruebas existentes mantienen la cobertura de `_`, `+`, `-`, `(`, `)` y `=`.

### Revisión de las ocho líneas

| Línea | Regla comprobada y resultado |
|---|---|
| 1 | Estados separados por espacios, inicio alfanumérico y solo los cinco caracteres prohibidos. Corregida la restricción ASCII adicional. |
| 2 | Símbolos alfanuméricos individuales separados por espacios. Sin cambios. |
| 3 | Símbolos individuales de pila separados por espacios y lista literal de prohibidos. Corregida la restricción ASCII adicional. |
| 4 | Un único estado inicial perteneciente a la línea 1. Sin cambios. |
| 5 | Estados finales declarados, separados por espacios. Sin cambios. |
| 6 | Un símbolo de fondo perteneciente al alfabeto de pila. Sin cambios. |
| 7 | Sintaxis, pertenencia de estados/símbolos y palabra de reemplazo; `#` como palabra vacía; no determinismo produce error 7. Sin cambios. |
| 8 | Palabra sobre el alfabeto de entrada; `#` para palabra vacía. Sin cambios. |

No se identificó otra discrepancia verificable con las reglas explícitas.
El PDF no define la representación de conjuntos vacíos: se preservó su
tratamiento, sin inventar formatos. También quedan sin especificar en el PDF
la traza finita de ciclos infinitos y la prioridad en bloques truncados;
estas decisiones existentes no se presentan como exigencias del enunciado.

### Verificación ejecutada

- `python3 -m unittest discover -v`: **66/66 pruebas aprobadas**, 6,567 s,
  sin fallos, errores ni omisiones. Incluyen los **24.000 casos masivos**
  y **200 bloques por CLI**; no son métodos adicionales.
- Luego se ejecutó cada ejemplo oficial mediante `python3 main.py`,
  alimentado por stdin y terminado con `_FIN`. Comparación de bytes sin
  recortar ni normalizar: **109, 91, 22 y 22 bytes**, todos exactos,
  incluidos espacios y saltos finales. Retorno 0 y stderr vacío.
- También se ejecutaron juntos los cuatro ejemplos en una carpeta temporal
  que contenía únicamente `main.py` y `dpda.py`, mediante
  `python3 -S main.py`: salida exacta. Ambos archivos bastan para ejecutar
  el programa; no se requieren tests, documentación ni paquetes externos.
- Se preservan bloques de ocho líneas, múltiples autómatas, terminación
  `_FIN`, posición con punto, tope primero y mensajes exactos.

**Resultado:** corrección literal aplicada, sin regresiones observadas ni
otro incumplimiento verificable encontrado en el alcance revisado.

## Historial anterior (no describe el estado vigente)

Las secciones siguientes se conservan como registro de auditorías previas.
Sus referencias a siete caracteres prohibidos, 63 pruebas y parche no aplicado
quedan sustituidas por la corrección y los resultados anteriores.

## Revisión directa del PDF — 10 de noviembre de 2026

Se revisaron el texto y las imágenes de las dos páginas del PDF original.
No se modificaron el algoritmo, `CARACTERES_PROHIBIDOS` ni las pruebas.
No se identificó un incumplimiento inequívoco en el alcance solicitado;
permanece la ambigüedad de comillas detallada en C.1 y en README:
la lectura literal permite ASCII U+0022/U+0027, mientras que la interpretación
de sustitución tipográfica justifica su prohibición actual.

Corrección documental: la tabla sí muestra visualmente `0 1` y `A L`.
La representación compacta proviene de la extracción de texto, no de una
contradicción del enunciado. Los saltos visuales de las transiciones se
reunieron en la línea 7, respetando los ocho renglones de entrada.

Se ejecutaron los cuatro ejemplos individualmente mediante `python3 main.py`
y se comparó stdout byte por byte con las trazas completas de la página 2:
109, 91, 22 y 22 bytes, respectivamente, incluido el salto de línea final.
Los resultados fueron `Aceptado`, `Rechazado`, `Error encontrado en 7`
y `Error encontrado en 6`, sin diferencias de espacios, punto ni orden de pila.

`python3 -m unittest discover -v`: **63 pruebas aprobadas**, en 5,766 s.
Este total incluye cuatro métodos que recorren **24.000 casos** y otro que
verifica 200 bloques por CLI; los casos no son 24.000 métodos adicionales.
También se comprobaron 37 caracteres especiales permitidos en nombres,
pila y transiciones completas, los siete caracteres actualmente prohibidos
en ambas declaraciones, inicios alfanuméricos ASCII/Unicode e inicios
especiales inválidos. Todas estas comprobaciones aprobaron.

Estado: listo funcionalmente para entregar en el alcance revisado, con la
salvedad tipográfica indicada; no se certifica equivalencia estricta por
puntos de código mientras se prohíban las dos comillas ASCII adicionales.
Solo se actualizó documentación para registrar la revisión y corregir la
afirmación anterior sobre los espacios de la tabla.

## Auditoría anterior

Fecha: 4 de noviembre de 2026. Fuente: `/home/luciano/Escritorio/PROYECTO 2.pdf`,
páginas 1 y 2. Entorno ejecutado: Linux, Python 3.13.5, biblioteca estándar.

**Veredicto: SÍ CON OBSERVACIONES.** No se encontraron discrepancias funcionales
reproducibles bajo las interpretaciones documentadas. No se puede certificar
cumplimiento literal del 100 %: las comillas, los conjuntos vacíos y otros casos
no están definidos inequívocamente. Las pruebas masivas son evidencia finita,
no una demostración para todas las entradas posibles.

En esta auditoría se añadieron únicamente `tests/test_auditoria.py` y este
informe. Los cambios anteriores en README, dpda y test_dpda ya existían al iniciar
esta revisión. No se modificó el algoritmo principal ni se añadieron dependencias.

## A. Matriz de cumplimiento

«CUMPLE» indica respaldo por inspección y pruebas ejecutadas; «AMBIGUO» indica
que la decisión depende de una interpretación o de información externa.
Los nombres de pruebas pertenecen a `tests/test_dpda.py`, salvo los de
`AuditoriaMasiva` e `IntegracionAuditada`, en `tests/test_auditoria.py`.

| Requisito / origen | Estado | Evidencia |
|---|---|---|
| Lenguaje permitido: Python (p. 1) | CUMPLE | `main.py`, ejecución real con Python 3.13.5 |
| Entrada por teclado/entrada estándar (p. 1) | CUMPLE | `main.main` conecta `sys.stdin`; pruebas CLI con stdin por tubería |
| Ocho líneas por autómata (p. 1) | CUMPLE | `_iterar_resultados`; `EntradaCompleta`, 200 bloques de integración |
| Autómatas consecutivos hasta `_FIN` (p. 1) | CUMPLE | `test_multiples_automatas_y_fin`, CLI ignora texto posterior a `_FIN` |
| Línea 1: estados separados, primer carácter alfanumérico (p. 1) | CUMPLE | `_validar_estados`; validación dirigida y 1.000 casos inválidos de línea 1 |
| Línea 2: símbolos individuales alfanuméricos separados (p. 1) | CUMPLE | `_validar_alfabeto_entrada`; 1.000 casos inválidos y simulaciones generadas |
| Línea 3: símbolos individuales de pila separados (p. 1) | CUMPLE | `_validar_alfabeto_pila`; 1.000 casos inválidos |
| Prohibición de `#`, coma, punto, U+201D y U+2018 en estados/pila (p. 1) | CUMPLE | `test_todos_los_caracteres_prohibidos` y pruebas de comillas |
| Permitir todos los otros caracteres (p. 1), incluidas comillas ASCII | AMBIGUO | ASCII también está prohibido; reproducción y propuesta en C |
| Permitir `_`, `+`, `-`, `(`, `)`, `=` tras el inicio del estado/en pila (p. 1) | CUMPLE | `test_simbolos_especiales_en_estados_y_transiciones` |
| Línea 4: un único estado inicial declarado (p. 1) | CUMPLE | `_validar_estado_inicial`; 1.000 mutaciones de línea 4 |
| Línea 5: estados finales declarados (p. 1) | CUMPLE | `_validar_estados_finales`; 1.000 mutaciones de línea 5 |
| Declaraciones de conjuntos vacíos | AMBIGUO | El PDF no especifica representación; el programa las rechaza |
| Línea 6: fondo de pila declarado (p. 1) | CUMPLE | Ejemplo oficial 4, 1.000 mutaciones de línea 6 |
| Línea 7: sintaxis exacta y referencias válidas (p. 1) | CUMPLE | `_analizar_transicion`; pruebas de delimitadores, estados y símbolos |
| Error 7 ante no determinismo (p. 1) | CUMPLE | Ejemplo 3; duplicados conflictivos; conflicto epsilon/consumo en ambos órdenes |
| Duplicados idénticos de transición | AMBIGUO | Se interpretan como un solo elemento de la relación; PDF no los prohíbe |
| Línea 8: palabra sobre alfabeto de entrada (p. 1) | CUMPLE | `_validar_palabra`; 1.000 mutaciones de línea 8 |
| `#` como palabra vacía (p. 1) | CUMPLE | `test_palabra_vacia_aceptada`, inserción vacía, simulaciones con epsilon |
| Estado inicial y pila inicial con fondo (definición del autómata/p. 1) | CUMPLE | Trazas oficiales y oráculo independiente |
| Transiciones con consumo y actualización de estado (semántica APD) | CUMPLE | 8.000 casos sin epsilon y 4.000 con epsilon finito |
| Transiciones vacías y reemplazo de pila (semántica APD y `#`) | CUMPLE | 4.000 casos finitos; cadenas epsilon antes/después del consumo |
| Tope a la izquierda y orden de apilado (p. 1) | CUMPLE | Ejemplo 1; oráculo con pila invertida; inserciones múltiples |
| Aceptar al finalizar solo con palabra consumida, estado final y solo fondo (p. 1) | CUMPLE | `test_tres_condiciones_de_aceptacion_independientes`; pila vacía y adicional |
| Continuar epsilon aunque se satisfagan temporalmente las condiciones | CUMPLE | Lectura de «cómputo finalizó»; `test_no_acepta_antes_de_finalizar_el_computo` |
| Traza `palabra_con_punto estado pila` (p. 1) | CUMPLE | Comparaciones completas de cadenas, incluidos espacios y salto final |
| Mensajes `Aceptado`, `Rechazado`, `Error encontrado en N` (p. 1) | CUMPLE | Cuatro ejemplos y validaciones de las ocho líneas |
| Cuatro resultados oficiales (p. 2) | CUMPLE | `EjemplosDelPdf`, `test_cuatro_ejemplos_en_cli`, sin normalizar salidas |
| Alfabetos separados por espacios en tabla y texto | CUMPLE | Revisión visual del 10 de noviembre: `0 1` y `A L`; la extracción de texto pierde espacios |
| Bloques incompletos / primer error cuando falta información | AMBIGUO | PDF no especifica; se reporta siguiente línea faltante, incluso con error previo |
| Ciclos infinitos: detección y salida exigida por el usuario | CUMPLE | 4.000 ciclos demostrables; terminación controlada y prefijo de traza válido |
| Formato/extensión de traza de un ciclo infinito según PDF | AMBIGUO | PDF no define una salida finita para estos casos |
| No rechazar falsamente por aparente repetición | CUMPLE | 4.000 casos epsilon finitos, reconstrucción de pila y 1.000 desapilados dirigidos |
| Sin menús, bibliotecas externas ni excepciones inesperadas | CUMPLE | CLI normal y `python3 -S main.py`, stderr vacío y retorno 0 |
| Grupo de 1–5 participantes, fecha/hora y entrega (p. 1–2) | AMBIGUO | No verificable mediante el código; el PDF indica viernes 20 de noviembre, 9:40 |

## B. Resultados de pruebas ejecutadas

| Medición | Resultado |
|---|---:|
| Métodos de prueba descubiertos por unittest | 63 |
| Métodos aprobados | 63 |
| Métodos fallidos / errores / omitidos | 0 / 0 / 0 |
| Casos aleatorios de la batería masiva | 24.000 |
| Casos masivos aprobados / fallidos / no concluyentes | 24.000 / 0 / 0 |
| Bloques aleatorios adicionales por CLI sin site-packages | 200 |
| Bloques CLI adicionales aprobados | 200 |
| Duración informada por unittest | 4,762 s |
| Duración externa del proceso completo | 4,885202 s |
| Código de salida de la suite | 0 |

Los 24.000 casos son iteraciones reproducibles con `subTest`, agrupadas en cuatro
métodos; los 200 bloques se agrupan en otro método. Los 58 métodos anteriores
están incluidos en los 63. No deben sumarse métodos, bloques y subcasos como si
fueran la misma unidad. No se exige que todos los modelos generados sean únicos;
se muestrean con reemplazo. Las comprobaciones exploratorias de ambigüedades no
se cuentan como pruebas aprobadas de conformidad literal.

### Diseño del oráculo y cobertura masiva

| Familia | Casos | Semilla | Criterio independiente |
|---|---:|---:|---|
| Transiciones con consumo | 8.000 | 20261104 | Máximo `longitud(palabra)` transiciones; traza y resultado completos |
| Epsilon finito | 4.000 | 20261105 | Cada epsilon aumenta índice de estado; cota `Q × (longitud + 1) + 1`; comparación completa |
| Ciclos demostrables | 4.000 | 20261106 | Anillo sin consumo, sin desapilado, final inaccesible; rechazo y prefijo exacto |
| Entradas inválidas | 8.000 | 20261107 | Una línea mutada por caso, 1.000 por cada línea; diagnóstico exacto |
| Integración de bloques válidos | 200 | 20261108 | Mismo oráculo independiente, comparación de stdout completo |

Los modelos finitos tienen 2, 3, 6, 12 o 24 estados, tres símbolos de pila,
dos símbolos de entrada y palabras de 0 a 35 caracteres. Las reglas incluyen
eliminación, conservación e inserción múltiple, destinos finales/no finales y
transiciones ausentes. Los ciclos usan anillos de 1–25 estados y crecimiento de
0–5 símbolos por paso. La suite dirigida añade palabras de 1.000 símbolos,
1.001 estados, 1.000 desapilados epsilon y reconstrucciones que vuelven al mismo
estado/tope después de exponer otra parte de la pila.

`referencia` recibe las reglas generadas antes de serializarlas. No utiliza
`analizar_automata`, `Automata`, el diccionario de transiciones, el formateador ni
el detector de ciclos del producto. Busca reglas linealmente y mantiene una pila
mutable con tope a la derecha. Las respuestas inválidas proceden de mutaciones
con error conocido, no del validador real.

Para ciclos, no se afirma que exista una longitud de traza oficial: se verifica
que la salida termina en rechazo y que todas las configuraciones impresas forman
un prefijo correcto de la ejecución independiente. Nunca se considera que agotar
un límite de simulación demuestre rechazo. Si el oráculo finito agota su cota,
lanza un fallo; no hubo casos de ese tipo.

Cada familia masiva tiene un plazo de 45 segundos mediante SIGALRM en Linux;
la integración tiene timeout de 15 segundos y la ejecución externa de la suite
usó timeout de 180 segundos. En sistemas sin SIGALRM debe conservarse el timeout
externo. Los límites son del arnés de pruebas, no del algoritmo auditado.

### Comandos

Desde `/home/luciano/Escritorio/Proyecto2AATA`:

```bash
python3 -m unittest discover -v
python3 main.py
```

El primer comando se ejecutó mediante `subprocess.run` con captura de stdout,
stderr, medición `time.perf_counter()` y timeout de 180 segundos. El segundo se
alimentó por stdin con el ejemplo 1 más `_FIN` y produjo la salida exacta inferior.
Las pruebas también ejecutaron `main.py` mediante subprocess con y sin `-S`.
`git diff --check` terminó sin errores.

Para repetir únicamente la batería añadida:

```bash
python3 -m unittest tests.test_auditoria -v
```

### Ejemplos oficiales

Las cuatro entradas están en `EjemplosDelPdf` y en la prueba CLI conjunta.
Se reponen espacios en `0 1` y `A L` y se juntan las transiciones visualmente
partidas en una sola línea 7, conforme a las instrucciones de la página 1.
No se altera, recorta ni normaliza la salida esperada. La salida conjunta
comparada, carácter por carácter y con un salto de línea final, es:

```text
.000111 q1 L
0.00111 q1 AL
00.0111 q1 AAL
000.111 q1 AAAL
0001.11 q2 AAL
00011.1 q2 AL
000111. q2 L
Aceptado
.00011 q1 L
0.0011 q1 AL
00.011 q1 AAL
000.11 q1 AAAL
0001.1 q2 AAL
00011. q2 AL
Rechazado
Error encontrado en 7
Error encontrado en 6
```

## C. Errores encontrados y evidencia

**No se encontraron fallos inequívocos en los requisitos funcionales no ambiguos.**
No se propone ni aplica un parche al simulador. Existe, sin embargo, una
restricción adicional verificable frente a la lectura estricta por puntos de
código de la lista de caracteres; no debe ocultarse tras el resultado de la suite.

### C.1. Comillas ASCII: discrepancia bajo lectura Unicode literal

1. **Problema:** `CARACTERES_PROHIBIDOS` agrega U+0022 y U+0027 a los caracteres
   tipográficos que se ven en el PDF. Las pruebas existentes comprueban esa
   política actual; su aprobación no resuelve qué quiso exigir el profesor.
2. **Requisito relevante:** página 1, todo carácter fuera de la lista será
   permitido. Si se interpreta la lista literalmente como puntos de código,
   prohibir las comillas ASCII incumple esa cláusula. Si las comillas del PDF
   son sustituciones tipográficas de comillas ASCII, la restricción es razonable.
3. **Entrada exacta reproducida** (la tercera y sexta líneas contienen U+0022):

```text
q
a
"
q
q
"
(q,a,"=q,")
a
```

4. **Salida esperada bajo lectura Unicode literal:**

```text
.a q "
a. q "
Aceptado
```

5. **Salida obtenida:**

```text
Error encontrado en 3
```

6. **Responsable:** `dpda.py`, constante `CARACTERES_PROHIBIDOS`, utilizada por
   `_contiene_caracter_prohibido` y `_validar_alfabeto_pila` (también afecta estados).
7. **Parche mínimo si se exige lectura Unicode literal:** retirar únicamente
   `"'"` y `'"'` de la constante y ajustar las pruebas y documentación de esa
   política. Impacto: permite esos caracteres en estados y pila; no cambia
   determinismo, simulación ni salidas oficiales. **No aplicado**, porque el
   PDF tipografiado permite ambas interpretaciones y no hay un defecto
   inequívoco que justifique cambiar preventivamente la política.

También se reprodujo rechazo para U+0027 y aceptación para U+201C y U+2019.
Estos últimos no están en la lista literal implementada. Es la observación
más importante para cualquier afirmación de cumplimiento estricto.

## D. Ambigüedades y límites

- **Alfabetos de la tabla:** la lectura literal de la instrucción exige `0 1`
  y `A L`. No se amplió el analizador para aceptar `01` o `AL`; hacerlo también
  permitiría tokens multicaracter que contradicen la primera página. El PDF
  advierte que no se copie y pegue su tabla por variaciones de formato.
- **Comillas:** detalle y efecto concreto en C.1. La equivalencia ASCII no debe
  presentarse como un requisito textual inequívoco.
- **Conjuntos vacíos:** el programa rechaza alfabetos, finales y transiciones
  vacíos. En teoría un conjunto final o de transiciones puede estar vacío;
  el PDF no define cómo representarlo ni exige expresamente no vaciedad.
  Si el evaluador usa una línea vacía para esos conjuntos, habrá discrepancias.
- **Errores múltiples y truncamiento:** en ocho líneas se reporta el primer
  error; con menos de ocho se reporta la siguiente línea faltante, aun cuando
  una línea presente ya sea inválida. No hay prioridad oficial especificada.
- **Fin de archivo y espacios:** EOF después de un bloque completo finaliza
  normalmente. Se toleran espacios externos, tabuladores como separadores y
  `_FIN` con espacios externos. Las líneas vacías no se omiten. El PDF no
  especifica esas variantes; la palabra vacía requiere `#`, no una línea vacía.
- **Duplicados idénticos:** se colapsan como elementos de un conjunto; los
  duplicados con distinto destino o reemplazo son error 7. No hay una regla
  textual de rechazo por repetición idéntica.
- **Alfanumérico Unicode:** `isalnum()` admite letras/números fuera de ASCII.
  El PDF no establece una restricción ASCII ni normalización Unicode.
- **Finalización y epsilon:** se interpreta literalmente «cómputo finalizó»:
  se siguen ejecutando epsilon aplicables antes de evaluar aceptación. Una
  definición alternativa de aceptación por alcanzar una configuración final
  cambiaría ciertos casos, pero no es la adoptada por el texto del proyecto.
- **Pila vacía y ciclos:** la pila vacía se imprime como campo vacío, dejando
  un espacio al final de la configuración. Los ciclos se cortan con rechazo.
  El PDF no muestra ejemplos ni una longitud oficial de traza para esos casos.
- **Recursos:** se acumulan trazas y configuraciones completas. Una ejecución
  finita muy larga puede requerir mucha memoria; no se midió un máximo de
  tamaño porque el PDF no fija límites. No hay corte arbitrario de pasos en
  producción. La prueba masiva epsilon cubre una familia finita demostrable,
  no todas las formas posibles de ejecución epsilon.
- **Detección de ciclos, revisión conceptual:** el modo guarda posición,
  estado, tope y altura de origen; se invalida al descender por debajo de esa
  altura. Si se repite sin descenso, la parte inferior nunca fue consultada
  y la misma evolución determinista vuelve a ocurrir sin consumir entrada.
  Repetir solo estado y tope sin esa condición sería incorrecto; el código
  sí conserva la condición. Las pruebas de reconstrucción y desapilado
  verifican casos donde una repetición aparente debe continuar.
- **Aspectos administrativos:** integrantes y entrega efectiva no se verifican
  mediante tests. La certificación se limita al programa y los archivos leídos.

## E. Veredicto final

**¿Está el proyecto listo para entregar según el PDF? SÍ CON OBSERVACIONES.**

La implementación reproduce los cuatro resultados oficiales, supera 24.000
casos masivos verificados, 200 bloques adicionales por CLI y todas las pruebas
dirigidas. No se detectó un fallo funcional inequívoco que requiera cambiar el
algoritmo. Se preservó el formato exacto y no se instalaron dependencias.

La observación sobre comillas ASCII y la representación de conjuntos vacíos
impide afirmar cumplimiento incondicional del 100 %. El resultado anterior
no convierte esas decisiones en requisitos del profesor ni acredita todos
los autómatas posibles. El proyecto puede entregarse con las interpretaciones
actuales, teniendo presentes las consecuencias concretas documentadas.
