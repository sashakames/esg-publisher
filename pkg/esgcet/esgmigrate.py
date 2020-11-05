from ESGConfigParser import SectionParser
import configparser as cfg
import os, sys
from urllib.parse import urlparse
# import esgcet.settings
import shutil
from datetime import date
from pathlib import Path
import argparse

import json


VERBOSE = True

DEFAULT_ESGINI = '/esg/config/esgcet'
CONFIG_FN_DEST = "~/.esg/esg.ini"

def project_list(cfg_obj):
    return [x[0] for x in cfg_obj.get_options_from_table('project_options')]



def project_migrate(project, path):

    print(project)
    SP = SectionParser("project:{}".format(project), directory=path)
    SP.parse(path)

    ret = {'drs' : SP.get_facets('dataset_id')}
    try:
        ret[''] = { x[0] : x[1] for x in SP.get_options_from_table('category_defaults') }
    except:
        if VERBOSE:
            print("No category defaults found for {}".format(project))
    return ret


def run(args):

    ini_path = DEFAULT_ESGINI

    project = ""
    if 'project' in args:
        project = args['project']
    if 'fn' in args:
        ini_path = args['fn']
    elif args.get('automigrate', False):
        if os.path.exists(CONFIG_FN_DEST):
            print('Config file already exists, exiting')
            return
    #  TODO  For automigrate, exit if the new settings file is found

    if not os.path.exists(ini_path + '/esg.ini'):
        print("esg.ini not found or unreadable")
        return

    try:
        sp = SectionParser('config:cmip6', directory=ini_path)
        sp.parse( ini_path)
    except Exception as e:
        print("Exception encountered {}".format(str(e)))
        return


    thredds_url = sp.get("thredds_url")
    res = urlparse(thredds_url)
    data_node = res.netloc

    spdef = list(sp['DEFAULT'])
    index_node = ""
    if 'rest_service_url' in spdef:
        index_url = sp.get('rest_service_url')
    elif 'hessian_service_url' in spdef:
        index_url = sp.get('hessian_service_url')
    if index_url != "":
        res = urlparse(index_url)
        index_node = res.netloc
    else:
        index_node = ""
        print("WARNING: No index node setting found in previous config, migration of settings will be incomplete!")
    log_level = sp.get('log_level')


    try:
        pid_creds_in = sp.get_options_from_table('pid_credentials')
    except:
        pid_creds_in = []

    pid_creds = []
    for i, pc in enumerate(pid_creds_in):
        rec = {}
        rec['url'] = pc[0]
        rec['port'] = pc[1]
        rec['vhost'] = pc[2]
        rec['user'] = pc[3]
        rec['password'] = pc[4]
        rec['ssl_enabled'] = bool(pc[5])
        rec['priority'] = i+1
        pid_creds.append(rec)

    try:
        data_roots = sp.get_options_from_table('thredds_dataset_roots')
    except:
        data_roots = []

    dr_dict = {}
    for dr in data_roots:
        dr_dict[dr[1]] = dr[0]

    try:
        svc_urls = sp.get_options_from_table('thredds_file_services')
    except:
        svc_urls = []

    DATA_TRANSFER_NODE = ""
    GLOBUS_UUID = ""

    for line in svc_urls:
        if line[0] == "GridFTP":
            res = urlparse(line[1])
            DATA_TRANSFER_NODE = res.netloc
        elif line[0] == "Globus":
            parts= line[1].split(':')
            GLOBUS_UUID = parts[1][0:36] # length of UUID

    cert_base = sp.get('hessian_service_certfile')

    project_config = {}
    if project.lower() == "all":
        plist = project_list(sp)
        project_config = {proj: project_migrate(proj, ini_path) for proj in plist}

    elif len(project) > 0:
        print(ini_path)
        project_config = {project: project_migrate(project, ini_path)}

    CERT_FN = cert_base.replace('%(home)s', '~')

    print(str(dr_dict))
    print(str(pid_creds))
    print(data_node)
    print(index_node)
    print(CERT_FN)
    print(DATA_TRANSFER_NODE)
    print(GLOBUS_UUID)

    d = date.today()
    t = d.strftime("%y%m%d")
    home = str(Path.home())
    config_file = home + "/.esg/esg.ini"
    backup = home + "/.esg/" + t + "esg.ini"
    shutil.copyfile(config_file, backup)
    config = cfg.ConfigParser()
    config.read(config_file)
    new_config = {"data_node": data_node, "index_node": index_node, "data_roots": json.dumps(dr_dict), "cert": CERT_FN,
                  "globus_uuid": GLOBUS_UUID, "data_transfer_node": DATA_TRANSFER_NODE, "pid_creds": json.dumps(pid_creds)}
    if len(project_config) > 0:
        new_config['project_config'] = json.dumps(project_config)

    for key, value in new_config.items():
        try:
            test = config['user'][key]
        except:
            config['user'][key] = value
    with open(config_file, "w") as cf:
        config.write(cf)


def main():

    args = {}
    if len(sys.argv) > 2:
        args['fn'] = sys.argv[1]
        args['project'] = sys.argv[2]
    run(args)


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    main()
