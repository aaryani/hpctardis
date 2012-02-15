# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2012, RMIT e-Research Office
#   (RMIT University, Australia)
# Copyright (c) 2010-2011, Monash e-Research Centre
#   (Monash University, Australia)
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    *  Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    *  Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    *  Neither the name of the VeRSI, the VeRSI Consortium members, nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

"""
tests.py

.. moduleauthor:: Ian Thomas <Ian.Edward.Thomas@rmit.edu.au>

"""
import logging
import re
from os import path
   
from django.test import TestCase
from django.test.client import Client
from os.path import abspath, basename, dirname, join, exists

from os import makedirs
from os.path import abspath, basename, dirname, join, exists
from shutil import rmtree


from django.contrib.auth.models import User, Group
from tempfile import mkdtemp, mktemp
from os import walk, path
from django.conf import settings
from tardis.tardis_portal.models import Experiment, ExperimentParameter, \
    DatafileParameter, DatasetParameter, ExperimentACL, Dataset_File, \
    DatafileParameterSet, ParameterName, GroupAdmin, Schema, \
    Dataset, ExperimentParameterSet, DatasetParameterSet, \
    UserProfile, UserAuthentication

from nose.plugins.skip import SkipTest        

from django.conf import settings

from tardis.tardis_portal import models
from tardis.tardis_portal.auth.localdb_auth import django_user

#from tardis.apps.hpctardis.metadata import _get_metadata
#from tardis.apps.hpctardis.metadata import _get_schema
#from tardis.apps.hpctardis.metadata import _save_metadata
from tardis.apps.hpctardis.metadata import process_all_experiments
from tardis.apps.hpctardis.metadata import process_experimentX

from tardis.apps.hpctardis.models import PartyRecord
from tardis.apps.hpctardis.models import ActivityRecord
from tardis.apps.hpctardis.models import NameParts
from tardis.apps.hpctardis.models import PartyRecord
from tardis.apps.hpctardis.models import PartyLocation
from tardis.apps.hpctardis.models import ActivityPartyRelation
from tardis.apps.hpctardis.models import PublishAuthorisation


from tardis.tardis_portal.ParameterSetManager import ParameterSetManager
from tardis.tardis_portal.models import ParameterName
from tardis.tardis_portal.models import ExperimentACL, Experiment, UserProfile
from tardis.tardis_portal.models import DatasetParameterSet
from tardis.tardis_portal.models import DatasetParameter
from tardis.tardis_portal.models import Schema

logger = logging.getLogger(__name__)


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class HPCprotocolTest(TestCase):
    
    user = 'tardis_user1'
    pwd = 'secret'
    email = 'tardis@gmail.com'
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(self.user, self.email, self.pwd)
        # TODO extract the only the username form <User:....>
        self.assertEquals(str(User.objects.get(username=self.user)), 'tardis_user1') 
    
    def test_protocol1(self):
        from django.core.urlresolvers import reverse
        import os
        
        url=reverse('tardis.apps.hpctardis.views.protocol')
        response = self.client.post(url, {'username':self.user, 
                                               'password':self.pwd,
                                               'authMethod':'localdb'})
        self.assertEquals(response.status_code, 200)
        str_response = str(response.content)   
        self.assertEquals(str_response, 'Successful') 
    
    def test_protocol2(self):
        from django.core.urlresolvers import reverse
        import os
        
        url=reverse('tardis.apps.hpctardis.views.protocol')
        response = self.client.post(url, {'authMethod':'localdb'})
        self.assertEquals(response.status_code, 200)
        str_response = str(response.content)   
        self.assertEquals(str_response, 'Please enter Username and Password') 
                             
    
       
    def test_authentication(self):
        from django.core.urlresolvers import reverse
        import os
        import tempfile
        
        url=reverse('tardis.apps.hpctardis.views.login')
        


        temp = tempfile.TemporaryFile()
        temp.write("Username~venki\nName~Venki Bala\nExperiment~Test Exp\nFacility~localhost\nDescription~Test desc\nFacility~localhost\nFolderName~myfolder\nCounter~7\nPackage~test_package")   
        temp.seek(0)
        
        response = self.client.post(url, {'username':self.user, 
                                               'password':self.pwd, 
                                               'authMethod':'localdb','file':temp}) 
        temp.close()
        self.assertEquals(response.status_code, 200)
        
        str_response = str(response.content)    
        checkuser = response.content.find(str(self.user))
        self.assertEquals(checkuser >= 0, True)
        
        content_list = []
        content_list = str_response.split(str(self.user))     
        self.assertEquals((str(settings.STAGING_PATH) + '/'),content_list[0])
        
     #   self.assertEquals(self.user, checkuser)
        
        content_list = content_list[1].split('/')
        staging = path.join(settings.STAGING_PATH ,str(self.user),content_list[1])
        self.assertEquals(response.content, staging)

        content_list = content_list[1].split('@')
        expid1 = int(content_list[0])
        expid2 = int(content_list[1])
        self.assertEquals(expid1,expid2)
        
        foldername = 'localhost.test_package.myfolder.7'
        returnfolder = str(content_list[2])
        self.assertEquals(foldername,returnfolder)
     #  Test for Creation of experiment
        
        try:
            e = Experiment.objects.get(pk=expid1)
        except Experiment.DoesNotExist:
            logger.exception('Experiment for eid %i in TestCase does not exist' % expid1)
     
        self.assertEquals(str(e.title).rstrip('\n'),'Test Exp')
        self.assertEquals(str(e.institution_name),'RMIT University')
        self.assertEquals(str(e.description).rstrip('\n'),'Test desc')
        self.assertEquals(str(e.created_by),str(self.user))
        
        

