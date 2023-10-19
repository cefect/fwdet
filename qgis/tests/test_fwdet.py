'''
Created on Oct. 17, 2023

@author: cefect
'''


import pytest, copy, os, gc
from qgis.core import (
    QgsRasterLayer, QgsProject,
    QgsProcessingOutputLayerDefinition, QgsApplication
    )

from definitions import wbt_exe
from processing_scripts.fwdet_21 import FwDET as AlgoClass




@pytest.fixture(scope='function')
def output_params(qproj):
    """setting up default output parameters for tests"""    
    def get_out():
        return QgsProcessingOutputLayerDefinition(sink='TEMPORARY_OUTPUT', destinationProject=qproj)
    
    return {
        'OUTPUT_WaterDepth':get_out()
        }
    

@pytest.mark.dev 
@pytest.mark.parametrize('caseName',['PeeDee'])
@pytest.mark.parametrize('numIterations',[
                                            #0,
                                          1,
                                          #5
                                          ])
@pytest.mark.parametrize('slopeTH',[
                                    #0, 
                                    0.5
                                    ])
def test_runner(
        INUN_VLAY, 
        INPUT_DEM,   
        numIterations, slopeTH, caseName, 
        output_params, context, feedback,
        ):
    """test the main runner""" 
 
    
    #execute
    algo=AlgoClass()
    algo.initAlgorithm()
    algo._init_algo(output_params, context, feedback)
    res_d = algo.run_algo(INPUT_DEM, INUN_VLAY, numIterations, slopeTH)
     
    #validate
    assert isinstance(res_d, dict)
    assert set(res_d.keys()).symmetric_difference(output_params.keys())==set()
    
    #todo: add quantiative validation
    

