from rest_framework import serializers

from nautobot.circuits.models import Provider, Circuit, CircuitTermination, CircuitType, ProviderNetwork
from nautobot.core.api import WritableNestedSerializer
from nautobot.dcim.api.nested_serializers import (
    NestedCableSerializer,
    NestedInterfaceSerializer,
    NestedSiteSerializer,
)
from nautobot.dcim.api.serializers import (
    CableTerminationSerializer,
    ConnectedEndpointSerializer,
)
from nautobot.extras.api.customfields import CustomFieldModelSerializer
from nautobot.extras.api.serializers import (
    StatusModelSerializerMixin,
    TaggedObjectSerializer,
)
from nautobot.tenancy.api.nested_serializers import NestedTenantSerializer

# Not all of these variable(s) are not actually used anywhere in this file, but required for the
# automagically replacing a Serializer with its corresponding NestedSerializer.
from .nested_serializers import (  # noqa: F401
    NestedCircuitSerializer,
    NestedCircuitTerminationSerializer,
    NestedCircuitTypeSerializer,
    NestedProviderNetworkSerializer,
    NestedProviderSerializer,
)

#
# Providers
#


class ProviderSerializer(TaggedObjectSerializer, CustomFieldModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="circuits-api:provider-detail")
    circuit_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Provider
        fields = [
            "id",
            "url",
            "name",
            "slug",
            "asn",
            "account",
            "portal_url",
            "noc_contact",
            "admin_contact",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "circuit_count",
            "computed_fields",
        ]
        opt_in_fields = ["computed_fields"]


#
# Provider Network
#


class ProviderNetworkSerializer(TaggedObjectSerializer, CustomFieldModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="circuits-api:providernetwork-detail")
    provider = NestedProviderSerializer()

    class Meta:
        model = ProviderNetwork
        fields = [
            "id",
            "url",
            "provider",
            "name",
            "slug",
            "description",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "computed_fields",
        ]
        opt_in_fields = ["computed_fields"]


#
# Circuits
#


class CircuitTypeSerializer(CustomFieldModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="circuits-api:circuittype-detail")
    circuit_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CircuitType
        fields = [
            "id",
            "url",
            "name",
            "slug",
            "description",
            "circuit_count",
            "custom_fields",
            "created",
            "last_updated",
            "computed_fields",
        ]
        opt_in_fields = ["computed_fields"]


class CircuitCircuitTerminationSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="circuits-api:circuittermination-detail")
    site = NestedSiteSerializer()
    provider_network = NestedProviderNetworkSerializer()
    connected_endpoint = NestedInterfaceSerializer()

    class Meta:
        model = CircuitTermination
        fields = [
            "id",
            "url",
            "site",
            "provider_network",
            "connected_endpoint",
            "port_speed",
            "upstream_speed",
            "xconnect_id",
        ]


class CircuitSerializer(TaggedObjectSerializer, StatusModelSerializerMixin, CustomFieldModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="circuits-api:circuit-detail")
    provider = NestedProviderSerializer()
    type = NestedCircuitTypeSerializer()
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    termination_a = CircuitCircuitTerminationSerializer(read_only=True)
    termination_z = CircuitCircuitTerminationSerializer(read_only=True)

    class Meta:
        model = Circuit
        fields = [
            "id",
            "url",
            "cid",
            "provider",
            "type",
            "status",
            "tenant",
            "install_date",
            "commit_rate",
            "description",
            "termination_a",
            "termination_z",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "computed_fields",
        ]
        opt_in_fields = ["computed_fields"]


class CircuitTerminationSerializer(CableTerminationSerializer, ConnectedEndpointSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="circuits-api:circuittermination-detail")
    circuit = NestedCircuitSerializer()
    site = NestedSiteSerializer(required=False, allow_null=True)
    provider_network = NestedProviderNetworkSerializer(required=False, allow_null=True)
    cable = NestedCableSerializer(read_only=True)

    class Meta:
        model = CircuitTermination
        fields = [
            "id",
            "url",
            "circuit",
            "term_side",
            "site",
            "provider_network",
            "port_speed",
            "upstream_speed",
            "xconnect_id",
            "pp_info",
            "description",
            "cable",
            "cable_peer",
            "cable_peer_type",
            "connected_endpoint",
            "connected_endpoint_type",
            "connected_endpoint_reachable",
        ]
