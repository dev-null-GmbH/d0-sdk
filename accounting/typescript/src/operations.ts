// Generated from the pinned public catalog.
export const operations = {
  "listTaxRules": {
    "method": "GET",
    "path": "/tax-rules",
    "params": [
      {
        "name": "limit",
        "wire": "limit",
        "in": "query",
        "required": false
      },
      {
        "name": "after",
        "wire": "after",
        "in": "query",
        "required": false
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "calculateTax": {
    "method": "POST",
    "path": "/tax-calculations",
    "params": [
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "getFinancialStatements": {
    "method": "GET",
    "path": "/reports/financial-statements",
    "params": [
      {
        "name": "fiscalYearId",
        "wire": "fiscalYearId",
        "in": "query",
        "required": true,
        "pattern": "^fy_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "mappingRevisionId",
        "wire": "mappingRevisionId",
        "in": "query",
        "required": true,
        "pattern": "^map_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "asOf",
        "wire": "asOf",
        "in": "query",
        "required": false,
        "pattern": "^(empty|je_[0-9A-HJKMNP-TV-Z]{26})$"
      },
      {
        "name": "currency",
        "wire": "currency",
        "in": "query",
        "required": false,
        "pattern": "^[A-Z]{3}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "listFiscalYears": {
    "method": "GET",
    "path": "/fiscal-years",
    "params": [
      {
        "name": "limit",
        "wire": "limit",
        "in": "query",
        "required": false
      },
      {
        "name": "after",
        "wire": "after",
        "in": "query",
        "required": false,
        "pattern": "^fy_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "createFiscalYear": {
    "method": "POST",
    "path": "/fiscal-years",
    "params": [
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "getFiscalYear": {
    "method": "GET",
    "path": "/fiscal-years/{yearId}",
    "params": [
      {
        "name": "yearId",
        "wire": "yearId",
        "in": "path",
        "required": true,
        "pattern": "^fy_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "finalizeFiscalYear": {
    "method": "POST",
    "path": "/fiscal-years/{yearId}/finalize",
    "params": [
      {
        "name": "yearId",
        "wire": "yearId",
        "in": "path",
        "required": true,
        "pattern": "^fy_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "closeFiscalYear": {
    "method": "POST",
    "path": "/fiscal-years/{yearId}/close",
    "params": [
      {
        "name": "yearId",
        "wire": "yearId",
        "in": "path",
        "required": true,
        "pattern": "^fy_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "carryforwardFiscalYear": {
    "method": "POST",
    "path": "/fiscal-years/{yearId}/carryforward",
    "params": [
      {
        "name": "yearId",
        "wire": "yearId",
        "in": "path",
        "required": true,
        "pattern": "^fy_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "getTrialBalance": {
    "method": "GET",
    "path": "/reports/trial-balance",
    "params": [
      {
        "name": "asOf",
        "wire": "asOf",
        "in": "query",
        "required": false,
        "pattern": "^(empty|je_[0-9A-HJKMNP-TV-Z]{26})$"
      },
      {
        "name": "currency",
        "wire": "currency",
        "in": "query",
        "required": false,
        "pattern": "^[A-Z]{3}$"
      },
      {
        "name": "bookingDateFrom",
        "wire": "bookingDateFrom",
        "in": "query",
        "required": false
      },
      {
        "name": "bookingDateTo",
        "wire": "bookingDateTo",
        "in": "query",
        "required": false
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": true
  },
  "listAccountMappings": {
    "method": "GET",
    "path": "/account-mappings",
    "params": [
      {
        "name": "limit",
        "wire": "limit",
        "in": "query",
        "required": false
      },
      {
        "name": "after",
        "wire": "after",
        "in": "query",
        "required": false,
        "pattern": "^map_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "publishAccountMapping": {
    "method": "POST",
    "path": "/account-mappings",
    "params": [
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "getAccountMapping": {
    "method": "GET",
    "path": "/account-mappings/{mappingId}",
    "params": [
      {
        "name": "mappingId",
        "wire": "mappingId",
        "in": "path",
        "required": true,
        "pattern": "^map_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "retireAccount": {
    "method": "POST",
    "path": "/accounts/{accountId}/retire",
    "params": [
      {
        "name": "accountId",
        "wire": "accountId",
        "in": "path",
        "required": true,
        "pattern": "^acct_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "downloadTenantExport": {
    "method": "GET",
    "path": "/exports/tenant",
    "params": [],
    "status": 200,
    "bodyType": "",
    "responseType": "application/zip",
    "test": false
  },
  "listTenants": {
    "method": "GET",
    "path": "/tenants",
    "params": [
      {
        "name": "limit",
        "wire": "limit",
        "in": "query",
        "required": false
      },
      {
        "name": "after",
        "wire": "after",
        "in": "query",
        "required": false,
        "pattern": "^ten_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "createTenant": {
    "method": "POST",
    "path": "/tenants",
    "params": [
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "listMemberships": {
    "method": "GET",
    "path": "/tenants/{tenantId}/memberships",
    "params": [
      {
        "name": "tenantId",
        "wire": "tenantId",
        "in": "path",
        "required": true,
        "pattern": "^ten_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "limit",
        "wire": "limit",
        "in": "query",
        "required": false
      },
      {
        "name": "after",
        "wire": "after",
        "in": "query",
        "required": false,
        "pattern": "^mem_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "createMembership": {
    "method": "POST",
    "path": "/tenants/{tenantId}/memberships",
    "params": [
      {
        "name": "tenantId",
        "wire": "tenantId",
        "in": "path",
        "required": true,
        "pattern": "^ten_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "replaceMembership": {
    "method": "PUT",
    "path": "/tenants/{tenantId}/memberships/{membershipId}",
    "params": [
      {
        "name": "tenantId",
        "wire": "tenantId",
        "in": "path",
        "required": true,
        "pattern": "^ten_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "membershipId",
        "wire": "membershipId",
        "in": "path",
        "required": true,
        "pattern": "^mem_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "listAccounts": {
    "method": "GET",
    "path": "/accounts",
    "params": [
      {
        "name": "limit",
        "wire": "limit",
        "in": "query",
        "required": false
      },
      {
        "name": "after",
        "wire": "after",
        "in": "query",
        "required": false,
        "pattern": "^acct_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": true
  },
  "createAccount": {
    "method": "POST",
    "path": "/accounts",
    "params": [
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": true
  },
  "getAccount": {
    "method": "GET",
    "path": "/accounts/{accountId}",
    "params": [
      {
        "name": "accountId",
        "wire": "accountId",
        "in": "path",
        "required": true,
        "pattern": "^acct_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": true
  },
  "getAccountStatement": {
    "method": "GET",
    "path": "/accounts/{accountId}/statement",
    "params": [
      {
        "name": "accountId",
        "wire": "accountId",
        "in": "path",
        "required": true,
        "pattern": "^acct_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "limit",
        "wire": "limit",
        "in": "query",
        "required": false
      },
      {
        "name": "asOf",
        "wire": "asOf",
        "in": "query",
        "required": false,
        "pattern": "^(empty|je_[0-9A-HJKMNP-TV-Z]{26})$"
      },
      {
        "name": "currency",
        "wire": "currency",
        "in": "query",
        "required": false,
        "pattern": "^[A-Z]{3}$"
      },
      {
        "name": "bookingDateFrom",
        "wire": "bookingDateFrom",
        "in": "query",
        "required": false
      },
      {
        "name": "bookingDateTo",
        "wire": "bookingDateTo",
        "in": "query",
        "required": false
      },
      {
        "name": "after",
        "wire": "after",
        "in": "query",
        "required": false
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "getAccountBalances": {
    "method": "GET",
    "path": "/accounts/{accountId}/balances",
    "params": [
      {
        "name": "accountId",
        "wire": "accountId",
        "in": "path",
        "required": true,
        "pattern": "^acct_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "asOf",
        "wire": "asOf",
        "in": "query",
        "required": false,
        "pattern": "^(empty|je_[0-9A-HJKMNP-TV-Z]{26})$"
      },
      {
        "name": "currency",
        "wire": "currency",
        "in": "query",
        "required": false,
        "pattern": "^[A-Z]{3}$"
      },
      {
        "name": "bookingDateFrom",
        "wire": "bookingDateFrom",
        "in": "query",
        "required": false
      },
      {
        "name": "bookingDateTo",
        "wire": "bookingDateTo",
        "in": "query",
        "required": false
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "listPeriods": {
    "method": "GET",
    "path": "/periods",
    "params": [
      {
        "name": "limit",
        "wire": "limit",
        "in": "query",
        "required": false
      },
      {
        "name": "after",
        "wire": "after",
        "in": "query",
        "required": false,
        "pattern": "^per_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": true
  },
  "createPeriod": {
    "method": "POST",
    "path": "/periods",
    "params": [
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": true
  },
  "getPeriod": {
    "method": "GET",
    "path": "/periods/{periodId}",
    "params": [
      {
        "name": "periodId",
        "wire": "periodId",
        "in": "path",
        "required": true,
        "pattern": "^per_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": true
  },
  "festschreibenPeriod": {
    "method": "POST",
    "path": "/periods/{periodId}/festschreiben",
    "params": [
      {
        "name": "periodId",
        "wire": "periodId",
        "in": "path",
        "required": true,
        "pattern": "^per_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "listJournalEntries": {
    "method": "GET",
    "path": "/journal-entries",
    "params": [
      {
        "name": "limit",
        "wire": "limit",
        "in": "query",
        "required": false
      },
      {
        "name": "after",
        "wire": "after",
        "in": "query",
        "required": false,
        "pattern": "^je_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "status",
        "wire": "status",
        "in": "query",
        "required": true
      },
      {
        "name": "periodId",
        "wire": "periodId",
        "in": "query",
        "required": false,
        "pattern": "^per_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "documentId",
        "wire": "documentId",
        "in": "query",
        "required": false,
        "pattern": "^doc_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "bookingDateFrom",
        "wire": "bookingDateFrom",
        "in": "query",
        "required": false
      },
      {
        "name": "bookingDateTo",
        "wire": "bookingDateTo",
        "in": "query",
        "required": false
      },
      {
        "name": "externalReference",
        "wire": "externalReference",
        "in": "query",
        "required": false
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": true
  },
  "createJournalEntryDraft": {
    "method": "POST",
    "path": "/journal-entries",
    "params": [
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": true
  },
  "getJournalEntry": {
    "method": "GET",
    "path": "/journal-entries/{entryId}",
    "params": [
      {
        "name": "entryId",
        "wire": "entryId",
        "in": "path",
        "required": true,
        "pattern": "^je_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": true
  },
  "replaceJournalEntryDraft": {
    "method": "PUT",
    "path": "/journal-entries/{entryId}",
    "params": [
      {
        "name": "entryId",
        "wire": "entryId",
        "in": "path",
        "required": true,
        "pattern": "^je_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "ifMatch",
        "wire": "If-Match",
        "in": "header",
        "required": true,
        "pattern": "^\"je-v1-[A-Za-z0-9_-]{32}\"$"
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
    "test": true
  },
  "discardJournalEntryDraft": {
    "method": "DELETE",
    "path": "/journal-entries/{entryId}",
    "params": [
      {
        "name": "entryId",
        "wire": "entryId",
        "in": "path",
        "required": true,
        "pattern": "^je_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "ifMatch",
        "wire": "If-Match",
        "in": "header",
        "required": true,
        "pattern": "^\"je-v1-[A-Za-z0-9_-]{32}\"$"
      }
    ],
    "status": 204,
    "bodyType": "",
    "responseType": "",
    "test": true
  },
  "postJournalEntry": {
    "method": "POST",
    "path": "/journal-entries/{entryId}/post",
    "params": [
      {
        "name": "entryId",
        "wire": "entryId",
        "in": "path",
        "required": true,
        "pattern": "^je_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "ifMatch",
        "wire": "If-Match",
        "in": "header",
        "required": false,
        "pattern": "^\"je-v1-[A-Za-z0-9_-]{32}\"$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "reverseJournalEntry": {
    "method": "POST",
    "path": "/journal-entries/{entryId}/reverse",
    "params": [
      {
        "name": "entryId",
        "wire": "entryId",
        "in": "path",
        "required": true,
        "pattern": "^je_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "linkJournalEntryDocument": {
    "method": "POST",
    "path": "/journal-entries/{entryId}/documents/{documentId}",
    "params": [
      {
        "name": "entryId",
        "wire": "entryId",
        "in": "path",
        "required": true,
        "pattern": "^je_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "documentId",
        "wire": "documentId",
        "in": "path",
        "required": true,
        "pattern": "^doc_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      }
    ],
    "status": 204,
    "bodyType": "",
    "responseType": "",
    "test": false
  },
  "listDocuments": {
    "method": "GET",
    "path": "/documents",
    "params": [
      {
        "name": "limit",
        "wire": "limit",
        "in": "query",
        "required": false
      },
      {
        "name": "after",
        "wire": "after",
        "in": "query",
        "required": false,
        "pattern": "^doc_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "status",
        "wire": "status",
        "in": "query",
        "required": false
      },
      {
        "name": "origin",
        "wire": "origin",
        "in": "query",
        "required": false
      },
      {
        "name": "documentDateFrom",
        "wire": "documentDateFrom",
        "in": "query",
        "required": false
      },
      {
        "name": "documentDateTo",
        "wire": "documentDateTo",
        "in": "query",
        "required": false
      },
      {
        "name": "journalEntryId",
        "wire": "journalEntryId",
        "in": "query",
        "required": false,
        "pattern": "^je_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "sourceDocumentId",
        "wire": "sourceDocumentId",
        "in": "query",
        "required": false,
        "pattern": "^doc_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "createDocument": {
    "method": "POST",
    "path": "/documents",
    "params": [
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "listDocumentSources": {
    "method": "GET",
    "path": "/documents/{documentId}/sources",
    "params": [
      {
        "name": "documentId",
        "wire": "documentId",
        "in": "path",
        "required": true,
        "pattern": "^doc_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "getDocument": {
    "method": "GET",
    "path": "/documents/{documentId}",
    "params": [
      {
        "name": "documentId",
        "wire": "documentId",
        "in": "path",
        "required": true,
        "pattern": "^doc_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "downloadDocument": {
    "method": "GET",
    "path": "/documents/{documentId}/content",
    "params": [
      {
        "name": "documentId",
        "wire": "documentId",
        "in": "path",
        "required": true,
        "pattern": "^doc_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/octet-stream",
    "test": false
  },
  "createDocumentUploadRequest": {
    "method": "POST",
    "path": "/documents/{documentId}/upload-requests",
    "params": [
      {
        "name": "documentId",
        "wire": "documentId",
        "in": "path",
        "required": true,
        "pattern": "^doc_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "completeDocument": {
    "method": "POST",
    "path": "/documents/{documentId}/complete",
    "params": [
      {
        "name": "documentId",
        "wire": "documentId",
        "in": "path",
        "required": true,
        "pattern": "^doc_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "createDocumentPreservation": {
    "method": "POST",
    "path": "/documents/{documentId}/preservation-requests",
    "params": [
      {
        "name": "documentId",
        "wire": "documentId",
        "in": "path",
        "required": true,
        "pattern": "^doc_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "getDocumentPreservation": {
    "method": "GET",
    "path": "/document-preservation-requests/{preservationId}",
    "params": [
      {
        "name": "preservationId",
        "wire": "preservationId",
        "in": "path",
        "required": true,
        "pattern": "^prsv_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "createEInvoiceValidation": {
    "method": "POST",
    "path": "/documents/{documentId}/e-invoice-validations",
    "params": [
      {
        "name": "documentId",
        "wire": "documentId",
        "in": "path",
        "required": true,
        "pattern": "^doc_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      }
    ],
    "status": 202,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "getEInvoiceValidation": {
    "method": "GET",
    "path": "/e-invoice-validations/{validationId}",
    "params": [
      {
        "name": "validationId",
        "wire": "validationId",
        "in": "path",
        "required": true,
        "pattern": "^eiv_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "createZUGFeRDPDF": {
    "method": "POST",
    "path": "/e-invoice-validations/{validationId}/zugferd-pdfs",
    "params": [
      {
        "name": "validationId",
        "wire": "validationId",
        "in": "path",
        "required": true,
        "pattern": "^eiv_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "getZUGFeRDPDF": {
    "method": "GET",
    "path": "/zugferd-pdfs/{zugferdPdfId}",
    "params": [
      {
        "name": "zugferdPdfId",
        "wire": "zugferdPdfId",
        "in": "path",
        "required": true,
        "pattern": "^eip_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "listWebhookEndpoints": {
    "method": "GET",
    "path": "/webhook-endpoints",
    "params": [
      {
        "name": "limit",
        "wire": "limit",
        "in": "query",
        "required": false
      },
      {
        "name": "after",
        "wire": "after",
        "in": "query",
        "required": false,
        "pattern": "^whep_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "createWebhookEndpoint": {
    "method": "POST",
    "path": "/webhook-endpoints",
    "params": [
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
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
    "test": false
  },
  "getWebhookEndpoint": {
    "method": "GET",
    "path": "/webhook-endpoints/{webhookEndpointId}",
    "params": [
      {
        "name": "webhookEndpointId",
        "wire": "webhookEndpointId",
        "in": "path",
        "required": true,
        "pattern": "^whep_[0-9A-HJKMNP-TV-Z]{26}$"
      }
    ],
    "status": 200,
    "bodyType": "",
    "responseType": "application/json",
    "test": false
  },
  "replaceWebhookEndpoint": {
    "method": "PUT",
    "path": "/webhook-endpoints/{webhookEndpointId}",
    "params": [
      {
        "name": "webhookEndpointId",
        "wire": "webhookEndpointId",
        "in": "path",
        "required": true,
        "pattern": "^whep_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "ifMatch",
        "wire": "If-Match",
        "in": "header",
        "required": true,
        "pattern": "^\"whep-v1-[A-Za-z0-9_-]{32}\"$"
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
    "test": false
  },
  "deleteWebhookEndpoint": {
    "method": "DELETE",
    "path": "/webhook-endpoints/{webhookEndpointId}",
    "params": [
      {
        "name": "webhookEndpointId",
        "wire": "webhookEndpointId",
        "in": "path",
        "required": true,
        "pattern": "^whep_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "ifMatch",
        "wire": "If-Match",
        "in": "header",
        "required": true,
        "pattern": "^\"whep-v1-[A-Za-z0-9_-]{32}\"$"
      }
    ],
    "status": 204,
    "bodyType": "",
    "responseType": "",
    "test": false
  },
  "rotateWebhookEndpointSecret": {
    "method": "PUT",
    "path": "/webhook-endpoints/{webhookEndpointId}/secret",
    "params": [
      {
        "name": "webhookEndpointId",
        "wire": "webhookEndpointId",
        "in": "path",
        "required": true,
        "pattern": "^whep_[0-9A-HJKMNP-TV-Z]{26}$"
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "xAccountingActingUserIssuer",
        "wire": "X-Accounting-Acting-User-Issuer",
        "in": "header",
        "required": false,
        "pattern": "^https://[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "xAccountingActingUserSubject",
        "wire": "X-Accounting-Acting-User-Subject",
        "in": "header",
        "required": false,
        "pattern": "^[\\x21-\\x2B\\x2D-\\x7E]+$"
      },
      {
        "name": "ifMatch",
        "wire": "If-Match",
        "in": "header",
        "required": true,
        "pattern": "^\"whep-v1-[A-Za-z0-9_-]{32}\"$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ],
    "status": 204,
    "bodyType": "application/json",
    "responseType": "",
    "test": false
  }
} as const;
