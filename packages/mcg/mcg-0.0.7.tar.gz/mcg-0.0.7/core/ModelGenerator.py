from core.Generator import Generator


class ModelGenerator(Generator):

    def __init__(self, args):
        self.project = args["project"]
        self.api = args["api"]
        self.data = args["data"]

    def insert_into_file(self):
        pass

    def generate(self):
        model_file = open(self.api + '.js', 'a')
        model_file.write("import { Meteor } from 'meteor/meteor';\n")
        model_file.write("import { Mongo } from 'meteor/mongo';\n")
        model_file.write("\nclass " + self.data["name"].title() + "Collection extends Mongo.Collection\n")
        model_file.write("{\n")

        for model_method in self.data["model"]:
            model_file.write("\n\t" + model_method["name"] + "(")

            params_len = len(model_method["params_received"])
            counter = 0
            for param in model_method["params_received"]:
                counter += 1
                if counter != params_len:
                    model_file.write(param + ", ")
                else:
                    model_file.write(param)

            model_file.write(")\n")
            model_file.write("\t{")
            model_file.write("\n\t\treturn super." + model_method["mongo_op"] + "(")

            params_len = len(model_method["params_passed"])
            counter = 0
            for param in model_method["params_passed"]:
                counter += 1
                if counter != params_len:
                    model_file.write(param + ", ")
                else:
                    model_file.write(param)

            model_file.write(");\n")
            model_file.write("\t}\n\n")

        model_file.write("}\n\n")
        model_file.write("export const " + self.data["name"] +
                         " = new " + self.data["name"].title() + "Collection('" + self.data["name"] + "');")
        model_file.close()
