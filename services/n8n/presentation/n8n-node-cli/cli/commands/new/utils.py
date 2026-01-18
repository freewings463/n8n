"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/commands/new/utils.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/node-cli/src/commands/new 的模块。导入/依赖:外部:无；内部:无；本地:../utils/package-manager、../utils/prompts。导出:createIntro。关键函数/方法:createIntro。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI package default -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/commands/new/utils.ts -> services/n8n/presentation/n8n-node-cli/cli/commands/new/utils.py

import { detectPackageManagerFromUserAgent } from '../../utils/package-manager';
import { getCommandHeader } from '../../utils/prompts';

export const createIntro = async () => {
	const maybePackageManager = detectPackageManagerFromUserAgent();
	const packageManager = maybePackageManager ?? 'npm';
	const commandName = maybePackageManager ? `${packageManager} create @n8n/node` : 'n8n-node new';
	return await getCommandHeader(commandName);
};
