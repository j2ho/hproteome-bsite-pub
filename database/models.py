from django.db import models
from django.urls import reverse
import uuid

# Create your models here.

class Target(models.Model): 

    uniprot = models.CharField(max_length=20)
    protname = models.CharField(max_length=100, help_text='protein name given by uniprot', null=True)
    domains = models.ManyToManyField('Domain',blank=True)
    PROT_TYPES = (('PR', 'Protease'),
            ('GP','GPCR'),
            ('NHR','Nuclear Hormone Receptor'),
            ('KI','Kinase'),
            ('IC','Ion Channel'),
            ('UN','Unspecified'),
            )
    proteintype = models.CharField(max_length=3, choices=PROT_TYPES)
    
    class Meta:
        ordering = ['uniprot']
    def __str__(self): 
        return self.uniprot

    def get_absolute_url(self):
        return reverse('target-detail', args=[str(self.id)])

class Domain(models.Model): 
   
    name = models.CharField(max_length=30)
    firstres = models.IntegerField(default=1)
    resnum = models.CharField(max_length=20, help_text='residues that domain contains (e.g.[110-420])')
    sites = models.ManyToManyField('Site',blank=True)
    domainfile = models.FileField(upload_to='sitedb', null=True)
    seqcsvfile = models.FileField(upload_to='sitedb', null=True) 
    strcsvfile = models.FileField(upload_to='sitedb', null=True) 

    class Meta:
        ordering = ['firstres']

    def get_absolute_url(self): 
        return reverse('domain-detail', args=[str(self.id)])

    def __str__(self): 
        return self.name.split('_')[0]


class Site(models.Model): 

    rank = models.IntegerField(default=1)
    SEARCH_METHODS = (('sequence', 'sequence search'),('structure', 'structure search'))
    method = models.CharField(max_length=10, choices=SEARCH_METHODS, default='sequence')
    coordinate = models.CharField(max_length=100, help_text='Enter coordinate (e.g. (1.2983, 2.0900, -5.3980))')
    ligands = models.ManyToManyField('LigandInstance',blank=True)
    uniquename = models.CharField(max_length=100,blank=True)

    class Meta:
        ordering = ['rank']

    def __str__(self): 
        return self.uniquename


class LigandInstance(models.Model):
    #a unique ligand result with unique 'template_chain_ligandname_tmscore' value

    ligname = models.CharField(max_length=3)
    templates = models.ManyToManyField('TemplateInstance',blank=True)
    ligrank = models.IntegerField(default=1)
    #templ_chain = models.CharField(max_length=20)
    #templ_chain_lignum = models.CharField(max_length=50, help_text='e.g. 4KDH_A_100')
    #tmscore = models.FloatField()
    ligcoord = models.CharField(max_length=50)
    mol2file = models.FileField(upload_to='sitedb',null=True, blank=True) #if docked .mol2 is available
    dockedfile = models.FileField(upload_to='sitedb', null=True)
    #mol2file = models.CharField(max_length=100, default='none')
    #dockedfile = models.CharField(max_length=100, default='none')
    liguniquename = models.CharField(max_length=100,blank=True)

    class Meta:
        ordering = ['ligrank']
    
    def get_absolute_url(self): 
        return reverse('ligand-detail', args=[str(self.id)])

    def __str__(self): 
        return self.ligname


class TemplateInstance(models.Model): 

    templ_chain_lignum = models.CharField(max_length=50, help_text='e.g. 4KDH_A_100')
    tmscore = models.FloatField()
    
    class Meta:
        ordering = ['-tmscore']

    def __str__(self): 
        return '%s_%.4f'%(self.templ_chain_lignum,self.tmscore)
