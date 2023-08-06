# -*- coding: utf-8 -*-
"""
Enables .example directive.

To add new directives, 
1. Reuse "todo_node". DON'T change its name. 
    Make sure 'sphinx.ext.todo' is enabled in the extension list
2. Make a new XXDirective(BaseAdmonition)
3. change self.options['class'] = ['my_directive']
4. direc.insert(0, nodes.title(text=_('MyDirective')))
"""

from docutils import nodes
from docutils.parsers.rst import directives

import sphinx
from sphinx.locale import _
from sphinx.environment import NoUri
from sphinx.util.nodes import set_source_info
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives.admonitions import BaseAdmonition


class todo_node(nodes.Admonition, nodes.Element):
    pass


class ExampleDirective(BaseAdmonition):
    """
    An example entry, displayed (if configured) in the form of an admonition.
    """

    node_class = todo_node
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'class': directives.class_option,
    }

    def run(self):
        if not self.options.get('class'):
            self.options['class'] = ['example']

        (direc,) = super(ExampleDirective, self).run()
        if isinstance(direc, nodes.system_message):
            return [direc]

        direc.insert(0, nodes.title(text=_('Example')))
        set_source_info(self, direc)

        env = self.state.document.settings.env
        targetid = 'index-%s' % env.new_serialno('index')
        targetnode = nodes.target('', '', ids=[targetid])
        return [targetnode, direc]


class ReferencesDirective(BaseAdmonition):
    """
    A direc entry, displayed (if configured) in the form of an admonition.
    """
    node_class = todo_node
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'class': directives.class_option,
    }

    def run(self):
        if not self.options.get('class'):
            self.options['class'] = ['references']

        (direc,) = super(ReferencesDirective, self).run()
        if isinstance(direc, nodes.system_message):
            return [direc]

        direc.insert(0, nodes.title(text=_('References')))
        set_source_info(self, direc)

        env = self.state.document.settings.env
        targetid = 'index-%s' % env.new_serialno('index')
        targetnode = nodes.target('', '', ids=[targetid])
        return [targetnode, direc]

