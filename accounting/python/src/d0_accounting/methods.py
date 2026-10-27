# Generated from the pinned Accounting public catalog. Do not edit.
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from . import generated as g


class AccountingOperations:
    def _call(self, operation: str, request: Mapping[str, Any]) -> Any:
        raise NotImplementedError

    def list_bank_sources(self, request: g.ListBankSourcesRequest) -> g.ListBankSourcesResult:
        return cast(g.ListBankSourcesResult, self._call('listBankSources', request))

    def create_bank_source(self, request: g.CreateBankSourceRequest) -> g.CreateBankSourceResult:
        return cast(g.CreateBankSourceResult, self._call('createBankSource', request))

    def get_bank_source(self, request: g.GetBankSourceRequest) -> g.GetBankSourceResult:
        return cast(g.GetBankSourceResult, self._call('getBankSource', request))

    def update_bank_source(self, request: g.UpdateBankSourceRequest) -> g.UpdateBankSourceResult:
        return cast(g.UpdateBankSourceResult, self._call('updateBankSource', request))

    def list_bank_accounts(self, request: g.ListBankAccountsRequest) -> g.ListBankAccountsResult:
        return cast(g.ListBankAccountsResult, self._call('listBankAccounts', request))

    def create_bank_account(self, request: g.CreateBankAccountRequest) -> g.CreateBankAccountResult:
        return cast(g.CreateBankAccountResult, self._call('createBankAccount', request))

    def get_bank_account(self, request: g.GetBankAccountRequest) -> g.GetBankAccountResult:
        return cast(g.GetBankAccountResult, self._call('getBankAccount', request))

    def map_bank_account(self, request: g.MapBankAccountRequest) -> g.MapBankAccountResult:
        return cast(g.MapBankAccountResult, self._call('mapBankAccount', request))

    def list_bank_account_sources(self, request: g.ListBankAccountSourcesRequest) -> g.ListBankAccountSourcesResult:
        return cast(g.ListBankAccountSourcesResult, self._call('listBankAccountSources', request))

    def create_bank_account_source(self, request: g.CreateBankAccountSourceRequest) -> g.CreateBankAccountSourceResult:
        return cast(g.CreateBankAccountSourceResult, self._call('createBankAccountSource', request))

    def get_bank_account_source(self, request: g.GetBankAccountSourceRequest) -> g.GetBankAccountSourceResult:
        return cast(g.GetBankAccountSourceResult, self._call('getBankAccountSource', request))

    def update_bank_account_source(self, request: g.UpdateBankAccountSourceRequest) -> g.UpdateBankAccountSourceResult:
        return cast(g.UpdateBankAccountSourceResult, self._call('updateBankAccountSource', request))

    def import_bank_movements(self, request: g.ImportBankMovementsRequest) -> g.ImportBankMovementsResult:
        return cast(g.ImportBankMovementsResult, self._call('importBankMovements', request))

    def list_bank_imports(self, request: g.ListBankImportsRequest) -> g.ListBankImportsResult:
        return cast(g.ListBankImportsResult, self._call('listBankImports', request))

    def get_bank_import(self, request: g.GetBankImportRequest) -> g.GetBankImportResult:
        return cast(g.GetBankImportResult, self._call('getBankImport', request))

    def list_bank_source_movements(self, request: g.ListBankSourceMovementsRequest) -> g.ListBankSourceMovementsResult:
        return cast(g.ListBankSourceMovementsResult, self._call('listBankSourceMovements', request))

    def list_bank_movements(self, request: g.ListBankMovementsRequest) -> g.ListBankMovementsResult:
        return cast(g.ListBankMovementsResult, self._call('listBankMovements', request))

    def get_bank_movement(self, request: g.GetBankMovementRequest) -> g.GetBankMovementResult:
        return cast(g.GetBankMovementResult, self._call('getBankMovement', request))

    def list_bank_observations(self, request: g.ListBankObservationsRequest) -> g.ListBankObservationsResult:
        return cast(g.ListBankObservationsResult, self._call('listBankObservations', request))

    def resolve_bank_movement(self, request: g.ResolveBankMovementRequest) -> g.ResolveBankMovementResult:
        return cast(g.ResolveBankMovementResult, self._call('resolveBankMovement', request))

    def list_bank_allocations(self, request: g.ListBankAllocationsRequest) -> g.ListBankAllocationsResult:
        return cast(g.ListBankAllocationsResult, self._call('listBankAllocations', request))

    def create_bank_allocation(self, request: g.CreateBankAllocationRequest) -> g.CreateBankAllocationResult:
        return cast(g.CreateBankAllocationResult, self._call('createBankAllocation', request))

    def get_bank_allocation(self, request: g.GetBankAllocationRequest) -> g.GetBankAllocationResult:
        return cast(g.GetBankAllocationResult, self._call('getBankAllocation', request))

    def release_bank_allocation(self, request: g.ReleaseBankAllocationRequest) -> g.ReleaseBankAllocationResult:
        return cast(g.ReleaseBankAllocationResult, self._call('releaseBankAllocation', request))

    def list_tax_rules(self, request: g.ListTaxRulesRequest) -> g.ListTaxRulesResult:
        return cast(g.ListTaxRulesResult, self._call('listTaxRules', request))

    def calculate_tax(self, request: g.CalculateTaxRequest) -> g.CalculateTaxResult:
        return cast(g.CalculateTaxResult, self._call('calculateTax', request))

    def get_financial_statements(self, request: g.GetFinancialStatementsRequest) -> g.GetFinancialStatementsResult:
        return cast(g.GetFinancialStatementsResult, self._call('getFinancialStatements', request))

    def list_fiscal_years(self, request: g.ListFiscalYearsRequest) -> g.ListFiscalYearsResult:
        return cast(g.ListFiscalYearsResult, self._call('listFiscalYears', request))

    def create_fiscal_year(self, request: g.CreateFiscalYearRequest) -> g.CreateFiscalYearResult:
        return cast(g.CreateFiscalYearResult, self._call('createFiscalYear', request))

    def get_fiscal_year(self, request: g.GetFiscalYearRequest) -> g.GetFiscalYearResult:
        return cast(g.GetFiscalYearResult, self._call('getFiscalYear', request))

    def finalize_fiscal_year(self, request: g.FinalizeFiscalYearRequest) -> g.FinalizeFiscalYearResult:
        return cast(g.FinalizeFiscalYearResult, self._call('finalizeFiscalYear', request))

    def close_fiscal_year(self, request: g.CloseFiscalYearRequest) -> g.CloseFiscalYearResult:
        return cast(g.CloseFiscalYearResult, self._call('closeFiscalYear', request))

    def carryforward_fiscal_year(self, request: g.CarryforwardFiscalYearRequest) -> g.CarryforwardFiscalYearResult:
        return cast(g.CarryforwardFiscalYearResult, self._call('carryforwardFiscalYear', request))

    def get_trial_balance(self, request: g.GetTrialBalanceRequest) -> g.GetTrialBalanceResult:
        return cast(g.GetTrialBalanceResult, self._call('getTrialBalance', request))

    def list_account_mappings(self, request: g.ListAccountMappingsRequest) -> g.ListAccountMappingsResult:
        return cast(g.ListAccountMappingsResult, self._call('listAccountMappings', request))

    def publish_account_mapping(self, request: g.PublishAccountMappingRequest) -> g.PublishAccountMappingResult:
        return cast(g.PublishAccountMappingResult, self._call('publishAccountMapping', request))

    def get_account_mapping(self, request: g.GetAccountMappingRequest) -> g.GetAccountMappingResult:
        return cast(g.GetAccountMappingResult, self._call('getAccountMapping', request))

    def retire_account(self, request: g.RetireAccountRequest) -> g.RetireAccountResult:
        return cast(g.RetireAccountResult, self._call('retireAccount', request))

    def download_tenant_export(self, request: g.DownloadTenantExportRequest) -> g.DownloadTenantExportResult:
        return cast(g.DownloadTenantExportResult, self._call('downloadTenantExport', request))

    def list_tenants(self, request: g.ListTenantsRequest) -> g.ListTenantsResult:
        return cast(g.ListTenantsResult, self._call('listTenants', request))

    def create_tenant(self, request: g.CreateTenantRequest) -> g.CreateTenantResult:
        return cast(g.CreateTenantResult, self._call('createTenant', request))

    def list_memberships(self, request: g.ListMembershipsRequest) -> g.ListMembershipsResult:
        return cast(g.ListMembershipsResult, self._call('listMemberships', request))

    def create_membership(self, request: g.CreateMembershipRequest) -> g.CreateMembershipResult:
        return cast(g.CreateMembershipResult, self._call('createMembership', request))

    def replace_membership(self, request: g.ReplaceMembershipRequest) -> g.ReplaceMembershipResult:
        return cast(g.ReplaceMembershipResult, self._call('replaceMembership', request))

    def list_accounts(self, request: g.ListAccountsRequest) -> g.ListAccountsResult:
        return cast(g.ListAccountsResult, self._call('listAccounts', request))

    def create_account(self, request: g.CreateAccountRequest) -> g.CreateAccountResult:
        return cast(g.CreateAccountResult, self._call('createAccount', request))

    def get_account(self, request: g.GetAccountRequest) -> g.GetAccountResult:
        return cast(g.GetAccountResult, self._call('getAccount', request))

    def get_account_statement(self, request: g.GetAccountStatementRequest) -> g.GetAccountStatementResult:
        return cast(g.GetAccountStatementResult, self._call('getAccountStatement', request))

    def get_account_balances(self, request: g.GetAccountBalancesRequest) -> g.GetAccountBalancesResult:
        return cast(g.GetAccountBalancesResult, self._call('getAccountBalances', request))

    def list_periods(self, request: g.ListPeriodsRequest) -> g.ListPeriodsResult:
        return cast(g.ListPeriodsResult, self._call('listPeriods', request))

    def create_period(self, request: g.CreatePeriodRequest) -> g.CreatePeriodResult:
        return cast(g.CreatePeriodResult, self._call('createPeriod', request))

    def get_period(self, request: g.GetPeriodRequest) -> g.GetPeriodResult:
        return cast(g.GetPeriodResult, self._call('getPeriod', request))

    def festschreiben_period(self, request: g.FestschreibenPeriodRequest) -> g.FestschreibenPeriodResult:
        return cast(g.FestschreibenPeriodResult, self._call('festschreibenPeriod', request))

    def list_journal_entries(self, request: g.ListJournalEntriesRequest) -> g.ListJournalEntriesResult:
        return cast(g.ListJournalEntriesResult, self._call('listJournalEntries', request))

    def create_journal_entry_draft(self, request: g.CreateJournalEntryDraftRequest) -> g.CreateJournalEntryDraftResult:
        return cast(g.CreateJournalEntryDraftResult, self._call('createJournalEntryDraft', request))

    def get_journal_entry(self, request: g.GetJournalEntryRequest) -> g.GetJournalEntryResult:
        return cast(g.GetJournalEntryResult, self._call('getJournalEntry', request))

    def replace_journal_entry_draft(self, request: g.ReplaceJournalEntryDraftRequest) -> g.ReplaceJournalEntryDraftResult:
        return cast(g.ReplaceJournalEntryDraftResult, self._call('replaceJournalEntryDraft', request))

    def discard_journal_entry_draft(self, request: g.DiscardJournalEntryDraftRequest) -> g.DiscardJournalEntryDraftResult:
        return cast(g.DiscardJournalEntryDraftResult, self._call('discardJournalEntryDraft', request))

    def post_journal_entry(self, request: g.PostJournalEntryRequest) -> g.PostJournalEntryResult:
        return cast(g.PostJournalEntryResult, self._call('postJournalEntry', request))

    def reverse_journal_entry(self, request: g.ReverseJournalEntryRequest) -> g.ReverseJournalEntryResult:
        return cast(g.ReverseJournalEntryResult, self._call('reverseJournalEntry', request))

    def link_journal_entry_document(self, request: g.LinkJournalEntryDocumentRequest) -> g.LinkJournalEntryDocumentResult:
        return cast(g.LinkJournalEntryDocumentResult, self._call('linkJournalEntryDocument', request))

    def list_documents(self, request: g.ListDocumentsRequest) -> g.ListDocumentsResult:
        return cast(g.ListDocumentsResult, self._call('listDocuments', request))

    def create_document(self, request: g.CreateDocumentRequest) -> g.CreateDocumentResult:
        return cast(g.CreateDocumentResult, self._call('createDocument', request))

    def list_document_sources(self, request: g.ListDocumentSourcesRequest) -> g.ListDocumentSourcesResult:
        return cast(g.ListDocumentSourcesResult, self._call('listDocumentSources', request))

    def get_document(self, request: g.GetDocumentRequest) -> g.GetDocumentResult:
        return cast(g.GetDocumentResult, self._call('getDocument', request))

    def download_document(self, request: g.DownloadDocumentRequest) -> g.DownloadDocumentResult:
        return cast(g.DownloadDocumentResult, self._call('downloadDocument', request))

    def create_document_upload_request(self, request: g.CreateDocumentUploadRequestRequest) -> g.CreateDocumentUploadRequestResult:
        return cast(g.CreateDocumentUploadRequestResult, self._call('createDocumentUploadRequest', request))

    def complete_document(self, request: g.CompleteDocumentRequest) -> g.CompleteDocumentResult:
        return cast(g.CompleteDocumentResult, self._call('completeDocument', request))

    def create_document_preservation(self, request: g.CreateDocumentPreservationRequest) -> g.CreateDocumentPreservationResult:
        return cast(g.CreateDocumentPreservationResult, self._call('createDocumentPreservation', request))

    def get_document_preservation(self, request: g.GetDocumentPreservationRequest) -> g.GetDocumentPreservationResult:
        return cast(g.GetDocumentPreservationResult, self._call('getDocumentPreservation', request))

    def create_e_invoice_validation(self, request: g.CreateEInvoiceValidationRequest) -> g.CreateEInvoiceValidationResult:
        return cast(g.CreateEInvoiceValidationResult, self._call('createEInvoiceValidation', request))

    def get_e_invoice_validation(self, request: g.GetEInvoiceValidationRequest) -> g.GetEInvoiceValidationResult:
        return cast(g.GetEInvoiceValidationResult, self._call('getEInvoiceValidation', request))

    def create_zugferd_pdf(self, request: g.CreateZUGFeRDPDFRequest) -> g.CreateZUGFeRDPDFResult:
        return cast(g.CreateZUGFeRDPDFResult, self._call('createZUGFeRDPDF', request))

    def get_zugferd_pdf(self, request: g.GetZUGFeRDPDFRequest) -> g.GetZUGFeRDPDFResult:
        return cast(g.GetZUGFeRDPDFResult, self._call('getZUGFeRDPDF', request))

    def list_webhook_endpoints(self, request: g.ListWebhookEndpointsRequest) -> g.ListWebhookEndpointsResult:
        return cast(g.ListWebhookEndpointsResult, self._call('listWebhookEndpoints', request))

    def create_webhook_endpoint(self, request: g.CreateWebhookEndpointRequest) -> g.CreateWebhookEndpointResult:
        return cast(g.CreateWebhookEndpointResult, self._call('createWebhookEndpoint', request))

    def get_webhook_endpoint(self, request: g.GetWebhookEndpointRequest) -> g.GetWebhookEndpointResult:
        return cast(g.GetWebhookEndpointResult, self._call('getWebhookEndpoint', request))

    def replace_webhook_endpoint(self, request: g.ReplaceWebhookEndpointRequest) -> g.ReplaceWebhookEndpointResult:
        return cast(g.ReplaceWebhookEndpointResult, self._call('replaceWebhookEndpoint', request))

    def delete_webhook_endpoint(self, request: g.DeleteWebhookEndpointRequest) -> g.DeleteWebhookEndpointResult:
        return cast(g.DeleteWebhookEndpointResult, self._call('deleteWebhookEndpoint', request))

    def rotate_webhook_endpoint_secret(self, request: g.RotateWebhookEndpointSecretRequest) -> g.RotateWebhookEndpointSecretResult:
        return cast(g.RotateWebhookEndpointSecretResult, self._call('rotateWebhookEndpointSecret', request))
