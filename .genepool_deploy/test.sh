#!/bin/bash -l

set -ex
module load python ruby/2.2.2
./script/test
./script/feature
./script/doc
