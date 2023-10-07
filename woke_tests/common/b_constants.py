from .a_imports import *

"""
This file contains all the constants used in the project.
"""

csv = plib.Path("gitignore/flows_and_txns.csv")
# this overwrites the file
_ = csv.write_text(
    "sequence_number,flow_number,flow_name,block_number,from,to,return_value,events,console_logs\n"
)

# when we `from woke.testing import *`, we actually import a generic type T
# this should probably be fixed, but until then, just use different name here
TE = TypeVar("TE")
"""this represents a generic type of something we'll read from the env"""


def get_env(
    var_name: str,
    default_value: TE,
) -> TE:
    """get an environment variable and type cast it, or return a default value if it's not set"""
    value = os.environ.get(var_name)

    if value is None:
        return default_value

    try:
        return type(default_value)(value)
    except ValueError:
        console.print(f"Could not cast {var_name}={value} to {type(default_value)}")
        return default_value


SEQUENCES_COUNT = get_env("WOKE_TESTS_SEQUENCES_COUNT", 1)
FLOWS_COUNT = get_env("WOKE_TESTS_FLOWS_COUNT", 100)

NUM_PACCS = get_env("WOKE_TESTS_NUM_PRIV_ACC", 1)
NUM_USERS = get_env("WOKE_TESTS_NUM_USERS", 3)

NUM_TOKENS = get_env("WOKE_TESTS_NUM_TOKENS", 4)
NUM_TOKENS_EACH_USER = get_env("WOKE_TESTS_NUM_TOKENS", 100)

# region tolerances
DUINT_ABS_TOL = get_env("WOKE_TESTS_DUINT_ABS_TOL", 10_000)
# endregion

# region ignores
# endregion

# region weights
# endregion

crypto_names = [
    # it's visually easier to read if the names are the same length
    "Alice",
    "Brant",
    "Chady",
    "David",
    "Evena",
    "Frank",
    "Georg",
    "Helen",
    "Irene",
    "Johny",
    "Karen",
    "Laura",
    "Mikey",
    "Nancy",
    "Olivi",
    "Paula",
    "Queen",
    "Rachy",
    "Steve",
    "Tommy",
    "Unity",
    "Veron",
    "Wendy",
    "Xavie",
    "Yvonn",
    "Zebra",
]

WETH = Address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
V3FACTORY_ADDRESS = Address("0x1F98431c8aD98523631AE4a59f267346ea31F984")
INITIAL_MOCK_TOKENS = 2**120 - 1
