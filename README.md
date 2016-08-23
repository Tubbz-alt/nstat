[![Code Climate](https://codeclimate.com/github/intracom-telecom-sdn/nstat/badges/gpa.svg)](https://codeclimate.com/github/intracom-telecom-sdn/nstat)
[![Build Status](https://travis-ci.org/intracom-telecom-sdn/nstat.svg?branch=master)](https://travis-ci.org/intracom-telecom-sdn/nstat)
[![Coverage Status](https://coveralls.io/repos/intracom-telecom-sdn/nstat/badge.svg?branch=master&service=github)](https://coveralls.io/github/intracom-telecom-sdn/nstat?branch=master)
[![Docker Automated buil](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg?maxAge=2592000)](https://hub.docker.com/r/intracom/nstat/)

# NSTAT: Network Stress-Test Automation Toolkit

## Overview

NSTAT is an environment written in Python for easily writing and running
SDN controller stress tests in a highly-configurable and modular manner.

Key features in brief:
- [Fully automated, end-to-end testing](https://github.com/intracom-telecom-sdn/nstat/wiki/NSTAT#work-flow) with exhaustive test cases
- Easy and rich [configuration system](https://github.com/intracom-telecom-sdn/nstat/wiki/NSTAT#configuration-keys)
- Scalable traffic generation with [MT-Cbench](https://github.com/intracom-telecom-sdn/mtcbench) emulator,
  able to emulate networks in the order of thousands of switches
- Unification of different stress tests, see below:
    - [Switch scalability test with active MT-Cbench switches](https://github.com/intracom-telecom-sdn/nstat/wiki/Switch-scalability-test-with-active-MT-Cbench-switches)
    - [Switch scalability test with active Multinet switches](https://github.com/intracom-telecom-sdn/nstat/wiki/Switch-scalability-test-with-active-Multinet-switches)
    - [Switch scalability test with idle MT-Cbench switches](https://github.com/intracom-telecom-sdn/nstat/wiki/Switch-scalability-test-with-idle-MT-Cbench-switches)
    - [Switch scalability test with idle Multinet switches](https://github.com/intracom-telecom-sdn/nstat/wiki/Switch-scalability-test-with-idle-Multinet-switches)
    - [Controller stability test with active MT-Cbench switches](https://github.com/intracom-telecom-sdn/nstat/wiki/Controller-stability-test-with-active-MT-Cbench-switches)
    - [Controller stability test with idle Multinet switches](https://github.com/intracom-telecom-sdn/nstat/wiki/Controller-stability-test-with-idle-Multinet-switches)
    - [Flow scalability test with idle Multinet switches](https://github.com/intracom-telecom-sdn/nstat/wiki/Flow-scalability-test-with-idle-Multinet-switches)
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
- [MT-Cbench](https://github.com/intracom-telecom-sdn/mtcbench) traffic generator
- [code design, concepts and conventions](https://github.com/intracom-telecom-sdn/nstat/wiki/Code-design)
- [code structure](https://github.com/intracom-telecom-sdn/nstat/wiki/Code-design#code-structure)
- [plotting methodology](https://github.com/intracom-telecom-sdn/nstat/wiki/Plotting)

-----------------------------------------------------------

## Browse performance results

- [5/19/2016]: Performance Stress Tests Report v1.2: **"Beryllium Vs Lithium SR3"** [[pdf]](https://raw.githubusercontent.com/wiki/intracom-telecom-sdn/nstat/files/ODL_performance_report_v1.2.pdf)

- [1/2/2016]: Performance Stress Tests Report v1.1: **"Lithium SR3"** [[pdf]](https://raw.githubusercontent.com/wiki/intracom-telecom-sdn/nstat/files/ODL_performance_report_v1.1.pdf)

- [6/29/2015]: Performance Stress Tests Report v1.0: **"Lithium vs Helium Comparison"**: [[pdf]](https://raw.githubusercontent.com/wiki/intracom-telecom-sdn/nstat/files/ODL_performance_report_v1.0.pdf)

Indicative experimental results from [switch  scalability](https://github.com/intracom-telecom-sdn/nstat/wiki/ODL-Helium-SR3-switch-scalability-results)
and [stability](https://github.com/intracom-telecom-sdn/nstat/wiki/ODL-Helium-SR3-stability-results)
test cases with OpenDaylight controller are also provided.

The [CPU shares](https://github.com/intracom-telecom-sdn/nstat/wiki/Capping-controller-and-generator-CPU-resources-in-collocated-tests) page
shows the performance effect of allocating different CPU partitions
to individual NSTAT test components.

-----------------------------------------------------------

## What's next?

Plans and ideas for next releases are provided in the [future releases](https://github.com/intracom-telecom-sdn/nstat/wiki/Future-releases) page.

-----------------------------------------------------------

## Contact and Support

For issues regarding NSTAT, please use the [issue tracking](https://github.com/intracom-telecom-sdn/nstat/issues) section.

For any other questions and feedback, contact us at [nstat-support@intracom-telecom.com](mailto:nstat-support@intracom-telecom.com).



