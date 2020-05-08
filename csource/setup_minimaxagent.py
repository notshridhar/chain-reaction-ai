from distutils.core import setup, Extension

MOD = "minimax_agent"
setup(
    name=MOD,
    ext_modules=[
        Extension(
            MOD,
            sources=["src/cqueue.c", "src/engine.c", "src/minimax.c", "mod_minimaxagent.c"],
            include_dirs=["src"],
        )
    ],
    description="Chain Reaction Minimax Agent",
)
