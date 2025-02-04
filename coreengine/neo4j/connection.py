'''Module for connecting to Neo4j database.'''
import os
import logging
import yaml
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, DatabaseError, CypherSyntaxError, CypherTypeError
from dotenv import load_dotenv
from coreengine.vault.azurevault import GenLiteAzureVault

load_dotenv()

logger=logging.getLogger("GenLite_App")

class Neo4jConnection:
    driver=None
    '''Class for connecting to Neo4j database.'''

    def __init__(self):
        '''Constructor  for Neo4jConnection class.'''

        self.__configfilepath = 'coreengine/neo4j/config.yaml'
        self.__config = self.__loadconfig__(self.__configfilepath)
        template_config = self.__config.get("neo4j", {})
        self.__uri = template_config.get('neo4j_url', '')
        self.__user = template_config.get('neo4j_username', '')
        self.__pwd = template_config.get('neo4j_password', '')

        if self.__pwd == 'azurevault':
            neo4j_password_vault_key = template_config.get('neo4j_password_vault_key', '')
            if os.environ.get(neo4j_password_vault_key) is None:
                # Get the API key from the Azure Key Vault
                azure_vault = GenLiteAzureVault()
                self.__pwd = azure_vault.get_secret(neo4j_password_vault_key)
                os.environ[neo4j_password_vault_key] = self.__pwd
            else:
                self.__pwd = os.environ.get(neo4j_password_vault_key)
        self.driver = None

        # print("Neo4j URL:", self.__uri)
        # print("Neo4j Username:", self.__user)
        # print("Neo4j Password:", self.__pwd)

        try:
            self.driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except ServiceUnavailable as e:
            logger.error("Failed to create the driver: %s", e)

    def __loadconfig__(self, configfilepath):
        '''
        Loads the config file
        '''
        with open(configfilepath, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config

    def close(self):
        '''Closes the driver.'''
        if self.driver is not None:
            self.driver.close()

    def query(self, query, parameters=None, db=None):
        '''Executes the query and returns the results.'''
        session = None
        response = None
        try:
            session = self.driver.session(
                database=db
                ) if db is not None else self.driver.session()
            response = list(session.run(query, parameters))
        except DatabaseError as dberror:
            response = None
            print("DatabaseError:", dberror)
            logger.error("DatabaseError: %s", dberror)
        except CypherSyntaxError as cse:
            response = None
            print("CypherSyntaxError:", cse)
            logger.error("CypherSyntaxError: %s", cse)
        except CypherTypeError as cte:
            response = None
            print("CypherTypeError:", cte)
            logger.error("CypherTypeError: %s", cte)
        finally:
            if session is not None:
                session.close()
        return response
