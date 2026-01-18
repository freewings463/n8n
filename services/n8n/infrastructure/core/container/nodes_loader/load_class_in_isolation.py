"""
MIGRATION-META:
  source_path: packages/core/src/nodes-loader/load-class-in-isolation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/nodes-loader 的模块。导入/依赖:外部:vm、${filePath}；内部:@n8n/backend-common；本地:无。导出:loadClassInIsolation。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node loading/discovery -> infrastructure/container/nodes_loader
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/nodes-loader/load-class-in-isolation.ts -> services/n8n/infrastructure/core/container/nodes_loader/load_class_in_isolation.py

import { inTest } from '@n8n/backend-common';
import { createContext, Script } from 'vm';

const context = createContext({ require });
export const loadClassInIsolation = <T>(filePath: string, className: string) => {
	if (process.platform === 'win32') {
		filePath = filePath.replace(/\\/g, '/');
	}

	// Note: Skip the isolation because it breaks nock mocks in tests
	if (inTest) {
		// eslint-disable-next-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
		return new (require(filePath)[className])() as T;
	} else {
		const script = new Script(`new (require('${filePath}').${className})()`);
		return script.runInContext(context) as T;
	}
};
