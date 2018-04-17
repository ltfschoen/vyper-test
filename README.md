# README

---
Vyper smart contract language
---

Includes Troubleshooting tips and information about Vyper

# Table of Contents
  * [Chapter 0 - Setup WITHOUT Docker](#chapter-0)
  * [Chapter 1 - Setup WITH Docker](#chapter-1)
  * [Chapter 2 - Docker Containers and Images (Show/Delete)](#chapter-2)
  * [Chapter 3 - About Vyper](#chapter-3)

## Chapter 0 - Setup WITHOUT Docker <a id="chapter-0"></a>

* Install [PyEnv](https://github.com/pyenv/pyenv)
* Clone the repo
    ```bash
    git clone https://github.com/ethereum/vyper.git;
    cd vyper; make; make test;
    ```

* Troubleshooting
    * Refer to fork with [Troubleshooting steps](https://github.com/ltfschoen/vyper/blob/master/README_MAC.md)

## Chapter 1 - Setup WITH Docker <a id="chapter-1"></a>

* Install and Run Docker
* Fork my repo https://github.com/ltfschoen/vyper
* Terminal #1 - Clone the fork

    ```bash
    cd ~;
    git clone https://github.com/ltfschoen/vyper;
    cd vyper;
    ```    

* Terminal #1 - Build the custom DockerfileMac. This allows file changes in the Docker container to be synchronised with your host machine and vice versa.

    ```bash
    docker build -t vyper:1 . -f DockerfileMac
    ```

* Terminal #2 - Create another Bash terminal window/tab in the same folder

* Terminal #2 - Open the directory in a Text Editor or IDE

* Terminal #1 - Start a shell session in the Docker container that you just created.
    
    ```bash
    docker run -it -v $(pwd):/code vyper:1 /bin/bash
    ```

* Terminal #1 (within Docker Container shell session) - Compile a Vyper contract
    ```bash
    vyper examples/crowdfund.v.py
    ```

* Make changes to examples/crowdfund.v.py in the Text Editor. The changes will also be reflected in the Docker Container.

* Terminal #1 - Repeat the previous command to try and re-compile the Vyper contract

## Chapter 2 - Docker Containers and Images (Show/Delete) <a id="chapter-2"></a>

* List all Docker containers 
    ```bash
    docker ps -a
    ```

* Stop all running containers. 
    ```bash
    docker stop $(docker ps -aq)
    ```

* Remove a specific Docker container
    ```bash
    docker rm <CONTAINER_ID>
    ```
* Remove a docker container 
    ```bash
    docker rm $(docker ps -aq)
    ```

* Remove all Docker images
    ```bash
    docker rmi $(docker images -q)
    ```

## Chapter 3 - About Vyper <a id="chapter-3"></a>

* Vyper Online Compilter (to bytecode or LLL) https://vyper.online/

* Vyper Features (vs Solidity)
    * Asserts instead of Modifiers
        * Pros
            * No arbitrary pre-conditions, no post-conditions
            * No arbitrary state changes
            * Less execution jumps for easier auditability
    * No Class Inheritance
    * No Function or Operator Overloading 
        * Pros
            * Safer since mitigates funds being stolen 
    * No Recursive Calling or Infinite-length Loops
        * Pros 
            * Avoids gas limit attacks since gas limit upper bound may be set
    * `.v.py` File Extension so Python syntax highlighting may be used
    * All Vyper syntax is valid Python 3 syntax, but not all Python 3 functionality is available in Vyper
    * Reference
        * http://viper.readthedocs.io/en/latest/


* Vyper Syntax where Files `.v.py` are a Smart Contract 
    * Class-like with:
        * State Variable
            * Usage: Permanently stored in contract Storage
            * Example
                ```python
                storedData: int128
                ```
        * [Types, Visibility, Getters](http://viper.readthedocs.io/en/latest/types.html#types)
            * TODO
        * Functions
            * Usage: 
                * Executable units in contract
                * Internally or Externally
                * Visibility-and-getters differ toward other contracts
                * Decorated with `@public` or `@private`
            * Example
                ```python
                @public
                @payable
                def bid(): // Function
                // ...
                ```
        * Events
            * Usage
                * Searchable by Clients and Light Clients since Events are logged in specially indexed data structures
                * Declared before global declarations and Function definitions
            * Example
                ```python
                Payment: event({amount: int128, arg2: indexed(address)})

                total_paid: int128

                @public
                def pay():
                    self.total_paid += msg.value
                    log.Payment(msg.value, msg.sender)
                ```
        * Structs
            * TODO