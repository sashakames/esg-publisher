from esgcet.args import PublisherArgs
import os
import sys
from esgcet.settings import *

from esgcet.pub_internal import ESGPubCore


def run(fullmap, pub_args):

    pubcore = ESGPubCore()

    proj = pubcore.get_project(pub_args, fullmap)
    proj.workflow()


def main():

    pub_args = PublisherArgs()
    pub = pub_args.get_args()
    maps = pub.map  # full mapfile path

    if maps is None:
        print("Missing argument --map, use " + sys.argv[0] + " --help for usage.", file=sys.stderr)
        exit(1)
    for m in maps:
        if os.path.isdir(m):
            files = os.listdir(m)
            for f in files:
                if os.path.isdir(m + f):
                    continue
                run(m + f, pub_args)
        else:
            myfile = open(m)
            ismap = False
            first = True
            for line in myfile:
                # if parsed line is not mapfile line, run on each file
                if first:
                    if '#' in line:
                        ismap = True
                        break
                    first = False

                length = len(line)
                run(line[0:length - 1], pub_args)
            myfile.close()
            if ismap:
                run(m, pub_args)


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    main()
