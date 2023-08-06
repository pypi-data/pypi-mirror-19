from core.Generator import Generator


class MethodsGenerator(Generator):

    def __init__(self, args):
        self.project = args["project"]
        self.api = args["api"]
        self.data = args["data"]

    def insert_into_file(self):
        pass

    def generate(self):
        methods = open('methods.js', 'a')
        methods.write("import { Meteor } from 'meteor/meteor';\n")
        methods.write("import { ValidatedMethod } from 'meteor/mdg:validated-method';\n")
        methods.write("import { SimpleSchema } from 'meteor/aldeed:simple-schema';\n")
        methods.write("import { DDPRateLimiter } from 'meteor/ddp-rate-limiter';\n")
        methods.write("import { _ } from 'meteor/underscore';\n")
        methods.write("import { check } from 'meteor/check';\n")
        methods.write("import { " + self.data["name"] + " } from './" + self.data["name"] + ".js';\n")

        for met in self.data["methods"]:
            methods.write("\nexport const " + met["name"] + " = new ValidatedMethod({\n")
            methods.write("\tname: '" + self.data["name"] + "." + met["name"] + "',")
            methods.write("\n\n\tvalidate(args) {\n")
            methods.write("\n\t\tcheck(args, {\n")

            number_of_fields = len(self.data["fields"])
            counter = 0
            for field in self.data["fields"]:
                counter += 1
                methods.write("\t\t\t" + field["name"] + ": " + field["type"])
                if counter != number_of_fields:
                    methods.write(",\n")
            methods.write("\n\t\t});\n\n")
            methods.write("\t},\n\n")

            methods.write("\trun(args) {\n")
            methods.write("\t\treturn " + self.data["name"] + "." + met["model_method"] + "(args);")
            methods.write("\n\t}\n")
            methods.write("});\n\n")
        methods.close()
