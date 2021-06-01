

from pathlib import Path
import configparser as cfg
import sys
import json
import os




def run():



    try:
        map_json_data = json.load(open(a.map_data, 'r'))
    except:
        print("Error with argparse. Exiting.", file=sys.stderr)
        exit(1)

    try:
        scanfn = a.scan_file
    except:
        print("Error with argparse. Exiting.", file=sys.stderr)
        exit(1)

    if a.data_node is None:
        try:
            data_node = config['user']['data_node']
        except:
            print("Error: data node not supplied in config or command line. Exiting.", file=sys.stderr)
            exit(1)
    else:
        data_node = a.data_node

    if a.index_node is None:
        try:
            index_node = config['user']['index_node']
        except:
            print("Error: index node not supplied in config or command line. Exiting.", file=sys.stderr)
            exit(1)
    else:
        index_node = a.index_node

    if a.set_replica and a.no_replica:
        print("Error: replica publication simultaneously set and disabled.", file=sys.stderr)
        exit(1)
    elif a.set_replica:
        replica = True
    elif a.no_replica:
        replica = False
    else:
        try:
            r = config['user']['set_replica']
            if 'yes' in r or 'true' in r:
                replica = True
            elif 'no' in r or 'false' in r:
                replica = False
            else:
                print("Config file error: set_replica must be true, false, yes, or no.", file=sys.stderr)
                exit(1)
        except:
            print("Set_replica not defined. Use --set-replica or --no-replica or define in config file.", file=sys.stderr)
            exit(1)

    try:
        data_roots = json.loads(config['user']['data_roots'])
        if data_roots == 'none':
            print("Data roots undefined. Define in config file to create file metadata.", file=sys.stderr)
            exit(1)
    except:
        print("Data roots undefined. Define in config file to create file metadata.", file=sys.stderr)
        exit(1)

    try:
        globus = json.loads(config['user']['globus_uuid'])
    except:
        # globus undefined
        globus = "none"

    try:
        dtn = config['user']['data_transfer_node']
    except:
        # dtn undefined
        dtn = "none"

    third_arg_mkd = False
    if a.json is not None:
        json_file = a.json
        third_arg_mkd = True


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



if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    main()
