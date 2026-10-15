// Code generated from the pinned Platform machine contract. Do not edit.
package platform

import (
	"context"
	"errors"
	"github.com/dev-null-GmbH/d0-sdk/platform/go/gen"
)

var testOperations = map[string]bool{
	"deleteDNSRecord": true,
	"getDomain":       true,
	"listDNSRecords":  true,
	"listDomains":     true,
	"upsertDNSRecord": true,
}

func (c *Client) ListAuditEvents(ctx context.Context, params *gen.PlatformListAuditEventsParams) (*gen.PlatformListAuditEventsResponse, error) {
	if err := c.allow("listAuditEvents"); err != nil {
		return nil, err
	}
	r, err := c.api.PlatformListAuditEventsWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetClusterCatalog(ctx context.Context) (*gen.PlatformGetClusterCatalogResponse, error) {
	if err := c.allow("getClusterCatalog"); err != nil {
		return nil, err
	}
	r, err := c.api.PlatformGetClusterCatalogWithResponse(ctx)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) QuoteCluster(ctx context.Context, body gen.PlatformQuoteClusterJSONRequestBody) (*gen.PlatformQuoteClusterResponse, error) {
	if err := c.allow("quoteCluster"); err != nil {
		return nil, err
	}
	r, err := c.api.PlatformQuoteClusterWithResponse(ctx, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListClusters(ctx context.Context) (*gen.PlatformListClustersResponse, error) {
	if err := c.allow("listClusters"); err != nil {
		return nil, err
	}
	r, err := c.api.PlatformListClustersWithResponse(ctx)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) DeleteCluster(ctx context.Context, id string, params *gen.PlatformDeleteClusterParams) (*gen.PlatformDeleteClusterResponse, error) {
	if err := c.allow("deleteCluster"); err != nil {
		return nil, err
	}
	if !validPath(id) {
		return nil, errors.New("invalid Platform path identifier")
	}
	if params == nil || !validKey(params.IdempotencyKey) {
		return nil, errors.New("idempotency key must be 16–128 safe characters")
	}
	r, err := c.api.PlatformDeleteClusterWithResponse(ctx, id, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetCluster(ctx context.Context, id string) (*gen.PlatformGetClusterResponse, error) {
	if err := c.allow("getCluster"); err != nil {
		return nil, err
	}
	if !validPath(id) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformGetClusterWithResponse(ctx, id)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetClusterKubeconfig(ctx context.Context, id string) (*gen.PlatformGetClusterKubeconfigResponse, error) {
	if err := c.allow("getClusterKubeconfig"); err != nil {
		return nil, err
	}
	if !validPath(id) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformGetClusterKubeconfigWithResponse(ctx, id)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) RotateClusterKubeconfig(ctx context.Context, id string, params *gen.PlatformRotateClusterKubeconfigParams) (*gen.PlatformRotateClusterKubeconfigResponse, error) {
	if err := c.allow("rotateClusterKubeconfig"); err != nil {
		return nil, err
	}
	if !validPath(id) {
		return nil, errors.New("invalid Platform path identifier")
	}
	if params == nil || !validKey(params.IdempotencyKey) {
		return nil, errors.New("idempotency key must be 16–128 safe characters")
	}
	r, err := c.api.PlatformRotateClusterKubeconfigWithResponse(ctx, id, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ResizeCluster(ctx context.Context, id string, params *gen.PlatformResizeClusterParams, body gen.PlatformResizeClusterJSONRequestBody) (*gen.PlatformResizeClusterResponse, error) {
	if err := c.allow("resizeCluster"); err != nil {
		return nil, err
	}
	if !validPath(id) {
		return nil, errors.New("invalid Platform path identifier")
	}
	if params == nil || !validKey(params.IdempotencyKey) {
		return nil, errors.New("idempotency key must be 16–128 safe characters")
	}
	r, err := c.api.PlatformResizeClusterWithResponse(ctx, id, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ResumeCluster(ctx context.Context, id string, params *gen.PlatformResumeClusterParams) (*gen.PlatformResumeClusterResponse, error) {
	if err := c.allow("resumeCluster"); err != nil {
		return nil, err
	}
	if !validPath(id) {
		return nil, errors.New("invalid Platform path identifier")
	}
	if params == nil || !validKey(params.IdempotencyKey) {
		return nil, errors.New("idempotency key must be 16–128 safe characters")
	}
	r, err := c.api.PlatformResumeClusterWithResponse(ctx, id, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) SuspendCluster(ctx context.Context, id string, params *gen.PlatformSuspendClusterParams) (*gen.PlatformSuspendClusterResponse, error) {
	if err := c.allow("suspendCluster"); err != nil {
		return nil, err
	}
	if !validPath(id) {
		return nil, errors.New("invalid Platform path identifier")
	}
	if params == nil || !validKey(params.IdempotencyKey) {
		return nil, errors.New("idempotency key must be 16–128 safe characters")
	}
	r, err := c.api.PlatformSuspendClusterWithResponse(ctx, id, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetDeveloperLimits(ctx context.Context) (*gen.PlatformGetDeveloperLimitsResponse, error) {
	if err := c.allow("getDeveloperLimits"); err != nil {
		return nil, err
	}
	r, err := c.api.PlatformGetDeveloperLimitsWithResponse(ctx)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetDeveloperUsage(ctx context.Context, params *gen.PlatformGetDeveloperUsageParams) (*gen.PlatformGetDeveloperUsageResponse, error) {
	if err := c.allow("getDeveloperUsage"); err != nil {
		return nil, err
	}
	r, err := c.api.PlatformGetDeveloperUsageWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListDomains(ctx context.Context) (*gen.PlatformListDomainsResponse, error) {
	if err := c.allow("listDomains"); err != nil {
		return nil, err
	}
	r, err := c.api.PlatformListDomainsWithResponse(ctx)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetDomain(ctx context.Context, domain string) (*gen.PlatformGetDomainResponse, error) {
	if err := c.allow("getDomain"); err != nil {
		return nil, err
	}
	if !validPath(domain) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformGetDomainWithResponse(ctx, domain)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetDomainAuthCode(ctx context.Context, domain string) (*gen.PlatformGetDomainAuthCodeResponse, error) {
	if err := c.allow("getDomainAuthCode"); err != nil {
		return nil, err
	}
	if !validPath(domain) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformGetDomainAuthCodeWithResponse(ctx, domain)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ResetDomainAuthCode(ctx context.Context, domain string) (*gen.PlatformResetDomainAuthCodeResponse, error) {
	if err := c.allow("resetDomainAuthCode"); err != nil {
		return nil, err
	}
	if !validPath(domain) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformResetDomainAuthCodeWithResponse(ctx, domain)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetDomainContacts(ctx context.Context, domain string) (*gen.PlatformGetDomainContactsResponse, error) {
	if err := c.allow("getDomainContacts"); err != nil {
		return nil, err
	}
	if !validPath(domain) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformGetDomainContactsWithResponse(ctx, domain)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) UpdateDomainContacts(ctx context.Context, domain string, body gen.PlatformUpdateDomainContactsJSONRequestBody) (*gen.PlatformUpdateDomainContactsResponse, error) {
	if err := c.allow("updateDomainContacts"); err != nil {
		return nil, err
	}
	if !validPath(domain) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformUpdateDomainContactsWithResponse(ctx, domain, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 204 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListDNSRecords(ctx context.Context, domain string) (*gen.PlatformListDNSRecordsResponse, error) {
	if err := c.allow("listDNSRecords"); err != nil {
		return nil, err
	}
	if !validPath(domain) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformListDNSRecordsWithResponse(ctx, domain)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) DeleteDNSRecord(ctx context.Context, domain string, name string, pType string) (*gen.PlatformDeleteDNSRecordResponse, error) {
	if err := c.allow("deleteDNSRecord"); err != nil {
		return nil, err
	}
	if !validPath(domain) {
		return nil, errors.New("invalid Platform path identifier")
	}
	if !validPath(name) {
		return nil, errors.New("invalid Platform path identifier")
	}
	if !validPath(pType) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformDeleteDNSRecordWithResponse(ctx, domain, name, pType)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 204 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) UpsertDNSRecord(ctx context.Context, domain string, name string, pType string, body gen.PlatformUpsertDNSRecordJSONRequestBody) (*gen.PlatformUpsertDNSRecordResponse, error) {
	if err := c.allow("upsertDNSRecord"); err != nil {
		return nil, err
	}
	if !validPath(domain) {
		return nil, errors.New("invalid Platform path identifier")
	}
	if !validPath(name) {
		return nil, errors.New("invalid Platform path identifier")
	}
	if !validPath(pType) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformUpsertDNSRecordWithResponse(ctx, domain, name, pType, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) SetDomainNameservers(ctx context.Context, domain string, body gen.PlatformSetDomainNameserversJSONRequestBody) (*gen.PlatformSetDomainNameserversResponse, error) {
	if err := c.allow("setDomainNameservers"); err != nil {
		return nil, err
	}
	if !validPath(domain) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformSetDomainNameserversWithResponse(ctx, domain, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 204 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetObjectStorageCatalog(ctx context.Context) (*gen.PlatformGetObjectStorageCatalogResponse, error) {
	if err := c.allow("getObjectStorageCatalog"); err != nil {
		return nil, err
	}
	r, err := c.api.PlatformGetObjectStorageCatalogWithResponse(ctx)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListObjectStorageBuckets(ctx context.Context) (*gen.PlatformListObjectStorageBucketsResponse, error) {
	if err := c.allow("listObjectStorageBuckets"); err != nil {
		return nil, err
	}
	r, err := c.api.PlatformListObjectStorageBucketsWithResponse(ctx)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateObjectStorageBucket(ctx context.Context, body gen.PlatformCreateObjectStorageBucketJSONRequestBody) (*gen.PlatformCreateObjectStorageBucketResponse, error) {
	if err := c.allow("createObjectStorageBucket"); err != nil {
		return nil, err
	}
	r, err := c.api.PlatformCreateObjectStorageBucketWithResponse(ctx, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 && r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) DeleteObjectStorageBucket(ctx context.Context, id string) (*gen.PlatformDeleteObjectStorageBucketResponse, error) {
	if err := c.allow("deleteObjectStorageBucket"); err != nil {
		return nil, err
	}
	if !validPath(id) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformDeleteObjectStorageBucketWithResponse(ctx, id)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 && r.StatusCode() != 204 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListObjectStorageCredentials(ctx context.Context, id string) (*gen.PlatformListObjectStorageCredentialsResponse, error) {
	if err := c.allow("listObjectStorageCredentials"); err != nil {
		return nil, err
	}
	if !validPath(id) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformListObjectStorageCredentialsWithResponse(ctx, id)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateObjectStorageCredential(ctx context.Context, id string, body gen.PlatformCreateObjectStorageCredentialJSONRequestBody) (*gen.PlatformCreateObjectStorageCredentialResponse, error) {
	if err := c.allow("createObjectStorageCredential"); err != nil {
		return nil, err
	}
	if !validPath(id) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformCreateObjectStorageCredentialWithResponse(ctx, id, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) DeleteObjectStorageCredential(ctx context.Context, id string, credentialId string) (*gen.PlatformDeleteObjectStorageCredentialResponse, error) {
	if err := c.allow("deleteObjectStorageCredential"); err != nil {
		return nil, err
	}
	if !validPath(id) {
		return nil, errors.New("invalid Platform path identifier")
	}
	if !validPath(credentialId) {
		return nil, errors.New("invalid Platform path identifier")
	}
	r, err := c.api.PlatformDeleteObjectStorageCredentialWithResponse(ctx, id, credentialId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 && r.StatusCode() != 204 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}
