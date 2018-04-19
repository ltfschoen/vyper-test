from vyper import compiler
from ethereum.tools import tester
from ethereum import utils as ethereum_utils
# http://web3py.readthedocs.io/en/stable
import web3
from web3 import Web3, HTTPProvider, EthereumTesterProvider, IPCProvider
from sys import platform

from web3.contract import Contract

GETH_IPC_PATH = '/Users/Ls/code/blockchain/geth-node/chaindata/geth.ipc'
GENERIC_PASSWORD_TO_ENCRYPT = 'test123456'

provider_ipc = IPCProvider(GETH_IPC_PATH);
# provider_ethereum_test = EthereumTesterProvider()
# HTTP Provider Reference: http://web3py.readthedocs.io/en/stable/providers.html#httpprovider
provider_http = Web3.HTTPProvider("http://127.0.0.1:8545")
# web3.py instance
web3 = Web3(provider_ipc)
print('OS Platform: {}'.format(platform))
print('Web3 provider: {}'.format(web3))

# print("Block Number: %s", web3.eth.blockNumber)

def get_encoded_contract_constructor_arguments(constructor_args=None):
    if constructor_args:
        return contract_translator.encode_constructor_arguments(constructor_args['args'])
    else:
        return b''

def get_logs(last_receipt, contract, event_name=None):
    # Get all log ids from the contract events
    contract_log_ids = contract.translator.event_data.keys()
    # Filter and return all logs originating from the contract 
    # or only those matching the event_name (if specified)
    logs = [log for log in last_receipt.logs
            if log.topics[0] in contract_log_ids and
            log.address == contract.address and
            (not event_name or
                contract.translator.event_data[log.topics[0]]['name'] == event_name)]
    assert len(logs) > 0, "No logs in the last receipt of the contract"
    # Return all events decoded from the last receipt of the contract
    return [contract.translator.decode_event(log.topics, log.data) for log in logs]

def get_last_log_from_contract_receipts(tester, contract, event_name=None):
    # Get only the receipts for the last block from the chain (aka tester.s)
    last_receipt = tester.s.head_state.receipts[-1]
    # Get last log event with correct name and return the decoded event
    print(get_logs(last_receipt, contract, event_name=event_name))
    return get_logs(last_receipt, contract, event_name=event_name)[-1]

# Set the Vyper compiler to run when the Vyper language is requested
tester.languages['vyper'] = compiler.Compiler()
# Set the new "chain" (aka tester.s)
tester.s = tester.Chain()
tester.s.head_state.gas_limit = 10**9
initial_chain_state = tester.s.snapshot()
# Load contract source code
source_code = open('contracts/auctions/simple_open_auction.v.py').read()
# Compile contract code interface (aka tester.c)
FIVE_DAYS = 432000
tester.c = tester.s.contract(source_code, language='vyper', args=[tester.accounts[0], FIVE_DAYS])
# Generate ABI from contract source code
abi = tester.languages['vyper'].mk_full_signature(source_code)
# print("ABI: %s", abi)
# Generate Contract Translator from ABI
contract_translator = tester.ContractTranslator(abi)
# Generate Bytecode from contract source code
contract_constructor_args = []
byte_code = tester.languages['vyper'].compile(source_code) + \
    get_encoded_contract_constructor_arguments(contract_constructor_args)
# print("Bytecode: %s", byte_code)
address = tester.s.tx(to=b'', data=byte_code)
print("Address: %s", address)
# Instantiate contract from its ABI and Bytecode
contract_instance = tester.ABIContract(tester.s, abi, address)
print("Contract Instance: %s", contract_instance)
# Execute method on the tester chain to check the beneficiary is correct
assert ethereum_utils.remove_0x_head(tester.c.beneficiary()) == tester.accounts[0].hex()
# Execute method on the tester chain to check bidding time is 5 days
assert tester.c.auction_end() == tester.s.head_state.timestamp + FIVE_DAYS
# Revert chain state on failed transaction
tester.s.revert(initial_chain_state)

# Instantiate and deploy contract
contract_instance_web3 = web3.eth.contract(abi=abi, bytecode=byte_code)
print("Contract Instance with Web3: %s", contract_instance)

# # Get transaction hash from deployed contract
# deploy_txn_hash = contract_instance_web3.deploy(transaction={'from': web3.eth.accounts[0], 'gas': 410000})
# print("Deployed Contract Tx Hash: %s", deploy_txn_hash)

# # Get tx receipt to get contract address
# tx_receipt = web3.eth.getTransactionReceipt(deploy_txn_hash)
# contract_address = tx_receipt['contractAddress']
# print("Contract Address with Web3: %s", contract_address)

# Alternative attempt using Web3.py 4.1.0 and Geth 
# https://github.com/ltfschoen/geth-node
# http://web3py.readthedocs.io/en/stable/contracts.html?highlight=deploy
deploy_txn_hash = contract_instance_web3.constructor(web3.eth.coinbase, 12345).transact()
# Returns ValueError: {'code': -32000, 'message': 'unknown account'}
print("Deployed Contract Tx Hash: %s", deploy_txn_hash)
txn_receipt = web3.eth.getTransactionReceipt(deploy_txn_hash)
print("Transaction Receipt: %s", txn_receipt['contractAddress'])

