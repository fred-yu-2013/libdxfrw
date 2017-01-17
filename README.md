libdxfrw
==========

libdxfrw is a free C++ library to read and write DXF files in both formats, ascii and binary form.
Also can read DWG files from R14 to the last V2015.
 It is licensed under the terms of the GNU General Public License version 2 (or at you option
any later version).


If you are looking for general information about the project, check our website:
http://sourceforge.net/projects/libdxfrw

Building and installing the library
==========

Use the tipical 
```
autoreconf -vfi (optional)
./configure
make
make install (as root)
```

[VC++]
- Open vs2013\libdxfrw.sln with VS2013
- Build Solution
There is also a dwg to dxf converter that depends on libdxfrw that can be built the same way.
- Open dwg2dxf\vs2013\dwg2dxf.sln with VS2013
- Build Solution

Example usage of the library
==========

The dwg to dxf converter (dwg2dxf) included in this package can be used as reference.

