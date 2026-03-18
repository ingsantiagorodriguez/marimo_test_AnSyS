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
    # <p style="text-align: center;">Material adicional práctico de AnSyS e IPS #2</p>
    ### <p style="text-align: center;">Santiago Rodríguez</p>
    #### <p style="text-align: center;">Facultad de Ingeniería - UNLP</p>
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Energía y potencia de SVID y SVIC
    En este ejercicio calcularemos la energía y potencia, siempre que ambas sean finitas, para las señales del ejercicio 5 de la P1 utilizando python.
    Comenzaremos por las SVIDS, ya que las definiciones son más simples.

    ## Caso SVID:

    Para una SVID, su energía es $E = \sum_{n=-\infty}^{\infty} |x[n]|^{2}$

    * Para estimar en python la energía de una señal discreta, tendremos que hacer una aproximación, ya que no tenemos la secuencia de $-\infty$ a $\infty$.

    Entonces:
    $$
    \begin{equation*}
    E = \sum_{n=-\infty}^{\infty} |x[n]|^{2} \approx \sum_{n=N_1}^{N_2} |x[n]|^{2}
    \end{equation*}
    $$

    Para la potencia, que se define como $P = \lim_{N \to \infty} \frac{1}{2N+1} \sum_{n=-N}^{N} |x[n]|^{2}$, también tendremos que hacer la misma aproximación.

    Entonces:
    $$
    \begin{equation*}
    P = \lim_{N \to \infty} \frac{1}{2N+1} \sum_{n=-N}^{N} |x[n]|^{2} \approx \frac{1}{N_2 - N_1} \sum_{n=N_1}^{N_2} |x[n]|^{2}
    \end{equation*}
    $$

    * Si la secuencia es periódica (de período $N$), el cálculo, que se puede resolver de **forma exacta**, cambia a:
    $$
    \begin{equation*}
    P = \frac{1}{N}\sum_{n=0}^{N-1} |x[n]|^{2}
    \end{equation*}
    $$

    ## Caso SVIC:

    Para una SVIC, su energía es $E = \int_{-\infty}^{\infty} |x(t)|^{2} \, dt$.

    * Para estimar en python la energía de una señal continua, tendremos que hacer aproximaciones.
    * Por un lado, aproximaremos la integral con una suma de Riemann.
    * Para ello, consideraremos en realidad una señal $x[n]$, que ha sido creada a partir de discretizar la señal continua cada $T_s$ segundos.
    * Por otra parte, consideraremos que tenemos suficientes puntos de la señal, ya que no es posible tener puntos desde $-\infty$ a $\infty$.

    Entonces:
    $$
    \begin{equation*}
    E = \int_{-\infty}^{\infty} |x(t)|^{2} \, dt \approx \sum_{n = N_1}^{N_2} |x[n]|^{2} \, Ts
    \end{equation*}
    $$

    En cuanto a su potencia, la misma es $P = \lim_{T \to \infty} \frac{1}{2T} \int_{-T}^{T} |x(t)|^{2} \, dt$.

    * Así como con la energía, también habrá que hacer aproximaciones para calcular la potencia de una señal continua en python.
    * Primeramente, tendremos que quitar el límite y solamente considerar los puntos contemplados en la señal.
    * Nuevamente se aproximará la integral con una suma de Riemann.
    * Consideraremos que en realidad contamos con un vector discreto $x[n]$ que fue obtenido observando la $x(t)$ cada $T_s$ segundos.

    Entonces:

    $$
    \begin{equation*}
    P = \lim_{T \to \infty} \frac{1}{2T} \int_{-T}^{T} |x(t)|^{2} \, dt \approx \frac{1}{N_2-N_1} \sum_{n=N_1}^{N_2} |x[n]|^{2} \, Ts
    \end{equation*}
    $$

    Finalmente, si la señal es periódica (de período $T_0$), sabemos que su energía será $\infty$, y su potencia podremos calcularla y estimarla de la siguiente manera:

    $$
    \begin{equation*}
    P = \frac{1}{T_{0}} \int_{T_{0}} |x(t)|^{2} \, dt \approx \frac{1}{T_{0}} \sum_{n=0}^{[T_0 / T_s]-1} |x[n]|^{2} \, Ts
    \end{equation*}
    $$

    ## Conclusiones:

    * Debe tenerse en cuenta que al no poder generar señales de $-\infty$ a $\infty$, lo que calcularemos **siempre** será una aproximación.
    * Para señales continuas además tendremos que discretizar la variable independiente $t$ utilizando un paso $T_s$ (convenientemente pequeño).
    * Si las aproximaciones son adecuadas, los resultados obtenidos por las estimaciones denerían ser similares a los obtenidos *a mano*.
    """)
    return


@app.cell
def _(escalon, mo, np):
    from numpy import pi
    opciones = {
        "i) u(t)": lambda t: escalon(t),
        "ii) 4 sen(2πt + π/3)": lambda t: 4*np.sin(2*pi*t + pi/3),
        "iii) 2 e^{j6π t}": lambda t: 2*np.exp(6j*pi*t),
        "iv) (0.5)^n u[n]": lambda n: ((0.5)**n)*escalon(n),
        "v) ∑ 3 δ[n - 3k]": lambda n: 3.0*(n % 3 == 0),
    }

    dropdown = mo.ui.dropdown(options=opciones, value="i) u(t)")

    # Control para límites del eje t (rango completo de -20 a 20)
    t_range = mo.ui.range_slider(
        start=-40, stop=40, step=1, value=(-5, 5),
        label="Límites abscisas", full_width=False
    )

    # Controles para límites del eje y
    y_min = mo.ui.number(start=-10, stop=10, step=0.5, value=-2, label="y mín")
    y_max = mo.ui.number(start=-10, stop=10, step=0.5, value=4, label="y máx")

    # Mostramos los controles en una fila
    mo.hstack([dropdown, t_range, y_min, y_max], justify="center", align="stretch")
    return dropdown, opciones, t_range, y_max, y_min


@app.cell
def _(mo):
    mo.md(r"""
    ## Visualización y cálculos (aproximados) de energía, potencia y valor medio
    """)
    return


@app.cell
def _(
    FONT_SIZE,
    dropdown,
    mo,
    np,
    opciones,
    panel_resultados,
    plot_completo,
    plt,
    stem_completo,
    t_range,
    y_max,
    y_min,
):
    # Definir tipos de señal (continua o discreta)
    from matplotlib.pylab import plot
    tipos = {
        "i) u(t)": "continua",
        "ii) 4 sen(2πt + π/3)": "continua",
        "iii) 2 e^{j6π t}": "continua",
        "iv) (0.5)^n u[n]": "discreta",
        "v) ∑ 3 δ[n - 3k]": "discreta",
    }

    # Obtener valores actuales de los controles
    clave_seleccionada = dropdown.selected_key  # clave del dropdown
    t_min, t_max = t_range.value
    y_min_val = y_min.value
    y_max_val = y_max.value
    funcion = opciones[clave_seleccionada]  # función correspondiente
    tipo = tipos[clave_seleccionada]

    if tipo == "continua":
        # Generar vector de tiempo continuo en el intervalo seleccionado
        num_puntos = 3000
        t = np.linspace(t_min, t_max, num_puntos)
        dt = t[1] - t[0]
        x = funcion(t)

        # Cálculos aproximados (sobre el intervalo mostrado)
        energia = np.sum(np.abs(x)**2) * dt
        potencia = np.sum(np.abs(x)**2) * dt / (t_max - t_min)
        valor_medio = np.sum(x) * dt / (t_max - t_min)

        # Preparar texto de resultados
        if np.iscomplexobj(x):
            panel = panel_resultados(
                f"Resultados para t ∈ [{t_min:.2f}, {t_max:.2f}]",
                [
                ("Energía", f"{energia:.4f}"),
                ("Potencia media", f"{potencia:.4f}"),
                ("Valor medio", f"{valor_medio.real:.4f} + {valor_medio.imag:.4f}j"),
                ]
            )
            # Gráfica: parte real e imaginaria
            fig = plot_completo(t, np.real(x), maximize=True, axis_limits=[t_min, t_max, y_min_val, y_max_val],
            font_size=FONT_SIZE, xlabel='$t$',
            title='Ej 5 - P1', line_style='r', line_width=2, marker_size=3)
            plot_completo(t, np.imag(x), hold=True, maximize=True, axis_limits=[t_min, t_max, y_min_val, y_max_val],
            font_size=FONT_SIZE, xlabel='$t$',
            title='Ej 5 - P1', line_style='b', line_width=2, marker_size=3)
            plt.legend(['Real','Imag'])
        else:
            panel = panel_resultados(
            f"Resultados para t ∈ [{t_min:.2f}, {t_max:.2f}]",
            [
                ("Energía", f"{energia:.4f}"),
                ("Potencia media", f"{potencia:.4f}"),
                ("Valor medio", f"{valor_medio.real:.4f} + {valor_medio.imag:.4f}j"),
                ]
            )
            fig = plot_completo(t, x, maximize=True, axis_limits=[t_min, t_max, y_min_val, y_max_val],
            font_size=FONT_SIZE, xlabel='$t$',
            title='Ej 5 - P1', line_style='b', line_width=2, marker_size=3)
            plt.legend([clave_seleccionada])

    else:  # señal discreta
        # Convertir rango de tiempo a índices enteros
        n_min = int(np.floor(t_min))
        n_max = int(np.ceil(t_max))
        n = np.arange(n_min, n_max + 1)
        x = funcion(n)

        # Cálculos aproximados
        energia = np.sum(np.abs(x)**2)
        potencia = np.mean(np.abs(x)**2)
        valor_medio = np.mean(x)

        # Preparar texto de resultados
        if np.iscomplexobj(x):
            panel = panel_resultados(
                f"Resultados para n ∈ [{n_min}, {n_max}]",
                [
                ("Energía", f"{energia:.4f}"),
                ("Potencia media", f"{potencia:.4f}"),
                ("Valor medio", f"{valor_medio.real:.4f} + {valor_medio.imag:.4f}j"),
                ]
            )
            fig = stem_completo(n, np.real(x), maximize=True, axis_limits=[t_min, t_max, y_min_val, y_max_val],
            font_size=FONT_SIZE, xlabel='$n$',
            title='Ej 5 - P1', line_style='r', line_width=2, marker_size=3)
            plot_completo(n, np.imag(x), hold=True, maximize=True, axis_limits=[t_min, t_max, y_min_val, y_max_val],
            font_size=FONT_SIZE, xlabel='$n$',
            title='Ej 5 - P1', line_style='b', line_width=2, marker_size=3)
            plt.legend(['Real','Imag'])
        else:
            panel = panel_resultados(
                f"Resultados para n ∈ [{n_min}, {n_max}]",
                [
                ("Energía", f"{energia:.4f}"),
                ("Potencia media", f"{potencia:.4f}"),
                ("Valor medio", f"{valor_medio.real:.4f} + {valor_medio.imag:.4f}j"),
                ]
            )
            fig = stem_completo(n, x, maximize=True, axis_limits=[t_min, t_max, y_min_val, y_max_val],
            font_size=FONT_SIZE, xlabel='$n$',
            title='Ej 5 - P1', line_style='b', line_width=2, marker_size=3)
            plt.legend([clave_seleccionada])

    # Mostrar gráfica y resultados en una fila
    #mo.hstack([mo.as_html(fig), mo.md(resultados)], justify="start")
    mo.hstack([mo.as_html(fig), panel], justify="center", gap=5)
    return


@app.cell
def _(mo):
    # Función helper para generar el panel de resultados con HTML estilizado
    def panel_resultados(titulo, items):
        filas = ""
        for label, valor in items:
            filas += f"""
            <tr>
                <td style="padding: 10px 18px; font-size: 16px; color: #aaaaaa; font-weight: 500;">{label}</td>
                <td style="padding: 10px 18px; font-size: 18px; color: #ffffff; font-weight: 700; text-align: right;">{valor}</td>
            </tr>
            """
        return mo.Html(f"""
        <div style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 24px 32px;
            background: #1e1e1e;
            border-radius: 12px;
            border: 1px solid #333;
            min-width: 320px;
            height: 100%;
            box-sizing: border-box;
        ">
            <div style="
                font-size: 17px;
                font-weight: 700;
                color: #e0e0e0;
                margin-bottom: 20px;
                padding-bottom: 12px;
                border-bottom: 1px solid #444;
                letter-spacing: 0.3px;
            ">{titulo}</div>
            <table style="border-collapse: collapse; width: 100%;">
                {filas}
            </table>
        </div>
        """)

    return (panel_resultados,)


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from public.utils import escalon, plot_completo, stem_completo

    FONT_SIZE = 25
    return FONT_SIZE, escalon, mo, np, plot_completo, plt, stem_completo


if __name__ == "__main__":
    app.run()
