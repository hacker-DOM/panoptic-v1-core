#!/usr/bin/env just --justfile
# https://github.com/casey/just
# Also `brew install just`

# It seems that on MacOS, just will use `zsh` to run commands (recipes).
# I think it uses the system's default shell. To make sure it's consistent,
# let's set it explicitly.
set shell := ["zsh", "-c"]

# Run `just f` to fuzz this project! :-)
alias f := fuzz

# The first recipe will be the default one (the one run if you just run `just` in the directory). We'll define the implementation later and just refer to it now.
default: default_impl

setup:
    set -e;
    python3 -m venv .venv;
    source .venv/bin/activate;
    pip install woke;

fuzz:
    WOKE_TESTS_FLOWS_COUNT=20 WOKE_TESTS_SEQUENCES_COUNT=2 woke --debug fuzz -s 4f2a521550c29390 --passive -n 1 woke_tests/tier2/test_.py

default_impl:
    # fun fact 1 - the $'...' syntax is called ANSI-C quoting and allows us to
    # interpret backslashes as in the C language.
    # fun fact 2 - removing the `=` after `--list-prefix` will not work,
    # (the error msg is `error: Found argument '- ' which wasn't expected, or isn't valid in this context`)
    # I'm not sure if this is a quirk of shell or a bug in Just
    @just --list --unsorted --justfile {{justfile()}} --list-heading $'Recipes:\n' --list-prefix='- '


