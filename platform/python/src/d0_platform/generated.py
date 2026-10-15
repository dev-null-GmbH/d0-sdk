# Generated from the pinned Platform machine contract. Do not edit.
from __future__ import annotations

from typing import Any, Literal, NotRequired, TypedDict


class AuditEventBody(TypedDict):
    actor: NotRequired[str]
    created_at: str
    detail: NotRequired[dict[str, Any]]
    from_state: NotRequired[str]
    id: str
    resource_id: str
    resource_type: Literal['order', 'cluster', 'object_storage_bucket', 'object_storage_credential']
    state_version: int
    to_state: str

class AuthCodeOutputBody(TypedDict):
    auth_code: str

class BoundBody(TypedDict):
    max: int
    min: int

class Bucket(TypedDict):
    created_at: str
    id: str
    name: str
    s3_name: str
    state: str

class Catalog(TypedDict):
    enabled: bool
    endpoint: str
    limits: Limits
    region: str

class CatalogBody(TypedDict):
    max_memory_per_vcpu: int
    memory_gib: BoundBody
    network: CatalogBodyNetworkStruct
    presets: list[PresetBody] | None
    rates: RateCardBody
    storage_gib: BoundBody
    vcpu: BoundBody

class CatalogBodyNetworkStruct(TypedDict):
    dedicated_ipv6: bool
    public_ipv4_available: bool

class ClusterBody(TypedDict):
    created_at: str
    currency: NotRequired[str]
    endpoint: NotRequired[str]
    id: str
    name: str
    offering: str
    price_cents: NotRequired[int]
    public_ipv4_address: NotRequired[str]
    ready: bool
    spec: SpecBody
    state: str
    state_version: int
    updated_at: str

class ClusterQuoteOutputBody(TypedDict):
    price: PriceBody
    spec: SpecBody

class CreatedCredential(TypedDict):
    credential: Credential
    secret_access_key: str

class Credential(TypedDict):
    access_key_id: NotRequired[str]
    created_at: str
    id: str
    name: str
    state: str
    write_access: bool

class DailyUsage(TypedDict):
    day: str
    duration_ms: float
    errors: int
    rate_limited: int
    requests: int

class DomainBody(TypedDict):
    created_at: str
    expires_at: NotRequired[str]
    fqdn: str
    nameservers: NotRequired[list[str] | None]
    status: str
    updated_at: str

class ErrorDetail(TypedDict):
    location: NotRequired[str]
    message: NotRequired[str]
    value: NotRequired[dict[str, Any]]

class ErrorModel(TypedDict):
    detail: NotRequired[str]
    errors: NotRequired[list[ErrorDetail] | None]
    instance: NotRequired[str]
    status: NotRequired[int]
    title: NotRequired[str]
    type: NotRequired[str]

class KubeconfigOutputBody(TypedDict):
    kubeconfig: str

class Limits(TypedDict):
    max_bucket_bytes: int
    max_buckets: int
    max_credentials_per_bucket: int
    max_total_bytes: int

class ListAuditEventsOutputBody(TypedDict):
    events: list[AuditEventBody] | None
    next_before: str

class ListClustersOutputBody(TypedDict):
    clusters: list[ClusterBody] | None

class ListDomainsOutputBody(TypedDict):
    domains: list[DomainBody] | None

class ListRecordsOutputBody(TypedDict):
    records: list[RecordBody] | None

class NameserverInput(TypedDict):
    host: str
    ipv4: NotRequired[str]
    ipv6: NotRequired[str]

class ObjectStorageBucketsOutputBody(TypedDict):
    buckets: list[Bucket] | None

class ObjectStorageCreateBucketInputBody(TypedDict):
    name: str

class ObjectStorageCreateCredentialInputBody(TypedDict):
    name: str
    write_access: bool

class ObjectStorageCredentialsOutputBody(TypedDict):
    credentials: list[Credential] | None

class PresetBody(TypedDict):
    name: str
    price: PriceBody
    spec: SpecBody

class PriceBody(TypedDict):
    amount_cents: int
    currency: str
    interval: str

class ProductUsage(TypedDict):
    duration_ms: float
    errors: int
    product: str
    rate_limited: int
    requests: int

class RateCardBody(TypedDict):
    base_cents: int
    currency: str
    per_memory_gib_cents: int
    per_public_ipv4_cents: int
    per_storage_gib_cents: int
    per_vcpu_cents: int

class RateLimitBucket(TypedDict):
    remaining: int
    requests_per_window: int
    reset_after_seconds: int
    scope: Literal['organization', 'client']
    window_seconds: int

class RecordBody(TypedDict):
    name: str
    read_only: bool
    records: list[str] | None
    ttl: int
    type: str

class RecordUpsertBody(TypedDict):
    records: list[str] | None
    ttl: NotRequired[int]

class RegistrantInput(TypedDict):
    city: str
    company_name: NotRequired[str]
    country: str
    email: str
    first_name: str
    last_name: str
    phone: str
    registration_data: NotRequired[RegistrationData]
    state: NotRequired[str]
    street: str
    street_number: NotRequired[str]
    zipcode: str

class RegistrationData(TypedDict):
    customer: NotRequired[dict[str, Any]]
    domain: NotRequired[dict[str, Any]]

class ResizeClusterInputBody(TypedDict):
    spec: SpecReqBody

