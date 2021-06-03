import sys
import json
import os

from esgcet.pub_internal import ESGPubCore
from esgcet.args import PublisherArgs

def run(pub_args):

    argdict = pub_args.get_dict()

    pubcore = ESGPubCore()

    try:
        map_json_data = json.load(open(argdict("mapdata"), 'r'))
    except:
        print("Error with map data. Exiting.", file=sys.stderr)
        exit(1)

    proj = pubcore.get_project(pub_args)
    out_json_data = proj.mk_dataset(map_json_data)

    if "outfile" in argdict:
        outfile = argdict["outfile"]
        with open(outfile, 'w') as of:
            json.dump(out_json_data, of)
    else:
        print(json.dumps(out_json_data))


def main():
    pub_args = PublisherArgs()

    run(pub_args)


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    main()
