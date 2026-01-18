"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/mcp.event-relay.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/mcp 的模块。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/db、@n8n/di、@/events/event.service、@/events/…/event-relay、@/events/…/relay.event-map；本地:无。导出:McpEventRelay。关键函数/方法:init、onWorkflowDeactivated。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/mcp.event-relay.ts -> services/n8n/application/cli/services/mcp/mcp_event_relay.py

import { Logger } from '@n8n/backend-common';
import { WorkflowRepository } from '@n8n/db';
import { Service } from '@n8n/di';

import { EventService } from '@/events/event.service';
import { EventRelay } from '@/events/relays/event-relay';
import type { RelayEventMap } from '@/events/maps/relay.event-map';

/**
 * Event relay for MCP module to handle workflow events
 */
@Service()
export class McpEventRelay extends EventRelay {
	constructor(
		eventService: EventService,
		private readonly workflowRepository: WorkflowRepository,
		private readonly logger: Logger,
	) {
		super(eventService);
	}

	init() {
		this.setupListeners({
			'workflow-deactivated': async (event) => await this.onWorkflowDeactivated(event),
		});
	}

	/**
	 * Handles workflow deactivated events.
	 * When a workflow is deactivated, automatically disables MCP access.
	 */
	private async onWorkflowDeactivated(event: RelayEventMap['workflow-deactivated']) {
		const { workflow, workflowId } = event;

		// Only process if workflow has MCP access enabled
		if (workflow.settings?.availableInMCP === true) {
			try {
				// Update the workflow settings to disable MCP access
				const updatedSettings = {
					...workflow.settings,
					availableInMCP: false,
				};

				await this.workflowRepository.update(workflowId, {
					settings: updatedSettings,
				});

				this.logger.info('Disabled MCP access for deactivated workflow', {
					workflowId,
					workflowName: workflow.name,
				});
			} catch (error) {
				this.logger.error('Failed to disable MCP access for deactivated workflow', {
					workflowId,
					error: error instanceof Error ? error.message : String(error),
				});
			}
		}
	}
}
