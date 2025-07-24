import os
from neo4j import GraphDatabase
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from llm_client import extract_triples
from dotenv import load_dotenv

print("Loading environment variables...")
load_dotenv()

# Get credentials from environment variables
NEO4J_URI = "neo4j+s://7708e898.databases.neo4j.io"  # Replace <your-uri> with your AuraDB instance URI
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
print(f"NEO4J_URI: {NEO4J_URI}")
print(f"NEO4J_USERNAME: {NEO4J_USERNAME}")
print(f"NEO4J_PASSWORD: {'*' * len(NEO4J_PASSWORD) if NEO4J_PASSWORD else None}")

# Neo4j setup for AuraDB
try:
    print("Attempting to create Neo4j driver...")
    neo4j_driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )
    print("Neo4j driver created successfully.")
except Exception as e:
    print("Error creating Neo4j driver:", e)
    raise

# Store triples in Neo4j
def store_graph(triples):
    print("Storing triples in Neo4j:", triples)
    try:
        with neo4j_driver.session() as session:
            for src, rel, tgt in triples:
                print(f"Storing triple: ({src})-[{rel}]->({tgt})")
                session.run(
                    f"""
                    MERGE (a:Concept {{name: $src}})
                    MERGE (b:Concept {{name: $tgt}})
                    MERGE (a)-[r:`{rel.replace(' ', '_')}`]->(b)
                    """,
                    {"src": src, "tgt": tgt}
                )
        print("All triples stored successfully.")
    except Exception as e:
        print("Error storing triples:", e)
        raise

# Web server for graph visualization and note input
app = Flask(__name__)
print("Flask app created.")

@app.route("/", methods=["GET", "POST"])
def index():
    print("Accessed / route with method:", request.method)
    if request.method == "POST":
        note = request.form.get("note")
        print("Received note:", note)
        if note:
            try:
                print("Extracting triples from note...")
                triples = extract_triples(note)
                print("Extracted triples:", triples)
                store_graph(triples)
                print("Triplets stored in Neo4j.")
            except Exception as e:
                print("Error processing note:", e)
        else:
            print("No note received in POST request.")
        return redirect(url_for("index"))

    print("Rendering index page.")
    return render_template_string("""
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet"/>
    </head>
    <body>
    <h2>Second Brain Note Graph</h2>
    <form method="post">
        <textarea name="note" rows="4" cols="80" placeholder="Write a note here..."></textarea><br>
        <button type="submit">Add Note</button>
    </form>
    <hr>
    <div id="mynetwork" style="height: 600px;"></div>
    <script>
    fetch('/graph').then(res => res.json()).then(data => {
        var nodes = new vis.DataSet(data.nodes);
        var edges = new vis.DataSet(data.edges);
        var container = document.getElementById('mynetwork');
        var data = { nodes: nodes, edges: edges };
        var options = { nodes: { shape: 'dot', size: 16 }, edges: { arrows: 'to' } };
        new vis.Network(container, data, options);
    });
    </script>
    </body>
    </html>
    """)

@app.route("/graph")
def get_graph():
    print("Accessed /graph route.")
    try:
        with neo4j_driver.session() as session:
            print("Running Cypher query to get graph data...")
            result = session.run("MATCH (a)-[r]->(b) RETURN a.name AS source, TYPE(r) AS rel, b.name AS target")
            nodes = set()
            edges = []
            for row in result:
                print("Found relationship:", row)
                nodes.add(row["source"])
                nodes.add(row["target"])
                edges.append({"from": row["source"], "to": row["target"], "label": row["rel"]})
            print("Returning graph data as JSON.")
            return jsonify({
                "nodes": [{"id": n, "label": n} for n in nodes],
                "edges": edges
            })
    except Exception as e:
        print("Error fetching graph data:", e)
        return jsonify({"error": str(e)}), 500

# Run the web app
if __name__ == "__main__":
    print("Starting Flask app on port 5000...")
    app.run(debug=True, port=5000)