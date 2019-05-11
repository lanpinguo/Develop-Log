#!/bin/bash

set -e

RPATH_FLAGS="-Wl,-rpath,/usr/local/lib:/usr/lib/x86_64-linux-gnu/hdf5/serial"
MY_LDFLAGS="-L/usr/local/lib -L/usr/lib/x86_64-linux-gnu/hdf5/serial ${RPATH_FLAGS}"
MY_CPPFLAGS="-I/usr/local/include -I/usr/include/hdf5/serial"

sudo apt-get update

# If building on Ubuntu 18.04LTS, replace libpng16-dev with libpng-dev,
# and libpython3.5-dev with libpython3-dev.
sudo apt-get -y install     \
    libblas-dev             \
    liblapack-dev           \
    libgmp-dev              \
    swig                    \
    libgsl-dev              \
    autoconf                \
    pkg-config              \
    libpng-dev            \
    git                     \
    guile-2.0-dev           \
    libfftw3-dev            \
    libhdf5-dev     \
    hdf5-tools              \
    libpython3-dev        \
    python3-numpy           \
    python3-scipy           \
    python3-matplotlib      \
    python3-pip             \
    gfortran

mkdir -p ~/install

cd ~/install
git clone https://github.com/NanoComp/harminv.git
cd harminv/
sh autogen.sh --enable-shared
make && sudo make install

cd ~/install
git clone https://github.com/NanoComp/libctl.git
cd libctl/
sh autogen.sh --enable-shared
make && sudo make install

cd ~/install
git clone https://github.com/NanoComp/h5utils.git
cd h5utils/
sh autogen.sh CC=mpicc LDFLAGS="${MY_LDFLAGS}" CPPFLAGS="${MY_CPPFLAGS}"
make && sudo make install

cd ~/install
git clone https://github.com/NanoComp/mpb.git
cd mpb/
sh autogen.sh --enable-shared CC=mpicc LDFLAGS="${MY_LDFLAGS}" CPPFLAGS="${MY_CPPFLAGS}" --with-hermitian-eps
make && sudo make install

cd ~/install
git clone https://github.com/HomerReid/libGDSII.git
cd libGDSII/
sh autogen.sh
make && sudo make install

sudo pip3 install --upgrade pip
# If pip3 doesn't work on ubuntu 18.04, just use pip
pip3 install --user --no-cache-dir mpi4py
export HDF5_MPI="ON"
pip3 install --user --no-binary=h5py h5py

cd ~/install
git clone https://github.com/NanoComp/meep.git
cd meep/
sh autogen.sh --enable-shared --with-mpi PYTHON=python3 \
    CC=mpicc CXX=mpic++ LDFLAGS="${MY_LDFLAGS}" CPPFLAGS="${MY_CPPFLAGS}"
make && sudo make install

