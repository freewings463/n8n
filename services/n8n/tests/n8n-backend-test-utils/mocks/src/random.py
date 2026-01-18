"""
MIGRATION-META:
  source_path: packages/@n8n/backend-test-utils/src/random.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/backend-test-utils/src 的模块。导入/依赖:外部:uuid；内部:@n8n/constants、n8n-workflow；本地:无。导出:CredentialPayload、randomApiKey、chooseRandomly、randomValidPassword、randomInvalidPassword、randomName、randomEmail、randomCredentialPayload 等2项。关键函数/方法:randomApiKey、randomUppercaseLetter、randomValidPassword、randomString、randomInt、randomInvalidPassword、chooseRandomly 等6项。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Test utilities package -> tests/mocks
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/backend-test-utils/src/random.ts -> services/n8n/tests/n8n-backend-test-utils/mocks/src/random.py

import { MIN_PASSWORD_CHAR_LENGTH, MAX_PASSWORD_CHAR_LENGTH } from '@n8n/constants';
import { randomInt, randomString, UPPERCASE_LETTERS } from 'n8n-workflow';
import type { ICredentialDataDecryptedObject } from 'n8n-workflow';
import { v4 as uuid } from 'uuid';

export type CredentialPayload = {
	name: string;
	type: string;
	data: ICredentialDataDecryptedObject;
	isManaged?: boolean;
	isGlobal?: boolean;
	isResolvable?: boolean;
};

export const randomApiKey = () => `n8n_api_${randomString(40)}`;

export const chooseRandomly = <T>(array: T[]) => array[randomInt(array.length)];

const randomUppercaseLetter = () => chooseRandomly(UPPERCASE_LETTERS.split(''));

export const randomValidPassword = () =>
	randomString(MIN_PASSWORD_CHAR_LENGTH, MAX_PASSWORD_CHAR_LENGTH - 2) +
	randomUppercaseLetter() +
	randomInt(10);

export const randomInvalidPassword = () =>
	chooseRandomly([
		randomString(1, MIN_PASSWORD_CHAR_LENGTH - 1),
		randomString(MAX_PASSWORD_CHAR_LENGTH + 2, MAX_PASSWORD_CHAR_LENGTH + 100),
		'abcdefgh', // valid length, no number, no uppercase
		'abcdefg1', // valid length, has number, no uppercase
		'abcdefgA', // valid length, no number, has uppercase
		'abcdefA', // invalid length, no number, has uppercase
		'abcdef1', // invalid length, has number, no uppercase
		'abcdeA1', // invalid length, has number, has uppercase
		'abcdefg', // invalid length, no number, no uppercase
	]);

const POPULAR_TOP_LEVEL_DOMAINS = ['com', 'org', 'net', 'io', 'edu'];

const randomTopLevelDomain = () => chooseRandomly(POPULAR_TOP_LEVEL_DOMAINS);

export const randomName = () => randomString(4, 8).toLowerCase();

export const randomEmail = () => `${randomName()}@${randomName()}.${randomTopLevelDomain()}`;

export const randomCredentialPayload = ({
	isManaged = false,
	isGlobal,
	isResolvable,
	type,
}: {
	isManaged?: boolean;
	isGlobal?: boolean;
	isResolvable?: boolean;
	type?: string;
} = {}): CredentialPayload => {
	const payload: CredentialPayload = {
		name: randomName(),
		type: type ?? 'githubApi',
		data: { accessToken: randomString(6, 16) },
		isManaged,
	};

	// Only include optional fields if they have defined values
	if (isGlobal !== undefined) payload.isGlobal = isGlobal;
	if (isResolvable !== undefined) payload.isResolvable = isResolvable;

	return payload;
};

export const randomCredentialPayloadWithOauthTokenData = ({
	isManaged = false,
}: { isManaged?: boolean } = {}): CredentialPayload => ({
	name: randomName(),
	type: randomName(),
	data: { accessToken: randomString(6, 16), oauthTokenData: { access_token: randomString(6, 16) } },
	isManaged,
});

export const uniqueId = () => uuid();
