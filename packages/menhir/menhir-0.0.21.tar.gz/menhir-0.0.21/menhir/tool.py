"""Tool interface for tool implementations.

A tool is implemented as an opaque class.  Implementations of the tool
multi-methods are provided for each tool.

"""
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
    """Provide the tool's name."""
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
def execute_build_phase(tool, path, info, args, **kwargs):
    """Execute a build phase."""
    missing_impl(tool, execute_build_phase.__name__)


@singledispatch
def add_arg_parser(tool, parsers):
    """Add an arg parser for the tool to parsers."""
    missing_impl(tool, add_arg_parser.__name__)
