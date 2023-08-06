from core.Generator import Generator
from core.TestsGenerator import TestsGenerator
from faker import Factory


class ModelTestsGenerator(Generator, TestsGenerator):

    def __init__(self, args):
        self.project = args["project"]
        self.api = args["api"]
        self.data = args["data"]

    def insert_into_file(self):
        pass

    def generate(self):
        fake = Factory.create()
        model_tests_file = open(self.api + '.tests.js', 'a')
        model_tests_file.write("import { Meteor } from 'meteor/meteor';")
        model_tests_file.write("\nimport { assert } from 'meteor/practicalmeteor:chai';")
        model_tests_file.write("\nimport { " + self.api + " } from './" + self.api + ".js';")
        model_tests_file.write("\n")
        model_tests_file.write("\nif (Meteor.isServer) {")
        model_tests_file.write("\n\tdescribe('" + self.api + " collection', () => {")

        for methods in self.data["model"]:
            model_tests_file.write("\n")
            model_tests_file.write("\n\t\tit( '" + methods["name"] + " correctly' , () => {")
            model_tests_file.write("\n\t\t\tconst " + self.api + "Id = " + self.api + "." + methods["mongo_op"] + "({")

            for fields in self.data["fields"]:
                model_tests_file.write("\n\t\t\t\t" + fields["name"] + ": ")
                super(ModelTestsGenerator, self).fetch_type(model_tests_file, fields)
                model_tests_file.write(", ")

            model_tests_file.write("\n\t\t\t});")
            model_tests_file.write("\n\t\t\tconst result = " + self.api + ".find({ _id: " + self.api + "Id });")
            model_tests_file.write("\n\t\t\tconst collectionName = result._getCollectionName();")
            model_tests_file.write("\n\t\t\tconst count = result.count();")
            model_tests_file.write("\n\n\t\t\tassert.equal(collectionName, '" + self.api + "');")
            model_tests_file.write("\n\t\t\tassert.equal(count, 1);")
            model_tests_file.write("\n\t\t});")

        model_tests_file.write("\n\t});")
        model_tests_file.write("\n}")
