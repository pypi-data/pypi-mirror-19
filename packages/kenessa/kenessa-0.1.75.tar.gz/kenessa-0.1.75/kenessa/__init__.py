import json
import os
import kenessa
from check import checker


class Province:
    def __init__(self, identifier):
        self.path = os.path.dirname(kenessa.__file__)
        self.json_province = json.loads(open(self.path + '/json/province.json').read())
        self.json_district = json.loads(open(self.path + '/json/district.json').read())
        self.json_sector = json.loads(open(self.path + '/json/sector.json').read())
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
        if self.identifier == 'all':
            data = []
            for province in self.json_province:
                json_p = {province['name']: []}
                json_d = []
                for district in self.json_district:
                    if province['id'] == district['province_id']:
                        json_d.append(district)

                province['district'] = json_d
                json_p[province['name']].append(province)

                data.append(json_p)
            return data
        else:
            data = {}
            province = Province(self.identifier).province()
            if province is None:
                return None
            data['id'] = province['id']
            data['name'] = province['name']
            data['code'] = province['code']

            json_p = {data['name']: []}
            json_d = []

            for district in self.json_district:
                if data['id'] == district['province_id']:
                    json_d.append(district)
            data['district'] = json_d
            json_p[data['name']].append(data)

            return json_p

    def sector(self):
        if self.identifier == 'all':
            data = []
            for province in self.json_province:
                json_p = {province['name']: []}
                data_district = []
                for district in self.json_district:
                    if province['id'] == district['province_id']:
                        json_d = {district['name']:[]}
                        json_c = []
                        for sector in self.json_sector:
                            if district['id'] == sector['district_id']:
                                json_c.append(sector)
                        district['sector'] = json_c
                        json_d[district['name']].append(district)
                        data_district.append(json_d)
                        province['district'] = data_district
                json_p[province['name']].append(province)
                data.append(json_p)

            return data
        else:
            data = {}
            province = Province(self.identifier).province()
            if province is None:
                return None
            data['id'] = province['id']
            data['name'] = province['name']
            data['code'] = province['code']
            json_p = {data['name']: []}

            data_district = []
            for district in self.json_district:
                if district['province_id'] == data['id']:
                    json_d = {district['name']: []}
                    json_c = []
                    for sector in self.json_sector:
                        if sector['district_id'] == district['id']:
                            json_c.append(sector)
                    district['sector'] = json_c
                    json_d[district['name']].append(district)
                    data_district.append(json_d)
            data['district'] = data_district
            json_p[data['name']].append(data)

            return json_p


class District(Province):
    def district(self):
        self.identifier, params = checker(self.identifier)
        if params == 'all':
            return self.district()
        else:

            for district in self.json_district:
                try:
                    if district[params].lower() == self.identifier.lower():
                        return district
                except AttributeError:
                    if district[params] == self.identifier:
                        return district

            return None

    def sector(self):
        self.identifier, params = checker(self.identifier)
        if params == 'all':
            data = []
            for district in self.json_district:
                json_d = {district['name']: []}
                district['sector'] = ''
                json_c = []
                for sector in self.json_sector:
                    if district['id'] == sector['district_id']:
                        json_c.append(sector)

                district['sector'] = json_c
                json_d[district['name']].append(district)

                data.append(json_d)
            return data
        else:
            data = {}
            district = District(self.identifier).district()
            if district is None:
                return None
            data['id'] = district['id']
            data['name'] = district['name']
            data['code'] = district['code']

            json_d = {data['name']: []}
            json_c = []

            for sector in self.json_sector:
                if data['id'] == sector['district_id']:
                    json_c.append(sector)

            data['sector'] = json_c
            json_d[data['name']].append(data)

            return json_d


