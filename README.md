# blockchain_real_estate_workaround
Repository for blockchain based real estate transactional workaround using Ganache, Solidity and Python3.

## The documentation of solidity and web3 was extensively referred for this project development. With time these documentations are updated. Do prefer the latest documentation and modules for project to work effectively if this project breaks.

## The development was done on Python 3.6
## The project was tested on Python 3.6

## About Branch: <u>main</u>
> This is the development and workaround branch.

### Directory Structure
```
|--- blockchain_workaround      ### Directory wherein basic solidity and python integration was tried and tested.
|
|--- land_registration_workaround   ### Use case specific workaround was performed in this directory.
|
|--- web_application   ### Final web application for use case was developed under this directory.

```

### To start the project implementation on your Desktop
> Install The Dependancies.
>> 1. Download and Install Node
>> 2. Install Ganache-cli using NPM.
```
    npm install -g ganache-cli
```
>> 3. Setup the solidity compiler
```
    npm install -g solc
```
>> 4. Setup the python virtual environment. 
>> 5. Install the python requirements.
```
    pip install -r requirements.txt
```

### References
* https://medium.com/coinmonks/how-to-develop-ethereum-contract-using-python-flask-9758fe65976e
* https://github.com/Kerala-Blockchain-Academy/Land-Registration
* https://github.com/ethereum/solc-js
* https://github.com/ethereum/py-solc
