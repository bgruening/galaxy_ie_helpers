#!/usr/bin/env python
import galaxy_ie_helpers
import sys
import argparse

def gx_get():
    parser = argparse.ArgumentParser(description='Get datasets from Galaxy.')
    parser.add_argument('-i', '--id',
                        required = True,
                        nargs='+',
                        help='The dataset ID/name from your Galaxy history, or a regex pattern to search all files in the history')
    parser.add_argument('-t', '--identifier_type', dest="identifier_type", choices=['hid', 'name', 'regex'], default='hid',
                        help='Type of the argument File/ID Number. Per default, integer ID number. If a pattern is specified in the -i argument, then this argument should be set to "regex"')
    parser.add_argument('--history-id', dest="history_id", default=None,
                        help='History ID. The history ID and the dataset ID uniquly identify a dataset. Per default this is set to the current Galaxy history.')
    args = parser.parse_args()

    # Returns a string, or a list of strings
    results = galaxy_ie_helpers.get( args.id, args.identifier_type, args.history_id )
    if type(results) is str:
        print(results)
    else:
        print('\n'.join(results))

def gx_put():
    parser = argparse.ArgumentParser(description='Put datasets back into Galaxy.')
    parser.add_argument('-p', '--filepath', 
        required = True,
        nargs='+',
        help='Specify the path to the files that should be uploaded to Galaxy.')
    parser.add_argument('-t', '--filetype', help='Galaxy file format. If not specified Galaxy will try to guess the filetype automatically.', default='auto')
    parser.add_argument('--history-id', dest="history_id", default=None, 
        help='History ID. The history ID and the dataset ID uniquly identify a dataset. Per default this is set to the current Galaxy history.')
    args = parser.parse_args()

    put( args.filepath, file_type=args.filetype, history_id=args.history_id )

def gx_get_user_history():
    parser = argparse.ArgumentParser(description='Get the History Dataset User.')
    parser.add_argument('--history-id', dest="history_id", default=None,
        help='History ID. The history ID and the dataset ID uniquly identify a dataset. Per default this is set to the current Galaxy history.')
    args = parser.parse_args()
    galaxy_ie_helpers.get_user_history(history_id=args.history_id)
