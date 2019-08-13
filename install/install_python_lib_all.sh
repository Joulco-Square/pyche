#!/usr/bin/env bash

SCRIPT_DIR="$(realpath "$(dirname "$BASH_SOURCE")")"

$SCRIPT_DIR/install_python_lib.sh 3.5;
$SCRIPT_DIR/install_python_lib.sh 3.7;