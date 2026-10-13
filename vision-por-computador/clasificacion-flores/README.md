# Clasificación de Flores

## Descripción del proyecto

Este proyecto corresponde al **Avance 2** de la asignatura **Taller de Introducción a Visión por Computadora**.

El objetivo del proyecto es preparar y analizar un dataset de imágenes de flores para una futura tarea de clasificación automática mediante modelos de visión por computador.

En esta etapa todavía **no se entrena el modelo**. El avance se enfoca en la adquisición, organización, revisión y análisis inicial del dataset utilizando **Roboflow** y Python.

---

## Integrantes

- Luciano Villanueva Ramírez
- Mauricio Pérez
- Francisco Flores Cares

---

## Objetivo del avance

El objetivo de este avance es evidenciar la preparación inicial del dataset de imágenes, considerando:

- Selección y organización del dataset.
- Configuración del proyecto en Roboflow.
- Carga de imágenes en la plataforma.
- Definición de clases.
- Uso de etiquetas/tags para apoyar la revisión.
- Análisis inicial del dataset mediante Roboflow Analytics.
- Generación de resultados exploratorios con Python.

---

## Dataset utilizado

El dataset fue gestionado mediante **Roboflow**, plataforma utilizada para organizar datasets en proyectos de visión por computador.

El proyecto corresponde a una tarea de **clasificación de imágenes**, donde cada imagen pertenece a una clase principal de flor.

### Clases del dataset

El dataset actual contiene cinco clases:

| Clase en carpeta | Nombre formal |
|---|---|
| `dienteleon` | Diente de león |
| `girasol` | Girasol |
| `margarita` | Margarita |
| `rosa` | Rosa |
| `tulipan` | Tulipán |

---

## Distribución del dataset

El dataset contiene un total de **255 imágenes**, distribuidas en conjuntos de entrenamiento, validación y prueba.

### Distribución por división

| División | Cantidad de imágenes |
|---|---:|
| Train | 178 |
| Valid | 53 |
| Test | 24 |
| **Total** | **255** |

### Distribución por clase

| Clase | Cantidad de imágenes |
|---|---:|
| Diente de león | 50 |
| Girasol | 38 |
| Margarita | 50 |
| Rosa | 31 |
| Tulipán | 86 |
| **Total** | **255** |

---

## Análisis cuantitativo y cualitativo

A nivel cuantitativo, el dataset cuenta con **255 imágenes** organizadas en cinco clases. La clase con mayor cantidad de imágenes es **tulipán**, con 86 imágenes, mientras que la clase con menor cantidad es **rosa**, con 31 imágenes.

Esto indica que el dataset no se encuentra completamente balanceado. Sin embargo, para esta etapa inicial es suficiente para realizar la preparación del flujo de trabajo y el análisis preliminar. En etapas posteriores se recomienda aumentar la cantidad de imágenes de las clases con menor representación, especialmente **rosa** y **girasol**.

A nivel cualitativo, las imágenes presentan variabilidad visual en fondos, iluminación, distancia y composición. Algunas flores aparecen en primer plano, mientras que otras se encuentran en jardines, campos o fondos naturales. Esta variabilidad es positiva porque permite preparar un dataset más diverso para el futuro entrenamiento del modelo.

---

## Configuración en Roboflow

Se creó un proyecto en **Roboflow** configurado para una tarea de **Image Classification**. Esta configuración es adecuada para el tema del proyecto, ya que el objetivo es clasificar una imagen completa según el tipo de flor correspondiente.

En Roboflow se realizó:

- Creación del workspace/proyecto.
- Carga de imágenes.
- Definición de clases.
- Organización del dataset.
- Revisión de imágenes.
- Uso de tags para apoyar el proceso de revisión.
- Análisis preliminar mediante la sección Analytics.
- Creación de una versión del dataset para exportación.

---

## Etiquetado y tags

Las imágenes fueron organizadas según su clase principal:

- `dienteleon`
- `girasol`
- `margarita`
- `rosa`
- `tulipan`

Además, se utilizaron tags como apoyo para la revisión del dataset. Los tags permiten marcar características adicionales de las imágenes sin reemplazar la clase principal.

### Tags utilizados

| Tag | Uso |
|---|---|
| `revisado` | Imagen revisada y considerada correcta |
| `primer_plano` | Flor visible de cerca |
| `campo` | Imagen tomada en jardín, campo o entorno natural |
| `varias_flores` | Imagen con más de una flor visible |
| `borrosa` | Imagen con baja calidad o dudosa |

Estos tags ayudan a organizar el dataset y detectar imágenes que podrían necesitar revisión antes del entrenamiento final.

---

## Analytics de Roboflow

En la sección **Analytics** de Roboflow se revisaron estadísticas preliminares del dataset, incluyendo el total de imágenes, tamaño y proporciones.

El análisis permitió observar:

- Total de imágenes cargadas.
- Tamaño general de las imágenes.
- Variabilidad en proporciones visuales.
- Distribución del dataset.
- Existencia de imágenes anchas, muy anchas, altas y cuadradas.

Esta información es útil para evaluar la calidad inicial del dataset antes de entrenar un modelo de clasificación.

---

## Preprocesamiento

En Roboflow se generó una versión del dataset aplicando preprocesamiento para preparar las imágenes para etapas posteriores.

El preprocesamiento utilizado fue:

- **Auto-Orient:** corrección automática de orientación.
- **Resize:** redimensionamiento de imágenes a **224x224 píxeles**.

El tamaño **224x224** es adecuado para modelos CNN como **ResNet50**, que será considerado en la etapa de entrenamiento.

---

## Tecnologías utilizadas

- Python
- Pandas
- Matplotlib
- Pillow
- Roboflow
- Git
- GitHub

  
git clone https://github.com/lucianoVillanuevaR/Clasificacion-Flores.git

cd Clasificacion-Flores

python3 -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python3 main.py
