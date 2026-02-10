# Project Status: micro.llama2.c

## Descripción
Este proyecto es una implementación minimalista de Llama 2 en C y Python, basada en el trabajo de Andrej Karpathy (llama2.c). El objetivo es entrenar y ejecutar modelos pequeños de Llama 2 (TinyStories) de manera eficiente.

## Arquitectura
- **train.py**: Script principal para el entrenamiento del modelo usando PyTorch.
- **model.py**: Definición de la arquitectura Transformer de Llama 2.
- **sample.py**: Script para generar texto a partir de un checkpoint entrenado (.pt).
- **run.c / runq.c**: Implementación en C para la inferencia de los modelos (en formato .bin).
- **tokenizer.model / tokenizer.bin**: Tokenizadores utilizados por el modelo.

## Estado Actual
- El usuario instaló dependencias y descargó el modelo `stories15M.pt`.
- **Éxito**: La inferencia con `sample.py` funciona correctamente y genera texto coherente.
- **Pendiente**: Compilación de la versión de C para mayor velocidad.

## Tareas Pendientes
- [x] Corregir la carga de checkpoints en `sample.py`.
- [x] Descargar un modelo válido (`.pt`) y probar inferencia.
- [x] Configurar entorno para `stories260K.pt` (descarga de modelo y tokenizer tok512).
- [ ] Configurar compilador GCC/MSVC para la versión de C (`run.c`).

## Instrucciones de Instalación y Uso (Python)

### 1. Descargar Modelo (.pt)
```cmd
mkdir data

curl -L https://huggingface.co/karpathy/tinyllamas/resolve/main/stories15M.pt -o data/stories15M.pt
```

### 2. Ejecutar Inferencia
```cmd
python sample.py --checkpoint=data/stories15M.pt --start="Once upon a time"
```


## Instrucciones para stories260K (Pruebas ESP32)

### 1. Descargar Modelo y Tokenizer
```cmd
:: Crear carpetas
mkdir data

:: Descargar modelo .pt
curl -L https://huggingface.co/karpathy/tinyllamas/resolve/main/stories260K/stories260K.pt -o data/stories260K.pt

:: Descargar tokenizer personalizado (REQUERIDO para 260K)
curl -L https://huggingface.co/karpathy/tinyllamas/resolve/main/stories260K/tok512.model -o data/tok512.model
```

### 2. Ejecutar
```cmd
python sample.py --checkpoint=data/stories260K.pt --start="Once_upon_a_time"
```
