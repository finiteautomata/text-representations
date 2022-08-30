import os
import glob
from .utils import preprocess_text

base_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "..",
    )
)

curated_path = os.path.join(base_path, "data", "contracts", "curated")

downloaded_contracts = os.path.join(
    base_path, "data", "contracts",
    "downloaded", "txt",
)

curated_contracts = {
    "ADMA": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "ADMA Biomanufacturing - Services Agreement.txt"),
        **kwargs
    ),
    "Biogen Credit Agreement": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "Biogen Credit Agreement - 2020.txt"),
         **kwargs
    ),

    "Bright Horizons - Credit Agreement": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "Bright Horizons - Credit Agreement.txt"),
         **kwargs
    ),
    "Datawatch": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "DataWatch Corp.txt"),
         **kwargs
    ),

    # Strange contract, ask Will
    # "DnB": lambda **kwargs: yield_lines(
    #     os.path.join(curated_path, "DnB - Services Agreement.txt"),
    #     chunk_flextronics, **kwargs
    # ),

    "Flextronics": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "Flextronics - Data Processing Service Agreement.txt"),
         **kwargs
    ),

    # Awkward structure
    # "General Atlantic": lambda **kwargs: yield_lines(
    #     os.path.join(curated_path, "General Atlantic - Merger Agreement.txt"),
    #     chunk_general_atlantic, **kwargs
    # ),

    "GA - Purchase Agreement": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "GA - Purchase Agreement.txt"),
         **kwargs
    ),

    # Quite ok, it has a veeeeeeery long exhibit clause at the end of it
    "IMA between Black Rock and the Fed": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "IMA between Black Rock and the Fed.txt"),
         **kwargs
    ),

    "Jagged Peak Energy - Assignment Agreement": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "Jagged Peak Energy - Assignment Agreement.txt"),
         **kwargs
    ),

    "Oasis Petroleum - Credit Agreement": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "Oasis Petroleum - Credit Agreement.txt"),
         **kwargs
    ),

    "Quality Technology Services - Service Agreement": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "Quality Technology Services - Service Agreement.txt"),
         **kwargs
    ),

    "RenovoRx - Service Agreement": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "RenovoRx - Service Agreement.txt"),
         **kwargs
    ),

    "Sample Asset Purchase Agreement": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "Sample Asset Purchase Agreement.txt"),
         **kwargs
    ),


    "Sample DIP Loan Agreement": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "Sample DIP Loan Agreement.txt"),
         **kwargs
    ),

    "Veritone - Merger Agreement": lambda **kwargs: yield_lines(
        os.path.join(curated_path, "Veritone - Merger Agreement.txt"),
         **kwargs
    )
}


contracts = curated_contracts.copy()

contract_paths = glob.glob(os.path.join(downloaded_contracts, "*.txt"))

def create_contract_generator(path):
    # This is to avoid lambda in loop issue :-)
    return lambda **kwargs: yield_lines(path, **kwargs)

for path in contract_paths:
    basename = os.path.basename(path)
    name, ext = os.path.splitext(basename)

    contracts[name] = create_contract_generator(path)


def yield_lines(path, **kwargs):
    """
    Helper function for pre-chunked contracts
    """
    with open(path, "r") as f:
        for paragraph in preprocess_text(f, **kwargs):
            yield paragraph
