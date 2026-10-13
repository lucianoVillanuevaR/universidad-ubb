from pathlib import Path
import random

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# ============================================
# AVANCE 2 - CLASIFICACIÓN DE FLORES
# Exploración inicial del dataset de imágenes
# ============================================

DATASET_DIR = Path("dataset")
RESULTADOS_DIR = Path("resultados")

RESULTADOS_DIR.mkdir(exist_ok=True)

splits = ["train", "valid", "test"]
extensiones = ["*.jpg", "*.jpeg", "*.png", "*.webp"]

registros = []

print("=== AVANCE 2: EXPLORACIÓN DEL DATASET DE IMÁGENES ===\n")

# ============================================
# 1. Validar estructura del dataset
# ============================================

if not DATASET_DIR.exists():
    print("ERROR: No se encontró la carpeta 'dataset'.")
    print("La estructura esperada es:")
    print("dataset/train")
    print("dataset/valid")
    print("dataset/test")
    exit()

# ============================================
# 2. Recorrer train, valid y test
# ============================================

for split in splits:
    split_path = DATASET_DIR / split

    if not split_path.exists():
        print(f"Advertencia: no existe la carpeta {split_path}")
        continue

    for clase_path in sorted(split_path.iterdir()):
        if clase_path.is_dir():
            cantidad = 0

            for extension in extensiones:
                cantidad += len(list(clase_path.glob(extension)))

            registros.append({
                "division": split,
                "clase": clase_path.name,
                "cantidad": cantidad
            })

df = pd.DataFrame(registros)

# ============================================
# 3. Validar que existan imágenes
# ============================================

if df.empty:
    print("No se encontraron imágenes.")
    print("Revisa que tengas carpetas como:")
    print("dataset/train/girasol")
    print("dataset/train/rosa")
    print("dataset/train/tulipan")
    exit()

# ============================================
# 4. Mostrar resumen en consola
# ============================================

print("Resumen por división y clase:")
print(df)

print("\nCantidad total de imágenes:")
print(df["cantidad"].sum())

print("\nCantidad total por clase:")
print(df.groupby("clase")["cantidad"].sum())

print("\nCantidad total por división:")
print(df.groupby("division")["cantidad"].sum())

# Guardar resumen en CSV
df.to_csv(RESULTADOS_DIR / "resumen_dataset.csv", index=False)

# ============================================
# 5. Crear gráfico de distribución
# ============================================

plt.figure(figsize=(9, 5))

labels = df["clase"] + " - " + df["division"]

plt.bar(labels, df["cantidad"])
plt.title("Distribución de imágenes por clase y división")
plt.xlabel("Clase y división")
plt.ylabel("Cantidad de imágenes")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(RESULTADOS_DIR / "distribucion_dataset.png")
plt.close()

# ============================================
# 6. Crear mosaico de ejemplos del dataset
# ============================================

train_path = DATASET_DIR / "train"

if train_path.exists():
    clases = sorted([carpeta.name for carpeta in train_path.iterdir() if carpeta.is_dir()])

    filas = len(clases)
    columnas = 3

    fig, axes = plt.subplots(filas, columnas, figsize=(9, 3 * filas))

    # Si hay una sola clase, axes no viene como matriz, lo normalizamos
    if filas == 1:
        axes = [axes]

    for fila, clase in enumerate(clases):
        clase_path = train_path / clase

        imagenes = []

        for extension in extensiones:
            imagenes.extend(list(clase_path.glob(extension)))

        if len(imagenes) == 0:
            continue

        cantidad_muestras = min(columnas, len(imagenes))
        imagenes_seleccionadas = random.sample(imagenes, cantidad_muestras)

        for col in range(columnas):
            ax = axes[fila][col] if filas > 1 else axes[col]

            if col < cantidad_muestras:
                img_path = imagenes_seleccionadas[col]
                img = Image.open(img_path).convert("RGB")

                ax.imshow(img)
                ax.set_title(clase)
                ax.axis("off")
            else:
                ax.axis("off")

    plt.suptitle("Ejemplos de imágenes por clase", fontsize=14)
    plt.tight_layout()
    plt.savefig(RESULTADOS_DIR / "ejemplos_dataset.png")
    plt.close()

# ============================================
# 7. Conclusiones del avance
# ============================================

print("\nArchivos generados:")
print("- resultados/resumen_dataset.csv")
print("- resultados/distribucion_dataset.png")
print("- resultados/ejemplos_dataset.png")

print("\nConclusión del avance:")
print("El dataset inicial de imágenes está organizado en train, valid y test.")
print("Las clases encontradas corresponden a cinco tipos de flores: dienteleon, girasol, margarita, rosa y tulipan.")
print("El dataset presenta una distribución no completamente balanceada, ya que la clase tulipan posee más imágenes que rosa y girasol.")
print("En esta etapa no se entrena el modelo, solo se prepara y analiza el dataset.")

print("\nPróximo paso:")
print("Entrenar un modelo de clasificación de imágenes usando Transfer Learning con ResNet50.")