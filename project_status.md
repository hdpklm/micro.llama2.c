# Project Status: micro.llama2.c

## 📖 Descripción y Arquitectura
Este proyecto es una implementación minimalista de Llama 2 en C y Python. El objetivo es entrenar modelos de la familia TinyStories para su ejecución en hardware limitado como el **ESP32**.

---

## 📂 Gestión de Datos: Train vs Validation

El proyecto utiliza un sistema de **Shards** (fragmentos) para cargar datos. La lógica de separación en `tinystories.py` es estrictamente alfabética:

1. El script busca todos los archivos `.bin` y los **ordena alfabéticamente** (`sorted`).
2. **Shard 0** (el primer archivo): Se usa para **Validation** (test).
3. **Shards 1 en adelante**: Se usan para **Train** (entrenamiento).

### Nomenclatura Recomendada
Para garantizar que el modelo use los archivos correctos, usa prefijos numéricos:
- `00_val.json` → Se convertirá en el archivo de test (Shard 0).
- `01_train.json` → Primer archivo de entrenamiento (Shard 1).
- `02_train.json` ...

**Nota sobre el Sistema de Archivos**: Aunque Windows o Linux almacenen archivos en un orden interno, el código de este proyecto usa la función `sorted()` de Python, por lo que **el nombre manda siempre sobre el orden de creación.**

---

## 🛠️ Preparación del Dataset

El dataset debe estar en `data/TinyStories_all_data/custom_data.json` con el formato:
`[{"story": "Instruction: ... Response: ..."}]`

### 1. Para Modelo PEQUEÑO (ESP32 - 260K)
Usa un vocabulario reducido de 512 tokens para ahorrar memoria.
```cmd
:: Pretokenizar con vocabulario mini
python tinystories.py pretokenize --vocab_size=512

:: REQUERIDO: Duplicar el dataset si es muy pequeño (el trainer necesita 2 archivos)
copy data\tok512\custom_data.bin data\tok512\custom_data2.bin
```

### 2. Para Modelo GRANDE (15M o superior)
Usa el vocabulario estándar de Llama 2 (32,000 tokens).
```cmd
:: Pretokenizar con vocabulario Llama2
python tinystories.py pretokenize --vocab_size=0

:: REQUERIDO: Duplicar si es necesario
copy data\TinyStories_all_data\custom_data.bin data\TinyStories_all_data\custom_data2.bin
```

---

## 🚀 Entrenamiento y Fine-tuning

### A. Modelo PEQUEÑO (260KParams) - El ideal para ESP32
**Dimensiones**: `dim=64`, `n_layers=5`, `n_heads=8`.

- **Desde Cero (Scratch)**:
  ```cmd
  python train.py --init_from="scratch" --dim=64 --n_layers=5 --n_heads=8 --n_kv_heads=4 --max_seq_len=512 --vocab_source="custom" --vocab_size=512 --max_iters=500
  ```
- **Refinar (Fine-tuning)**:
  1. Copia `data/stories260K.pt` a `out/ckpt.pt`.
  2. Ejecuta:
  ```cmd
  python train.py --init_from="resume" --vocab_source="custom" --vocab_size=512 --max_iters=100 --batch_size=4
  ```

### B. Modelo GRANDE (15M Params)
**Dimensiones**: `dim=288`, `n_layers=6`, `n_heads=6`.

- **Desde Cero (Scratch)**:
  ```cmd
  python train.py --init_from="scratch" --dim=288 --n_layers=6 --n_heads=6 --vocab_source="llama2" --vocab_size=32000
  ```
- **Refinar (Fine-tuning)**:
  1. Copia `data/stories15M.pt` a `out/ckpt.pt`.
  2. Ejecuta:
  ```cmd
  python train.py --init_from="resume" --vocab_source="llama2" --vocab_size=32000 --max_iters=100
  ```

---

## 📊 Cálculo de Tamaño y Límites

| Modelo | Parámetros | Tamaño (.pt/bin) | Recomendación Hardware |
| :--- | :--- | :--- | :--- |
| **260K** | ~260,000 | ~1 MB (FP32) / 260 KB (Int8) | ESP32 estándar / S3 |
| **15M** | ~15,000,000 | ~60 MB (FP32) / 15 MB (Int8) | PC / Raspberry Pi / ESP32 con PSRAM externa |

