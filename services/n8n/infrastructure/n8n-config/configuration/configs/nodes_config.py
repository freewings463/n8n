"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/nodes.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:无；内部:无；本地:../decorators。导出:NodesConfig。关键函数/方法:isStringArray。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/nodes.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/nodes_config.py

import { Config, Env } from '../decorators';

function isStringArray(input: unknown): input is string[] {
	return Array.isArray(input) && input.every((item) => typeof item === 'string');
}

class JsonStringArray extends Array<string> {
	constructor(str: string) {
		super();

		let parsed: unknown;

		try {
			parsed = JSON.parse(str);
		} catch {
			return [];
		}

		return isStringArray(parsed) ? parsed : [];
	}
}

@Config
export class NodesConfig {
	/** Node types to load. Includes all if unspecified. @example '["n8n-nodes-base.hackerNews"]' */
	@Env('NODES_INCLUDE')
	include: JsonStringArray = [];

	/**
	 * Node types not to load. Defaults to excluding `ExecuteCommand` and `LocalFileTrigger` for security.
	 * Set to an empty array to enable all node types.
	 *
	 * @example '["n8n-nodes-base.hackerNews"]'
	 */
	@Env('NODES_EXCLUDE')
	exclude: JsonStringArray = ['n8n-nodes-base.executeCommand', 'n8n-nodes-base.localFileTrigger'];

	/** Node type to use as error trigger */
	@Env('NODES_ERROR_TRIGGER_TYPE')
	errorTriggerType: string = 'n8n-nodes-base.errorTrigger';

	/** Whether to enable Python execution on the Code node. */
	@Env('N8N_PYTHON_ENABLED')
	pythonEnabled: boolean = true;
}
