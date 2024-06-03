from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_note_graph(self, title, nodes):
        with self.driver.session() as session:
            session.write_transaction(self._create_note_graph, title, nodes)

    @staticmethod
    def _create_note_graph(tx, title, nodes):
        tx.run("CREATE (n:Note {title: $title})", title=title)
        for node in nodes:
            tx.run("CREATE (m:Node {label: $label})", label=node["label"])
            tx.run("MATCH (n:Note {title: $title}), (m:Node {label: $label}) "
                   "CREATE (n)-[:CONTAINS]->(m)", title=title, label=node["label"])

    def get_note_graph(self, title):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_note_graph, title)
            return result

    @staticmethod
    def _get_note_graph(tx, title):
        result = tx.run("MATCH (n:Note {title: $title})-[:CONTAINS]->(m:Node) "
                        "RETURN n.title AS title, collect(m.label) AS nodes", title=title)
        return result.single()
