# MIRbot 3.0.2

## Written by PyratLabs 2017, [http://pyrat.io/](http://pyrat.io/)

![MIRbot](images/mirbot.png)

### Description

[![Build Status](https://travis-ci.org/PyratLabs/MIRbot.svg?branch=master)](https://travis-ci.org/PyratLabs/MIRbot)

MIR (Modular Information Retrieval Bot) is a modular Python 3 IRC bot that I
wrote based upon Molobot by CodeDemons. It was created for personal uses but I
am releasing it for others to play with. I haven't yet explained how modules
work but I have included one module that I use on ngIRCd.

This has been released under the MIT License.


### Donations

**BITCOIN DONATIONS**
 * 1BFhtdVYmtAuYostpZLDAiGt1dmJaHTRDW


### Requirements

 1. Python 3.4+

### License

MIRbot has been released under an MIT License

    Copyright (c) 2017 PyratLabs (http://pyrat.io/)

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

### Installation

MIRbot can be installed using pip:

    pip install mirbot


### Usage

MIRbot comes with a CLI launcher:

    Command:        mirbot
    Arguments:      -c --config     /path/to/configdir
                    -d --daemon
                    -h --help

You can also run MIRbot from a Docker container, below is an example:

    docker build -t mirbot .
    docker run -d --name "mirbot" -v $(pwd)/.mirbot:/var/lib/mirbot mirbot
