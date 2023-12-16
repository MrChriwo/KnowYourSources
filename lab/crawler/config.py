# crawler config file contains the handling of the parameters / arguments
import os
import argparse
import logging
import requests


__prefix__ = '[Crawler]'


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Crawler for the abstracts of the web')
    parser.add_argument('--source', help='defines the source on kaggle', required=True)
    parser.add_argument('--target', help='defines the target column to crawl', nargs="+" ,required=True)
    # parser.add_argument('--output', help='defines the output file', required=False, default="output.txt")
    parser.add_argument('--workers', help='defines the number of crawler workers', required=False, default="1")
    parser.add_argument('--logfile', help='defines the log file', required=False, default="crawler.log")
    args = parser.parse_args()
    return args

def check_source(url): 
    url = f"https://www.kaggle.com/datasets/{url}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f'{__prefix__} The source is not valid')
            return False
        else:
            print(f'{__prefix__} source is valid')
            return True
    except Exception as e:
        print(f'{__prefix__} Error while checking the source: {e}')
        return False


def create_file(target) -> bool:
    print(f'{__prefix__} Creating file...\n')

    working_directory = os.getcwd()

    # If the output file is not absolute, file will be placed in the working directory
    if not os.path.isabs(target):
        target = os.path.join(working_directory, target)

    # Checking if the directory exists, if not, it will be created
    output_directory = os.path.dirname(target)
    if not os.path.exists(output_directory):
        try:
            print(f'{__prefix__} Creating directory {output_directory}')
            os.makedirs(output_directory)
        except Exception as e:
            print(f'{__prefix__} Error while creating the file directory: {e}')
            return False

    # try to create the file
    try:
        with open(target, 'w') as f:
            f.write('')
        print(f'{__prefix__} File created at', target + '\n')
        return True
    except Exception as e:
        print(f' {__prefix__} Error while creating the file: {e}')
        return False
    

# checking the arguments
def check_arguments(args: argparse.Namespace) -> bool:
    print(type(args.target))
    if args.source == "":
        print(f"{__prefix__} The source is not defined")
        return False
    else: 
        if not check_source(args.source):
            return False

    # if args.output is not None and not os.path.exists(args.output):
    #     if not create_file(args.output):
    #         return False
        
    if args.logfile is not None and not os.path.exists(args.logfile):
        if not create_file(args.logfile):
            return False
    if args.workers is not None and not args.workers.isdigit():
        print(f"{__prefix__} The number of workers is not a digit")
        return False
    return True

# initialize the arguments- if the arguments are not valid, the program will be terminated
# if the arguments are valid, the arguments will be returned

def init_args(): 
    args = get_arguments()
    if not check_arguments(args):
        return
    else:
        return args 