"""
MIGRATION-META:
  source_path: packages/cli/src/scaling/pubsub/pubsub.eventbus.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/scaling/pubsub 的模块。导入/依赖:外部:无；内部:@n8n/di、@/typed-emitter；本地:./pubsub.event-map。导出:PubSubEventBus。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/scaling/pubsub/pubsub.eventbus.ts -> services/n8n/application/cli/services/scaling/pubsub/pubsub_eventbus.py

import { Service } from '@n8n/di';

import { TypedEmitter } from '@/typed-emitter';

import type { PubSubEventMap } from './pubsub.event-map';

@Service()
export class PubSubEventBus extends TypedEmitter<PubSubEventMap> {}
