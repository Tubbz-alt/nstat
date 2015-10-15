[![Code Climate](https://codeclimate.com/github/intracom-telecom-sdn/nstat/badges/gpa.svg)](https://codeclimate.com/github/intracom-telecom-sdn/nstat)
[![Build Status](https://travis-ci.org/intracom-telecom-sdn/nstat.svg?branch=develop_release_1.1)](https://travis-ci.org/intracom-telecom-sdn/nstat)
[![Coverage Status](https://coveralls.io/repos/intracom-telecom-sdn/nstat/badge.svg?branch=develop_release_1.1&service=github)](https://coveralls.io/github/intracom-telecom-sdn/nstat?branch=develop_release_1.1)

# NSTAT: Network Stress-Test Automation Toolkit

## Overview

NSTAT is an environment written in Python for easily writing and running
SDN controller stress tests in a highly-configurable and modular manner.

Key features in brief:
- [Fully automated, end-to-end testing](https://github.com/intracom-telecom-sdn/nstat/wiki/NSTAT#work-flow) with exhaustive test cases
- Easy and rich [configuration system](https://github.com/intracom-telecom-sdn/nstat/wiki/NSTAT#configuration-keys)
- [Scalable traffic generation](https://github.com/intracom-telecom-sdn/nstat/wiki/MT-Cbench),
  able to emulate networks in the order of [thousands of switches](https://github.com/intracom-telecom-sdn/NSTAT/wiki/odl_scalability_results_lithium)
- Unification of different stress tests, see below:
  * SouthBound idle switch scalability (with [Cbench](https://github.com/intracom-telecom-sdn/nstat/wiki/Southbound-idle-scalability-cbench),
  [MT-Cbench](https://github.com/intracom-telecom-sdn/nstat/wiki/Southbound-idle-scalability-mtcbench) and [Mininet](https://github.com/intracom-telecom-sdn/nstat/wiki/Southbound-idle-scalability-mininet))
  * SouthBound active switch scalability (with [Cbench](https://github.com/intracom-telecom-sdn/nstat/wiki/Southbound-active-scalability-cbench)
  and [MT-Cbench](https://github.com/intracom-telecom-sdn/nstat/wiki/Southbound-active-scalability-mtcbench))
  * SouthBound active switch stability (with [Cbench](https://github.com/intracom-telecom-sdn/nstat/wiki/Southbound-active-stability-cbench)
  and [MT-Cbench](https://github.com/intracom-telecom-sdn/nstat/wiki/Southbound-active-stability-mtcbench))
  * [Northbound flow scalablity](https://github.com/intracom-telecom-sdn/nstat/wiki/Northbound-active-scalability-mininet)
- Comprehensive reporting and configurable plotting

For a detailed features listing have a look at the [features](https://github.com/intracom-telecom-sdn/nstat/wiki/Features) page.

-----------------------------------------------------------

## Get started!

To get started right away and run some sample test cases, proceed to the
[installation](https://github.com/intracom-telecom-sdn/nstat/wiki/Installation)
page.

-----------------------------------------------------------

## Read the docs

- [NSTAT testing procedure, command line options and configuration parameters](https://github.com/intracom-telecom-sdn/nstat/wiki/NSTAT)
- documentation for tests
- [MT-Cbench](https://github.com/intracom-telecom-sdn/nstat/wiki/MT-Cbench) traffic generator
- [code design, concepts and conventions](https://github.com/intracom-telecom-sdn/nstat/wiki/Code-design)
- [code structure](https://github.com/intracom-telecom-sdn/nstat/wiki/Code-design#code-structure)
- [plotting methodology](https://github.com/intracom-telecom-sdn/nstat/wiki/Plotting)

-----------------------------------------------------------

## Browse performance results

- [6/29/2015]: Performance Stress Tests Report for **OpenDaylight Lithium Release**: [[pdf]](https://raw.githubusercontent.com/wiki/intracom-telecom-sdn/nstat/files/ODL_performance_report_v1.0.pdf).

- We provide indicative experimental results from [switch  scalability](https://github.com/intracom-telecom-sdn/nstat/wiki/ODL-scalability-results)
and [stability](https://github.com/intracom-telecom-sdn/nstat/wiki/ODL-stability-results)
test cases with OpenDaylight controller. The [CPU shares](https://github.com/intracom-telecom-sdn/nstat/wiki/Cpu-shares) page
shows the performance effect of allocating different CPU partitions
to test components.

-----------------------------------------------------------

## What's next?

Plans and ideas for next releases are provided in the [future releases](https://github.com/intracom-telecom-sdn/nstat/wiki/Future-releases) page.

-----------------------------------------------------------

## Contact and Support

For issues regarding NSTAT, please use the [issue tracking](https://github.com/intracom-telecom-sdn/nstat/issues) section.

For any other questions and feedback, contact us at [nstat-support@intracom-telecom.com](mailto:nstat-support@intracom-telecom.com).
