import os, sys
sys.path.append('/home/j2ho/django_all')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sitedb.settings'
import django 
django.setup() 
from django.contrib.auth.models import User
from django.core.files import File

from database.models import *

import glob

def readcsv(csvfile): 
    ligdic = {} 
    with open(csvfile, 'r') as f: 
        lines = f.readlines() 
    for ln in lines[1:]:
        x = ln.strip().split(',')
        templ_list = []
        ligrank = x[0]
        ligname = x[1]
        siterank = x[2]
        ligcoord ='(%.3f, %.3f, %.3f)'% ( float(x[3].strip('"(')),float(x[4]),float(x[5].strip(')"')))
        templates = x[6:]
        for elem in templates:
            elem = elem.strip('"').strip()
            templ_list.append(elem)
        ##################11##
        if int(ligrank) > 30: 
            continue
        ####################
        ligdic[ligname] = {'ligrank':ligrank, 'siterank':siterank, 'ligcoord':ligcoord, 'templates':templ_list}
    return ligdic


def registerligands(d, uniid, domainname, csvfile, method='sequence'):
    tmp = []
    ligdic = readcsv(csvfile)
    sites = {}
    for lig in ligdic:
        singledic = ligdic[lig]
        siterank = singledic['siterank']
        ligcoord = singledic['ligcoord']
        if not siterank in sites: 
            sites[siterank] = ligcoord
    for siterank in sites:
        s = Site.objects.get_or_create(rank=siterank, method=method,coordinate=sites[siterank],uniquename='%s_%s_site%s'%(domainname,method[:3],siterank))
     
    for lig in ligdic:
        singledic = ligdic[lig]
        ligname = lig
        ligrank = singledic['ligrank']
        siterank = singledic['siterank']
        ligcoord = singledic['ligcoord']
        filepath = 'sitedb/%s/%s_%s_%s.mol2'%(uniid, domainname, method[:3], ligname)
        filepathd = 'sitedb/%s/%s_%s_%s_docked.pdb'%(uniid, domainname, method[:3], ligname)
        liguniquename = '%s_%s_%s_%s_%s'%(uniid,domainname,method,ligrank,ligname)
        print(liguniquename)
#        for elem in l:
#            l.delete() 
        if os.path.exists('%s/%s'%('/home/j2ho/django_all/media', filepath)):
            l = LigandInstance(ligname=ligname, ligrank=ligrank, ligcoord=ligcoord, liguniquename=liguniquename, mol2file=filepath, dockedfile=filepathd)
            l.save()

        else:
            l = LigandInstance(ligname=ligname, ligrank=ligrank, ligcoord=ligcoord, liguniquename=liguniquename)
            l.save() 
#            if len(l) > 1:
#                l = l[0]
#            else: 
#                l = LigandInstance.objects.get_or_create(ligname = lig, ligrank=ligrank, ligcoord=ligcoord)

#        if os.path.exists('%s/%s'%('/home/j2ho/django_all/media', filepathd)):
#            l = LigandInstance.objects.get(ligname = lig, ligrank=ligrank, ligcoord=ligcoord,mol2file=filepath, dockedfile=filepathd)
#        else: 
#            l = LigandInstance.objects.filter(ligname = lig, ligrank=ligrank, ligcoord=ligcoord)
#            l = l[0]
        templates = singledic['templates']
        l = LigandInstance.objects.get(liguniquename=liguniquename)
        for template in templates:
            x= template.split('_')
            name = '%s_%s_%s'%(x[0],x[1],x[2])
            tm = float(x[3])
            t = TemplateInstance.objects.get_or_create(templ_chain_lignum = name, tmscore = tm)
            t = TemplateInstance.objects.get(templ_chain_lignum = name, tmscore = tm)
            #t.save()
            l.templates.add(t)
        s = Site.objects.get(uniquename='%s_%s_site%s'%(domainname,method[:3],siterank))
        s.ligands.add(l)
    d = Domain.objects.get(name=domainname)
    for siterank in sites:
        s = Site.objects.get(uniquename='%s_%s_site%s'%(domainname,method[:3],siterank))
        d.sites.add(s)


import re
import requests
from urllib.request import urlopen

def getproteinname(uniid):
    url = 'https://rest.uniprot.org/uniprot/%s'%uniid
    html = requests.get(url).json()
    if html['entryType'] == 'Inactive':
        return None
    else:
        if 'recommendedName' in  html['proteinDescription']:
            title =  (html['proteinDescription']['recommendedName']['fullName']['value'])
        elif 'submissionNames' in html['proteinDescription']:
            title =  (html['proteinDescription']['submissionNames'][0]['fullName']['value'])
        return str(title)

def getlist(filename): 
    namelist = []
    f = open(filename, 'r')
    lines = f.readlines() 
    f.close() 
    for ln in lines: 
        namelist.append(ln.strip())
    return namelist

