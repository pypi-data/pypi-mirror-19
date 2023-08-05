#include "lue/cxx_api/constant_size/time/time_domain.h"


namespace lue {
namespace constant_size {
namespace time {

TimeDomain::TimeDomain(
    lue::TimeDomain& group)

    : _group{std::ref(group)}

{
}

} // namespace time
}  // namespace constant_size
} // namespace lue
