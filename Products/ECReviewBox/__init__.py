# -*- coding: UTF-8 -*-
# $Id: __init__.py 773 2007-05-21 22:11:07Z amelung $
#
# Copyright (c) 2007 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECReviewBox.
import os, os.path

from Globals import package_home

from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from Products.CMFCore import permissions
from Products.CMFCore.DirectoryView import registerDirectory

# local imports
from Products.ECReviewBox.config import SKINS_DIR, GLOBALS
from Products.ECReviewBox.config import PRODUCT_NAME
from Products.ECReviewBox.config import ADD_PERMISSION

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    """
    """
    # Import Types here to register them
    from Products.ECReviewBox import content

    from AccessControl import ModuleSecurityInfo
    from AccessControl import allow_module, allow_class, allow_type

    content_types, constructors, ftis = process_types(
        listTypes(PRODUCT_NAME),
        PRODUCT_NAME)
    
    utils.ContentInit(
        PRODUCT_NAME + ' Content',
        content_types      = content_types,
        permission         = permissions.AddPortalContent,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
