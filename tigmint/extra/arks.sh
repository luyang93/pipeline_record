#!/usr/bin/env bash
export PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/ARKS/bin:$PATH
export LD_LIBRARY_PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/envs/tigmint/lib:$LD_LIBRARY_PATH

arks-make arks draft=draft.tigmint reads=reads time=1
