from plone.distribution import DEFAULT_PROFILE
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

    pre_handler = GlobalObject(
        title="Pre Handler",
        description=(
            "Function called before initial site creation, used to process answers payload."
        ),
        required=False,
    )

    handler = GlobalObject(
        title="Handler",
        description=("Function called after initial site creation."),
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

    profile_id = zope.schema.TextLine(
        title="Profile",
        description="Base profile to be used during site creation.",
        required=False,
        default=DEFAULT_PROFILE,
    )

    headless = zope.schema.Bool(
        title="Headless",
        description="Check if distribution is headless (no server side templates)",
        default=True,
    )


def _check_function(
    name: str, product: str, func: FunctionType | None = None
) -> FunctionType | None:
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
    pre_handler=None,
    handler=None,
    post_handler=None,
    profile_id=DEFAULT_PROFILE,
    headless=True,
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
    pre_handler = _check_function("pre_handler", product, pre_handler)
    handler = _check_function("handler", product, handler)
    post_handler = _check_function("post_handler", product, post_handler)

    distribution = Distribution(
        name,
        title,
        description,
        directory,
        product,
        pre_handler,
        handler,
        post_handler,
        profile_id,
        headless,
    )

    _context.action(
        discriminator=("register", product, name),
        callable=_distribution_registry.register,
        args=(distribution,),
    )
