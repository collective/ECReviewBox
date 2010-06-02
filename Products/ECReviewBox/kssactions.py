from kss.core import KSSView, kssaction


class ReviewTable(KSSView):
  
    @kssaction
    def toggleRow(self, id, state, index):
        core = self.getCommandSet('core')
        toggle = u'#%s' % id
        expanded = u'.expanded.row%s' % index
        collapsed = u'.collapsed.row%s'% index
        if state == u'collapsed':
            alt = u'collapse row'
            src = u'Expanded'
            core.setStyle(collapsed, "display", "none")
            core.setStyle(expanded, "display", "block")
        else:
            alt = u'expand row'
            src = u'Collapsed'
            core.setStyle(collapsed, "display", "block")
            core.setStyle(expanded, "display", "none")
        core.setAttribute(toggle, "src", "tree%s.gif" % src)
        core.setAttribute(toggle, "alt", alt)
        for s in [u'collapsed', u'expanded']:
            core.toggleClass(toggle, u'kssattr-state-' + s)
        return self.render()

