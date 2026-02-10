# Project Status: micro.llama2.c

## 📖 Descripción y Arquitectura
Este proyecto es una implementación minimalista de Llama 2 en C y Python. El objetivo es entrenar modelos de la familia TinyStories para su ejecución en hardware limitado como el **ESP32**.

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

## 🚑 Solución de Problemas
- **Index out of range**: Mismatch entre `vocab_size` pretokenizado y el del entrenamiento.
- **AssertionError: No bin files found**: Asegúrate de tener al menos 2 archivos `.bin` en la carpeta `tokN`.
- **FileNotFoundError 'Cul'**: No uses caracteres especiales o espacios libres en los comandos de Windows.
