// Generated from the pinned machine contract.
export const operations = {
  "listAuditEvents": {
    "scope": "platform.audit.read",
    "method": "GET",
    "path": "/audit/events",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "limit",
        "wire": "limit",
        "in": "query",
        "required": false,
        "minimum": 1,
        "maximum": 500
      },
      {
        "name": "before",
        "wire": "before",
        "in": "query",
        "required": false,
        "maxLength": 1024
      }
    ]
  },
  "getClusterCatalog": {
    "scope": "platform.clusters.read",
    "method": "GET",
    "path": "/cluster-plans",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": []
  },
  "quoteCluster": {
    "scope": "platform.clusters.read",
    "method": "POST",
    "path": "/cluster-quote",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "application/json",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ]
  },
  "listClusters": {
    "scope": "platform.clusters.read",
    "method": "GET",
    "path": "/clusters",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": []
  },
  "deleteCluster": {
    "scope": "platform.clusters.write",
    "method": "DELETE",
    "path": "/clusters/{id}",
    "status": 202,
    "statuses": [
      202
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "id",
        "wire": "id",
        "in": "path",
        "required": true
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      }
    ]
  },
  "getCluster": {
    "scope": "platform.clusters.read",
    "method": "GET",
    "path": "/clusters/{id}",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "id",
        "wire": "id",
        "in": "path",
        "required": true
      }
    ]
  },
  "getClusterKubeconfig": {
    "scope": "platform.clusters.credentials",
    "method": "GET",
    "path": "/clusters/{id}/kubeconfig",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "id",
        "wire": "id",
        "in": "path",
        "required": true
      }
    ]
  },
  "rotateClusterKubeconfig": {
    "scope": "platform.clusters.credentials",
    "method": "POST",
    "path": "/clusters/{id}/kubeconfig:rotate",
    "status": 202,
    "statuses": [
      202
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "id",
        "wire": "id",
        "in": "path",
        "required": true
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      }
    ]
  },
  "resizeCluster": {
    "scope": "platform.clusters.write",
    "method": "POST",
    "path": "/clusters/{id}/resize",
    "status": 202,
    "statuses": [
      202
    ],
    "emptyStatuses": [],
    "bodyType": "application/json",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "id",
        "wire": "id",
        "in": "path",
        "required": true
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ]
  },
  "resumeCluster": {
    "scope": "platform.clusters.write",
    "method": "POST",
    "path": "/clusters/{id}/resume",
    "status": 202,
    "statuses": [
      202
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "id",
        "wire": "id",
        "in": "path",
        "required": true
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      }
    ]
  },
  "suspendCluster": {
    "scope": "platform.clusters.write",
    "method": "POST",
    "path": "/clusters/{id}/suspend",
    "status": 202,
    "statuses": [
      202
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "id",
        "wire": "id",
        "in": "path",
        "required": true
      },
      {
        "name": "idempotencyKey",
        "wire": "Idempotency-Key",
        "in": "header",
        "required": true
      }
    ]
  },
  "getDeveloperLimits": {
    "scope": "platform.usage.read",
    "method": "GET",
    "path": "/developers/limits",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": []
  },
  "getDeveloperUsage": {
    "scope": "platform.usage.read",
    "method": "GET",
    "path": "/developers/usage",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "product",
        "wire": "product",
        "in": "query",
        "required": false,
        "maxLength": 64
      },
      {
        "name": "environment",
        "wire": "environment",
        "in": "query",
        "required": false,
        "enum": [
          "production",
          "test"
        ]
      },
      {
        "name": "client_id",
        "wire": "client_id",
        "in": "query",
        "required": false,
        "maxLength": 128
      },
      {
        "name": "from_",
        "wire": "from",
        "in": "query",
        "required": false
      },
      {
        "name": "until",
        "wire": "until",
        "in": "query",
        "required": false
      }
    ]
  },
  "listDomains": {
    "scope": "platform.domains.read",
    "method": "GET",
    "path": "/domains",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": true,
    "params": []
  },
  "getDomain": {
    "scope": "platform.domains.read",
    "method": "GET",
    "path": "/domains/{domain}",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": true,
    "params": [
      {
        "name": "domain",
        "wire": "domain",
        "in": "path",
        "required": true,
        "pattern": "^[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)+$",
        "maxLength": 253,
        "minLength": 3
      }
    ]
  },
  "getDomainAuthCode": {
    "scope": "platform.domains.authcode",
    "method": "GET",
    "path": "/domains/{domain}/authcode",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "domain",
        "wire": "domain",
        "in": "path",
        "required": true,
        "pattern": "^[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)+$",
        "maxLength": 253,
        "minLength": 3
      }
    ]
  },
  "resetDomainAuthCode": {
    "scope": "platform.domains.authcode",
    "method": "POST",
    "path": "/domains/{domain}/authcode/reset",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "domain",
        "wire": "domain",
        "in": "path",
        "required": true,
        "pattern": "^[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)+$",
        "maxLength": 253,
        "minLength": 3
      }
    ]
  },
  "getDomainContacts": {
    "scope": "platform.domains.read",
    "method": "GET",
    "path": "/domains/{domain}/contacts",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "domain",
        "wire": "domain",
        "in": "path",
        "required": true,
        "pattern": "^[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)+$",
        "maxLength": 253,
        "minLength": 3
      }
    ]
  },
  "updateDomainContacts": {
    "scope": "platform.domains.write",
    "method": "PUT",
    "path": "/domains/{domain}/contacts",
    "status": 204,
    "statuses": [
      204
    ],
    "emptyStatuses": [
      204
    ],
    "bodyType": "application/json",
    "responseType": "",
    "test": false,
    "params": [
      {
        "name": "domain",
        "wire": "domain",
        "in": "path",
        "required": true,
        "pattern": "^[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)+$",
        "maxLength": 253,
        "minLength": 3
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ]
  },
  "listDNSRecords": {
    "scope": "platform.dns.read",
    "method": "GET",
    "path": "/domains/{domain}/dns/records",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": true,
    "params": [
      {
        "name": "domain",
        "wire": "domain",
        "in": "path",
        "required": true,
        "pattern": "^[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)+$",
        "maxLength": 253,
        "minLength": 3
      }
    ]
  },
  "deleteDNSRecord": {
    "scope": "platform.dns.write",
    "method": "DELETE",
    "path": "/domains/{domain}/dns/records/{name}/{type}",
    "status": 204,
    "statuses": [
      204
    ],
    "emptyStatuses": [
      204
    ],
    "bodyType": "",
    "responseType": "",
    "test": true,
    "params": [
      {
        "name": "domain",
        "wire": "domain",
        "in": "path",
        "required": true,
        "pattern": "^[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)+$",
        "maxLength": 253,
        "minLength": 3
      },
      {
        "name": "name",
        "wire": "name",
        "in": "path",
        "required": true,
        "maxLength": 253
      },
      {
        "name": "type",
        "wire": "type",
        "in": "path",
        "required": true,
        "pattern": "^[A-Za-z]+$"
      }
    ]
  },
  "upsertDNSRecord": {
    "scope": "platform.dns.write",
    "method": "PUT",
    "path": "/domains/{domain}/dns/records/{name}/{type}",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "application/json",
    "responseType": "application/json",
    "test": true,
    "params": [
      {
        "name": "domain",
        "wire": "domain",
        "in": "path",
        "required": true,
        "pattern": "^[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)+$",
        "maxLength": 253,
        "minLength": 3
      },
      {
        "name": "name",
        "wire": "name",
        "in": "path",
        "required": true,
        "maxLength": 253
      },
      {
        "name": "type",
        "wire": "type",
        "in": "path",
        "required": true,
        "pattern": "^[A-Za-z]+$"
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ]
  },
  "setDomainNameservers": {
    "scope": "platform.domains.write",
    "method": "PUT",
    "path": "/domains/{domain}/nameservers",
    "status": 204,
    "statuses": [
      204
    ],
    "emptyStatuses": [
      204
    ],
    "bodyType": "application/json",
    "responseType": "",
    "test": false,
    "params": [
      {
        "name": "domain",
        "wire": "domain",
        "in": "path",
        "required": true,
        "pattern": "^[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)+$",
        "maxLength": 253,
        "minLength": 3
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ]
  },
  "getObjectStorageCatalog": {
    "scope": "platform.storage.read",
    "method": "GET",
    "path": "/object-storage",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": []
  },
  "listObjectStorageBuckets": {
    "scope": "platform.storage.read",
    "method": "GET",
    "path": "/object-storage/buckets",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": []
  },
  "createObjectStorageBucket": {
    "scope": "platform.storage.write",
    "method": "POST",
    "path": "/object-storage/buckets",
    "status": 201,
    "statuses": [
      201,
      202
    ],
    "emptyStatuses": [
      202
    ],
    "bodyType": "application/json",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ]
  },
  "deleteObjectStorageBucket": {
    "scope": "platform.storage.write",
    "method": "DELETE",
    "path": "/object-storage/buckets/{id}",
    "status": 202,
    "statuses": [
      202,
      204
    ],
    "emptyStatuses": [
      202,
      204
    ],
    "bodyType": "",
    "responseType": "",
    "test": false,
    "params": [
      {
        "name": "id",
        "wire": "id",
        "in": "path",
        "required": true
      }
    ]
  },
  "listObjectStorageCredentials": {
    "scope": "platform.storage.credentials",
    "method": "GET",
    "path": "/object-storage/buckets/{id}/credentials",
    "status": 200,
    "statuses": [
      200
    ],
    "emptyStatuses": [],
    "bodyType": "",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "id",
        "wire": "id",
        "in": "path",
        "required": true
      }
    ]
  },
  "createObjectStorageCredential": {
    "scope": "platform.storage.credentials",
    "method": "POST",
    "path": "/object-storage/buckets/{id}/credentials",
    "status": 201,
    "statuses": [
      201
    ],
    "emptyStatuses": [],
    "bodyType": "application/json",
    "responseType": "application/json",
    "test": false,
    "params": [
      {
        "name": "id",
        "wire": "id",
        "in": "path",
        "required": true
      },
      {
        "name": "body",
        "wire": "body",
        "in": "body",
        "required": true
      }
    ]
  },
  "deleteObjectStorageCredential": {
    "scope": "platform.storage.credentials",
    "method": "DELETE",
    "path": "/object-storage/buckets/{id}/credentials/{credential_id}",
    "status": 202,
    "statuses": [
      202,
      204
    ],
    "emptyStatuses": [
      202,
      204
    ],
    "bodyType": "",
    "responseType": "",
    "test": false,
    "params": [
      {
        "name": "id",
        "wire": "id",
        "in": "path",
        "required": true
      },
      {
        "name": "credential_id",
        "wire": "credential_id",
        "in": "path",
        "required": true
      }
    ]
  }
} as const;
