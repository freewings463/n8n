"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/types/requests.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/source-control.ee/types 的类型。导入/依赖:外部:无；内部:@n8n/db；本地:./source-control-commit、./source-control-disconnect、./source-control-generate-key-pair、./source-control-get-status 等5项。导出:无。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/types/requests.ts -> services/n8n/application/cli/services/modules/source-control.ee/types/requests.py

import type { AuthenticatedRequest } from '@n8n/db';

import type { SourceControlCommit } from './source-control-commit';
import type { SourceControlDisconnect } from './source-control-disconnect';
import type { SourceControlGenerateKeyPair } from './source-control-generate-key-pair';
import type { SourceControlGetStatus } from './source-control-get-status';
import type { SourceControlPreferences } from './source-control-preferences';
import type { SourceControlPush } from './source-control-push';
import type { SourceControlSetBranch } from './source-control-set-branch';
import type { SourceControlSetReadOnly } from './source-control-set-read-only';
import type { SourceControlStage } from './source-control-stage';

export declare namespace SourceControlRequest {
	type UpdatePreferences = AuthenticatedRequest<{}, {}, Partial<SourceControlPreferences>, {}>;
	type SetReadOnly = AuthenticatedRequest<{}, {}, SourceControlSetReadOnly, {}>;
	type SetBranch = AuthenticatedRequest<{}, {}, SourceControlSetBranch, {}>;
	type Commit = AuthenticatedRequest<{}, {}, SourceControlCommit, {}>;
	type Stage = AuthenticatedRequest<{}, {}, SourceControlStage, {}>;
	type Push = AuthenticatedRequest<{}, {}, SourceControlPush, {}>;
	type Disconnect = AuthenticatedRequest<{}, {}, SourceControlDisconnect, {}>;
	type GetStatus = AuthenticatedRequest<{}, {}, {}, SourceControlGetStatus>;
	type GenerateKeyPair = AuthenticatedRequest<{}, {}, SourceControlGenerateKeyPair, {}>;
}
