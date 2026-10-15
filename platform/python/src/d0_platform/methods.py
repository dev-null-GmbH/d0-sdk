# Generated from the pinned Platform machine contract. Do not edit.
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from . import generated as g


class PlatformOperations:
    def _call(self, operation: str, request: Mapping[str, Any]) -> Any:
        raise NotImplementedError

    def list_audit_events(self, request: g.ListAuditEventsRequest) -> g.ListAuditEventsResult:
        return cast(g.ListAuditEventsResult, self._call('listAuditEvents', request))

    def get_cluster_catalog(self, request: g.GetClusterCatalogRequest) -> g.GetClusterCatalogResult:
        return cast(g.GetClusterCatalogResult, self._call('getClusterCatalog', request))

    def quote_cluster(self, request: g.QuoteClusterRequest) -> g.QuoteClusterResult:
        return cast(g.QuoteClusterResult, self._call('quoteCluster', request))

    def list_clusters(self, request: g.ListClustersRequest) -> g.ListClustersResult:
        return cast(g.ListClustersResult, self._call('listClusters', request))

    def delete_cluster(self, request: g.DeleteClusterRequest) -> g.DeleteClusterResult:
        return cast(g.DeleteClusterResult, self._call('deleteCluster', request))

    def get_cluster(self, request: g.GetClusterRequest) -> g.GetClusterResult:
        return cast(g.GetClusterResult, self._call('getCluster', request))

    def get_cluster_kubeconfig(self, request: g.GetClusterKubeconfigRequest) -> g.GetClusterKubeconfigResult:
        return cast(g.GetClusterKubeconfigResult, self._call('getClusterKubeconfig', request))

    def rotate_cluster_kubeconfig(self, request: g.RotateClusterKubeconfigRequest) -> g.RotateClusterKubeconfigResult:
        return cast(g.RotateClusterKubeconfigResult, self._call('rotateClusterKubeconfig', request))

    def resize_cluster(self, request: g.ResizeClusterRequest) -> g.ResizeClusterResult:
        return cast(g.ResizeClusterResult, self._call('resizeCluster', request))

    def resume_cluster(self, request: g.ResumeClusterRequest) -> g.ResumeClusterResult:
        return cast(g.ResumeClusterResult, self._call('resumeCluster', request))

    def suspend_cluster(self, request: g.SuspendClusterRequest) -> g.SuspendClusterResult:
        return cast(g.SuspendClusterResult, self._call('suspendCluster', request))

    def get_developer_limits(self, request: g.GetDeveloperLimitsRequest) -> g.GetDeveloperLimitsResult:
        return cast(g.GetDeveloperLimitsResult, self._call('getDeveloperLimits', request))

    def get_developer_usage(self, request: g.GetDeveloperUsageRequest) -> g.GetDeveloperUsageResult:
        return cast(g.GetDeveloperUsageResult, self._call('getDeveloperUsage', request))

    def list_domains(self, request: g.ListDomainsRequest) -> g.ListDomainsResult:
        return cast(g.ListDomainsResult, self._call('listDomains', request))

    def get_domain(self, request: g.GetDomainRequest) -> g.GetDomainResult:
        return cast(g.GetDomainResult, self._call('getDomain', request))

    def get_domain_auth_code(self, request: g.GetDomainAuthCodeRequest) -> g.GetDomainAuthCodeResult:
        return cast(g.GetDomainAuthCodeResult, self._call('getDomainAuthCode', request))

    def reset_domain_auth_code(self, request: g.ResetDomainAuthCodeRequest) -> g.ResetDomainAuthCodeResult:
        return cast(g.ResetDomainAuthCodeResult, self._call('resetDomainAuthCode', request))

    def get_domain_contacts(self, request: g.GetDomainContactsRequest) -> g.GetDomainContactsResult:
        return cast(g.GetDomainContactsResult, self._call('getDomainContacts', request))

    def update_domain_contacts(self, request: g.UpdateDomainContactsRequest) -> g.UpdateDomainContactsResult:
        return cast(g.UpdateDomainContactsResult, self._call('updateDomainContacts', request))

    def list_dns_records(self, request: g.ListDNSRecordsRequest) -> g.ListDNSRecordsResult:
        return cast(g.ListDNSRecordsResult, self._call('listDNSRecords', request))

    def delete_dns_record(self, request: g.DeleteDNSRecordRequest) -> g.DeleteDNSRecordResult:
        return cast(g.DeleteDNSRecordResult, self._call('deleteDNSRecord', request))

    def upsert_dns_record(self, request: g.UpsertDNSRecordRequest) -> g.UpsertDNSRecordResult:
        return cast(g.UpsertDNSRecordResult, self._call('upsertDNSRecord', request))

    def set_domain_nameservers(self, request: g.SetDomainNameserversRequest) -> g.SetDomainNameserversResult:
        return cast(g.SetDomainNameserversResult, self._call('setDomainNameservers', request))

    def get_object_storage_catalog(self, request: g.GetObjectStorageCatalogRequest) -> g.GetObjectStorageCatalogResult:
        return cast(g.GetObjectStorageCatalogResult, self._call('getObjectStorageCatalog', request))

    def list_object_storage_buckets(self, request: g.ListObjectStorageBucketsRequest) -> g.ListObjectStorageBucketsResult:
        return cast(g.ListObjectStorageBucketsResult, self._call('listObjectStorageBuckets', request))

    def create_object_storage_bucket(self, request: g.CreateObjectStorageBucketRequest) -> g.CreateObjectStorageBucketResult:
        return cast(g.CreateObjectStorageBucketResult, self._call('createObjectStorageBucket', request))

    def delete_object_storage_bucket(self, request: g.DeleteObjectStorageBucketRequest) -> g.DeleteObjectStorageBucketResult:
        return cast(g.DeleteObjectStorageBucketResult, self._call('deleteObjectStorageBucket', request))

    def list_object_storage_credentials(self, request: g.ListObjectStorageCredentialsRequest) -> g.ListObjectStorageCredentialsResult:
        return cast(g.ListObjectStorageCredentialsResult, self._call('listObjectStorageCredentials', request))

    def create_object_storage_credential(self, request: g.CreateObjectStorageCredentialRequest) -> g.CreateObjectStorageCredentialResult:
        return cast(g.CreateObjectStorageCredentialResult, self._call('createObjectStorageCredential', request))

    def delete_object_storage_credential(self, request: g.DeleteObjectStorageCredentialRequest) -> g.DeleteObjectStorageCredentialResult:
        return cast(g.DeleteObjectStorageCredentialResult, self._call('deleteObjectStorageCredential', request))
