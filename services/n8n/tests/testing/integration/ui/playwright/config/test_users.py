"""
MIGRATION-META:
  source_path: packages/testing/playwright/config/test-users.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/config 的配置。导入/依赖:外部:无；内部:无；本地:./constants。导出:UserCredentials、INSTANCE_OWNER_CREDENTIALS、INSTANCE_ADMIN_CREDENTIALS、INSTANCE_MEMBER_CREDENTIALS、INSTANCE_CHAT_CREDENTIALS。关键函数/方法:getRandomName、randFirstName、randLastName。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/config/test-users.ts -> services/n8n/tests/testing/integration/ui/playwright/config/test_users.py

import { DEFAULT_USER_PASSWORD } from './constants';

export interface UserCredentials {
	email: string;
	password: string;
	firstName: string;
	lastName: string;
	mfaEnabled?: boolean;
	mfaSecret?: string;
	mfaRecoveryCodes?: string[];
}

// Simple name generators
const FIRST_NAMES = [
	'Alex',
	'Jordan',
	'Taylor',
	'Morgan',
	'Casey',
	'Riley',
	'Avery',
	'Quinn',
	'Sam',
	'Drew',
	'Blake',
	'Sage',
	'River',
	'Rowan',
	'Skylar',
	'Emery',
];

const LAST_NAMES = [
	'Smith',
	'Johnson',
	'Williams',
	'Brown',
	'Jones',
	'Garcia',
	'Miller',
	'Davis',
	'Rodriguez',
	'Martinez',
	'Hernandez',
	'Lopez',
	'Gonzalez',
	'Wilson',
	'Anderson',
	'Thomas',
];

const getRandomName = (names: string[]): string => {
	return names[Math.floor(Math.random() * names.length)];
};

const randFirstName = (): string => getRandomName(FIRST_NAMES);
const randLastName = (): string => getRandomName(LAST_NAMES);

export const INSTANCE_OWNER_CREDENTIALS: UserCredentials = {
	email: 'nathan@n8n.io',
	password: DEFAULT_USER_PASSWORD,
	firstName: randFirstName(),
	lastName: randLastName(),
	mfaEnabled: false,
	mfaSecret: 'KVKFKRCPNZQUYMLXOVYDSQKJKZDTSRLD',
	mfaRecoveryCodes: ['d04ea17f-e8b2-4afa-a9aa-57a2c735b30e'],
};

export const INSTANCE_ADMIN_CREDENTIALS: UserCredentials = {
	email: 'admin@n8n.io',
	password: DEFAULT_USER_PASSWORD,
	firstName: randFirstName(),
	lastName: randLastName(),
};

export const INSTANCE_MEMBER_CREDENTIALS: UserCredentials[] = [
	{
		email: 'member@n8n.io',
		password: DEFAULT_USER_PASSWORD,
		firstName: randFirstName(),
		lastName: randLastName(),
	},
	{
		email: 'member2@n8n.io',
		password: DEFAULT_USER_PASSWORD,
		firstName: randFirstName(),
		lastName: randLastName(),
	},
];

export const INSTANCE_CHAT_CREDENTIALS: UserCredentials = {
	email: 'chat@n8n.io',
	password: DEFAULT_USER_PASSWORD,
	firstName: randFirstName(),
	lastName: randLastName(),
};
