# flake8: noqa

import os
import sys
from lecloud import actions

# we read access key from system environment in this case.
# so make sure you have properly set them before run this test.
#
# typically execute shell command:
#
#     export ACCESS_KEY=YOUR_ACCESS_KEY
#     export ACCESS_SECRET=YOUR_ACCESS_KEY
#     export ENDPOINT_URL=SOME_REGION_ENDPOINT
#     export IS_DEBUG=True
#

actions.setup(os.environ['ACCESS_KEY'],
              os.environ['ACCESS_SECRET'],
              os.environ['ENDPOINT_URL'],
              os.environ['IS_DEBUG'])


def describe_instances():
    ret = actions.describe_instances()
    print ret


def describe_volumes():
    ret = actions.describe_volumes()
    print ret


def describe_networks():
    ret = actions.describe_networks()
    print ret


if __name__ == '__main__':
    describe_instances()
    describe_volumes()
    describe_networks()
