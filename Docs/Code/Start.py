import pandas as pd
import igraph
from typing import Optional, Dict, Any

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """Load data from a CSV file into a pandas DataFrame."""
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")
        return data
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
        return None

def pd_to_igraph(data: pd.DataFrame) -> Optional[igraph.Graph]:
    """
    Convert DataFrame to directed igraph Graph with weights.
    Assumes columns: origin, dest, time.
    """
    try:
        graph = igraph.Graph(directed=True)
        # Add vertices based on max ID
        max_id = max(data['ponto_origem'].max(), data['ponto_destino'].max())
        graph.add_vertices(max_id + 1)
        graph.vs['name'] = [str(i) for i in range(max_id + 1)]  # Set names
        
        # Add edges with weights
        for _, row in data.iterrows():
            graph.add_edge(row['ponto_origem'], row['ponto_destino'], weight=row['tempo_transporte'])
        
        print("DataFrame converted to directed igraph Graph successfully.")
        return graph
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def add_points_data_to_graph(graph: igraph.Graph, data: pd.DataFrame) -> None:
    """
    DataFrame has 5 columns representing point attributes:
    - ID
    - Name
    - Type
    - Priority
    - Minimum Care Time
    """
    try:
        for index, row in data.iterrows():
            vertex_id = str(row[0])
            if vertex_id in graph.vs['name']:
                vertex_index = graph.vs.find(name=vertex_id).index
                graph.vs[vertex_index]['Name'] = row[1]
                graph.vs[vertex_index]['Type'] = row[2]
                graph.vs[vertex_index]['Priority'] = row[3]
                graph.vs[vertex_index]['Minimum_Care_Time'] = row[4]
        print("Point data added to igraph Graph successfully.")
    except Exception as e:
        print(f"An error occurred while adding point data to igraph: {e}")

def initial_data_df(file_path: str) -> pd.DataFrame:
    """
    Returns a DataFrame that has 2 columns representing initial data:
    - Starting Point
    - Total Time Available
    """
    df = pd.DataFrame(pd.read_csv(file_path))
    return df


def problem_data_df(input_folder: str) -> Dict[str, Any]:
    """
    Loads data and builds the full igraph Graph with attributes.
    Returns a dictionary with the graph, points data, and initial data.
    """
    # Load CSVs
    initial_data = pd.read_csv(f"{input_folder}/dados_iniciais.csv")
    points_data = pd.read_csv(f"{input_folder}/pontos.csv")
    edges_data = pd.read_csv(f"{input_folder}/ruas.csv")
    
    # Build graph
    graph = pd_to_igraph(edges_data)  # Now returns undirected graph
    add_points_data_to_graph(graph, points_data)
    
    return {
        "graph": graph,
        "points_data": points_data,
        "initial_data": initial_data
    }