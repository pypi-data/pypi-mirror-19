from .constants import DESCRIPTOR_TYPE, DEVICE_CAPABILITY_TYPE, ENDPOINT
from .formatters import UInt8Formatter, UInt16Formatter, BCD16Formatter, BitMapFormatter, StringFormatter, Formatter, CommentFormatter
from .defaults import defaults


class Descriptor(object):
    def __init__(self, descriptor_type, *formatters):
        self._data = []
        self._size = 0
        self.append(UInt8Formatter(descriptor_type, 'Descriptor Type'))

        for formatter in formatters:
            self.append(formatter)

    def append(self, formatter):
        self._data.append(formatter)
        self._size += len(formatter)

    def prepend(self, formatter):
        self._data.prepend(formatter)
        self._size += len(formatter)

    def get_data(self):
        return [UInt8Formatter(len(self), 'Descriptor Size')] + self._data

    def __len__(self):
        return self._size + 1

    def __call__(*args):
        raise Exception(args)

    def __str__(self):
        formatters = self.get_data()
        max_main_length = max(formatter.get_main_length() for formatter in formatters)
        for formatter in formatters:
            formatter.set_max_main_length(max_main_length)
        return '{\n' + ''.join('\t{}\n'.format(formatter) for formatter in formatters) + '}'


class DescriptorWithChildren(Descriptor):
    def __init__(self, descriptor_type, *children):
        super(DescriptorWithChildren, self).__init__(descriptor_type)

        self._children = []
        self._children_size = 0

        self._size_formatter = UInt16Formatter(0, 'Size of descriptor and all its sub descriptors')
        self._number_formatter = UInt8Formatter(0, 'Number of sub descriptors')

        for child in children:
            self.add(child)

    def add(self, child):
        self._children.append(child)
        try:
            self._children_size += child.get_size()
        except AttributeError:
            self._children_size += len(child)

    def get_size(self):
        return len(self) + self._children_size

    def get_number(self):
        return len(self._children)

    def get_data(self):
        self._size_formatter.set(self.get_size())
        self._number_formatter.set(self.get_number())

        data = super(DescriptorWithChildren, self).get_data()
        for child in self._children:
            data += [Formatter(), CommentFormatter(child.__class__.__name__)] + child.get_data()

        return data


class StringDescriptor(Descriptor):
    def __init__(self, *args):
        super(StringDescriptor, self).__init__(DESCRIPTOR_TYPE.STRING)
        if len(args) == 1 and (type(args[0]) == str or type(args[0]) == unicode):
            self.append(StringFormatter(args[0], 'String'))
        else:
            for i, langid in enumerate(args):
                self.append(UInt16Formatter(langid, 'Language Identifier {}'.format(i)))


class DeviceDescriptor(Descriptor):
    def __init__(self, **kwargs):
        super(DeviceDescriptor, self).__init__(DESCRIPTOR_TYPE.DEVICE)

        self.append(BCD16Formatter(defaults.get('usb_version', kwargs, 2.0), "USB Version"))
        self.append(UInt8Formatter(defaults.get('device_class', kwargs, 0), "Device Class"))
        self.append(UInt8Formatter(defaults.get('device_subclass', kwargs, 0), "Device Sub-class"))
        self.append(UInt8Formatter(defaults.get('device_protocol', kwargs, 0), "Device Protocol"))
        self.append(UInt8Formatter(defaults.get('max_packet_size', kwargs, 8), "Max packet size for EP0"))
        self.append(UInt16Formatter(defaults.get('vendor_id', kwargs, 0), "Vendor ID"))
        self.append(UInt16Formatter(defaults.get('product_id', kwargs, 0), "Product ID"))
        self.append(UInt16Formatter(defaults.get('device_release_number', kwargs, 0), "Device release number"))
        self.append(UInt8Formatter(defaults.get('manufacturer_string', kwargs, 0), "Manufacturer string index"))
        self.append(UInt8Formatter(defaults.get('product_string', kwargs, 0), "Product string index"))
        self.append(UInt8Formatter(defaults.get('serial_number_string', kwargs, 0), "Serial string index"))
        self.append(UInt8Formatter(defaults.get('number_of_configurations', kwargs, 1), "Number of configurations"))


