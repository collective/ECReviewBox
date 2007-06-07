# -*- coding: UTF-8 -*-
# $Id$
#
# Copyright (c) 2007 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECReviewBox.
#
# ECReviewBox is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# ECReviewBox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ECReviewBox; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from Products.Archetypes.public import DisplayList
from Products.CMFCore import permissions

GLOBALS = globals()

I18N_DOMAIN = 'eduComponents'

# define skins directory
SKINS_DIR = 'skins'

# define dependencies
DEPENDENCIES = ['ECAssignmentBox', 'DataGridField']

# define product, tool names and icons
PRODUCT_NAME = 'ECReviewBox'

ECRB_NAME  = 'ECReviewBox'
ECRB_TITLE = 'Peer-Review Box'
ECRB_META  = ECRB_NAME
ECRB_ICON  = 'ecrb.png'

ECR_NAME  = 'ECReview'
ECR_TITLE = 'Peer-Review'
ECR_META  = ECR_NAME
#ECR_ICON  = 'ecr.png'

# define permissions
ACCESS_PERMISSION = permissions.AccessContentsInformation
VIEW_PERMISSION   = permissions.View
MODIFY_PERMISSION = permissions.ModifyPortalContent
ADD_PERMISSION    = permissions.AddPortalContent
MANAGE_PERMISSION = permissions.ManageProperties
