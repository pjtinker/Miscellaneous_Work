# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 13:21:47 2018

@author: hemlo
"""

import os
import sys, getopt
import argparse
import pandas as pd
import numpy as np
import re

pre = re.compile('^.__')
suff = re.compile('\([1-9][0-9]+\)$')
seen = re.compile('_[a-z]$')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",  help="input file name", default=False)
    parser.add_argument("-o", "--output",  help="output file name", default=False)
    args = parser.parse_args()
    
    if(not args.input or not args.output):
        print("Invalid number of arguments")
        sys.exit(1)
    if(not args.input.endswith('.csv')):
        print("Input file must be .csv format")
        sys.exit(1)
    if(not args.output.endswith('.csv')):
        args.output = args.output + ".csv"
    try:
        data = pd.read_csv(args.input)
    except Exception as e:
        print("Unable to open " + args.input + "\nPlease check the file path.")
        sys.exit(1)
    else:
        pass
    finally:
        pass
    columns = ['OTU','Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
    new_data = pd.DataFrame(columns=columns)
    new_data['OTU'] = data['OTU']
    for i in range(1, len(columns)):
        tax = data.Taxonomy.str.split(';').str.get(i-1)
        for idx, line in enumerate(tax):
            line = re.sub(pre, '', line)
            line = re.sub(suff, '', line)
            if line:
                tax[idx] = line
            else:
                line = new_data[columns[i-1]][idx]
                if re.search(seen, line):
                    tax[idx] = new_data[columns[i-1]][idx]
                else:
                    tax[idx] = new_data[columns[i-1]][idx] + '_' + columns[i-1][0].lower()
                
    
        new_data[columns[i]] = tax
    try:
        new_data.to_csv(args.output, index=False)  
    except Exception as e:
        print("Unable to save file " + args.output)
        sys.exit(1)
    sys.exit(0)        
    
if __name__ == '__main__':
    main()