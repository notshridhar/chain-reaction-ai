from distutils.core import setup, Extension

MOD = "chain_engine"
setup(
    name=MOD,
    ext_modules=[
        Extension(
            MOD,
            sources=["src/cqueue.c", "src/engine.c", "mod_chainengine.c"],
            include_dirs=["src"],
        )
    ],
    description="C Chain Reaction Engine",
)
