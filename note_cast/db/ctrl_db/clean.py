from neomodel import db

def delete_all_nodes():
    results, meta = db.cypher_query("MATCH (p:Podcast) DETACH DELETE (p)")
    results, meta = db.cypher_query("MATCH (e:Episode) DETACH DELETE (e)")
    results, meta = db.cypher_query("MATCH (q:Quote) DETACH DELETE (q)")
    results, meta = db.cypher_query("MATCH (u:User) DETACH DELETE (u)")
    results, meta = db.cypher_query("MATCH (n:Note) DETACH DELETE (n)")
    results, meta = db.cypher_query("MATCH (c:Category) DETACH DELETE (c)")