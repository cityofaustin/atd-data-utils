"""
Helper methods to work with PostgREST.
"""
from copy import deepcopy
import requests
import pdb

class Postgrest(object):
    """
    Class to interact with PostgREST.
    """
    def __init__(self, url, auth=None):

        self.auth = auth
        self.url = url

        self.headers = {
            "Content-Type": "application/json",
            "Prefer": "return=representation",  # return entire record json in response
        }

        if self.auth:
            self.headers["Authorization"] = f"Bearer {self.auth}"
        

    def insert(self, data=None):
        self.res = requests.post(self.url, headers=self.headers, json=data)
        self.res.raise_for_status()
        return self.res.json()


    def update(self, query_string, data=None):
        """
        This method is dangerous! It is possible to delete and modify records
        en masse. Read the PostgREST docs.
        """
        url = f"{self.url}?{query_string}"
        self.res = requests.patch(url, headers=self.headers, json=data)
        self.res.raise_for_status()
        return self.res.json()


    def upsert(self, data=None):
        """
        This method is dangerous! It is possible to delete and modify records
        en masse. Read the PostgREST docs.
        """
        headers = deepcopy(self.headers)
        headers["Prefer"] += ", resolution=merge-duplicates"
        self.res = requests.post(self.url, headers=headers, json=data)
        self.res.raise_for_status()
        return self.res.json()


    def delete(self, query_string):
        """
        This method is dangerous! It is possible to delete and modify records
        en masse. Read the PostgREST docs.
        """
        url = f"{self.url}?{query_string}"
        self.res = requests.delete(url, headers=self.headers)
        self.res.raise_for_status()
        return self.res.json()


    def select(self, query_string, increment=1000, limit=10000):
        """Select records from PostgREST DB. See documentation for horizontal
        and vertical filtering at http://postgrest.org/.
        
        Args:
            query_string (string): a PostgREST-compliant query string.

            increment (int, optional): The maximum number of records to
                return request per request. This is applied as a "limit" to
                each API request, until the user-specified limit is reached.
                
                Note that the PosgrREST DB itself will likely have limiting
                configured that cannot be exceeded. For example, our
                instances have a limit of 5000 records per request.

            limit (int, optional): The maximum number of records to return
                from the query. This method will continue to query records
                until the limit is reached or no more records are returned.
        
        Returns:
            TYPE: List 
        """
        if not query_string:
            raise Exception("Query string cannot be empty.")

        url = f"{self.url}?{query_string}&limit={increment}"

        records = []

        while True:
            query_url = f"{url}&offset={len(records)}"

            self.res = requests.get(query_url, headers=self.headers)

            self.res.raise_for_status()

            records += self.res.json()

            if len(self.res.json()) < increment or len(records) >= limit:
                return records[0:limit]









