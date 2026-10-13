# Proyectos universitarios | Universidad del Bío-Bío

Repositorio académico de **Ingeniería de Ejecución en Computación e Informática** de la **Universidad del Bío-Bío (UBB)**.

Aquí se reúnen trabajos, laboratorios, ejercicios y material de asignaturas en un solo lugar, organizados por área y proyecto. Cada carpeta conserva su código y, cuando está disponible, su documentación específica.

**9 proyectos · 6 áreas académicas · JavaScript, Python, Java, SQL y tecnologías web**

## Índice de proyectos

### Inteligencia Artificial

| Proyecto | Descripción | Tecnologías |
| --- | --- | --- |
| [Juego Rullo](inteligencia-artificial/juego-rullo/) | Juego web de tableros con un solucionador basado principalmente en búsqueda voraz (*greedy*). | HTML, CSS, JavaScript |
| [N-Puzzle](inteligencia-artificial/n-puzzle/) | Resolución de rompecabezas deslizables mediante BFS, IDDFS y búsqueda bidireccional. | JavaScript, Node.js |
| [Laboratorio 06 — Búsqueda de caminos](inteligencia-artificial/laboratorio-06/) | Comparación de búsqueda voraz y A* sobre una grilla con obstáculos y heurística de distancia euclidiana. | JavaScript, Node.js |
| [Redes neuronales — MNIST](inteligencia-artificial/redes-neuronales/) | Clasificación de dígitos manuscritos con perceptrones multicapa (MLP), comparación de arquitecturas y evaluación de modelos. | Python, scikit-learn |

### Bases de Datos

| Proyecto | Descripción | Tecnologías |
| --- | --- | --- |
| [Gestión de alumnos](bases-de-datos/proyecto-alumnos/) | Aplicación de consola para ingresar y modificar alumnos, además de ejecutar consultas sobre una base de datos relacional. | JavaScript, Node.js, PostgreSQL, SQL |

### Ingeniería de Software

| Proyecto | Descripción | Tecnologías |
| --- | --- | --- |
| [Tarea 01 — API REST](ingenieria-de-software/tarea-01/) | Material educativo de una API para autenticación y gestión de usuarios, con JWT y arquitectura MVC. | Node.js, Express, PostgreSQL, TypeORM |

### Metodología del Desarrollo

| Proyecto | Descripción | Tecnologías |
| --- | --- | --- |
| [Tarea 01](metodologia-del-desarrollo/tarea-01/) | Ejercicios y desafíos de programación correspondientes a la asignatura. | JavaScript |

### Proyectos Java

| Proyecto | Descripción | Tecnologías |
| --- | --- | --- |
| [Sistema de gestión de talleres](proyectos-java/sistema-talleres/) | Aplicación de escritorio para administrar talleres, inscripciones, listas de espera, asistencia y reportes. | Java 17, Swing, MVC, Apache Ant |

### Visión por Computador

| Proyecto | Descripción | Tecnologías |
| --- | --- | --- |
| [Clasificación de flores](vision-por-computador/clasificacion-flores/) | Preparación, organización y análisis exploratorio de un dataset de 255 imágenes en cinco clases. Incluye revisión y preprocesamiento para una futura clasificación; este avance no incluye entrenamiento del modelo. | Python, Pandas, Matplotlib, Pillow, Roboflow |

## Estructura del repositorio

~~~text
universidad-ubb/
├── bases-de-datos/
│   └── proyecto-alumnos/
├── ingenieria-de-software/
│   └── tarea-01/
├── inteligencia-artificial/
│   ├── juego-rullo/
│   ├── laboratorio-06/
│   ├── n-puzzle/
│   └── redes-neuronales/
├── metodologia-del-desarrollo/
│   └── tarea-01/
├── proyectos-java/
│   └── sistema-talleres/
├── vision-por-computador/
│   └── clasificacion-flores/
└── README.md
~~~

## Cómo explorar o ejecutar los proyectos

Clona el repositorio:

~~~bash
git clone https://github.com/lucianoVillanuevaR/universidad-ubb.git
cd universidad-ubb
~~~

Entra a la carpeta del proyecto que te interese y consulta su `README.md`. Los proyectos son **independientes**: no existe un comando único para instalar o ejecutar todo el repositorio. Algunos requieren Node.js o Python, otros Java y otros una base de datos PostgreSQL. Determinados datasets o archivos de configuración deben prepararse por separado.

## Autoría y uso académico

Este repositorio centraliza material académico, pero **no implica autoría individual sobre todos los archivos**. Hay trabajos en colaboración y material de apoyo de clases.

- **Gestión de alumnos:** el README original identifica a Luciano Villanueva R. y Francisco Flores.
- **Clasificación de flores:** el README original identifica como integrantes a Luciano Villanueva Ramírez, Mauricio Pérez y Francisco Flores Cares.
- **API REST de Ingeniería de Software:** el README original identifica como autores a **Marco Cerda y Sebastián Espinoza** y describe el proyecto como material educativo; conserva además su archivo de licencia en la carpeta correspondiente.
- En los demás proyectos, revisa los README individuales para conocer su contexto, integrantes y condiciones de uso.

La presencia de código aquí no sustituye las atribuciones ni las licencias de cada subproyecto.

## Otros desarrollos

Algunos trabajos más amplios se mantienen en repositorios independientes para conservar sus procesos de desarrollo y despliegue:

- [Sistema de gestión de pedidos accesible — Riquísimo](https://github.com/lucianoVillanuevaR/gestion-pedidos-accesible): proyecto de título con frontend, backend y enfoque de accesibilidad.
- [Landing page de Tuperno](https://github.com/lucianoVillanuevaR/tuperno-landing-page): trabajo realizado durante la práctica profesional.

---

**Universidad del Bío-Bío · Ingeniería de Ejecución en Computación e Informática**
