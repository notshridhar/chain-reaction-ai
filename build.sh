# Just a small script to build all c extension modules
# and copy the built libraries to working folder


# build modules
cd csource/
python3 setup_chainengine.py  build --build-lib ./build/libs
python3 setup_minimaxagent.py build --build-lib ./build/libs

# copy to backends folder
cd ..
cp csource/build/libs/* core/backends/c_ext/
rm core/backends/c_ext/extn.md
