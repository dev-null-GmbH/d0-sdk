# Generated from the pinned ERiC public catalog. Do not edit.
from __future__ import annotations

from typing import Any, Literal, NotRequired, TypedDict


class Artifact(TypedDict):
    bytes: bytes
    contentType: str
    contentDigest: str

class EBilanzFormPlanInput(TypedDict):
    reporting_start: NotRequired[str]
    reporting_end: NotRequired[str]
    ub_income_statement: NotRequired[bool]
    tax_statement_type: NotRequired[Literal['SB', 'EB']]
    corporation_tax_option: NotRequired[bool]
    micro_bilg_prepared: NotRequired[bool]
    result_appropriation: NotRequired[bool]
    legal_form: Literal['EU', 'EUF', 'EUN', 'GmbH', 'UG', 'AG', 'OHG', 'KG', 'GKG', 'AGKG', 'GOHG', 'AGOHG', 'GBR', 'PG', 'ASG', 'soPG', 'EWI', 'Other.MUN', 'MU']
    income_statement_format: NotRequired[Literal['GKV', 'UKV']]
    fiscal_start: str
    closing_date: str
    statement_type: NotRequired[Literal['E', 'EB', 'UBandE', 'LSB', 'LAB', 'UB', 'LZB', 'ZW', 'UJ']]
    revision_status: NotRequired[Literal['E', 'B', 'G', 'BG', 'I', 'sK']]
    fiscal_end: NotRequired[str]
    accounting_standard: NotRequired[Literal['AO', 'HAOE', 'HGBM']]

class Problem(TypedDict):
    type: str
    title: str
    status: int

class EBilanzFormPlan(TypedDict):
    entry_schema: str
    schema_version: Literal['ebilanz-form-plan-v7', 'ebilanz-form-plan-v8', 'ebilanz-form-plan-v9', 'ebilanz-form-plan-v10', 'ebilanz-form-plan-v11', 'ebilanz-form-plan-v12', 'ebilanz-form-plan-v13', 'ebilanz-form-plan-v14', 'ebilanz-form-plan-v15', 'ebilanz-form-plan-v16', 'ebilanz-form-plan-v17', 'ebilanz-form-plan-v18', 'ebilanz-form-plan-v19', 'ebilanz-form-plan-v20']
    procedure: Literal['Bilanz_6.9']
    taxonomy_version: Literal['6.9']
    taxonomy_archive_sha256: Digest
    technical_guides_archive_sha256: Digest
    semantic_rule_version: str
    case: InlineObject1
    case_bindings: list[EBilanzFormBinding]
    contexts: list[EBilanzContext]
    fields: list[EBilanzFormField]
    presentation_edges: list[EBilanzFormEdge]
    calculation_edges: list[EBilanzFormCalculation]
    dimension_sets: list[EBilanzMappingDimensionSet]
    bal: InlineObject2
    limits: list[str]
    period_rules: InlineObject3
    reconciliation: NotRequired[EBilanzFormReconciliation]
    partnership: NotRequired[EBilanzFormPartnership]

class EBilanzFormPartnership(TypedDict):
    shareholder_tuple: str
    shareholder_id: str
    shareholder_group: str
    partner_axis: str
    tax_axis: str
    tax_member: str
    equity_axis: str
    equity_member_root: str
    kke_partner_groups: list[str]
    kke_equity_member_roots: NotRequired[dict[str, str]]
    required_kke_fields: list[str]

class EBilanzFormReconciliation(TypedDict):
    root_concept: str
    kind_concept: str
    kind_choices: list[str]
    requires_nonzero: bool
    entries: list[EBilanzFormTransferEntry]

class EBilanzFormTransferEntry(TypedDict):
    concept: str
    target_concept: str
    current_delta_concept: str
    previous_delta_concept: NotRequired[str]
    targets: list[str]

EBilanzFormCalculation = TypedDict('EBilanzFormCalculation', {
    'from': str,
    'to': str,
    'weight': int,
    'network': str,
})

EBilanzFormEdge = TypedDict('EBilanzFormEdge', {
    'from': str,
    'to': str,
    'component': Literal['B', 'GuV', 'GuVMicroBilG', 'EV', 'BVV', 'SGE', 'SGEP', 'BAL', 'KKE'],
})

class EBilanzFormBasis(TypedDict):
    name: Literal['tax', 'commercial', 'transition']
    columns: list[str]

class EBilanzMappingDimensionSet(TypedDict):
    id: Digest
    axes: list[EBilanzMappingAxis]

class EBilanzMappingAxis(TypedDict):
    name: str
    label: str
    kind: Literal['explicit', 'typed']
    typed_domain: NotRequired[str]
    members: list[EBilanzMappingMember]

class EBilanzMappingMember(TypedDict):
    name: str
    label: str
    value_legal_forms: list[Literal['EU', 'EUF', 'EUN', 'GmbH', 'UG', 'AG', 'OHG', 'KG', 'GKG', 'AGKG', 'GOHG', 'AGOHG', 'GBR', 'PG', 'ASG', 'soPG', 'EWI', 'Other.MUN', 'MU']]
    valid_since: NotRequired[list[str]]
    valid_through: NotRequired[list[str]]
    fiscal_valid_since: NotRequired[str]
    fiscal_valid_through: NotRequired[str]
    tax_prohibited_nonzero: NotRequired[bool]

