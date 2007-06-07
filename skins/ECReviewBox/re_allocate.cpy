## Script (Python) "re_allocate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
I18N_DOMAIN = 'eduComponents'

REQUEST  = container.REQUEST
RESPONSE = REQUEST.RESPONSE

# shuffle
context.reAllocate()

status='success'
message = context.translate('Submissions have been re-shuffled.',
                            domain = I18N_DOMAIN)

return state.set(status=status, portal_status_message = message)