class ConfigurationDescriptor(DescriptorWithChildren):
    def __init__(self, *children, **kwargs):
        super(ConfigurationDescriptor, self).__init__(DESCRIPTOR_TYPE.CONFIGURATION, *children)

        self.append(self._size_formatter)
        self.append(self._number_formatter)

        self.append(UInt8Formatter(defaults.get('configuration_number', kwargs, 1), "Configuration Number"))
        self.append(UInt8Formatter(defaults.get('configuration_string', kwargs, 0), "Configuration String"))

        self.append(BitMapFormatter(
            1,
            [
                0, 0, 0, 0, 0,
                kwargs.get('remote_wakeup', 0),
                kwargs.get('self_powered', 0),
            ],
            "Attributes"
        ))

        self.append(UInt8Formatter(defaults.get('max_power', kwargs, 0), "Max power"))

    def get_number(self):
        n = 0
        for child in self._children:
            if type(child) == InterfaceDescriptor:
                n += 1
        return n


class InterfaceDescriptor(Descriptor):
    def __init__(self, **kwargs):
        super(InterfaceDescriptor, self).__init__(DESCRIPTOR_TYPE.INTERFACE)

        self.append(UInt8Formatter(defaults.get('interface_number', kwargs, 0), "Interface number"))
        self.append(UInt8Formatter(defaults.get('alternate_setting', kwargs, 0), "Alternate setting"))
        self.append(UInt8Formatter(defaults.get('endpoint_count', kwargs, 0), "Number of endpoints"))
        self.append(UInt8Formatter(defaults.get('interface_class', kwargs, 0), "Interface Class"))
        self.append(UInt8Formatter(defaults.get('interface_subclass', kwargs, 0), "Interface Sub-class"))
        self.append(UInt8Formatter(defaults.get('interface_protocol', kwargs, 0), "Interface Protocol"))
        self.append(UInt8Formatter(defaults.get('interface_string', kwargs, 0), "Interface String"))


class EndpointDescriptor(Descriptor):
    def __init__(self, **kwargs):
        super(EndpointDescriptor, self).__init__(DESCRIPTOR_TYPE.ENDPOINT)

        endpoint_number = defaults.get('endpoint_number', kwargs, 0)
        endpoint_in = defaults.get('endpoint_in', kwargs, False)
        self.append(BitMapFormatter(
            1,
            BitMapFormatter.uint_parse(4, endpoint_number) +
            [
                0, 0, 0,
                endpoint_in,
            ],
            "Endpoint Address"
        ))

        attributes = None
        transfer_type = defaults.get('transfer_type', kwargs, ENDPOINT.TRANSFER_TYPE_CONTROL)
        if transfer_type == ENDPOINT.TRANSFER_TYPE_CONTROL or transfer_type == ENDPOINT.TRANSFER_TYPE_BULK:
            attributes = BitMapFormatter(
                1,
                BitMapFormatter.uint_parse(2, transfer_type),
                "Attributes"
            )
        elif transfer_type == ENDPOINT.TRANSFER_TYPE_INTERRUPT:
            attributes = BitMapFormatter(
                1,
                BitMapFormatter.uint_parse(2, transfer_type) +
                [0, 0] +
                BitMapFormatter.uint_parse(2, defaults.get('usage_type', kwargs, ENDPOINT.USAGE_TYPE_INTERRUPT_PERIODIC)),
                "Attributes"
            )
        elif transfer_type == ENDPOINT.TRANSFER_TYPE_ISOCHRONOUS:
            attributes = BitMapFormatter(
                1,
                BitMapFormatter.uint_parse(2, transfer_type) +
                BitMapFormatter.uint_parse(2, defaults.get('synchronization_type', kwargs, ENDPOINT.SYNCHRONIZATION_TYPE_NONE)) +
                BitMapFormatter.uint_parse(2, defaults.get('usage_type', kwargs, ENDPOINT.USAGE_TYPE_ISOCHRONOUS_DATA)),
                "Attributes"
            )
        else:
            raise Exception("Invalid transfer type")

        self.append(attributes)

        default_max_packet_size = 512 if transfer_type == ENDPOINT.TRANSFER_TYPE_CONTROL else 1024
        self.append(UInt16Formatter(defaults.get('max_packet_size', kwargs, default_max_packet_size), "Max Packet Size"))
        self.append(UInt8Formatter(defaults.get('interval', kwargs, 0), "Interval"))


class InterfaceAssociationDescriptor(Descriptor):
    def __init__(self, **kwargs):
        super(InterfaceAssociationDescriptor, self).__init__(DESCRIPTOR_TYPE.INTERFACE_ASSOCIATION)

        self.append(UInt8Formatter(defaults.get('first_interface_number', kwargs, 0), "First interface number"))
        self.append(UInt8Formatter(defaults.get('interface_count', kwargs, 0), "Number of interfaces"))
        self.append(UInt8Formatter(defaults.get('interface_class', kwargs, 0), "Interface Class"))
        self.append(UInt8Formatter(defaults.get('interface_subclass', kwargs, 0), "Interface Sub-class"))
        self.append(UInt8Formatter(defaults.get('interface_protocol', kwargs, 0), "Interface Protocol"))
        self.append(UInt8Formatter(defaults.get('interface_association_string', kwargs, 0), "Interface Association String"))


