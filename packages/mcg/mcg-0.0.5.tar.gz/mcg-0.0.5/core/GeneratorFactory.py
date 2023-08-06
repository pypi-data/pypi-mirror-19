from core.ProjectGenerator import ProjectGenerator
from core.ModelGenerator import ModelGenerator
from core.ModelTestsGenerator import ModelTestsGenerator
from core.MethodsGenerator import MethodsGenerator
from core.MethodsTestsGenerator import MethodsTestsGenerator
from core.PublicationGenerator import PublicationGenerator
from core.PublicationTestsGenerator import PublicationTestsGenerator


class GeneratorFactory(object):

    def generate_file(self, object_type, args):
        return eval(object_type)(args).generate()