type Digest = str
class EBilanzFormField(TypedDict):
    concept: str
    label: str
    kind: Literal['monetary', 'text', 'date', 'boolean', 'year', 'language', 'tuple', 'abstract', 'qname', 'positive_integer']
    period: Literal['', 'instant', 'duration']
    allowed_states: list[Literal['value', 'nil', 'tuple']]
    required: bool
    required_state: NotRequired[Literal['value', 'nil', 'tuple']]
    required_when: NotRequired[Literal['account_details_unavailable', 'kke_coordinate']]
    fiscal_requirement: NotRequired[str]
    components: list[Literal['B', 'GuV', 'GuVMicroBilG', 'EV', 'BVV', 'SGE', 'SGEP', 'BAL', 'STU', 'KKE']]
    pattern: NotRequired[str]
    tuple: NotRequired[EBilanzFormTuple]
    dimension_set_ids: list[Digest]
    valid_since: NotRequired[list[str]]
    valid_through: NotRequired[list[str]]
    fiscal_valid_since: NotRequired[str]
    fiscal_valid_through: NotRequired[str]
    selection_value: NotRequired[Literal['']]
    value_literal: NotRequired[Literal['siehe Fußnote', 'false', 'true']]
    footnote_required: NotRequired[Literal[True]]
    repeatable: NotRequired[bool]

class EBilanzFormTuple(TypedDict):
    mode: Literal['choice', 'sequence']
    children: list[str]
    required_children: list[str]
    many: bool
    selected_member: NotRequired[str]
    children_state: NotRequired[Literal['nil']]
    repeatable_children: NotRequired[list[str]]

type EBilanzContext = InlineObject4 | InlineObject5
type EBilanzDimension = InlineObject6 | InlineObject7
class EBilanzFormBinding(TypedDict):
    tuple_path: NotRequired[list[str]]
    concept: str
    value_from: Literal['fiscal_start', 'closing_date', 'tax_number', 'tax_office', 'literal_false', 'literal_true', 'company_name', 'street', 'postcode', 'city', 'fiscal_end']

type ID = str
type RetrievalPreservationInput = dict[str, Any]
class RetrievalDecryption(TypedDict):
    id: ID
    product_id: ID
    download_id: ID
    status: Literal['queued', 'running', 'completed', 'failed']
    created_at: str
    preserved: bool
    artifact_id: NotRequired[ID]

class RetrievalDecryptionInput(TypedDict):
    download_id: ID

class EBilanzMappingCatalog(TypedDict):
    schema_version: Literal['ebilanz-mapping-metadata-v1']
    procedure: Literal['Bilanz_6.9']
    taxonomy_version: Literal['6.9']
    taxonomy_archive_sha256: Digest
    semantic_rule_version: str
    scope: InlineObject8
    targets: list[EBilanzMappingTarget]
    dimension_sets: list[EBilanzMappingDimensionSet]
    limits: list[str]

class EBilanzMappingTarget(TypedDict):
    concept: str
    label: str
    period: Literal['instant', 'duration']
    nillable: bool
    components: list[Literal['B', 'GuV', 'BVV', 'SGE', 'SGEP', 'BAL', 'KKE']]
    value_legal_forms: list[Literal['EU', 'EUF', 'EUN', 'GmbH', 'UG', 'AG', 'OHG', 'KG', 'GKG', 'AGKG', 'GOHG', 'AGOHG', 'GBR', 'PG', 'ASG', 'soPG', 'EWI', 'Other.MUN', 'MU']]
    dimension_set_ids: list[Digest]
    valid_since: NotRequired[list[str]]
    valid_through: NotRequired[list[str]]
    fiscal_valid_since: NotRequired[str]
    fiscal_valid_through: NotRequired[str]
    fiscal_requirement: NotRequired[str]

class EBilanzMappingDecisionInput(TypedDict):
    signed_decision: str

class DecisionReceipt(TypedDict):
    id: ID
    mapping_id: MappingID
    revision: Revision
    action: Literal['confirm', 'withdraw']
    evidence_type: Literal['partner_asserted']
    mapping_sha256: Digest
    created_at: str

type Revision = int
type MappingID = str
class EBilanzMappingRevision(TypedDict):
    id: MappingID
    product_id: ID
    revision: Revision
    document: EBilanzMappingDocument
    mapping_sha256: Digest
    challenge: str
    statement_version: Literal['eric.ebilanz-mapping-confirmation.v1']
    statement: str
    status: Literal['unconfirmed', 'confirmed', 'withdrawn']

class EBilanzMappingDocument(TypedDict):
    schema_version: Literal['ebilanz-6.9-mapping-v1']
    source_namespace: str
    procedure: Literal['Bilanz_6.9']
    taxonomy_archive_sha256: Digest
    entries: list[EBilanzMappingEntry]

class EBilanzMappingEntry(TypedDict):
    source_key: str
    concept: str
    context_kind: Literal['instant', 'duration']
    dimensions: list[EBilanzDimension]

class EBilanzMappingRevisionInput(TypedDict):
    expected_revision: Revision
    document: EBilanzMappingDocument

class EBilanzMappingInput(TypedDict):
    document: EBilanzMappingDocument

class UStVAMappingDecisionInput(TypedDict):
    signed_decision: str

class UStVAMappingRevision(TypedDict):
    id: MappingID
    product_id: ID
    revision: Revision
    document: UStVAMappingDocument
    mapping_sha256: Digest
    challenge: str
    statement_version: Literal['eric.mapping-confirmation.v1']
    statement: str
    status: Literal['unconfirmed', 'confirmed', 'withdrawn']

class UStVAMappingDocument(TypedDict):
    schema_version: Literal['ustva-2026-mapping-v1']
    source_namespace: str
    procedure: Literal['UStVA_2026']
    rule_version: str
    rules_sha256: Digest
    entries: list[UStVAMappingEntry]

class UStVAMappingEntry(TypedDict):
    source_key: str
    group: Literal['Kz21', 'Kz35', 'Kz37', 'Kz39', 'Kz41', 'Kz42', 'Kz43', 'Kz44', 'Kz45', 'Kz46', 'Kz48', 'Kz49', 'Kz50', 'Kz59', 'Kz60', 'Kz61', 'Kz62', 'Kz63', 'Kz64', 'Kz65', 'Kz66', 'Kz67', 'Kz69', 'Kz73', 'Kz76', 'Kz77', 'Kz81', 'Kz84', 'Kz86', 'Kz87', 'Kz89', 'Kz90', 'Kz91', 'Kz93', 'Kz94', 'Kz95']

class UStVAMappingRevisionInput(TypedDict):
    expected_revision: Revision
    document: UStVAMappingDocument

