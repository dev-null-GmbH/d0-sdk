// Code generated from the pinned Accounting public catalog. Do not edit.
package accounting

import (
	"context"
	"github.com/dev-null-GmbH/d0-sdk/accounting/go/gen"
)

var testOperations = map[string]bool{
	"createAccount":            true,
	"createJournalEntryDraft":  true,
	"createPeriod":             true,
	"discardJournalEntryDraft": true,
	"getAccount":               true,
	"getJournalEntry":          true,
	"getPeriod":                true,
	"getTrialBalance":          true,
	"listAccounts":             true,
	"listJournalEntries":       true,
	"listPeriods":              true,
	"replaceJournalEntryDraft": true,
}

func (c *Client) ListTaxRules(ctx context.Context, params *gen.ListTaxRulesParams) (*gen.ListTaxRulesResponse, error) {
	if err := c.allow("listTaxRules"); err != nil {
		return nil, err
	}
	r, err := c.api.ListTaxRulesWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CalculateTax(ctx context.Context, params *gen.CalculateTaxParams, body gen.CalculateTaxJSONRequestBody) (*gen.CalculateTaxResponse, error) {
	if err := c.allow("calculateTax"); err != nil {
		return nil, err
	}
	r, err := c.api.CalculateTaxWithResponse(ctx, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetFinancialStatements(ctx context.Context, params *gen.GetFinancialStatementsParams) (*gen.GetFinancialStatementsResponse, error) {
	if err := c.allow("getFinancialStatements"); err != nil {
		return nil, err
	}
	r, err := c.api.GetFinancialStatementsWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListFiscalYears(ctx context.Context, params *gen.ListFiscalYearsParams) (*gen.ListFiscalYearsResponse, error) {
	if err := c.allow("listFiscalYears"); err != nil {
		return nil, err
	}
	r, err := c.api.ListFiscalYearsWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateFiscalYear(ctx context.Context, params *gen.CreateFiscalYearParams, body gen.CreateFiscalYearJSONRequestBody) (*gen.CreateFiscalYearResponse, error) {
	if err := c.allow("createFiscalYear"); err != nil {
		return nil, err
	}
	r, err := c.api.CreateFiscalYearWithResponse(ctx, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetFiscalYear(ctx context.Context, yearId gen.FiscalYearId) (*gen.GetFiscalYearResponse, error) {
	if err := c.allow("getFiscalYear"); err != nil {
		return nil, err
	}
	r, err := c.api.GetFiscalYearWithResponse(ctx, yearId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) FinalizeFiscalYear(ctx context.Context, yearId gen.FiscalYearId, params *gen.FinalizeFiscalYearParams) (*gen.FinalizeFiscalYearResponse, error) {
	if err := c.allow("finalizeFiscalYear"); err != nil {
		return nil, err
	}
	r, err := c.api.FinalizeFiscalYearWithResponse(ctx, yearId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CloseFiscalYear(ctx context.Context, yearId gen.FiscalYearId, params *gen.CloseFiscalYearParams, body gen.CloseFiscalYearJSONRequestBody) (*gen.CloseFiscalYearResponse, error) {
	if err := c.allow("closeFiscalYear"); err != nil {
		return nil, err
	}
	r, err := c.api.CloseFiscalYearWithResponse(ctx, yearId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CarryforwardFiscalYear(ctx context.Context, yearId gen.FiscalYearId, params *gen.CarryforwardFiscalYearParams, body gen.CarryforwardFiscalYearJSONRequestBody) (*gen.CarryforwardFiscalYearResponse, error) {
	if err := c.allow("carryforwardFiscalYear"); err != nil {
		return nil, err
	}
	r, err := c.api.CarryforwardFiscalYearWithResponse(ctx, yearId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetTrialBalance(ctx context.Context, params *gen.GetTrialBalanceParams) (*gen.GetTrialBalanceResponse, error) {
	if err := c.allow("getTrialBalance"); err != nil {
		return nil, err
	}
	r, err := c.api.GetTrialBalanceWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListAccountMappings(ctx context.Context, params *gen.ListAccountMappingsParams) (*gen.ListAccountMappingsResponse, error) {
	if err := c.allow("listAccountMappings"); err != nil {
		return nil, err
	}
	r, err := c.api.ListAccountMappingsWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) PublishAccountMapping(ctx context.Context, params *gen.PublishAccountMappingParams, body gen.PublishAccountMappingJSONRequestBody) (*gen.PublishAccountMappingResponse, error) {
	if err := c.allow("publishAccountMapping"); err != nil {
		return nil, err
	}
	r, err := c.api.PublishAccountMappingWithResponse(ctx, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetAccountMapping(ctx context.Context, mappingId gen.AccountMappingId) (*gen.GetAccountMappingResponse, error) {
	if err := c.allow("getAccountMapping"); err != nil {
		return nil, err
	}
	r, err := c.api.GetAccountMappingWithResponse(ctx, mappingId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) RetireAccount(ctx context.Context, accountId gen.AccountId, params *gen.RetireAccountParams) (*gen.RetireAccountResponse, error) {
	if err := c.allow("retireAccount"); err != nil {
		return nil, err
	}
	r, err := c.api.RetireAccountWithResponse(ctx, accountId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) DownloadTenantExport(ctx context.Context) (*gen.DownloadTenantExportResponse, error) {
	if err := c.allow("downloadTenantExport"); err != nil {
		return nil, err
	}
	r, err := c.api.DownloadTenantExportWithResponse(ctx)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListTenants(ctx context.Context, params *gen.ListTenantsParams) (*gen.ListTenantsResponse, error) {
	if err := c.allow("listTenants"); err != nil {
		return nil, err
	}
	r, err := c.api.ListTenantsWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateTenant(ctx context.Context, params *gen.CreateTenantParams, body gen.CreateTenantJSONRequestBody) (*gen.CreateTenantResponse, error) {
	if err := c.allow("createTenant"); err != nil {
		return nil, err
	}
	r, err := c.api.CreateTenantWithResponse(ctx, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListMemberships(ctx context.Context, tenantId gen.TenantId, params *gen.ListMembershipsParams) (*gen.ListMembershipsResponse, error) {
	if err := c.allow("listMemberships"); err != nil {
		return nil, err
	}
	r, err := c.api.ListMembershipsWithResponse(ctx, tenantId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateMembership(ctx context.Context, tenantId gen.TenantId, params *gen.CreateMembershipParams, body gen.CreateMembershipJSONRequestBody) (*gen.CreateMembershipResponse, error) {
	if err := c.allow("createMembership"); err != nil {
		return nil, err
	}
	r, err := c.api.CreateMembershipWithResponse(ctx, tenantId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ReplaceMembership(ctx context.Context, tenantId gen.TenantId, membershipId gen.MembershipId, params *gen.ReplaceMembershipParams, body gen.ReplaceMembershipJSONRequestBody) (*gen.ReplaceMembershipResponse, error) {
	if err := c.allow("replaceMembership"); err != nil {
		return nil, err
	}
	r, err := c.api.ReplaceMembershipWithResponse(ctx, tenantId, membershipId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListAccounts(ctx context.Context, params *gen.ListAccountsParams) (*gen.ListAccountsResponse, error) {
	if err := c.allow("listAccounts"); err != nil {
		return nil, err
	}
	r, err := c.api.ListAccountsWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateAccount(ctx context.Context, params *gen.CreateAccountParams, body gen.CreateAccountJSONRequestBody) (*gen.CreateAccountResponse, error) {
	if err := c.allow("createAccount"); err != nil {
		return nil, err
	}
	r, err := c.api.CreateAccountWithResponse(ctx, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetAccount(ctx context.Context, accountId gen.AccountId) (*gen.GetAccountResponse, error) {
	if err := c.allow("getAccount"); err != nil {
		return nil, err
	}
	r, err := c.api.GetAccountWithResponse(ctx, accountId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetAccountStatement(ctx context.Context, accountId gen.AccountId, params *gen.GetAccountStatementParams) (*gen.GetAccountStatementResponse, error) {
	if err := c.allow("getAccountStatement"); err != nil {
		return nil, err
	}
	r, err := c.api.GetAccountStatementWithResponse(ctx, accountId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetAccountBalances(ctx context.Context, accountId gen.AccountId, params *gen.GetAccountBalancesParams) (*gen.GetAccountBalancesResponse, error) {
	if err := c.allow("getAccountBalances"); err != nil {
		return nil, err
	}
	r, err := c.api.GetAccountBalancesWithResponse(ctx, accountId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListPeriods(ctx context.Context, params *gen.ListPeriodsParams) (*gen.ListPeriodsResponse, error) {
	if err := c.allow("listPeriods"); err != nil {
		return nil, err
	}
	r, err := c.api.ListPeriodsWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreatePeriod(ctx context.Context, params *gen.CreatePeriodParams, body gen.CreatePeriodJSONRequestBody) (*gen.CreatePeriodResponse, error) {
	if err := c.allow("createPeriod"); err != nil {
		return nil, err
	}
	r, err := c.api.CreatePeriodWithResponse(ctx, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetPeriod(ctx context.Context, periodId gen.PeriodId) (*gen.GetPeriodResponse, error) {
	if err := c.allow("getPeriod"); err != nil {
		return nil, err
	}
	r, err := c.api.GetPeriodWithResponse(ctx, periodId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) FestschreibenPeriod(ctx context.Context, periodId gen.PeriodId, params *gen.FestschreibenPeriodParams) (*gen.FestschreibenPeriodResponse, error) {
	if err := c.allow("festschreibenPeriod"); err != nil {
		return nil, err
	}
	r, err := c.api.FestschreibenPeriodWithResponse(ctx, periodId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListJournalEntries(ctx context.Context, params *gen.ListJournalEntriesParams) (*gen.ListJournalEntriesResponse, error) {
	if err := c.allow("listJournalEntries"); err != nil {
		return nil, err
	}
	r, err := c.api.ListJournalEntriesWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateJournalEntryDraft(ctx context.Context, params *gen.CreateJournalEntryDraftParams, body gen.CreateJournalEntryDraftJSONRequestBody) (*gen.CreateJournalEntryDraftResponse, error) {
	if err := c.allow("createJournalEntryDraft"); err != nil {
		return nil, err
	}
	r, err := c.api.CreateJournalEntryDraftWithResponse(ctx, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetJournalEntry(ctx context.Context, entryId gen.EntryId) (*gen.GetJournalEntryResponse, error) {
	if err := c.allow("getJournalEntry"); err != nil {
		return nil, err
	}
	r, err := c.api.GetJournalEntryWithResponse(ctx, entryId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ReplaceJournalEntryDraft(ctx context.Context, entryId gen.EntryId, params *gen.ReplaceJournalEntryDraftParams, body gen.ReplaceJournalEntryDraftJSONRequestBody) (*gen.ReplaceJournalEntryDraftResponse, error) {
	if err := c.allow("replaceJournalEntryDraft"); err != nil {
		return nil, err
	}
	r, err := c.api.ReplaceJournalEntryDraftWithResponse(ctx, entryId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) DiscardJournalEntryDraft(ctx context.Context, entryId gen.EntryId, params *gen.DiscardJournalEntryDraftParams) (*gen.DiscardJournalEntryDraftResponse, error) {
	if err := c.allow("discardJournalEntryDraft"); err != nil {
		return nil, err
	}
	r, err := c.api.DiscardJournalEntryDraftWithResponse(ctx, entryId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 204 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) PostJournalEntry(ctx context.Context, entryId gen.EntryId, params *gen.PostJournalEntryParams) (*gen.PostJournalEntryResponse, error) {
	if err := c.allow("postJournalEntry"); err != nil {
		return nil, err
	}
	r, err := c.api.PostJournalEntryWithResponse(ctx, entryId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ReverseJournalEntry(ctx context.Context, entryId gen.EntryId, params *gen.ReverseJournalEntryParams, body gen.ReverseJournalEntryJSONRequestBody) (*gen.ReverseJournalEntryResponse, error) {
	if err := c.allow("reverseJournalEntry"); err != nil {
		return nil, err
	}
	r, err := c.api.ReverseJournalEntryWithResponse(ctx, entryId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) LinkJournalEntryDocument(ctx context.Context, entryId gen.EntryId, documentId gen.DocumentId, params *gen.LinkJournalEntryDocumentParams) (*gen.LinkJournalEntryDocumentResponse, error) {
	if err := c.allow("linkJournalEntryDocument"); err != nil {
		return nil, err
	}
	r, err := c.api.LinkJournalEntryDocumentWithResponse(ctx, entryId, documentId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 204 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListDocuments(ctx context.Context, params *gen.ListDocumentsParams) (*gen.ListDocumentsResponse, error) {
	if err := c.allow("listDocuments"); err != nil {
		return nil, err
	}
	r, err := c.api.ListDocumentsWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateDocument(ctx context.Context, params *gen.CreateDocumentParams, body gen.CreateDocumentJSONRequestBody) (*gen.CreateDocumentResponse, error) {
	if err := c.allow("createDocument"); err != nil {
		return nil, err
	}
	r, err := c.api.CreateDocumentWithResponse(ctx, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListDocumentSources(ctx context.Context, documentId gen.DocumentId) (*gen.ListDocumentSourcesResponse, error) {
	if err := c.allow("listDocumentSources"); err != nil {
		return nil, err
	}
	r, err := c.api.ListDocumentSourcesWithResponse(ctx, documentId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetDocument(ctx context.Context, documentId gen.DocumentId) (*gen.GetDocumentResponse, error) {
	if err := c.allow("getDocument"); err != nil {
		return nil, err
	}
	r, err := c.api.GetDocumentWithResponse(ctx, documentId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) DownloadDocument(ctx context.Context, documentId gen.DocumentId) (*gen.DownloadDocumentResponse, error) {
	if err := c.allow("downloadDocument"); err != nil {
		return nil, err
	}
	r, err := c.api.DownloadDocumentWithResponse(ctx, documentId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateDocumentUploadRequest(ctx context.Context, documentId gen.DocumentId, params *gen.CreateDocumentUploadRequestParams) (*gen.CreateDocumentUploadRequestResponse, error) {
	if err := c.allow("createDocumentUploadRequest"); err != nil {
		return nil, err
	}
	r, err := c.api.CreateDocumentUploadRequestWithResponse(ctx, documentId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CompleteDocument(ctx context.Context, documentId gen.DocumentId, params *gen.CompleteDocumentParams) (*gen.CompleteDocumentResponse, error) {
	if err := c.allow("completeDocument"); err != nil {
		return nil, err
	}
	r, err := c.api.CompleteDocumentWithResponse(ctx, documentId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateDocumentPreservation(ctx context.Context, documentId gen.DocumentId, params *gen.CreateDocumentPreservationParams, body gen.CreateDocumentPreservationJSONRequestBody) (*gen.CreateDocumentPreservationResponse, error) {
	if err := c.allow("createDocumentPreservation"); err != nil {
		return nil, err
	}
	r, err := c.api.CreateDocumentPreservationWithResponse(ctx, documentId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetDocumentPreservation(ctx context.Context, preservationId gen.DocumentPreservationId) (*gen.GetDocumentPreservationResponse, error) {
	if err := c.allow("getDocumentPreservation"); err != nil {
		return nil, err
	}
	r, err := c.api.GetDocumentPreservationWithResponse(ctx, preservationId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateEInvoiceValidation(ctx context.Context, documentId gen.DocumentId, params *gen.CreateEInvoiceValidationParams) (*gen.CreateEInvoiceValidationResponse, error) {
	if err := c.allow("createEInvoiceValidation"); err != nil {
		return nil, err
	}
	r, err := c.api.CreateEInvoiceValidationWithResponse(ctx, documentId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetEInvoiceValidation(ctx context.Context, validationId gen.EInvoiceValidationId) (*gen.GetEInvoiceValidationResponse, error) {
	if err := c.allow("getEInvoiceValidation"); err != nil {
		return nil, err
	}
	r, err := c.api.GetEInvoiceValidationWithResponse(ctx, validationId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateZUGFeRDPDF(ctx context.Context, validationId gen.EInvoiceValidationId, params *gen.CreateZUGFeRDPDFParams, body gen.CreateZUGFeRDPDFJSONRequestBody) (*gen.CreateZUGFeRDPDFResponse, error) {
	if err := c.allow("createZUGFeRDPDF"); err != nil {
		return nil, err
	}
	r, err := c.api.CreateZUGFeRDPDFWithResponse(ctx, validationId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetZUGFeRDPDF(ctx context.Context, zugferdPdfId gen.ZUGFeRDPDFId) (*gen.GetZUGFeRDPDFResponse, error) {
	if err := c.allow("getZUGFeRDPDF"); err != nil {
		return nil, err
	}
	r, err := c.api.GetZUGFeRDPDFWithResponse(ctx, zugferdPdfId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ListWebhookEndpoints(ctx context.Context, params *gen.ListWebhookEndpointsParams) (*gen.ListWebhookEndpointsResponse, error) {
	if err := c.allow("listWebhookEndpoints"); err != nil {
		return nil, err
	}
	r, err := c.api.ListWebhookEndpointsWithResponse(ctx, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateWebhookEndpoint(ctx context.Context, params *gen.CreateWebhookEndpointParams, body gen.CreateWebhookEndpointJSONRequestBody) (*gen.CreateWebhookEndpointResponse, error) {
	if err := c.allow("createWebhookEndpoint"); err != nil {
		return nil, err
	}
	r, err := c.api.CreateWebhookEndpointWithResponse(ctx, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetWebhookEndpoint(ctx context.Context, webhookEndpointId gen.WebhookEndpointId) (*gen.GetWebhookEndpointResponse, error) {
	if err := c.allow("getWebhookEndpoint"); err != nil {
		return nil, err
	}
	r, err := c.api.GetWebhookEndpointWithResponse(ctx, webhookEndpointId)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ReplaceWebhookEndpoint(ctx context.Context, webhookEndpointId gen.WebhookEndpointId, params *gen.ReplaceWebhookEndpointParams, body gen.ReplaceWebhookEndpointJSONRequestBody) (*gen.ReplaceWebhookEndpointResponse, error) {
	if err := c.allow("replaceWebhookEndpoint"); err != nil {
		return nil, err
	}
	r, err := c.api.ReplaceWebhookEndpointWithResponse(ctx, webhookEndpointId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) DeleteWebhookEndpoint(ctx context.Context, webhookEndpointId gen.WebhookEndpointId, params *gen.DeleteWebhookEndpointParams) (*gen.DeleteWebhookEndpointResponse, error) {
	if err := c.allow("deleteWebhookEndpoint"); err != nil {
		return nil, err
	}
	r, err := c.api.DeleteWebhookEndpointWithResponse(ctx, webhookEndpointId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 204 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) RotateWebhookEndpointSecret(ctx context.Context, webhookEndpointId gen.WebhookEndpointId, params *gen.RotateWebhookEndpointSecretParams, body gen.RotateWebhookEndpointSecretJSONRequestBody) (*gen.RotateWebhookEndpointSecretResponse, error) {
	if err := c.allow("rotateWebhookEndpointSecret"); err != nil {
		return nil, err
	}
	r, err := c.api.RotateWebhookEndpointSecretWithResponse(ctx, webhookEndpointId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 204 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}
