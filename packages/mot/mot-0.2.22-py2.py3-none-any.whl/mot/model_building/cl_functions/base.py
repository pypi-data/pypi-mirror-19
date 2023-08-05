import os
from .parameters import FreeParameter

__author__ = 'Robbert Harms'
__date__ = "2016-10-03"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class CLFunction(object):

    def __init__(self, return_type, function_name, parameter_list):
        """The header to one of the CL library functions.

        Ideally the functions map bijective to the CL function files.

        Args:
            return_type (str): Return type of the CL function.
            function_name (string): The name of the CL function
            parameter_list (list of mot.model_building.cl_functions.parameters.CLFunctionParameter): The list of parameters required for this function
        """
        super(CLFunction, self).__init__()
        self._return_type = return_type
        self._function_name = function_name
        self._parameter_list = parameter_list

    @property
    def return_type(self):
        """Get the type (in CL naming) of the returned value from this function.

        Returns:
            str: The return type of this CL function. (Examples: double, int, double4, ...)
        """
        return self._return_type

    @property
    def cl_function_name(self):
        """Return the name of the implemented CL function

        Returns:
            str: The name of this CL function
        """
        return self._function_name

    @property
    def parameter_list(self):
        """Return the list of parameters from this CL function.

        Returns:
            A list containing instances of CLFunctionParameter."""
        return self._parameter_list

    def get_cl_header(self):
        """Get the CL header for this function and all its dependencies

        Returns:
            str: The CL header code for inclusion in CL source code.
        """
        return ''

    def get_cl_code(self):
        """Get the function code for this function and all its dependencies.

        Returns:
            str: The CL header code for inclusion in CL source code.
        """
        return ''

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return type(self) == type(other)

    def __ne__(self, other):
        return type(self) != type(other)


class DependentCLFunction(CLFunction):

    def __init__(self, return_type, function_name, parameter_list, dependency_list):
        """A CL function with dependencies on multiple other CLFunctions.

        Args:
            return_type (str): Return type of the CL function.
            function_name (string): The name of the CL function
            parameter_list (list of mot.model_building.cl_functions.parameters.CLFunctionParameter): The list of parameters required for this function
            dependency_list (list of CLFunction): The list of CLFunctions this function is dependent on
        """
        super(DependentCLFunction, self).__init__(return_type, function_name, parameter_list)
        self._dependency_list = dependency_list

    def _get_cl_dependency_headers(self):
        """Get the CL code for all the headers for all the dependencies.

        Returns:
            str: The CL code with the headers.
        """
        header = ''
        for d in self._dependency_list:
            header += d.get_cl_header() + "\n"
        return header

    def _get_cl_dependency_code(self):
        """Get the CL code for all the CL code for all the dependencies.

        Returns:
            str: The CL code with the actual code.
        """
        code = ''
        for d in self._dependency_list:
            code += d.get_cl_code() + "\n"
        return code


class ModelFunction(DependentCLFunction):

    def __init__(self, name, cl_function_name, parameter_list, dependency_list=()):
        """This CL function is for all estimable models

        Args:
            name (str): The name of the model
            cl_function_name (string): The name of the CL function
            parameter_list (list or tuple of CLFunctionParameter): The list of parameters required for this function
            dependency_list (list or tuple of CLFunction): The list of CLFunctions this function is dependent on
        """
        super(ModelFunction, self).__init__('mot_float_type', cl_function_name, parameter_list, dependency_list)
        self._name = name

    @property
    def name(self):
        """Get the name of this model function.

        Returns:
            str: The name of this model function.
        """
        return self._name

    def get_free_parameters(self):
        """Get all the free parameters in this model

        Returns:
            list: the list of free parameters in this model
        """
        return self.get_parameters_of_type(FreeParameter)

    def get_parameters_of_type(self, instance_types):
        """Get all parameters whose state instance is one of the given types.

        Args:
            instance_types (list of DataType class names, or single DataType classname);
                The instance type we want to get all the parameters of.

        Returns:
            A list of parameters whose type matches one or more of the given types.
        """
        return list([p for p in self.parameter_list if isinstance(p, instance_types)])

    def get_parameter_by_name(self, param_name):
        """Get a parameter by name.

        Args:
            param_name (str): The name of the parameter to return

        Returns:
            ClFunctionParameter: the parameter of the given name

        Raises:
            KeyError: if the parameter could not be found.
        """
        for e in self.parameter_list:
            if e.name == param_name:
                return e
        raise KeyError('The parameter with the name "{}" could not be found.'.format(param_name))

    def get_extra_results_maps(self, results_dict):
        """Get extra results maps with extra output from this model function.

        This is used by the function finalize_optimization_results() from the ModelBuilder to add extra maps
        to the resulting dictionary.

        Suppose a model has a parameter that can be viewed in multiple ways. It would be nice to be able
        to output maps for that parameter in multiple ways such that the amount of post-processing is as least as
        possible.

        For example, suppose a model calculates an angle (theta) and a radius (r). Perhaps we would like to return
        the cartesian coordinate of that point alongside the polar coordinates. This function allows you (indirectly)
        to add the additional maps.

        Do not modify the dictionary in place.

        Args:
            results_dict (dict): The result dictionary with all the maps you need and perhaps other maps from other
                models as well. The maps are 1 dimensional, a long list of values for all the voxels in the ROI.

        Returns:
            dict: A new dictionary with the additional maps to add.
        """
        return {}

    def get_cl_dependency_headers(self):
        """Get the CL code for all the headers for all the dependencies.

        Returns:
            str: The CL code with the headers.
        """
        return self._get_cl_dependency_headers()

    def get_cl_dependency_code(self):
        """Get the CL code for all the CL code for all the dependencies.

        Returns:
            str: The CL code with the actual code.
        """
        return self._get_cl_dependency_code()


class LibraryFunction(DependentCLFunction):

    def __init__(self, return_type, function_name, parameter_list, cl_header_file,
                 cl_code_file, var_replace_dict, dependency_list):
        """Create a CL function for a library function.

        These functions are not meant to be optimized, but can be used a helper functions for the models.

        Args:
            return_type (str): Return type of the CL function.
            function_name (str): The name of the CL function
            cl_header_file (str): The location of the header file .h or .ph
            cl_code_file (str): The location of the code file .c or .pcl
            var_replace_dict (dict): In the cl_header and cl_code file these replacements will be made
                (using the % format function of Python)
            parameter_list (list or tuple of mot.model_building.cl_functions.parameters.CLFunctionParameter): The list of parameters required for this function
            dependency_list (list or tuple of mot.model_building.cl_functions.base.CLFunction): The list of CLFunctions this function is dependent on
        """
        super(LibraryFunction, self).__init__(return_type, function_name, parameter_list, dependency_list)
        self._cl_header_file = cl_header_file
        self._cl_code_file = cl_code_file
        self._var_replace_dict = var_replace_dict

    def get_cl_header(self):
        """Get the CL header for this function and all its dependencies.

        Returns:
            str: The CL code for the header
        """
        header = self._get_cl_dependency_headers()
        header += "\n"
        body = open(os.path.abspath(self._cl_header_file), 'r').read()
        if self._var_replace_dict:
            body = body % self._var_replace_dict
        return header + "\n" + body

    def get_cl_code(self):
        """Get the CL code for this function and all its dependencies.

        Returns:
            str: The CL code for the body of the function
        """
        code = self._get_cl_dependency_code()
        code += "\n"
        body = open(os.path.abspath(self._cl_code_file), 'r').read()
        if self._var_replace_dict:
            body = body % self._var_replace_dict
        return code + "\n" + body