class UStVAMappingInput(TypedDict):
    document: UStVAMappingDocument

class RetrievalArchiveAcknowledgement(TypedDict):
    id: ID
    artifact_id: ID
    product_id: ID
    acknowledged_at: str
    evidence_type: Literal['client_asserted']
    content_sha256: Digest
    provenance_sha256: Digest
    archive_reference: str

class RetrievalArchiveAcknowledgementInput(TypedDict):
    content_sha256: Digest
    provenance_sha256: Digest
    archive_reference: str

class RetrievalArtifact(TypedDict):
    id: ID
    product_id: ID
    purpose: Literal['authorized_test_retrieval']
    preserved_at: str
    content_media_type: Literal['application/octet-stream']
    content_bytes: int
    content_sha256: Digest
    provenance_media_type: Literal['application/json']
    provenance_bytes: int
    provenance_sha256: Digest

class CredentialOperation(TypedDict):
    intake_id: ID
    credential_id: ID
    source_version_id: ID
    version_id: ID
    job_id: ID
    status: Literal['queued', 'running', 'completed', 'failed', 'revoked']
    qualification: Literal['unqualified']

class FilingDecisionInput(TypedDict):
    decision_jws: str

class FilingConsent(TypedDict):
    id: ID
    product_id: ID
    preparation_id: ID
    mandate_id: ID
    binding_sha256: Digest
    binding_json: str
    purpose: Literal['authorized_test_transmission']
    evidence_type: Literal['partner_asserted']
    transmission_eligibility: Literal['blocked']
    status: Literal['pending', 'confirmed', 'revoked', 'expired']
    expires_at: str
    statement_version: Literal['eric.test-transmission-consent.v1']
    statement: Literal['Ich autorisiere ausschließlich die TEST-Übermittlung der unveränderten, vollständig geprüften Vorbereitung mit dem hier gebundenen Verfahren, Zeitraum und Zertifikat. Dies ist keine Produktionsübermittlung und keine steuerliche Einreichung. Die Ausführung bleibt bis zur unabhängigen technischen Qualifikation gesperrt.']
    review_html: str
    review_json: str
    manifest_json: str

class FilingConsentInput(TypedDict):
    mandate_id: ID

class FilingConsentOpened(TypedDict):
    id: ID
    product_id: ID
    preparation_id: ID
    mandate_id: ID
    binding_sha256: Digest
    binding_json: str
    purpose: Literal['authorized_test_transmission']
    evidence_type: Literal['partner_asserted']
    transmission_eligibility: Literal['blocked']
    status: Literal['pending', 'confirmed', 'revoked', 'expired']
    expires_at: str
    statement_version: Literal['eric.test-transmission-consent.v1']
    statement: Literal['Ich autorisiere ausschließlich die TEST-Übermittlung der unveränderten, vollständig geprüften Vorbereitung mit dem hier gebundenen Verfahren, Zeitraum und Zertifikat. Dies ist keine Produktionsübermittlung und keine steuerliche Einreichung. Die Ausführung bleibt bis zur unabhängigen technischen Qualifikation gesperrt.']
    review_html: str
    review_json: str
    manifest_json: str
    challenge: str

class UStVADerivedRules(TypedDict):
    version: str
    projection: str
    tax_policy: str
    formula: str
    sources: list[UStVADerivedRuleSource]
    groups: list[UStVADerivedRuleGroup]

class UStVADerivedRuleGroup(TypedDict):
    group: str
    base_field: str
    tax_field: str
    tax_required: bool
    result_sign: Literal[-1, 0, 1]

class UStVADerivedRuleSource(TypedDict):
    url: NotRequired[str]
    archive_sha256: NotRequired[Digest]
    member: NotRequired[str]
    sha256: Digest
    locator: NotRequired[str]

class SoftwareCredential(TypedDict):
    id: ID
    version_id: ID
    job_id: ID
    status: Literal['queued', 'running', 'inspected', 'failed', 'revoked', 'created']
    qualification: Literal['unqualified']
    credential_kind: Literal['software', 'cez']

class CredentialIntakeInput(TypedDict):
    origin: str
    action: Literal['create', 'rotate', 'create-cez', 'change-cez-pin']
    credential_id: NotRequired[ID]
    expected_version_id: NotRequired[ID]

class CredentialIntake(TypedDict):
    intake_id: ID
    credential_id: ID
    version_id: ID
    job_id: ID
    expires_at: str
    capability: str
    upload_url: str

class UtilityJob(TypedDict):
    id: ID
    product_id: ID
    operation: Literal['check-iban', 'check-bic', 'check-tax-number', 'check-bufa', 'check-ewaz', 'check-idnr', 'check-widnr', 'format-tax-number', 'format-ewaz', 'convert-tax-number', 'convert-ewaz', 'tax-office-states', 'test-tax-offices', 'tax-offices', 'tax-office', 'field-choices']
    status: Literal['queued', 'running', 'completed', 'failed']
    attempts: int
    result: NotRequired[UtilityResult]

class UtilityResult(TypedDict):
    outcome: Literal['succeeded', 'rejected', 'failed']
    failure: NotRequired[str]
    response: NotRequired[UtilityResponse]

class UtilityResponse(TypedDict):
    protocol: Literal[1]
    operation: Literal['check-iban', 'check-bic', 'check-tax-number', 'check-bufa', 'check-ewaz', 'check-idnr', 'check-widnr', 'format-tax-number', 'format-ewaz', 'convert-tax-number', 'convert-ewaz', 'tax-office-states', 'test-tax-offices', 'tax-offices', 'tax-office', 'field-choices']
    request_sha256: Digest
    sdk_release: Literal['44.3.6.0']
    sdk_archive_sha256: Digest
    native_code: int
    version_xml: str
    result_xml: NotRequired[str]
    result_text: NotRequired[str]

