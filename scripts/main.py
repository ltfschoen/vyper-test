from vyper import compiler
from ethereum.tools import tester
from ethereum import utils as ethereum_utils

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
