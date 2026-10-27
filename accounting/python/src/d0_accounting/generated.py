# Generated from the pinned Accounting public catalog. Do not edit.
from __future__ import annotations

from typing import Any, Literal, NotRequired, TypedDict


class Event(TypedDict):
    schema: Literal['devacc.event.v1']
    event_id: EventId
    tenant_id: str
    type: Literal['journal_entry.posted']
    occurred_at: str
    resource: dict[str, Any]
    entry_hash: NotRequired[str]

type EventId = str
class AsyncEvent(TypedDict):
    schema: Literal['devacc.async-event.v1']
    event_id: EventId
    tenant_id: str
    type: Literal['document.archived', 'document.preservation.applied', 'einvoice.validation.succeeded', 'einvoice.validation.failed', 'einvoice.zugferd-pdf.succeeded', 'einvoice.zugferd-pdf.failed']
    occurred_at: str
    resource: dict[str, Any]

class Problem(TypedDict):
    type: str
    title: str
    status: int
    detail: NotRequired[str]
    instance: NotRequired[str]
    errors: NotRequired[list[dict[str, Any]]]

class WebhookEndpointSecretReplace(TypedDict):
    secret: WebhookEndpointSecret

type WebhookEndpointSecret = str
type WebhookEndpointId = str
class WebhookEndpoint(TypedDict):
    id: WebhookEndpointId
    url: WebhookEndpointURL
    eventTypes: WebhookEndpointEventTypes
    active: bool
    createdAt: str
    updatedAt: str

type WebhookEndpointEventTypes = list[WebhookEventType]
type WebhookEventType = Literal['journal_entry.posted']
type WebhookEndpointURL = str
class WebhookEndpointReplace(TypedDict):
    url: WebhookEndpointURL
    eventTypes: WebhookEndpointEventTypes
    active: bool

class WebhookEndpointCreate(TypedDict):
    url: WebhookEndpointURL
    eventTypes: WebhookEndpointEventTypes
    secret: WebhookEndpointSecret

class WebhookEndpointPage(TypedDict):
    data: list[WebhookEndpoint]
    nextCursor: NotRequired[WebhookEndpointId]

type ZUGFeRDPDF = ZUGFeRDPDFPending | ZUGFeRDPDFCompleted | ZUGFeRDPDFFailed
class ZUGFeRDPDFFailed(TypedDict):
    id: ZUGFeRDPDFId
    validationId: EInvoiceValidationId
    invoiceDocumentId: DocumentId
    visualDocumentId: DocumentId
    target: ZUGFeRDPDFStandard
    recipe: ZUGFeRDPDFRecipe
    status: Literal['failed']
    requestedAt: str
    completedAt: str
    failure: ZUGFeRDPDFFailure

class ZUGFeRDPDFFailure(TypedDict):
    code: Literal['unsupported-source', 'generation-capacity-exceeded']

class ZUGFeRDPDFRecipe(TypedDict):
    name: str
    version: str

class ZUGFeRDPDFStandard(TypedDict):
    name: str
    version: str
    profile: str

type DocumentId = str
type EInvoiceValidationId = str
type ZUGFeRDPDFId = str
class ZUGFeRDPDFCompleted(TypedDict):
    id: ZUGFeRDPDFId
    validationId: EInvoiceValidationId
    invoiceDocumentId: DocumentId
    visualDocumentId: DocumentId
    target: ZUGFeRDPDFStandard
    recipe: ZUGFeRDPDFRecipe
    status: Literal['completed']
    requestedAt: str
    completedAt: str
    outputDocument: ZUGFeRDPDFDocument
    result: ZUGFeRDPDFResult

class ZUGFeRDPDFResult(TypedDict):
    schema: Literal['devacc.einvoice.zugferd-pdf.v1']
    invoiceSha256: str
    visualSha256: str
    output: ZUGFeRDPDFOutput
    standard: ZUGFeRDPDFStandard
    recipe: ZUGFeRDPDFRecipe
    processor: ZUGFeRDPDFComponent
    ruleset: ZUGFeRDPDFComponent

class ZUGFeRDPDFComponent(TypedDict):
    name: str
    version: str

class ZUGFeRDPDFOutput(TypedDict):
    contentId: Literal['output']
    mediaType: Literal['application/pdf']
    sizeBytes: int
    sha256: str
    pdfConformance: str
    embeddedFilename: str

