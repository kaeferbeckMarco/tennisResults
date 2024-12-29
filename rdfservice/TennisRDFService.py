from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import FOAF
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef
from pyvis.network import Network
import os
import networkx as nx
import matplotlib.pyplot as plt

class TennisRDFService:


    def visualize_knowledge_graph_in_notebook(self,rdf_graph):
        # Create a directed graph in NetworkX
        nx_graph = nx.DiGraph()

        # Add RDF triples to the NetworkX graph
        for subj, pred, obj in rdf_graph:
            # Simplify labels for display
            subj_label = subj.split('/')[-1]
            pred_label = pred.split('/')[-1]
            obj_label = obj.split('/')[-1] if isinstance(obj, URIRef) else obj

            # Add nodes and edges with labels
            nx_graph.add_node(subj_label)
            nx_graph.add_node(obj_label)
            nx_graph.add_edge(subj_label, obj_label, label=pred_label)

        # Plot the graph
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(nx_graph)  # Positioning for clarity

        # Draw nodes and edges
        nx.draw(nx_graph, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')

        # Draw edge labels
        edge_labels = {(u, v): d['label'] for u, v, d in nx_graph.edges(data=True)}
        nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_size=9)

        plt.title("Knowledge Graph Visualization")
        plt.show()

    def visualize_knowledge_graph(self,rdf_graph):

        net = Network(height="750px", width="100%", directed=True)
        for subj, pred, obj in rdf_graph:
            subj_label = str(subj).split("/")[-1]
            pred_label = str(pred).split("/")[-1]
            obj_label = str(obj).split("/")[-1] if isinstance(obj, URIRef) else str(obj)

            net.add_node(subj_label, label=subj_label, title=str(subj))
            net.add_node(obj_label, label=obj_label, title=str(obj))
            net.add_edge(subj_label, obj_label, title=pred_label)

        # Save the visualization to the templates directory
        output_path = os.path.join("webservice","templates", "knowledge_graph.html")
        net.write_html(output_path)

    def create_player_knowledge_graph(self,player_uri):
        """
        Queries DBpedia for player information and constructs an RDF knowledge graph with tennis-related details.

        :param player_uri: The DBpedia URI for the player
        :return: RDF knowledge graph
        """
        graph = Graph()
        dbo = Namespace("http://dbpedia.org/ontology/")
        ex = Namespace("http://example.org/tennis/")
        graph.bind("dbo", dbo)
        graph.bind("foaf", FOAF)
        graph.bind("ex", ex)

        sparql = SPARQLWrapper("https://dbpedia.org/sparql")

        detail_query = f"""
        SELECT ?birthDate ?birthPlace ?height ?singlesTitles ?doublesTitles ?highestSinglesRanking ?highestDoublesRanking WHERE {{
          <{player_uri}> dbo:birthDate ?birthDate .
          OPTIONAL {{ <{player_uri}> dbo:birthPlace ?birthPlace }}
          OPTIONAL {{ <{player_uri}> dbo:height ?height }}
          OPTIONAL {{ <{player_uri}> dbo:singlesTitles ?singlesTitles }}
          OPTIONAL {{ <{player_uri}> dbo:doublesTitles ?doublesTitles }}
          OPTIONAL {{ <{player_uri}> dbo:highestSinglesRanking ?highestSinglesRanking }}
          OPTIONAL {{ <{player_uri}> dbo:highestDoublesRanking ?highestDoublesRanking }}
        }}
        """

        sparql.setQuery(detail_query)
        sparql.setReturnFormat(JSON)

        try:
            results = sparql.query().convert()
            print("Detail query results:", results)

            player_node = URIRef(player_uri)

            for result in results["results"]["bindings"]:
                if "name" in result:
                    graph.add((player_node, FOAF.name, Literal(result["name"]["value"])))
                if "birthDate" in result:
                    graph.add((player_node, dbo.birthDate, Literal(result["birthDate"]["value"])))
                if "birthPlace" in result:
                    graph.add((player_node, dbo.birthPlace, URIRef(result["birthPlace"]["value"])))
                if "height" in result:
                    graph.add((player_node, dbo.height, Literal(float(result["height"]["value"]))))
                if "singlesTitles" in result:
                    graph.add((player_node, ex.singlesTitles, Literal(int(result["singlesTitles"]["value"]))))
                if "doublesTitles" in result:
                    graph.add((player_node, ex.doublesTitles, Literal(int(result["doublesTitles"]["value"]))))
                if "highestSinglesRanking" in result:
                    graph.add((player_node, ex.highestSinglesRanking, Literal(int(result["highestSinglesRanking"]["value"]))))
                if "highestDoublesRanking" in result:
                    graph.add((player_node, ex.highestDoublesRanking, Literal(int(result["highestDoublesRanking"]["value"]))))
        except Exception as e:
            print(f"Error querying DBpedia for {player_uri}: {e}")

        return graph
