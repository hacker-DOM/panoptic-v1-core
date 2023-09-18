from .b_helpers import *


class Hooks(Helpers):
    @override
    def pre_sequence(s):
        # s.tokens = []

        s._deploy()
        for i in range(NUM_TOKENS):
            decimals = random_int(
                # TOKEN_MIN_DECIMALS,
                18,
                # TOKEN_MAX_DECIMALS,
                18,
            )
            total_supply = NUM_USERS * NUM_TOKENS_EACH_USER * 10**decimals
            # token: ERC20 = ERC20.deploy(_totalSupply=total_supply, from_=s.paccs[0])
            # token.label = num_to_letter(i).upper()
            # print(f'Created token {token.label} with {decimals} decimals and {total_supply} total supply')
            # s.tokens.append(token)
            #
            # for j in range(NUM_USERS):
            #     _ = token.transfer(s.users[j], NUM_TOKENS_EACH_USER * 10**decimals, from_=s.paccs[0])

    @override
    def pre_flow(s, flow: Callable[..., None]):
        with open(csv, "a") as f:
            _ = f.write(f"{s.sequence_num},{s.flow_num},{flow.__name__}\n")

    @override
    def post_sequence(s):
        ...
        # s.tokens = None  # pyright: ignore [reportGeneralTypeIssues]
        # s.factory = None  # pyright: ignore [reportGeneralTypeIssues]
        # s.pairs = None  # pyright: ignore [reportGeneralTypeIssues]
