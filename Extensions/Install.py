# -*- coding: utf-8 -*-
# $Id: Install.py 835 2007-06-27 15:05:17Z amelung $
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

def setupWorkflow(self, out):
    """
    Assign ECAutoAssignement objects to ec_assignment_workflow.
    """
    
    wf_tool = getToolByName(self, 'portal_workflow')
    
    if 'ec_assignment_workflow' in wf_tool.objectIds():
        wf_tool.setChainForPortalTypes((ECR_NAME,), ECA_WF_NAME)
    
        # in case the workflows have changed, update all workflow-aware objects
        wf_tool.updateRoleMappings()
    
        out.write("Assigned '%s' to %s.\n" % (ECR_TITLE, ECA_WF_NAME))

    else:
        out.write("Failed to assign '%' to %s.\n" % (ECR_TITLE, ECA_WF_NAME))

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
    setupWorkflow(self, out)
    
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