class ZUGFeRDPDFDocument(TypedDict):
    id: DocumentId
    origin: Literal['derived']
    status: Literal['archived']
    originalFilename: str
    mediaType: Literal['application/pdf']
    sizeBytes: int
    contentSha256: str
    documentDate: str
    classification: str
    retentionUntil: str
    createdAt: str
    archivedAt: str

class ZUGFeRDPDFPending(TypedDict):
    id: ZUGFeRDPDFId
    validationId: EInvoiceValidationId
    invoiceDocumentId: DocumentId
    visualDocumentId: DocumentId
    target: ZUGFeRDPDFStandard
    recipe: ZUGFeRDPDFRecipe
    status: Literal['pending']
    requestedAt: str

class ZUGFeRDPDFCreate(TypedDict):
    visualDocumentId: DocumentId

type EInvoiceValidation = EInvoiceValidationPending | EInvoiceValidationCompleted | EInvoiceValidationFailed
class EInvoiceValidationFailed(TypedDict):
    id: EInvoiceValidationId
    documentId: DocumentId
    status: Literal['failed']
    requestedAt: str
    completedAt: str
    failure: EInvoiceValidationFailure

class EInvoiceValidationFailure(TypedDict):
    code: Literal['validation-processing-failed']

class EInvoiceValidationCompleted(TypedDict):
    id: EInvoiceValidationId
    documentId: DocumentId
    status: Literal['completed']
    requestedAt: str
    completedAt: str
    result: EInvoiceValidationResult

class EInvoiceValidationResult(TypedDict):
    schema: Literal['devacc.einvoice.validation.v1']
    sourceSha256: str
    valid: bool
    syntax: Literal['ubl', 'cii', 'unknown']
    profile: NotRequired[str]
    validator: EInvoiceValidationComponent
    ruleset: EInvoiceValidationComponent
    issues: list[EInvoiceValidationIssue]

class EInvoiceValidationIssue(TypedDict):
    severity: Literal['error', 'warning', 'information']
    code: str
    message: str
    location: NotRequired[str]

class EInvoiceValidationComponent(TypedDict):
    name: str
    version: str

class EInvoiceValidationPending(TypedDict):
    id: EInvoiceValidationId
    documentId: DocumentId
    status: Literal['pending']
    requestedAt: str

class DocumentPreservation(TypedDict):
    id: DocumentPreservationId
    documentId: DocumentId
    requestedBy: MembershipId
    requestedAt: str
    reason: str
    retainUntil: NotRequired[str]
    legalHold: bool
    status: Literal['pending', 'applied']
    nextAttemptAt: NotRequired[str]
    failureCode: NotRequired[Literal['archive-unavailable', 'source-integrity-mismatch', 'protection-unconfirmed']]
    appliedAt: NotRequired[str]
    observedRetainUntil: NotRequired[str]
    observedLegalHold: NotRequired[bool]

type MembershipId = str
type DocumentPreservationId = str
class DocumentPreservationCreate(TypedDict):
    reason: str
    retainUntil: NotRequired[str]
    legalHold: NotRequired[Literal[True]]

class Document(TypedDict):
    id: DocumentId
    origin: DocumentOrigin
    status: DocumentStatus
    originalFilename: str
    mediaType: str
    sizeBytes: int
    contentSha256: str
    documentDate: str
    classification: str
    retentionUntil: str
    createdAt: str
    archivedAt: str | None

type DocumentStatus = Literal['pending', 'archived']
type DocumentOrigin = Literal['uploaded', 'derived']
class DocumentUploadRequest(TypedDict):
    url: str
    method: Literal['PUT']
    headers: dict[str, Any]
    expiresAt: str

class DocumentSourceList(TypedDict):
    data: list[DocumentSource]

class DocumentSource(TypedDict):
    documentId: DocumentId
    role: Literal['invoice', 'visual']
    kind: Literal['zugferd-pdf']

class DocumentCreateResult(TypedDict):
    document: Document
    upload: DocumentUploadRequest

class DocumentCreate(TypedDict):
    originalFilename: str
    mediaType: str
    sizeBytes: int
    contentSha256: str
    documentDate: str

class DocumentPage(TypedDict):
    data: list[Document]
    nextCursor: NotRequired[DocumentId]

type EntryId = str
class JournalEntry(TypedDict):
    bookingText: NotRequired[str | None]
    externalReference: NotRequired[str | None]
    id: EntryId
    periodId: PeriodId
    status: JournalEntryStatus
    bookingDate: str
    currency: Currency
    seq: NotRequired[int | None]
    entryHash: NotRequired[str | None]
    reversalOf: NotRequired[EntryId]
    lines: list[JournalLine]
    createdAt: str
    postedAt: NotRequired[str | None]

