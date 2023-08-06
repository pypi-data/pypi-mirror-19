# -*- coding: utf-8 -*-
# *********************************************************************
# lewis - a library for creating hardware device simulators
# Copyright (C) 2016-2017 European Spallation Source ERIC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *********************************************************************

from argparse import ArgumentParser
from datetime import datetime
import inspect

from . import Adapter, ForwardProperty
from six import iteritems

from lewis.core.logging import has_log
from lewis.core.utils import seconds_since, FromOptionalDependency, format_doc_text
from lewis.core.exceptions import LewisException, LimitViolationException

# pcaspy might not be available. To make EPICS-based adapters show up
# in the listed adapters anyway dummy types are created in this case
# and the failure is postponed to runtime, where a more appropriate
# LewisException can be raised.
missing_pcaspy_exception = LewisException(
    'In order to use EPICS-interfaces, pcaspy must be installed:\n'
    '\tpip install pcaspy\n'
    'A fully working installation of EPICS-base is required for this package. '
    'Please refer to the documentation for advice.')

Driver, SimpleServer = FromOptionalDependency(
    'pcaspy', missing_pcaspy_exception).do_import('Driver', 'SimpleServer')


class PV(object):
    """
    The PV-class is used to declare the EPICS-interface exposed by a sub-class of
    EpicsAdapter. The ``target_property`` argument specifies which property of the adapter
    the PV maps to. To make development easier it can also be a part of the exposed
    device. If the property exists on both the Adapter-subclass and the device, the former
    has precedence. This is useful for overriding behavior for protocol specific "quirks".

    If the PV should be read only, this needs to be specified via
    the corresponding parameter. The information about the poll interval is used
    py EpicsAdapter to update the PV in regular intervals. All other named arguments
    are forwarded to the pcaspy server's `pvdb`, so it's possible to pass on
    limits, types, enum-values and so on.

    In case those arguments change at runtime, it's possible to provide ``meta_data_property``,
    which should contain the name of a property that returns a dict containing these values.
    For example if limits change:

    .. sourcecode:: Python

        class Interface(EpicsAdapter):
            pvs = {
                'example': PV('example', meta_data_property='example_meta')
            }

            @property
            def example_meta(self):
                return {
                    'lolim': self._device._example_low_limit,
                    'hilim': self._device._example_high_limit,
                }

    The PV infos are then updated together with the value, determined by ``poll_interval``.

    :param target_property: Property of the adapter to expose.
    :param poll_interval: Update interval of the PV.
    :param read_only: Should be True if the PV is read only.
    :param meta_data_property: Property which returns a dict containing PV metadata.
    :param doc: Description of the PV. If not supplied, docstring of mapped property is used.
    :param kwargs: Arguments forwarded into pcaspy pvdb-dict.
    """

    def __init__(self, target_property, poll_interval=1.0, read_only=False,
                 meta_data_property=None, doc=None, **kwargs):
        self.property = target_property
        self.read_only = read_only
        self.poll_interval = poll_interval
        self.meta_data_property = meta_data_property
        self.doc = doc
        self.config = kwargs


@has_log
class PropertyExposingDriver(Driver):
    def __init__(self, target, pv_dict):
        super(PropertyExposingDriver, self).__init__()

        self._target = target
        self._set_logging_context(target)

        self._pv_dict = pv_dict
        self._timers = {k: 0.0 for k in self._pv_dict.keys()}
        self._last_update_call = None

    def write(self, pv, value):
        self.log.debug('PV put request: %s=%s', pv, value)

        pv_object = self._pv_dict.get(pv)

        if not pv_object or pv_object.read_only:
            return False

        try:
            setattr(self._target, pv_object.property, value)
            self.setParam(pv, getattr(self._target, pv_object.property))
            return True
        except LimitViolationException:
            return False

    def process_pv_updates(self, force=False):
        dt = seconds_since(self._last_update_call or datetime.now())
        # Updates bound parameters as needed

        updates = []

        for pv, pv_object in iteritems(self._pv_dict):
            self._timers[pv] += dt
            if self._timers[pv] >= pv_object.poll_interval or force:
                try:
                    new_value = getattr(self._target, pv_object.property)
                    self.setParam(pv, new_value)

                    if pv_object.meta_data_property is not None:
                        self.setParamInfo(pv, getattr(self._target, pv_object.meta_data_property))

                    self._timers[pv] = 0.0
                    updates.append((pv, new_value))
                except (AttributeError, TypeError):
                    pass

        self.updatePVs()

        self.log.debug('Processed PV updates: %s',
                       ', '.join(('{}={}'.format(pv, val) for pv, val in updates)))

        self._last_update_call = datetime.now()


