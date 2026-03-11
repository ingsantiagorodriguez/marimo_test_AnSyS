import numpy as np
import matplotlib.pyplot as plt

# ---------- Funciones de señal ----------
def cajon(t):
    return 1.0 * ((t >= -0.5) & (t <= 0.5))

def tri(t):
    return (t+1) * ((t >= -1) & (t < 0)) + (-t + 1) * ((t >= 0) & (t <= 1))

def tri1(t):
    return (t+1) * ((t >= -1) & (t < 1)) + (-t + 3) * ((t >= 1) & (t < 3))

def escalon(t):
    return 1.0 * (t >= 0)

def sindSR(N, t):
    h = np.sin(N * np.pi * t) / (np.sin(np.pi * t) + 1e-15)
    h[np.abs(t) < 1e-15] = N
    return h

def triN(n, N):
    if N > 0:
        return (N - np.abs(n)) * ((n > -N) & (n < N))
    return 0

def triN_norm(n, N):
    if N > 0:
        return (1/N) * (N - np.abs(n)) * ((n > -N) & (n < N))
    return 0

# ---------- Funciones de trazado ----------
import matplotlib.pyplot as plt

def plot_completo(t, x, subplot=None, hold=False, maximize=False, axis_limits=None,
                  xlabel='', ylabel='', title='', font_size=20, line_style='b-',
                  line_width=1, marker_size=3, usetex=False, **kwargs):
    """
    Parámetros adicionales:
    usetex : bool, opcional
        Si es True, habilita LaTeX para renderizar todo el texto.
        Requiere tener LaTeX instalado en el sistema.
    """
    # Configurar LaTeX si se solicita (solo para esta gráfica)
    if usetex:
        plt.rcParams['text.usetex'] = True
        plt.rcParams['font.family'] = 'serif'
    else:
        plt.rcParams['text.usetex'] = False   # Volver al modo normal

    # ... (resto de tu función igual)
    new_figure = False
    if subplot is None:
        if not hold:
            new_figure = True
    else:
        if not hold:
            new_figure = True

    if new_figure:
        if maximize:
            plt.figure(figsize=(16, 10))
        else:
            plt.figure()

    if subplot is not None:
        if isinstance(subplot, (list, tuple)) and len(subplot) == 3:
            m, n, p = subplot
            plt.subplot(m, n, p)
        else:
            raise ValueError("subplot debe ser [m,n,p]")

    plt.plot(t, x, line_style, linewidth=line_width, markersize=marker_size, **kwargs)
    if axis_limits is not None:
        plt.xlim(axis_limits[0], axis_limits[1])
        plt.ylim(axis_limits[2], axis_limits[3])
    plt.grid(True)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if title:
        plt.title(title)
    plt.rcParams.update({'font.size': font_size})
    return plt.gca()

def stem_completo(n, x, subplot=None, hold=False, maximize=False, axis_limits=None,
                  xlabel='', ylabel='', title='', font_size=12,
                  color='auto', line_style='-', line_width=1,
                  marker='o', marker_size=6, filled=True, **kwargs):
    new_figure = False
    if subplot is None:
        if not hold:
            new_figure = True
    else:
        if not hold:
            new_figure = True
    if new_figure:
        if maximize:
            plt.figure(figsize=(16, 10))
        else:
            plt.figure()
    if subplot is not None:
        if isinstance(subplot, (list, tuple)) and len(subplot) == 3:
            m, n_sub, p = subplot
            plt.subplot(m, n_sub, p)
        else:
            raise ValueError("subplot debe ser [m,n,p]")

    if color == 'auto':
        color = None
    markerfmt = marker
    if color is not None:
        markerfmt = color + marker
    linefmt = '-' if line_style == '-' else line_style
    if color is not None:
        linefmt = color + linefmt
    markerline, stemlines, baseline = plt.stem(n, x, linefmt=linefmt,
                                                markerfmt=markerfmt, basefmt='k-')
    plt.setp(stemlines, linewidth=line_width)
    plt.setp(markerline, markersize=marker_size)
    if filled:
        if color is None:
            c = markerline.get_color()
            plt.setp(markerline, markerfacecolor=c, markeredgecolor=c)
        else:
            plt.setp(markerline, markerfacecolor=color, markeredgecolor=color)

    if axis_limits is not None:
        plt.xlim(axis_limits[0], axis_limits[1])
        plt.ylim(axis_limits[2], axis_limits[3])
    plt.grid(True)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if title:
        plt.title(title)
    plt.rcParams.update({'font.size': font_size})
    return plt.gca()

def hist_completo(axis_limits, xlabel, ylabel, title, font_size, data, bins):
    plt.hist(data, bins=bins, edgecolor='black')
    if axis_limits is not None:
        plt.xlim(axis_limits[0], axis_limits[1])
        plt.ylim(axis_limits[2], axis_limits[3])
    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.rcParams.update({'font.size': font_size})
    return plt.gca()

def plot_completo_semilog(axis_limits, xlabel, ylabel, title, font_size, color, line_width, t, x):
    plt.semilogx(t, x, color, linewidth=line_width)
    if axis_limits is not None:
        plt.xlim(axis_limits[0], axis_limits[1])
        plt.ylim(axis_limits[2], axis_limits[3])
    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.rcParams.update({'font.size': font_size})
    return plt.gca()