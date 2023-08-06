
# OneFL Deduper

| Branch | [Travis-CI] | [Coveralls] |
| :----- | :---------------------------: | :-------: |
| Master | [![Build Status](https://travis-ci.org/ufbmi/onefl-deduper.svg?branch=master)](https://travis-ci.org/ufbmi/onefl-deduper?branch=master) | [![Coverage Status](https://coveralls.io/repos/github/ufbmi/onefl-deduper/badge.svg?branch=master)](https://coveralls.io/github/ufbmi/onefl-deduper?branch=master) |
| Develop | [![Build Status](https://travis-ci.org/ufbmi/onefl-deduper.svg?branch=develop)](https://travis-ci.org/ufbmi/onefl-deduper?branch=develop) | [![Coverage Status](https://coveralls.io/repos/github/ufbmi/onefl-deduper/badge.svg?branch=develop)](https://coveralls.io/github/ufbmi/onefl-deduper?branch=develop) |

# Intro

Welcome to the OneFlorida "De-Duper" tool.

This tool genereates "Linkage Unique Identifiers" (LUID's)
used for patient de-duplication (aka "Entity Resolution", aka "Record Linkage").


The current plan is to have a CSV files as input for two separate scripts
as in the diagram below:

<pre>

    +- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    |   Partner Domain
    |
    | (generate a CSV files with PHI)
    |
    |       +--------------+                     +------------+
    |       | PHI_DATA.csv | --> hash_gen.py --> | HASHES.csv |
    |       +--------------+                     +------------+
    |                                               ||
    +- - - - - - - - - - - - - - - - - - - - - - -  || - - - - - - - - - - - - 
    |                                               \/
    |                                       +-----------------+
    |                                       |  UF SFTP Server |
    |                                       +-----------------+
    |                                           ||
    |                                           ||
    |                                           \/
    |                                       +------------+
    |      ____________                     | HASHES.csv |
    |    /              \                   +------------+
    |   |               /|                      /
    |   |\_____________/ |                     /
    |   |              | |  <-- ofid_gen.py <--
    |   |  UF Database | |                     
    |   |              |/ 
    |    \_____________/
    |
    |    UF Domain
    |
    |    (generate OF_ID from hashes)
    |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
</pre>


# References

- http://infolab.stanford.edu/serf/
- "Swoosh: A Generic Approach to Entity Resolution" - http://link.springer.com/article/10.1007%2Fs00778-008-0098-x
