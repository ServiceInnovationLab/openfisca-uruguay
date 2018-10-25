# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
from openfisca_uruguay.entities import *


class eligible_for_pension(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Eligiblity for pension"
    reference = "https://legislativo.parlamento.gub.uy/temporales/leytemp5815466.htm"

    def formula(person, period, parameters):
        return person('number_of_years_worked', period) >= 15


class edad_de_jubilacion(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Edad de jubilacion"
    reference = "https://www.bps.gub.uy/3498/jubilaciones.html"

    def formula(person, period, parameters):

        # work for 30 years then age is 60
        worked_for_30 = person('number_of_years_worked', period) >= 30

        # work for 15 years, then age is 70
        worked_for_15 = person('number_of_years_worked', period) >= 15

        retirement_ages = (worked_for_30 * 60) + \
            (worked_for_15 * not_(worked_for_30) * 70)

       
        # if a woman, subtract one year for each child
        women = (person('gender', period) == 1)

        child_offset = (women * person('number_of_children', period))

        return retirement_ages - child_offset
