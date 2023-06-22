#!/usr/bin/env python3

"""Nagios plugin to monitor if the currently running release of debian matches the desired target distribution"""

import argparse
import validators
from natsort import natsort_keygen
from apt_repo import APTRepository
from urllib.request import urlopen
from nagiosplugin import Resource, Metric, Result, Check, Context
from nagiosplugin.state import Ok, Warn, Critical


class Release(Resource):

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
        mirror: str,
        fmt_metric=None,
        result_cls=Result,
    ):
        self.target = target
        super().__init__(name, fmt_metric, result_cls)

        # prepare natural comparison key generation function
        self.ns_key = natsort_keygen()

        # determine current debian version for target release
        repo = APTRepository(mirror, self.target, "main")
        self.target_version = repo.release_file.version

    def evaluate(self, metric, resource):
        """Compares metric with given Resource"""

        if self.ns_key(metric.value) < self.ns_key(self.target_version):
            self.result = Warn
            return self.result_cls(Warn, metric=metric)

        self.result = Ok
        return self.result_cls(Ok, metric=metric)

    def describe(self, metric):
        """Add description to warning"""

        if self.result == Warn:
            return f'OS version is older than "{self.target}" ({metric.value} < {self.target_version})'

        return None


def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "target",
        metavar="TARGET",
        type=str,
        nargs="?",
        default="stable",
        choices=("oldoldstable", "oldstable", "stable", "testing", "experimental"),
        help='Default: "stable", supported: "oldoldstable", "oldstable", "stable", "testing", "experimental"',
    )

    def url(s: str) -> str:
        """Validate if URL is valid"""
        if not validators.url(s):
            raise ValueError("Invalid repository URL provided")
        return s

    parser.add_argument(
        "--mirror",
        metavar="MIRROR",
        type=url,
        default="https://deb.debian.org/debian/",
        help="Debian Mirror to use as release reference. Default: https://deb.debian.org/debian/",
    )

    return parser.parse_args()


def main():
    """Software entry point"""

    # handle command line args
    args = parse_args()

    # execute check
    check = Check(Release(), ReleaseContext("release", args.target, args.mirror))
    check.main()


if __name__ == "__main__":
    main()