class JournalLine(TypedDict):
    taxRuleId: NotRequired[str]
    lineNo: int
    accountId: AccountId
    accountNo: str
    side: Side
    amount: Money
    taxKey: NotRequired[str | None]

class Money(TypedDict):
    amount: str
    currency: Currency

type Currency = str
type Side = Literal['debit', 'credit']
type AccountId = str
type JournalEntryStatus = Literal['draft', 'posted']
type PeriodId = str
class JournalEntryReversalCreate(TypedDict):
    periodId: PeriodId
    bookingDate: str

class JournalEntryCreate(TypedDict):
    bookingText: NotRequired[str | None]
    externalReference: NotRequired[str | None]
    periodId: PeriodId
    bookingDate: str
    currency: Currency
    lines: list[JournalLineCreate]

class JournalLineCreate(TypedDict):
    taxRuleId: NotRequired[str]
    accountId: AccountId
    side: Side
    amount: Money
    taxKey: NotRequired[str | None]

class JournalEntryPage(TypedDict):
    data: list[JournalEntry]
    nextCursor: NotRequired[EntryId]

class Period(TypedDict):
    id: PeriodId
    label: str
    startsOn: str
    endsOn: str
    status: PeriodStatus
    festgeschriebenAt: NotRequired[str | None]
    createdAt: str

type PeriodStatus = Literal['open', 'festgeschrieben']
class PeriodCreate(TypedDict):
    label: str
    startsOn: str
    endsOn: str

class PeriodPage(TypedDict):
    data: list[Period]
    nextCursor: NotRequired[PeriodId]

class AccountBalances(TypedDict):
    accountId: AccountId
    asOf: PostingSnapshot
    data: list[AccountBalance]

class AccountBalance(TypedDict):
    currency: Currency
    openingBalance: Money
    debitTotal: Money
    creditTotal: Money
    closingBalance: Money

type PostingSnapshot = str
class AccountStatementPage(TypedDict):
    accountId: AccountId
    asOf: PostingSnapshot
    data: list[AccountMovement]
    nextCursor: NotRequired[AccountStatementCursor]

type AccountStatementCursor = str
class AccountMovement(TypedDict):
    taxRuleId: NotRequired[str]
    bookingText: NotRequired[str | None]
    externalReference: NotRequired[str | None]
    entryId: EntryId
    seq: int
    lineNo: int
    bookingDate: str
    periodId: PeriodId
    accountNo: str
    side: Side
    amount: Money
    taxKey: str | None
    reversalOf: NotRequired[EntryId]

class Account(TypedDict):
    retiredAt: NotRequired[str | None]
    id: AccountId
    accountNo: str
    name: str
    accountType: NotRequired[str | None]
    createdAt: str

class AccountCreate(TypedDict):
    accountNo: str
    name: str
    accountType: NotRequired[str | None]

class AccountPage(TypedDict):
    data: list[Account]
    nextCursor: NotRequired[AccountId]

class Membership(TypedDict):
    id: MembershipId
    subject: str
    permissions: AccessPermissions
    status: MembershipStatus
    revision: int
    createdAt: str

type MembershipStatus = Literal['active', 'inactive']
type AccessPermissions = list[AccessPermission]
type AccessPermission = Literal['accounting.read', 'accounting.write', 'documents.read', 'documents.write', 'periods.close', 'webhooks.manage', 'access.manage', 'exports.read', 'audit.read', 'banking.read', 'banking.manage', 'banking.ingest', 'banking.reconcile']
class MembershipReplace(TypedDict):
    permissions: AccessPermissions
    status: MembershipStatus
    expectedRevision: int

type TenantId = str
class MembershipCreate(TypedDict):
    subject: str
    permissions: AccessPermissions

class MembershipPage(TypedDict):
    data: list[Membership]
    nextCursor: NotRequired[MembershipId]

class Tenant(TypedDict):
    id: TenantId
    name: str
    createdAt: str

class TenantCreate(TypedDict):
    name: str

class TenantPage(TypedDict):
    data: list[Tenant]
    nextCursor: NotRequired[TenantId]

class AccountMapping(TypedDict):
    id: AccountMappingId
    version: int
    digest: str
    createdAt: str
    items: list[AccountMappingItem]

class AccountMappingItem(TypedDict):
    accountId: AccountId
    accountNo: str
    accountName: str
    classification: AccountClassification
    reportCode: str
    reportName: str

