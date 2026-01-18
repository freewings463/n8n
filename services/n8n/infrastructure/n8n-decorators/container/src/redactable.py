"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/redactable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src 的模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:RedactableError、Redactable。关键函数/方法:toRedactable。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/redactable.ts -> services/n8n/infrastructure/n8n-decorators/container/src/redactable.py

import { UnexpectedError } from 'n8n-workflow';

type UserLike = {
	id: string;
	email?: string;
	firstName?: string;
	lastName?: string;
	role?: {
		slug: string;
	};
};

export class RedactableError extends UnexpectedError {
	constructor(fieldName: string, args: string) {
		super(
			`Failed to find "${fieldName}" property in argument "${args.toString()}". Please set the decorator \`@Redactable()\` only on \`LogStreamingEventRelay\` methods where the argument contains a "${fieldName}" property.`,
		);
	}
}

function toRedactable(userLike: UserLike) {
	return {
		userId: userLike.id,
		_email: userLike.email,
		_firstName: userLike.firstName,
		_lastName: userLike.lastName,
		globalRole: userLike.role?.slug,
	};
}

type FieldName = 'user' | 'inviter' | 'invitee';

/**
 * Mark redactable properties in a `{ user: UserLike }` field in an `LogStreamingEventRelay`
 * method arg. These properties will be later redacted by the log streaming
 * destination based on user prefs. Only for `n8n.audit.*` logs.
 *
 * Also transform `id` to `userId` and `role` to `globalRole`.
 *
 * @example
 *
 * { id: '123'; email: 'test@example.com', role: 'some-role' } ->
 * { userId: '123'; _email: 'test@example.com', globalRole: 'some-role' }
 */
export const Redactable =
	(fieldName: FieldName = 'user'): MethodDecorator =>
	(_target, _propertyName, propertyDescriptor: PropertyDescriptor) => {
		// eslint-disable-next-line @typescript-eslint/no-restricted-types
		const originalMethod = propertyDescriptor.value as Function;

		type MethodArgs = Array<{ [fieldName: string]: UserLike }>;

		propertyDescriptor.value = function (...args: MethodArgs) {
			const index = args.findIndex((arg) => arg[fieldName] !== undefined);

			if (index === -1) throw new RedactableError(fieldName, args.toString());

			const userLike = args[index]?.[fieldName];

			// @ts-expect-error Transformation
			if (userLike) args[index][fieldName] = toRedactable(userLike);

			// eslint-disable-next-line @typescript-eslint/no-unsafe-return
			return originalMethod.apply(this, args);
		};

		return propertyDescriptor;
	};
