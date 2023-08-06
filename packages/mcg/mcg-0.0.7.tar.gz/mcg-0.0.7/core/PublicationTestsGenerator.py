from core.Generator import Generator
from core.TestsGenerator import TestsGenerator
from faker import Factory


class PublicationTestsGenerator(Generator, TestsGenerator):

    def __init__(self, args):
        self.project = args["project"]
        self.api = args["api"]
        self.data = args["data"]

    def insert_into_file(self):
        pass

    def generate(self):
        fake = Factory.create()
        publication_tests = open('publications.tests.js', 'a')
        publication_tests.write("import { Meteor } from 'meteor/meteor';")
        publication_tests.write("\nimport { " + self.api + " } from '../" + self.api + ".js';")
        publication_tests.write("\nimport { assert } from 'meteor/practicalmeteor:chai';")
        publication_tests.write("\nimport { PublicationCollector } from 'meteor/johanbrook:publication-collector';")
        publication_tests.write("\nimport './publications.js';")
        publication_tests.write("\n")
        publication_tests.write("\ndescribe('" + self.api + " publications', () => {")

        # BeforeEach
        publication_tests.write("\n")
        publication_tests.write("\n\tbeforeEach(() => {")
        publication_tests.write("\n\t\t" + self.api + ".remove({});")
        publication_tests.write("\n\t\t" + self.api + ".insert({")
        
        for fields in self.data["fields"]:
            publication_tests.write("\n\t\t\t" + fields["name"] + ": ")
            super(PublicationTestsGenerator, self).fetch_type(publication_tests, fields)
            publication_tests.write(", ")
        
        publication_tests.write("\n\t\t});")
        publication_tests.write("\n\t});")

        # Describes Publications
        for pub in self.data["publications"]:
            publication_tests.write("\n")
            publication_tests.write("\n\tdescribe('" + pub["name"] + "', () => {")
            publication_tests.write("\n\t\tit('sends all " + self.api + "', (done) => {")
            publication_tests.write("\n\t\t\tconst collector = new PublicationCollector();")
            publication_tests.write("\n\t\t\tcollector.collect('" + pub["name"] + "', (collections) => {")
            publication_tests.write("\n\t\t\t\tassert.equal(collections." + self.api + ".length, 1);")
            publication_tests.write("\n\t\t\t\tdone();")
            publication_tests.write("\n\t\t\t});")
            publication_tests.write("\n\t\t});")
            publication_tests.write("\n\t});")

        publication_tests.write("\n});")