type AccountClassification = Literal['asset', 'liability', 'equity', 'income', 'expense']
type AccountMappingId = str
class AccountMappingCreate(TypedDict):
    items: list[AccountMappingInputItem]

class AccountMappingInputItem(TypedDict):
    accountId: AccountId
    classification: AccountClassification
    reportCode: str
    reportName: str

class AccountMappingPage(TypedDict):
    data: list[AccountMappingSummary]
    nextCursor: NotRequired[AccountMappingId]

class AccountMappingSummary(TypedDict):
    id: AccountMappingId
    version: int
    digest: str
    createdAt: str

class TrialBalance(TypedDict):
    asOf: PostingSnapshot
    data: list[TrialBalanceRow]
    totals: list[AccountBalance]

class TrialBalanceRow(TypedDict):
    accountId: AccountId
    accountNo: str
    currency: Currency
    openingBalance: Money
    debitTotal: Money
    creditTotal: Money
    closingBalance: Money

class FiscalYearCarryforward(TypedDict):
    targetYearId: FiscalYearId
    targetPeriodId: PeriodId
    mappingRevisionId: AccountMappingId
    resultAccountId: AccountId
    documentId: DocumentId
    currency: str

type FiscalYearId = str
class FiscalYearCloseResult(TypedDict):
    entries: list[JournalEntry]
    period: Period

class FiscalYearClose(TypedDict):
    periodId: PeriodId
    mappingRevisionId: AccountMappingId
    resultAccountId: AccountId
    documentId: DocumentId

class FiscalYear(TypedDict):
    id: FiscalYearId
    label: str
    startsOn: str
    endsOn: str
    status: FiscalYearStatus
    finalizedAt: NotRequired[str | None]
    createdAt: str

type FiscalYearStatus = Literal['open', 'finalized']
class FiscalYearCreate(TypedDict):
    label: str
    startsOn: str
    endsOn: str

class FiscalYearPage(TypedDict):
    data: list[FiscalYear]
    nextCursor: NotRequired[FiscalYearId]

class FinancialStatements(TypedDict):
    asOf: PostingSnapshot
    fiscalYearId: FiscalYearId
    mappingRevisionId: AccountMappingId
    mappingDigest: str
    bookingDateFrom: str
    bookingDateTo: str
    closingEntryIds: list[EntryId]
    data: list[FinancialStatementGroup]
    totals: list[FinancialStatementTotals]

class FinancialStatementTotals(TypedDict):
    currency: Currency
    assets: Money
    liabilities: Money
    equity: Money
    income: Money
    expense: Money
    result: Money
    balanceDifference: Money

class FinancialStatementGroup(TypedDict):
    classification: AccountClassification
    reportCode: str
    reportName: str
    amount: Money
    accounts: list[FinancialStatementAccount]

class FinancialStatementAccount(TypedDict):
    accountId: AccountId
    accountNo: str
    accountName: str
    amount: Money

class TaxCalculation(TypedDict):
    tax: Money
    evidence: TaxRule

class TaxRule(TypedDict):
    id: str
    taxKey: str
    effectiveFrom: str
    effectiveUntil: str | None
    rateNumerator: str
    rateDenominator: str
    sourceVersion: str
    artifactSha256: str

class TaxCalculationInput(TypedDict):
    taxRuleId: str
    bookingDate: str
    net: Money

class TaxRulePage(TypedDict):
    data: list[TaxRule]
    nextCursor: str | None

class BankAllocationRelease(TypedDict):
    reason: str

class BankAllocation(TypedDict):
    id: BankAllocationId
    movementId: BankMovementId
    movementRevision: int
    entryId: EntryId
    lineNo: int
    amountCents: str
    createdAt: str
    releasedAt: str | None
    releaseReason: str | None
    stale: bool

type BankMovementId = str
type BankAllocationId = str
class BankAllocationCreate(TypedDict):
    expectedReviewRevision: int
    expectedRevision: int
    entryId: EntryId
    lineNo: int
    amountCents: str

class BankAllocationPage(TypedDict):
    data: list[BankAllocation]
    nextCursor: str | None

class BankResolution(TypedDict):
    expectedReviewRevision: int
    expectedRevision: int
    duplicateOf: NotRequired[str | None]
    supersedes: NotRequired[str | None]
    reason: str

