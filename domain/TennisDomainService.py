from persistence.TennisServerPersitencyService import TennisServerPersitencyService
from rdfservice.TennisRDFService import TennisRDFService


class TennisServerDomainService:

    def __init__(self):
        self.repository = TennisServerPersitencyService()
        self.rdf_service = TennisRDFService()

    def get_matches(self, tourney_id):
        return self.repository.load_matches(tourney_id)

    def get_tournaments(self):
        return self.repository.load_tournaments()


    def create_and_populate_database(self):
        self.repository.create_database()
        self.repository.populate_database_with_csv_data()


    def create_player_knowledge_graph(self, dbpedia_uri):
        return self.rdf_service.create_player_knowledge_graph(dbpedia_uri)

    def visualize_knowledge_graph(self, rdf_graph):
        return self.rdf_service.visualize_knowledge_graph(rdf_graph)

    def visualize_knowledge_graph_in_notebook(self, rdf_graph):
        return self.rdf_service.visualize_knowledge_graph_in_notebook(rdf_graph)




