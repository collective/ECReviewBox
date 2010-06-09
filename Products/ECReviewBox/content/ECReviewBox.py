# -*- coding: utf-8 -*-
# $Id: ECReviewBox.py 835 2007-06-27 15:05:17Z amelung $
#
# Copyright (c) 2007 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECReviewBox.
from random import randint
from random import (randint, shuffle)

# Zope imports
from AccessControl import ClassSecurityInfo
from DateTime import DateTime

# Plone imports
from Products.Archetypes.atapi import *

#from Products.Archetypes.public import BooleanField
#from Products.Archetypes.public import ReferenceField

#from Products.Archetypes.public import BooleanWidget
#from Products.Archetypes.public import ReferenceWidget

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import log_exc, log

# Other product imports
from Products.ECAssignmentBox.ECAssignmentBox import ECAssignmentBox
from Products.ECAssignmentBox.ECAssignmentBox import ECAssignmentBox_schema
from Products.ECAssignmentBox import permissions

from Products.ECAutoAssessmentBox.ECAutoAssessmentBox import ECAutoAssessmentBox

# DataGridField imports
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn


# Local product imports
from Products.ECReviewBox.config import *
from Products.ECReviewBox.content.ECReview import *

try:
    # use ECAssignmentBox's schema and modifiy it
    ECReviewBoxSchema = ECAssignmentBox_schema.copy() 
    
    # we hide the field assignment_reference because it is
    # unsuitable for review boxes
    ECReviewBoxSchema['assignment_reference'].widget.visible = {
        'view' : 'invisible',
        'edit' : 'invisible'
    }
except Exception, e:
    pass

ECReviewBoxSchema = Schema((

    ReferenceField(
        'referencedBox',
        allowed_types = (ECAssignmentBox.meta_type, ECAutoAssessmentBox.meta_type),
        #allowed_types_method = 'getAllowedRefTypes',
        multiValued = False,
        required = True,
        relationship = 'RelReference',
        #searchable = True,
        widget = ReferenceBrowserWidget(
            label_msgid='label_reference_box',
            label='Referenced assignment box',
            description_msgid='help_reference_box',
            description=
                'All submissions inside selected assignment box which are ' +
                'in a state that the container of this review box considers ' +
                'as a completed state will be used for the peer review.',
            i18n_domain=I18N_DOMAIN,
            allow_search = True,
            show_indexes = False,
        ),
    ),

    DataGridField(
        'allocations',
        columns = ('user', 'orig_user', 'orig_path', 'orig_submission', ),
        #required = True,
        searchable = False,
        widget = DataGridWidget(
            modes = ('view'),
            #visible = {'view':'invisible', 'edit':'invisible'},
            label_msgid = 'label_allocations',
            label = "Allocated assignments",
            description_msgid = 'help_allocations',
            description = """Shows users and allocated assignments from the referenced box""",
            i18n_domain = I18N_DOMAIN,
            columns = {
                'user':Column("Reviewer"),
                'orig_user':Column("Original user"),
                'orig_path':Column("Original path"),
                'orig_submission':Column("Original submission"),
                #'xyz':SelectColumn("Xyz", vocabulary="getXyzVocab"),
            },
        ),
        # let only box owner and manager read the data grid 
        read_permission = permissions.ModifyPortalContent,
    ),

    BooleanField(
        'origAsAnswer',
        default = False,
        #required = True,
        widget = BooleanWidget(
            label = 'Use original assignment as answer template',
            label_msgid = 'label_orig_as_answer',
            description = 'If selected, the original assignments will be automaticly pasted as answer templates inside this box',
            description_msgid = 'help_orig_as_answer',
            i18n_domain = I18N_DOMAIN,
        ),
        read_permission = permissions.ModifyPortalContent,
    ),

)) + ECReviewBoxSchema

#finalizeATCTSchema(ECReviewBoxSchema, folderish=True, moveDiscussion=False)
finalizeATCTSchema(ECReviewBoxSchema, folderish=True,)