def _grep(string, l):
    expr = re.compile(string)
    match = expr.search(l)
    return match

class SimplePublishTest(TestCase):
    """ Publish Experiments as RIFCS"""
    
    def setUp(self):
        self.client = Client()
        from django.contrib.auth.models import User
        self.username = 'tardis_user1'
        self.pwd = 'secret'
        email = ''
        self.user = User.objects.create_user(self.username, email, self.pwd)
        self.userprofile = UserProfile(user=self.user)
      
    def tearDown(self):
        from shutil import rmtree
        rmtree(self.experiment_path)
        
    def test_publish(self):
        """ Create an experiment and publish it as RIF-CS using RMITANDSService"""
        login = self.client.login(username=self.username,
                                  password=self.pwd)
        self.assertTrue(login)
        # Create simple experiment
        exp = models.Experiment(title='test exp1',
                                institution_name='rmit',
                                created_by=self.user,
                                public=True
                                )
        exp.save()
        acl = ExperimentACL(
            pluginId=django_user,
            entityId=str(self.user.id),
            experiment=exp,
            canRead=True,
            isOwner=True,
            aclOwnershipType=ExperimentACL.OWNER_OWNED,
            )
        acl.save()
        self.assertEqual(exp.title, 'test exp1')
        self.assertEqual(exp.url, None)
        self.assertEqual(exp.institution_name, 'rmit')
        self.assertEqual(exp.approved, False)
        self.assertEqual(exp.handle, None)
        self.assertEqual(exp.created_by, self.user)
        self.assertEqual(exp.public, True)
        self.assertEqual(exp.get_or_create_directory(),
                         path.join(settings.FILE_STORE_PATH, str(exp.id)))

        self.experiment_path = path.join(settings.FILE_STORE_PATH, str(exp.id))
        # publish
        data = {'legal':'on',
                'profile':'default.xml'}
        response = self.client.post("/experiment/view/publish/1/", data)
        
        logger.debug("response=%s" % response)
        # check resulting rif-cs
        response = self.client.post("/rif_cs/")
        self.assertTrue(_grep("test exp1",str(response)))
        self.assertTrue(_grep("<key>http://www.rmit.edu.au/HPC/2/1</key>",str(response)))
        self.assertTrue(_grep("""<addressPart type="text">%s</addressPart>""" %
                               settings.GROUP_ADDRESS
                              ,str(response)))
        self.assertFalse(_grep("<key>http://www.rmit.edu.au/HPC/2/2</key>",str(response)))
        logger.debug("response=%s" % response)
        
        
