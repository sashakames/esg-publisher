import os, sys, json
import esgcet.mapfile as mp
import esgcet.mk_dataset as mkd

mappath = sys.argv[1]
maplist = sys.argv[2]

for line in open(maplist):

    fullmap = mappath + '/' + line.strip()

    map_json_data = mp.run([fullmap, 'no'])
    datafile=map_json_data[0][1]

    destpath=os.path.dirname()
    outname=os.path.basename()
    idx = outname.rfind(.)
    scanfntemplate = "{}.scan.json"
    scanpath=scanfntemplate.format(outname[0:idx])

    autstr='autocurator --out_pretty --out_json {} --files "{}/*.nc"'
    os.system(autstr.format(scanpath, destpath))
    mk_dataset