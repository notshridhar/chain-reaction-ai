import os
import shutil
import setuptools
from distutils.core import setup, Extension


MODULE_NAME = "chain-reaction"

# copy in scripts
if not os.path.exists('scripts'):
    os.makedirs('scripts')
shutil.copyfile('chain-reaction.py', 'scripts/chain-reaction')


# Python modules
def py_packages_list():
    return [
        "chain_reaction",
        "chain_reaction.backends",
        "chain_reaction.graphics",
        "chain_reaction.wrappers",
        "chain_reaction.backends.c_ext",
        "chain_reaction.backends.python",
    ]


# C extensions
def c_extension_list():
    MINIMAX_EXTN = Extension(
        "chain_reaction.backends.c_ext.minimax_agent",
        sources=[
            "csource/src/cqueue.c",
            "csource/src/engine.c",
            "csource/src/minimax.c",
            "csource/mod_minimaxagent.c",
        ],
        include_dirs=["csource/src"],
    )

    return [MINIMAX_EXTN]


# scripts
def scripts_list():
    return ["scripts/chain-reaction"]

setup(
    name=MODULE_NAME,
    version="0.1.0",
    author="Shridhar Hegde",
    scripts=scripts_list(),
    packages=py_packages_list(),
    ext_modules=c_extension_list(),
    description="Chain Reaction Game",
)

# delete scripts directory
os.remove("scripts/chain-reaction")
os.rmdir("scripts")