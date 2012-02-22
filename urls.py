from django.conf.urls.defaults import patterns
#from tardis.urls import urlpatterns as tardisurls
from django.conf import settings

# Create the hpcardis links
urlpatterns = patterns('tardis.apps.hpctardis.views',
                       
    (r'^publish/(?P<experiment_id>\d+)/$', 'publish_experiment'),                
    (r'^rif_cs/$','rif_cs'),
    (r'^publishauth/$','auth_exp_publish'),
    (r'^protocol/$','protocol'),
    (r'^login/$','login'),
    (r'^addfiles/$','addfiles'),
)
  
# FIXME: These links do not work to override default tardis behaviour while hpctardis is child of tardis_portal
# app
 
#urlpatterns += patterns(
#    'tardis.apps.hpctardis.download',
#    (r'^download/datafile/(?P<datafile_id>\d+)/$', 'download_datafile'),
#    (r'^download/experiment/(?P<experiment_id>\d+)/(?P<comptype>[a-z]{3})/$',
#     'download_experiment_alt'),
#    (r'^download/datafiles/$', 'download_datafiles'),
#    (r'^download/datafile/ws/$', 'download_datafile_ws'))

#urlpatterns += patterns(
#    'tardis.apps.hpctardis.views',
#     (r'^parameters/(?P<dataset_file_id>\d+)/$', 'retrieve_parameters'),
#    (r'^ajax/edit_datafile_parameters/(?P<parameterset_id>\d+)/$',
#        'edit_datafile_par'),
#    (r'^ajax/edit_dataset_parameters/(?P<parameterset_id>\d+)/$',
#        'edit_dataset_par'),
#    (r'^ajax/edit_experiment_parameters/(?P<parameterset_id>\d+)/$',
#        'edit_experiment_par'),                        
#    (r'^ajax/add_datafile_parameters/(?P<datafile_id>\d+)/$',
#        'add_datafile_par'),
#    (r'^ajax/add_dataset_parameters/(?P<dataset_id>\d+)/$',
#        'add_dataset_par'),
#    (r'^ajax/add_experiment_parameters/(?P<experiment_id>\d+)/$',
#        'add_experiment_par'),
#    
#    )
 