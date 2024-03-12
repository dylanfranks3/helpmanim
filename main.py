#!/usr/bin/env python
# cli interface
import argparse
import runner
def parser():
    parser = argparse.ArgumentParser(description='SIMULATOR CLI TOOL')
    parser.add_argument('-d', '--directory', help='<Required> arg to pass the directory, see readme', required=True)
    parser.add_argument('-m','--model',help='arg that decides the model, pass: normal, NAN',required=False,default='direct')
    parser.add_argument('-v','--visualise',help='arg whether to create a visualising .mp3 in exec path',type=bool,required=False,default=False)
    parser.add_argument('-l','--logging',help='arg whether to show state of network post execution in stdout',type=bool,required=False,default=False)
    
    args = vars(parser.parse_args())
    
    dataDirectory = args['directory']
    model = args['model']
    visualise = args['visualise']
    logging = args['logging']

    runner.buildSim(dataDirectory,model,visualise,logging)