class ECReviewBox(ECAssignmentBox):
    """Assignments for peer reviewing"""

    __implements__ = (ECAssignmentBox.__implements__,)
    security = ClassSecurityInfo()

    schema = ECReviewBoxSchema

    portal_type = meta_type = ECRB_META
    archetype_name = ECRB_TITLE
    content_icon = ECRB_ICON

    typeDescription = 'Enables the creation of online assignments for peer reviewing'
    typeDescMsgId = 'description_edit_ecrb'

    _at_rename_after_creation = True

    filter_content_types = 1
    allowed_content_types = [ECReview.meta_type]


    # overwrite the archetypes edit method
    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, item, container):
        """
        """
        BaseFolder.manage_afterAdd(self, item, container)

        referencedBox  = self.getReferencedBox()
       
        self.completedStates = container.completedStates
        if referencedBox and not self.allocations:
            self._allocate(referencedBox)

            
    security.declarePublic('availableReviews')
    def availableReviews(self):
        """
        Returns a dictionary of all available, unsuperseded reviews in this
        review box. Each dictionary key is the original user, i.e. the name
        of the user who submitted the reviewed assignment in the referenced
        assignment box. Each item is itself a dictionary with the two keys
        'solution' and 'review', the former being the original submitted
        solution in the referenced assignment box and the latter being the
        corresponding review.
        """
        result = {}
        wft = getToolByName(self, 'portal_workflow')
        children = self.getChildNodes()
        for c in children:
            if wft.getInfoFor(c, 'review_state') == 'superseded': continue
            u = c.getOwner().getId()
            ou = c.getAllocatedSubmission(u)[0]['orig_user']
            solution = c.getAllocatedSubmission(u)[0]['orig_submission']
            review = str(c.get_data())
            result[ou] = {'solution': solution, 'review': review}
        return result


    security.declarePublic('gist')
    def gist(self, text):
        """
        Shortens text to the first 47 characters of it's first line and adds
        an ellipsis. Tries to cut text at word boundaries so the gist doesn't
        end with an incomplete word.
        TODO: Move this function somewhere else because it doesn't belong here.
        """
        if text.isspace(): return ""
        line = filter(
            lambda x: not x.isspace() and len(x) > 0,
            text.splitlines()
        )[0]
        if len(line) <= 50: return line
        gist = line[0:47]
        gistend = gist.split()[-1]
        words = len(gist.split())
        last_word = line.split()[words-1]
        if gistend == last_word or words == 1: return gist.rstrip() + u'...'
        return gist.rstrip(last_word).rstrip() + u'...'
        

    security.declarePublic('getAllocatedSubmission')
    def getAllocatedSubmission(self, user_id):
        """
        Return the submission text for the given user or None, if user_id 
        isn't in the list of enabled users.
        """
        datagrid = self.getField('allocations')
        
        return datagrid.search(self, user=user_id)


    security.declarePublic('getOrigAsAnswer')
    def getOrigAsAnswer(self): return self.origAsAnswer


    security.declareProtected(permissions.ModifyPortalContent, 'reAllocate')
    def reAllocate(self):
        """
        TODO:
        """
        return self._allocate(self.getReferencedBox())
    

    security.declarePrivate('_allocate')
    def _allocate(self, referencedBox):
        """
        Get all assignments in the referenced assignment box which are in a
        completed state and re-assign each submission to a new user.

        @param referencedBox: the referenced assignment box
        """
        
        if not referencedBox:
            log('referencedBox is %s' % repr(referencedBox))
            return
        
        #log('referencedBox: %s' % repr(referencedBox.getPhysicalPath()))

        # lets use the catalog to get all assignments inside the referenced 
        # assignment box
        catalog = getToolByName(self, 'portal_catalog')
    
        brains = catalog.searchResults(
            path = {'query':'/'.join(referencedBox.getPhysicalPath()), 'depth':1,},
        )
        
        # reset current allocations    
        self.allocations = []
        
        users = []
        submissions = []
        subsBackup = []
        
        # walk through all submissions
        for brain in brains:
            # get creator's unique name
            creator = brain.Creator
            # add all user to a separate list, this means everyone who submitted
            # an assignment takes part at the peer review
            users.append(creator)

            # filter only accepted or graded assignments
            if brain.review_state in self.completedStates:
                # get the real object
                assignment = brain.getObject()
                
                #path = (hasattr(assignment, 'getPath') and assignment.getPath()) or '/'.join(assignment.getPhysicalPath())
                path = '/'.join(assignment.getPhysicalPath())

                #answer = assignment.getAsPlainText()
                answer = str(assignment.get_data())

                #log('creator: %s' % creator)
                #log('path: %s' % path)
                #log('answer: %s' % answer)

                # allow readable submissions only
                if answer:
                    # add all users and submission to another list
                    submissions.append({'orig_user': creator, 
                                        'orig_path': path, 
                                        'orig_submission': answer,
                                        })
                    
        if len(submissions)==0:
            messenger = getToolByName(self, 'plone_utils')
            messenger.addPortalMessage(_(u"""
                No submissions eligible for a peer review where found
                inside the referenced assignment box."""),
                'error')
            messenger.addPortalMessage(_(u"""
                Please check whether the referenced assignment box contains any
                submissions which the container that this review box resides in
                considers as being in a completed state, delete the created
                review box and try again in a different container, with
                different settings or with a different assignment box."""))
            return

        # ensure that 'users' is a list of unique names
        users = dict(map(lambda i: (i, 1), users)).keys()
        #log('unique user list: %s' % repr(users))

        # lets dice: user 1 gets the submission of user 2 and so on; the last 
        # user in the list finally gets the original submission of user 1
        allocations = []
        
        # prevent neverending loop if only one submission exists
        if len(submissions) == 1:
            row = submissions.pop(0)
            row['user'] = users[0]
            allocations.append(row)
        # in any other case: lets roll the dices
        else:
            
            for user in users:
                
                #log('user: %s' % user)
                #log('len(submissions): %s' % len(submissions))
                
                if len(submissions) == 0:
                    submissions = subsBackup
                    subsBackup = []

                row = submissions.pop(randint(0, len(submissions)-1))
                
                
                # ensure that no user gets his/her own original submission
                if user == row['orig_user']:
                    #log('len(submissions) = %s' % len(submissions))
                    row2 = submissions.pop(randint(0, len(submissions)-1))
                    submissions.append(row.copy())
                    row = row2    
                    
                    
                # ensure that the last remaining pair won't match
                elif len(submissions) == 1:
                    
                    log('users[len(users)-1] = %s' % users[len(users)-1])
                    log('submissions[0]["orig_user"] = %s' % submissions[0]['orig_user'])
                    
                    if users[len(users)-1] == submissions[0]['orig_user']:
                        submissions.append(row.copy())
                        row = submissions.pop(0)                    
                
                subsBackup.append(row.copy())        
                
                row['user'] = user
                allocations.append(row)

        self.getField('allocations').set(self, allocations)

        # that's all there is to it!
        return
            

registerType(ECReviewBox, PRODUCT_NAME)