---

## ⚡ Inferencia y Pruebas
Para evitar errores de parsing en la consola de Windows:
1. Usa siempre el formato `--key=val`.
2. Sustituye espacios por guiones bajos `_` en el prompt.

```cmd
:: Ejemplo Inferencia 260K
python sample.py --checkpoint=data/stories260K.pt --start="Instruction:_Hola_quien_eres?_Response:"
```

---

## Tareas Pendientes
- [x] Corregir la carga de checkpoints en `sample.py`.
- [x] Descargar un modelo válido (`.pt`) y probar inferencia.
- [x] Configurar entorno para `stories260K.pt` (split Train/Val y Fine-tuning).
- [ ] Configurar compilador GCC/MSVC para la versión de C (`run.c`).

---

## 🚑 Solución de Problemas
- **Index out of range**: Mismatch entre `vocab_size` pretokenizado y el del entrenamiento.
- **AssertionError: No bin files found**: Asegúrate de tener al menos 2 archivos `.bin` en la carpeta `tokN`.
- **FileNotFoundError 'Cul'**: No uses caracteres especiales o espacios libres en los comandos de Windows.


# Guía Definitiva: Fine-Tuning Modelo 260K (ESP32)

Esta guía contiene los pasos y comandos probados para entrenar el modelo ultraligero (260K parámetros) con tu propio dataset.

## 1. Estructura de Datos (Obligatorio)
Para que el entrenamiento funcione, necesitas **dos archivos** (uno para test, otro para training) pretokenizados en la carpeta correcta.

### Paso A: Crear los JSON
Crea estos dos archivos en `data/TinyStories_all_data/`:
1. **`00_val.json`** (Test): Pon aquí 2 o 3 ejemplos.
2. **`01_train.json`** (Entrenamiento): Pon aquí el resto de tus datos.
*Formato:* `[{"story": "Instruction: ... Response: ..."}]`

### Paso B: Pretokenizar (Vocabulario 512)
Ejecuta este comando para generar los archivos binarios:
```cmd
python tinystories.py pretokenize --vocab_size=512
```
*Verifica que en `data/tok512/` se hayan creado `00_val.bin` y `01_train.bin`.*

---

## 2. Preparar el Modelo Base
Debes tener el modelo base en la carpeta de salida para "resumir" el entrenamiento desde ahí.
```cmd
mkdir out
copy data\stories260K.pt out\ckpt.pt
```

---

## 3. COMANDO DE ENTRENAMIENTO (Probado)
Este comando está ajustado para datasets pequeños (para evitar errores de memoria o índice).

**Ejecutar:**
```cmd
python train.py --init_from="resume" --vocab_source="custom" --vocab_size=512 --batch_size=1 --gradient_accumulation_steps=16 --max_seq_len=64 --max_new_iters=100 --eval_interval=5 --learning_rate=5e-4 --decay_lr=False --always_save_checkpoint=True
```

### Explicación de Parámetros Clave:
- `--init_from="resume"`: Carga el cerebro del modelo 260K.
- `--max_new_iters=100`: Entrena 100 pasos nuevos obligatoriamente.
- `--always_save_checkpoint=True`: **Crucial**. Obliga a guardar los cambios aunque el "test" inicial sea peor que el del modelo original.
- `--vocab_size=512`: Usa el diccionario reducido del ESP32.
- `--learning_rate=5e-4` y `--decay_lr=False`: Mantiene el aprendizaje activo.

---

## 4. Probar el Modelo (Inferencia)
Nota: Usa guiones bajos `_` para evitar errores en la terminal de Windows.
```cmd
python sample.py --checkpoint=out/ckpt.pt --start="Instruction:_Hola_quien_eres?_Response:"
```



###### test:
> train
```bash
python train.py --init_from="resume" --vocab_source="custom" --vocab_size=512 --batch_size=1 --gradient_accumulation_steps=16 --max_seq_len=64 --max_new_iters=1000 --eval_interval=5 --learning_rate=5e-4 --decay_lr=False --always_save_checkpoint=True
```

> test
```bash
python sample.py --checkpoint=out/ckpt.pt --start="Instruction: Explícame qué es un átomo. Response: el atomo es "
```



