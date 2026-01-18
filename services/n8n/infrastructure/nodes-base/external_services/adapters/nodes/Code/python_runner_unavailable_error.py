"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Code/python-runner-unavailable.error.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Code 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:PythonRunnerUnavailableError。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Code/python-runner-unavailable.error.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Code/python_runner_unavailable_error.py

import { UserError } from 'n8n-workflow';

type FailureReason = 'python' | 'venv';

const REASONS: Record<FailureReason, string> = {
	python: 'Python 3 is missing from this system',
	venv: 'Virtual environment is missing from this system',
};

export class PythonRunnerUnavailableError extends UserError {
	constructor(reason?: FailureReason) {
		const message = reason
			? `Python runner unavailable: ${REASONS[reason]}`
			: 'Python runner unavailable';

		super(message, {
			description:
				'Internal mode is intended only for debugging. For production, deploy in external mode: https://docs.n8n.io/hosting/configuration/task-runners/#setting-up-external-mode',
		});
	}
}
