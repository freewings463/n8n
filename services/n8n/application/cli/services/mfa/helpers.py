"""
MIGRATION-META:
  source_path: packages/cli/src/mfa/helpers.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/mfa 的工具。导入/依赖:外部:无；内部:@n8n/config、@n8n/db、@n8n/di；本地:无。导出:isMfaFeatureEnabled、handleMfaDisable。关键函数/方法:isMfaFeatureEnabled、isMfaFeatureDisabled、getUsersWithMfaEnabled、handleMfaDisable。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/mfa/helpers.ts -> services/n8n/application/cli/services/mfa/helpers.py

import { GlobalConfig } from '@n8n/config';
import { UserRepository } from '@n8n/db';
import { Container } from '@n8n/di';

export const isMfaFeatureEnabled = () => Container.get(GlobalConfig).mfa.enabled;

const isMfaFeatureDisabled = () => !isMfaFeatureEnabled();

const getUsersWithMfaEnabled = async () =>
	await Container.get(UserRepository).count({ where: { mfaEnabled: true } });

export const handleMfaDisable = async () => {
	if (isMfaFeatureDisabled()) {
		// check for users with MFA enabled, and if there are
		// users, then keep the feature enabled
		const users = await getUsersWithMfaEnabled();
		if (users) {
			Container.get(GlobalConfig).mfa.enabled = true;
		}
	}
};
