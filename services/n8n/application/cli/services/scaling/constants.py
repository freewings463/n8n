"""
MIGRATION-META:
  source_path: packages/cli/src/scaling/constants.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/scaling 的模块。导入/依赖:外部:无；内部:无；本地:./pubsub/pubsub.types。导出:QUEUE_NAME、JOB_TYPE_NAME、COMMAND_PUBSUB_CHANNEL、WORKER_RESPONSE_PUBSUB_CHANNEL、SELF_SEND_COMMANDS、IMMEDIATE_COMMANDS。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/scaling/constants.ts -> services/n8n/application/cli/services/scaling/constants.py

import type { PubSub } from './pubsub/pubsub.types';

export const QUEUE_NAME = 'jobs';

export const JOB_TYPE_NAME = 'job';

/** Pubsub channel for commands sent by a main process to workers or to other main processes. */
export const COMMAND_PUBSUB_CHANNEL = 'n8n.commands';

/** Pubsub channel for messages sent by workers in response to commands from main processes. */
export const WORKER_RESPONSE_PUBSUB_CHANNEL = 'n8n.worker-response';

/**
 * Commands that should be sent to the sender as well, e.g. during workflow activation and
 * deactivation in multi-main setup. */
export const SELF_SEND_COMMANDS = new Set<PubSub.Command['command']>([
	'add-webhooks-triggers-and-pollers',
	'remove-triggers-and-pollers',
]);

/**
 * Commands that should not be debounced when received, e.g. during webhook handling in
 * multi-main setup.
 */
export const IMMEDIATE_COMMANDS = new Set<PubSub.Command['command']>([
	'add-webhooks-triggers-and-pollers',
	'remove-triggers-and-pollers',
	'relay-execution-lifecycle-event',
]);