class VASPMetadataTest(TestCase):
    """ Tests ability to create experiments, dataset with VASP datafiles and extract appropriate datafiles"""
    
    def setUp(self):
        self.client = Client()
        from django.contrib.auth.models import User
        self.username = 'tardis_user1'
        self.pwd = 'secret'
        email = ''
        self.user = User.objects.create_user(self.username, email, self.pwd)
        self.userprofile = UserProfile(user=self.user)
    
    
    def tearDown(self):
        from shutil import rmtree
        rmtree(self.experiment_path)
          
    def _test_metadata(self,schema,name,dataset,fields):
        """ Check that metadata is correct"""
        try:
            sch = models.Schema.objects.get(namespace__exact=schema,name=name)
        except Schema.DoesNotExist:
            logger.error("could not find schema %s %s" % (schema,name))
            self.assertTrue(False)
        self.assertEqual(schema,sch.namespace)
        self.assertEqual(name,sch.name)
        try:
            datasetparameterset = models.DatasetParameterSet.objects.get(schema=sch, dataset=dataset)
        except DatasetParameterSet.DoesNotExist:
            self.assertTrue(False) 
        psm = ParameterSetManager(parameterset=datasetparameterset)
        for key, field_type, value in fields:
            logger.debug("key=%s,field_type=%s,value=%s" % (key,field_type, value))
            try:
                # First check stringed value
                param = psm.get_params(key,value=True)
                logger.debug("param val=%s" % param)
                # assume any duplicate parameters are same value
                self.assertEquals(str(param[0]),str(value),
                                  "incorrect value in %s: expected "
                                  "%s found %s" % (key,repr(value),repr(param)))
                # Then correct type
                param = psm.get_params(key,value=False)
                logger.debug("param type=%s" % param[0])                
                self.assertEquals(param[0].name.data_type,
                                  field_type,
                                  "incorrect type in %s: expected "
                                  "%s found %s" %
                                   (key,param[0].name.data_type, field_type))
            except DatasetParameter.DoesNotExist:
                logger.error("cannot find %s" % key)
                self.assertTrue(False, "cannot find %s" % key)
                
    def _metadata_extract(self,expname,files,ns,schname,results,staging_hook=False):
        """ Check that we can create an VASP experiment and extract metadata from it"""
        
        login = self.client.login(username=self.username,
                                  password=self.pwd)
        self.assertTrue(login)
        exp = models.Experiment(title=expname,
                                institution_name='rmit',
                                created_by=self.user,
                                public=True
                                )
        exp.save()
        acl = ExperimentACL(
            pluginId=django_user,
            entityId=str(self.user.id),
            experiment=exp,
            canRead=True,
            isOwner=True,
            aclOwnershipType=ExperimentACL.OWNER_OWNED,
            )
        acl.save() 
        self.assertEqual(exp.title, expname)
        self.assertEqual(exp.url, None)
        self.assertEqual(exp.institution_name, 'rmit')
        self.assertEqual(exp.approved, False)
        self.assertEqual(exp.handle, None)
        self.assertEqual(exp.created_by, self.user)
        self.assertEqual(exp.public, True)
        self.assertEqual(exp.get_or_create_directory(),
                         path.join(settings.FILE_STORE_PATH, str(exp.id)))

        self.experiment_path = path.join(settings.FILE_STORE_PATH, str(exp.id))
      
        dataset = models.Dataset(description="dataset description...",
                                 experiment=exp)
        dataset.save()
        for f in files:
            self._make_datafile(dataset,
                       path.join(path.abspath(path.dirname(__file__)),f))       
        if not staging_hook:            
            process_experimentX(exp)
        else:
            logger.debug("use staging hook")
            pass        
        self._test_metadata(ns,schname,dataset,results)
        return dataset
                
    def test_metadata1(self):
        """ Test first set of VASP data"""
        dataset = self._metadata_extract(expname="testexp1",
                                 files = ['testing/dataset1/OUTCAR',
                                          'testing/dataset1/KPOINTS',
                                          'testing/dataset1/vasp.sub.o813344',
                                          'testing/dataset1/INCAR',
                                          'testing/dataset1/metadata.vasp',
                                          'testing/dataset1/POSCAR' ],
                               ns="http://tardis.edu.au/schemas/vasp/1",
                               schname="vasp 1.0",
                               results= [("kpoint_grid",ParameterName.STRING," 8  8  8   \n"),
                                        ("kpoint_grid_offset",ParameterName.STRING," 0  0  0\n"),
                                          ("ENCUT",ParameterName.NUMERIC,"400.0"),
                                          ("NIONS",ParameterName.NUMERIC,"216.0"),
                                          ("NELECT",ParameterName.NUMERIC,"864.0"),
                                          ("ISIF",ParameterName.NUMERIC,"3.0"),
                                          ("ISPIN",ParameterName.NUMERIC,"4.0"),
                                         
                                          ("NSW",ParameterName.NUMERIC,"42.0"),
                                          ("IBRION",ParameterName.NUMERIC,"2.0"),
                                          ("ISMEAR",ParameterName.NUMERIC,"-6.0"),
                                          ("POTIM",ParameterName.NUMERIC,"0.5"),
                                           ("EDIFF",ParameterName.NUMERIC,"0.0001"),
                                          ("EDIFFG",ParameterName.NUMERIC,"0.001"),
                                          ("Descriptor Line",ParameterName.STRING,"Bulk Diamond"),
                                          ("NELM",ParameterName.NUMERIC,"60.0"),
                                          ("TEEND",ParameterName.NUMERIC,"0.0"),
                                          ("SMASS",ParameterName.NUMERIC,"-3.0"),
                                          ("TITEL",ParameterName.STRING,'PAW_PBE C 08Apr2002'),
                                      
                                      ("Cell Scaling",ParameterName.NUMERIC,"1.0"),
                                           ("Cell Parameter1",ParameterName.STRING,'    10.6863390000000003    0.0000000000000000    0.0000000000000000\n'),
                                           ("Cell Parameter2",ParameterName.STRING,'     0.0000000000000000   10.6863390000000003    0.0000000000000000\n'),
                                           ("Cell Parameter3",ParameterName.STRING,'     0.0000000000000000    0.0000000000000000   10.6863390000000003\n'),
                                        
                                        #  ("Cell Parameters",ParameterName.STRING,"   1.00000000000000     \n    10.6863390000000003    0.0000000000000000    0.0000000000000000\n     0.0000000000000000   10.6863390000000003    0.0000000000000000\n     0.0000000000000000    0.0000000000000000   10.6863390000000003\n")
                                          ])
        self._test_metadata(schema="http://tardis.edu.au/schemas/general/1",
                               name="general 1.0",
                               dataset=dataset,
                               fields= [ ("Project",ParameterName.STRING,"FOOBAR Project"),
                                          ("Walltime",ParameterName.STRING,"01:59:17"),
                                          ("Number Of CPUs",ParameterName.NUMERIC,"64.0"),
                                          ("Maximum virtual memory",ParameterName.NUMERIC,"27047.0"),
                                          ("Max jobfs disk use",ParameterName.NUMERIC,"0.1")])
                                                                         
        
    def test_metadata2(self):
        """ Tests second set of VASP data"""
        
        dataset = self._metadata_extract(expname="testexp2",
                                 files = ['testing/dataset2/OUTCAR',
                                          'testing/dataset2/KPOINTS',
                                          'testing/dataset2/vasp.sub.o935843',
                                          'testing/dataset2/vasp.sub.o935800',
                                          'testing/dataset2/INCAR',
                                          'testing/dataset2/metadata.vasp',
                                          'testing/dataset2/POSCAR',
                                          'testing/dataset2/OSZICAR' ],
                               ns="http://tardis.edu.au/schemas/vasp/1",
                               schname="vasp 1.0",
                               results= [("kpoint_grid",ParameterName.STRING," 8  8  8   \n"),
                                        ("kpoint_grid_offset",ParameterName.STRING," 0  0  0\n"),
                                          ("ENCUT",ParameterName.NUMERIC,"400.0"),
                                          ("NIONS",ParameterName.NUMERIC,"215.0"),
                                          ("NELECT",ParameterName.NUMERIC,"800.0"),
                                          ("ISIF",ParameterName.NUMERIC,"2.0"),
                                          ("ISPIN",ParameterName.NUMERIC,"1.0"),
                                        
                                          ("NSW",ParameterName.NUMERIC,"0.0"),
                                          ("IBRION",ParameterName.NUMERIC,"-1.0"),
                                          ("ISMEAR",ParameterName.NUMERIC,"-99.0"),
                                          ("POTIM",ParameterName.NUMERIC,"0.5"),
                                          ("EDIFF",ParameterName.NUMERIC,"5e-06"),
                                          ("EDIFFG",ParameterName.NUMERIC,"5e-05"),
                                          ("NELM",ParameterName.NUMERIC,"60.0"),
                                          ("ISTART",ParameterName.NUMERIC,"0.0"),
                                          ("TEBEG",ParameterName.NUMERIC,"0.0"),
                                          ("TEEND",ParameterName.NUMERIC,"0.0"),
                                          ("SMASS",ParameterName.NUMERIC,"-3.0"),
                                          ("LEXCH",ParameterName.STRING,"PE\n PE\n 8\n 8"),
                                          
                                           ("Cell Scaling",ParameterName.NUMERIC,"1.0"),
                                           ("Cell Parameter1",ParameterName.STRING,'    10.6851970403940548    0.0000000000000000    0.0000000000000000\n'),
                                           ("Cell Parameter2",ParameterName.STRING,'     0.0000000000000000   10.6851970403940548    0.0000000000000000\n'),
                                           ("Cell Parameter3",ParameterName.STRING,'     0.0000000000000000    0.0000000000000000   10.6851970403940548\n'),
                                           
                                            #("Cell Parameters",ParameterName.STRING,"   1.00000000000000     \n    10.6851970403940548    0.0000000000000000    0.0000000000000000\n     0.0000000000000000   10.6851970403940548    0.0000000000000000\n     0.0000000000000000    0.0000000000000000   10.6851970403940548\n"),
                                      
                            
                                          ("TITEL",ParameterName.STRING,"PAW_PBE C 08Apr2002\n PAW_PBE N 08Apr2002"),
                                           ("Descriptor Line",ParameterName.STRING,"NV-Diamond Static"),
                                          ("Final Iteration",ParameterName.NUMERIC,"17.0")
                                          ])
        
        self._test_metadata(schema="http://tardis.edu.au/schemas/general/1",
                               name="general 1.0",
                               dataset=dataset,
                               fields= [   ("Project",ParameterName.STRING,"FOOBAR Project"),
                                          ("Walltime",ParameterName.STRING,"04:27:18"),
                                          ("Number Of CPUs",ParameterName.NUMERIC,"56.0"),
                                          ("Maximum virtual memory",ParameterName.NUMERIC,"57537.0"),
                                          ("Max jobfs disk use",ParameterName.NUMERIC,"0.1"),])
        
    def test_metadata3(self):
        """ Tests first set of SIESTA data"""
        
        dataset = self._metadata_extract(expname="testexp2",
                                 files = ['testing/dataset3/input.fdf',
                                          'testing/dataset3/output',
                                          'testing/dataset3/metadata.siesta',
                                          'testing/dataset3/siesta.sub.o923124'],
                               ns="http://tardis.edu.au/schemas/siesta/1",
                               schname="siesta 1.0",
                               results= [("SystemName",ParameterName.STRING,"my System"),
                                        ("MeshCutoff",ParameterName.NUMERIC,"500.0"),
                                          ("ElectronicTemperature",ParameterName.NUMERIC,"100.0"),
                                          ("k-grid",ParameterName.STRING,'9    0    0    0\n0    1    0    0\n0    0    1    0\n'),
                                     
                                          ("PAO.Basis",ParameterName.STRING,'Si  3 0.2658542\n n=2  0  2  E  4.9054837  -0.5515252\n   5.6679504  1.8444465\n   1.000   1.000\n n=3  1  2  E  15.6700423  -0.8457466\n   6.6151626  3.9384685\n   1.000   1.000\n n=3  2  1  E  44.0436726  -0.4370817\n   4.5403665\n   1.000\nP  3 0.1963113\n n=3  0  2  E  40.2507184  -0.7320000\n   5.8661651  -0.6144891\n   1.000   1.000\n n=3  1  2  E  78.4504409  -0.8743580\n   6.8187128  -0.3120693\n   1.000   1.000\n n=3  2  1  E  32.5566663  -0.2998069\n   4.9053838\n   1.000\n'),
                                          ("MD.TypeOfRun",ParameterName.STRING,"cg"),
                                          ("MD.NumCGsteps",ParameterName.NUMERIC,"100.0"),
                                          ("MD.MaxForceTol",ParameterName.NUMERIC,"0.001"),
                                          ("iscf",ParameterName.STRING,'siesta:   19   -34376.1097   -34376.0348   -34376.0689  0.0026 -3.1498\n'),
                                          ("E_KS",ParameterName.NUMERIC,'-34376.0348'),
                                          ("Occupation Function",ParameterName.STRING,'FD'),
                                          ("OccupationMPOrder",ParameterName.NUMERIC,'1.0')
                                          ])
        self._test_metadata(schema="http://tardis.edu.au/schemas/general/1",
                               name="general 1.0",
                               dataset=dataset,
                               fields= [  ("Project",ParameterName.STRING,"FOOBAR Project"), #Assume single work for project
                                   ("Walltime",ParameterName.STRING,"04:27:18"), 
                                     ("Number Of CPUs",ParameterName.NUMERIC,"6.0"),
                                     ("Maximum virtual memory",ParameterName.NUMERIC,"7537.0"),
                                      ("Max jobfs disk use",ParameterName.NUMERIC,"2.1")
                 ])

        
        
        
    def test_metadata4(self):
        """ Tests first set of GULP data"""
        
        dataset = self._metadata_extract(expname="testexp2",
                                 files = ['testing/dataset4/optiexample.gin',
                                          'testing/dataset4/optiexample.gout',
                                          'testing/dataset4/mdexample.gin',
                                          'testing/dataset4/mdexample.gout'],
                               ns="http://tardis.edu.au/schemas/gulp/1",
                               schname="gulp 1.0",
                               results= [("Run Type",ParameterName.STRING,"opti"),
                                        ("Run Keyword",ParameterName.STRING,"conp sm"),
                                        ("Library",ParameterName.STRING,"foobar"),
                                        ("CoordinateFile",ParameterName.STRING,"ss.xyz"),
                                        ("Formula",ParameterName.STRING,"foobar"),
                                        ("Total number atoms/shell",ParameterName.NUMERIC,"120.0")
                                        
                                        ])

        self._test_metadata(schema="http://tardis.edu.au/schemas/gulp/2",
                               name="gulp2 1.0",
                               dataset=dataset,
                               fields= [("Run Type",ParameterName.STRING,"md"),
                                        ("Run Keyword",ParameterName.STRING,"conv"),
                                        ("Formula",ParameterName.STRING,"foobar")
                                        ])
                
    def test_metadata5(self):
        """ Tests first set of CRYSTAL data"""
        
        dataset = self._metadata_extract(expname="testexp2",
                                 files = ['testing/dataset5/INPUT',
                                          'testing/dataset5/OUTPUT',
                                          'testing/dataset5/crystaljob.o599843'],
                               ns="http://tardis.edu.au/schemas/crystal/1",
                               schname="crystal 1.0",
                               results= [("Experiment name",ParameterName.STRING,"FOOBAR\n"),
                                        ("Calculation type",ParameterName.STRING,"CRYSTAL\n"),                                    
                                        ("Space/layer/rod/point group",ParameterName.NUMERIC,"14.0"),                              
                                        ("Lattice parameter",ParameterName.STRING,"1 2 3 4\n"),
                                        ("SLABCUT",ParameterName.STRING,"no"),                                    
                                        ("OPTGEOM",ParameterName.STRING,"no"),                                                                        
                                        ("TESTGEOM",ParameterName.STRING,"no"),                                                                        
                                        ("UHF",ParameterName.STRING,"yes"),                                                                        
                                        ("DFT",ParameterName.STRING,"yes"),                                                                                                                
                                        ("MAXCYCLE",ParameterName.NUMERIC,"325.0"),                                                                                                                
                                        ("SHRINK",ParameterName.STRING,"2 13"),
                                        ("FMIXING",ParameterName.NUMERIC,"87.0"),                                                                                                                                                                                            
                                        ("BROYDEN",ParameterName.STRING,"0.0032 10 20")                                                                                                                                                                                            
                                        ])

        dataset2 = self._metadata_extract(expname="testexp2",
                                 files = ['testing/dataset5b/INPUT'],
                               ns="http://tardis.edu.au/schemas/crystal/1",
                               schname="crystal 1.0",
                               results= [("Space/layer/rod/point group",ParameterName.NUMERIC,"42.0"),
                                     ("Lattice parameter",ParameterName.STRING,"foobar2\n"),                                    
                                        ("SLABCUT",ParameterName.STRING,"yes"),                                                                        
                                        ("OPTGEOM",ParameterName.STRING,"yes"),                                                                        
                                        ("TESTGEOM",ParameterName.STRING,"yes"),                                                                        
                                        ("UHF",ParameterName.STRING,"no"),                                                                        
                                        ("DFT",ParameterName.STRING,"no")                                                                        
                                        ])

        
        
        
    def test_metadata_postsave(self):
        """ Tests use of postsave hook to trigger metadata extraction"""
        #raise SkipTest()
        dataset = self._metadata_extract(expname="testexp2",
                                 files = ['testing/dataset3/input.fdf',
                                          'testing/dataset3/output',
                                          'testing/dataset3/metadata.siesta',
                                          'testing/dataset3/siesta.sub.o923124'],
                               ns="http://tardis.edu.au/schemas/siesta/1",
                               schname="siesta 1.0",
                               results= [("SystemName",ParameterName.STRING,"my System"),
                                        ("MeshCutoff",ParameterName.NUMERIC,"500.0"),
                                          ("ElectronicTemperature",ParameterName.NUMERIC,"100.0"),
                                          ("k-grid",ParameterName.STRING,'9    0    0    0\n0    1    0    0\n0    0    1    0\n'),
                                     
                                          ("PAO.Basis",ParameterName.STRING,'Si  3 0.2658542\n n=2  0  2  E  4.9054837  -0.5515252\n   5.6679504  1.8444465\n   1.000   1.000\n n=3  1  2  E  15.6700423  -0.8457466\n   6.6151626  3.9384685\n   1.000   1.000\n n=3  2  1  E  44.0436726  -0.4370817\n   4.5403665\n   1.000\nP  3 0.1963113\n n=3  0  2  E  40.2507184  -0.7320000\n   5.8661651  -0.6144891\n   1.000   1.000\n n=3  1  2  E  78.4504409  -0.8743580\n   6.8187128  -0.3120693\n   1.000   1.000\n n=3  2  1  E  32.5566663  -0.2998069\n   4.9053838\n   1.000\n'),
                                          ("MD.TypeOfRun",ParameterName.STRING,"cg"),
                                          ("MD.NumCGsteps",ParameterName.NUMERIC,"100.0"),
                                          ("MD.MaxForceTol",ParameterName.NUMERIC,"0.001"),
                                          ("iscf",ParameterName.STRING,'siesta:   19   -34376.1097   -34376.0348   -34376.0689  0.0026 -3.1498\n'),
                                          ("E_KS",ParameterName.NUMERIC,'-34376.0348'),
                                          ("Occupation Function",ParameterName.STRING,'FD'),
                                          ("OccupationMPOrder",ParameterName.NUMERIC,'1.0')
                                          ],
                               staging_hook= True)
        self._test_metadata(schema="http://tardis.edu.au/schemas/general/1",
                               name="general 1.0",
                               dataset=dataset,
                               fields= [
                ("Project",ParameterName.STRING,"FOOBAR Project"), #Assume single work for project
                ("Walltime",ParameterName.STRING,"04:27:18"), 
                ("Number Of CPUs",ParameterName.NUMERIC,"6.0"),
                ("Maximum virtual memory",ParameterName.NUMERIC,"7537.0"),
                ("Max jobfs disk use",ParameterName.NUMERIC,"2.1")
                 ])
        
        
    def _make_datafile(self,dataset,filename):
        """ Make datafile from filename in given dataset"""
 
        df_file = models.Dataset_File(dataset=dataset,
                                      filename=path.basename(filename),
                                      url=filename,
                                      protocol='staging')
        df_file.save()
        return df_file
 
        
