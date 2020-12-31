# TrainLink API
 
This is an API to intergrate with a DCC++ (or DCC++ EX) BaseStation. It provides a simple way to control it over your local network, with multiple instances supported. This means if you open a website using TrainLink on two devices connected to the same server, they will be kept in sync! If you don't know anything about TrainLink, I suggest you check out [the main repo](https://github.com/trainlink-org/trainlink-api), this gives a better overview of the TrainLink system.

**Note:** Before version 0.2.0, the whole codebase was kept in one repository. It has now been split into separate repositories to help with maintainance, but the old releases are kept in the [main repository](https://github.com/trainlink-org/trainlink-api) for now, just for completeness.

## What is in this Repository?
This repository contains the Python version of the server for TrainLink. Due to being written in Python, this version of the server can be run on most OSes, on most architectures (Raspberry Pi included!)

## Dependancies

## Installation

## Branches and releases
Releases are numbered according to the [Semantic Numbering](https://semver.org/) scheme. Therefore, releases will be numbered as following:

>Given a version number MAJOR.MINOR.PATCH, increment the:
>
>MAJOR version when you make incompatible API changes,  
MINOR version when you add functionality in a backwards compatible manner, and  
PATCH version when you make backwards compatible bug fixes."

### Branches
Master branch - Where code for the next release accumulates.  
Preview branch - Code that is finished, but not fully tested yet.  
Development-x.x branch - Where I write my code, almost guaranteed to be unstable!  
Any other branches - Same as above.

## Contributing
Want to suggest a feature, found a bug, or even better, fixed a bug? Please, go ahead and submit a pull request or issue! Every little helps, and even the smallest contribution will go a long way to help me with this project. You don't need to know how to code, as correcting typos or updating the documentation would help a lot! For more information on contributing, please see the wiki on the main repository.

## More Information
For more information please see the following:
* [The main repo](https://github.com/trainlink-org/trainlink-api) - Gives an overview of the TrainLink system.
* [The wiki](https://github.com/trainlink-org/trainlink-api/wiki) - FAQ and other repository maintainance help
* [Readthedocs](https://trainlink-api.readthedocs.io) - information on the API itself and the function calls

Many thanks,  
Matt  
\- November 2020