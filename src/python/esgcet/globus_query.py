import json, copy
import tempfile
import sys, os

from subprocess import Popen, PIPE

from globus_sdk import SearchClient


FILTER_TEMPLATE = {
    "type" : "match_all",
    "field_name" : "data_node",
    "values" : []
    }

SEARCH_TEMPLATE = {
    "q" : "",
    "filters" : [
        {
        "type" : "match_all",
        "field_name" : "latest",
        "values" : ["true"]
        }
        ],
    }

GLOBUS_CMD = "/home/jovyan/conda-envs/esgf-pub520/bin/globus"

class ESGGlobusQuery():

    def __init__(self, UUID_in, data_node_in):
        self._UUID = UUID_in
        self._data_node_filter = self._add_filter("data_node", data_node_in)
        self._search_client = SearchClient()

    def _add_filter(self, name, value):
        tmpfilter = copy.deepcopy(FILTER_TEMPLATE)
        tmpfilter["field_name"] = name
        if type(value) is list:
            tmpfilter["type"] = "match_any"
            tmpfilter["values"] = value
        else:
            tmpfilter["values"].append(value)
        return tmpfilter
    
    def globus_get_record(self, subj):
#        print(f"DEBUG {subj}")

        res = self._search_client.get_subject(self._UUID, subj)
        return res
        
    def query_file_records(self, dataset_id, post_proc=True, latest=True, crit={}):
        q = copy.deepcopy(SEARCH_TEMPLATE)
        q["filters"].append(self._add_filter("type", "File"))
        if dataset_id:
            q["filters"].append(self._add_filter("dataset_id", dataset_id))
        elif crit:
            pass # TODO add filter criteria
        else:
            print("WARNING no search criteria or dataset ID")
            return None
            
        if latest:
            q["filters"].append(self._add_filter("latest", "true"))
        res = self._run_query(q, False)
        return [it["entries"][0]["content"] for it in res["gmeta"]]
        
    def dataset_query_master(self, master_id):
        self._dataset_query(master_id, "master_id")
    
    def _dataset_query(self, _id, field, latest=True):

        q = copy.deepcopy(SEARCH_TEMPLATE)
        q["filters"].append(self._data_node_filter)
        q["filters"].append(self._add_filter("type", "Dataset"))
        q["filters"].append(self._add_filter(field, _id))
        if latest:
            q["filters"].append(self._add_filter("latest", "true"))

        res = self._run_query(q)
        print (f"DEBUG : {res}")
        return self._post_proc_query(res)

    def _run_query(self, q, single=False):

        subj = self._search_client.post_search(self._UUID, q)
          
        return subj

    def _post_proc_query(self, subj): 
        if subj:
            res = self.globus_get_record(subj)
            if res and "content" in res:
                return res["content"]
            else:
                raise RuntimeError(f"Unexpected error {res}")
        else:
            print("No record found")
            return {}

def test():        
    UUID = "5cc79324-1b74-4a77-abc3-838aba2fc734"
    DATA_NODE = "esgf-fake-test.llnl.gov"

    x = ESGGlobusQuery(UUID, DATA_NODE)

    res = x.dataset_query(sys.argv[1])
    with open("test.json", "w") as outf:
        json.dump(res, outf)
    

    res2 = x.file_query(res["id"])

    

#test()