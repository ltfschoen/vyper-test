# README

Travic CI Build Status: [![Build Status](https://api.travis-ci.org/ltfschoen/vyper-test.svg)](https://travis-ci.org/ltfschoen/vyper-test)

---
Vyper smart contract language
---

This is a very simplified implementation of https://github.com/ethereum/vyper by Vitalik Buterin under MIT licence. I have focused on including setup instructions for both macOS and using Docker including troubleshooting tips. I have created Vyper smart contracts and associated Unit Tests. I have summarised Vyper benefits and usage.

TODO
* [ ] - [Safe Remote Purchases] (http://viper.readthedocs.io/en/latest/vyper-by-example.html#safe-remote-purchases)
* [ ] - [Crowdfund](http://viper.readthedocs.io/en/latest/vyper-by-example.html#crowdfund)
* [ ] - [Voting](http://viper.readthedocs.io/en/latest/vyper-by-example.html#voting)
* [ ] - [Company Stock](http://viper.readthedocs.io/en/latest/vyper-by-example.html#company-stock)
* [X] - Deploy Vyper contract to Geth Private Network
* [ ] - Deploy Vyper contract to Ganache CLI / TestRPC
* [ ] - Deploy Vyper and integrate into Truffle
  * https://github.com/ethereum/vyper/issues/459
  * https://github.com/gakonst/ViperWeb3Deploy
* [ ] - Review Vyper code by others
  * https://github.com/Uniswap/contracts-vyper

# Table of Contents
  * [Chapter 0 - Setup WITHOUT Docker](#chapter-0)
  * [Chapter 1 - Setup WITH Docker](#chapter-1)
  * [Chapter 2 - Docker Containers and Images (Show/Delete)](#chapter-2)
  * [Chapter 3 - About Vyper](#chapter-3)
  * [Chapter 4 - Unit Tests](#chapter-4)

## Chapter 0 - Setup WITHOUT Docker <a id="chapter-0"></a>

* Install [PyEnv](https://github.com/pyenv/pyenv)
* Clone the Vyper repo and install Vyper
    ```bash
    pyenv global 3.6.2
    mkdir -p ~/code/clones && cd ~/code/clones
    git clone https://github.com/ethereum/vyper.git;
    cd vyper; 
    make; make test;
    ```
    * Troubleshooting
        * Refer to my fork with detailed setup instructions in README_MAC.md https://github.com/ltfschoen/vyper
* Clone this repo
    ```bash
    cd ~/code/clones;
    git clone https://github.com/ltfschoen/vyper-test;
    ```
* Install dependencies. Fix any incompatibilities
    ```bash
    pip3 install -r requirements.txt
    ```
* Compile a Vyper contract
    ```bash
    vyper contracts/auctions/simple_open_auction.v.py
    ```

* Start a Geth Node and View its Logs
    * https://github.com/ltfschoen/geth-node

* Option 1: Run Deployment Script to Deploy the Vyper Smart Contract to Truffle's built-in blockchain
    * Install Node Version Manager and switch to the latest version of Node.js (i.e. v9.8.0)
        ```
        nvm use v9.8.0
        ```

    * Install Truffle
        ```
        npm install -g truffle
        ```

    * Create new terminal tab in root of the project directory and run
        ```bash
        truffle develop --log
        ```

    * Modify scripts/main.py by changing `web3 = Web3(provider_ipc)` (used for a Geth Node) to `web3 = Web3(provider_http)` (used for Truffle) instead 
    
    * Run the script
        ```bash
        python3 scripts/main.py
        ```
    
    * Output after deploying the contract shown in the Truffle logs
        ```bash
        $ truffle develop --log
        Truffle Develop started at http://localhost:9545/

        Accounts:
        (0) ...
        (1) ...

        Private Keys:
        (0) ...
        (1) ...

        Mnemonic: ...

        develop:testrpc personal_listAccounts +0ms
        develop:testrpc eth_accounts +8ms
        develop:testrpc eth_accounts +7ms
        develop:testrpc personal_listAccounts +6ms
        develop:testrpc eth_gasPrice +5ms
        develop:testrpc eth_estimateGas +12ms
        develop:testrpc net_version +48ms
        develop:testrpc net_version +6ms
        develop:testrpc eth_sendTransaction +7ms
        develop:testrpc  +52ms
        develop:testrpc   Transaction: 0x3d29ae2796e9b94f59d7830062f081fff4f9811c0869e659e2faa4efe7370ccf +0ms
        develop:testrpc   Contract created: 0x8cdaf0cd259887258bc13a92c0a6da92698644c0 +0ms
        develop:testrpc   Gas usage: 273163 +0ms
        develop:testrpc   Block Number: 1 +0ms
        develop:testrpc   Block Time: Fri Apr 20 2018 13:01:53 GMT+1000 (AEST) +0ms
        develop:testrpc  +0ms
        develop:testrpc eth_getTransactionReceipt +5ms
        develop:testrpc eth_getTransactionReceipt +11ms
        develop:testrpc eth_getBlockByNumber +29ms
        develop:testrpc eth_call +13ms
        develop:testrpc eth_getBlockByNumber +30ms
        develop:testrpc eth_call +13ms
        ```

* Option 2: Run Deployment Script to Deploy the Vyper Smart Contract to Geth Private Network
    * Run the script
        ```bash
        python3 scripts/main.py
        ```

    * Example Terminal Output
        ```
        $ python3 scripts/main.py

        OS Platform: darwin
        Web3 provider: <web3.main.Web3 object at 0x10ebb6160>
        Initializing chain from provided state
        ABI: %s [{'name': '__init__', 'outputs': [], 'inputs': [{'type': 'address', 'name': '_beneficiary'}, {'type': 'int128', 'name': '_bidding_time'}], 'constant': False, 'payable': False, 'type': 'constructor'}, {'name': 'bid', 'outputs': [], 'inputs': [], 'constant': False, 'payable': True, 'type': 'function', 'gas': 76241}, {'name': 'end_auction', 'outputs': [], 'inputs': [], 'constant': False, 'payable': False, 'type': 'function', 'gas': 56101}, {'name': 'beneficiary', 'outputs': [{'type': 'address', 'name': 'out'}], 'inputs': [], 'constant': True, 'payable': False, 'type': 'function', 'gas': 543}, {'name': 'auction_start', 'outputs': [{'type': 'int128', 'name': 'out'}], 'inputs': [], 'constant': True, 'payable': False, 'type': 'function', 'gas': 573}, {'name': 'auction_end', 'outputs': [{'type': 'int128', 'name': 'out'}], 'inputs': [], 'constant': True, 'payable': False, 'type': 'function', 'gas': 603}, {'name': 'highest_bidder', 'outputs': [{'type': 'address', 'name': 'out'}], 'inputs': [], 'constant': True, 'payable': False, 'type': 'function', 'gas': 633}, {'name': 'highest_bid', 'outputs': [{'type': 'int128', 'name': 'out'}], 'inputs': [], 'constant': True, 'payable': False, 'type': 'function', 'gas': 663}, {'name': 'ended', 'outputs': [{'type': 'bool', 'name': 'out'}], 'inputs': [], 'constant': True, 'payable': False, 'type': 'function', 'gas': 693}]
        Address: %s b'\xd6\xf0\x84\xee\x15\xe3\x8cO~\t\x1f\x8d\xd0\xfeo\xe4\xa0\xe2\x03\xef'
        Contract Instance: %s <ethereum.tools.tester.ABIContract object at 0x1105aa5c0>
        Contract Instance with Web3: %s <ethereum.tools.tester.ABIContract object at 0x1105aa5c0>
        Accounts: %s 0x487F2778Ec7D0747d6E26AF80148Ec471a08b339
        Default Account: %s 0x487F2778Ec7D0747d6E26AF80148Ec471a08b339
        Unlocked Default Account: %s True
        Deployed Contract Tx Hash: %d b'\tk\xfb.k\xe5\x94\x1f\x152\xb3\x14d\x1dN6T\xf5\x97v(d\xa4\xd6DW\x93\xf2r\xe1\xe7\xfc'
        Mined Transaction Receipt: %s AttributeDict({'blockHash': HexBytes('0x74c26c73f9021c8aae1a6df1e283c13a2045f3c3a2b9aab1689307b1bc40c12b'), 'blockNumber': 3755, 'contractAddress': '0xc071ef1FE2f3d9b8D59C4106391b7fe417593cfa', 'cumulativeGasUsed': 273163, 'from': '0x487f2778ec7d0747d6e26af80148ec471a08b339', 'gasUsed': 273163, 'logs': [], 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'), 'root': '0xb5b377e641e9850d2f10d631251b5431a4f34a7745aafddca52b7654fb7bb60f', 'to': None, 'transactionHash': HexBytes('0x096bfb2e6be5941f1532b314641d4e3654f597762864a4d6445793f272e1e7fc'), 'transactionIndex': 0})
        Transaction Receipt: %s AttributeDict({'blockHash': HexBytes('0x74c26c73f9021c8aae1a6df1e283c13a2045f3c3a2b9aab1689307b1bc40c12b'), 'blockNumber': 3755, 'contractAddress': '0xc071ef1FE2f3d9b8D59C4106391b7fe417593cfa', 'cumulativeGasUsed': 273163, 'from': '0x487f2778ec7d0747d6e26af80148ec471a08b339', 'gasUsed': 273163, 'logs': [], 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'), 'root': '0xb5b377e641e9850d2f10d631251b5431a4f34a7745aafddca52b7654fb7bb60f', 'to': None, 'transactionHash': HexBytes('0x096bfb2e6be5941f1532b314641d4e3654f597762864a4d6445793f272e1e7fc'), 'transactionIndex': 0})
        Contract Instance: %s <web3.utils.datatypes.Contract object at 0x10f151a20>
        Called Getter method of beneficiary from Deployed Contract Instance: %s 0x487F2778Ec7D0747d6E26AF80148Ec471a08b339
        Called Getter method of auction_end from Deployed Contract Instance: %s 1524192662
        ```

* Run Unit tests
    * Troubleshooting
        * Recursively deleting the pycache folder created in both the tests/ subdirectory and the tests/auctions/ subdirectory, and the .pytest_cache folder in the project root directory, and then running `find . -name '*.pyc' -delete` just to be sure all the cache files had been removed from all subdirectories. Add `export PYTHONDONTWRITEBYTECODE=1` into ~/.bash_profile so Python cache files would no longer be generated.

    ```bash
    python3 -m pytest -v
    ```

* Troubleshooting
    * Refer to fork with [Troubleshooting steps](https://github.com/ltfschoen/vyper/blob/master/README_MAC.md)

* INCOMPLETE - Deploy Vyper contract to Ganache CLI / TestRPC
    * Create separate terminal tab and start virtual EVM and start Ganache CLI 

```bash
ganache-cli \
    --account="0x0000000000000000000000000000000000000000000000000000000000000001, 2471238800000000000" \
    --account="0x0000000000000000000000000000000000000000000000000000000000000002, 4471238800000000000" \
    --unlock "0x0000000000000000000000000000000000000000000000000000000000000001" \
    --unlock "0x0000000000000000000000000000000000000000000000000000000000000002" \
    --blocktime 0 \
    --deterministic true \
    --port 8545 \
    --hostname localhost \
    --seed 'blah' \
    --debug true \
    --mem true \
    --mnemonic 'something' \
    --db './db/chain_database' \
    --verbose \
    --networkId=3 \
    --gasLimit=7984452 \
    --gasPrice=20000000000;
```

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

* Follow steps in Chapter 0 to clone my repo and make the files accessible in the container

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
        * Contract State Variables
            * Usage: Permanently stored in contract Storage
            * Example
                ```python
                storedData: int128
                ```
            * Access 
                ```python
                self.storedData
                ```
        * Validations 
            * `assert`
                * Failure to pass results in the method to throw an error and the transaction is reverted
        * Objects
            * `block` - Object available within Vyper contract providing info about block at time of calling
            * `msg`
                * Object built-in that provides information about the message caller whenever a method in the contract is called
                * `msg.sender` to access public address of the caller of a method
                    * WARNING: If calling contract from outside it works correctly, but for subsequent internal function calls it will reference the contract itself instead of the sender of the transaction
                * `msg.value` to access amount of ether a user sends
        * [Types, Visibility, Getters](http://viper.readthedocs.io/en/latest/types.html#types)
            * `address`
            * `bool`
            * `timedelta` seconds
            * `timestamp` time
                * `block.timestamp` - Current Time
            * `wei_value` lowest denominator
            
        * Functions
            * Usage: 
                * Executable units in contract
                * Internally or Externally
                * Visibility-and-getters differ toward other contracts
                * Decorated with `@public` or `@private`
                    * Default is `@private` which is only accessible to methods in same contract
                    * `@public` callable by external contracts
                    * `@public` function creates a **Getter** function accessible with call `self.get_beneficiary(some_address)`

                * **Security** Structure functions that interact with other contracts (i.e. they call functions or send Ether) into three phases:
                    * 1. Check Conditions
                    * 2. Performing Actions (potentially changing conditions)
                    * 3. Interacting with other Contracts
                    * WARNING: If these phases are mixed up, the other contract could call back into the current contract and modify the state or cause effects (Ether payout) to be performed multiple times. If functions called internally include interaction with external contracts, they also have to be considered interaction with external contracts.
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

## Chapter 4 - Unit Tests <a id="chapter-4"></a>

```bash
pip3 install ethereum==2.3.1 pytest pytest-cov pytest-runner
python setup.py test
pytest -v --full-trace --setup-show
```