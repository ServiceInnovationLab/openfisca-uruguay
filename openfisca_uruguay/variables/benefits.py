# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
from openfisca_uruguay.entities import *


class eligible_for_pension(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Eligiblity for pension"
    reference = "https://www.bps.gub.uy/3498/jubilaciones.html"

    def formula(person, period, parameters):
        return person('number_of_years_worked', period) >= 15


class edad_de_jubilacion(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Edad de jubilacion"
    reference = "https://www.bps.gub.uy/3498/jubilaciones.html"

    """
    work for 30 years then age is 60
    work for 15 years, then age is 70
    One less year required for women, per child
    """
    def formula(person, period, parameters):

        worked_for_required_years = person(
            'jubilacion__worked_for_required_years', period)
        worked_for_advanced_age_required_years = person(
            'edad_avanazada__worked_required_years', period)

        edad_de_jubilacion = parameters(period).general.edad_de_jubilacion
        edad_avanazada = parameters(period).general.edad_avanazada

        # either worked for the longer required years therefore age is 60
        # OR they worked for only 15 therefore age is 70
        retirement_ages = (worked_for_required_years * edad_de_jubilacion) + \
            (worked_for_advanced_age_required_years * not_(worked_for_required_years)
                * edad_avanazada)

        return retirement_ages


class jubilacion__worked_for_required_years(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Person has worked for requried years to receive jubilacion"
    reference = "https://www.bps.gub.uy/3498/jubilaciones.html"

    def formula(person, period, parameters):
        required_years = person('jubilacion__required_work_years', period)
        return person('number_of_years_worked', period) >= required_years


class jubilacion__required_work_years(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Number of years this person must work to be eligible for jubilacion"
    reference = "https://www.bps.gub.uy/3498/jubilaciones.html"

    def formula(person, period, parameters):
        # if a woman, subtract one year for each child
        women = (person('gender', period) == 1)
        child_offset = (women * person('number_of_children', period))

        return (30 - child_offset)


class edad_avanazada__worked_required_years(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Person has worked for 15 years or more"
    reference = "https://www.bps.gub.uy/3498/jubilaciones.html"

    def formula(person, period, parameters):
        return person('number_of_years_worked', period) >= 15
