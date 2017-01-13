#!/usr/local/bin/python3.6
import svn.remote
import svn.local
import argparse
import sys
import os
import subprocess
import pprint
from os.path import expanduser


TEST_CATEGORY_OPTIONS = ['AWSQASmokeTest', 'AWSRegression', 'QASmokeTest', 'QARegression', 'CTSmoke', 'ProdSmoke']
SVN_BASE_LOCATION = 'http://svn.proddev.cccis.com:8090/svn/QA/trunk/acceptance-projects/'
DEFAULT_WORKSPACE = os.path.join(expanduser('~'), 'workspace')

parser = argparse.ArgumentParser(add_help=True,)

parser.add_argument('--select', action='append', dest='acceptance_modules_collection',
                    default=[],
                    help='Select the acceptance test module(s). Example python runtest.py --select apm-acceptance --select cwf-accptance',
                    )
parser.add_argument('--list', '-l',
                    help='List the acceptance modules from the SVN location: http://svn.proddev.cccis.com:8090/svn/QA/trunk/acceptance-projects/',
                    required=False,
                    action='store_true'
                    )
parser.add_argument('--category', action='store',
                    help='Specify the test category. Available options: {}'.format(TEST_CATEGORY_OPTIONS),
                    )
parser.add_argument('--version', action='version',
                    version='%(prog)s 1.0')


args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

if args.list:
    for project_module in svn.remote.RemoteClient(SVN_BASE_LOCATION).list():
        print(project_module)
    exit(0)

print('Running the category {} in the projects {}'.format(args.category, args.acceptance_modules_collection))

origWD = os.getcwd()
print('The current working dir is: {}'.format(origWD))


for project in args.acceptance_modules_collection:
    project_local_path = os.path.join(DEFAULT_WORKSPACE, project)
    if not os.path.isdir(project_local_path):
        print('Checking out the project - {}'. format(project))
        svn.remote.RemoteClient(os.path.join(SVN_BASE_LOCATION, project)).checkout(project_local_path)
    else:
        print('Project - {}, already exists in workspace. Updating it'.format(project))
        os.chdir(project_local_path)
        proc = subprocess.Popen('svn up', stdout=subprocess.PIPE, shell=True)
        (output, err) = proc.communicate()
        print('{}'.format(output.decode('utf-8')))
        local_repo = svn.local.LocalClient(project_local_path)
        pprint.pprint(local_repo.info())
    print('Running the maven command: mvn clean -Dmaven.clean.failOnError=false -P{} test allure:report'.format(args.category))

os.chdir(origWD)