def _get_XML_tag(xml,xpath):
    """ 
    For the given xml string, look for tag with tagtitle and 
    the innertag child and return list of all values
    """
    
    from lxml import etree
    tree = etree.fromstring(xml)
    r = tree.xpath(xpath,
                       namespaces={
            'rifcs':"http://ands.org.au/standards/rif-cs/registryObjects"})
    logger.debug("r=%s" % r)
        
    return r

    
class AuthPublishTest(TestCase):
    """ Tests ability to publish experiment with associated parties and
        authorised activities"""
     
    def setUp(self):
        self.client = Client()
        from django.contrib.auth.models import User
        self.username = 'tardis_user1'
        self.pwd = 'secret'
        email = ''
        self.user = User.objects.create_user(self.username, email, self.pwd)
        self.userprofile = UserProfile(user=self.user)
        party = PartyRecord()
        party.key = "http://www.rmit.edu.au/HPC/1/1"
        party.type = "person"
        np = NameParts()
        np.title="Mr"
        np.given="Joe"
        np.family="Bloggs"
        np.save()
        party.partyname = np
        party.save()
        
        email = PartyLocation()
        email.type ="email"
        email.value="test@email.com"
        email.party = party
        email.save()
        
        
            
        activity = ActivityRecord()
        activity.key="http://www.rmit.edu.au/HPC/3/2"
        activity.ident = activity.key
        activity.type = "project"
        np = NameParts()
        np.title="My Other Secret Project"
        np.save()
        activity.activityname = np
        activity.description = "Next stop, the galaxy"
        
        activity.save()
        
        apr = ActivityPartyRelation()
        apr.activity = activity
        apr.party = party
        
        apr.save()
        
        
        party = PartyRecord()
        party.key = "http://www.rmit.edu.au/HPC/1/2"        
        party.type = "person"
        np = NameParts()
        np.title="Ms"
        np.given="Alice"
        np.family="Smith"
        np.save()
        party.partyname = np
        party.save()
        
        email = PartyLocation()
        email.type ="email"
        email.value="test@email.com"
        email.party = party
        email.save()
        
        activity = ActivityRecord()
        activity.key="http://www.rmit.edu.au/HPC/3/1"
        activity.ident = activity.key
        activity.type = "project"
        np = NameParts()
        np.title="My Secret Project"
        np.save()
        activity.activityname = np
        activity.description = "World Domination"
        
        activity.save()
         
        apr = ActivityPartyRelation()
        apr.activity = activity
        apr.party = party
        
        apr.save()
    
        party = PartyRecord()
        party.key = "http://www.rmit.edu.au/HPC/1/3"        
        party.type = "person"
        np = NameParts()
        np.title="Mr"
        np.given="John"
        np.family="Smith"
        np.save()
        party.partyname = np
        party.save()
            
      
    def tearDown(self):
        from shutil import rmtree
        rmtree(self.experiment_path)
        
    def test_publish(self):
        """ Create an experiment and publish it as RIF-CS using RMITANDSService"""
        login = self.client.login(username=self.username,
                                  password=self.pwd)
        self.assertTrue(login)
        # Create simple experiment
        exp = models.Experiment(title='test exp1',
                                institution_name='rmit',
                                created_by=self.user,
                                public=False
                                )
        exp.save()
        acl = ExperimentACL(
            pluginId=django_user,
            entityId=str(self.user.id),
            experiment=exp,
            canRead=True,
            isOwner=True,
            aclOwnershipType=ExperimentACL.OWNER_OWNED,
            )
        acl.save()
        self.assertEqual(exp.title, 'test exp1')
        self.assertEqual(exp.url, None)
        self.assertEqual(exp.institution_name, 'rmit')
        self.assertEqual(exp.approved, False)
        self.assertEqual(exp.handle, None)
        self.assertEqual(exp.created_by, self.user)
        self.assertEqual(exp.public, False)
        self.assertEqual(exp.get_or_create_directory(),
                         path.join(settings.FILE_STORE_PATH, str(exp.id)))

        self.experiment_path = path.join(settings.FILE_STORE_PATH, str(exp.id))
        # publish
        data = {'legal':'on',
                'activities':[1,2],
                'form-0-party':'3',
                'form-0-relation':'hasCollector',
                'form-TOTAL_FORMS': u'1',
                'form-INITIAL_FORMS': u'0', 'form-MAX_NUM_FORMS': u'',
                 'profile':'default.xml'}
        response = self.client.post("/experiment/view/1/publish/", data)
        self.assertEquals(response.status_code,
                          200)
        logger.debug("response=%s" % response)
        
        
        self.assertEquals(response.context['publish_result'][0]['status'],
                          True)         
        self.assertEquals(response.context['publish_result'][0]['message'],
                          'Experiment ready of publishing, awaiting authorisation by activity managers')
        self.assertEquals(response.context['success'],
                          True)
        
        exp = models.Experiment.objects.get(title="test exp1")
        self.assertEqual(exp.public, False)
        
        auths = PublishAuthorisation.objects.filter(experiment=exp)
       
        auth = auths[0]
        logger.debug("auth=%s" % auth)
        self.assertEquals(auth.status,
                          PublishAuthorisation.PENDING_APPROVAL)
        
        
        # try publishing while awaiting results
        data = {}
        response = self.client.post("/experiment/view/1/publish/", data)
        self.assertEquals(response.status_code,
                          200)
        logger.debug("response=%s" % response)
        
        self.assertEquals(response.context['publish_result'][0]['status'],
                          True)         
        self.assertEquals(response.context['publish_result'][0]['message'],
                          'Experiment is under review')
        self.assertEquals(response.context['success'],
                          False)
        
        
        
        
        # wrong auth
        data={'expid':str(exp.id),
                          'authcode':'invalidkey'}
        logger.debug("data=%s" % data)
        response = self.client.get("/experiment/view/1/publish/",
                                   data)
        updated_auth = PublishAuthorisation.objects.get(id=auth.id)
        self.assertEquals(updated_auth.status,
                          PublishAuthorisation.PENDING_APPROVAL)
        self.assertEquals(response.status_code,
                          200)
        logger.debug("reponse=%s" % response)
        # right auth
        exp = models.Experiment.objects.get(title="test exp1")
        self.assertEqual(exp.public, False)
        
        
        
        data={'expid':str(exp.id),
                          'authcode':auth.auth_key}
        logger.debug("data=%s" % data)
        response = self.client.get("/publishauth/",
                         data)
        updated_auth = PublishAuthorisation.objects.get(id=auth.id)
        self.assertEquals(updated_auth.status,
                          PublishAuthorisation.APPROVED_PUBLIC)
        self.assertEquals(response.status_code,
                          200)
        self.assertEquals(response.context[u'message'],
                          u"Thank you for your approval Mr Joe Bloggs")
        logger.debug("reponse=%s" % response)
        
        
            
        exp = models.Experiment.objects.get(title="test exp1")
        self.assertEqual(exp.public, False)
        
        auth = auths[1]
        logger.debug("auth=%s" % auth)
        self.assertEquals(auth.status,
                          PublishAuthorisation.PENDING_APPROVAL)
        # wrong auth
        data={'expid':str(exp.id),
                          'authcode':'invalidkey'}
        logger.debug("data=%s" % data)
        response = self.client.get("/publishauth/",
                                   data)
        updated_auth = PublishAuthorisation.objects.get(id=auth.id)
        self.assertEquals(updated_auth.status,
                          PublishAuthorisation.PENDING_APPROVAL)
        self.assertEquals(response.status_code,
                          200)
        logger.debug("reponse=%s" % response)
        # right auth
        exp = models.Experiment.objects.get(title="test exp1")
        self.assertEqual(exp.public, False)
        
        data={'expid':str(exp.id),
                          'authcode':auth.auth_key}
        logger.debug("data=%s" % data)
        response = self.client.get("/publishauth/",
                         data)
        updated_auth = PublishAuthorisation.objects.get(id=auth.id)
        self.assertEquals(updated_auth.status,
                          PublishAuthorisation.APPROVED_PUBLIC)
        self.assertEquals(response.status_code,
                          200)
        self.assertEquals(response.context[u'message'],
                          u"Thank you for your approval Ms Alice Smith")
        logger.debug("reponse=%s" % response)
        
        
            
        exp = models.Experiment.objects.get(title="test exp1")
        self.assertEqual(exp.public, True)
         
        data={'expid':str(exp.id),
                          'authcode':auth.auth_key}
        logger.debug("data=%s" % data)
        response = self.client.get("/publishauth/",
                         data)
        updated_auth = PublishAuthorisation.objects.get(id=auth.id)
        self.assertEquals(updated_auth.status,
                          PublishAuthorisation.APPROVED_PUBLIC)
        self.assertEquals(response.status_code,
                          200)
        self.assertEquals(response.context[u'message'],u"Experiment already public")
        logger.debug("reponse=%s" % response)
        
        # check resulting rif-cs
        response = self.client.post("/rif_cs/")
        logger.debug("rifcs response=%s" % response.content)

        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:collection/rifcs:relatedObject[1]/rifcs:key')[0].text,
                   "http://www.rmit.edu.au/HPC/1/3")

        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:collection/rifcs:relatedObject[1]/rifcs:relation')[0].attrib['type'],
                   "hasCollector")
        
        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:collection/rifcs:relatedObject[2]/rifcs:key')[0].text,
                   "http://www.rmit.edu.au/HPC/3/1")


        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:collection/rifcs:relatedObject[2]/rifcs:relation')[0].attrib['type'],
                   "isOutputOf")
        
        
        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:collection/rifcs:relatedObject[3]/rifcs:key')[0].text,
                   "http://www.rmit.edu.au/HPC/3/2")
        

        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:collection/rifcs:relatedObject[3]/rifcs:relation')[0].attrib['type'],
                   "isOutputOf")
        
        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:party/rifcs:identifier')[0].text,
                   "http://www.rmit.edu.au/HPC/1/1")
    
        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:party/rifcs:identifier')[1].text,
                   "http://www.rmit.edu.au/HPC/1/2")
    
        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:party/rifcs:identifier')[2].text,
                   "http://www.rmit.edu.au/HPC/1/3")
    
    
        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:activity/rifcs:identifier')[0].text,
                   "http://www.rmit.edu.au/HPC/3/1")
        
        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:activity/rifcs:relatedObject/rifcs:key')[0].text,
                   "http://www.rmit.edu.au/HPC/1/2")
    
        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:activity/rifcs:relatedObject/rifcs:relation')[0].attrib['type'],
                   "isManagedBy")
    
        
        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:activity/rifcs:identifier')[1].text,
                   "http://www.rmit.edu.au/HPC/3/2")
    
        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:activity/rifcs:relatedObject/rifcs:key')[1].text,
                   "http://www.rmit.edu.au/HPC/1/1")
    
    
        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:activity/rifcs:relatedObject/rifcs:relation')[1].attrib['type'],
                   "isManagedBy")
    
        self.assertEquals(_get_XML_tag(
                   response.content,
                   '//rifcs:collection/rifcs:name/rifcs:namePart')[0].text,
                   "test exp1")
        
        # try to republish
        data = {'legal':'on',
                'activities':[1,2],
                'form-0-party':'3',
                'form-0-relation':'hasCollector',
                'form-TOTAL_FORMS': u'1',
                'form-INITIAL_FORMS': u'0', 'form-MAX_NUM_FORMS': u'',
                 'profile':'default.xml'}
        response = self.client.post("/experiment/view/1/publish/", data)
        
        self.assertEquals(response.context['publish_result'][0]['status'],
                          True)         
        self.assertEquals(response.context['publish_result'][0]['message'],
                          'Experiment is already published')
        self.assertEquals(response.context['success'],
                          False)
         
        self.assertEquals(response.status_code,
                          200)
        logger.debug("response=%s" % response)
 
 
 
