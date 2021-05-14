from esgcet.pub_client import publisherClient

import esgcet.list2json, sys
from datetime import datetime


def run(args):

    hostname = args[1]
    cert_fn = args[2]
    d = args[0]
    silent = args[3]
    verbose = args[4]


    pubCli = publisherClient(cert_fn, hostname, verbose=verbose, silent=silent)

    for rec in d:

        new_xml = esgcet.list2json.gen_xml(rec)
        if verbose:
            print(new_xml)
        resp = pubCli.publish(new_xml)
        if resp != 200:
            the_time = datetime.now()
            print(f"{the_time} ERROR: publication to index failed, code {resp}", sys.stderr)
            exit(-resp)

