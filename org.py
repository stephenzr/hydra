import sys

__author__ = 'lyle'

import csv


class OrgGraph:

    properties = ('EMPLOYEE','LOCATION','SBU','TITLE','MANAGER','FIRST_NAME','LAST_NAME','LEGAL_ENTITY',
                   'DEPARTMENT','PRODUCT_DESCRIPTION','COMPANY','EMAIL','NETWORK_LOGIN','STATUS','DEVELOPER_FLAG',
                   'ONBOARDING_DATE','ACCOUNT_STRING','TELECOMMUTER','OFFBOARDING_DATE','NICKNAME','TEAM',
                   'DISCRETIONARY_TITLE','DIVISION','COMPUTER_NO','BUSINESS_UNIT')

    dimensions =  ('EMPLOYEE','LOCATION','SBU','TITLE','MANAGER','LEGAL_ENTITY',
                   'DEPARTMENT','PRODUCT_DESCRIPTION','COMPANY','NETWORK_LOGIN','STATUS','DEVELOPER_FLAG',
                   'ONBOARDING_DATE','ACCOUNT_STRING','TELECOMMUTER','OFFBOARDING_DATE','NICKNAME','TEAM',
                   'DISCRETIONARY_TITLE','DIVISION','BUSINESS_UNIT')


    def get_default_nodes(self):
        return self.get_division_nodes()

    def get_default_edges(self):
        return self.get_division_edges()

    def get_default_dimension(self):
        return 'DIVISION'

    def get_division_nodes(self):
        return self.nodes['DIVISION']

    def get_division_edges(self):
        return self.edges['DIVISION']

    def get_legal_nodes(self):
        return self.nodes['LEGAL_ENTITY']

    def get_legal_edges(self):
        return self.edges['LEGAL_ENTITY']

    def get_nodes_for_dimension(self,dimension):
        return self.nodes[dimension]

    def get_edges_for_dimension(self,dimension):
        return self.edges[dimension]

    def get_property_index_for(self,property_name):
        i = 0
        for property in OrgGraph.properties:
            if property == property_name:
                return i
            i = i + 1
        return i

    def __init__(self, filename):
        self.parse_csv(filename)
        self.create_graph()

    def parse_csv(self, filename):
        self.raw_data = {}
        f = open( filename, 'rt')
        try:
            reader = csv.reader(f)
            header = True
            for row in reader:
                if header:
                    header = False
                    continue
                id = row[0]
                if self.raw_data.has_key(id):
                    raise ValueError("duplicate id found in input file: %s" % ( id ))
                self.raw_data[id] = row
        finally:
            f.close()

    def create_graph(self):

        self.nodes = {}
        self.edges = {}
        ids = {}
        for dimension in OrgGraph.dimensions:
            self.nodes[dimension] = {}
            self.edges[dimension] = {}
            ids[dimension] = 1

        self.create_nodes(ids)
        self.create_edges()

    def create_edges(self):
        people_nodes = self.nodes['EMPLOYEE']
        manager_index = self.get_property_index_for('MANAGER')
        for eid in self.raw_data.keys():
            e = self.raw_data[eid]
            manager_id = e[manager_index]
            if not people_nodes.has_key(eid) and people_nodes.has_key(manager_id):
                raise ValueError("couldn't find node")
            employee = people_nodes[eid]
            manager = people_nodes[manager_id]

            people_edges = self.edges['EMPLOYEE']
            key = eid + "~" + manager_id
            people_edges[eid + "~" + manager_id] = {'from': employee, 'to': manager}

            for dimension in OrgGraph.dimensions[1:]:
                e_dimension = employee[dimension]
                m_dimension = manager[dimension]
                dimension_key = e_dimension + "~" + m_dimension
                if not self.edges[dimension].has_key(dimension_key):
                    self.edges[dimension][dimension_key] = {'from': self.nodes[dimension][e_dimension],
                                                            'to': self.nodes[dimension][m_dimension],
                                                            'count': 1}
                else:
                    self.edges[dimension][dimension_key]['count'] += 1

    def create_nodes(self, ids):
        for eid in self.raw_data.keys():
            i = 0
            node = {}
            e = self.raw_data[eid]
            for property in OrgGraph.properties:
                node[property] = e[i]
                i = i + 1
            node['label'] = node['FIRST_NAME'] + node['LAST_NAME']
            node['label'] = node['NICKNAME']
            node['id'] = ids['EMPLOYEE']
            ids['EMPLOYEE'] = ids['EMPLOYEE'] + 1
            self.nodes['EMPLOYEE'][eid] = node

            for dimension in OrgGraph.dimensions[1:]:
                dimension_value = node[dimension]
                if not self.nodes[dimension].has_key(dimension_value):
                    self.nodes[dimension][dimension_value] = {'id': ids[dimension], 'label': dimension_value}
                    ids[dimension] = ids[dimension] + 1
