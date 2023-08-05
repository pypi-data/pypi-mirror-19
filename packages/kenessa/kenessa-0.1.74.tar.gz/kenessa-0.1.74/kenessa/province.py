import json
import os
import kenessa


class Province:
    def __init__(self, identifier):
        self.path = os.path.dirname(kenessa.__file__)
        self.json_province = json.loads(open(self.path + '/json/province.json').read())
        self.identifier = str(identifier).replace(" ", "")

    def province(self):
        if self.identifier == 'all':
            return self.json_province
        else:
            for province in self.json_province:
                keywords = province['keywords']
                keywords = [keyword.lower() for keyword in keywords]
                if self.identifier.lower() in keywords:
                    return province

            return None

    def district(self):
        pass



