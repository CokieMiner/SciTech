# ambulance_routing.py
import pandas as pd
import igraph  # type: ignore
from typing import Dict, Any, List, Tuple, Optional
from .Data_Import import pd_to_igraph, add_points_data_to_graph  # type: ignore  # Usa o teu código original


def precompute_all_pairs_shortest_paths(
    graph: igraph.Graph,
) -> Tuple[Dict[Tuple[int, int], float], Dict[Tuple[int, int], List[int]]]:
    """
    Pré-calcula distâncias e caminhos mais curtos entre todos os pares de nós.
    """
    distances: Dict[Tuple[int, int], float] = {}
    paths: Dict[Tuple[int, int], List[int]] = {}

    for v in range(len(graph.vs)):
        spaths = graph.get_shortest_paths(v, to=None, weights="weight", output="vpath")
        for u, path in enumerate(spaths):
            if path:
                dist = sum(
                    graph.es[graph.get_eid(path[i], path[i + 1])]["weight"]
                    for i in range(len(path) - 1)
                )
            else:
                dist = float("inf")
            distances[(v, u)] = dist
            paths[(v, u)] = path
    return distances, paths


def select_next_patient_optimized(
    current_node: int,
    patients: pd.DataFrame,
    time_left: float,
    hospitals: List[int],
    distances: Dict[Tuple[int, int], float],
    paths: Dict[Tuple[int, int], List[int]],
) -> Optional[Tuple[int, List[int], List[int], float]]:
    """
    Seleciona o próximo paciente a socorrer usando a matriz pré-calculada.
    """
    candidates = []

    for _, patient in patients.iterrows():
        patient_id = patient["id"]
        if patient["tipo"].lower() != "paciente":
            continue

        dist_to_patient = distances.get((current_node, patient_id), float("inf"))

        # Hospital mais próximo
        min_return_dist = float("inf")
        best_path_to_hospital = []
        for hospital_id in hospitals:
            dist_back = distances.get((patient_id, hospital_id), float("inf"))
            if dist_back < min_return_dist:
                min_return_dist = dist_back
                best_path_to_hospital = paths.get((patient_id, hospital_id), [])

        total_time_needed = (
            dist_to_patient + patient["tempo_cuidados_minimos"] + min_return_dist
        )
        if total_time_needed <= time_left:
            candidates.append(
                (
                    patient_id,
                    paths[(current_node, patient_id)],
                    best_path_to_hospital,
                    total_time_needed,
                    patient["prioridade"],
                )
            )

    if not candidates:
        return None

    # Prioridade decrescente e menor tempo total
    candidates.sort(key=lambda x: (-x[4], x[3]))
    selected = candidates[0]
    return selected[0], selected[1], selected[2], selected[3]


def ambulance_routing_optimized(
    graph: igraph.Graph,
    points_data: pd.DataFrame,
    initial_point: int,
    total_time: float,
) -> List[Dict[str, Any]]:
    """
    Simula a operação da ambulância, retornando uma lista de trajetos realizados.
    """
    hospitals = points_data[points_data["tipo"].str.lower() == "hospital"][
        "id"
    ].tolist()
    patients = points_data[points_data["tipo"].str.lower() == "paciente"].copy()
    current_node = initial_point
    time_left = total_time
    route_log: List[Dict[str, Any]] = []

    distances, paths = precompute_all_pairs_shortest_paths(graph)

    while time_left > 0 and not patients.empty:
        next_task = select_next_patient_optimized(
            current_node, patients, time_left, hospitals, distances, paths
        )
        if not next_task:
            break

        patient_id, path_to_patient, path_to_hospital, total_time_needed = next_task

        route_log.append(
            {
                "from": current_node,
                "to_patient": patient_id,
                "path_to_patient": path_to_patient,
                "path_to_hospital": path_to_hospital,
                "time_needed": total_time_needed,
                "priority": points_data.loc[
                    points_data["id"] == patient_id, "prioridade"
                ].values[0],
            }
        )

        # Atualiza estado
        time_left -= total_time_needed
        current_node = path_to_hospital[-1]
        patients = patients[patients["id"] != patient_id]

    return route_log


def run_from_csv_optimized(input_folder: str) -> List[Dict[str, Any]]:
    """
    Função principal para rodar o algoritmo diretamente dos CSVs.
    """
    dados_iniciais = pd.read_csv(f"{input_folder}/dados_iniciais.csv")
    pontos_data = pd.read_csv(f"{input_folder}/pontos.csv")
    ruas_data = pd.read_csv(f"{input_folder}/ruas.csv")

    graph = pd_to_igraph(ruas_data)
    add_points_data_to_graph(graph, pontos_data)

    initial_point = dados_iniciais.iloc[0]["ponto_inicial"]
    total_time = dados_iniciais.iloc[0]["tempo_total"]

    return ambulance_routing_optimized(graph, pontos_data, initial_point, total_time)


if __name__ == "__main__":
    log = run_from_csv_optimized(
        "/home/pedrom/Documentos/SciTech/SciTech/Dataset de Test/datasets/hard/8"
    )
    for step in log:
        print(step)
