# Tool interface for tool implementations
try:
    from functools import singledispatch
except:
    from singledispatch import singledispatch


def missing_impl(tool, f):
    raise Exception(
        'incorrect tool implementation',
        'Tool implementation %s is missing a "%s" implementation' % (
            type(tool),
            f,
        )
    )


@singledispatch
def name(tool):
    missing_impl(tool, name.__name__)


@singledispatch
def is_using_tool(tool, path):
    """Predicate to test if the path contains a project using the tool."""
    missing_impl(tool, is_using_tool.__name__)


@singledispatch
def dependencies(tool, path):
    """Return a list of dependency prefixes for the project at path."""
    missing_impl(tool, dependencies.__name__)


@singledispatch
def execute_build_phase(tool, path, phase_name):
    """Execute a build phase."""
    missing_impl(tool, dependencies.__name__)
