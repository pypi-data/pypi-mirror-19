#pragma once
#include <hdf5.h>
#include <functional>
#include <memory>
#include <string>


namespace lue {
namespace hdf5 {

/*!
    @ingroup    lue_cxx_api_hdf5_group
    @brief      This class represents an HDF5 identifier.

    Scoping the identifier in this class ensures that the identifier is
    closed upon exiting the scope.

    Copies can be made. Only when the last copy goes out of scope will the
    identifier be closed.
*/
class Identifier
{

public:


    /*!
        @brief      Type of function to call when the identifier must
                    be closed.
    */
    using Close = std::function<void(hid_t)>;

                   Identifier          (hid_t id,
                                        Close const& close);

                   Identifier          (Identifier const& other);

                   Identifier          (Identifier&& other);

    virtual        ~Identifier         ();

    Identifier&    operator=           (Identifier const& other);

    Identifier&    operator=           (Identifier&& other);

    bool           is_valid            () const;

                   operator hid_t      () const;

    std::string    pathname            () const;

    std::string    name                () const;

private:

    //! HDF5 identifier.
    std::shared_ptr<hid_t> _id;

    //! Function to call when the identifier must be closed.
    Close          _close;

    void           close_if_necessary  ();

};

} // namespace hdf5
} // namespace lue
