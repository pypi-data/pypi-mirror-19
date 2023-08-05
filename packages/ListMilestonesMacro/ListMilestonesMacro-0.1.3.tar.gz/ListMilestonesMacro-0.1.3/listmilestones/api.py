from trac.wiki.macros import WikiMacroBase, parse_args
from trac.ticket.model import Milestone
from trac.web.chrome import Chrome
from trac.web.main import RequestDispatcher
from trac.util.html import Markup
from trac.web.chrome import ITemplateProvider
from trac.core import *

class ListMilestonesMacro(WikiMacroBase):
    """
    Shows a list of chosen Milestones.

    Examples:

    {{{
        [[ListMilestones()]]               # Show all milestones
        [[ListMilestones(Product)]]        # Show milestones whose name starts with Product
        [[ListMilestones(Product, Test)]]  # Show milestones whose name starts with Product and Test
    }}}
    """

    implements(ITemplateProvider)

    def expand_macro(self, formatter, name, content):
        args, kwargs = parse_args(content, strict=False)

        milestones = filter(lambda m: not args or any(map(lambda a: m.name.startswith(a), args)), Milestone.select(self.env))

        req = formatter.req
        template = "listmilestones.html"
        data = {'milestones' : milestones}
        content_type = 'text/html'

        dispatcher = RequestDispatcher(self.env)
        response = dispatcher._post_process_request(req, template, data, content_type)

        # API < 1.1.2 does not return a method.
        if (len(response) == 3):
            template, data, content_type = response
            return Markup(Chrome(self.env).render_template(formatter.req, template, data, content_type=content_type, fragment=True))

        template, data, content_type, method = response
        return Markup(Chrome(self.env).render_template(formatter.req, template, data, content_type=content_type, fragment=True, method=method))

    def get_templates_dirs(self):
        from pkg_resources import resource_filename
        return [resource_filename(__name__, 'templates')]

    def get_htdocs_dirs(self):
        return []
