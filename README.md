# Proyecto del curso: Animando una Skip List — Algoritmos y Estructuras de Datos CS2023, UTEC (2026-2)

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

```
/cpp     → implementación de la Skip List en C++
/python  → parser del CSV y animación en Manim
/output  → CSV de eventos generado y video final
```

## Requisitos
- C++17 o superior
- Python 3, con la siguiente librería:
  - manim

## Cómo compilar y ejecutar

### 1. Descargar el repositorio
Clona o descarga este repositorio en tu computadora:
```bash
git clone https://github.com/GabrielSaavedraP/AED-Proyecto-SkipList
```
O usa el botón "Code → Download ZIP" desde GitHub y descomprime la carpeta.

### 2. Parte C++ (implementación de la Skip List)
1. Abre la carpeta `/cpp` en CLion (o tu IDE favorito).
2. En el repo encontrarás un main ya hecho en el archivo `SkipList.cpp`. Puedes modificarlo a tu gusto o dejarlo tal como está, pues ese caso fue el que se usó en el video demostrativo de la Skip List.
3. Compila y ejecuta el proyecto manualmente desde el IDE.
4. Al ejecutarlo, se generará el archivo `output/events.csv` con los eventos de la ejecución.

### 3. Parte Python (animación en Manim)
1. Abre la carpeta `/python` en PyCharm (o tu IDE favorito).
2. Asegúrate de tener instalada la librería `manim` (`pip install manim`).
3. Ejecuta manualmente el script de animación desde el IDE, indicando el archivo `events.csv` generado en el paso anterior como entrada.
4. También puedes ejecutarlo desde la terminal integrada del IDE:
   - Video de baja resolución: `manim -pql skiplist_animation.py SkipList`
   - Video de alta resolución: `manim -pqh skiplist_animation.py SkipList`
5. El video se generará dentro de la carpeta `python/media/videos/...`.

## Formato del CSV de eventos

Columnas:
```
Iteracion,Operacion,Valor,Accion,Nivel,Nodo_Actual,Nodo_Siguiente,Resultado
```

| Columna | Descripción |
|---|---|
| `Iteracion` | Número secuencial del evento (orden de reproducción) |
| `Operacion` | `INSERTAR`, `BUSCAR`, o `ELIMINAR` |
| `Valor` | Valor con el que estemos trabajando |
| `Accion` | Tipo de evento (ver tabla abajo) |
| `Nivel` | Nivel de la Skip List donde ocurre el evento |
| `Nodo_Actual` | Nodo donde está "parado" el algoritmo en ese momento |
| `Nodo_Siguiente` | Nodo siguiente evaluado (vacío si es el final) |
| `Resultado` | Resultado del evento |

### Tipos de `Accion`

| Acción | Descripción |
|---|---|
| `INICIAR` | Inicio de la operación (insertar, buscar o eliminar) |
| `AVANZAR` | El algoritmo avanza porque el valor siguiente es menor al buscado |
| `BAJAR` | El algoritmo baja de nivel al no poder avanzar más en el actual |
| `CALCULAR_NIVEL` | Se sortea aleatoriamente hasta qué nivel sube el nuevo nodo |
| `INSERTAR_NODO` | Se crea el nodo nuevo |
| `ACTUALIZAR_PUNTEROS` | Se enlaza el nodo nuevo con sus vecinos en un nivel |
| `ELIMINAR_NODO` | Se encuentra y desconecta el nodo a eliminar |
| `FIN_EXITO` | La operación terminó exitosamente |
| `FIN_FALLO` | La operación no encontró el valor (o era un duplicado) |

### Ejemplo real (insertar 5, con la lista ya conteniendo 23)

```csv
Iteracion,Operacion,Valor,Accion,Nivel,Nodo_Actual,Nodo_Siguiente,Resultado
8,INSERTAR,5,INICIAR,1,HEAD,23,INICIO_OPERACION
9,INSERTAR,5,BAJAR,1,HEAD,23,NIVEL_COMPLETADO
10,INSERTAR,5,BAJAR,0,HEAD,23,NIVEL_COMPLETADO
11,INSERTAR,5,CALCULAR_NIVEL,0,NULL,NULL,NIVEL_GENERADO_0
12,INSERTAR,5,INSERTAR_NODO,0,5,NULL,NODO_CREADO
13,INSERTAR,5,ACTUALIZAR_PUNTEROS,0,HEAD,5,ENLACE_LISTO
14,INSERTAR,5,FIN_EXITO,1,5,NULL,OPERACION_COMPLETA
```

## Video final
https://youtu.be/UV59AYh3784

## Inspiración
Estilo de animación inspirado en los canales y páginas web: [3Blue1Brown](https://www.3blue1brown.com/), [Reducible](https://www.youtube.com/c/Reducible) y [VisuAlgo](https://visualgo.net/).
```
