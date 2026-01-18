"""
MIGRATION-META:
  source_path: packages/cli/src/services/password.utility.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/services 的服务。导入/依赖:外部:bcryptjs；内部:@n8n/di；本地:无。导出:PasswordUtility。关键函数/方法:hash、compare。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/services/password.utility.ts -> services/n8n/application/cli/services/services/password_utility.py

import { Service as Utility } from '@n8n/di';
import { compare, hash } from 'bcryptjs';

const SALT_ROUNDS = 10;

@Utility()
export class PasswordUtility {
	async hash(plaintext: string) {
		return await hash(plaintext, SALT_ROUNDS);
	}

	async compare(plaintext: string, hashed: string | null) {
		if (hashed === null) {
			return false;
		}
		return await compare(plaintext, hashed);
	}
}