class BankMovement(TypedDict):
    reviewRevision: int
    id: BankMovementId
    aliasId: BankAccountSourceId
    accountId: BankAccountId
    sourceReference: str
    status: Literal['pending', 'booked', 'cancelled']
    amountCents: str
    currency: Currency
    bookingDate: str | None
    valueDate: str | None
    remittance: str | None
    counterparty: str | None
    bankReference: str | None
    provenance: dict[str, Any]
    revision: int
    observedAt: str
    receivedAt: str
    reviewRequired: bool
    duplicateOf: str | None
    supersededBy: str | None
    reconciliationStale: bool

type BankAccountId = str
type BankAccountSourceId = str
class BankObservationPage(TypedDict):
    data: list[BankObservation]
    nextCursor: str | None

class BankObservation(TypedDict):
    id: BankMovementId
    aliasId: BankAccountSourceId
    accountId: BankAccountId
    batchId: BankBatchId
    sourceReference: str
    status: Literal['pending', 'booked', 'cancelled']
    amountCents: str
    currency: Currency
    bookingDate: str | None
    valueDate: str | None
    remittance: str | None
    counterparty: str | None
    bankReference: str | None
    provenance: dict[str, Any]
    revision: int
    observedAt: str
    receivedAt: str

type BankBatchId = str
type BankObservationId = str
class BankMovementPage(TypedDict):
    data: list[BankMovement]
    nextCursor: str | None

class BankBatch(TypedDict):
    id: BankBatchId
    aliasId: BankAccountSourceId
    reference: str
    observedAt: str
    successfulSyncAt: str | None
    coverageFrom: str | None
    coverageTo: str | None
    complete: bool
    error: str | None
    receivedAt: str

class BankBatchPage(TypedDict):
    data: list[BankBatch]
    nextCursor: str | None

class BankImport(TypedDict):
    reference: str
    observedAt: str
    successfulSyncAt: NotRequired[str | None]
    coverageFrom: NotRequired[str | None]
    coverageTo: NotRequired[str | None]
    complete: bool
    error: NotRequired[str | None]
    movements: list[BankMovementInput]

class BankMovementInput(TypedDict):
    expectedRevision: int
    sourceReference: str
    status: Literal['pending', 'booked', 'cancelled']
    amountCents: str
    currency: Currency
    bookingDate: NotRequired[str | None]
    valueDate: NotRequired[str | None]
    remittance: NotRequired[str | None]
    counterparty: NotRequired[str | None]
    bankReference: NotRequired[str | None]
    provenance: NotRequired[dict[str, Any]]

class BankAccountSourceUpdate(TypedDict):
    active: bool
    expectedRevision: int

class BankAccountSource(TypedDict):
    id: BankAccountSourceId
    accountId: BankAccountId
    sourceId: BankSourceId
    externalAccountRef: str
    active: bool
    revision: int
    createdAt: str

type BankSourceId = str
class BankAccountSourceCreate(TypedDict):
    sourceId: BankSourceId
    externalAccountRef: str

class BankAccountSourcePage(TypedDict):
    data: list[BankAccountSource]
    nextCursor: str | None

class BankAccountMapping(TypedDict):
    ledgerAccountId: str | None
    expectedRevision: int

class BankAccount(TypedDict):
    id: BankAccountId
    name: str
    currency: Currency
    ledgerAccountId: str | None
    revision: int
    createdAt: str

class BankAccountCreate(TypedDict):
    name: str
    currency: Currency
    ledgerAccountId: NotRequired[str | None]

class BankAccountPage(TypedDict):
    data: list[BankAccount]
    nextCursor: str | None

class BankSourceUpdate(TypedDict):
    writerMembershipId: MembershipId
    active: bool
    expectedRevision: int

class BankSource(TypedDict):
    id: BankSourceId
    name: str
    writerMembershipId: MembershipId
    active: bool
    revision: int
    createdAt: str

class BankSourceCreate(TypedDict):
    name: str
    writerMembershipId: MembershipId

class BankSourcePage(TypedDict):
    data: list[BankSource]
    nextCursor: str | None

class ListBankSourcesRequest(TypedDict):
    limit: NotRequired[int]
    after: NotRequired[BankSourceId]

type ListBankSourcesResult = BankSourcePage

class CreateBankSourceRequest(TypedDict):
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: BankSourceCreate

type CreateBankSourceResult = BankSource

class GetBankSourceRequest(TypedDict):
    sourceId: BankSourceId

type GetBankSourceResult = BankSource

class UpdateBankSourceRequest(TypedDict):
    sourceId: BankSourceId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: BankSourceUpdate

type UpdateBankSourceResult = BankSource

