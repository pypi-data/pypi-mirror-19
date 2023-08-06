#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "utf8tool.h"

namespace py = pybind11;

PYBIND11_PLUGIN(utf8proc) {
    py::module m("utf8proc");

    m.def("normalize", &normalize);
    m.def("naturalSmallerThan", &naturalSmallerThan);
    m.def("sort", &naturalSortedIndices); //Returns indices
    m.def("naturalSorted", &naturalSorted); //Returns strings

#ifdef VERSION_INFO
    m.attr("__version__") = py::str(VERSION_INFO);
#else
    m.attr("__version__") = py::str("dev");
#endif

    return m.ptr();
}