class EpicsAdapter(Adapter):
    """
    Inheriting from this class provides an EPICS-interface to a device, powered by
    the pcaspy-module. In the simplest case all that is required is to inherit
    from this class and override the ``pvs``-member. It should be a dictionary
    that contains PV-names (without prefix) as keys and instances of PV as
    values.

    For a simple device with two properties, speed and position, the first of which
    should be read-only, it's enough to define the following:

    .. sourcecode:: Python

        class SimpleDeviceEpicsInterface(EpicsAdapter):
            pvs = {
                'VELO': PV('speed', read_only=True),
                'POS': PV('position', lolo=0, hihi=100)
            }

    For more complex behavior, the interface could contain properties that do not
    exist in the device itself. If the device should also have a PV called STOP
    that "stops the device", the interface could look like this:

    .. sourcecode:: Python

        class SimpleDeviceEpicsInterface(EpicsAdapter):
            pvs = {
                'VELO': PV('speed', read_only=True),
                'POS': PV('position', lolo=0, hihi=100),
                'STOP': PV('stop', type='int'),
            }

            @property
            def stop(self):
                return 0

            @stop.setter
            def stop(self, value):
                if value == 1:
                    self._device.halt()

    Even though the device does *not* have a property called ``stop`` (but a method called
    ``halt``), issuing the command

    ::

        $ caput STOP 1

    will achieve the desired behavior, because ``EpicsAdapter`` merges the properties
    of the device into ``SimpleDeviceEpicsInterface`` itself, so that it is does not
    matter whether the specified property in PV exists in the device or the adapter.

    The intention of this design is to keep device classes small and free of
    protocol specific stuff, such as in the case above where stopping a device
    via EPICS might involve writing a value to a PV, whereas other protocols may
    offer an RPC-way of achieving the same thing.

    :param device: The device that is exposed by the adapter.
    :param arguments: Command line arguments to parse.
    """
    protocol = 'epics'
    pvs = None

    def __init__(self, device, arguments=None):
        super(EpicsAdapter, self).__init__(device, arguments)

        self._options = self._parse_arguments(arguments or [])

        self._create_properties(self.pvs.values())

        self._server = None
        self._driver = None

    @property
    def documentation(self):
        pvs = []

        for name, pv in self.pvs.items():
            complete_name = self._options.prefix + name

            data_type = pv.config.get('type', 'float')
            read_only_tag = ', read only' if pv.read_only else ''

            doc = pv.doc or inspect.getdoc(getattr(type(self), pv.property)) or ''

            pvs.append('{} ({}{}):\n{}'.format(
                complete_name, data_type, read_only_tag, format_doc_text(doc)))

        return '\n\n'.join(
            [inspect.getdoc(self) or '', 'PVs\n==='] + pvs)

    def start_server(self):
        """
        Creates a pcaspy-server.

        .. note::

            The server does not process requests unless :meth:`handle` is called regularly.
        """
        if self._server is None:
            self._server = SimpleServer()
            self._server.createPV(prefix=self._options.prefix,
                                  pvdb={k: v.config for k, v in self.pvs.items()})
            self._driver = PropertyExposingDriver(target=self, pv_dict=self.pvs)
            self._driver.process_pv_updates(force=True)

            self.log.info('Started serving PVs: %s',
                          ', '.join((self._options.prefix + pv for pv in self.pvs.keys())))

    def stop_server(self):
        self._driver = None
        self._server = None

    @property
    def is_running(self):
        return self._server is not None

    def _create_properties(self, pvs):
        for pv in pvs:
            self._install_property(pv.property)

            if pv.meta_data_property is not None:
                self._install_property(pv.meta_data_property)

    def _install_property(self, prop):
        if prop not in dir(self):
            if prop not in dir(self._device):
                raise AttributeError('Can not find property \''
                                     + prop + '\' in device or interface.')
            setattr(type(self), prop, ForwardProperty('_device', prop, instance=self))

    def _parse_arguments(self, arguments):
        parser = ArgumentParser(description="Adapter to expose a device via EPICS")
        parser.add_argument('-p', '--prefix', help='Prefix to use for all PVs', default='')
        return parser.parse_args(arguments)

    def handle(self, cycle_delay=0.1):
        """
        Call this method to spend about ``cycle_delay`` seconds processing
        requests in the pcaspy server. Under load, for example when running ``caget`` at a
        high frequency, the actual time spent in the method may be much shorter. This effect
        is not corrected for.

        :param cycle_delay: Approximate time to be spent processing requests in pcaspy server.
        """
        if self._server is not None:
            self._server.process(cycle_delay)
            self._driver.process_pv_updates()
