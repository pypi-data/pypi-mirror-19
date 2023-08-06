from django.contrib import admin

from ovp_admin.modules import *

#from django.core.exceptions import PermissionDenied
#from django.http import HttpResponse, HttpResponseRedirect
#from django.contrib.admin.util import lookup_field
#from django.utils.html import strip_tags
#from django.contrib import messages
#from pyExcelerator import Workbook
#from atados import settings
#from django.utils.html import format_html

#from django.core.urlresolvers import reverse


import ovp_users.models as user
import ovp_projects.models as project
import ovp_organizations.models as organization
#+- import ovp_uploads.models as upload
#+- import ovp_projects.models as project
#+- import ovp_search.models as search_models
#+- import ovp_core.models as core


adm_reg = admin.site._registry
adm_reg[user.User].display_on_main_menu = True
adm_reg[project.Project].display_on_main_menu = True
adm_reg[project.Apply].display_on_main_menu = True
adm_reg[organization.Organization].display_on_main_menu = True


#++ ovp_projects.models.project.Project
#++ ovp_projects.models.apply.apply
#++ ovp_organizations.models.Organization
#++ ovp_users.models.User



#-- django.contrib.auth.models
#-- email_log.models.Email

#- ovp_core.models.skill.Skill
#- ovp_core.models.cause.Cause
#- ovp_core.models.address.GoogleAddress


#+- ovp_projects.models.job.Job
#+- ovp_projects.models.work.Work
#+- ovp_projects.models.job.JobDate
#+- ovp_uploads.models.UploadedImage
