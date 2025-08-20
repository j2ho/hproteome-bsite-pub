import os, sys, glob


for i, unidir in enumerate(unidirs):
    uniid = unidir.split('/')[-2]
    print (i, unidir)
    domainpdbs = glob.glob('%s*.pdb'%unidir)
    for domainpdb in domainpdbs:
        if 'docked' in domainpdb: 
            continue
        domainname = domainpdb.split('/')[-1].strip('.pdb')
        if len(domainname.split('_')) == 5:
                continue
        else: 
            domains.append(domainname) 
    for domainpdb in domainpdbs:
    

