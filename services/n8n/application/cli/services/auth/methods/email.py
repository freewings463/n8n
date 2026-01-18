"""
MIGRATION-META:
  source_path: packages/cli/src/auth/methods/email.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/auth/methods 的认证模块。导入/依赖:外部:无；内部:@n8n/db、@n8n/di、@/errors/…/auth.error、@/events/event.service、@/ldap.ee/helpers.ee、@/services/password.utility；本地:无。导出:handleEmailLogin。关键函数/方法:handleEmailLogin。用于承载认证实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Authentication helpers/use-cases -> application/services/auth
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/auth/methods/email.ts -> services/n8n/application/cli/services/auth/methods/email.py

import type { User } from '@n8n/db';
import { UserRepository } from '@n8n/db';
import { Container } from '@n8n/di';

import { AuthError } from '@/errors/response-errors/auth.error';
import { EventService } from '@/events/event.service';
import { isLdapLoginEnabled } from '@/ldap.ee/helpers.ee';
import { PasswordUtility } from '@/services/password.utility';

export const handleEmailLogin = async (
	email: string,
	password: string,
): Promise<User | undefined> => {
	const user = await Container.get(UserRepository).findOne({
		where: { email },
		relations: ['authIdentities', 'role'],
	});

	if (user?.password && (await Container.get(PasswordUtility).compare(password, user.password))) {
		return user;
	}

	// At this point if the user has a LDAP ID, means it was previously an LDAP user,
	// so suggest to reset the password to gain access to the instance.
	const ldapIdentity = user?.authIdentities?.find((i) => i.providerType === 'ldap');
	if (user && ldapIdentity && !isLdapLoginEnabled()) {
		Container.get(EventService).emit('login-failed-due-to-ldap-disabled', { userId: user.id });

		throw new AuthError('Reset your password to gain access to the instance.');
	}

	return undefined;
};