type UtilityInput = InlineObject9 | InlineObject10 | InlineObject11 | InlineObject12 | InlineObject13 | InlineObject14 | InlineObject15 | InlineObject16 | InlineObject17 | InlineObject18 | InlineObject19 | InlineObject20 | InlineObject21 | InlineObject22 | InlineObject23 | InlineObject24
class UStVAFieldCatalog(TypedDict):
    version: str
    archive_sha256: str
    schema_member: str
    schema_sha256: str
    periods: list[str]
    fields: list[UStVAFieldDefinition]

class UStVAFieldDefinition(TypedDict):
    code: str
    label: str
    schema_type: str
    unit: str
    kind: Literal['integer', 'decimal', 'choice', 'text', 'date']
    whole_digits: NotRequired[int]
    nonnegative: NotRequired[bool]
    choices: NotRequired[list[str]]
    choice_labels: NotRequired[dict[str, str]]
    max_length: NotRequired[int]

class DelegatedDecisionInput(TypedDict):
    decision_jws: str

class DelegatedReview(TypedDict):
    id: ID
    product_id: ID
    preparation_id: ID
    draft_id: ID
    revision: int
    profile_version: ProfileVersion
    manifest_sha256: str
    manifest_id: str
    payload_sha256: str
    review_html_sha256: str
    review_json_sha256: str
    statement_version: Literal['eric.test-review.v1']
    purpose: Literal['test_review_only']
    status: Literal['pending', 'confirmed', 'revoked', 'expired']
    expires_at: str
    statement: str
    evidence_type: Literal['partner_asserted']
    authority_id: ID
    authority_version: int
    actor_id: str

type ProfileVersion = str
class DelegatedReviewInput(TypedDict):
    purpose: Literal['test_review_only']

class DelegatedReviewOpened(TypedDict):
    id: ID
    product_id: ID
    preparation_id: ID
    draft_id: ID
    revision: int
    profile_version: ProfileVersion
    manifest_sha256: str
    manifest_id: str
    payload_sha256: str
    review_html_sha256: str
    review_json_sha256: str
    statement_version: Literal['eric.test-review.v1']
    purpose: Literal['test_review_only']
    status: Literal['pending', 'confirmed', 'revoked', 'expired']
    expires_at: str
    statement: str
    challenge: str
    review_html: str
    review_json: str
    manifest_json: str
    evidence_type: Literal['partner_asserted']
    authority_id: ID
    authority_version: int
    actor_id: str

class ValidationDiagnostics(TypedDict):
    schema: Literal['eric.validation-diagnostics.v1']
    status: Literal['available', 'unavailable']
    reason: NotRequired[Literal['native_result_unavailable', 'unsupported_result', 'projection_limit']]
    validation_id: str
    preparation_id: str
    procedure: str
    payload_sha256: str
    review_sha256: str
    request_sha256: str
    result_sha256: NotRequired[str]
    source_schema: str
    native_code: NotRequired[int]
    findings: list[ValidationDiagnosticFinding]

class ValidationDiagnosticFinding(TypedDict):
    kind: Literal['error', 'hint']
    ticket: str
    field_identifier: NotRequired[str]
    multiple_line_index: NotRequired[str]
    form_sequence: NotRequired[str]
    form_line: NotRequired[str]
    sub_area: NotRequired[str]
    private_id: NotRequired[str]
    rule_name: NotRequired[str]
    code: NotRequired[str]
    text: NotRequired[str]
    semantic_indices: NotRequired[list[DiagnosticSemanticIndex]]
    locations: list[DiagnosticLocation]

class DiagnosticLocation(TypedDict):
    review_path: str
    concept: NotRequired[str]
    context: NotRequired[str]
    fact_id: NotRequired[str]
    source_ref: NotRequired[str]
    source_version: NotRequired[str]

class DiagnosticSemanticIndex(TypedDict):
    name: str
    value: str

class Validation(TypedDict):
    id: ID
    product_id: ID
    preparation_id: ID
    status: Literal['queued', 'running', 'completed', 'failed']
    attempts: int
    outcome: NotRequired[Literal['valid', 'rejected', 'failed']]
    native_code: NotRequired[int]

class ValidationInput(TypedDict):
    preparation_id: ID

class Preparation(TypedDict):
    id: ID
    product_id: ID
    draft_id: ID
    revision: Revision
    profile_version: ProfileVersion
    manifest_id: Digest
    payload_sha256: Digest
    status: Literal['prepared']

class PreparationInput(TypedDict):
    draft_id: ID
    revision: Revision

class Draft(TypedDict):
    id: ID
    product_id: ID
    revision: Revision
    profile_version: ProfileVersion
    input: PreparationModuleInput

type PreparationModuleInput = UStVAInput | EBilanzInput | EBilanzMappedInput
class EBilanzMappedInput(TypedDict):
    schema_version: Literal['ebilanz-core-6.9-mapped-v1']
    source_snapshot_sha256: Digest
    mapping_id: MappingID
    mapping_revision: Revision
    draft: EBilanzMappedMetadata
    source_facts: list[EBilanzMappedFact]

type EBilanzMappedFact = InlineObject25 | InlineObject26
class EBilanzMappedMetadata(TypedDict):
    schema_version: Literal['ebilanz-core-6.9-v1']
    source_revision: str
    tax_number: str
    tax_office: str
    supplier: str
    closing_date: str
    contexts: list[EBilanzContext]
    facts: list[EBilanzFact]
    accounts: NotRequired[list[EBilanzAccount]]

class EBilanzAccount(TypedDict):
    id: str
    number: str
    label: str
    balance: str
    fact_id: str
    source: str

type EBilanzFact = InlineObject27 | InlineObject28 | InlineObject29 | InlineObject30
class EBilanzInput(TypedDict):
    corporation_tax_option: NotRequired[bool]
    micro_bilg_prepared: NotRequired[bool]
    schema_version: Literal['ebilanz-core-6.9-v1']
    source_revision: str
    mapping_version: str
    tax_number: str
    tax_office: str
    supplier: str
    closing_date: str
    contexts: list[EBilanzContext]
    facts: list[EBilanzFact]
    accounts: NotRequired[list[EBilanzAccount]]

