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

## 📝 Registro: v1.4 - Dataset de Ejemplo y Fine-tuning
- **Cambio**: Se creó un dataset de ejemplo (`data/TinyStories_all_data/custom_data.json`) con 10 instrucciones.
- **Documentación**: Se añadieron los pasos para "Fine-tuning" al `project_status.md`, incluyendo pretokenización y entrenamiento con `--init_from="resume"`.
- **Razón**: El usuario desea saber cómo preparar sus propios datos para entrenar el modelo antes de llevarlo al ESP32.

## 📝 Registro: v1.5 - Modalidades de Entrenamiento y Cálculo de Tamaño
- **Añadido**: Explicación en `project_status.md` sobre la diferencia entre refinar (resume) y entrenar desde cero (scratch).
- **Añadido**: Guía de cálculo de parámetros y peso del modelo para ESP32.
- **Razón**: El usuario necesita saber cómo configurar el tamaño exacto del modelo y calcular si cabrá en el hardware limitado del ESP32.

## 📝 Registro: v1.6 - Corrección de train.py para CPU
- **Fallo**: `RuntimeError: Attempting to deserialize object on a CUDA device but torch.cuda.is_available() is False.`
- **Causa**: 
    1. `train.py` tenía `device = "cuda"` hardcodeado, lo que forzaba a `torch.load` a buscar una GPU incluso al usar `map_location`.
    2. Al igual que en `sample.py`, faltaba `weights_only=False` para PyTorch 2.6+.
- **Solución**: 
    1. Se hizo dinámica la selección de `device` (CPU/CUDA) y `dtype`.
    2. Se añadió `weights_only=False` a `torch.load` en `train.py`.
    3. Se desactivó `compile` por defecto para evitar errores en Windows.

## 📝 Registro: v1.7 - Guía Maestra de Fine-tuning
- **Documentado**: Se creó la "Guía Maestra de Fine-tuning" en `project_status.md`.
- **Hallazgo**: El cargador de datos requiere al menos 2 shards binarios para el shuffle; se instruyó duplicar datos si el dataset es pequeño.
- **Hallazgo**: `configurator.py` rompe la ejecución con espacios en los parámetros de terminal; se recomendó el uso de guiones bajos (`_`).
- **Ajuste**: Se crearon las carpetas necesarias (`data/tok512/`) para que el entrenamiento encuentre los datos correctamente.

## 📝 Registro: v1.8 - Consolidación de Guía Multimodelo
- **Documentado**: Se reorganizó `project_status.md` para distinguir claramente entre el modelo de ESP32 (260K) y el grande (15M).
- **Añadido**: Instrucciones específicas de pretokenización para ambos casos (vocab 512 vs 32000).
- **Añadido**: Comandos de entrenamiento "desde cero" con parámetros exactos para recrear el tamaño 260K.
- **Añadido**: Tabla Comparativa de parámetros y requisitos de hardware.

## 📝 Registro: v1.9 - Explicación de Train/Validation Split
- **Añadido**: Explicación técnica en `project_status.md` sobre cómo el script usa `sorted()` para asignar el Shard 0 a validación.
- **Recomendación**: Uso de prefijos numéricos (`00_val`, `01_train`) para controlar el flujo de datos sin depender del sistema de archivos.
- **Razón**: El usuario tenía dudas sobre cómo el sistema diferenciaba entre entrenamiento y test, y si intervenía el orden de creación del archivo.

## 📝 Registro: v1.10 - Implementación de Shards y Prueba de Fine-tuning
- **Cambio**: Se dividió el dataset en `00_val.json` (test) y `01_train.json` (entrenamiento).
- **Éxito**: El script `train.py` ejecutó correctamente un ciclo de entrenamiento (10 iters) usando `stories260K.pt` como base.
- **Validación**: Se confirmó que el modelo separa los Shards correctamente (el log mostró pérdidas diferentes para train y val).

# Backup
*(Aquí se guardarán ideas descartadas o versiones anteriores en el futuro)*
