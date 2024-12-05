# Coding Contest Solutions

This is a repository for my solutions to coding contests. I will be using python for the solutions.

## How to Run

There are VS code launch templates that will run the solution for the current file. There is support for three example test input files and the full input file itself. The way the launch templates work is run main.py and redirect current file dynamically as a module. The example/input file is the first argument to the module. This allows for the import of the common modules to work correctly.

## Directory Structure

```sh
mkdir -p src/{contest name}/y{four digiti year}/{number system}
cd !!
touch solution.py
touch input.txt
touch example1.txt
touch example2.txt
```