class Exp():
    def __init__(self,desc):
        self.description = desc
            
    
    
class DescSplitTest(TestCase):
    """ Tests ability to split description field into brief, full and url sections
        for RIFCS        
    """
    
    def test_simple(self):
        from tardis.apps.hpctardis.publish.rif_cs_profile.rif_cs_PublishProvider import paragraphs
        paras = paragraphs('p1\n\t\np2\t\n\tstill p2\t   \n     \n\tp')
        output = [x for x in paras]    
        self.assertEquals(str(output),"['p1\\n', 'p2\\t\\n\\tstill p2\\t   \\n', '\\tp']")
    
            
    def test_breakupdesc(self):
        from tardis.apps.hpctardis.templatetags.extras import breakup_desc
        exp = Exp('brief\n\t\n'
                                            'link1type:link1url\nlink1desc\t\n\n'
                                            'full1\nfull2\n\n'
                                            'link2type:link2url\nlink2desc\t\n\n'
                                                'full3\n\nfull4')
        res = breakup_desc(exp)
        logger.debug("res=%s" % res)
      
        self.assertEquals(res[0][0],"brief\n")                
        self.assertEquals(res[0][1],[('link1type', 'link1url', 'link1desc\t\n'), ('link2type', 'link2url', 'link2desc\t\n')])
        self.assertEquals(res[0][2],('full1\nfull2\n\n\nfull3\n\n\nfull4',))
    
        
