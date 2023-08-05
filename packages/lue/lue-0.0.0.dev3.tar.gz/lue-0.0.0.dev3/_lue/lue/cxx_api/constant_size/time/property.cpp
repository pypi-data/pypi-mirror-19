#include "lue/cxx_api/constant_size/time/property.h"


namespace lue {
namespace constant_size {
namespace time {

Property::Property(
    lue::Property& group)

    : _group{std::ref(group)}

{
}


hdf5::Identifier const& Property::id() const
{
    return group().id();
}


std::string Property::name() const
{
    return group().name();
}


void Property::link_space_discretization(
    Property const& discretization)
{
    group().link_space_discretization(discretization.group());
}


lue::Property const& Property::group() const
{
    return _group.get();
}


lue::Property& Property::group()
{
    return _group.get();
}

} // namespace time
}  // namespace constant_size
} // namespace lue
