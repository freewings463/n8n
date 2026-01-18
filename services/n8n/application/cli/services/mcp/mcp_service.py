"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/mcp.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/mcp 的服务。导入/依赖:外部:@modelcontextprotocol/sdk/…/mcp.js；内部:@n8n/config、@n8n/db、@n8n/di、@/active-executions、@/credentials/credentials.service、@/services/url.service 等4项；本地:./tools/execute-workflow.tool、./tools/get-workflow-details.tool、./tools/search-workflows.tool。导出:McpService。关键函数/方法:getServer。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/mcp.service.ts -> services/n8n/application/cli/services/mcp/mcp_service.py

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { GlobalConfig } from '@n8n/config';
import { User } from '@n8n/db';
import { Service } from '@n8n/di';

import { createExecuteWorkflowTool } from './tools/execute-workflow.tool';
import { createWorkflowDetailsTool } from './tools/get-workflow-details.tool';
import { createSearchWorkflowsTool } from './tools/search-workflows.tool';

import { ActiveExecutions } from '@/active-executions';
import { CredentialsService } from '@/credentials/credentials.service';
import { UrlService } from '@/services/url.service';
import { Telemetry } from '@/telemetry';
import { WorkflowRunner } from '@/workflow-runner';
import { WorkflowFinderService } from '@/workflows/workflow-finder.service';
import { WorkflowService } from '@/workflows/workflow.service';

@Service()
export class McpService {
	constructor(
		private readonly workflowFinderService: WorkflowFinderService,
		private readonly workflowService: WorkflowService,
		private readonly urlService: UrlService,
		private readonly credentialsService: CredentialsService,
		private readonly activeExecutions: ActiveExecutions,
		private readonly globalConfig: GlobalConfig,
		private readonly telemetry: Telemetry,
		private readonly workflowRunner: WorkflowRunner,
	) {}

	getServer(user: User) {
		const server = new McpServer({
			name: 'n8n MCP Server',
			version: '1.0.0',
		});

		const workflowSearchTool = createSearchWorkflowsTool(
			user,
			this.workflowService,
			this.telemetry,
		);
		server.registerTool(
			workflowSearchTool.name,
			workflowSearchTool.config,
			workflowSearchTool.handler,
		);

		const executeWorkflowTool = createExecuteWorkflowTool(
			user,
			this.workflowFinderService,
			this.activeExecutions,
			this.workflowRunner,
			this.telemetry,
		);
		server.registerTool(
			executeWorkflowTool.name,
			executeWorkflowTool.config,
			executeWorkflowTool.handler,
		);

		const workflowDetailsTool = createWorkflowDetailsTool(
			user,
			this.urlService.getWebhookBaseUrl(),
			this.workflowFinderService,
			this.credentialsService,
			{
				webhook: this.globalConfig.endpoints.webhook,
				webhookTest: this.globalConfig.endpoints.webhookTest,
			},
			this.telemetry,
		);
		server.registerTool(
			workflowDetailsTool.name,
			workflowDetailsTool.config,
			workflowDetailsTool.handler,
		);

		return server;
	}
}
