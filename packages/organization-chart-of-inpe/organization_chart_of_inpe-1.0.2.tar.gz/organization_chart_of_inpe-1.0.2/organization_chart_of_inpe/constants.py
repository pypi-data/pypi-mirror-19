#!/usr/bin/env python
# -*- coding: utf-8 -*-


class OrganizationChartOfINPE:
    __ORGANIZATION_CHART_OF_INPE__ = {
        "CTE": ["LAC", "LAS", "LAP", "LCP"],
        "LIT": [],
        "ETE": ["DSS", "DEA", "DMC", "DSE"],
        "OBT": ["DGI", "DSR", "DPI"],
        "CPT": ["DMD", "DSA", "DOP"],
        "CEA": ["DAE", "DAS", "DGE", "SLB"],

        "CRH": [],  # civil servant inactive
    }

    __EXTERNAL_INSTITUTION__ = {
        "UNIFESP": [],
        "CEMADEN": [],
        "CTA": ["IEAV"],
    }

    __GRADUATE_PROGRAM__ = [
        "CAP",
    ]

    def is_key_a_division(self, key):
        key = str(key).strip().upper()

        # search if the key is part of the INPE
        for coordination in self.__ORGANIZATION_CHART_OF_INPE__:
            if coordination == key:
                return True

        for coordination in self.__ORGANIZATION_CHART_OF_INPE__:
            divisions = self.__ORGANIZATION_CHART_OF_INPE__[coordination]
            if key in divisions:
                return True

        # search if the key is part of the external institution
        for external_institution in self.__EXTERNAL_INSTITUTION__:
            if external_institution == key:
                return True

        for external_institution in self.__EXTERNAL_INSTITUTION__:
            divisions = self.__EXTERNAL_INSTITUTION__[external_institution]
            if key in divisions:
                return True

        # search if the key is part of graduate program
        for graduate_program in self.__GRADUATE_PROGRAM__:
            if graduate_program == key:
                return True

        return False

    def is_key_a_coordination(self, key):
        key = str(key).strip().upper()

        if key in self.__ORGANIZATION_CHART_OF_INPE__.keys():
            return True

        # CTA conta como coordenação por ter subdivisao, como UNIFESP e CEMADEN não tem divisao, entao nao conta
        if key == "CTA":
            return True

        # if key in self.__EXTERNAL_INSTITUTION__.keys():
        #     return True

        return False

    def get_full_name_of_division_by_key(self, keys):
        keys = str(keys).replace(" ", "").upper().split(",")
        affiliations = []

        for key in keys:
            # search if the key is part of the INPE
            for coordination in self.__ORGANIZATION_CHART_OF_INPE__:
                if coordination == key:
                    affiliations.append(coordination)

            for coordination in self.__ORGANIZATION_CHART_OF_INPE__:
                divisions = self.__ORGANIZATION_CHART_OF_INPE__[coordination]
                if key in divisions:
                    affiliations.append(coordination)
                    affiliations.append(key)

            # search if the key is part of the external institution
            for external_institution in self.__EXTERNAL_INSTITUTION__:
                if external_institution == key:
                    affiliations.append(external_institution)

            for external_institution in self.__EXTERNAL_INSTITUTION__:
                divisions = self.__EXTERNAL_INSTITUTION__[external_institution]
                if key in divisions:
                    affiliations.append(external_institution)
                    affiliations.append(key)

            # search if the key is part of graduate program
            for graduate_program in self.__GRADUATE_PROGRAM__:
                if graduate_program == key:
                    affiliations.append(graduate_program)

        return affiliations