class ListBankAccountsRequest(TypedDict):
    limit: NotRequired[int]
    after: NotRequired[BankAccountId]

type ListBankAccountsResult = BankAccountPage

class CreateBankAccountRequest(TypedDict):
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: BankAccountCreate

type CreateBankAccountResult = BankAccount

class GetBankAccountRequest(TypedDict):
    bankAccountId: BankAccountId

type GetBankAccountResult = BankAccount

class MapBankAccountRequest(TypedDict):
    bankAccountId: BankAccountId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: BankAccountMapping

type MapBankAccountResult = BankAccount

class ListBankAccountSourcesRequest(TypedDict):
    bankAccountId: BankAccountId
    limit: NotRequired[int]
    after: NotRequired[BankAccountSourceId]

type ListBankAccountSourcesResult = BankAccountSourcePage

class CreateBankAccountSourceRequest(TypedDict):
    bankAccountId: BankAccountId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: BankAccountSourceCreate

type CreateBankAccountSourceResult = BankAccountSource

class GetBankAccountSourceRequest(TypedDict):
    aliasId: BankAccountSourceId

type GetBankAccountSourceResult = BankAccountSource

class UpdateBankAccountSourceRequest(TypedDict):
    aliasId: BankAccountSourceId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: BankAccountSourceUpdate

type UpdateBankAccountSourceResult = BankAccountSource

class ImportBankMovementsRequest(TypedDict):
    aliasId: BankAccountSourceId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: BankImport

type ImportBankMovementsResult = BankBatch

class ListBankImportsRequest(TypedDict):
    aliasId: BankAccountSourceId
    limit: NotRequired[int]
    after: NotRequired[BankBatchId]

type ListBankImportsResult = BankBatchPage

class GetBankImportRequest(TypedDict):
    batchId: BankBatchId

type GetBankImportResult = BankBatch

class ListBankSourceMovementsRequest(TypedDict):
    aliasId: BankAccountSourceId
    limit: NotRequired[int]
    after: NotRequired[BankMovementId]

type ListBankSourceMovementsResult = BankMovementPage

class ListBankMovementsRequest(TypedDict):
    bankAccountId: BankAccountId
    limit: NotRequired[int]
    after: NotRequired[BankMovementId]

type ListBankMovementsResult = BankMovementPage

class GetBankMovementRequest(TypedDict):
    movementId: BankMovementId

type GetBankMovementResult = BankMovement

class ListBankObservationsRequest(TypedDict):
    movementId: BankMovementId
    limit: NotRequired[int]
    after: NotRequired[BankObservationId]

type ListBankObservationsResult = BankObservationPage

class ResolveBankMovementRequest(TypedDict):
    movementId: BankMovementId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: BankResolution

type ResolveBankMovementResult = BankMovement

class ListBankAllocationsRequest(TypedDict):
    movementId: BankMovementId
    limit: NotRequired[int]
    after: NotRequired[BankAllocationId]

type ListBankAllocationsResult = BankAllocationPage

class CreateBankAllocationRequest(TypedDict):
    movementId: BankMovementId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: BankAllocationCreate

type CreateBankAllocationResult = BankAllocation

class GetBankAllocationRequest(TypedDict):
    allocationId: BankAllocationId

type GetBankAllocationResult = BankAllocation

class ReleaseBankAllocationRequest(TypedDict):
    allocationId: BankAllocationId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: BankAllocationRelease

type ReleaseBankAllocationResult = BankAllocation

class ListTaxRulesRequest(TypedDict):
    limit: NotRequired[int]
    after: NotRequired[str]

type ListTaxRulesResult = TaxRulePage

class CalculateTaxRequest(TypedDict):
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: TaxCalculationInput

type CalculateTaxResult = TaxCalculation

class GetFinancialStatementsRequest(TypedDict):
    fiscalYearId: FiscalYearId
    mappingRevisionId: AccountMappingId
    asOf: NotRequired[PostingSnapshot]
    currency: NotRequired[Currency]

type GetFinancialStatementsResult = FinancialStatements

class ListFiscalYearsRequest(TypedDict):
    limit: NotRequired[int]
    after: NotRequired[FiscalYearId]

type ListFiscalYearsResult = FiscalYearPage

class CreateFiscalYearRequest(TypedDict):
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: FiscalYearCreate

type CreateFiscalYearResult = FiscalYear

class GetFiscalYearRequest(TypedDict):
    yearId: FiscalYearId

type GetFiscalYearResult = FiscalYear

