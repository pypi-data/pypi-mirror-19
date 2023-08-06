from faker import Factory


class TestsGenerator:

    def fetch_type(self, file, field):
        fake = Factory.create()
        
        if field["specific_type"] == 'simple_string':
            file.write("'" + fake.word() + "'")
        elif field["specific_type"] == 'sentence_string':
            file.write("'" + fake.sentence(variable_nb_words=True) + "'")
        elif field["specific_type"] == 'text_string':
            file.write("'" + fake.text() + "'")
        elif field["specific_type"] == 'id':
            file.write("'" + fake.md5(raw_output=False) + "'")
        elif field["specific_type"] == 'name':
            file.write("'" + fake.name() + "'")
        elif field["specific_type"] == 'phone_number':
            file.write("'" + fake.phone_number() + "'")
        elif field["specific_type"] == 'user_agent':
            file.write("'" + fake.user_agent() + "'")
        elif field["specific_type"] == 'job':
            file.write("'" + fake.job() + "'")
        elif field["specific_type"] == 'url':
            file.write("'" + fake.url() + "'")
        elif field["specific_type"] == 'email':
            file.write("'" + fake.email() + "'")
        elif field["specific_type"] == 'ipv4':
            file.write("'" + fake.ipv4(network=False) + "'")
        elif field["specific_type"] == 'mac_address':
            file.write("'" + fake.mac_address() + "'")
        elif field["specific_type"] == 'file_name':
            file.write("'" + fake.file_name(category=None, extension=None) + "'")
        elif field["specific_type"] == 'datetime':
            file.write("'" + fake.iso8601(tzinfo=None) + "'")
        elif field["specific_type"] == 'hex_color':
            file.write("'" + fake.hex_color() + "'")
        elif field["specific_type"] == 'rgb_color':
            file.write("'" + fake.rgb_color() + "'")
        elif field["specific_type"] == 'address':
            file.write("'" + fake.address() + "'")
        elif field["specific_type"] == 'postcode':
            file.write("'" + fake.postcode() + "'")
        elif field["specific_type"] == 'state':
            file.write("'" + fake.state() + "'")
        elif field["specific_type"] == 'city':
            file.write("'" + fake.city() + "'")
        elif field["specific_type"] == 'address_number':
            file.write(fake.random_number(digits=None, fix_len=False))
        elif field["specific_type"] == 'street_address':
            file.write("'" + fake.street_address() + "'")
        elif field["specific_type"] == 'state_abbr':
            file.write("'" + fake.state_abbr() + "'")
        elif field["specific_type"] == 'country':
            file.write("'" + fake.country() + "'")
        elif field["specific_type"] == 'country_code':
            file.write("'" + fake.country_code() + "'")
        elif field["specific_type"] == 'boolean':
            file.write(fake.pybool())
        elif field["specific_type"] == 'int':
            file.write(fake.pyint())
        elif field["specific_type"] == 'float':
            file.write(fake.pyfloat(left_digits=None, right_digits=None, positive=False))
        else:
            file.write("Unknown")
