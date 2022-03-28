#!/bin/bash

PACKAGES=(
  "pydocstyle"
  "pylint"
  "black"
  "osmnx"
  "networkx"
  "scikit-learn"
)

echo "Starting to check and install packages..."

if [[ "$VIRTUAL_ENV" != "" ]]; then
  echo "You are in a working virtualenv $VIRTUAL_ENV";
  python="$VIRTUAL_ENV/bin/python3"
  for package in ${PACKAGES[@]}; do
    if ! ${python} -c "import $package" &>/dev/null; then
      pip3 install $package
    fi
  done
  echo "All packages are installed."
else
    echo "You are not in a working virtualenv"
    echo "Exiting..."
    exit 1;
fi
