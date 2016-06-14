import io
import os
import inspect
import sys
import shutil
import uuid
import time
import shutil
import logging
import argparse
import traceback

TEST_DIRECTORY = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
TEST_DATA_DIRECTORY = os.path.abspath(os.path.join(TEST_DIRECTORY, 'data'))
sys.path.append(os.path.join(TEST_DIRECTORY, '..', 'src'))

from common import helpers
from client import OasisApiClient

parser = argparse.ArgumentParser(description='Test the Oasis API client.')
parser.add_argument(
    '--url', metavar='N', type=str, default='http://localhost:8001', required=False,
    help='The base URL for the API.')
parser.add_argument(
    '--num_analyses', metavar='N', type=int, default='1', required=False,
    help='The number of analyses to run.')

args = parser.parse_args()

base_url = args.url
num_analyses = args.num_analyses

sys.path.append(os.path.join(TEST_DIRECTORY, '..', 'src'))
inputs_data_directory = os.path.join(TEST_DIRECTORY, '..', 'example_data', 'inputs', 'nationwide')

analysis_settings_data_directory = os.path.join(TEST_DIRECTORY, '..', 'example_data', 'analysis_settings_csv')
upload_directory = os.path.join("upload", str(uuid.uuid1()))

shutil.copytree(
    os.path.join(inputs_data_directory, "csv"),
    upload_directory)

num_failed = 0
num_completed = 0

for analysis_id in range(num_analyses):
    try:
        logger = logging.Logger("Test", logging.DEBUG)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        client = OasisApiClient.OasisApiClient(base_url, logger)
        inputs_location = client.upload_inputs_from_directory(upload_directory, do_validation=False)
        analysis_settings_json = "Test"
        #client.run_analysis(analysis_settings_json, inputs_location, "outputs", do_clean=False)
        client.run_analysis(analysis_settings_data_directory, "inputs", "outputs", do_clean=False)
        num_completed = num_completed + 1
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "*** print_exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
            limit=2, file=sys.stdout)
        print "*** print_exc:"
        traceback.print_exc()
        print "*** format_exc, first and last line:"
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        print "*** format_exception:"
        print repr(traceback.format_exception(exc_type, exc_value,
                                          exc_traceback))
        print "*** extract_tb:"
        print repr(traceback.extract_tb(exc_traceback))
        print "*** format_tb:"
        print repr(traceback.format_tb(exc_traceback))
        print "*** tb_lineno:", exc_traceback.tb_lineno
        num_failed = num_failed + 1

print "Done. Num completed={}; Num failed={}".format(num_completed, num_failed)
