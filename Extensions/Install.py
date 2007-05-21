# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2007 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECReviewBox.

from StringIO import StringIO

from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.Archetypes.public import listTypes

from Products.CMFCore.utils import getToolByName

from Products.ECReviewBox.config import *

def installDependencies(self, out):
    """
    Tests wether or not depending products are available and installed. If 
    not, we will try to install them.
    """
    qi = getToolByName(self, 'portal_quickinstaller')
    for product in DEPENDENCIES:
        if qi.isProductInstallable(product):
            if not qi.isProductInstalled(product):
                qi.installProduct(product)
        else:
            out.write("Warnig: Depending product '%s' ist not installable." %
                      product)


def install(self):
    """
    Installs the product.
    """
    out = StringIO()

    # install depending products
    installDependencies(self, out)

    # install types
    installTypes(self, out, listTypes(PRODUCT_NAME), PRODUCT_NAME)

    # install subskins
    install_subskin(self, out, GLOBALS)

    # install workflows
    
    # install tools

    # register tool to Plone's preferences panel

    # enable portal_factory for given types
    factory_tool = getToolByName(self, 'portal_factory')
    factory_types=[
        ECRB_NAME,
        ] + factory_tool.getFactoryTypes().keys()
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=factory_types)

    print >> out, "Successfully installed %s." % PRODUCT_NAME
    return out.getvalue()


def uninstall(self, reinstall):
    """ 
    Uninstalls the product.
    """
    out = StringIO()
       
    print >> out, "Successfully uninstalled %s." % PRODUCT_NAME
    return out.getvalue()
