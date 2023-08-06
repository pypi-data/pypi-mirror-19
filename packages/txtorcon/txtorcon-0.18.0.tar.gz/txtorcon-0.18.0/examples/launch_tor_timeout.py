from __future__ import print_function

"""
Launch a private Tor instance.
"""

import sys
import txtorcon
from twisted.internet.task import react
from twisted.internet.defer import inlineCallbacks


@inlineCallbacks
def main(reactor):
    # this demonstrates error-handing on timeouts
    yield txtorcon.launch(
        reactor,
        timeout=2,
        stdout=sys.stdout,
        data_directory="./tordata",
    )


if __name__ == '__main__':
    react(main)
