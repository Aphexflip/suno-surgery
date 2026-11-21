# Suno Surgery: public project case study

## Problem

An AI generated song can sound good overall while still containing a flawed lyric, an awkward transition, or a short damaged section. Recreating the entire song can discard the parts that already work. I wanted a more controlled way to identify the problem, make a targeted change, compare versions, and keep the original.

## What this project contains

The repository has three related tools:

1. A Chrome and Edge browser extension for marking a section of a song and preparing a prompt that a person can use in Suno's own editing interface.
2. An offline browser interface for comparing and joining downloaded WAV audio files.
3. A Python command line utility for keeping track of song versions, notes, and local audio patching workflows.

These components are intended to remain useful independently. The browser extension does not automate Suno's private interfaces, capture credentials, or depend on an unofficial Suno API.

## My role and use of AI

I initiated the product idea and defined the practical workflow and requirements. I worked with AI coding tools to create and refine the implementation, then organized the parts into a single project. The tools produced substantial portions of the code. I am not claiming that I manually wrote every line.

The repository README credits ChatGPT for the original local editing interface and Muse for the original Python utility and browser extension. My contribution includes the problem definition, product direction, integration decisions, review of the workflow, and continued iteration.

## Technical choices

The project favors local processing, explicit user actions, preserving originals, and understandable file based version tracking. The Python utility uses standard library code for its core functionality. The extension and browser interface can be inspected and run locally.

The repository includes unit tests and instructions to reproduce them. Documentation reports 17 passing Python tests at the time the components were consolidated. That is not a claim that every browser workflow or real song has been comprehensively tested.

## What is demonstrated, and what is not

Demonstrated in the repository: code for the three tools, an executable local workflow, installation instructions, tests, and clear rules that prohibit collecting Suno login credentials or bypassing its official interface.

Still to validate: complete workflows with a larger selection of real downloaded tracks, broader browser compatibility, error handling under unusual audio files, and usefulness to people beyond my own experiments. This is an independent project, not evidence of a commercial deployment or measured customer impact.

## Why this matters to my engineering work

I have spent more than 19 years working with complex equipment and supporting customers. That background shapes how I approach software: keep the working parts intact, isolate the problem, make a controlled change, check the result, and document what happened.

AI tools have made it possible for me to explore software ideas faster. My goal is to build things that are useful, understandable, and enjoyable, while being clear about what is still experimental.

## Explore the project

[Project README](README.md)

[Browser extension](extension/README.md)

[Offline audio editor](gui/README.md)

[Python utility](cli/README.md)

[Tests](cli/tests)