gpcr = getlist('/home/j2ho/gpcr.list')
protease = getlist('/home/j2ho/protease.list')
nhr = getlist('/home/j2ho/nhr.list')
kinase = getlist('/home/j2ho/kinase.list')
ionchannel = getlist('/home/j2ho/ionchannel.list')
def getproteintype(uniid): 
    if uniid in gpcr: 
        return ('GP')
    elif uniid in protease:
        return ('PR')
    elif uniid in nhr: 
        return ('NHR')
    elif uniid in kinase: 
        return ('KI')
    elif uniid in ionchannel: 
        return ('IC')
    else: 
        return ('UN')


def getresidues(domainpdb): 
    fragnum = int(domainpdb.split('/')[-1].split('_')[1].strip('F'))
    basenum = 200*(fragnum-1) 
    resnumlist = []
    with open(domainpdb, 'r') as f: 
        lines = f.readlines() 
    for ln in lines: 
        resnum = int(ln[22:27]) + basenum 
        resnumlist.append(resnum)
    first = resnumlist[0]
    last = resnumlist[-1]
    return (int(first), '%i-%i'%(first, last))


#################


unidirs = glob.glob('/home/j2ho/django_all/media/sitedb/*/')


#ll = LigandInstance.objects.all() 
#for elem in ll:
#    elem.delete() 
################
#REGISTER TARGETS
registered = [] 
tl = Target.objects.all() 
for elem in tl:
    elem= str(elem) 
    registered.append(elem)

#for i, unidir in enumerate(unidirs):
#    uniid = unidir.split('/')[-2]
#    if not uniid in registered:
#sys.exit() 

#for unidir in unidirs[11535:]:
#        uniid = unidir.split('/')[-2]
#        protname = getproteinname(uniid)
#        if protname == None: 
#            print (unidir)
#        else: 
#            prottype = getproteintype(uniid)
#            t = Target.objects.get_or_create(uniprot=uniid, protname=protname, proteintype=prottype)
#REGISTER DOMAINS
#for i, unidir in enumerate(unidirs):
#    uniid = unidir.split('/')[-2]
#    if not uniid in registered:
#        continue
#    print (i, unidir)
#    t = Target.objects.get(uniprot=uniid)
#    domainpdbs = glob.glob('%s*.pdb'%unidir)
#    for domainpdb in domainpdbs:
#        print (domainpdb)
#        with open(domainpdb, 'r') as f: 
#            lines =f.readlines() 
#        if len(lines) == 0: 
#            os.system('rm %s'%domainpdb)
#        else: 
#            domainname = domainpdb.split('/')[-1].strip('.pdb')
#            firstres, residues = getresidues(domainpdb)
#            d = Domain.objects.get_or_create(name=domainname, resnum = residues, firstres=firstres, domainfile='sitedb/%s/%s.pdb'%(uniid,domainname))
#            d = Domain.objects.get(name=domainname)
#            t.domains.add(d)

#REGISTER SITES
#registeredlig = []
#ll = LigandInstance.objects.all() 
#for elem in ll: 
#if elem.
#    registeredlig.append(elem)
for i, unidir in enumerate(unidirs):
    uniid = unidir.split('/')[-2]
#    if not uniid=="O00142":
#        continue
    if not int(sys.argv[1]) <= i < int(sys.argv[2]):
        continue
    if not uniid in registered:
        continue
    print (i, unidir)
    domainpdbs = glob.glob('%s*.pdb'%unidir)
    for domainpdb in domainpdbs:
        if 'docked' in domainpdb: 
            continue
        domainname = domainpdb.split('/')[-1].strip('.pdb')

        if len(domainname.split('_')) == 5:
                continue
        seqcsv = '/home/j2ho/django_all/media/sitedb/%s/%s_seq.csv'%(uniid,domainname)
        strcsv = '/home/j2ho/django_all/media/sitedb/%s/%s_str.csv'%(uniid,domainname)
        if os.path.exists(seqcsv):
            d = Domain.objects.filter(name=domainname).update(seqcsvfile='sitedb/%s/%s_seq.csv'%(uniid,domainname))
            d = Domain.objects.get(name=domainname)
#            d.update(seqcsvfile=seqcsv)
#            d.seqcsvfile.save('%s/%s_seq.csv'%(uniid,domainname),File(open(seqcsv)))
            registerligands(d, uniid, domainname, seqcsv, method='sequence')
        if os.path.exists(strcsv):
            d = Domain.objects.filter(name=domainname).update(strcsvfile='sitedb/%s/%s_str.csv'%(uniid,domainname))
            d = Domain.objects.get(name=domainname)
#            d.update(seqcsvfile=seqcsv)
#            d.strcsvfile.save('%s/%s_str.csv'%(uniid,domainname),File(open(strcsv)))
            registerligands(d, uniid, domainname, strcsv, method='structure')
#    sys.exit()
    
#l = LigandInstance(ligname = 'LIG', templ_chain = '4KDH_A', templ_chain_lignum='4KDH_A_1000', tmscore=0.3929,ligcoord='(1.1239, 3.3241, -2.1349)', mol2file = 'sitedb/Q9H0K1/Q9H0K1_F1_d1_seq_ANP.mol2') 

#l.save()
