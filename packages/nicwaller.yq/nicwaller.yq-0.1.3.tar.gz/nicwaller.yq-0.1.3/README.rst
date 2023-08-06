yq
==

yq is a wrapper for jq that supports YAML files.

The yq wrapper was written by earonesty. I just added the packaging.

Pre-requisites

- You need to have jq already installed. (On Mac run `brew install jq`)

To install, just checkout this repository then run:

    make install

Use yq the same way you use jq. So if you have a YAML file called example.yaml:

    yq . example.yaml