type UStVAInput = UStVAInputV1 | UStVAInputV2 | UStVADerivedInput | UStVAMappedInput
class UStVAMappedInput(TypedDict):
    schema_version: Literal['ustva-2026-mapped-v1']
    source_snapshot_sha256: Digest
    mapping_id: MappingID
    mapping_revision: Revision
    draft: UStVADerivedMetadata
    facts: list[UStVAMappedFact]

class UStVAMappedFact(TypedDict):
    id: str
    source_ref: str
    source_version: str
    source_key: str
    base: NotRequired[str]
    tax: NotRequired[str]

class UStVADerivedMetadata(TypedDict):
    schema_version: Literal['ustva-2026-v2']
    source_revision: str
    creation_date: str
    year: Literal[2026]
    tax_office: str
    tax_number: str
    supplier: Supplier
    taxpayer: TaxpayerV2
    period: Literal['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '41', '42', '43', '44']
    correction: NotRequired[bool]
    economic_id: NotRequired[str]

class TaxpayerV2(TypedDict):
    designation: NotRequired[str]
    name: str
    first_name: NotRequired[str]
    street: NotRequired[str]
    house_number: NotRequired[str]
    postal_code: NotRequired[str]
    city: NotRequired[str]
    name_prefix: NotRequired[str]
    name_suffix: NotRequired[str]
    house_number_suffix: NotRequired[str]
    address_supplement: NotRequired[str]
    foreign_postal_code: NotRequired[str]
    country: NotRequired[str]
    po_box_city: NotRequired[str]
    po_box: NotRequired[str]
    phone: NotRequired[str]
    email: NotRequired[str]
    po_box_postal_code: NotRequired[str]
    large_recipient_postal_code: NotRequired[str]

class Supplier(TypedDict):
    name: str
    street: str
    house_number: str
    postal_code: str
    city: str
    country: str
    phone: str
    email: str

class UStVADerivedInput(TypedDict):
    schema_version: Literal['ustva-2026-derived-v1']
    source_snapshot_sha256: Digest
    mapping_version: str
    mapping_sha256: Digest
    draft: UStVADerivedMetadata
    facts: list[UStVADerivedFact]

class UStVADerivedFact(TypedDict):
    id: str
    source_ref: str
    source_version: str
    group: Literal['Kz21', 'Kz35', 'Kz37', 'Kz39', 'Kz41', 'Kz42', 'Kz43', 'Kz44', 'Kz45', 'Kz46', 'Kz48', 'Kz49', 'Kz50', 'Kz59', 'Kz60', 'Kz61', 'Kz62', 'Kz63', 'Kz64', 'Kz65', 'Kz66', 'Kz67', 'Kz69', 'Kz73', 'Kz76', 'Kz77', 'Kz81', 'Kz84', 'Kz86', 'Kz87', 'Kz89', 'Kz90', 'Kz91', 'Kz93', 'Kz94', 'Kz95']
    base: NotRequired[str]
    tax: NotRequired[str]

class UStVAInputV2(TypedDict):
    schema_version: Literal['ustva-2026-v2']
    source_revision: str
    creation_date: str
    year: Literal[2026]
    tax_office: str
    tax_number: str
    supplier: Supplier
    taxpayer: TaxpayerV2
    fields: UStVAFieldsV2
    period: Literal['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '41', '42', '43', '44']
    correction: NotRequired[bool]
    economic_id: NotRequired[str]

class UStVAFieldsV2(TypedDict):
    Kz21: NotRequired[str]
    Kz22: NotRequired[Literal['1']]
    Kz26: NotRequired[Literal['1']]
    Kz29: NotRequired[Literal['1']]
    Kz35: NotRequired[str]
    Kz36: NotRequired[str]
    Kz37: NotRequired[str]
    Kz39: NotRequired[str]
    Kz41: NotRequired[str]
    Kz42: NotRequired[str]
    Kz43: NotRequired[str]
    Kz44: NotRequired[str]
    Kz45: NotRequired[str]
    Kz46: NotRequired[str]
    Kz47: NotRequired[str]
    Kz48: NotRequired[str]
    Kz49: NotRequired[str]
    Kz50: NotRequired[str]
    Kz59: NotRequired[str]
    Kz60: NotRequired[str]
    Kz61: NotRequired[str]
    Kz62: NotRequired[str]
    Kz63: NotRequired[str]
    Kz64: NotRequired[str]
    Kz65: NotRequired[str]
    Kz66: NotRequired[str]
    Kz67: NotRequired[str]
    Kz69: NotRequired[str]
    Kz70: NotRequired[str]
    Kz73: NotRequired[str]
    Kz74: NotRequired[str]
    Kz76: NotRequired[str]
    Kz77: NotRequired[str]
    Kz80: NotRequired[str]
    Kz81: NotRequired[str]
    Kz83: str
    Kz84: NotRequired[str]
    Kz85: NotRequired[str]
    Kz86: NotRequired[str]
    Kz87: NotRequired[str]
    Kz89: NotRequired[str]
    Kz91: NotRequired[str]
    Kz93: NotRequired[str]
    Kz90: NotRequired[str]
    Kz94: NotRequired[str]
    Kz95: NotRequired[str]
    Kz96: NotRequired[str]
    Kz98: NotRequired[str]
    Kz500: NotRequired[Literal['1', '2', '3', '4']]
    Kz500_Begruendung: NotRequired[str]

class UStVAInputV1(TypedDict):
    schema_version: Literal['ustva-2026-v1']
    source_revision: str
    creation_date: str
    year: Literal[2026]
    month: str
    tax_office: str
    tax_number: str
    supplier: Supplier
    taxpayer: Taxpayer
    fields: Fields

class Fields(TypedDict):
    Kz81: NotRequired[str]
    Kz86: NotRequired[str]
    Kz66: NotRequired[str]
    Kz83: str

class Taxpayer(TypedDict):
    designation: str
    name: str
    first_name: str
    street: str
    house_number: str
    postal_code: str
    city: str

class DraftRevisionInput(TypedDict):
    expected_revision: Revision
    profile_version: ProfileVersion
    input: PreparationModuleInput

class DraftInput(TypedDict):
    profile_version: ProfileVersion
    input: PreparationModuleInput

class Profile(TypedDict):
    product_id: ID
    version: ProfileVersion
    manufacturer_id: str
    product_name: str
    product_version: str
    registration_evidence_sha256: str
    verified: bool

class ProfileInput(TypedDict):
    version: ProfileVersion
    manufacturer_id: str
    product_name: str
    product_version: str
    registration_evidence_sha256: str

class UserNoticeBundle(TypedDict):
    schema_version: Literal['eric.user-notices.v1']
    version: str
    sdk_release: str
    documentation_archive_sha256: Digest
    license_document_sha256: Digest
    license_member: str
    notices: list[UserNotice]

class UserNotice(TypedDict):
    id: str
    title: str
    text: str
    sha256: Digest
    acknowledgement_offered: bool
    source_section: str

class EricTestSimulation(TypedDict):
    id: str
    fixture: Literal['validation-accepted-v1', 'validation-rejected-v1']
    status: Literal['completed']
    outcome: Literal['simulated_accepted', 'simulated_rejected']
    simulated: Literal[True]

class GetUserNoticesRequest(TypedDict):
    productId: ID

type GetUserNoticesResult = UserNoticeBundle

class CreateProfileRequest(TypedDict):
    productId: ID
    idempotencyKey: str
    body: ProfileInput

type CreateProfileResult = Profile

class GetProfileRequest(TypedDict):
    productId: ID
    version: ProfileVersion

type GetProfileResult = Profile

class CreateDraftRequest(TypedDict):
    productId: ID
    idempotencyKey: str
    body: DraftInput

type CreateDraftResult = Draft

class ReviseDraftRequest(TypedDict):
    productId: ID
    draftId: ID
    idempotencyKey: str
    body: DraftRevisionInput

type ReviseDraftResult = Draft

class GetDraftRequest(TypedDict):
    productId: ID
    draftId: ID

type GetDraftResult = Draft

class GetDraftRevisionRequest(TypedDict):
    productId: ID
    draftId: ID
    revision: Revision

type GetDraftRevisionResult = Draft

class CreatePreparationRequest(TypedDict):
    productId: ID
    idempotencyKey: str
    body: PreparationInput

type CreatePreparationResult = Preparation

class GetPreparationRequest(TypedDict):
    productId: ID
    preparationId: ID

type GetPreparationResult = Preparation

class GetPreparationArtifactRequest(TypedDict):
    productId: ID
    preparationId: ID
    kind: Literal['payload.xml', 'review.html', 'review.json', 'manifest.json']

type GetPreparationArtifactResult = Artifact

class CreateValidationRequest(TypedDict):
    productId: ID
    idempotencyKey: str
    body: ValidationInput

type CreateValidationResult = Validation

class GetValidationRequest(TypedDict):
    productId: ID
    validationId: ID

type GetValidationResult = Validation

class GetValidationArtifactRequest(TypedDict):
    productId: ID
    validationId: ID
    kind: Literal['evidence.json', 'version.xml', 'result.xml', 'diagnostics.json']

type GetValidationArtifactResult = Artifact

class CreateDelegatedReviewRequest(TypedDict):
    productId: ID
    preparationId: ID
    idempotencyKey: str
    xEricActorStatus: str
    body: DelegatedReviewInput

type CreateDelegatedReviewResult = DelegatedReviewOpened

class GetDelegatedReviewRequest(TypedDict):
    productId: ID
    reviewId: ID
    xEricActorStatus: str

type GetDelegatedReviewResult = DelegatedReview

class ConfirmDelegatedReviewRequest(TypedDict):
    productId: ID
    reviewId: ID
    idempotencyKey: str
    xEricActorStatus: str
    body: DelegatedDecisionInput

type ConfirmDelegatedReviewResult = DelegatedReview

class RevokeDelegatedReviewRequest(TypedDict):
    productId: ID
    reviewId: ID
    idempotencyKey: str
    xEricActorStatus: str
    body: DelegatedDecisionInput

type RevokeDelegatedReviewResult = DelegatedReview

class GetUStVAFieldCatalogRequest(TypedDict):
    productId: ID

type GetUStVAFieldCatalogResult = UStVAFieldCatalog

class CreateUtilityRequest(TypedDict):
    productId: ID
    idempotencyKey: str
    body: UtilityInput

type CreateUtilityResult = UtilityJob

class GetUtilityRequest(TypedDict):
    productId: ID
    utilityId: ID

type GetUtilityResult = UtilityJob

class CreateCredentialIntakeRequest(TypedDict):
    productId: ID
    xEricActorStatus: str
    idempotencyKey: str
    body: CredentialIntakeInput

type CreateCredentialIntakeResult = CredentialIntake

class GetSoftwareCredentialRequest(TypedDict):
    productId: ID
    xEricActorStatus: str
    credentialId: ID
    xEricCredentialOrigin: str

type GetSoftwareCredentialResult = SoftwareCredential

class RevokeSoftwareCredentialRequest(TypedDict):
    productId: ID
    xEricActorStatus: str
    credentialId: ID
    idempotencyKey: str
    xEricCredentialOrigin: str

type RevokeSoftwareCredentialResult = SoftwareCredential

class GetUStVADerivedRulesRequest(TypedDict):
    productId: ID

type GetUStVADerivedRulesResult = UStVADerivedRules

class CreateFilingConsentRequest(TypedDict):
    productId: ID
    preparationId: ID
    xEricActorStatus: str
    xEricHumanAuthorization: NotRequired[str]
    idempotencyKey: str
    xEricReplayOnly: NotRequired[Literal['true']]
    body: FilingConsentInput

type CreateFilingConsentResult = FilingConsentOpened

class GetFilingConsentRequest(TypedDict):
    productId: ID
    consentId: ID
    xEricActorStatus: str
    xEricHumanAuthorization: NotRequired[str]

type GetFilingConsentResult = FilingConsent

class ConfirmFilingConsentRequest(TypedDict):
    productId: ID
    consentId: ID
    xEricActorStatus: str
    xEricHumanAuthorization: NotRequired[str]
    idempotencyKey: str
    body: FilingDecisionInput

type ConfirmFilingConsentResult = FilingConsent

class RevokeFilingConsentRequest(TypedDict):
    productId: ID
    consentId: ID
    xEricActorStatus: str
    xEricHumanAuthorization: NotRequired[str]
    idempotencyKey: str
    body: FilingDecisionInput

type RevokeFilingConsentResult = FilingConsent

class GetCredentialOperationRequest(TypedDict):
    productId: ID
    xEricActorStatus: str
    intakeId: ID
    xEricCredentialOrigin: str

type GetCredentialOperationResult = CredentialOperation

class GetRetrievalArtifactRequest(TypedDict):
    productId: ID
    artifactId: ID
    xEricActorStatus: str

type GetRetrievalArtifactResult = RetrievalArtifact

class GetRetrievalArtifactContentRequest(TypedDict):
    productId: ID
    artifactId: ID
    xEricActorStatus: str
    kind: Literal['content', 'provenance.json']

type GetRetrievalArtifactContentResult = Artifact

class CreateRetrievalArchiveAcknowledgementRequest(TypedDict):
    productId: ID
    artifactId: ID
    xEricActorStatus: str
    idempotencyKey: str
    body: RetrievalArchiveAcknowledgementInput

type CreateRetrievalArchiveAcknowledgementResult = RetrievalArchiveAcknowledgement

class CreateUStVAMappingRequest(TypedDict):
    productId: ID
    idempotencyKey: str
    body: UStVAMappingInput

type CreateUStVAMappingResult = UStVAMappingRevision

class ReviseUStVAMappingRequest(TypedDict):
    productId: ID
    mappingId: MappingID
    idempotencyKey: str
    body: UStVAMappingRevisionInput

type ReviseUStVAMappingResult = UStVAMappingRevision

class GetUStVAMappingRequest(TypedDict):
    productId: ID
    mappingId: MappingID

type GetUStVAMappingResult = UStVAMappingRevision

class GetUStVAMappingRevisionRequest(TypedDict):
    productId: ID
    mappingId: MappingID
    revision: Revision

type GetUStVAMappingRevisionResult = UStVAMappingRevision

class ConfirmUStVAMappingRequest(TypedDict):
    productId: ID
    mappingId: MappingID
    revision: Revision
    idempotencyKey: str
    xEricActorStatus: str
    body: UStVAMappingDecisionInput

type ConfirmUStVAMappingResult = DecisionReceipt

class WithdrawUStVAMappingRequest(TypedDict):
    productId: ID
    mappingId: MappingID
    revision: Revision
    idempotencyKey: str
    xEricActorStatus: str
    body: UStVAMappingDecisionInput

type WithdrawUStVAMappingResult = DecisionReceipt

class CreateEBilanzMappingRequest(TypedDict):
    productId: ID
    idempotencyKey: str
    body: EBilanzMappingInput

type CreateEBilanzMappingResult = EBilanzMappingRevision

class ReviseEBilanzMappingRequest(TypedDict):
    productId: ID
    mappingId: MappingID
    idempotencyKey: str
    body: EBilanzMappingRevisionInput

type ReviseEBilanzMappingResult = EBilanzMappingRevision

class GetEBilanzMappingRequest(TypedDict):
    productId: ID
    mappingId: MappingID

type GetEBilanzMappingResult = EBilanzMappingRevision

class GetEBilanzMappingRevisionRequest(TypedDict):
    productId: ID
    mappingId: MappingID
    revision: Revision

type GetEBilanzMappingRevisionResult = EBilanzMappingRevision

class ConfirmEBilanzMappingRequest(TypedDict):
    productId: ID
    mappingId: MappingID
    revision: Revision
    idempotencyKey: str
    xEricActorStatus: str
    body: EBilanzMappingDecisionInput

type ConfirmEBilanzMappingResult = DecisionReceipt

class WithdrawEBilanzMappingRequest(TypedDict):
    productId: ID
    mappingId: MappingID
    revision: Revision
    idempotencyKey: str
    xEricActorStatus: str
    body: EBilanzMappingDecisionInput

type WithdrawEBilanzMappingResult = DecisionReceipt

class GetEBilanzMappingCatalogRequest(TypedDict):
    productId: ID

type GetEBilanzMappingCatalogResult = EBilanzMappingCatalog

class CreateRetrievalDecryptionRequest(TypedDict):
    productId: ID
    xEricActorStatus: str
    idempotencyKey: str
    body: RetrievalDecryptionInput

type CreateRetrievalDecryptionResult = RetrievalDecryption

class GetRetrievalDecryptionRequest(TypedDict):
    productId: ID
    xEricActorStatus: str
    decryptionId: ID

type GetRetrievalDecryptionResult = RetrievalDecryption

class CreateRetrievalPreservationRequest(TypedDict):
    productId: ID
    xEricActorStatus: str
    decryptionId: ID
    idempotencyKey: str
    body: RetrievalPreservationInput

type CreateRetrievalPreservationResult = RetrievalDecryption

class PlanEBilanzFormRequest(TypedDict):
    productId: ID
    body: EBilanzFormPlanInput

type PlanEBilanzFormResult = EBilanzFormPlan

class CreateEricTestSimulationBody(TypedDict):
    fixture: Literal['validation-accepted-v1', 'validation-rejected-v1']

class CreateEricTestSimulationRequest(TypedDict):
    productId: str
    idempotencyKey: str
    body: CreateEricTestSimulationBody

type CreateEricTestSimulationResult = EricTestSimulation

class GetEricTestSimulationRequest(TypedDict):
    productId: str
    simulationId: str

type GetEricTestSimulationResult = EricTestSimulation

class InlineObject1(TypedDict):
    reporting_start: NotRequired[str]
    reporting_end: NotRequired[str]
    ub_income_statement: NotRequired[bool]
    tax_statement_type: NotRequired[Literal['SB', 'EB']]
    tax_statement_type_label: NotRequired[str]
    corporation_tax_option: NotRequired[bool]
    micro_bilg_prepared: bool
    result_appropriation: bool
    legal_form: Literal['EU', 'EUF', 'EUN', 'GmbH', 'UG', 'AG', 'OHG', 'KG', 'GKG', 'AGKG', 'GOHG', 'AGOHG', 'GBR', 'PG', 'ASG', 'soPG', 'EWI', 'Other.MUN', 'MU']
    legal_form_label: str
    income_statement_format: Literal['GKV', 'UKV']
    income_statement_format_label: str
    fiscal_start: str
    closing_date: str
    required_components: list[Literal['B', 'GuV', 'GuVMicroBilG', 'EV', 'BVV', 'SGE', 'SGEP', 'BAL', 'KS', 'STU', 'KKE']]
    account_details_required: bool
    account_detail_modes: list[Literal['provided', 'unavailable_with_footnote']]
    statement_type: Literal['E', 'EB', 'UBandE', 'LSB', 'LAB', 'UB', 'LZB', 'ZW', 'UJ']
    revision_status: Literal['E', 'B', 'G', 'BG', 'I', 'sK']
    fiscal_end: str
    statement_type_label: str
    revision_status_label: str
    accounting_standard: Literal['AO', 'HAOE', 'HGBM']
    accounting_standard_label: str

class InlineObject2(TypedDict):
    required_when: Literal['row_contains_value']
    required_fields: list[str]
    asset_axis: str
    tax_axis: str
    bases: list[EBilanzFormBasis]
    value_edges: list[EBilanzFormEdge]
    asset_edges: list[EBilanzFormEdge]
    calculation_edges: list[EBilanzFormCalculation]

class InlineObject3(TypedDict):
    reporting_period_binding: NotRequired[Literal['within_fiscal_year']]
    fiscal_start_min: str
    fiscal_start_max: str
    fiscal_end_min: str
    fiscal_end_max: str
    closing_date_binding: Literal['fiscal_start', 'fiscal_end', 'within_fiscal_year']
    self_employment_same_calendar_year: Literal[True]
    maximum_months: Literal[12]

class InlineObject4(TypedDict):
    id: str
    dimensions: NotRequired[list[EBilanzDimension]]
    start_date: str
    end_date: str

class InlineObject5(TypedDict):
    id: str
    dimensions: NotRequired[list[EBilanzDimension]]
    instant: str

class InlineObject6(TypedDict):
    name: str
    member: str

class InlineObject7(TypedDict):
    name: str
    typed_value: str

class InlineObject8(TypedDict):
    legal_forms: list[Literal['EU', 'GmbH', 'OHG', 'KG', 'GKG', 'AGKG', 'GOHG', 'AGOHG', 'GBR', 'PG', 'ASG', 'soPG', 'EWI', 'Other.MUN', 'MU']]
    accounting_standard: Literal['AO']
    income_statement_format: Literal['GKV']
    annual: Literal[True]

class InlineObject9(TypedDict):
    operation: Literal['check-iban']
    iban: str

class InlineObject10(TypedDict):
    operation: Literal['check-bic']
    value: str

class InlineObject11(TypedDict):
    operation: Literal['check-tax-number']
    value: str

class InlineObject12(TypedDict):
    operation: Literal['check-bufa']
    value: str

class InlineObject13(TypedDict):
    operation: Literal['check-ewaz']
    value: str

class InlineObject14(TypedDict):
    operation: Literal['check-idnr']
    value: str

class InlineObject15(TypedDict):
    operation: Literal['check-widnr']
    value: str

class InlineObject16(TypedDict):
    operation: Literal['format-tax-number']
    value: str

class InlineObject17(TypedDict):
    operation: Literal['format-ewaz']
    value: str

class InlineObject18(TypedDict):
    operation: Literal['convert-tax-number']
    value: str
    state: str
    tax_office: NotRequired[str]

class InlineObject19(TypedDict):
    operation: Literal['convert-ewaz']
    value: str
    state: str

class InlineObject20(TypedDict):
    operation: Literal['tax-office-states']

class InlineObject21(TypedDict):
    operation: Literal['test-tax-offices']

class InlineObject22(TypedDict):
    operation: Literal['tax-offices']
    value: str

class InlineObject23(TypedDict):
    operation: Literal['tax-office']
    value: str

class InlineObject24(TypedDict):
    operation: Literal['field-choices']
    value: NotRequired[str]
    procedure: Literal['ESt_2025']

class InlineObject25(TypedDict):
    id: str
    context: str
    unit: Literal['EUR']
    sources: list[str]
    source_ref: str
    source_version: str
    source_key: str
    state: Literal['value']
    value: str
    footnote: NotRequired[str]

class InlineObject26(TypedDict):
    id: str
    context: str
    unit: Literal['EUR']
    sources: list[str]
    source_ref: str
    source_version: str
    source_key: str
    state: Literal['nil']
    footnote: NotRequired[str]

class InlineObject27(TypedDict):
    id: str
    concept: str
    sources: list[str]
    context: str
    unit: NotRequired[Literal['EUR']]
    state: Literal['value']
    value: str
    footnote: NotRequired[str]

class InlineObject28(TypedDict):
    id: str
    concept: str
    sources: list[str]
    context: str
    unit: NotRequired[Literal['EUR']]
    state: Literal['nil']
    footnote: NotRequired[str]

class InlineObject29(TypedDict):
    id: str
    concept: str
    sources: list[str]
    state: Literal['tuple']
    children: list[EBilanzFact]

class InlineObject30(TypedDict):
    id: str
    concept: str
    sources: list[str]
    state: Literal['nil']
