# Project Log: micro.llama2.c

## 📝 Registro: v1.0 - Corrección de Inferencia y Parámetros
- **Fallo/Motivo**: El comando `sample.py` fallaba con `AssertionError` y luego con `UnpicklingError`.
- **Causa**: 
    1. El `configurator.py` requiere el formato `--key=val` para los argumentos.
    2. PyTorch 2.6 cambió el valor por defecto de `weights_only` a `True` en `torch.load`, lo que rompe la carga de checkpoints antiguos de este proyecto.
- **Solución/Cambio**: 
    1. Se instruyó al usuario a usar el formato `--key=val`.
    2. Se modificará `sample.py` para incluir `weights_only=False` en la llamada a `torch.load`.

## 📝 Registro: v1.1 - Archivo Corrupto Detectado
- **Fallo**: `_pickle.UnpicklingError: invalid load key, 'E'.`
- **Causa**: El archivo `stories260K.bin` tiene un tamaño de 15 bytes y contiene el texto "Entry not found". Probablemente una descarga fallida de HuggingFace. Además, es un archivo `.bin` (C) intentando ser leído como `.pt` (PyTorch).
- **Solución**: Notificar al usuario y proporcionar links correctos para modelos `.pt`.

## 📝 Registro: v1.2 - Inferencia Exitosa (Python)
- **Cambio**: Se descargó el modelo `stories15M.pt` (58MB).
- **Resultado**: El script `sample.py` generó texto correctamente: *"Once upon a time, there was a little girl named Lily..."*.
- **Estado**: La versión de Python está operativa.

## 📝 Registro: v1.3 - Resolución de stories260K.pt
- **Fallo**: `AssertionError: data\tok512.model` e `IndexError`.
- **Causa**: 
    1. El modelo `stories260K` tiene un vocabulario de solo 512 tokens.
    2. Intentar usar el tokenizer de Llama2 (32,000 tokens) causa un error de índice en la capa de embeddings.
- **Solución**: Se descargó el archivo `tok512.model` en la carpeta `data/`.
- **Resultado**: Inferencia exitosa con el modelo mini para pruebas.

# Backup
*(Aquí se guardarán ideas descartadas o versiones anteriores en el futuro)*