class Result(TypedDict):
    buckets: list[RateLimitBucket] | None
    client_id: str
    environment: Literal['production', 'test']
    observed_at: str
    over_limit: bool

class SetNameserversInputBody(TypedDict):
    nameservers: list[NameserverInput] | None

class SpecBody(TypedDict):
    memory_gib: int
    public_ipv4: bool
    storage_gib: int
    vcpu: int

class SpecReqBody(TypedDict):
    memory_gib: int
    public_ipv4: NotRequired[bool]
    storage_gib: int
    vcpu: int

class Totals(TypedDict):
    duration_ms: float
    errors: int
    rate_limited: int
    requests: int

class UpdateContactsInputBody(TypedDict):
    registrant: RegistrantInput

Usage = TypedDict('Usage', {'by_product': list[ProductUsage] | None, 'collection_gaps_24h': int, 'coverage_from': str, 'covered_products': list[str] | None, 'daily': list[DailyUsage] | None, 'environment': Literal['production', 'test'], 'from': str, 'observed_at': str, 'totals': Totals, 'until': str})

class ListAuditEventsRequest(TypedDict):
    limit: NotRequired[int]
    before: NotRequired[str]

type ListAuditEventsResult = ListAuditEventsOutputBody

class GetClusterCatalogRequest(TypedDict):
    pass

type GetClusterCatalogResult = CatalogBody

class QuoteClusterRequest(TypedDict):
    body: SpecReqBody

type QuoteClusterResult = ClusterQuoteOutputBody

class ListClustersRequest(TypedDict):
    pass

type ListClustersResult = ListClustersOutputBody

class DeleteClusterRequest(TypedDict):
    id: str
    idempotencyKey: str

type DeleteClusterResult = ClusterBody

class GetClusterRequest(TypedDict):
    id: str

type GetClusterResult = ClusterBody

class GetClusterKubeconfigRequest(TypedDict):
    id: str

type GetClusterKubeconfigResult = KubeconfigOutputBody

class RotateClusterKubeconfigRequest(TypedDict):
    id: str
    idempotencyKey: str

type RotateClusterKubeconfigResult = ClusterBody

class ResizeClusterRequest(TypedDict):
    id: str
    idempotencyKey: str
    body: ResizeClusterInputBody

type ResizeClusterResult = ClusterBody

class ResumeClusterRequest(TypedDict):
    id: str
    idempotencyKey: str

type ResumeClusterResult = ClusterBody

class SuspendClusterRequest(TypedDict):
    id: str
    idempotencyKey: str

type SuspendClusterResult = ClusterBody

class GetDeveloperLimitsRequest(TypedDict):
    pass

type GetDeveloperLimitsResult = Result

class GetDeveloperUsageRequest(TypedDict):
    product: NotRequired[str]
    environment: NotRequired[Literal['production', 'test']]
    client_id: NotRequired[str]
    from_: NotRequired[str]
    until: NotRequired[str]

type GetDeveloperUsageResult = Usage

class ListDomainsRequest(TypedDict):
    pass

type ListDomainsResult = ListDomainsOutputBody

class GetDomainRequest(TypedDict):
    domain: str

type GetDomainResult = DomainBody

class GetDomainAuthCodeRequest(TypedDict):
    domain: str

type GetDomainAuthCodeResult = AuthCodeOutputBody

class ResetDomainAuthCodeRequest(TypedDict):
    domain: str

type ResetDomainAuthCodeResult = AuthCodeOutputBody

class GetDomainContactsRequest(TypedDict):
    domain: str

type GetDomainContactsResult = RegistrantInput

class UpdateDomainContactsRequest(TypedDict):
    domain: str
    body: UpdateContactsInputBody

type UpdateDomainContactsResult = None

class ListDNSRecordsRequest(TypedDict):
    domain: str

type ListDNSRecordsResult = ListRecordsOutputBody

class DeleteDNSRecordRequest(TypedDict):
    domain: str
    name: str
    type: str

type DeleteDNSRecordResult = None

class UpsertDNSRecordRequest(TypedDict):
    domain: str
    name: str
    type: str
    body: RecordUpsertBody

type UpsertDNSRecordResult = RecordBody

class SetDomainNameserversRequest(TypedDict):
    domain: str
    body: SetNameserversInputBody

type SetDomainNameserversResult = None

class GetObjectStorageCatalogRequest(TypedDict):
    pass

type GetObjectStorageCatalogResult = Catalog

class ListObjectStorageBucketsRequest(TypedDict):
    pass

type ListObjectStorageBucketsResult = ObjectStorageBucketsOutputBody

class CreateObjectStorageBucketRequest(TypedDict):
    body: ObjectStorageCreateBucketInputBody

type CreateObjectStorageBucketResult = Bucket | None

class DeleteObjectStorageBucketRequest(TypedDict):
    id: str

type DeleteObjectStorageBucketResult = None

class ListObjectStorageCredentialsRequest(TypedDict):
    id: str

type ListObjectStorageCredentialsResult = ObjectStorageCredentialsOutputBody

class CreateObjectStorageCredentialRequest(TypedDict):
    id: str
    body: ObjectStorageCreateCredentialInputBody

type CreateObjectStorageCredentialResult = CreatedCredential

class DeleteObjectStorageCredentialRequest(TypedDict):
    id: str
    credential_id: str

type DeleteObjectStorageCredentialResult = None
