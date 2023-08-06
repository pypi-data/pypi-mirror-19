# -*- coding: utf-8 -*-

from __future__ import division

import humanize
import logging
import numpy as np
import pandas


from openfisca_core import formulas, periods, simulations
try:
    from openfisca_core.tools.memory import get_memory_usage, print_memory_usage
except ImportError:
    get_memory_usage = None
    print_memory_usage = None
from openfisca_survey_manager.calibration import Calibration

from .survey_collections import SurveyCollection
from .surveys import Survey

log = logging.getLogger(__name__)


class AbstractSurveyScenario(object):
    filtering_variable_by_entity = None
    id_variable_by_entity_key = None
    inflator_by_variable = None  # factor used to inflate variable total
    input_data_frame = None
    input_data_table_by_period = None
    legislation_json = None
    non_neutralizable_variables = None
    cache_blacklist = None
    reference_simulation = None
    reference_tax_benefit_system = None
    role_variable_by_entity_key = None
    simulation = None
    target_by_variable = None  # variable total target to inflate to
    tax_benefit_system = None
    used_as_input_variables = None
    weight_column_name_by_entity = None
    year = None

    def calibrate(self, target_margins_by_variable = None, parameters = None, total_population = None):
        survey_scenario = self
        survey_scenario.initialize_weights()
        calibration = Calibration(survey_scenario)

        if parameters is not None:
            assert parameters['method'] in ['linear', 'raking ratio', 'logit'], \
                "Incorect parameter value: method should be 'linear', 'raking ratio' or 'logit'"
            if parameters['method'] == 'logit':
                assert parameters['invlo'] is not None
                assert parameters['up'] is not None
        else:
            parameters = dict(method = 'logit', up = 3, invlo = 3)

        calibration.parameters.update(parameters)

        if total_population:
            calibration.total_population = total_population

        if target_margins_by_variable is not None:
            calibration.set_target_margins(target_margins_by_variable)

        calibration.calibrate()
        calibration.set_calibrated_weights()
        self.calibration = calibration

    def compute_aggregate(self, variable = None, aggfunc = 'sum', filter_by = None, period = None, reference = False,
                          missing_variable_default_value = np.nan):
        # TODO deal here with filter_by instead of openfisca_france_data ?
        assert aggfunc in ['count', 'mean', 'sum']
        tax_benefit_system = self.tax_benefit_system
        if filter_by is None and self.filtering_variable_by_entity is not None:
            entity_key = tax_benefit_system.column_by_name[variable].entity.key
            filter_by = self.filtering_variable_by_entity.get(entity_key)

        assert variable is not None
        if reference:
            simulation = self.reference_simulation
        else:
            simulation = self.simulation

        assert simulation is not None

        if filter_by:
            assert filter_by in self.tax_benefit_system.column_by_name, \
                "{} is not a variables of the tax benefit system".format(filter_by)

        if self.weight_column_name_by_entity:
            weight_column_name_by_entity = self.weight_column_name_by_entity
            entity_key = tax_benefit_system.column_by_name[variable].entity.key
            entity_weight = weight_column_name_by_entity[entity_key]
        else:
            entity_weight = None

        if variable in simulation.tax_benefit_system.column_by_name:
            value = simulation.calculate_add(variable, period = period)
        else:
            log.info("Variable {} not found. Assiging {}".format(variable, missing_variable_default_value))
            return missing_variable_default_value

        weight = (
            simulation.calculate_add(entity_weight, period = period).astype(float)
            if entity_weight else 1.0
            )
        filter_dummy = simulation.calculate_add(filter_by, period = period) if filter_by else 1.0

        if aggfunc == 'sum':
            return (value * weight * filter_dummy).sum()
        elif aggfunc == 'mean':
            return (value * weight * filter_dummy).sum() / (weight * filter_dummy).sum()
        elif aggfunc == 'count':
            return (weight * filter_dummy).sum()

    def compute_pivot_table(
            self, aggfunc = 'mean', columns = None, difference = None, filter_by = None, index = None,
            period = None, reference = False, values = None, missing_variable_default_value = np.nan):
        assert aggfunc in ['count', 'mean', 'sum']

        tax_benefit_system = self.tax_benefit_system
        if filter_by is None and self.filtering_variable_by_entity is not None:
            entity_key = tax_benefit_system.column_by_name[values[0]].entity.key
            filter_by = self.filtering_variable_by_entity.get(entity_key)

        assert isinstance(values, (str, list))
        if isinstance(values, str):
            values = ['values']

        # assert len(values) == 1

        if difference:
            return (
                self.compute_pivot_table(
                    aggfunc = aggfunc, columns = columns, filter_by = filter_by, index = index,
                    period = period, reference = False, values = values,
                    missing_variable_default_value = missing_variable_default_value
                    ) -
                self.compute_pivot_table(
                    aggfunc = aggfunc, columns = columns, filter_by = filter_by, index = index,
                    period = period, reference = True, values = values,
                    missing_variable_default_value = missing_variable_default_value)
                )

        if reference:
            simulation = self.reference_simulation
        else:
            simulation = self.simulation

        assert simulation is not None

        index_list = index if index is not None else []
        columns_list = columns if columns is not None else []
        variables = set(index_list + values + columns_list)
        entity_key = tax_benefit_system.column_by_name[values[0]].entity.key

        # Select the entity weight corresponding to the variables that will provide values
        if self.weight_column_name_by_entity is not None:
            weight = self.weight_column_name_by_entity[entity_key]
            variables.add(weight)
        else:
            weight = None

        if filter_by is not None:
            variables.add(filter_by)
        else:
            filter_dummy = 1.0

        for variable in variables:
            assert tax_benefit_system.column_by_name[variable].entity.key == entity_key, \
                'The variable {} is not present or does not belong to entity {}'.format(
                    variable,
                    entity_key,
                    )

        def calculate_variable(var):
            if var in simulation.tax_benefit_system.column_by_name:
                return simulation.calculate_add(var, period = period)
            else:
                log.info("Variable {} not found. Assiging {}".format(variable, missing_variable_default_value))
                return missing_variable_default_value

        data_frame = pandas.DataFrame(dict(
            (variable, calculate_variable(variable)) for variable in variables
            ))
        if filter_by in data_frame:
            filter_dummy = data_frame.get(filter_by)
        if weight is None:
            weight = 'weight'
            data_frame[weight] = 1.0

        data_frame[values[0]] = data_frame[values[0]] * data_frame[weight] * filter_dummy
        pivot_sum = data_frame.pivot_table(index = index, columns = columns, values = values, aggfunc = 'sum')
        pivot_mass = data_frame.pivot_table(index = index, columns = columns, values = weight, aggfunc = 'sum')
        if aggfunc == 'mean':
            return (pivot_sum / pivot_mass)
        elif aggfunc == 'sum':
            return pivot_sum
        elif aggfunc == 'count':
            return pivot_mass

    def create_data_frame_by_entity(self, variables = None, indices = False, period = None, reference = False,
            roles = False):
        assert variables is not None or indices or roles
        tax_benefit_system = self.tax_benefit_system

        if reference:
            simulation = self.reference_simulation
        else:
            simulation = self.simulation

        assert simulation is not None

        missing_variables = set(variables).difference(set(self.tax_benefit_system.column_by_name.keys()))
        if missing_variables:
            log.info("These variables aren't par of the tax-benefit system: {}".format(missing_variables))
        columns_to_fetch = [
            self.tax_benefit_system.column_by_name.get(variable_name) for variable_name in variables
            if self.tax_benefit_system.column_by_name.get(variable_name) is not None
            ]
        openfisca_data_frame_by_entity_key = dict()
        for entity in tax_benefit_system.entities:
            entity_key = entity.key
            column_names = [
                column.name for column in columns_to_fetch
                if column.entity == entity
                ]
            openfisca_data_frame_by_entity_key[entity_key] = pandas.DataFrame(
                dict(
                    (column_name, simulation.calculate_add(column_name, period = period))
                    for column_name in column_names
                    )
                )
        # TODO add roles
        return openfisca_data_frame_by_entity_key

    def custom_input_data_frame(self, input_data_frame, **kwargs):
        pass

    def dump_data_frame_by_entity(self, variables = None, survey_collection = None, survey_name = None):
        assert survey_collection is not None
        assert survey_name is not None
        assert variables is not None
        openfisca_data_frame_by_entity = self.create_data_frame_by_entity(variables = variables)
        for entity_key, data_frame in openfisca_data_frame_by_entity.iteritems():
            survey = Survey(name = survey_name)
            survey.insert_table(name = entity_key, data_frame = data_frame)
            survey_collection.surveys.append(survey)
            survey_collection.dump(collection = "openfisca")

    def fill(self, input_data_frame, simulation, period):
        assert period is not None
        log.info('Initialasing simulation using data_frame for period {}'.format(period))

        log.info("Initialasing {}".format(period))
        if period.unit == 'year':  # 1. year
            self.init_simulation_with_data_frame(
                input_data_frame = input_data_frame,
                period = period,
                simulation = simulation,
                )
        elif period.unit == 'month' and period.size == 3:  # 2. quarter
            for offset in range(period.size):
                period_item = periods.period('month', period.start.offset(offset, 'month'))
                self.init_simulation_with_data_frame(
                    input_data_frame = input_data_frame,
                    period = period_item,
                    simulation = simulation,
                    )
        elif period.unit == 'month' and period.size == 1:  # 3. months
            self.init_simulation_with_data_frame(
                input_data_frame = input_data_frame,
                period = period,
                simulation = simulation,
                )
        else:
            log.info("Unvalid period {}".format(period))
            raise

    def filter_input_variables(self, input_data_frame = None, simulation = None):
        """
        Clean the data_frame
        """
        assert input_data_frame is not None
        assert simulation is not None
        id_variable_by_entity_key = self.id_variable_by_entity_key
        role_variable_by_entity_key = self.role_variable_by_entity_key
        used_as_input_variables = self.used_as_input_variables

        tax_benefit_system = simulation.tax_benefit_system
        column_by_name = tax_benefit_system.column_by_name

        id_variables = [
            id_variable_by_entity_key[entity.key] for entity in simulation.entities.values()
            if not entity.is_person]
        role_variables = [
            role_variable_by_entity_key[entity.key] for entity in simulation.entities.values()
            if not entity.is_person]

        log.info('Variable used_as_input_variables in filter: \n {}'.format(used_as_input_variables))
        for column_name in input_data_frame:
            if column_name in id_variables + role_variables:
                continue
            if column_name not in column_by_name:
                log.info('Unknown column "{}" in survey, dropped from input table'.format(column_name))
                input_data_frame.drop(column_name, axis = 1, inplace = True)

        for column_name in input_data_frame:
            if column_name in id_variables + role_variables:
                continue
            column = column_by_name[column_name]
            formula_class = column.formula_class
            if not issubclass(formula_class, formulas.SimpleFormula):
                continue
            function = formula_class.function
            # Keeping the calculated variables that are initialized by the input data
            if function is not None:
                if column_name in used_as_input_variables:
                    log.info(
                        'Column "{}" not dropped because present in used_as_input_variables'.format(column_name))
                    continue

                log.info('Column "{}" in survey set to be calculated, dropped from input table'.format(column_name))
                input_data_frame.drop(column_name, axis = 1, inplace = True)
                #
            #
        #
        log.info('Keeping the following variables in the input_data_frame: \n {}'.format(input_data_frame.columns))
        return input_data_frame

    def inflate(self, inflator_by_variable = None, target_by_variable = None):
        assert inflator_by_variable or target_by_variable
        inflator_by_variable = dict() if inflator_by_variable is None else inflator_by_variable
        target_by_variable = dict() if target_by_variable is None else target_by_variable
        self.inflator_by_variable = inflator_by_variable
        self.target_by_variable = target_by_variable

        assert self.simulation is not None
        for reference in [False, True]:
            if reference is True:
                simulation = self.reference_simulation
            else:
                simulation = self.simulation
            if simulation is None:
                continue
            tax_benefit_system = self.tax_benefit_system
            for column_name in set(inflator_by_variable.keys()).union(set(target_by_variable.keys())):
                assert column_name in tax_benefit_system.column_by_name, \
                    "Variable {} is not a valid variable of the tax-benefit system".format(column_name)
                holder = simulation.get_or_new_holder(column_name)
                if column_name in target_by_variable:
                    inflator = inflator_by_variable[column_name] = \
                        target_by_variable[column_name] / self.compute_aggregate(
                            variable = column_name, reference = reference)
                    log.info('Using {} as inflator for {} to reach the target {} '.format(
                        inflator, column_name, target_by_variable[column_name]))
                else:
                    assert column_name in inflator_by_variable, 'column_name is not in inflator_by_variable'
                    log.info('Using inflator {} for {}.  The target is thus {}'.format(
                        inflator_by_variable[column_name],
                        column_name, inflator_by_variable[column_name] * self.compute_aggregate(variable = column_name))
                        )
                    inflator = inflator_by_variable[column_name]

                holder.array = inflator * holder.array

    def init_from_data_frame(self, input_data_frame = None, input_data_table_by_period = None):

        if input_data_frame is not None:
            self.set_input_data_frame(input_data_frame)

        self.input_data_table_by_period = self.input_data_table_by_period or input_data_table_by_period

        assert (
            self.input_data_frame is not None or
            self.input_data_table_by_period is not None
            )

        if self.used_as_input_variables is None:
            self.used_as_input_variables = []
        else:
            assert isinstance(self.used_as_input_variables, list)

        if 'initialize_weights' in dir(self):
            self.initialize_weights()
        #
        return self

    def init_simulation_with_data_frame(self, input_data_frame = None, period = None, simulation = None,
            verbose = False):
        """
        Initialize the simulation period with current input_data_frame
        """
        assert input_data_frame is not None
        assert period is not None
        assert simulation is not None
        used_as_input_variables = self.used_as_input_variables
        id_variable_by_entity_key = self.id_variable_by_entity_key
        role_variable_by_entity_key = self.role_variable_by_entity_key

        variables_mismatch = set(used_as_input_variables).difference(set(input_data_frame.columns))
        if variables_mismatch:
            log.info(
                'The following variables used as input variables are not present in the input data frame: \n {}'.format(
                    variables_mismatch))
            log.info('The following variables are used as input variables: \n {}'.format(used_as_input_variables))
            log.info('The input_data_frame contains the following variables: \n {}'.format(input_data_frame.columns))

        id_variables = [
            id_variable_by_entity_key[entity.key] for entity in simulation.entities.values()
            if not entity.is_person]
        role_variables = [
            role_variable_by_entity_key[entity.key] for entity in simulation.entities.values()
            if not entity.is_person]

        for id_variable in id_variables + role_variables:
            assert id_variable in input_data_frame.columns, \
                "Variable {} is not present in input dataframe".format(id_variable)

        input_data_frame = self.filter_input_variables(input_data_frame = input_data_frame, simulation = simulation)

        for key, entity in simulation.entities.iteritems():
            if entity.is_person:
                entity.count = entity.step_size = len(input_data_frame)
            else:
                entity.count = entity.step_size = \
                    (input_data_frame[role_variable_by_entity_key[key]] == 0).sum()
                entity.roles_count = int(input_data_frame[role_variable_by_entity_key[key]].max() + 1)
                assert isinstance(entity.roles_count, int), '{} is not a valid roles_count (int) for {}'.format(
                    entity.roles_count, entity.key)
                unique_ids_count = len(input_data_frame[id_variable_by_entity_key[key]].unique())
                assert entity.count == unique_ids_count, \
                    "There are {0} person of role 0 in {1} but {2} {1}".format(
                        entity.count, entity.key, unique_ids_count)

                entity.members_entity_id = input_data_frame[id_variable_by_entity_key[key]].astype('int').values
                entity.members_legacy_role = input_data_frame[role_variable_by_entity_key[key]].astype('int').values

        for column_name, column_serie in input_data_frame.iteritems():
            if column_name in role_variable_by_entity_key.values() + id_variable_by_entity_key.values():
                continue
            holder = simulation.get_or_new_holder(column_name)
            entity = holder.entity
            if verbose and (column_serie.values.dtype != holder.column.dtype):
                log.info(
                    'Converting {} from dtype {} to {}'.format(
                        column_name, column_serie.values.dtype, holder.column.dtype)
                    )
            if np.issubdtype(column_serie.values.dtype, np.float):
                if column_serie.isnull().any():
                    if verbose:
                        log.info('There are {} NaN values for {} non NaN values in variable {}'.format(
                            column_serie.isnull().sum(), column_serie.notnull().sum(), column_name))
                        log.info('We convert these NaN values of variable {} to {} its default value'.format(
                            column_name, holder.column.default))
                    input_data_frame.loc[column_serie.isnull(), column_name] = holder.column.default
                assert input_data_frame[column_name].notnull().all(), \
                    'There are {} NaN values for {} non NaN values in variable {}'.format(
                        column_serie.isnull().sum(), column_serie.notnull().sum(), column_name)

            if entity.is_person:
                array = column_serie.values.astype(holder.column.dtype)
            else:
                array = column_serie.values[
                    input_data_frame[role_variable_by_entity_key[entity.key]].values == 0
                    ].astype(holder.column.dtype)
            assert array.size == entity.count, 'Bad size for {}: {} instead of {}'.format(
                column_name, array.size, entity.count)

            holder.set_input(period, np.array(array, dtype = holder.column.dtype))

    # @property
    # def input_data_frame(self):
    #     return self.input_data_frame_by_entity.get(period = periods.period(self.year))

    def new_simulation(self, debug = False, debug_all = False, reference = False, trace = False):
        assert self.tax_benefit_system is not None
        tax_benefit_system = self.tax_benefit_system
        if self.reference_tax_benefit_system is not None and reference:
            tax_benefit_system = self.reference_tax_benefit_system
        elif reference:
            while True:
                reference_tax_benefit_system = tax_benefit_system.reference
                if isinstance(reference, bool) and reference_tax_benefit_system is None \
                        or reference_tax_benefit_system == reference:
                    break
                tax_benefit_system = reference_tax_benefit_system

        period = periods.period(self.year)
        self.neutralize_variables(tax_benefit_system)

        simulation = simulations.Simulation(
            debug = debug,
            debug_all = debug_all,
            opt_out_cache = True if self.cache_blacklist is not None else False,
            period = period,
            tax_benefit_system = tax_benefit_system,
            trace = trace,
            )
        # Case 1: fill simulation with a unique input_data_frame given by the attribute
        if self.input_data_frame is not None:
            input_data_frame = self.input_data_frame.copy()
            self.custom_input_data_frame(input_data_frame, period = period)
            self.fill(input_data_frame, simulation, period)
        # Case 2: fill simulation with a unique input_data_frame containing all entity variables
        elif self.input_data_table_by_period is not None:
            for period, table in self.input_data_table_by_period.iteritems():
                period = periods.period(period)
                input_data_frame = self.load_table(table = table)
                self.custom_input_data_frame(input_data_frame, period = period)
                self.fill(input_data_frame, simulation, period)
        #
        if not reference:
            self.simulation = simulation
        else:
            self.reference_simulation = simulation
        #
        if 'custom_initialize' in dir(self):
            self.custom_initialize(simulation)
        #
        return simulation

    def load_table(self, variables = None, collection = None, survey = None,
            table = None):
        collection = collection or self.collection
        survey_collection = SurveyCollection.load(collection = self.collection)
        survey = survey or "{}_{}".format(self.input_data_survey_prefix, self.year)
        survey_ = survey_collection.get_survey(survey)
        return survey_.get_values(table = table, variables = variables)  # .reset_index(drop = True)

    def memory_usage(self, reference = False):
        if reference:
            simulation = self.reference_simulation
        else:
            simulation = self.simulation
        print_memory_usage(simulation)

    def neutralize_variables(self, tax_benefit_system):
        """
        Neutralizing input variables not present in the input_data_frame and keep some crucial variables
        """
        for column_name, column in tax_benefit_system.column_by_name.items():
            formula_class = column.formula_class
            if not issubclass(formula_class, formulas.SimpleFormula):
                continue
            function = formula_class.function
            if function is not None:
                continue
            if column_name in self.used_as_input_variables:
                continue
            if self.non_neutralizable_variables and (column_name in self.non_neutralizable_variables):
                continue
            if self.weight_column_name_by_entity and column_name in self.weight_column_name_by_entity.values():
                continue

            tax_benefit_system.neutralize_column(column_name)

    def set_input_data_frame(self, input_data_frame):
        self.input_data_frame = input_data_frame

    def set_tax_benefit_systems(self, tax_benefit_system = None, reference_tax_benefit_system = None):
        """
        Set the tax and benefit system and eventually the reference atx and benefit system
        """
        assert tax_benefit_system is not None
        self.tax_benefit_system = tax_benefit_system
        if self.cache_blacklist is not None:
            self.tax_benefit_system.cache_blacklist = self.cache_blacklist
        if reference_tax_benefit_system is not None:
            self.reference_tax_benefit_system = reference_tax_benefit_system
            if self.cache_blacklist is not None:
                self.reference_tax_benefit_system.cache_blacklist = self.cache_blacklist

    def summarize_variable(self, variable = None, reference = False, weighted = False, force_compute = False):
        if reference:
            simulation = self.reference_simulation
        else:
            simulation = self.simulation

        tax_benefit_system = simulation.tax_benefit_system
        assert variable in tax_benefit_system.column_by_name.keys()
        column = tax_benefit_system.column_by_name[variable]

        if weighted:
            weight_variable = self.weight_column_name_by_entity[column.entity.key]
            weights = simulation.calculate(weight_variable)

        default_value = column.default
        infos_by_variable = get_memory_usage(simulation, variables = [variable])

        if not infos_by_variable:
            if force_compute:
                simulation.calculate_add(variable)
                self.summarize_variable(variable = variable, reference = reference, weighted = weighted)
                return
            else:
                print("{} is not computed yet. Use keyword argument force_compute = True".format(variable))
                return
        infos = infos_by_variable[variable]
        header_line = "{}: {} periods * {} cells * item size {} ({}, default = {}) = {}".format(
            variable,
            len(infos['periods']),
            infos['ncells'],
            infos['item_size'],
            infos['dtype'],
            default_value,
            humanize.naturalsize(infos['nbytes'], gnu = True),
            )
        print("")
        print(header_line)
        print("Details: ")
        holder = simulation.holder_by_name[variable]
        if holder is not None:
            if holder._array is not None:
                # Only used when column.is_permanent
                array = holder._array
                print("permanent: mean = {}, min = {}, max = {}, median = {}, default = {:.1%}".format(
                    array.mean() if not weighted else np.average(array, weights = weights),
                    array.min(),
                    array.max(),
                    np.median(array),
                    (
                        (array == default_value).sum() / len(array)
                        if not weighted
                        else ((array == default_value) * weights).sum() / weights.sum()
                        )
                    ))
            elif holder._array_by_period is not None:
                for period in sorted(holder._array_by_period.keys()):
                    array = holder._array_by_period[period]
                    print("{}: mean = {}, min = {}, max = {}, mass = {:.2e}, default = {:.1%}, median = {}".format(
                        period,
                        array.mean() if not weighted else np.average(array, weights = weights),
                        array.min(),
                        array.max(),
                        array.sum() if not weighted else np.sum(array * weights),
                        (
                            (array == default_value).sum() / len(array)
                            if not weighted
                            else ((array == default_value) * weights).sum() / weights.sum()
                            ),
                        np.median(array),
                        ))


