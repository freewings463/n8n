"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/errors/missing-requirements.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners/errors 的错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:MissingRequirementsError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/errors/missing-requirements.error.ts -> services/n8n/application/cli/services/task-runners/errors/missing_requirements_error.py

import { UserError } from 'n8n-workflow';

const ERROR_MESSAGE = 'Failed to start Python task runner in internal mode.';

type ReasonId = 'python' | 'venv';

const HINT =
	'Launching a Python runner in internal mode is intended only for debugging and is not recommended for production. Users are encouraged to deploy in external mode. See: https://docs.n8n.io/hosting/configuration/task-runners/#setting-up-external-mode';

export class MissingRequirementsError extends UserError {
	constructor(reasonId: ReasonId) {
		const reason = {
			python: 'because Python 3 is missing from this system.',
			venv: 'because its virtual environment is missing from this system.',
		}[reasonId];

		super([ERROR_MESSAGE, reason, HINT].join(' '));
	}
}
