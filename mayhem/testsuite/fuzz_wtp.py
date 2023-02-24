#!/usr/bin/env python3

import ast
import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports():
    from bugbear import BugBearChecker, BugBearVisitor

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    if fdp.ConsumeBool():
        # Test BugBearChecker
        with fdp.ConsumeTemporaryFile('.py', all_data=True, as_bytes=False) as tmp_name:
            BugBearChecker(filename=tmp_name)
    else:
        # Test BugBearVisitor
        tree = ast.parse(fdp.ConsumeRemainingString())
        BugBearVisitor(filename="<string>", lines=[]).visit(tree)


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
