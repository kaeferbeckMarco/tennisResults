from flask import Flask, render_template
from domain.TennisDomainService import TennisServerDomainService

class TennisServerFlaskService:
    app = Flask(__name__)

    def __init__(self):
        self.domain = TennisServerDomainService()

    @staticmethod
    @app.route("/")
    def index():
        return render_template("index.html")

    @staticmethod
    @app.route("/tournaments")
    def tournaments():
        domain = TennisServerDomainService()
        tourneys = domain.get_tournaments()
        return render_template("tournament.html", tournaments=tourneys)

    @staticmethod
    @app.route("/<tourney_id>/matches")
    def matches(tourney_id):
        domain = TennisServerDomainService()
        matches = domain.get_matches(tourney_id)
        return render_template("matches.html", matches=matches)

    @staticmethod
    @app.route("/player/<player_name>")
    def player_graph(player_name):
        domain = TennisServerDomainService()
        formatted_name = player_name.replace(" ", "_")
        dbpedia_uri = f"http://dbpedia.org/resource/{formatted_name}"
        rdf_graph = domain.create_player_knowledge_graph(dbpedia_uri)
        domain.visualize_knowledge_graph(rdf_graph)
        return render_template("knowledge_graph.html")

    def run(self):
        self.domain.create_and_populate_database()
        self.app.run(host='localhost', port=8080, debug=True, use_reloader=True)