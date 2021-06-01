

from pathlib import Path
import configparser as cfg
import sys
import json
import os


from pub_internal import ESGPubCore

def run(pub_args):

    argdict = pub_args.get_dict()

    pubcore = ESGPubCore()

    try:
        map_json_data = json.load(open(argdict("mapdata"), 'r'))
    except:
        print("Error with argparse. Exiting.", file=sys.stderr)
        exit(1)

    scanfn = argdict("scan_file")


    proj = pubcore.get_project(pub_args)

    out_json_data = proj.mk_dataset()

    try:
        if third_arg_mkd:
            out_json_data = mkd.run([map_json_data, scanfn, data_node, index_node, replica, data_roots, globus, dtn, silent, verbose, json_file])
        else:
            out_json_data = mkd.run([map_json_data, scanfn, data_node, index_node, replica, data_roots, globus, dtn, silent, verbose])
    except Exception as ex:
        print("Error making dataset: " + str(ex), file=sys.stderr)
        exit(1)

    if p:
        print(json.dumps(out_json_data))
    else:
        with open(outfile, 'w') as of:
            json.dump(out_json_data, of)


def main():
    pub_args = PublisherArgs()

    run(pub_args)


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    main()