class FinalizeFiscalYearRequest(TypedDict):
    yearId: FiscalYearId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]

type FinalizeFiscalYearResult = FiscalYear

class CloseFiscalYearRequest(TypedDict):
    yearId: FiscalYearId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: FiscalYearClose

type CloseFiscalYearResult = FiscalYearCloseResult

class CarryforwardFiscalYearRequest(TypedDict):
    yearId: FiscalYearId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: FiscalYearCarryforward

type CarryforwardFiscalYearResult = JournalEntry

class GetTrialBalanceRequest(TypedDict):
    asOf: NotRequired[PostingSnapshot]
    currency: NotRequired[Currency]
    bookingDateFrom: NotRequired[str]
    bookingDateTo: NotRequired[str]

type GetTrialBalanceResult = TrialBalance

class ListAccountMappingsRequest(TypedDict):
    limit: NotRequired[int]
    after: NotRequired[AccountMappingId]

type ListAccountMappingsResult = AccountMappingPage

class PublishAccountMappingRequest(TypedDict):
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: AccountMappingCreate

type PublishAccountMappingResult = AccountMapping

class GetAccountMappingRequest(TypedDict):
    mappingId: AccountMappingId

type GetAccountMappingResult = AccountMapping

class RetireAccountRequest(TypedDict):
    accountId: AccountId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]

type RetireAccountResult = Account

class DownloadTenantExportRequest(TypedDict):
    pass

type DownloadTenantExportResult = bytes

class ListTenantsRequest(TypedDict):
    limit: NotRequired[int]
    after: NotRequired[TenantId]

type ListTenantsResult = TenantPage

class CreateTenantRequest(TypedDict):
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: TenantCreate

type CreateTenantResult = Tenant

class ListMembershipsRequest(TypedDict):
    tenantId: TenantId
    limit: NotRequired[int]
    after: NotRequired[MembershipId]

type ListMembershipsResult = MembershipPage

class CreateMembershipRequest(TypedDict):
    tenantId: TenantId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: MembershipCreate

type CreateMembershipResult = Membership

class ReplaceMembershipRequest(TypedDict):
    tenantId: TenantId
    membershipId: MembershipId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: MembershipReplace

type ReplaceMembershipResult = Membership

class ListAccountsRequest(TypedDict):
    limit: NotRequired[int]
    after: NotRequired[AccountId]

type ListAccountsResult = AccountPage

class CreateAccountRequest(TypedDict):
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: AccountCreate

type CreateAccountResult = Account

class GetAccountRequest(TypedDict):
    accountId: AccountId

type GetAccountResult = Account

class GetAccountStatementRequest(TypedDict):
    accountId: AccountId
    limit: NotRequired[int]
    asOf: NotRequired[PostingSnapshot]
    currency: NotRequired[Currency]
    bookingDateFrom: NotRequired[str]
    bookingDateTo: NotRequired[str]
    after: NotRequired[AccountStatementCursor]

type GetAccountStatementResult = AccountStatementPage

class GetAccountBalancesRequest(TypedDict):
    accountId: AccountId
    asOf: NotRequired[PostingSnapshot]
    currency: NotRequired[Currency]
    bookingDateFrom: NotRequired[str]
    bookingDateTo: NotRequired[str]

type GetAccountBalancesResult = AccountBalances

class ListPeriodsRequest(TypedDict):
    limit: NotRequired[int]
    after: NotRequired[PeriodId]

type ListPeriodsResult = PeriodPage

class CreatePeriodRequest(TypedDict):
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: PeriodCreate

type CreatePeriodResult = Period

class GetPeriodRequest(TypedDict):
    periodId: PeriodId

type GetPeriodResult = Period

class FestschreibenPeriodRequest(TypedDict):
    periodId: PeriodId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]

type FestschreibenPeriodResult = Period

class ListJournalEntriesRequest(TypedDict):
    limit: NotRequired[int]
    after: NotRequired[EntryId]
    status: JournalEntryStatus
    periodId: NotRequired[PeriodId]
    documentId: NotRequired[DocumentId]
    bookingDateFrom: NotRequired[str]
    bookingDateTo: NotRequired[str]
    externalReference: NotRequired[str]

type ListJournalEntriesResult = JournalEntryPage

class CreateJournalEntryDraftRequest(TypedDict):
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: JournalEntryCreate

type CreateJournalEntryDraftResult = JournalEntry

class GetJournalEntryRequest(TypedDict):
    entryId: EntryId

type GetJournalEntryResult = JournalEntry

