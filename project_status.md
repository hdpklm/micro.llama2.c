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
- [ ] Configurar compilador GCC/MSVC para la versión de C (`run.c`).

## Instrucciones de Instalación y Uso (Python)

### 1. Descargar Modelo (.pt)
```cmd
mkdir out15M
curl -L https://huggingface.co/karpathy/tinyllamas/resolve/main/stories15M.pt -o out15M/stories15M.pt
```

### 2. Ejecutar Inferencia
```cmd
python sample.py --checkpoint=out15M/stories15M.pt --start="Once upon a time"
```
