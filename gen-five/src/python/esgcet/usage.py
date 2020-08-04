USAGE = """
Usage:
esgpublish [options] [--map] mapfile|map-directory
   map-directory contains a collection of mapfiles.  --map argument is supported for backward compatibility
   
   The following options can override settings values configured 
    Options:
    
    --test 
        PID registration will run in "test" mode.  Use this mode unless you are performing "production" publications.
        
    --set-replica
        Enable replica publication for this dataset(s)
    
    --no-replica
        Disable replica publication.
        
    --json <file>
        Load attributes from a <file> in .json form.  The attributes will override any found in the DRS structure or 
        global attributes.
        
    --data-node <hostname>
    
    --index-node <hostname>
    
    --certificate (-c) <pem-file>
        Use the following certificate file in .pem form for publishing (these are generate via a myproxy logon)
    --project
        set / override the project for this, for use with selecting the DRS or specific features, eg. PrePARE, PID
         
"""