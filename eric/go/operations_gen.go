// Code generated from the pinned ERiC public catalog. Do not edit.
package eric

import (
	"context"
	"errors"
	"github.com/dev-null-GmbH/d0-sdk/eric/go/genprod"
	"github.com/dev-null-GmbH/d0-sdk/eric/go/gentest"
	openapi_types "github.com/oapi-codegen/runtime/types"
)

func (c *Client) GetUserNotices(ctx context.Context, productId genprod.ID, params *genprod.GetUserNoticesParams) (*genprod.GetUserNoticesResponse, error) {
	if err := c.allow("GetUserNotices"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetUserNoticesWithResponse(ctx, productId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateProfile(ctx context.Context, productId genprod.ID, params *genprod.CreateProfileParams, body genprod.CreateProfileJSONRequestBody) (*genprod.CreateProfileResponse, error) {
	if err := c.allow("CreateProfile"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreateProfileWithResponse(ctx, productId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetProfile(ctx context.Context, productId genprod.ID, version genprod.ProfileVersion, params *genprod.GetProfileParams) (*genprod.GetProfileResponse, error) {
	if err := c.allow("GetProfile"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetProfileWithResponse(ctx, productId, version, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateDraft(ctx context.Context, productId genprod.ID, params *genprod.CreateDraftParams, body genprod.CreateDraftJSONRequestBody) (*genprod.CreateDraftResponse, error) {
	if err := c.allow("CreateDraft"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreateDraftWithResponse(ctx, productId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ReviseDraft(ctx context.Context, productId genprod.ID, draftId genprod.ID, params *genprod.ReviseDraftParams, body genprod.ReviseDraftJSONRequestBody) (*genprod.ReviseDraftResponse, error) {
	if err := c.allow("ReviseDraft"); err != nil {
		return nil, err
	}
	r, err := c.genprod.ReviseDraftWithResponse(ctx, productId, draftId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetDraft(ctx context.Context, productId genprod.ID, draftId genprod.ID, params *genprod.GetDraftParams) (*genprod.GetDraftResponse, error) {
	if err := c.allow("GetDraft"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetDraftWithResponse(ctx, productId, draftId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetDraftRevision(ctx context.Context, productId genprod.ID, draftId genprod.ID, revision genprod.Revision, params *genprod.GetDraftRevisionParams) (*genprod.GetDraftRevisionResponse, error) {
	if err := c.allow("GetDraftRevision"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetDraftRevisionWithResponse(ctx, productId, draftId, revision, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreatePreparation(ctx context.Context, productId genprod.ID, params *genprod.CreatePreparationParams, body genprod.CreatePreparationJSONRequestBody) (*genprod.CreatePreparationResponse, error) {
	if err := c.allow("CreatePreparation"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreatePreparationWithResponse(ctx, productId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetPreparation(ctx context.Context, productId genprod.ID, preparationId genprod.ID, params *genprod.GetPreparationParams) (*genprod.GetPreparationResponse, error) {
	if err := c.allow("GetPreparation"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetPreparationWithResponse(ctx, productId, preparationId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetPreparationArtifact(ctx context.Context, productId genprod.ID, preparationId genprod.ID, kind genprod.GetPreparationArtifactParamsKind, params *genprod.GetPreparationArtifactParams) (*genprod.GetPreparationArtifactResponse, error) {
	if err := c.allow("GetPreparationArtifact"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetPreparationArtifactWithResponse(ctx, productId, preparationId, kind, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	if err := verifyDigest(r.Body, r.HTTPResponse, false); err != nil {
		return nil, err
	}
	return r, nil
}

func (c *Client) CreateValidation(ctx context.Context, productId genprod.ID, params *genprod.CreateValidationParams, body genprod.CreateValidationJSONRequestBody) (*genprod.CreateValidationResponse, error) {
	if err := c.allow("CreateValidation"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreateValidationWithResponse(ctx, productId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetValidation(ctx context.Context, productId genprod.ID, validationId genprod.ID, params *genprod.GetValidationParams) (*genprod.GetValidationResponse, error) {
	if err := c.allow("GetValidation"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetValidationWithResponse(ctx, productId, validationId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetValidationArtifact(ctx context.Context, productId genprod.ID, validationId genprod.ID, kind genprod.GetValidationArtifactParamsKind, params *genprod.GetValidationArtifactParams) (*genprod.GetValidationArtifactResponse, error) {
	if err := c.allow("GetValidationArtifact"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetValidationArtifactWithResponse(ctx, productId, validationId, kind, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	if err := verifyDigest(r.Body, r.HTTPResponse, false); err != nil {
		return nil, err
	}
	return r, nil
}

func (c *Client) CreateDelegatedReview(ctx context.Context, productId genprod.ID, preparationId genprod.ID, params *genprod.CreateDelegatedReviewParams, body genprod.CreateDelegatedReviewJSONRequestBody) (*genprod.CreateDelegatedReviewResponse, error) {
	if err := c.allow("CreateDelegatedReview"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreateDelegatedReviewWithResponse(ctx, productId, preparationId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetDelegatedReview(ctx context.Context, productId genprod.ID, reviewId genprod.ID, params *genprod.GetDelegatedReviewParams) (*genprod.GetDelegatedReviewResponse, error) {
	if err := c.allow("GetDelegatedReview"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetDelegatedReviewWithResponse(ctx, productId, reviewId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ConfirmDelegatedReview(ctx context.Context, productId genprod.ID, reviewId genprod.ID, params *genprod.ConfirmDelegatedReviewParams, body genprod.ConfirmDelegatedReviewJSONRequestBody) (*genprod.ConfirmDelegatedReviewResponse, error) {
	if err := c.allow("ConfirmDelegatedReview"); err != nil {
		return nil, err
	}
	r, err := c.genprod.ConfirmDelegatedReviewWithResponse(ctx, productId, reviewId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) RevokeDelegatedReview(ctx context.Context, productId genprod.ID, reviewId genprod.ID, params *genprod.RevokeDelegatedReviewParams, body genprod.RevokeDelegatedReviewJSONRequestBody) (*genprod.RevokeDelegatedReviewResponse, error) {
	if err := c.allow("RevokeDelegatedReview"); err != nil {
		return nil, err
	}
	r, err := c.genprod.RevokeDelegatedReviewWithResponse(ctx, productId, reviewId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetUStVAFieldCatalog(ctx context.Context, productId genprod.ID, params *genprod.GetUStVAFieldCatalogParams) (*genprod.GetUStVAFieldCatalogResponse, error) {
	if err := c.allow("GetUStVAFieldCatalog"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetUStVAFieldCatalogWithResponse(ctx, productId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateUtility(ctx context.Context, productId genprod.ID, params *genprod.CreateUtilityParams, body genprod.CreateUtilityJSONRequestBody) (*genprod.CreateUtilityResponse, error) {
	if err := c.allow("CreateUtility"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreateUtilityWithResponse(ctx, productId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetUtility(ctx context.Context, productId genprod.ID, utilityId genprod.ID, params *genprod.GetUtilityParams) (*genprod.GetUtilityResponse, error) {
	if err := c.allow("GetUtility"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetUtilityWithResponse(ctx, productId, utilityId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateCredentialIntake(ctx context.Context, productId genprod.ID, params *genprod.CreateCredentialIntakeParams, body genprod.CreateCredentialIntakeJSONRequestBody) (*genprod.CreateCredentialIntakeResponse, error) {
	if err := c.allow("CreateCredentialIntake"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreateCredentialIntakeWithResponse(ctx, productId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetSoftwareCredential(ctx context.Context, productId genprod.ID, credentialId genprod.ID, params *genprod.GetSoftwareCredentialParams) (*genprod.GetSoftwareCredentialResponse, error) {
	if err := c.allow("GetSoftwareCredential"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetSoftwareCredentialWithResponse(ctx, productId, credentialId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) RevokeSoftwareCredential(ctx context.Context, productId genprod.ID, credentialId genprod.ID, params *genprod.RevokeSoftwareCredentialParams) (*genprod.RevokeSoftwareCredentialResponse, error) {
	if err := c.allow("RevokeSoftwareCredential"); err != nil {
		return nil, err
	}
	r, err := c.genprod.RevokeSoftwareCredentialWithResponse(ctx, productId, credentialId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetUStVADerivedRules(ctx context.Context, productId genprod.ID, params *genprod.GetUStVADerivedRulesParams) (*genprod.GetUStVADerivedRulesResponse, error) {
	if err := c.allow("GetUStVADerivedRules"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetUStVADerivedRulesWithResponse(ctx, productId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateFilingConsent(ctx context.Context, productId genprod.ID, preparationId genprod.ID, params *genprod.CreateFilingConsentParams, body genprod.CreateFilingConsentJSONRequestBody) (*genprod.CreateFilingConsentResponse, error) {
	if err := c.allow("CreateFilingConsent"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreateFilingConsentWithResponse(ctx, productId, preparationId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetFilingConsent(ctx context.Context, productId genprod.ID, consentId genprod.ID, params *genprod.GetFilingConsentParams) (*genprod.GetFilingConsentResponse, error) {
	if err := c.allow("GetFilingConsent"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetFilingConsentWithResponse(ctx, productId, consentId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ConfirmFilingConsent(ctx context.Context, productId genprod.ID, consentId genprod.ID, params *genprod.ConfirmFilingConsentParams, body genprod.ConfirmFilingConsentJSONRequestBody) (*genprod.ConfirmFilingConsentResponse, error) {
	if err := c.allow("ConfirmFilingConsent"); err != nil {
		return nil, err
	}
	r, err := c.genprod.ConfirmFilingConsentWithResponse(ctx, productId, consentId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) RevokeFilingConsent(ctx context.Context, productId genprod.ID, consentId genprod.ID, params *genprod.RevokeFilingConsentParams, body genprod.RevokeFilingConsentJSONRequestBody) (*genprod.RevokeFilingConsentResponse, error) {
	if err := c.allow("RevokeFilingConsent"); err != nil {
		return nil, err
	}
	r, err := c.genprod.RevokeFilingConsentWithResponse(ctx, productId, consentId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetCredentialOperation(ctx context.Context, productId genprod.ID, intakeId genprod.ID, params *genprod.GetCredentialOperationParams) (*genprod.GetCredentialOperationResponse, error) {
	if err := c.allow("GetCredentialOperation"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetCredentialOperationWithResponse(ctx, productId, intakeId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetRetrievalArtifact(ctx context.Context, productId genprod.ID, artifactId genprod.ID, params *genprod.GetRetrievalArtifactParams) (*genprod.GetRetrievalArtifactResponse, error) {
	if err := c.allow("GetRetrievalArtifact"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetRetrievalArtifactWithResponse(ctx, productId, artifactId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetRetrievalArtifactContent(ctx context.Context, productId genprod.ID, artifactId genprod.ID, kind genprod.GetRetrievalArtifactContentParamsKind, params *genprod.GetRetrievalArtifactContentParams) (*genprod.GetRetrievalArtifactContentResponse, error) {
	if err := c.allow("GetRetrievalArtifactContent"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetRetrievalArtifactContentWithResponse(ctx, productId, artifactId, kind, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	if err := verifyDigest(r.Body, r.HTTPResponse, true); err != nil {
		return nil, err
	}
	return r, nil
}

func (c *Client) CreateRetrievalArchiveAcknowledgement(ctx context.Context, productId genprod.ID, artifactId genprod.ID, params *genprod.CreateRetrievalArchiveAcknowledgementParams, body genprod.CreateRetrievalArchiveAcknowledgementJSONRequestBody) (*genprod.CreateRetrievalArchiveAcknowledgementResponse, error) {
	if err := c.allow("CreateRetrievalArchiveAcknowledgement"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreateRetrievalArchiveAcknowledgementWithResponse(ctx, productId, artifactId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateUStVAMapping(ctx context.Context, productId genprod.ID, params *genprod.CreateUStVAMappingParams, body genprod.CreateUStVAMappingJSONRequestBody) (*genprod.CreateUStVAMappingResponse, error) {
	if err := c.allow("CreateUStVAMapping"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreateUStVAMappingWithResponse(ctx, productId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ReviseUStVAMapping(ctx context.Context, productId genprod.ID, mappingId genprod.MappingID, params *genprod.ReviseUStVAMappingParams, body genprod.ReviseUStVAMappingJSONRequestBody) (*genprod.ReviseUStVAMappingResponse, error) {
	if err := c.allow("ReviseUStVAMapping"); err != nil {
		return nil, err
	}
	r, err := c.genprod.ReviseUStVAMappingWithResponse(ctx, productId, mappingId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetUStVAMapping(ctx context.Context, productId genprod.ID, mappingId genprod.MappingID, params *genprod.GetUStVAMappingParams) (*genprod.GetUStVAMappingResponse, error) {
	if err := c.allow("GetUStVAMapping"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetUStVAMappingWithResponse(ctx, productId, mappingId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetUStVAMappingRevision(ctx context.Context, productId genprod.ID, mappingId genprod.MappingID, revision genprod.Revision, params *genprod.GetUStVAMappingRevisionParams) (*genprod.GetUStVAMappingRevisionResponse, error) {
	if err := c.allow("GetUStVAMappingRevision"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetUStVAMappingRevisionWithResponse(ctx, productId, mappingId, revision, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ConfirmUStVAMapping(ctx context.Context, productId genprod.ID, mappingId genprod.MappingID, revision genprod.Revision, params *genprod.ConfirmUStVAMappingParams, body genprod.ConfirmUStVAMappingJSONRequestBody) (*genprod.ConfirmUStVAMappingResponse, error) {
	if err := c.allow("ConfirmUStVAMapping"); err != nil {
		return nil, err
	}
	r, err := c.genprod.ConfirmUStVAMappingWithResponse(ctx, productId, mappingId, revision, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) WithdrawUStVAMapping(ctx context.Context, productId genprod.ID, mappingId genprod.MappingID, revision genprod.Revision, params *genprod.WithdrawUStVAMappingParams, body genprod.WithdrawUStVAMappingJSONRequestBody) (*genprod.WithdrawUStVAMappingResponse, error) {
	if err := c.allow("WithdrawUStVAMapping"); err != nil {
		return nil, err
	}
	r, err := c.genprod.WithdrawUStVAMappingWithResponse(ctx, productId, mappingId, revision, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateEBilanzMapping(ctx context.Context, productId genprod.ID, params *genprod.CreateEBilanzMappingParams, body genprod.CreateEBilanzMappingJSONRequestBody) (*genprod.CreateEBilanzMappingResponse, error) {
	if err := c.allow("CreateEBilanzMapping"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreateEBilanzMappingWithResponse(ctx, productId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ReviseEBilanzMapping(ctx context.Context, productId genprod.ID, mappingId genprod.MappingID, params *genprod.ReviseEBilanzMappingParams, body genprod.ReviseEBilanzMappingJSONRequestBody) (*genprod.ReviseEBilanzMappingResponse, error) {
	if err := c.allow("ReviseEBilanzMapping"); err != nil {
		return nil, err
	}
	r, err := c.genprod.ReviseEBilanzMappingWithResponse(ctx, productId, mappingId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetEBilanzMapping(ctx context.Context, productId genprod.ID, mappingId genprod.MappingID, params *genprod.GetEBilanzMappingParams) (*genprod.GetEBilanzMappingResponse, error) {
	if err := c.allow("GetEBilanzMapping"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetEBilanzMappingWithResponse(ctx, productId, mappingId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetEBilanzMappingRevision(ctx context.Context, productId genprod.ID, mappingId genprod.MappingID, revision genprod.Revision, params *genprod.GetEBilanzMappingRevisionParams) (*genprod.GetEBilanzMappingRevisionResponse, error) {
	if err := c.allow("GetEBilanzMappingRevision"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetEBilanzMappingRevisionWithResponse(ctx, productId, mappingId, revision, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) ConfirmEBilanzMapping(ctx context.Context, productId genprod.ID, mappingId genprod.MappingID, revision genprod.Revision, params *genprod.ConfirmEBilanzMappingParams, body genprod.ConfirmEBilanzMappingJSONRequestBody) (*genprod.ConfirmEBilanzMappingResponse, error) {
	if err := c.allow("ConfirmEBilanzMapping"); err != nil {
		return nil, err
	}
	r, err := c.genprod.ConfirmEBilanzMappingWithResponse(ctx, productId, mappingId, revision, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) WithdrawEBilanzMapping(ctx context.Context, productId genprod.ID, mappingId genprod.MappingID, revision genprod.Revision, params *genprod.WithdrawEBilanzMappingParams, body genprod.WithdrawEBilanzMappingJSONRequestBody) (*genprod.WithdrawEBilanzMappingResponse, error) {
	if err := c.allow("WithdrawEBilanzMapping"); err != nil {
		return nil, err
	}
	r, err := c.genprod.WithdrawEBilanzMappingWithResponse(ctx, productId, mappingId, revision, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetEBilanzMappingCatalog(ctx context.Context, productId genprod.ID, params *genprod.GetEBilanzMappingCatalogParams) (*genprod.GetEBilanzMappingCatalogResponse, error) {
	if err := c.allow("GetEBilanzMappingCatalog"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetEBilanzMappingCatalogWithResponse(ctx, productId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateRetrievalDecryption(ctx context.Context, productId genprod.ID, params *genprod.CreateRetrievalDecryptionParams, body genprod.CreateRetrievalDecryptionJSONRequestBody) (*genprod.CreateRetrievalDecryptionResponse, error) {
	if err := c.allow("CreateRetrievalDecryption"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreateRetrievalDecryptionWithResponse(ctx, productId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetRetrievalDecryption(ctx context.Context, productId genprod.ID, decryptionId genprod.ID, params *genprod.GetRetrievalDecryptionParams) (*genprod.GetRetrievalDecryptionResponse, error) {
	if err := c.allow("GetRetrievalDecryption"); err != nil {
		return nil, err
	}
	r, err := c.genprod.GetRetrievalDecryptionWithResponse(ctx, productId, decryptionId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateRetrievalPreservation(ctx context.Context, productId genprod.ID, decryptionId genprod.ID, params *genprod.CreateRetrievalPreservationParams, body genprod.CreateRetrievalPreservationJSONRequestBody) (*genprod.CreateRetrievalPreservationResponse, error) {
	if err := c.allow("CreateRetrievalPreservation"); err != nil {
		return nil, err
	}
	r, err := c.genprod.CreateRetrievalPreservationWithResponse(ctx, productId, decryptionId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 201 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) PlanEBilanzForm(ctx context.Context, productId genprod.ID, params *genprod.PlanEBilanzFormParams, body genprod.PlanEBilanzFormJSONRequestBody) (*genprod.PlanEBilanzFormResponse, error) {
	if err := c.allow("PlanEBilanzForm"); err != nil {
		return nil, err
	}
	r, err := c.genprod.PlanEBilanzFormWithResponse(ctx, productId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) CreateEricTestSimulation(ctx context.Context, tenantId gentest.Tenant, productId gentest.Product, params *gentest.CreateEricTestSimulationParams, body gentest.CreateEricTestSimulationJSONRequestBody) (*gentest.CreateEricTestSimulationResponse, error) {
	if err := c.allow("createEricTestSimulation"); err != nil {
		return nil, err
	}
	if tenantId.String() != c.tenant {
		return nil, errors.New("test tenant path does not match selected tenant")
	}
	r, err := c.gentest.CreateEricTestSimulationWithResponse(ctx, tenantId, productId, params, body)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 202 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}

func (c *Client) GetEricTestSimulation(ctx context.Context, tenantId gentest.Tenant, productId gentest.Product, simulationId openapi_types.UUID, params *gentest.GetEricTestSimulationParams) (*gentest.GetEricTestSimulationResponse, error) {
	if err := c.allow("getEricTestSimulation"); err != nil {
		return nil, err
	}
	if tenantId.String() != c.tenant {
		return nil, errors.New("test tenant path does not match selected tenant")
	}
	r, err := c.gentest.GetEricTestSimulationWithResponse(ctx, tenantId, productId, simulationId, params)
	if err != nil {
		return nil, err
	}
	if r.StatusCode() != 200 {
		return nil, c.problem(r.StatusCode(), r.Body, r.HTTPResponse)
	}
	return r, nil
}
