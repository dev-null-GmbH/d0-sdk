# Generated from the pinned ERiC public catalog. Do not edit.
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from . import generated as g


class EricOperations:
    def _call(self, operation: str, request: Mapping[str, Any]) -> Any:
        raise NotImplementedError

    def get_user_notices(self, request: g.GetUserNoticesRequest) -> g.GetUserNoticesResult:
        return cast(g.GetUserNoticesResult, self._call('GetUserNotices', request))

    def create_profile(self, request: g.CreateProfileRequest) -> g.CreateProfileResult:
        return cast(g.CreateProfileResult, self._call('CreateProfile', request))

    def get_profile(self, request: g.GetProfileRequest) -> g.GetProfileResult:
        return cast(g.GetProfileResult, self._call('GetProfile', request))

    def create_draft(self, request: g.CreateDraftRequest) -> g.CreateDraftResult:
        return cast(g.CreateDraftResult, self._call('CreateDraft', request))

    def revise_draft(self, request: g.ReviseDraftRequest) -> g.ReviseDraftResult:
        return cast(g.ReviseDraftResult, self._call('ReviseDraft', request))

    def get_draft(self, request: g.GetDraftRequest) -> g.GetDraftResult:
        return cast(g.GetDraftResult, self._call('GetDraft', request))

    def get_draft_revision(self, request: g.GetDraftRevisionRequest) -> g.GetDraftRevisionResult:
        return cast(g.GetDraftRevisionResult, self._call('GetDraftRevision', request))

    def create_preparation(self, request: g.CreatePreparationRequest) -> g.CreatePreparationResult:
        return cast(g.CreatePreparationResult, self._call('CreatePreparation', request))

    def get_preparation(self, request: g.GetPreparationRequest) -> g.GetPreparationResult:
        return cast(g.GetPreparationResult, self._call('GetPreparation', request))

    def get_preparation_artifact(self, request: g.GetPreparationArtifactRequest) -> g.GetPreparationArtifactResult:
        return cast(g.GetPreparationArtifactResult, self._call('GetPreparationArtifact', request))

    def create_validation(self, request: g.CreateValidationRequest) -> g.CreateValidationResult:
        return cast(g.CreateValidationResult, self._call('CreateValidation', request))

    def get_validation(self, request: g.GetValidationRequest) -> g.GetValidationResult:
        return cast(g.GetValidationResult, self._call('GetValidation', request))

    def get_validation_artifact(self, request: g.GetValidationArtifactRequest) -> g.GetValidationArtifactResult:
        return cast(g.GetValidationArtifactResult, self._call('GetValidationArtifact', request))

    def create_delegated_review(self, request: g.CreateDelegatedReviewRequest) -> g.CreateDelegatedReviewResult:
        return cast(g.CreateDelegatedReviewResult, self._call('CreateDelegatedReview', request))

    def get_delegated_review(self, request: g.GetDelegatedReviewRequest) -> g.GetDelegatedReviewResult:
        return cast(g.GetDelegatedReviewResult, self._call('GetDelegatedReview', request))

    def confirm_delegated_review(self, request: g.ConfirmDelegatedReviewRequest) -> g.ConfirmDelegatedReviewResult:
        return cast(g.ConfirmDelegatedReviewResult, self._call('ConfirmDelegatedReview', request))

    def revoke_delegated_review(self, request: g.RevokeDelegatedReviewRequest) -> g.RevokeDelegatedReviewResult:
        return cast(g.RevokeDelegatedReviewResult, self._call('RevokeDelegatedReview', request))

    def get_u_st_va_field_catalog(self, request: g.GetUStVAFieldCatalogRequest) -> g.GetUStVAFieldCatalogResult:
        return cast(g.GetUStVAFieldCatalogResult, self._call('GetUStVAFieldCatalog', request))

    def create_utility(self, request: g.CreateUtilityRequest) -> g.CreateUtilityResult:
        return cast(g.CreateUtilityResult, self._call('CreateUtility', request))

    def get_utility(self, request: g.GetUtilityRequest) -> g.GetUtilityResult:
        return cast(g.GetUtilityResult, self._call('GetUtility', request))

    def create_credential_intake(self, request: g.CreateCredentialIntakeRequest) -> g.CreateCredentialIntakeResult:
        return cast(g.CreateCredentialIntakeResult, self._call('CreateCredentialIntake', request))

    def get_software_credential(self, request: g.GetSoftwareCredentialRequest) -> g.GetSoftwareCredentialResult:
        return cast(g.GetSoftwareCredentialResult, self._call('GetSoftwareCredential', request))

    def revoke_software_credential(self, request: g.RevokeSoftwareCredentialRequest) -> g.RevokeSoftwareCredentialResult:
        return cast(g.RevokeSoftwareCredentialResult, self._call('RevokeSoftwareCredential', request))

    def get_u_st_va_derived_rules(self, request: g.GetUStVADerivedRulesRequest) -> g.GetUStVADerivedRulesResult:
        return cast(g.GetUStVADerivedRulesResult, self._call('GetUStVADerivedRules', request))

    def create_filing_consent(self, request: g.CreateFilingConsentRequest) -> g.CreateFilingConsentResult:
        return cast(g.CreateFilingConsentResult, self._call('CreateFilingConsent', request))

    def get_filing_consent(self, request: g.GetFilingConsentRequest) -> g.GetFilingConsentResult:
        return cast(g.GetFilingConsentResult, self._call('GetFilingConsent', request))

    def confirm_filing_consent(self, request: g.ConfirmFilingConsentRequest) -> g.ConfirmFilingConsentResult:
        return cast(g.ConfirmFilingConsentResult, self._call('ConfirmFilingConsent', request))

    def revoke_filing_consent(self, request: g.RevokeFilingConsentRequest) -> g.RevokeFilingConsentResult:
        return cast(g.RevokeFilingConsentResult, self._call('RevokeFilingConsent', request))

    def get_credential_operation(self, request: g.GetCredentialOperationRequest) -> g.GetCredentialOperationResult:
        return cast(g.GetCredentialOperationResult, self._call('GetCredentialOperation', request))

    def get_retrieval_artifact(self, request: g.GetRetrievalArtifactRequest) -> g.GetRetrievalArtifactResult:
        return cast(g.GetRetrievalArtifactResult, self._call('GetRetrievalArtifact', request))

    def get_retrieval_artifact_content(self, request: g.GetRetrievalArtifactContentRequest) -> g.GetRetrievalArtifactContentResult:
        return cast(g.GetRetrievalArtifactContentResult, self._call('GetRetrievalArtifactContent', request))

    def create_retrieval_archive_acknowledgement(self, request: g.CreateRetrievalArchiveAcknowledgementRequest) -> g.CreateRetrievalArchiveAcknowledgementResult:
        return cast(g.CreateRetrievalArchiveAcknowledgementResult, self._call('CreateRetrievalArchiveAcknowledgement', request))

    def create_u_st_va_mapping(self, request: g.CreateUStVAMappingRequest) -> g.CreateUStVAMappingResult:
        return cast(g.CreateUStVAMappingResult, self._call('CreateUStVAMapping', request))

    def revise_u_st_va_mapping(self, request: g.ReviseUStVAMappingRequest) -> g.ReviseUStVAMappingResult:
        return cast(g.ReviseUStVAMappingResult, self._call('ReviseUStVAMapping', request))

    def get_u_st_va_mapping(self, request: g.GetUStVAMappingRequest) -> g.GetUStVAMappingResult:
        return cast(g.GetUStVAMappingResult, self._call('GetUStVAMapping', request))

    def get_u_st_va_mapping_revision(self, request: g.GetUStVAMappingRevisionRequest) -> g.GetUStVAMappingRevisionResult:
        return cast(g.GetUStVAMappingRevisionResult, self._call('GetUStVAMappingRevision', request))

    def confirm_u_st_va_mapping(self, request: g.ConfirmUStVAMappingRequest) -> g.ConfirmUStVAMappingResult:
        return cast(g.ConfirmUStVAMappingResult, self._call('ConfirmUStVAMapping', request))

    def withdraw_u_st_va_mapping(self, request: g.WithdrawUStVAMappingRequest) -> g.WithdrawUStVAMappingResult:
        return cast(g.WithdrawUStVAMappingResult, self._call('WithdrawUStVAMapping', request))

    def create_e_bilanz_mapping(self, request: g.CreateEBilanzMappingRequest) -> g.CreateEBilanzMappingResult:
        return cast(g.CreateEBilanzMappingResult, self._call('CreateEBilanzMapping', request))

    def revise_e_bilanz_mapping(self, request: g.ReviseEBilanzMappingRequest) -> g.ReviseEBilanzMappingResult:
        return cast(g.ReviseEBilanzMappingResult, self._call('ReviseEBilanzMapping', request))

    def get_e_bilanz_mapping(self, request: g.GetEBilanzMappingRequest) -> g.GetEBilanzMappingResult:
        return cast(g.GetEBilanzMappingResult, self._call('GetEBilanzMapping', request))

    def get_e_bilanz_mapping_revision(self, request: g.GetEBilanzMappingRevisionRequest) -> g.GetEBilanzMappingRevisionResult:
        return cast(g.GetEBilanzMappingRevisionResult, self._call('GetEBilanzMappingRevision', request))

    def confirm_e_bilanz_mapping(self, request: g.ConfirmEBilanzMappingRequest) -> g.ConfirmEBilanzMappingResult:
        return cast(g.ConfirmEBilanzMappingResult, self._call('ConfirmEBilanzMapping', request))

    def withdraw_e_bilanz_mapping(self, request: g.WithdrawEBilanzMappingRequest) -> g.WithdrawEBilanzMappingResult:
        return cast(g.WithdrawEBilanzMappingResult, self._call('WithdrawEBilanzMapping', request))

    def get_e_bilanz_mapping_catalog(self, request: g.GetEBilanzMappingCatalogRequest) -> g.GetEBilanzMappingCatalogResult:
        return cast(g.GetEBilanzMappingCatalogResult, self._call('GetEBilanzMappingCatalog', request))

    def create_retrieval_decryption(self, request: g.CreateRetrievalDecryptionRequest) -> g.CreateRetrievalDecryptionResult:
        return cast(g.CreateRetrievalDecryptionResult, self._call('CreateRetrievalDecryption', request))

    def get_retrieval_decryption(self, request: g.GetRetrievalDecryptionRequest) -> g.GetRetrievalDecryptionResult:
        return cast(g.GetRetrievalDecryptionResult, self._call('GetRetrievalDecryption', request))

    def create_retrieval_preservation(self, request: g.CreateRetrievalPreservationRequest) -> g.CreateRetrievalPreservationResult:
        return cast(g.CreateRetrievalPreservationResult, self._call('CreateRetrievalPreservation', request))

    def plan_e_bilanz_form(self, request: g.PlanEBilanzFormRequest) -> g.PlanEBilanzFormResult:
        return cast(g.PlanEBilanzFormResult, self._call('PlanEBilanzForm', request))

    def create_eric_test_simulation(self, request: g.CreateEricTestSimulationRequest) -> g.CreateEricTestSimulationResult:
        return cast(g.CreateEricTestSimulationResult, self._call('createEricTestSimulation', request))

    def get_eric_test_simulation(self, request: g.GetEricTestSimulationRequest) -> g.GetEricTestSimulationResult:
        return cast(g.GetEricTestSimulationResult, self._call('getEricTestSimulation', request))
