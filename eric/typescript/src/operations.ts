// Generated from the pinned public catalog.
export const operations = {
  "GetUserNotices": {
    "method": "GET",
    "path": "/products/{productId}/notices",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "CreateProfile": {
    "method": "POST",
    "path": "/products/{productId}/profiles",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetProfile": {
    "method": "GET",
    "path": "/products/{productId}/profiles/{version}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "version",
        "wire": "version",
        "in": "path",
        "required": true,
        "pattern": "^[1-9][0-9]{0,9}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "CreateDraft": {
    "method": "POST",
    "path": "/products/{productId}/drafts",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "ReviseDraft": {
    "method": "PUT",
    "path": "/products/{productId}/drafts/{draftId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "draftId",
        "wire": "draftId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetDraft": {
    "method": "GET",
    "path": "/products/{productId}/drafts/{draftId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "draftId",
        "wire": "draftId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetDraftRevision": {
    "method": "GET",
    "path": "/products/{productId}/drafts/{draftId}/revisions/{revision}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "draftId",
        "wire": "draftId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "revision",
        "wire": "revision",
        "in": "path",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "CreatePreparation": {
    "method": "POST",
    "path": "/products/{productId}/preparations",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetPreparation": {
    "method": "GET",
    "path": "/products/{productId}/preparations/{preparationId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "preparationId",
        "wire": "preparationId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetPreparationArtifact": {
    "method": "GET",
    "path": "/products/{productId}/preparations/{preparationId}/artifacts/{kind}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "preparationId",
        "wire": "preparationId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "kind",
        "wire": "kind",
        "in": "path",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/xml",
    "profile": "production",
    "artifact": true,
    "contentLength": false
  },
  "CreateValidation": {
    "method": "POST",
    "path": "/products/{productId}/validations",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 202,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetValidation": {
    "method": "GET",
    "path": "/products/{productId}/validations/{validationId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "validationId",
        "wire": "validationId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetValidationArtifact": {
    "method": "GET",
    "path": "/products/{productId}/validations/{validationId}/artifacts/{kind}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "validationId",
        "wire": "validationId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "kind",
        "wire": "kind",
        "in": "path",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/xml",
    "profile": "production",
    "artifact": true,
    "contentLength": false
  },
  "CreateDelegatedReview": {
    "method": "POST",
    "path": "/products/{productId}/preparations/{preparationId}/delegated-reviews",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "preparationId",
        "wire": "preparationId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetDelegatedReview": {
    "method": "GET",
    "path": "/products/{productId}/delegated-reviews/{reviewId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "reviewId",
        "wire": "reviewId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "ConfirmDelegatedReview": {
    "method": "POST",
    "path": "/products/{productId}/delegated-reviews/{reviewId}/confirmations",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "reviewId",
        "wire": "reviewId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "RevokeDelegatedReview": {
    "method": "POST",
    "path": "/products/{productId}/delegated-reviews/{reviewId}/revocations",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "reviewId",
        "wire": "reviewId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetUStVAFieldCatalog": {
    "method": "GET",
    "path": "/products/{productId}/modules/ustva-2026/field-catalog",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "CreateUtility": {
    "method": "POST",
    "path": "/products/{productId}/utilities",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 202,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetUtility": {
    "method": "GET",
    "path": "/products/{productId}/utilities/{utilityId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "utilityId",
        "wire": "utilityId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "CreateCredentialIntake": {
    "method": "POST",
    "path": "/products/{productId}/credential-intakes",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetSoftwareCredential": {
    "method": "GET",
    "path": "/products/{productId}/credentials/{credentialId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "credentialId",
        "wire": "credentialId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricCredentialOrigin",
        "wire": "X-ERIC-Credential-Origin",
        "in": "header",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "RevokeSoftwareCredential": {
    "method": "POST",
    "path": "/products/{productId}/credentials/{credentialId}/revoke",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "credentialId",
        "wire": "credentialId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "xEricCredentialOrigin",
        "wire": "X-ERIC-Credential-Origin",
        "in": "header",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetUStVADerivedRules": {
    "method": "GET",
    "path": "/products/{productId}/modules/ustva-2026/derived-rules",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "CreateFilingConsent": {
    "method": "POST",
    "path": "/products/{productId}/preparations/{preparationId}/filing-consents",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "preparationId",
        "wire": "preparationId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "xEricHumanAuthorization",
        "wire": "X-ERIC-Human-Authorization",
        "in": "header",
        "required": false
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "xEricReplayOnly",
        "wire": "X-ERIC-Replay-Only",
        "in": "header",
        "required": false
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetFilingConsent": {
    "method": "GET",
    "path": "/products/{productId}/filing-consents/{consentId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "consentId",
        "wire": "consentId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "xEricHumanAuthorization",
        "wire": "X-ERIC-Human-Authorization",
        "in": "header",
        "required": false
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "ConfirmFilingConsent": {
    "method": "POST",
    "path": "/products/{productId}/filing-consents/{consentId}/confirmations",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "consentId",
        "wire": "consentId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "xEricHumanAuthorization",
        "wire": "X-ERIC-Human-Authorization",
        "in": "header",
        "required": false
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "RevokeFilingConsent": {
    "method": "POST",
    "path": "/products/{productId}/filing-consents/{consentId}/revocations",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "consentId",
        "wire": "consentId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "xEricHumanAuthorization",
        "wire": "X-ERIC-Human-Authorization",
        "in": "header",
        "required": false
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetCredentialOperation": {
    "method": "GET",
    "path": "/products/{productId}/credential-operations/{intakeId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "intakeId",
        "wire": "intakeId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricCredentialOrigin",
        "wire": "X-ERIC-Credential-Origin",
        "in": "header",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetRetrievalArtifact": {
    "method": "GET",
    "path": "/products/{productId}/retrieval-artifacts/{artifactId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "artifactId",
        "wire": "artifactId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetRetrievalArtifactContent": {
    "method": "GET",
    "path": "/products/{productId}/retrieval-artifacts/{artifactId}/{kind}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "artifactId",
        "wire": "artifactId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "kind",
        "wire": "kind",
        "in": "path",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/octet-stream",
    "profile": "production",
    "artifact": true,
    "contentLength": true
  },
  "CreateRetrievalArchiveAcknowledgement": {
    "method": "POST",
    "path": "/products/{productId}/retrieval-artifacts/{artifactId}/archive-acknowledgement",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "artifactId",
        "wire": "artifactId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "CreateUStVAMapping": {
    "method": "POST",
    "path": "/products/{productId}/mappings",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "ReviseUStVAMapping": {
    "method": "PUT",
    "path": "/products/{productId}/mappings/{mappingId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "mappingId",
        "wire": "mappingId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetUStVAMapping": {
    "method": "GET",
    "path": "/products/{productId}/mappings/{mappingId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "mappingId",
        "wire": "mappingId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetUStVAMappingRevision": {
    "method": "GET",
    "path": "/products/{productId}/mappings/{mappingId}/revisions/{revision}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "mappingId",
        "wire": "mappingId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
      },
      {
        "name": "revision",
        "wire": "revision",
        "in": "path",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "ConfirmUStVAMapping": {
    "method": "POST",
    "path": "/products/{productId}/mappings/{mappingId}/revisions/{revision}/confirmations",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "mappingId",
        "wire": "mappingId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
      },
      {
        "name": "revision",
        "wire": "revision",
        "in": "path",
        "required": true
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "WithdrawUStVAMapping": {
    "method": "POST",
    "path": "/products/{productId}/mappings/{mappingId}/revisions/{revision}/withdrawals",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "mappingId",
        "wire": "mappingId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
      },
      {
        "name": "revision",
        "wire": "revision",
        "in": "path",
        "required": true
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "CreateEBilanzMapping": {
    "method": "POST",
    "path": "/products/{productId}/ebilanz-mappings",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "ReviseEBilanzMapping": {
    "method": "PUT",
    "path": "/products/{productId}/ebilanz-mappings/{mappingId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "mappingId",
        "wire": "mappingId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetEBilanzMapping": {
    "method": "GET",
    "path": "/products/{productId}/ebilanz-mappings/{mappingId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "mappingId",
        "wire": "mappingId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetEBilanzMappingRevision": {
    "method": "GET",
    "path": "/products/{productId}/ebilanz-mappings/{mappingId}/revisions/{revision}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "mappingId",
        "wire": "mappingId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
      },
      {
        "name": "revision",
        "wire": "revision",
        "in": "path",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "ConfirmEBilanzMapping": {
    "method": "POST",
    "path": "/products/{productId}/ebilanz-mappings/{mappingId}/revisions/{revision}/confirmations",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "mappingId",
        "wire": "mappingId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
      },
      {
        "name": "revision",
        "wire": "revision",
        "in": "path",
        "required": true
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "WithdrawEBilanzMapping": {
    "method": "POST",
    "path": "/products/{productId}/ebilanz-mappings/{mappingId}/revisions/{revision}/withdrawals",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "mappingId",
        "wire": "mappingId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
      },
      {
        "name": "revision",
        "wire": "revision",
        "in": "path",
        "required": true
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetEBilanzMappingCatalog": {
    "method": "GET",
    "path": "/products/{productId}/modules/ebilanz-6.9/mapping-catalog",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "CreateRetrievalDecryption": {
    "method": "POST",
    "path": "/products/{productId}/retrieval-decryptions",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 202,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "GetRetrievalDecryption": {
    "method": "GET",
    "path": "/products/{productId}/retrieval-decryptions/{decryptionId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "decryptionId",
        "wire": "decryptionId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "CreateRetrievalPreservation": {
    "method": "POST",
    "path": "/products/{productId}/retrieval-decryptions/{decryptionId}/preservation",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "xEricActorStatus",
        "wire": "X-ERIC-Actor-Status",
        "in": "header",
        "required": true
      },
      {
        "name": "decryptionId",
        "wire": "decryptionId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 201,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "PlanEBilanzForm": {
    "method": "POST",
    "path": "/products/{productId}/modules/ebilanz-6.9/form-plan",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 200,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "production",
    "artifact": false,
    "contentLength": false
  },
  "createEricTestSimulation": {
    "method": "POST",
    "path": "/v1/tenants/{tenantId}/products/{productId}/simulations",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "format": "uuid"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true,
        "pattern": "^[A-Za-z0-9._:-]{1,128}$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 202,
    "bodyType": "application/json",
    "responseType": "application/json",
    "profile": "test",
    "artifact": false,
    "contentLength": false
  },
  "getEricTestSimulation": {
    "method": "GET",
    "path": "/v1/tenants/{tenantId}/products/{productId}/simulations/{simulationId}",
    "params": [
      {
        "name": "productId",
        "wire": "productId",
        "in": "path",
        "required": true,
        "format": "uuid"
      },
      {
        "name": "simulationId",
        "wire": "simulationId",
        "in": "path",
        "required": true,
        "format": "uuid"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "profile": "test",
    "artifact": false,
    "contentLength": false
  }
} as const;