class PrivateDataTest(TestCase):
    
         
    def setUp(self):
        self.client = Client()
        from django.contrib.auth.models import User
        self.username = 'tardis_user1'
        self.pwd = 'secret'
        email = ''
        self.user = User.objects.create_user(self.username, email, self.pwd)
        settings.PRIVATE_DATAFILES = True

    def tearDown(self):
        settings.PRIVATE_DATAFILES= False
        
    def test_download_exp(self):
        login = self.client.login(username=self.username,
                                  password=self.pwd)
        self.assertTrue(login)
        # Create simple experiment
        exp = models.Experiment(title='test exp1',
                                institution_name='rmit',
                                created_by=self.user,
                                public=False
                                )
        exp.save()
        acl = ExperimentACL(
            pluginId=django_user,
            entityId=str(self.user.id),
            experiment=exp,
            canRead=True,
            isOwner=True,
            aclOwnershipType=ExperimentACL.OWNER_OWNED,
            )
        acl.save()
        self.assertEqual(exp.title, 'test exp1')
        self.assertEqual(exp.url, None)
        self.assertEqual(exp.institution_name, 'rmit')
        self.assertEqual(exp.approved, False)
        self.assertEqual(exp.handle, None)
        self.assertEqual(exp.created_by, self.user)
        self.assertEqual(exp.public, False)
        self.assertEqual(exp.get_or_create_directory(),
                         path.join(settings.FILE_STORE_PATH, str(exp.id)))

        response = self.client.get("/download/experiment/%s/zip/" % exp.id)
        
        self.assertEqual(response['Content-Disposition'],
                 'attachment; filename="experiment%s-complete.zip"' % exp.id)
      
      
        self.assertEquals([x.name for x in response.templates
                            if "contact_download" in x.name],
                          [])
        
        exp.public = True
        exp.save()
        
        response = self.client.get("/download/experiment/%s/zip/" % exp.id)
        
        self.assertEquals([x.name for x in response.templates
                            if "contact_download" in x.name],
                          ['hpctardis/contact_download.html'])
                 
                         