# Helpers

# TODO NOT WORKING RIGH NOW
def init_simulation_with_data_frame_by_entity(input_data_frame_by_entity = None, simulation = None):
    assert input_data_frame_by_entity is not None
    assert simulation is not None
    for entity in simulation.entities.values():
        if entity.index_for_person_variable_name is not None:
            input_data_frame = input_data_frame_by_entity[entity.index_for_person_variable_name]
        else:
            input_data_frame = input_data_frame_by_entity['individus']
        input_data_frame = filter_input_variables(input_data_frame)

        if entity.is_persons_entity:
            entity.count = entity.step_size = len(input_data_frame)
        else:
            entity.count = entity.step_size = len(input_data_frame)
            entity.roles_count = input_data_frame_by_entity['individus'][
                entity.role_for_person_variable_name].max() + 1
            assert isinstance(entity.roles_count, int)

        # Convert columns from df to array:
        for column_name, column_serie in input_data_frame.iteritems():
            holder = simulation.get_or_new_holder(column_name)
            entity = holder.entity
            if column_serie.values.dtype != holder.column.dtype:
                log.info(
                    'Converting {} from dtype {} to {}'.format(
                        column_name, column_serie.values.dtype, holder.column.dtype)
                    )
            if np.issubdtype(column_serie.values.dtype, np.float):
                assert column_serie.notnull().all(), 'There are {} NaN values in variable {}'.format(
                    column_serie.isnull().sum(), column_name)

            array = column_serie.values.astype(holder.column.dtype)
            assert array.size == entity.count, 'Bad size for {}: {} instead of {}'.format(
                column_name,
                array.size,
                entity.count)
            holder.array = np.array(array, dtype = holder.column.dtype)
