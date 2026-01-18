"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/rules/v2/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/rules 的入口。导入/依赖:外部:无；内部:无；本地:./binary-data-storage.rule、./cli-replace-update-workflow-command.rule、./disabled-nodes.rule、./dotenv-upgrade.rule 等16项。导出:v2Rules。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/rules/v2/index.ts -> services/n8n/application/cli/services/modules/breaking-changes/rules/v2/__init__.py

import { BinaryDataStorageRule } from './binary-data-storage.rule';
import { CliActivateAllWorkflowsRule } from './cli-replace-update-workflow-command.rule';
import { DisabledNodesRule } from './disabled-nodes.rule';
import { DotenvUpgradeRule } from './dotenv-upgrade.rule';
import { FileAccessRule } from './file-access.rule';
import { GitNodeBareReposRule } from './git-node-bare-repos.rule';
import { OAuthCallbackAuthRule } from './oauth-callback-auth.rule';
import { ProcessEnvAccessRule } from './process-env-access.rule';
import { PyodideRemovedRule } from './pyodide-removed.rule';
import { QueueWorkerMaxStalledCountRule } from './queue-worker-max-stalled-count.rule';
import { RemovedDatabaseTypesRule } from './removed-database-types.rule';
import { RemovedNodesRule } from './removed-nodes.rule';
import { SettingsFilePermissionsRule } from './settings-file-permissions.rule';
import { SqliteLegacyDriverRule } from './sqlite-legacy-driver.rule';
import { TaskRunnerDockerImageRule } from './task-runner-docker-image.rule';
import { TaskRunnersRule } from './task-runners.rule';
import { TunnelOptionRule } from './tunnel-option.rule';
import { StartNodeRemovedRule } from './start-node-removed.rule';
import { WaitNodeSubworkflowRule } from './wait-node-subworkflow.rule';
import { WorkflowHooksDeprecatedRule } from './workflow-hooks-deprecated.rule';

const v2Rules = [
	// Workflow-level rules
	RemovedNodesRule,
	ProcessEnvAccessRule,
	PyodideRemovedRule,
	FileAccessRule,
	DisabledNodesRule,
	WaitNodeSubworkflowRule,
	GitNodeBareReposRule,
	StartNodeRemovedRule,
	// Instance-level rules
	DotenvUpgradeRule,
	OAuthCallbackAuthRule,
	CliActivateAllWorkflowsRule,
	WorkflowHooksDeprecatedRule,
	QueueWorkerMaxStalledCountRule,
	TunnelOptionRule,
	RemovedDatabaseTypesRule,
	SettingsFilePermissionsRule,
	TaskRunnersRule,
	TaskRunnerDockerImageRule,
	SqliteLegacyDriverRule,
	BinaryDataStorageRule,
];
export { v2Rules };
