# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.20.2",
#     "matplotlib>=3.10.8",
#     "numpy>=2.4.3",
#     "pyzmq>=27.1.0",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""
    # <p style="text-align: center;">Material adicional práctico de AnSyS e IPS #1</p>
    ### <p style="text-align: center;">Santiago Rodríguez</p>
    #### <p style="text-align: center;">Facultad de Ingeniería - UNLP</p>
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Desplazamiento y escalamiento de una SVIC
    Considere la transformación lineal $x(at+b)$. Experimente como la señal $x(t) = \sqcap (t)$ varía según la transformación aplicada.

    * Varíe los parámetros $a$ y $b$ con los deslizadores para descubir como resulta la transformación.

    * Para invertir el valor de $a$ y experimentar la reflexión, tilde la casilla "invertir signo de $a$".
    """)
    return


@app.cell
def _(mo):
    slider_a = mo.ui.slider(0.5, 2, value = 1, step=0.1, debounce=True)
    slider_b = mo.ui.slider(-2, 2, value=0, step=0.25, debounce=True)
    invertir_a = mo.ui.checkbox(label="Invertir signo de $a$")

    mo.vstack([
        mo.hstack([
            mo.vstack([mo.md(r"$a$:"), slider_a]),
            mo.vstack([mo.md(r"$b$:"), slider_b])
        ], justify="space-around"),
        invertir_a
    ])
    return invertir_a, slider_a, slider_b


@app.cell
def _(FONT_SIZE, cajon, invertir_a, plot_completo, plt, slider_a, slider_b, t):
    # Valor efectivo de a
    a_efectivo = slider_a.value * (-1 if invertir_a.value else 1)

    caj = cajon(a_efectivo*t+slider_b.value)

    plot_completo(t, caj, maximize=True, axis_limits=[-6, 6, -1, 2],font_size=FONT_SIZE,
                  xlabel='$t$', ylabel='$\sqcap(at+b)$', title='Transformaciones de la VIC',
                  line_style='r.-', line_width=2, marker_size=3)
    plt.legend(['$\sqcap('+ str(a_efectivo) + 't+' + str(slider_b.value) + ')$ = $\sqcap('+ str(a_efectivo) + '(t+' + f"{slider_b.value / a_efectivo:.1f}" + ')$)' ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Manejo de señales VIC
    * Una vez realizado el ejercicio 2) de la P1, pueden verificarse los resultados del trabajo realizado en papel seleccionando los diferentes incisos del menú desplegable.
    * Modifique los límites de los ejes de abscisas y ordenadas para observar adecuadamente cada transformación.
    """)
    return


@app.cell
def _(escalon, mo, tri1):
    opciones = {
        "a) h(t+1)": lambda t: tri1(t + 1),
        "b) h(2t-3)": lambda t: tri1(2*t - 3),
        "c) 2h(-0.5(t+10))": lambda t: 2 * tri1(-0.5*(t + 10)),
        "d) h(t/2)[u(t+2)-u(t-2)]": lambda t: tri1(t/2)*(escalon(t+2)-escalon(t-2)),
        "e) h(t^2)": lambda t: tri1(t**2),
        "f) Impar{h(t)}": lambda t: (tri1(t) - tri1(-t)) / 2,
        "g) Par{h(t)}": lambda t: (tri1(t) + tri1(-t)) / 2,
    }

    dropdown = mo.ui.dropdown(options=opciones, value="a) h(t+1)")
    dropdown

    # Control para límites del eje t (rango completo de -20 a 20)
    t_range = mo.ui.range_slider(
        start=-20, stop=20, step=1, value=(-20, 20),
        label="Límites eje t", full_width=False
    )

    # Controles para límites del eje y
    y_min = mo.ui.number(start=-10, stop=10, step=0.5, value=-2, label="y mín")
    y_max = mo.ui.number(start=-10, stop=10, step=0.5, value=4, label="y máx")

    # Mostramos los controles en una fila
    mo.hstack([dropdown, t_range, y_min, y_max], justify="space-around")
    return dropdown, opciones, t_range, y_max, y_min


@app.cell
def _(
    FONT_SIZE,
    dropdown,
    opciones,
    plot_completo,
    plt,
    t,
    t_range,
    x,
    y_max,
    y_min,
):
    # Etiquetas LaTeX
    etiquetas_latex = {
        "a) h(t+1)": "$h(t+1)$",
        "b) h(2t-3)": "$h(2t-3)$",
        "c) 2h(-0.5(t+10))": "$2h(-0.5(t+10))$",
        "d) h(t/2)[u(t+2)-u(t-2)]": "$h(t/2)[u(t+2) - u(t-2)]$",
        "e) h(t^2)": "$h(t^2)$",
        "f) Impar{h(t)}": "$\\operatorname{Impar}\\{h(t)\\}$",
        "g) Par{h(t)}": "$\\operatorname{Par}\\{h(t)\\}$",
    }

    # Crear mapeo inverso: función -> clave (etiqueta)
    funcion_a_clave = {v: k for k, v in opciones.items()}

    # Obtener función seleccionada y calcular xa
    funcion_seleccionada = dropdown.value
    xa = funcion_seleccionada(t)

    # Obtener la clave correspondiente a la función seleccionada
    clave_seleccionada = funcion_a_clave[funcion_seleccionada]

    # Obtener etiqueta LaTeX
    etiqueta_latex = etiquetas_latex[clave_seleccionada]

    # Límites seleccionados
    t_min, t_max = t_range.value
    y_lim_inf = y_min.value
    y_lim_sup = y_max.value

    # Graficar
    plot_completo(t, x, maximize=True, line_style='b--', line_width=2, font_size=FONT_SIZE)
    plot_completo(t, xa, hold=True, axis_limits=[t_min, t_max, y_lim_inf, y_lim_sup],
                  font_size=FONT_SIZE, xlabel='$t$', ylabel=etiqueta_latex,
                  title='Ej 2 - P1', line_style='r.-', line_width=2, marker_size=3)

    # Leyenda: usamos las mismas etiquetas LaTeX
    plt.legend(['$h(t)$', etiqueta_latex])
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    ##import funciones.utils
    from public.utils import tri1, escalon, cajon, plot_completo

    # Definiciones del script
    dt = 1e-3
    t = np.linspace(-20, 20, int(40/dt) + 1)
    x = tri1(t)
    FONT_SIZE = 25
    return FONT_SIZE, cajon, escalon, mo, plot_completo, plt, t, tri1, x


if __name__ == "__main__":
    app.run()
