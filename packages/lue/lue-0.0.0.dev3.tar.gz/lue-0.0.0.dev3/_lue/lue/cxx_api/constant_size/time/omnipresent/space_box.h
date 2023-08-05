#pragma once
#include "lue/cxx_api/constant_size/time/omnipresent/same_shape/item.h"


namespace lue {
namespace constant_size {
namespace time {
namespace omnipresent {

/*!
    @ingroup    lue_cxx_api_group
*/
class SpaceBox:
    public same_shape::Item
{

public:

                   SpaceBox            (hdf5::Identifier const& location);

                   SpaceBox            (hdf5::Identifier const& location,
                                        hid_t const type_id);

                   SpaceBox            (same_shape::Item&& coordinates);

                   SpaceBox            (SpaceBox const& other)=delete;

                   SpaceBox            (SpaceBox&& other)=default;

                   ~SpaceBox           ()=default;

    SpaceBox&      operator=           (SpaceBox const& other)=delete;

    SpaceBox&      operator=           (SpaceBox&& other)=default;

private:


};


SpaceBox           create_space_box    (hdf5::Identifier const& location,
                                        hid_t const file_type_id,
                                        hid_t const memory_type_id,
                                        size_t rank);

}  // namespace omnipresent
}  // namespace time
}  // namespace constant_size
}  // namespace lue
