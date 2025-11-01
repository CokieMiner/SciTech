import matplotlib
matplotlib.use("TkAgg")
import igraph as ig  # type: ignore
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from typing import Optional, List, Any


def plot_graph(
    df_pontos: pd.DataFrame,
    df_ruas: pd.DataFrame,
    fig: Optional[Figure] = None,
    route_log: Optional[List[Any]] = None,
) -> Figure:
    """
    Plots the graph using matplotlib and returns the figure.
    """
    if fig is None:
        fig = plt.figure(figsize=(10, 10))

    ax = fig.add_subplot(111)

    # Extract data
    pontos_de_origem = df_ruas["ponto_origem"].tolist()
    pontos_de_destino = df_ruas["ponto_destino"].tolist()
    tempo_transporte = df_ruas["tempo_transporte"].tolist()
    nomes = df_pontos["nome"].tolist()
    prioridades = df_pontos["prioridade"].tolist()
    tempo_cuidados_minimos = df_pontos["tempo_cuidados_minimos"].tolist()
    tipo = df_pontos["tipo"].tolist()

    # Create graph
    g = ig.Graph()
    g.add_vertices(len(df_pontos))
    pares_partida_chegada = list(zip(pontos_de_origem, pontos_de_destino))
    g.add_edges(pares_partida_chegada)
    g.es["weight"] = tempo_transporte

    # Edge labels
    labels_das_arestas = [f"{t}" for t in tempo_transporte]
    max_tempo = max(tempo_transporte) if tempo_transporte else 1

    # Vertex labels
    labels_vertices = []
    for i, _ in enumerate(nomes):
        if tipo[i] != "hospital":
            labels_vertices.append(f"{i}-CM: {tempo_cuidados_minimos[i]}m")
        else:
            labels_vertices.append(f"{i}")

    # Edge widths
    larguras_visuais = [t / max_tempo * 8 for t in tempo_transporte]

    # Vertex colors based on priority and route
    cmap = plt.get_cmap("viridis")
    norm = mpl.colors.Normalize(vmin=min(prioridades), vmax=max(prioridades))
    cores_dos_vertices = []

    # Create set of visited patients for highlighting
    visited_patients = set()
    if route_log:
        visited_patients = {step["to_patient"] for step in route_log}

    for i, prioridade in enumerate(prioridades):
        if tipo[i] != "hospital":
            if route_log and f"P{i:03d}" in visited_patients:
                cores_dos_vertices.append("orange")  # Highlight visited patients
            else:
                cores_dos_vertices.append(cmap(norm(prioridade)))
        else:
            cores_dos_vertices.append("red")

    # Layout
    layout = g.layout("fr")

    # Plot
    ig.plot(
        g,
        target=ax,
        layout=layout,
        vertex_size=15,
        vertex_color=cores_dos_vertices,
        vertex_label=labels_vertices,
        vertex_label_dist=2.5,
        vertex_label_degree=-np.pi / 4,
        vertex_label_size=10,
        edge_width=larguras_visuais,
        edge_color="gray",
        edge_label=labels_das_arestas,
        edge_font_size=8,
        edge_curved=False,
        edge_label_position=0.25,
        edge_label_color="black",
    )

    ax.set_title("Grafo", fontsize=16)
    ax.set_xticks([])
    ax.set_yticks([])

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', label='Prioridade')

    return fig


def create_canvas(
    parent: tk.Widget,
    df_pontos: pd.DataFrame,
    df_ruas: pd.DataFrame,
    route_log: Optional[List[Any]] = None,
) -> FigureCanvasTkAgg:
    """
    Creates a matplotlib canvas embedded in tkinter.
    """
    fig = plot_graph(df_pontos, df_ruas, route_log=route_log)
    canvas = FigureCanvasTkAgg(fig, master=parent)
    return canvas


# Example usage (for testing)
if __name__ == "__main__":
    # Hardcoded for testing
    df_pontos = pd.read_csv(
        "/home/pedrom/Documentos/SciTech/SciTech/Docs/Dataset de Test/datasets/hard/10/pontos.csv"
    )
    df_ruas = pd.read_csv(
        "/home/pedrom/Documentos/SciTech/SciTech/Docs/Dataset de Test/datasets/hard/10/ruas.csv"
    )
    fig = plot_graph(df_pontos, df_ruas)
    plt.show()
