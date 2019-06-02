#!/bin/bash

cd msh_so
tar -cvf msh_so.tar 0.fat 1.img
dd if=msh_so.tar of=msh_so.img
cd ..
cp msh_so/msh_so.img msh/
rm -rf msh_so/msh_so.img
rm -rf msh_so/msh_so.tar