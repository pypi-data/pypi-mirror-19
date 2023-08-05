"""
LUE Python package

The LUE Python package allows you to perform I/O to the LUE Scientific
Database, which is an HDF5 binary data format.

LUE information is stored in a dataset (see lue.Dataset). Each dataset
contains a collection of universes (lue.Universes, lue.Universe)
and a collection of phenomena (lue.Phenomena, lue.Phenomenon). Each
universe contains a collection of phenomena (lue.Phenomenon). Each
phenomenon contains a collection of property sets (lue.PropertySets,
lue.PropertySet). Each property set is connected to a single domain
(lue.Domain) and contains a collection of properties (lue.Properties,
lue.Property).

For more information about the API, see the help pages of the imported
modules and the various classes, e.g.: help(lue._lue), help(lue.Dataset).
Note that, although the documentation mentions the subpackage name
`lue._lue` in various places, the `lue._lue` module should not be used
directly in code. All high-level symbols are imported in the main `lue`
module.  So, use `lue.Dataset` instead of `lue._lue.Dataset`, for example.

For more information about LUE, see the LUE project page:
https://github.com/pcraster/lue
"""
from ._lue import *
from .describe import describe_dataset


__version__ = "0.0.0.dev3"


### # # [space.type][space.item_type]
### # _omnipresent_space_domain_api_dict = {
### #     space_domain.omnipresent: {
### #         space_domain_item.none: int
### #     },
### #     space_domain.located: {
### #         space_domain_item.box: O_SpaceBox
### #     }
### # }
### 
### 
### _property_set_api_dict = {
###     time_domain.omnipresent: O_PropertySet
### }
### 
### 
### # def _space_domain_api(
### #         space_domain):
### # 
### #     # Give a regular space domain, wrap it by a type that is smarter, given
### #     # the actual space domain configuration.
### #     return _space_domain_api[space_domain.configuration.type]
### #         [space_domain.configuration.item_type](space_domain)
### # 
### # 
### # def _decorated_space_domain(
### #         function):
### #     def space_domain(*args, **kwargs):
### #         return _space_domain_api(function(*args, **kwargs))
### # 
### #     return space_domain
### # 
### # property_set.add_property_set = _decorated_add_property_set(
### #     Phenomenon.add_property_set)
### 
### 
### def _property_set_api(
###         property_set):
### 
###     # Give a regular property set, wrap it by a type that is smarter, given
###     # the actual time domain configuration.
###     return _property_set_api_dict[property_set.domain.configuration.time.type](
###         property_set)
### 
### 
### def _decorated_add_property_set(
###         function):
###     def add_property_set(*args, **kwargs):
###         return _property_set_api(function(*args, **kwargs))
### 
###     return add_property_set
### 
### Phenomenon.add_property_set = _decorated_add_property_set(
###     Phenomenon.add_property_set)
### 
### 
### def _decorated_property_sets__get_item__(
###         function):
###     def __getitem__(*args, **kwargs):
###         return _property_set_api(function(*args, **kwargs))
### 
###     return __getitem__
### 
### 
### # When a property set is requested, it is wrapped in a type that
### # provides an API that is suitable given the time domain properties
### # of the property set's domain.
### PropertySets.__getitem__ = _decorated_property_sets__get_item__(
###     PropertySets.__getitem__)
### 
### 
### 
### # # When a space domain is requested, it is wrapped in a type that provides
### # # an API that is suitable given the time and space domain properties.
### # 
### # def _decorated_space_domain(
### #         function):
### #     def space_domain(*args, **kwargs):
### #         return _space_domain_api(function(*args, **kwargs))
### # 
### #     return add_property_set
### # 
### # Phenomenon.add_property_set = _decorated_add_property_set(
### #     Phenomenon.add_property_set)



Chunks = Shape


# Make the types more convenient by wrapping dumb types by smart API types,
# given domain properties.

_api = {
    time_domain.omnipresent: {
        # Information that is omnipresent in time.

        "property_set": O_PropertySet,
        "domain": O_Domain,

        time_domain_item.none: {
            space_domain.omnipresent: {

                # Information that is omnipresent in space.

                # TODO
                space_domain_item.none: None
            },
            space_domain.located: {

                # Information that is located in space.

                # Box
                space_domain_item.box: O_SpaceBoxDomain,

                # TODO more options
            },
        },
    },

    time_domain.shared: {
        "property_set": None,
        "domain": None,
    },

    # time_domain.located: {
    #     # Information that is located in time.

    #     # TODO

    # },
}


# TODO How about replacing all this by classes that use decorators to wrap
#      some of the methods?
def _install_api():

    def property_set_api(
            property_set):

        time_domain_type = property_set.domain.configuration.time.type

        # Give a regular property set, wrap it by a type that is smarter,
        # given the actual time domain configuration.
        return _api[time_domain_type]["property_set"](property_set)


    def decorated_add_property_set(
            function):

        def add_property_set(
                *args,
                **kwargs):
            return property_set_api(function(*args, **kwargs))

        return add_property_set


    # Wrap method by one that returns a specialized property instance.
    Phenomenon.add_property_set = decorated_add_property_set(
        Phenomenon.add_property_set)


    def decorated_property_sets__get_item__(
            function):

        def __getitem__(
                *args,
                **kwargs):
            return property_set_api(function(*args, **kwargs))

        return __getitem__


    # When a property set is requested, it is wrapped in a type that
    # provides an API that is suitable given the time domain properties
    # of the property set's domain.
    PropertySets.__getitem__ = decorated_property_sets__get_item__(
        PropertySets.__getitem__)


    def domain_api(
            domain):

        time_domain_type = domain.time_domain.configuration.type

        # Given a regular domain, wrap it by a type that is smarter,
        # given the actual time domain configuration.
        return _api[time_domain_type]["domain"](domain)


    def decorated_domain_get(
            property_):

        def domain_get(
                *args,
                **kwargs):
            return domain_api(property_.fget(*args, **kwargs))

        return domain_get


    O_PropertySet.domain = property(decorated_domain_get(
        O_PropertySet.domain))


    def o_space_domain_api(
            space_domain):

        type = space_domain.configuration.type
        item_type = space_domain.configuration.item_type

        # Given a regular space domain, wrap it by a type that is smarter,
        # given the actual space domain configuration.
        return _api[time_domain.omnipresent][time_domain_item.none] \
            [type][item_type](space_domain)


    def decorated_o_space_domain_get(
            property_):

        def o_space_domain_get(
                *args,
                **kwargs):
            return o_space_domain_api(property_.fget(*args, **kwargs))

        return o_space_domain_get


    # Wrap property getter by one that returns a specialized space
    # domain instance.
    O_Domain.space_domain = property(decorated_o_space_domain_get(
        O_Domain.space_domain))


_install_api()
