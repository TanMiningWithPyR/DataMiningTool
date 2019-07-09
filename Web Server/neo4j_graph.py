# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 15:45:21 2019

@author: Fuyou Tan
"""
import numpy as np
import pandas as pd
import os

from py2neo import Node, Relationship, Graph

class DataToNeo4j(object):
    """import dataframe into neo4j"""
    
    def __init__(self, new_graph_database=False):
        """establish connection"""
        link = Graph("http://localhost:7474", username="neo4j", password="!2WSX3edc4")
        self.graph = link
        if new_graph_database:
            self.graph.delete_all()
        
    def create_nodes(self, df_node, node_label):
        """establish node"""
        for i in df_node.index:
            i_node = Node(node_label, id=i)
            #print(i)
            for column in df_node.columns:
                property_value = df_node.loc[i][column] 
                if type(property_value) == type('a'):
                    i_node[column] = property_value 
                elif not np.isnan(property_value):
                    i_node[column] = property_value 
                else:
                    pass
                    #print(column)
                    
            self.graph.create(i_node)
            
    def create_relations(self, from_node_label, from_node_property, to_node_label, to_node_property, relation_type):
        """establish relation"""
        match_CQL = "MATCH (f:" + from_node_label + "),(t:" + to_node_label + ")"
        where_CQL = "WHERE f." + from_node_property + " = t." + to_node_property
        create_CQL = "CREATE (f)-[:" + relation_type + "]->(t)"
        CQL = " ".join([match_CQL,where_CQL,create_CQL]) 
        self.graph.run(CQL)
            
if __name__=='__main__':
    os.chdir("C:\\Users\\Fuyou Tan\\Documents\\develop\\AccessTool\ec3in1")
    tbl_graph = DataToNeo4j(new_graph_database=True)
    
    tblTableName = pd.read_csv("Neo4j_files\\tblTableName_utf.csv")
    tblTableName = tblTableName.set_index("id")
    tbl_graph.create_nodes(tblTableName, 'Table')
    tbl_graph.graph.run("CREATE CONSTRAINT ON (c_id:Table) ASSERT c_id.id IS UNIQUE")
    
    tblTableStruction = pd.read_csv("Neo4j_files\\tblTableStruction_utf.csv",
                                    dtype = {'field_width':np.float,
                                             'field_precision':np.float,
                                             'index':np.str})
    tblTableStruction = tblTableStruction.set_index("id")
    tbl_graph.create_nodes(tblTableStruction, 'Field')
    tbl_graph.graph.run("CREATE CONSTRAINT ON (c_id:Field) ASSERT c_id.id IS UNIQUE")
    
    tbl_graph.create_relations(from_node_label='Table',
                               from_node_property='id',
                               to_node_label='Field',
                               to_node_property='table_id',
                               relation_type='Have_Field')
    
    tbl_graph.create_relations(from_node_label="Field",
                               from_node_property="referance",
                               to_node_label="Field",
                               to_node_property="id",
                               relation_type='Referance')
    