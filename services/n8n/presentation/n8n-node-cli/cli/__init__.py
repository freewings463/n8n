"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/index.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/node-cli/src 的入口。导入/依赖:外部:无；内部:无；本地:./commands/build、./commands/cloud-support、./commands/dev、./commands/lint 等3项。导出:commands。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI package default -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/index.ts -> services/n8n/presentation/n8n-node-cli/cli/__init__.py

import Build from './commands/build';
import CloudSupport from './commands/cloud-support';
import Dev from './commands/dev';
import Lint from './commands/lint';
import New from './commands/new';
import Prerelease from './commands/prerelease';
import Release from './commands/release';

export const commands = {
	new: New,
	build: Build,
	dev: Dev,
	prerelease: Prerelease,
	release: Release,
	lint: Lint,
	// eslint-disable-next-line @typescript-eslint/naming-convention
	'cloud-support': CloudSupport,
};
