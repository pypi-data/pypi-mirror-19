from core.Generator import Generator
import os
from subprocess import call


class ProjectGenerator(Generator):

    def __init__(self, args):
        self.project = args['project']

    def generate(self):
        print("Creating Project " + self.project + "...")
        call("meteor create --full " + self.project, shell=True)
        os.chdir(self.project)
        call(['ls', '-la'])

    def insert_into_file(self):
        pass
