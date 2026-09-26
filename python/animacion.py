from manim import *
import csv
import os
from pathlib import Path


def buscar_csv():
    """Busca animacion.csv: 1) variable SKIPLIST_CSV, 2) junto a este script,
    3) ../ProyectoAED/animacion.csv (estructura original del repo)."""
    aqui = Path(__file__).resolve().parent
    candidatos = []
    if os.environ.get("SKIPLIST_CSV"):
        candidatos.append(Path(os.environ["SKIPLIST_CSV"]))
    candidatos += [
        aqui / "animacion.csv",
        aqui.parent / "ProyectoAED" / "animacion.csv",
    ]
    for ruta in candidatos:
        if ruta.exists():
            return ruta
    raise FileNotFoundError(
        "No se encontró animacion.csv. Ejecuta primero el programa C++ "
        "o define SKIPLIST_CSV con la ruta del archivo."
    )


class SkipList(Scene):

    def construct(self):

        # --------------------------------------------------
        # LEER CSV REAL GENERADO POR C++
        # --------------------------------------------------

        ruta_csv = buscar_csv()

        with open(ruta_csv, newline="", encoding="utf-8") as archivo:
            eventos = list(csv.DictReader(archivo))

        if len(eventos) == 0:
            raise ValueError("El archivo animacion.csv está vacío.")

        self.eventos = eventos

        self.valores = sorted({
            int(evento["Valor"])
            for evento in eventos
            if evento["Operacion"] == "INSERTAR"
        })

        self.max_nivel = max(
            int(evento["Nivel"])
            for evento in eventos
        )

        self.total_operaciones = sum(
            1
            for evento in eventos
            if evento["Accion"] == "INICIAR"
        )

        self.numero_operacion = 0

        # --------------------------------------------------
        # ESTRUCTURAS VISUALES
        # --------------------------------------------------

        self.nodos = {}
        self.nivel_nodo = {}

        self.enlaces = {}
        self.flechas = {}

        self.verticales = {}

        self.indicador = None
        self.estado = None
        self.operacion_texto = None
        self.contador_texto = None

        self.pendiente_eliminar = None

        # --------------------------------------------------
        # PREPARACIÓN
        # --------------------------------------------------

        self.preparar_posiciones()

        self.introduccion()

        self.preparar_escena_principal()

        self.crear_niveles()

        self.crear_head()

        # --------------------------------------------------
        # EJECUCIÓN REAL DEL CSV
        # --------------------------------------------------

        for evento in eventos:
            self.animar_evento(evento)

        # --------------------------------------------------
        # CIERRE
        # --------------------------------------------------

        self.cierre()

    # ==================================================
    # POSICIONES
    # ==================================================

    def preparar_posiciones(self):

        self.posiciones = {}

        # HEAD más a la derecha para no tapar "Nivel"
        self.posiciones["HEAD"] = -4.75

        inicio = -3.2
        fin = 4.75

        if len(self.valores) == 1:

            self.posiciones[str(self.valores[0])] = 0

        else:

            paso = (fin - inicio) / (len(self.valores) - 1)

            for i, valor in enumerate(self.valores):

                self.posiciones[str(valor)] = inicio + paso * i

    def posicion_y(self, nivel):

        return -1.35 + nivel * 0.95

    # ==================================================
    # INTRODUCCIÓN
    # ==================================================

    def introduccion(self):

        titulo = Text(
            "SKIP LIST",
            font_size=52,
            color=BLUE_B
        )

        titulo.move_to([0, 2.4, 0])

        subtitulo = Text(
            "Animando una Estructura de Datos",
            font_size=29
        )

        subtitulo.next_to(
            titulo,
            DOWN,
            buff=0.35
        )

        integrantes = VGroup(

            Text(
                "Ariel Mathias Fernando Choque Marcelo",
                font_size=19
            ),

            Text(
                "Rodrigo de Santa Maria Anco Ito",
                font_size=19
            ),

            Text(
                "Gabriel Saavedra Peralta",
                font_size=19
            )
        )

        integrantes.arrange(
            DOWN,
            buff=0.16
        )

        integrantes.next_to(
            subtitulo,
            DOWN,
            buff=0.55
        )

        self.play(
            Write(titulo),
            run_time=0.8
        )

        self.play(
            FadeIn(subtitulo),
            run_time=0.5
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(nombre, shift=RIGHT * 0.15)
                    for nombre in integrantes
                ],
                lag_ratio=0.2
            ),
            run_time=0.8
        )

        self.wait(1.5)

        self.play(
            FadeOut(titulo),
            FadeOut(subtitulo),
            FadeOut(integrantes),
            run_time=0.6
        )

        # --------------------------------------------------
        # EXPLICACIÓN CONCEPTUAL
        # --------------------------------------------------

        titulo_concepto = Text(
            "¿Qué es una Skip List?",
            font_size=38,
            color=BLUE_B
        )

        titulo_concepto.to_edge(
            UP,
            buff=0.6
        )

        linea0 = Text(
            "TDA: Conjunto Ordenado",
            font_size=25,
            color=GREEN
        )

        linea1 = Text(
            "Es una estructura ordenada formada por varios niveles.",
            font_size=25
        )

        linea2 = Text(
            "El Nivel 0 contiene todos los elementos.",
            font_size=24
        )

        linea3 = Text(
            "Los niveles superiores funcionan como atajos.",
            font_size=24,
            color=YELLOW
        )

        linea4 = Text(
            "La altura de cada nodo se decide probabilísticamente.",
            font_size=24
        )

        explicacion = VGroup(
            linea0,
            linea1,
            linea2,
            linea3,
            linea4
        )

        explicacion.arrange(
            DOWN,
            buff=0.38
        )

        explicacion.move_to([0, 0.2, 0])

        self.play(
            FadeIn(titulo_concepto),
            run_time=0.5
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(linea, shift=UP * 0.1)
                    for linea in explicacion
                ],
                lag_ratio=0.25
            ),
            run_time=1.3
        )

        self.wait(3)

        # --------------------------------------------------
        # SORTEO 50 %
        # --------------------------------------------------

        moneda = Circle(
            radius=0.48,
            color=YELLOW
        )

        moneda.set_fill(
            YELLOW,
            opacity=0.12
        )

        moneda_texto = Text(
            "50%",
            font_size=24,
            color=YELLOW
        )

        moneda_texto.move_to(moneda)

        grupo_moneda = VGroup(
            moneda,
            moneda_texto
        )

        grupo_moneda.move_to([4.9, -2.2, 0])

        probabilidad = Text(
            "Probabilidad de subir otro nivel",
            font_size=19,
            color=GRAY_B
        )

        probabilidad.next_to(
            grupo_moneda,
            LEFT,
            buff=0.3
        )

        self.play(
            GrowFromCenter(grupo_moneda),
            FadeIn(probabilidad),
            run_time=0.5
        )

        self.play(
            Rotate(
                grupo_moneda,
                angle=2 * PI
            ),
            run_time=0.8
        )

        self.wait(1.5)

        # --------------------------------------------------
        # USO PRÁCTICO
        # --------------------------------------------------

        self.play(
            FadeOut(grupo_moneda),
            FadeOut(probabilidad),
            FadeOut(explicacion),
            run_time=0.5
        )

        uso = Text(
            "Aplicación práctica",
            font_size=31,
            color=GREEN
        )

        uso.move_to([0, 0.7, 0])

        uso_texto = Text(
            "Mantiene datos ordenados con búsquedas eficientes.\n"
            "Ej.: Redis la usa en sus Sorted Sets (rankings, leaderboards).",
            font_size=23,
            line_spacing=1.2
        )

        uso_texto.next_to(
            uso,
            DOWN,
            buff=0.4
        )

        self.play(
            FadeIn(uso),
            FadeIn(uso_texto),
            run_time=0.5
        )

        self.wait(2.5)

        self.play(
            FadeOut(titulo_concepto),
            FadeOut(uso),
            FadeOut(uso_texto),
            run_time=0.6
        )

    # ==================================================
    # ESCENA PRINCIPAL
    # ==================================================

    def preparar_escena_principal(self):

        self.titulo_fijo = Text(
            "SKIP LIST",
            font_size=31,
            color=BLUE_B
        )

        self.titulo_fijo.to_edge(
            UP,
            buff=0.18
        )

        fuente = Text(
            "Ejecución real: C++  →  CSV  →  Manim",
            font_size=15,
            color=GRAY_B
        )

        fuente.to_corner(
            UR,
            buff=0.2
        )

        self.play(
            FadeIn(self.titulo_fijo),
            FadeIn(fuente),
            run_time=0.5
        )

        self.wait(1)

    # ==================================================
    # NIVELES
    # ==================================================

    def crear_niveles(self):

        for nivel in range(
            self.max_nivel,
            -1,
            -1
        ):

            etiqueta = Text(
                f"Nivel {nivel}",
                font_size=18,
                color=GRAY_B
            )

            # Mucho más separado de HEAD
            etiqueta.move_to([
                -6.45,
                self.posicion_y(nivel),
                0
            ])

            self.play(
                FadeIn(etiqueta),
                run_time=0.18
            )

    # ==================================================
    # HEAD
    # ==================================================

    def crear_head(self):

        objetos = []

        for nivel in range(
            self.max_nivel + 1
        ):

            caja = RoundedRectangle(
                width=1.10,
                height=0.56,
                corner_radius=0.10,
                color=TEAL
            )

            caja.move_to([
                self.posiciones["HEAD"],
                self.posicion_y(nivel),
                0
            ])

            texto = Text(
                "HEAD",
                font_size=16
            )

            texto.move_to(caja)

            nodo = VGroup(
                caja,
                texto
            )

            self.nodos[
                (nivel, "HEAD")
            ] = nodo

            objetos.append(nodo)

        self.play(
            LaggedStart(
                *[
                    FadeIn(
                        objeto,
                        shift=UP * 0.10
                    )
                    for objeto in objetos
                ],
                lag_ratio=0.15
            ),
            run_time=0.6
        )

        lineas = VGroup()

        for nivel in range(
            self.max_nivel
        ):

            linea = DashedLine(
                self.nodos[
                    (nivel, "HEAD")
                ].get_top(),

                self.nodos[
                    (nivel + 1, "HEAD")
                ].get_bottom(),

                color=GRAY,
                stroke_width=2
            )

            linea.set_z_index(-1)

            lineas.add(linea)

        if len(lineas) > 0:

            self.play(
                LaggedStart(
                    *[
                        Create(linea)
                        for linea in lineas
                    ],
                    lag_ratio=0.2
                ),
                run_time=0.4
            )

    # ==================================================
    # OPERACIÓN ACTUAL
    # ==================================================

    def nombre_operacion(self, operacion):

        if operacion == "INSERTAR":
            return "INSERCIÓN"

        if operacion == "BUSCAR":
            return "BÚSQUEDA"

        if operacion == "ELIMINAR":
            return "ELIMINACIÓN"

        return operacion

    def cambiar_operacion(
        self,
        operacion,
        valor
    ):

        nombre = self.nombre_operacion(
            operacion
        )

        texto = Text(
            f"{nombre}: {valor}",
            font_size=25,
            color=BLUE_B
        )

        texto.move_to([
            0,
            2.65,
            0
        ])

        contador = Text(
            f"Operación {self.numero_operacion} de {self.total_operaciones}",
            font_size=16,
            color=GRAY_B
        )

        contador.next_to(
            texto,
            DOWN,
            buff=0.12
        )

        if self.operacion_texto is None:

            self.operacion_texto = texto
            self.contador_texto = contador

            self.play(
                FadeIn(
                    self.operacion_texto
                ),
                FadeIn(
                    self.contador_texto
                ),
                run_time=0.35
            )

        else:

            self.play(
                Transform(
                    self.operacion_texto,
                    texto
                ),
                Transform(
                    self.contador_texto,
                    contador
                ),
                run_time=0.35
            )

    # ==================================================
    # ESTADO INFERIOR
    # ==================================================

    def cambiar_estado(
        self,
        texto,
        color=WHITE
    ):

        nuevo = Text(
            texto,
            font_size=19,
            color=color
        )

        if nuevo.width > 12:
            nuevo.scale_to_fit_width(12)

        nuevo.move_to([
            0,
            -2.95,
            0
        ])

        if self.estado is None:

            self.estado = nuevo

            self.play(
                FadeIn(self.estado),
                run_time=0.22
            )

        else:

            self.play(
                Transform(
                    self.estado,
                    nuevo
                ),
                run_time=0.22
            )

    # ==================================================
    # INDICADOR AMARILLO
    # ==================================================

    def mover_indicador(
        self,
        nivel,
        valor
    ):

        clave = (
            nivel,
            valor
        )

        if clave not in self.nodos:
            return

        nuevo = SurroundingRectangle(
            self.nodos[clave],
            buff=0.08,
            color=YELLOW,
            stroke_width=4
        )

        if self.indicador is None:

            self.indicador = nuevo

            self.play(
                Create(
                    self.indicador
                ),
                run_time=0.28
            )

        else:

            self.play(
                Transform(
                    self.indicador,
                    nuevo
                ),
                run_time=0.4
            )

    # ==================================================
    # INSERTAR NODO VISUAL
    # ==================================================

    def insertar_nodo_visual(
        self,
        valor,
        nivel_maximo
    ):

        self.nivel_nodo[
            valor
        ] = nivel_maximo

        objetos = []

        for nivel in range(
            nivel_maximo + 1
        ):

            caja = RoundedRectangle(
                width=0.72,
                height=0.56,
                corner_radius=0.10,
                color=BLUE
            )

            caja.move_to([
                self.posiciones[valor],
                self.posicion_y(nivel),
                0
            ])

            texto = Text(
                valor,
                font_size=21
            )

            texto.move_to(caja)

            nodo = VGroup(
                caja,
                texto
            )

            self.nodos[
                (nivel, valor)
            ] = nodo

            objetos.append(nodo)

        self.play(
            LaggedStart(
                *[
                    FadeIn(
                        objeto,
                        shift=UP * 0.18
                    )
                    for objeto in objetos
                ],
                lag_ratio=0.18
            ),
            run_time=0.6
        )

        lineas = VGroup()

        for nivel in range(
            nivel_maximo
        ):

            linea = DashedLine(
                self.nodos[
                    (nivel, valor)
                ].get_top(),

                self.nodos[
                    (nivel + 1, valor)
                ].get_bottom(),

                color=GRAY,
                stroke_width=2
            )

            linea.set_z_index(-1)

            lineas.add(linea)

        self.verticales[
            valor
        ] = lineas

        if len(lineas) > 0:

            self.play(
                LaggedStart(
                    *[
                        Create(linea)
                        for linea in lineas
                    ],
                    lag_ratio=0.2
                ),
                run_time=0.4
            )

    # ==================================================
    # CREAR FLECHA
    # ==================================================

    def crear_flecha(
        self,
        nivel,
        origen,
        destino
    ):

        if destino == "NULL":
            return None

        clave_origen = (
            nivel,
            origen
        )

        clave_destino = (
            nivel,
            destino
        )

        if clave_origen not in self.nodos:
            return None

        if clave_destino not in self.nodos:
            return None

        flecha = Arrow(
            self.nodos[
                clave_origen
            ].get_right(),

            self.nodos[
                clave_destino
            ].get_left(),

            buff=0.08,
            stroke_width=3,
            color=WHITE,
            max_tip_length_to_length_ratio=0.3
        )

        flecha.set_z_index(-1)

        return flecha

    # ==================================================
    # ACTUALIZAR PUNTEROS
    # ==================================================

    def actualizar_punteros(
        self,
        operacion,
        valor,
        nivel,
        origen,
        destino
    ):

        clave = (
            nivel,
            origen
        )

        destino_anterior = (
            self.enlaces.get(
                clave,
                "NULL"
            )
        )

        animaciones = []

        # Eliminar flecha anterior
        if clave in self.flechas:

            animaciones.append(
                FadeOut(
                    self.flechas[clave]
                )
            )

            del self.flechas[clave]

        # Si se inserta entre dos nodos,
        # conservar el enlace desde el nodo nuevo
        if (
            operacion == "INSERTAR"
            and destino == valor
        ):

            self.enlaces[
                (nivel, destino)
            ] = destino_anterior

            if destino_anterior != "NULL":

                salida_nuevo = (
                    self.crear_flecha(
                        nivel,
                        destino,
                        destino_anterior
                    )
                )

                if salida_nuevo is not None:

                    self.flechas[
                        (nivel, destino)
                    ] = salida_nuevo

                    animaciones.append(
                        Create(
                            salida_nuevo
                        )
                    )

        # Crear nuevo enlace
        self.enlaces[
            clave
        ] = destino

        nueva = self.crear_flecha(
            nivel,
            origen,
            destino
        )

        if nueva is not None:

            self.flechas[
                clave
            ] = nueva

            animaciones.append(
                Create(nueva)
            )

        if len(animaciones) > 0:

            self.play(
                *animaciones,
                run_time=0.7
            )

    # ==================================================
    # ELIMINAR NODO
    # ==================================================

    def eliminar_nodo_visual(
        self,
        valor
    ):

        animaciones = []

        nivel_maximo = (
            self.nivel_nodo.get(
                valor,
                0
            )
        )

        for nivel in range(
            nivel_maximo + 1
        ):

            clave_nodo = (
                nivel,
                valor
            )

            if clave_nodo in self.nodos:

                animaciones.append(
                    FadeOut(
                        self.nodos[
                            clave_nodo
                        ]
                    )
                )

                del self.nodos[
                    clave_nodo
                ]

            clave_flecha = (
                nivel,
                valor
            )

            if clave_flecha in self.flechas:

                animaciones.append(
                    FadeOut(
                        self.flechas[
                            clave_flecha
                        ]
                    )
                )

                del self.flechas[
                    clave_flecha
                ]

            if clave_flecha in self.enlaces:

                del self.enlaces[
                    clave_flecha
                ]

        if valor in self.verticales:

            animaciones.append(
                FadeOut(
                    self.verticales[
                        valor
                    ]
                )
            )

            del self.verticales[
                valor
            ]

        if len(animaciones) > 0:

            self.play(
                *animaciones,
                run_time=0.6
            )

    # ==================================================
    # EVENTOS DEL CSV
    # ==================================================

    def animar_evento(
        self,
        evento
    ):

        operacion = evento[
            "Operacion"
        ]

        valor = evento[
            "Valor"
        ]

        accion = evento[
            "Accion"
        ]

        nivel = int(
            evento["Nivel"]
        )

        actual = evento[
            "Nodo_Actual"
        ]

        siguiente = evento[
            "Nodo_Siguiente"
        ]

        resultado = evento[
            "Resultado"
        ]

        # --------------------------------------------------
        # INICIAR OPERACIÓN
        # --------------------------------------------------

        if accion == "INICIAR":

            self.numero_operacion += 1

            self.cambiar_operacion(
                operacion,
                valor
            )

            self.cambiar_estado(
                f"Iniciamos desde HEAD en el nivel {nivel}"
            )

            self.mover_indicador(
                nivel,
                actual
            )

            self.wait(0.8)

        # --------------------------------------------------
        # AVANZAR
        # --------------------------------------------------

        elif accion == "AVANZAR":

            self.cambiar_estado(
                f"{siguiente} < {valor}   →   avanzamos a la derecha"
            )

            self.mover_indicador(
                nivel,
                siguiente
            )

        # --------------------------------------------------
        # BAJAR
        # --------------------------------------------------

        elif accion == "BAJAR":

            if nivel > 0:

                self.cambiar_estado(
                    f"Terminamos el nivel {nivel}   →   bajamos"
                )

                self.mover_indicador(
                    nivel - 1,
                    actual
                )

            else:

                self.cambiar_estado(
                    "Recorrido del Nivel 0 completado"
                )

                clave = (
                    0,
                    actual
                )

                if clave in self.nodos:

                    self.play(
                        Indicate(
                            self.nodos[
                                clave
                            ],
                            color=YELLOW
                        ),
                        run_time=0.35
                    )

        # --------------------------------------------------
        # SORTEO DE NIVEL
        # --------------------------------------------------

        elif accion == "CALCULAR_NIVEL":

            self.cambiar_estado(
                f"Sorteo probabilístico   →   nivel generado: {nivel}",
                YELLOW
            )

            moneda = Circle(
                radius=0.30,
                color=YELLOW
            )

            moneda.set_fill(
                YELLOW,
                opacity=0.15
            )

            texto = Text(
                "50%",
                font_size=17,
                color=YELLOW
            )

            texto.move_to(moneda)

            grupo = VGroup(
                moneda,
                texto
            )

            grupo.move_to([
                5.6,
                2.55,
                0
            ])

            self.play(
                GrowFromCenter(grupo),
                run_time=0.25
            )

            self.play(
                Rotate(
                    grupo,
                    angle=2 * PI
                ),
                run_time=0.8
            )

            self.wait(0.6)

            self.play(
                FadeOut(grupo),
                run_time=0.2
            )

        # --------------------------------------------------
        # INSERTAR NODO
        # --------------------------------------------------

        elif accion == "INSERTAR_NODO":

            self.cambiar_estado(
                f"Se crea el nodo {valor} hasta el nivel {nivel}",
                BLUE_B
            )

            self.insertar_nodo_visual(
                valor,
                nivel
            )

        # --------------------------------------------------
        # ACTUALIZAR PUNTEROS
        # --------------------------------------------------

        elif accion == "ACTUALIZAR_PUNTEROS":

            self.cambiar_estado(
                f"Actualizamos el enlace: {actual}  →  {siguiente}",
                BLUE_A
            )

            self.actualizar_punteros(
                operacion,
                valor,
                nivel,
                actual,
                siguiente
            )

        # --------------------------------------------------
        # ELIMINAR
        # --------------------------------------------------

        elif accion == "ELIMINAR_NODO":

            self.pendiente_eliminar = valor

            self.cambiar_estado(
                f"Encontramos {valor}: será eliminado",
                RED
            )

            nivel_maximo = (
                self.nivel_nodo.get(
                    valor,
                    0
                )
            )

            for nivel_nodo in range(
                nivel_maximo + 1
            ):

                clave = (
                    nivel_nodo,
                    valor
                )

                if clave in self.nodos:

                    self.play(
                        Indicate(
                            self.nodos[
                                clave
                            ],
                            color=RED
                        ),
                        run_time=0.35
                    )

        # --------------------------------------------------
        # ÉXITO
        # --------------------------------------------------

        elif accion == "FIN_EXITO":

            if operacion == "BUSCAR":

                if actual != "NULL":

                    self.mover_indicador(
                        0,
                        actual
                    )

                    clave = (
                        0,
                        actual
                    )

                    if clave in self.nodos:

                        self.play(
                            Indicate(
                                self.nodos[
                                    clave
                                ],
                                color=GREEN
                            ),
                            run_time=0.5
                        )

                self.cambiar_estado(
                    f"{valor} encontrado correctamente",
                    GREEN
                )

            elif operacion == "INSERTAR":

                self.cambiar_estado(
                    f"{valor} insertado correctamente",
                    GREEN
                )

            elif operacion == "ELIMINAR":

                if (
                    self.pendiente_eliminar
                    is not None
                ):

                    self.eliminar_nodo_visual(
                        self.pendiente_eliminar
                    )

                    self.pendiente_eliminar = None

                self.cambiar_estado(
                    f"{valor} eliminado correctamente",
                    GREEN
                )

            self.wait(1.3)

        # --------------------------------------------------
        # FALLO / CASO BORDE
        # --------------------------------------------------

        elif accion == "FIN_FALLO":

            if actual != "NULL":

                clave = (
                    0,
                    actual
                )

                if clave in self.nodos:

                    self.play(
                        Indicate(
                            self.nodos[
                                clave
                            ],
                            color=RED
                        ),
                        run_time=0.4
                    )

            caso_borde = Text(
                "CASO BORDE",
                font_size=22,
                color=RED
            )

            caso_borde.move_to([
                4.9,
                2.6,
                0
            ])

            self.play(
                FadeIn(caso_borde),
                run_time=0.3
            )

            lista_vacia = len(self.nivel_nodo) == 0

            if operacion == "BUSCAR" and lista_vacia:
                mensaje = f"Lista vacía: HEAD apunta a NULL, {valor} no existe"
            elif operacion == "BUSCAR":
                mensaje = f"{valor} no se encuentra en la Skip List"
            elif operacion == "INSERTAR":
                mensaje = f"{valor} ya existe: no se insertan duplicados"
            else:
                mensaje = f"{valor} no existe: no hay nada que eliminar"

            self.cambiar_estado(
                mensaje,
                RED
            )

            self.wait(1.8)

            self.play(
                FadeOut(caso_borde),
                run_time=0.3
            )

        # Pausa pequeña para que cada evento
        # pueda apreciarse visualmente.
        self.wait(0.25)

    # ==================================================
    # CIERRE
    # ==================================================

    def cierre(self):

        if self.indicador is not None:

            self.play(
                FadeOut(
                    self.indicador
                ),
                run_time=0.3
            )

        self.wait(0.5)

        # Quitar TODO lo que siga en pantalla (nodos, flechas, etiquetas
        # "Nivel", líneas verticales de HEAD, títulos, estado...)
        if len(self.mobjects) > 0:

            self.play(
                *[
                    FadeOut(objeto)
                    for objeto in self.mobjects
                ],
                run_time=0.8
            )

        # --------------------------------------------------
        # COMPLEJIDAD
        # --------------------------------------------------

        titulo = Text(
            "Complejidad",
            font_size=39,
            color=BLUE_B
        )

        titulo.move_to([
            0,
            1.75,
            0
        ])

        operaciones = Text(
            "Buscar   •   Insertar   •   Eliminar",
            font_size=25
        )

        operaciones.next_to(
            titulo,
            DOWN,
            buff=0.45
        )

        promedio = Text(
            "Tiempo esperado:  O(log n)",
            font_size=33,
            color=GREEN
        )

        promedio.next_to(
            operaciones,
            DOWN,
            buff=0.45
        )

        peor = Text(
            "Peor caso: O(n)",
            font_size=23,
            color=YELLOW
        )

        peor.next_to(
            promedio,
            DOWN,
            buff=0.35
        )

        espacio = Text(
            "Espacio esperado: O(n)",
            font_size=22,
            color=GRAY_B
        )

        espacio.next_to(
            peor,
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(titulo),
            run_time=0.4
        )

        self.play(
            FadeIn(operaciones),
            run_time=0.4
        )

        self.play(
            Write(promedio),
            run_time=0.6
        )

        self.play(
            FadeIn(peor),
            FadeIn(espacio),
            run_time=0.5
        )

        self.wait(4)

        # --------------------------------------------------
        # RESUMEN FINAL
        # --------------------------------------------------

        self.play(
            FadeOut(titulo),
            FadeOut(operaciones),
            FadeOut(promedio),
            FadeOut(peor),
            FadeOut(espacio),
            run_time=0.6
        )

        resumen = Text(
            "Skip List",
            font_size=42,
            color=BLUE_B
        )

        resumen.move_to([
            0,
            1.35,
            0
        ])

        resumen2 = Text(
            "Orden + niveles + saltos probabilísticos",
            font_size=25
        )

        resumen2.next_to(
            resumen,
            DOWN,
            buff=0.4
        )

        resumen3 = Text(
            "Implementación C++  •  Eventos CSV  •  Animación Manim",
            font_size=21,
            color=GRAY_B
        )

        resumen3.next_to(
            resumen2,
            DOWN,
            buff=0.35
        )

        final = Text(
            "Fin",
            font_size=28,
            color=GREEN
        )

        final.next_to(
            resumen3,
            DOWN,
            buff=0.6
        )

        self.play(
            FadeIn(resumen),
            run_time=0.4
        )

        self.play(
            FadeIn(resumen2),
            FadeIn(resumen3),
            run_time=0.5
        )

        self.play(
            FadeIn(final),
            run_time=0.3
        )

        self.wait(3.5)
