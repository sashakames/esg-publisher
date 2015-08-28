from lxml import etree

def get_fvalue(ele):

    chd = ele.getchildren()


    if len(chd) == 0:
        return [[]]

#        res =  ele.get("value")

#        if not res is None:
#            return [[res.split(',')]]
#        else:
#            return []

    arr = []

    for x in chd:
 
        vals = x.get("value")
       
        res = get_fvalue(x)

        valarr = []

        if not vals is None:
            valarr = [vals.split(',')]

        for y in res:
            arr.append( valarr + y)
    return arr

    

def get_xml_config(fn):

    doc = etree.parse(fn)

    root = doc.getroot()

    fields = get_fvalue(root)

    return fields


