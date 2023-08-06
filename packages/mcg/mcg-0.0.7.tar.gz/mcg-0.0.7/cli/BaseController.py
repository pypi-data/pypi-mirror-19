from cement.core.controller import CementBaseController, expose
from core.Manager import Manager

VERSION = '0.0.7'

BANNER = """
Meteor Crud Generator v%s
Copyright (c) 2017 Bizarro Solutions
""" % VERSION


class BaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'MCG generates backend and unit tests for a Meteor Application'
        epilog = "Suggestions or bugs must be reported to info@bizarro.solutions"

        arguments = [
            (['-v', '--version'],
             dict(action='version', version=BANNER)),
            (['-p', '--project'],
             dict(help='Option to create a Meteor Project')),
            (['-a', '--api'],
             dict(help='Option to create a Meteor Api'))
            ]

    @expose(hide=True, aliases=['run'])
    def default(self):
        self.app.log.info("Run command. [default] Function")

    @expose(help="Create command. [create] Function")
    def create(self):
        manager = Manager({"project": self.app.pargs.project, "api": self.app.pargs.api})
        manager.begin()
