#!/usr/bin/env python3

"""Nagios plugin to monitor if the currently running release of debian matches the desired target distribution"""

import argparse
from natsort import natsort_keygen
from apt_repo import APTRepository
from urllib.request import urlopen
from nagiosplugin import Resource, Metric, Result, Check, Context
from nagiosplugin.state import Ok, Warn, Critical


class DebianRelease(Resource):

    """Resource Model for Current Debian Release"""

    def probe(self):
        with open("/etc/debian_version", "r") as fd:
            line = fd.readline().strip()
            fd.close()

        return Metric("debian_version", line, context="release")


class ReleaseContext(Context):

    """Evaluation context for debian release number"""

    def __init__(
        self,
        name: str,
        target: str,
        fmt_metric="Newer target release as currently installed {value} exists.",
        result_cls=Result,
    ):
        self.target = target
        super().__init__(name, fmt_metric, result_cls)

        # prepare natural comparison key generation function
        self.ns_key = natsort_keygen()

        # determine current debian version for target release
        repo = APTRepository("http://debian.rub.de/debian/", self.target, "main")
        self.version = repo.release_file.version

    def evaluate(self, metric, resource):
        """Compares metric with given Resource"""

        if self.ns_key(metric.value) < self.ns_key(self.version):
            return self.result_cls(Warn, metric=metric)

        return self.result_cls(Ok, metric=metric)


def parse_args():
    """Parse command line arguments"""


def main():
    """Software entry point"""

    # args = parse_args()
    check = Check(DebianRelease(), ReleaseContext("release", "stable"))
    check.main()


if __name__ == "__main__":
    main()
