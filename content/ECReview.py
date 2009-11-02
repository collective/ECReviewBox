# -*- coding: utf-8 -*-
# $Id: ECReview.py 835 2007-06-27 15:05:17Z amelung $
#
# Copyright (c) 2007 Otto-von-Guericke-University, Magdeburg
#
# This file is part of ECReviewBox.

# Pythone imports

# Zope imports
from AccessControl import Unauthorized
from AccessControl.SecurityManagement import getSecurityManager, setSecurityManager, newSecurityManager

# Plone imports
from Products.CMFPlone.utils import log_exc, log
from Products.ATContentTypes.content.base import updateActions, updateAliases
from Products.Archetypes.atapi import registerType

from AccessControl import ClassSecurityInfo

# Other product imports

# Local product imports
from Products.ECReviewBox.config import *
from Products.ECAssignmentBox.ECAssignment import ECAssignment

class ECReview(ECAssignment):
    """Submission to a review box."""

    __implements__ = (ECAssignment.__implements__,)
    security = ClassSecurityInfo()

    #schema = ECAssignment.schema
    portal_type = meta_type = ECR_META
    archetype_name = ECR_TITLE

    default_view   = 'ecr_view'
    immediate_view = 'ecr_view'

    typeDescription = "A submission to a review box."
    typeDescMsgId = 'description_edit_ecr'

    # -- actions --------------------------------------------------------------
    actions = updateActions(ECAssignment, (
        {
        'action':      "string:$object_url/ecr_grade",
        'category':    "object",
        'id':          'grade',
        'name':        'Grade',
        'permissions': (permissions.ModifyPortalContent,),
        'condition':   'python:1'
        },
        ))

    aliases = updateAliases(ECAssignment, {
        'view': 'ecr_view',
        'grade': 'ecr_grade',
        })


    # -- methods --------------------------------------------------------------

registerType(ECReview, PRODUCT_NAME)
