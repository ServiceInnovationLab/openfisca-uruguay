# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
from openfisca_uruguay.entities import *


class number_of_children(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Number of years worked"
