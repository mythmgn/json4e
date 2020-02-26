#!/bin/bash                                                                                                                                                                                                   
# ##########################################################################                           
# Author: Guannan Ma                                                                                              
# Brief:  Upload json4 to pypi                                                                                             
#                                                                                                      
# Returns:                                                                                             
#   succ: 0                                                                                            
#   fail: not 0                                                                                        
# ##########################################################################   
rm -rf ./build ./json4e.egg-info ./dist
python setup.py bdist_wheel
twine upload  output/dist/*
