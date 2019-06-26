import copy

from manuscript.tools.castings import as_is
import manuscript.tools.constants as mc
import manuscript.exceptions as mex


class Definition:
    """ The basis of all elements """

    PARAM_GROUP_DESC = ["Required parameters",
                        "Optional parameters",
                        "Dependent parameters"]

    params = [{"name": (as_is, None)},   # Required (e.g. cannot overridden)
              {mc.VALUES: (str, "")},    # Optional, default value given
              {}]                        # Optional, default value from other attribute or if not then from settings

    def __init__(self, work, *args, **kwargs):
        """ The final super().__init__()

        Connects the work,
        completes the elements parameters, and
        finally declares the element been defined

        Parameters
        ----------
        work :  the play where everything is connected to
        args :  other non-keyword parameters
        kwargs :    the keyword parameters

        Returns
        -------
        None
        """
        # print(f"Create element: {kwargs.get('name', None)}")
        self.work = work
        self.params = self.get_params()  # Complete params

        # Set required parameters
        for param, (func, default_value) in self.params[0].items():
            val = kwargs.get(param, None)
            if val is not None:
                setattr(self, param, func(val))
            else:
                raise mex.MMParameterError(f"*** Required parameter '{param}' missing")

        # Set optional parameters (default_value = name of the attribute)
        for param, (func, default_value) in self.params[1].items():
            val = kwargs.get(param, None)
            if val is None:
                val = default_value
            setattr(self, param, func(val))

        # set dependent parameters
        #
        # search value in this order:
        #   1. kwargs == parameter is given in init
        #   2. default value from self
        #   3. default value from settings
        #   4. otherwise --> error
        for param, (func, default_value) in self.params[2].items():
            val = kwargs.get(param, None)
            if val is None:
                val = kwargs.get(default_value, None)
            if val is None:
                val = self.work.settings.__dict__.get(default_value, None)
            if val is not None:
                setattr(self, param, func(val))
            else:
                raise mex.MMParameterError(f"*** The parameter that '{param}'' is dependent on is not set")

        self.work.define_action(self.name, self)

        # test if non-defined parameters
        for kwarg in kwargs:
            """
            if defining and audio is not defined ==> OK
            """
            if self.__dict__.get(kwarg, None) is None:
                raise mex.MMParameterError(f"*** Non-defined parameter '{kwarg} = {kwargs[kwarg]}' in {self.__dict__}")

    def __repr__(self):
        return "".join([self.__class__.__name__, "(", f"name='{self.name}'", ")"])

    def __str__(self):
        return  self.get_params_as_text()

    def get_params(self):
        """ Combine params of each parent class and itself """
        self_cls = self.__class__
        params = [{}, {}, {}]
        for cls in self_cls.mro():
            params = [{**pp, **cp}
                      for pp, cp in zip(params, cls.__dict__.get(
                          "params", [{}, {}, {}]))]
        return params

    def get_params_as_text(self):
        """ Combine to string the values of params of each parent class and itself """
        name = self.__dict__.get("name", "<NOT DEFINED>")
        result = f"\nPARAMETERS OF ELEMENT: {name} of class {self.__class__.__name__}"
        for param_group_index, param_group in enumerate(self.params):
            result += f"\n{self.PARAM_GROUP_DESC[param_group_index]}"
            length = max([15] + [len(key) for key in param_group])
            for key in param_group:
                value = self.__dict__.get(key, None)
                result += f"\n{' ':5}{key:{length}}: {value}"
        return result

    def copy(self, **kwargs):
        """ Copy object and set new values from kwargs """
        me = copy.copy(self)

        for key, value in kwargs.items():

            # Check reserved parameters
            if key in self.reserved_names:
                raise mex.MMParameterError(f"*** Illegal parameter: '{key}'.")
            if key not in vars(me):
                raise mex.MMParameterError(f"*** '{value}' tried to set non defined attribute '{key}'")

            # Required parameters == params[0] are not allowed to be overridden
            if key in self.params[0] and value is not None:
                raise mex.MMParameterError(f"*** '{key}' tried to override required attribute '{key}'")
            #
            # Find conversion function and set attribute
            # Order: try first required [0] then optional [1]
            # and finally dependent [2).
            # If not found use ("", (str, ""))
            #
            func = self.params[0].get(
                key, self.params[1].get(
                    key, self.params[2].get(
                        key, ("", (str, "")))))[0]

            setattr(me, key, func(value))
        return me
