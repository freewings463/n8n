"""
MIGRATION-META:
  source_path: packages/cli/src/public-api/v1/handlers/users/users.service.ee.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/public-api/v1/handlers 的服务。导入/依赖:外部:lodash/pick、uuid；内部:@n8n/db、@n8n/di、@n8n/typeorm；本地:无。导出:clean。关键函数/方法:delete、getUser、getAllUsersAndCount、pickUserSelectableProperties、clean。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/public-api/v1/handlers/users/users.service.ee.ts -> services/n8n/infrastructure/cli/persistence/repositories/public-api/v1/handlers/users/users_service_ee.py

import type { User } from '@n8n/db';
import { UserRepository } from '@n8n/db';
import { Container } from '@n8n/di';
// eslint-disable-next-line n8n-local-rules/misplaced-n8n-typeorm-import
import { In } from '@n8n/typeorm';
import pick from 'lodash/pick';
import { validate as uuidValidate } from 'uuid';

export async function getUser(data: {
	withIdentifier: string;
	includeRole?: boolean;
}): Promise<(User & { role?: string }) | null> {
	return await Container.get(UserRepository)
		.findOne({
			where: {
				...(uuidValidate(data.withIdentifier) && { id: data.withIdentifier }),
				...(!uuidValidate(data.withIdentifier) && { email: data.withIdentifier }),
			},
			relations: ['role'],
		})
		.then((user) => {
			if (!user) return null;

			if (!data?.includeRole) delete (user as Partial<User>).role;

			return { ...user, role: user.role?.slug } as User & { role: string | null };
		});
}

export async function getAllUsersAndCount(data: {
	includeRole?: boolean;
	limit?: number;
	offset?: number;
	in?: string[];
}): Promise<[Array<User & { role?: string }>, number]> {
	const { in: _in } = data;

	const users = await Container.get(UserRepository).find({
		where: { ...(_in && { id: In(_in) }) },
		skip: data.offset,
		take: data.limit,
		relations: ['role'],
	});
	if (!data?.includeRole) {
		users.forEach((user) => {
			delete (user as Partial<User>).role;
		});
	}
	const count = await Container.get(UserRepository).count();
	return [
		users.map((user) => ({ ...user, role: user.role?.slug }) as User & { role?: string }),
		count,
	];
}

const userProperties = [
	'id',
	'email',
	'firstName',
	'lastName',
	'createdAt',
	'updatedAt',
	'isPending',
];
function pickUserSelectableProperties(user: User, options?: { includeRole: boolean }) {
	return pick(user, userProperties.concat(options?.includeRole ? ['role'] : []));
}

export function clean(user: User, options?: { includeRole: boolean }): Partial<User>;
export function clean(users: User[], options?: { includeRole: boolean }): Array<Partial<User>>;

export function clean(
	users: User[] | User,
	options?: { includeRole: boolean },
): Array<Partial<User>> | Partial<User> {
	return Array.isArray(users)
		? users.map((user) => pickUserSelectableProperties(user, options))
		: pickUserSelectableProperties(users, options);
}
