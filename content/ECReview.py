# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2005 Otto-von-Guericke-University, Magdeburg
#
# This file is part of ECAutoAssessmentBox.

# Pythone imports

# Zope imports
from AccessControl import Unauthorized
from AccessControl.SecurityManagement import getSecurityManager, setSecurityManager, newSecurityManager

# Plone imports
from Products.CMFPlone.utils import log_exc, log
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.base import updateActions, updateAliases

from AccessControl import ClassSecurityInfo

# Other product imports

# Local product imports
from Products.ECReviewBox.config import *
from Products.ECAssignmentBox.ECAssignment import ECAssignment

class ECReview(ECAssignment):
    """Submission to a review box."""

    __implements__ = (ECAssignment.__implements__,)
    security = ClassSecurityInfo()

    schema = ECAssignment.schema
    portal_type = meta_type = ECR_META
    archetype_name = ECR_TITLE

    default_view   = 'ecr_view'
    immediate_view = 'ecr_view'

    filter_content_types = 1
    allowed_content_types = [ECAssignment.meta_type]

    # -- actions --------------------------------------------------------------
    aliases = updateAliases(ECAssignment, {
        'view': 'ecr_view',
        })


    # -- methods --------------------------------------------------------------

registerATCT(ECReview, PRODUCT_NAME)