class DeviceQualifierDescriptor(Descriptor):
    def __init__(self, **kwargs):
        super(DeviceQualifierDescriptor, self).__init__(DESCRIPTOR_TYPE.DEVICE_QUALIFIER)

        self.append(BCD16Formatter(defaults.get('usb_version', kwargs, 2.0), "USB Version"))
        self.append(UInt8Formatter(defaults.get('device_class', kwargs, 0), "Device Class"))
        self.append(UInt8Formatter(defaults.get('device_subclass', kwargs, 0), "Device Sub-class"))
        self.append(UInt8Formatter(defaults.get('device_protocol', kwargs, 0), "Device Protocol"))
        self.append(UInt8Formatter(defaults.get('max_packet_size', kwargs, 8), "Max packet size for EP0"))
        self.append(UInt8Formatter(defaults.get('number_of_configurations', kwargs, 1), "Number of configurations"))
        self.append(UInt8Formatter(0, "Reserved"))


class BOSDescriptor(DescriptorWithChildren):
    def __init__(self, *children):
        super(BOSDescriptor, self).__init__(DESCRIPTOR_TYPE.BOS, *children)

        self.append(self._size_formatter)
        self.append(self._number_formatter)


class CapabilityDescriptor(Descriptor):
    def __init__(self, capability_type, *formatters):
        super(CapabilityDescriptor, self).__init__(
            DESCRIPTOR_TYPE.DEVICE_CAPABILITY,
            UInt8Formatter(capability_type, "Device capability type"),
            *formatters
        )


class USB20ExtensionDescriptor(CapabilityDescriptor):
    def __init__(self, lpm=False, besl=False, besl_baseline=None, besl_deep=None):
        super(USB20ExtensionDescriptor, self).__init__(DEVICE_CAPABILITY_TYPE.USB_20_EXTENSION)

        self.append(BitMapFormatter(
            4,
            [
                0,
                lpm,
                besl,
                besl_baseline is not None,
                besl_deep is not None,
                0, 0, 0
            ] +
            (BitMapFormatter.uint_parse(4, besl_baseline) if besl_baseline else []) +
            (BitMapFormatter.uint_parse(4, besl_deep) if besl_deep else []),
            "Attributes"
        ))


class SuperSpeedDeviceCapabilityDescriptor(CapabilityDescriptor):
    def __init__(self, ltm=False, supported_speed_low=False, supported_speed_full=False, supported_speed_high=False, supported_speed_gen1=False, full_functionality_support_speed=0, u1_device_exit_latency=0, u2_device_exit_latency=0):
        super(SuperSpeedDeviceCapabilityDescriptor, self).__init__(DEVICE_CAPABILITY_TYPE.SUPERSPEED_USB)

        self.append(BitMapFormatter(1, [0, ltm], "Attributes"))
        self.append(BitMapFormatter(2, [
            supported_speed_low,
            supported_speed_full,
            supported_speed_high,
            supported_speed_gen1,
        ], "Supported speeds"))
        self.append(UInt8Formatter(full_functionality_support_speed, "Full functionality support speed"))
        self.append(UInt8Formatter(u1_device_exit_latency, "U1 Device Exit Latency"))
        self.append(UInt16Formatter(u2_device_exit_latency, "U2 Device Exit Latency"))


class SuperSpeedEndpointCompanionDescriptor(Descriptor):
    def __init__(self, **kwargs):
        super(SuperSpeedEndpointCompanionDescriptor, self).__init__(DESCRIPTOR_TYPE.SUPERSPEED_USB_ENDPOINT_COMPANION)

        self.append(UInt8Formatter(defaults.get('max_burst', kwargs, 1)-1, "Max Burst"))

        max_streams = kwargs.get('max_streams')
        mult = kwargs.get('mult')
        if max_streams is not None:
            if max_streams < 16:
                self.append(UInt8Formatter(max_streams, "Max streams"))
            else:
                raise Exception("Max streams out of range")
        elif mult is not None:
            self.append(BitMapFormatter(
                1,
                BitMapFormatter.uint_parse(2, mult),
                [
                    0, 0, 0, 0, 0,
                    kwargs.get('ssp_iso_companion', False)
                ],
                "Attributes",
            ))
        else:
            self.append(UInt8Formatter(0, "Attributes"))

        self.append(UInt16Formatter(defaults.get('bytes_per_interval', kwargs, 0), "Bytes Per Interval"))
