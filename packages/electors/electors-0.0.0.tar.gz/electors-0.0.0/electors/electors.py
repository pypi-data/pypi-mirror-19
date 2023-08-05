#!/usr/bin/env python

from __future__ import division


def main():

    CLINT = int(input("Number of votes for Clinton: "))
    TRUMP = int(input("Number of votes for Trump: "))
    THIRD = int(input("Number of third party votes: "))
    ELEC = int(input("Number of electoral votes in the state: "))

    TOT = CLINT + TRUMP + THIRD
    PROP_TRUMP = round((TRUMP / TOT) * ELEC)
    PROP_CLINT = round((CLINT / TOT) * ELEC)

    print("""
    Trump: {0}
    Clinton: {1}
    Third-Party: {2}\n""".format(int(PROP_TRUMP), int(PROP_CLINT), int(ELEC - (PROP_TRUMP + PROP_TRUMP))))

if __name__ == "__main__":
    main()