class ReplaceJournalEntryDraftRequest(TypedDict):
    entryId: EntryId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    ifMatch: str
    body: JournalEntryCreate

type ReplaceJournalEntryDraftResult = JournalEntry

class DiscardJournalEntryDraftRequest(TypedDict):
    entryId: EntryId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    ifMatch: str

type DiscardJournalEntryDraftResult = None

class PostJournalEntryRequest(TypedDict):
    entryId: EntryId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    ifMatch: NotRequired[str]

type PostJournalEntryResult = JournalEntry

class ReverseJournalEntryRequest(TypedDict):
    entryId: EntryId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: JournalEntryReversalCreate

type ReverseJournalEntryResult = JournalEntry

class LinkJournalEntryDocumentRequest(TypedDict):
    entryId: EntryId
    documentId: DocumentId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]

type LinkJournalEntryDocumentResult = None

class ListDocumentsRequest(TypedDict):
    limit: NotRequired[int]
    after: NotRequired[DocumentId]
    status: NotRequired[DocumentStatus]
    origin: NotRequired[DocumentOrigin]
    documentDateFrom: NotRequired[str]
    documentDateTo: NotRequired[str]
    journalEntryId: NotRequired[EntryId]
    sourceDocumentId: NotRequired[DocumentId]

type ListDocumentsResult = DocumentPage

class CreateDocumentRequest(TypedDict):
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: DocumentCreate

type CreateDocumentResult = DocumentCreateResult

class ListDocumentSourcesRequest(TypedDict):
    documentId: DocumentId

type ListDocumentSourcesResult = DocumentSourceList

class GetDocumentRequest(TypedDict):
    documentId: DocumentId

type GetDocumentResult = Document

class DownloadDocumentRequest(TypedDict):
    documentId: DocumentId

type DownloadDocumentResult = bytes

class CreateDocumentUploadRequestRequest(TypedDict):
    documentId: DocumentId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]

type CreateDocumentUploadRequestResult = DocumentUploadRequest

class CompleteDocumentRequest(TypedDict):
    documentId: DocumentId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]

type CompleteDocumentResult = Document

class CreateDocumentPreservationRequest(TypedDict):
    documentId: DocumentId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: DocumentPreservationCreate

type CreateDocumentPreservationResult = DocumentPreservation

class GetDocumentPreservationRequest(TypedDict):
    preservationId: DocumentPreservationId

type GetDocumentPreservationResult = DocumentPreservation

class CreateEInvoiceValidationRequest(TypedDict):
    documentId: DocumentId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]

type CreateEInvoiceValidationResult = EInvoiceValidation

class GetEInvoiceValidationRequest(TypedDict):
    validationId: EInvoiceValidationId

type GetEInvoiceValidationResult = EInvoiceValidation

class CreateZUGFeRDPDFRequest(TypedDict):
    validationId: EInvoiceValidationId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: ZUGFeRDPDFCreate

type CreateZUGFeRDPDFResult = ZUGFeRDPDF

class GetZUGFeRDPDFRequest(TypedDict):
    zugferdPdfId: ZUGFeRDPDFId

type GetZUGFeRDPDFResult = ZUGFeRDPDF

class ListWebhookEndpointsRequest(TypedDict):
    limit: NotRequired[int]
    after: NotRequired[WebhookEndpointId]

type ListWebhookEndpointsResult = WebhookEndpointPage

class CreateWebhookEndpointRequest(TypedDict):
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    body: WebhookEndpointCreate

type CreateWebhookEndpointResult = WebhookEndpoint

class GetWebhookEndpointRequest(TypedDict):
    webhookEndpointId: WebhookEndpointId

type GetWebhookEndpointResult = WebhookEndpoint

class ReplaceWebhookEndpointRequest(TypedDict):
    webhookEndpointId: WebhookEndpointId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    ifMatch: str
    body: WebhookEndpointReplace

type ReplaceWebhookEndpointResult = WebhookEndpoint

class DeleteWebhookEndpointRequest(TypedDict):
    webhookEndpointId: WebhookEndpointId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    ifMatch: str

type DeleteWebhookEndpointResult = None

class RotateWebhookEndpointSecretRequest(TypedDict):
    webhookEndpointId: WebhookEndpointId
    idempotencyKey: str
    xAccountingActingUserIssuer: NotRequired[str]
    xAccountingActingUserSubject: NotRequired[str]
    ifMatch: str
    body: WebhookEndpointSecretReplace

type RotateWebhookEndpointSecretResult = None
