"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/dto/approve-consent-request.dto.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/mcp/dto 的模块。导入/依赖:外部:zod、zod-class；内部:无；本地:无。导出:ApproveConsentRequestDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/dto/approve-consent-request.dto.ts -> services/n8n/application/cli/services/modules/mcp/dto/approve_consent_request_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

export class ApproveConsentRequestDto extends Z.class({
	approved: z.boolean(),
}) {}
