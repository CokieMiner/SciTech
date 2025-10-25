import pandas as pd
import igraph #type: ignore
from typing import Optional, Dict, Any
import unittest

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
        graph = igraph.Graph(directed=False)
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
        for _, row in data.iterrows():
            vertex_id = str(row['id'])
            if vertex_id in graph.vs['name']:
                vertex_index = graph.vs.find(name=vertex_id).index
                graph.vs[vertex_index]['Name'] = row['nome']
                graph.vs[vertex_index]['Type'] = row['tipo']
                graph.vs[vertex_index]['Priority'] = row['prioridade']
                graph.vs[vertex_index]['Minimum_Care_Time'] = row['tempo_cuidados_minimos']
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


def problem_data_dict(input_folder: str) -> Dict[str, Any]:
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






# ----------------------------------------------------  Test Cases -----------------------------------------------------------------------------------



class TestStart(unittest.TestCase):
    def test_load_data(self):
        df = load_data("/home/pedrom/Documentos/SciTech/Dataset de Test/datasets/hard/10/ruas.csv")
        self.assertIsNotNone(df)
        self.assertEqual(len(df.columns), 3)

    def test_pd_to_igraph(self):
        data = pd.DataFrame({'ponto_origem': [0, 1], 'ponto_destino': [1, 2], 'tempo_transporte': [1, 2]})
        graph = pd_to_igraph(data)
        self.assertIsNotNone(graph)
        self.assertEqual(graph.vcount(), 3)
        self.assertEqual(graph.ecount(), 2)

    def test_add_points_data_to_graph(self):
        graph = igraph.Graph(directed=True)
        graph.add_vertices(3)
        graph.vs['name'] = ['0', '1', '2']
        data = pd.DataFrame({'id': [0, 1], 'nome': ['A', 'B'], 'tipo': ['type1', 'type2'], 'prioridade': [10, 20], 'tempo_cuidados_minimos': [1, 2]})
        add_points_data_to_graph(graph, data)
        self.assertEqual(graph.vs[0]['Name'], 'A')

    def test_initial_data_df(self):
        df = initial_data_df("/home/pedrom/Documentos/SciTech/Dataset de Test/datasets/hard/10/dados_iniciais.csv")
        self.assertIsNotNone(df)
        self.assertEqual(df.iloc[0]['ponto_inicial'], 0)

    def test_problem_data_df(self):
        data = problem_data_dict("/home/pedrom/Documentos/SciTech/Dataset de Test/datasets/hard/10")
        self.assertIn('graph', data)
        self.assertIn('points_data', data)
        self.assertIn('initial_data', data)

    def test_show_hard_10_data(self):
        """Test that loads and displays the hard/10 dataset in the terminal."""
        data = problem_data_dict("/home/pedrom/Documentos/SciTech/Dataset de Test/datasets/hard/10")
        print("\n=== Hard/10 Dataset Summary ===")
        print(f"Graph: {data['graph'].vcount()} vertices, {data['graph'].ecount()} edges")
        print("Points Data:")
        print(data['points_data'].head())
        print("Initial Data:")
        print(data['initial_data'])
        # Always pass since it's for display
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()