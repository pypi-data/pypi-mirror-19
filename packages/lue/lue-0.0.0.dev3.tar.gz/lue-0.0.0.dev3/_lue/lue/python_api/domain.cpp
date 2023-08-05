#include "lue/cxx_api/domain.h"
#include "lue/cxx_api/constant_size/time/omnipresent/domain.h"
#include "lue/cxx_api/constant_size/time/omnipresent/space_box_domain.h"
#include <pybind11/pybind11.h>


namespace py = pybind11;
using namespace pybind11::literals;


namespace lue {
namespace python {

void init_domain(
        py::module& module)
{
    py::enum_<TimeDomainType>(module, "time_domain",
        "time_domain docstring...")
        .value("omnipresent", TimeDomainType::omnipresent)
        .value("shared", TimeDomainType::shared)
        // # .value("unique", TimeDomainType:unique)
    ;

    py::enum_<TimeDomainItemType>(module, "time_domain_item",
        "time_domain item docstring...")
        .value("none", TimeDomainItemType::none)
        // .value("point", TimeDomainItemType::point)
        .value("period", TimeDomainItemType::period)
        // .value("cell", TimeDomainItemType::cell)
    ;

    py::enum_<SpaceDomainType>(module, "space_domain",
        "space_domain docstring...")
        .value("omnipresent", SpaceDomainType::omnipresent)
        .value("located", SpaceDomainType::located)
    ;

    py::enum_<SpaceDomainItemType>(module, "space_domain_item",
        "space_domain item docstring...")
        .value("none", SpaceDomainItemType::none)
        .value("box", SpaceDomainItemType::box)
    ;

    py::class_<TimeDomainConfiguration>(module, "TimeDomainConfiguration",
        "TimeDomainConfiguration docstring...")
        .def(py::init<>(),
            "__init__ docstring...")
        .def(py::init<TimeDomainType const&, TimeDomainItemType const&>(),
            "__init__ docstring...",
            "type"_a,
            "item_type"_a)
        .def_property_readonly("type", &TimeDomainConfiguration::type,
            "type docstring...")
        .def_property_readonly("item_type",
            &TimeDomainConfiguration::item_type,
            "item type docstring...")
    ;

    py::class_<SpaceDomainConfiguration>(module, "SpaceDomainConfiguration",
        "SpaceDomainConfiguration docstring...")
        .def(py::init<>(),
            "__init__ docstring...")
        .def(py::init<SpaceDomainItemType const&>(),
            "__init__ docstring...",
            "item_type"_a)
        .def(py::init<SpaceDomainType const&, SpaceDomainItemType const&>(),
            "__init__ docstring...",
            "type"_a,
            "item_type"_a)
        .def_property_readonly("type", &SpaceDomainConfiguration::type,
            "type docstring...")
        .def_property_readonly("item_type",
            &SpaceDomainConfiguration::item_type,
            "item type docstring...")
    ;

    py::class_<DomainConfiguration>(module, "DomainConfiguration",
        "DomainConfiguration docstring...")
        .def(py::init<>(),
            "__init__ docstring...")
        .def(py::init<
                TimeDomainConfiguration const&>(),
            "__init__ docstring..."
            "time"_a)
        .def(py::init<
                SpaceDomainConfiguration const&>(),
            "__init__ docstring..."
            "space"_a)
        .def(py::init<
                TimeDomainConfiguration const&,
                SpaceDomainConfiguration const&>(),
            "__init__ docstring..."
            "time"_a, "space"_a)
        .def_property_readonly("time", &DomainConfiguration::time,
            "time docstring...",
            py::return_value_policy::reference_internal)
        .def_property_readonly("space", &DomainConfiguration::space,
            "space docstring...",
            py::return_value_policy::reference_internal)
    ;

    py::class_<TimeDomain>(module, "TimeDomain", py::base<hdf5::Group>(),
        "TimeDomain docstring...")
        .def_property_readonly("configuration", &TimeDomain::configuration,
            "configuration docstring...",
            py::return_value_policy::reference_internal)
    ;

    py::class_<SpaceDomain>(module, "SpaceDomain", py::base<hdf5::Group>(),
        "SpaceDomain docstring...")

        .def_property_readonly("configuration", &SpaceDomain::configuration,
            "configuration docstring...",
            py::return_value_policy::reference_internal)

    ;

    py::class_<Domain>(module, "Domain", py::base<hdf5::Group>(),
        "Domain docstring...")
        .def_property_readonly("configuration", &Domain::configuration,
            "configuration docstring...",
            py::return_value_policy::reference_internal)
        .def_property_readonly("time_domain", &Domain::time_domain,
            "time docstring...",
            py::return_value_policy::reference_internal)
        .def_property_readonly("space_domain", &Domain::space_domain,
            "space docstring...",
            py::return_value_policy::reference_internal)
    ;

    py::class_<constant_size::time::Domain>(module, "_Domain",
        "_Domain docstring...")

        .def_property_readonly("configuration",
                &constant_size::time::Domain::configuration,
            "configuration docstring...",
            py::return_value_policy::reference_internal)

        .def_property_readonly("time_domain",
                &constant_size::time::Domain::time_domain,
            "time docstring...",
            py::return_value_policy::reference_internal)

        .def_property_readonly("space_domain",
                &constant_size::time::Domain::space_domain,
            "space docstring...",
            py::return_value_policy::reference_internal)
    ;

    py::class_<constant_size::time::omnipresent::Domain>(module, "O_Domain",
        py::base<constant_size::time::Domain>(),
        "O_Domain docstring...")

        .def(py::init<Domain&>(),
            "__init__ docstring..."
            "group"_a,
            py::keep_alive<1, 2>())

        // .def_property_readonly("configuration",
        //         &time::omnipresent::Domain::configuration,
        //     "configuration docstring...",
        //     py::return_value_policy::reference_internal)

    ;

    py::class_<constant_size::time::SpaceDomain>(module, "_SpaceDomain",
        "_SpaceDomain docstring...")
    ;

    py::class_<constant_size::time::omnipresent::SpaceDomain>(module,
        "O_SpaceDomain",
        py::base<constant_size::time::SpaceDomain>(),
        "O_SpaceDomain docstring...")

        .def(py::init<SpaceDomain&>(),
            "__init__ docstring..."
            "group"_a,
            py::keep_alive<1, 2>())
    ;

    py::class_<constant_size::time::omnipresent::SpaceBox>(module,
        "O_SpaceBox",
        py::base<constant_size::time::omnipresent::same_shape::Item>(),
        "O_SpaceBox...")

        .def("reserve_items",
                &constant_size::time::omnipresent::SpaceBox::reserve_items,
            "reserve_items docstring...",
            py::return_value_policy::reference_internal)
    ;

    py::class_<constant_size::time::omnipresent::SpaceBoxDomain>(module,
        "O_SpaceBoxDomain",
        py::base<constant_size::time::omnipresent::SpaceDomain>(),
        "O_SpaceBoxDomain docstring...")

        .def(py::init<SpaceDomain&>(),
            "__init__ docstring..."
            "group"_a,
            py::keep_alive<1, 2>())

        .def_property_readonly("boxes",
                &constant_size::time::omnipresent::SpaceBoxDomain::boxes,
            "boxes docstring...",
            py::return_value_policy::reference_internal)
    ;
}

}  // namespace python
}  // namespace lue
