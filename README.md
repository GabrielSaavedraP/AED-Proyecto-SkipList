
# Proyecto del curso: Animando una Skip List  - Algoritmos y Estructuras de Datos CS2023, UTEC (2026-2).

## Integrantes
- Ariel Mathias Fernando Choque Marcelo — Implementación en C++
- Rodrigo de Santa María Anco Ito — Animación en Python/Manim
- Gabriel Saavedra Peralta — Guion, informe y coordinación

## Descripción
Implementación de una **Skip List** en C++ y animación educativa de su funcionamiento
usando **Manim (Python)**, conectados mediante un archivo CSV de eventos generado por
la ejecución real de la estructura.

La animación no simula pasos "a mano": cada evento visual proviene de la ejecución
real de la Skip List implementada en C++, que registra su comportamiento paso a paso
en un archivo CSV, el cual es leído e interpretado por el script de animación en Python.

## Estructura del repositorio

/cpp → implementación de la Skip List en C++
/python → parser del CSV y animación en Manim
/output → CSV de eventos generado y video final


## Requisitos
- C++17 o superior 
- Python 3, con las siguientes librerías:
  - manim
  - [PLACEHOLDER: otras librerías si llegamos a agregar]

## Cómo compilar y ejecutar

### 1. Descargar el repositorio
Clona o descarga este repositorio en tu computadora:
```bash
git clone https://github.com/GabrielSaavedraP/AED-Proyecto-SkipList
```
O usa el botón "Code -> Download ZIP" desde GitHub y descomprime la carpeta.

### 2. Parte C++ (implementación de la Skip List)
1. Abre la carpeta `/cpp` en CLion (o tu IDE favorito)
2. Compila y ejecuta el proyecto manualmente desde el IDE.
3. Al ejecutarlo, se generará el archivo `output/events.csv` con los eventos de la ejecución.

### 3. Parte Python (animación en Manim)
1. Abre la carpeta `/python` en PyCharm (o tu IDE favorito).
2. Asegúrate de tener instalada la librería `manim` (`pip install manim`).
3. Ejecuta manualmente el script de animación desde el IDE, indicando el archivo `events.csv` generado en el paso anterior como entrada.
4. El video se generará dentro de la carpeta `python/media/videos/...`.

## Formato del CSV de eventos

Columnas:
iteracion,operacion,valor,accion,nivel,nodo_actual,nodo_siguiente,resultado


| Columna | Descripción |
|---|---|
| `iteracion` | Número secuencial del evento (orden de reproducción) |
| `operacion` | `insert`, `search`, o `remove` |
| `valor` | Valor con el que estemos trabajando |
| `accion` | Tipo de evento (ver tabla abajo) |
| `nivel` | Nivel de la Skip List donde ocurre el evento |
| `nodo_actual` | Nodo donde está "parado" el algoritmo en ese momento |
| `nodo_siguiente` | Nodo siguiente evaluado (vacío si es el final) |
| `resultado` | Resultado del evento |

### Tipos de `accion`

| Acción | Descripción | `resultado` posible |
|---|---|---|
| `sorteo_nivel` | Se decide aleatoriamente si el nodo sube un nivel más | `sube_nivel` / `se_detiene` |
| `comparar` | Se compara `nodo_actual`/`nodo_siguiente` contra `valor` | `avanza` / `baja` / `inserta_aqui` |
| `recorrer` | El algoritmo pasa por un nodo existente (search/remove) | — |
| `insertar_nodo` | Se crea y enlaza un nodo nuevo en ese nivel | — |
| `eliminar_nodo` | Se desconecta un nodo en ese nivel | — |
| `encontrado` | Resultado final positivo de `search` | — |
| `no_encontrado` | Resultado final negativo de `search`/`remove` | — |
| `fin` | Fin de la operación completa | — |

### Ejemplo (insertar 17)

```csv
iteracion,operacion,valor,accion,nivel,nodo_actual,nodo_siguiente,resultado
1,insert,17,sorteo_nivel,1,,,sube_nivel
2,insert,17,sorteo_nivel,2,,,sube_nivel
3,insert,17,sorteo_nivel,3,,,se_detiene
4,insert,17,comparar,2,6,,baja
5,insert,17,comparar,1,6,12,avanza
6,insert,17,comparar,1,12,,baja
7,insert,17,comparar,0,12,19,inserta_aqui
8,insert,17,insertar_nodo,0,17,,
9,insert,17,insertar_nodo,1,17,,
10,insert,17,fin,,,,
```

## Video final
[PLACEHOLDER A NUESTRO VIDEO. supongo que lo subiremos en YT]

## Inspiración
Estilo de animación inspirado en el canal [3Blue1Brown](https://www.3blue1brown.com/).
[PLACEHOLDER SI ENCUENTRAN ALGUNA OTRA INSPIRACION CHEVERE]
