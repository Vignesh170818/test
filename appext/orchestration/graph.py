'''Method to get relevant business context for the given code'''
import asyncio
from pathlib import Path
from sre_constants import RANGE
from plugins.graphservice.controller import GenLiteGenerateGraph
from plugins.graphservice.model import GraphInput
from genliteappext.genliteform import GenLiteMainForm
from coreengine.neo4j.connection import Neo4jConnection
import pyvis
from neo4j import GraphDatabase
import neo4j

n4j = Neo4jConnection()

async def get_graph(form: GenLiteMainForm, serviceCode):
    '''Method to get design input'''
    graphsourcecodelang = form.code_language.data
    servicesCode = form.services_code.data
    uniqueName = form.unique_name.data
    llmplatform = form.llm_platform_options.data
    cypherquery = ''
    graphobject = GenLiteGenerateGraph(
        llmplatform=llmplatform
        )
    
    # for file in serviceCode:
    inputdict = GraphInput(
            graphsourcecodelang = graphsourcecodelang,
            graphsourcecode = servicesCode,
            uniqueId = uniqueName
            )
    cypherquery =  await asyncio.to_thread(graphobject.generate, inputdict)
    n4j.driver.execute_query(cypherquery, 
        database_="neo4j",
    )
        
    query = "MATCH p=()-->(n) where n.uniqueId= '" + uniqueName + "'"
    # for i in range(1,len(files)):
    #     query = query + "or n.uniqueId= '" + files[i]["filename"] + "'"
    query = query + " RETURN p"
    
     # Query to get a graphy result
    query_graph = n4j.driver.execute_query(query,
        result_transformer_=neo4j.Result.graph,
    )
    visual_graph = pyvis.network.Network()

    for node in query_graph.nodes:
        if node.labels:
            node_label = list(node.labels)[0]
            node_text = node._properties["name"]
            visual_graph.add_node(node.element_id, node_text, group=node_label)

    for relationship in query_graph.relationships:
        if relationship.start_node.labels and relationship.end_node.labels:
            visual_graph.add_edge(
                relationship.start_node.element_id,
                relationship.end_node.element_id,
                title=relationship.type
            )
    return  visual_graph 
