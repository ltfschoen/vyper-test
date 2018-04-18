# OPEN AUCTION SMART CONTRACT

# CONTRACT STATE VARIABLES - GLOBAL

# Declarations
beneficiary: public(address)

auction_start: public(timestamp)
auction_end: public(timestamp)

highest_bidder: public(address)
highest_bid: public(wei_value)

ended: public(bool)

# CONTRACT STATE VARIABLES - PRIVATE

# CONSTRUCTOR - PUBLIC

@public
def __init__(_beneficiary: address, _bidding_time: timedelta):
    # :param _beneficiary: Beneficiary address receives money from
    #   highest bid when auction period ends
    # :type _beneficiary: address
    #
    # :param _bidding_time: Participants submit bids during limited time period
    # :type _beneficiary: timedelta
    #
    # :output N/A: N/A

    # Assignment
    self.beneficiary = _beneficiary
    self.auction_start = block.timestamp
    self.auction_end = self.auction_start + _bidding_time

# FUNCTIONS - PUBLIC

# Transaction to bid on the auction with value sent
# in addition to gas fees. Refund the value if auction is not won
@public
@payable
def bid():
    # Check if bid occurred before bid period finishes
    assert block.timestamp < self.auction_end
    # Check if new bid is sufficient by being greater than highest bid
    assert msg.value > self.highest_bid
    # Check if the previously stored highest bid is not equal to zero
    if not self.highest_bid == 0:
        # Sends money back to the previous highest bidder
        send(self.highest_bidder, self.highest_bid)
    # Set valid new highest bid
    self.highest_bidder = msg.sender
    self.highest_bid = msg.value

# End the auction and send the highest bid amount to the beneficiary.
@public
def end_auction():
    # STRUCTURED FUNCTION PHASES

    # 1. Conditions
    #   - Check if auction end time has been reached
    assert block.timestamp >= self.auction_end
    #   - Check if auction already ended. Prevent malicious calls
    assert not self.ended

    # 2. Effects
    self.ended = True

    # 3. Interaction
    send(self.beneficiary, self.highest_bid)