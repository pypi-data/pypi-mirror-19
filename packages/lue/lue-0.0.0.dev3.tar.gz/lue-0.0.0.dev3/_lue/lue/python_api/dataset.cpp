#include "lue/cxx_api/dataset.h"
#include <pybind11/pybind11.h>


namespace py = pybind11;
using namespace pybind11::literals;


namespace lue {
namespace python {

void init_dataset(
        py::module& module)
{

    py::class_<Dataset>(module, "Dataset", py::base<hdf5::File>(),
        R"(LUE dataset representing the scientific database

    A LUE dataset can contain collections of universes, phenomena, and/or
    property sets.

    It is not possible to create Dataset instances from scratch:
    a constructor is not defined. New datasets can be created with the
    free function create_dataset(). Existing datasets can be opened
    with open_dataset().

    A LUE dataset is not similar to an HDF5 dataset. An HDF5 dataset
    represents a multidimensional array in an HDF5 file. The HDF5 file
    is managed by the LUE dataset.
)")
        .def("__repr__",
            [](Dataset const& dataset) {
                return "Dataset(name='" + dataset.pathname() + "')";
            }
        )
        .def("add_phenomenon", &Dataset::add_phenomenon,
            R"(Add new phenomenon to dataset

    :param str name: Name of phenomenon to create
    :raises RuntimeError: In case the phenomenon cannot be created
)",
            "name"_a,
            py::return_value_policy::reference_internal)
        .def_property_readonly("phenomena", &Dataset::phenomena,
            R"(Return phenomena collection

    :rtype: lue.Phenomena
)",
            py::return_value_policy::reference_internal)
        .def("add_universe", &Dataset::add_universe,
            R"(Add new universe to dataset

    :param str name: Name of universe to create
    :raises RuntimeError: In case the universe cannot be created
)",
            "name"_a,
            py::return_value_policy::reference_internal)
        .def_property_readonly("universes", &Dataset::universes,
            R"(Return universes collection

    :rtype: lue.Universes
)",
            py::return_value_policy::reference_internal)
    ;


    py::enum_<unsigned int>(module, "access_flag",
        "access_flag docstring...")
        .value("rw", H5F_ACC_RDWR)
        .value("ro", H5F_ACC_RDONLY)
    ;


    // TODO Support passing in access flags
    module.def("open_dataset", &open_dataset,
            // [](std::string const& name) {
            //     return open_dataset(name, H5F_ACC_RDWR);
            // },
        "name"_a, "flags"_a,
        "Open existing LUE dataset\n",
        py::return_value_policy::move);
    module.def("create_dataset", &create_dataset,
        "name"_a,
        "Create new LUE dataset\n"
        "\n"
        "If the dataset already exists it is overwritten",
        py::return_value_policy::move);

}

}  // namespace python
}  // namespace lue
