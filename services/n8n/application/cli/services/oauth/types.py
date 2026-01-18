"""
MIGRATION-META:
  source_path: packages/cli/src/oauth/types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/oauth 的OAuth类型。导入/依赖:外部:无；内部:@n8n/constants；本地:无。导出:CsrfStateRequired、CreateCsrfStateData、CsrfState、MAX_CSRF_AGE、enum、OAuth1CredentialData、algorithmMap。关键函数/方法:无。用于定义OAuth相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/oauth/types.ts -> services/n8n/application/cli/services/oauth/types.py

import { Time } from '@n8n/constants';

export type CsrfStateRequired = {
	/** Random CSRF token, used to verify the signature of the CSRF state */
	token: string;
	/** Creation timestamp of the CSRF state. Used for expiration.  */
	createdAt: number;
	/** Encrypted stringified CSRF state data */
	data: string;
};

export type CreateCsrfStateData = {
	cid: string;
	origin: 'static-credential' | 'dynamic-credential';
	[key: string]: unknown;
};

export type CsrfState = CsrfStateRequired;

export const MAX_CSRF_AGE = 5 * Time.minutes.toMilliseconds;

export const enum OauthVersion {
	V1 = 1,
	V2 = 2,
}

export interface OAuth1CredentialData {
	signatureMethod: 'HMAC-SHA256' | 'HMAC-SHA512' | 'HMAC-SHA1';
	consumerKey: string;
	consumerSecret: string;
	authUrl: string;
	accessTokenUrl: string;
	requestTokenUrl: string;
}

export const algorithmMap = {
	'HMAC-SHA256': 'sha256',
	'HMAC-SHA512': 'sha512',
	'HMAC-SHA1': 'sha1',
} as const;
