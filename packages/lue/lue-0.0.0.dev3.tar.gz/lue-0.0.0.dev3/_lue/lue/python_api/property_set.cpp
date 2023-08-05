#include "lue/cxx_api/constant_size.h"
#include "lue/cxx_api/property_sets.h"
#include "lue/python_api/collection.h"
#include "lue/python_api/numpy.h"
#include <pybind11/numpy.h>
#include <numpy/arrayobject.h>


namespace py = pybind11;
using namespace pybind11::literals;


namespace lue {
namespace python {

DEFINE_INIT_NUMPY()


std::tuple<hid_t, hid_t> numpy_type_to_hdf5_types(
    int type_id)
{
    hid_t file_type_id = -1;
    hid_t memory_type_id = -1;

    switch(type_id) {
        case NPY_UINT32: {
            file_type_id = H5T_STD_U32LE;
            memory_type_id = H5T_NATIVE_UINT32;
            break;
        }
        case NPY_INT32: {
            file_type_id = H5T_STD_I32LE;
            memory_type_id = H5T_NATIVE_INT32;
            break;
        }
        case NPY_UINT64: {
            file_type_id = H5T_STD_U64LE;
            memory_type_id = H5T_NATIVE_UINT64;
            break;
        }
        case NPY_INT64: {
            file_type_id = H5T_STD_I64LE;
            memory_type_id = H5T_NATIVE_INT64;
            break;
        }
        case NPY_FLOAT32: {
            file_type_id = H5T_IEEE_F32LE;
            memory_type_id = H5T_NATIVE_FLOAT;
            break;
        }
        case NPY_FLOAT64: {
            file_type_id = H5T_IEEE_F64LE;
            memory_type_id = H5T_NATIVE_DOUBLE;
            break;
        }
        default: {
            throw std::runtime_error("Unsupported numpy type");
            break;
        }
    }

    return std::make_tuple(file_type_id, memory_type_id);
}


void init_property_set(
        py::module& module)
{

    init_numpy();

    BASE_COLLECTION(PropertySet)

    py::class_<PropertySets>(module, "PropertySets",
            py::base<PropertySetCollection>(),
        "PropertySets docstring...")
        .def("__repr__",
            [](PropertySets const& property_sets) {
                return "PropertySets(size=" + std::to_string(
                    property_sets.size()) + ")";
            }
        )
        // .def("add", &PropertySets::add,
        //     "add docstring...",
        //     py::return_value_policy::reference_internal)
    ;


    py::enum_<SizeOfItemCollectionType>(module, "size_of_item_collection",
        "size_of_item_collection docstring...")
        .value("constant", SizeOfItemCollectionType::constant_size)
    ;


    py::class_<PropertySetConfiguration>(module, "PropertySetConfiguration",
        "PropertySetConfiguration docstring...")
        .def(py::init<SizeOfItemCollectionType const>(),
            "__init__ docstring...",
            "type"_a)
        .def_property_readonly("size_of_item_collection_type",
                &PropertySetConfiguration::size_of_item_collection_type,
            "size_of_item_collection_type docstring...")
    ;


    py::class_<PropertySet>(module, "PropertySet", py::base<hdf5::Group>(),
        "PropertySet docstring...")
        .def("__repr__",
            [](PropertySet const& property_set) {
                return "PropertySet(pathname='" +
                    property_set.id().pathname() + "')";
            }
        )
        .def_property_readonly("configuration", &PropertySet::configuration,
            "configuration docstring...",
            py::return_value_policy::reference_internal)
        .def_property_readonly("domain", &PropertySet::domain,
            "domain docstring...",
            py::return_value_policy::reference_internal)
        // .def("add_property", &PropertySet::add_property,
        //     "add_property docstring...",
        //     py::return_value_policy::reference_internal)
        .def_property_readonly("properties", &PropertySet::properties,
            "properties docstring...",
            py::return_value_policy::reference_internal)
    ;

    // TODO Refactor Group and PropertySet API's into common base classes.
    //      Multiple classes implement the interfaces.
    py::class_<constant_size::time::PropertySet>(module, "_PropertySet",
        "_PropertySet docstring...")

        // Group API
        .def_property_readonly("id", &constant_size::time::PropertySet::id,
            "id docstring...",
            py::return_value_policy::reference_internal)
        .def_property_readonly("domain", &constant_size::time::PropertySet::domain,
            "domain docstring...",
            py::return_value_policy::reference_internal)



        // PropertySet API
        // .def("add_property", &time::PropertySet::add_property,
        //     "add_property docstring...",
        //     py::return_value_policy::reference_internal)
        .def_property_readonly("configuration",
            &constant_size::time::PropertySet::configuration,
            "configuration docstring...",
            py::return_value_policy::reference_internal)
        .def_property_readonly("properties", &constant_size::time::PropertySet::properties,
            "properties docstring...",
            py::return_value_policy::reference_internal)
    ;

    py::class_<constant_size::time::omnipresent::PropertySet>(module,
        "O_PropertySet", py::base<constant_size::time::PropertySet>(),
        "O_PropertySet docstring...")

        .def(py::init<PropertySet&>(),
            "__init__ docstring..."
            "group"_a,
            py::keep_alive<1, 2>())

        .def("reserve_items",
                &constant_size::time::omnipresent::PropertySet::reserve_items,
            "reserve_items docstring...",
            py::return_value_policy::reference_internal)

        // .def_property_readonly("items",
        //         &time::omnipresent::PropertySet::items,
        //     "items docstring...",
        //     py::return_value_policy::reference_internal)

        .def_property_readonly("ids",
                &constant_size::time::omnipresent::PropertySet::ids,
            "ids docstring...",
            py::return_value_policy::reference_internal)

        .def("add_property", [](
                    constant_size::time::omnipresent::PropertySet& self,
                    std::string const& name,
                    py::handle const& numpy_type_id_object,
                    py::tuple const& shape,
                    py::tuple const& chunks) ->
                        constant_size::time::omnipresent::same_shape::Property& {

                int numpy_type_id = NPY_NOTYPE;
                {
                    PyArray_Descr* dtype;
                    if(!PyArray_DescrConverter(numpy_type_id_object.ptr(),
                            &dtype)) {
                        throw py::error_already_set();
                    }
                    numpy_type_id = dtype->type_num;
                    Py_DECREF(dtype);
                }

                Shape shape_(shape.size());

                for(size_t i = 0; i < shape.size(); ++i) {
                    shape_[i] = py::int_(shape[i]);
                }

                Chunks chunks_(chunks.size());

                for(size_t i = 0; i < chunks.size(); ++i) {
                    chunks_[i] = py::int_(chunks[i]);
                }

                hid_t file_type_id, memory_type_id;
                std::tie(file_type_id, memory_type_id) =
                    numpy_type_to_hdf5_types(numpy_type_id);

                return self.add_property(name, file_type_id, memory_type_id,
                    shape_, chunks_);
            },
            "add_property docstring...",
            py::return_value_policy::reference_internal)

        .def("add_property", [](
                    constant_size::time::omnipresent::PropertySet& self,
                    std::string const& name,
                    py::handle const& numpy_type_id_object,
                    size_t const rank) ->
                        constant_size::time::omnipresent::different_shape::Property& {

                int numpy_type_id = NPY_NOTYPE;
                {
                    PyArray_Descr* dtype;
                    if(!PyArray_DescrConverter(numpy_type_id_object.ptr(),
                            &dtype)) {
                        throw py::error_already_set();
                    }
                    numpy_type_id = dtype->type_num;
                    Py_DECREF(dtype);
                }

                hid_t file_type_id, memory_type_id;
                std::tie(file_type_id, memory_type_id) =
                    numpy_type_to_hdf5_types(numpy_type_id);

                return self.add_property(name, file_type_id, // memory_type_id,
                    rank);
            },
            "add_property docstring...",
            py::return_value_policy::reference_internal)
    ;


#define cast(object, type) \
    try {  \
        object.cast<type&>();  \
        std::cout << " " #type "&\n";  \
    }  \
    catch(...) {  \
        std::cout << "!" #type "&\n";  \
    }  \
    try {  \
        object.cast<type*>();  \
        std::cout << " " #type "*\n";  \
    }  \
    catch(...) {  \
        std::cout << "!" #type "*\n";  \
    }  \
    try {  \
        object.cast<type const&>();  \
        std::cout << " " #type " const&\n";  \
    }  \
    catch(...) {  \
        std::cout << "!" #type " const&\n";  \
    }  \
    try {  \
        object.cast<type const*>();  \
        std::cout << " " #type " const*\n";  \
    }  \
    catch(...) {  \
        std::cout << "!" #type " const*\n";  \
    }


    // py::class_<time::omnipresent::size_per_item::constant::PropertySet>(
    //     module, "O_C_PropertySet",
    //     py::base<time::omnipresent::PropertySet>(),
    //     "O_C_PropertySet docstring...")

    //     .def(py::init<PropertySet&>(),
    //         "__init__ docstring..."
    //         "group"_a,
    //         py::keep_alive<1, 2>())
    // //     .def("add_property", [](
    // //                 time::omnipresent::omnipresent::PropertySet& self,
    // //                 std::string const& name,
    // //                 py::handle const& numpy_type_id_object,
    // //                 py::tuple const& shape,
    // //                 py::tuple const& chunks) ->
    // //                     time::omnipresent::omnipresent::Property& {

    // //             int numpy_type_id = NPY_NOTYPE;
    // //             {
    // //                 PyArray_Descr* dtype;
    // //                 if(!PyArray_DescrConverter(numpy_type_id_object.ptr(),
    // //                         &dtype)) {
    // //                     throw py::error_already_set();
    // //                 }
    // //                 numpy_type_id = dtype->type_num;
    // //                 Py_DECREF(dtype);
    // //             }

    // //             Shape shape_(shape.size());

    // //             for(size_t i = 0; i < shape.size(); ++i) {
    // //                 shape_[i] = py::int_(shape[i]);
    // //             }

    // //             Chunks chunks_(chunks.size());

    // //             for(size_t i = 0; i < chunks.size(); ++i) {
    // //                 chunks[i] = chunks[i];
    // //             }

    // //             return self.add_property(name,
    // //                 numpy_type_to_hdf5_type(numpy_type_id), shape_, chunks_);
    // //         },
    // //         // &time::omnipresent::omnipresent::PropertySet::add_property,
    // //         "add_property docstring...",
    // //         py::return_value_policy::reference_internal)
    // //     .def("reserve_items",
    // //             &time::omnipresent::omnipresent::PropertySet::reserve_items,
    // //         "reserve docstring...",
    // //         py::return_value_policy::reference_internal)
    // //     .def_property_readonly("items",
    // //             &time::omnipresent::omnipresent::PropertySet::items,
    // //         "items docstring...",
    // //         py::return_value_policy::reference_internal)
    // ;

}

}  // namespace python
}  // namespace lue
