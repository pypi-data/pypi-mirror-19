import asyncio
import sys
from concurrent.futures import ThreadPoolExecutor
from logging import basicConfig, getLogger, INFO
from logging.config import dictConfig
from typing import Union, Dict, Any

from typeguard import check_argument_types

from asphalt.core.component import Component, component_types
from asphalt.core.context import Context
from asphalt.core.util import PluginContainer, qualified_name

__all__ = ('run_application',)

policies = PluginContainer('asphalt.core.event_loop_policies')


def uvloop_policy():
    import uvloop
    return uvloop.EventLoopPolicy()


def gevent_policy():
    import aiogevent
    return aiogevent.EventLoopPolicy()


def run_application(component: Union[Component, Dict[str, Any]], *, event_loop_policy: str = None,
                    max_threads: int = None, logging: Union[Dict[str, Any], int, None] = INFO):
    """
    Configure logging and start the given root component in the default asyncio event loop.

    Assuming the root component was started successfully, the event loop will continue running
    until the process is terminated.

    Initializes the logging system first based on the value of ``logging``:
      * If the value is a dictionary, it is passed to :func:`logging.config.dictConfig` as
        argument.
      * If the value is an integer, it is passed to :func:`logging.basicConfig` as the logging
        level.
      * If the value is ``None``, logging setup is skipped entirely.

    By default, the logging system is initialized using :func:`~logging.basicConfig` using the
    ``INFO`` logging level.

    The default executor in the event loop is replaced with a new
    :class:`~concurrent.futures.ThreadPoolExecutor` where the maximum number of threads is set to
    the value of ``max_threads`` or, if omitted, the default value of
    :class:`~concurrent.futures.ThreadPoolExecutor`.

    :param component: the root component (either a component instance or a configuration dictionary
        where the special ``type`` key is either a component class or a ``module:varname``
        reference to one)
    :param event_loop_policy: entry point name (from the ``asphalt.core.event_loop_policies``
        namespace) of an alternate event loop policy (or a module:varname reference to one)
    :param max_threads: the maximum number of worker threads in the default thread pool executor
        (the default value depends on the event loop implementation)
    :param logging: a logging configuration dictionary, :ref:`logging level <python:levels>` or
        ``None``

    """
    assert check_argument_types()

    # Configure the logging system
    if isinstance(logging, dict):
        dictConfig(logging)
    elif isinstance(logging, int):
        basicConfig(level=logging)

    # Inform the user whether -O or PYTHONOPTIMIZE was set when Python was launched
    logger = getLogger(__name__)
    logger.info('Running in %s mode', 'development' if __debug__ else 'production')

    # Switch to an alternate event loop policy if one was provided
    if event_loop_policy:
        create_policy = policies.resolve(event_loop_policy)
        policy = create_policy()
        asyncio.set_event_loop_policy(policy)
        logger.info('Switched event loop policy to %s', qualified_name(policy))

    # Assign a new default executor with the given max worker thread limit if one was provided
    event_loop = asyncio.get_event_loop()
    if max_threads is not None:
        event_loop.set_default_executor(ThreadPoolExecutor(max_threads))
        logger.info('Installed a new thread pool executor with max_workers=%d', max_threads)

    # Instantiate the root component if a dict was given
    if isinstance(component, dict):
        component = component_types.create_object(**component)

    logger.info('Starting application')
    context = Context()
    exception = None
    try:
        # Start the root component
        try:
            event_loop.run_until_complete(component.start(context))
        except Exception as e:
            exception = e
            logger.exception('Error during application startup')
            sys.exit(1)
        else:
            # Enable the component tree to be garbage collected
            del component

            # Finally, run the event loop until the process is terminated or Ctrl+C is pressed
            logger.info('Application started')
            try:
                event_loop.run_forever()
            except KeyboardInterrupt:
                pass
    finally:
        # Cancel all running tasks
        for task in asyncio.Task.all_tasks(event_loop):
            task.cancel()

        # Run all the finish callbacks
        future = context.finished.dispatch(exception, return_future=True)
        event_loop.run_until_complete(future)

        event_loop.close()
        logger.info('Application stopped')
