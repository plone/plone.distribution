from plone.distribution.core import Distribution
from plone.distribution.registry import _distribution_registry
from types import FunctionType
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import MessageID
from zope.configuration.fields import Path
from zope.configuration.name import resolve
from zope.interface import Interface

import pathlib
import zope.schema


def _resolveDottedName(dotted):
    __traceback_info__ = dotted

    try:
        return resolve(dotted)
    except ModuleNotFoundError:
        return


class IRegisterDistributionDirective(Interface):
    """Register distributions with the global registry."""

    name = zope.schema.TextLine(
        title="Name", description="Distribution short name.", required=True
    )

    title = MessageID(
        title="Title", description="Distribution Title.", default="", required=True
    )

    description = MessageID(
        title="Description",
        description="Optional description for the distribution.",
        default="",
        required=False,
    )

    handler = GlobalObject(
        title="Handler",
        description=("Function called after initial site creation. "),
        required=False,
    )

    post_handler = GlobalObject(
        title="Post Handler",
        description=(
            "Function called after site is created and handler processed profiles."
        ),
        required=False,
    )

    directory = Path(
        title="Distribution Directory",
        description="If not specified 'distributions/<name>' is used.",
        required=False,
    )


def _check_function(name: str, product: str, func: FunctionType = None) -> FunctionType:
    if func and not isinstance(func, FunctionType):
        # Probably a string, so resolve dotted name
        func = f"{product}{func}" if func.startswith(".") else func
        func = _resolveDottedName(func)
        if not func:
            raise ValueError(f"{name} points to non existing function: {func}")
    return func


def register_distribution(
    _context,
    name,
    title,
    description="",
    directory=None,
    handler=None,
    post_handler=None,
):
    """Add a new distribution to the registry."""
    product = _context.package.__name__
    package_path = pathlib.Path(_context.package.__file__).parent.resolve()
    if directory is None:
        directory = f"distributions/{name}"
    directory = package_path / directory

    if description is None:
        description = ""

    # Validate handler and post_handler functions
    handler = _check_function("handler", product, handler)
    post_handler = _check_function("post_handler", product, post_handler)

    distribution = Distribution(
        name, title, description, directory, handler, post_handler
    )

    _context.action(
        discriminator=("register", product, name),
        callable=_distribution_registry.register,
        args=(distribution,),
    )
