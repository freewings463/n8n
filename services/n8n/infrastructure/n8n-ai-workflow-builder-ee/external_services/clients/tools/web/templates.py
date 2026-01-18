"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/web/templates.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools/web 的工作流模块。导入/依赖:外部:无；内部:@n8n/backend-common；本地:无。导出:FetchWorkflowsResult。关键函数/方法:isTemplateSearchResponse、isTemplateFetchResponse、buildSearchQueryString、fetchTemplateList、fetchTemplateByID、fetchWorkflowsFromTemplates。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected external HTTP client usage -> infrastructure/external_services/clients
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/web/templates.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/external_services/clients/tools/web/templates.py

import type { Logger } from '@n8n/backend-common';

import type {
	TemplateSearchQuery,
	TemplateSearchResponse,
	Category,
	TemplateFetchResponse,
	WorkflowMetadata,
} from '@/types';

/**
 * Base URL for n8n template API
 */
const N8N_API_BASE_URL = 'https://api.n8n.io/api';

/**
 * Type guard for TemplateSearchResponse
 */
function isTemplateSearchResponse(data: unknown): data is TemplateSearchResponse {
	if (typeof data !== 'object' || data === null) return false;
	const obj = data as Record<string, unknown>;
	return typeof obj.totalWorkflows === 'number' && Array.isArray(obj.workflows);
}

/**
 * Type guard for TemplateFetchResponse
 */
function isTemplateFetchResponse(data: unknown): data is TemplateFetchResponse {
	if (typeof data !== 'object' || data === null) return false;
	const obj = data as Record<string, unknown>;
	return (
		typeof obj.id === 'number' &&
		typeof obj.name === 'string' &&
		typeof obj.workflow === 'object' &&
		obj.workflow !== null
	);
}

/**
 * Build query string from search parameters
 */
function buildSearchQueryString(query: TemplateSearchQuery): string {
	const params = new URLSearchParams();

	// Fixed preset values (not overridable)
	params.append('price', '0'); // Always free templates
	params.append('combineWith', 'and'); // Don't ignore any search criteria
	params.append('sort', 'createdAt:desc,rank:desc'); // Most recent templates first
	params.append('rows', String(query.rows ?? 5)); // Default 5 results per page
	params.append('page', '1'); // Always first page

	// Optional user-provided values
	if (query.search) params.append('search', query.search);
	if (query.category) params.append('category', query.category);
	if (query.nodes) params.append('nodes', query.nodes);

	return params.toString();
}

/**
 * Fetch template/workflow list from n8n API
 */
export async function fetchTemplateList(query: {
	search?: string;
	category?: Category;
	rows?: number;
	nodes?: string;
}): Promise<TemplateSearchResponse> {
	const queryString = buildSearchQueryString(query);
	const url = `${N8N_API_BASE_URL}/templates/search${queryString ? `?${queryString}` : ''}`;

	const response = await fetch(url, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json',
		},
	});

	if (!response.ok) {
		throw new Error(`Failed to fetch templates: ${response.status} ${response.statusText}`);
	}

	const data: unknown = await response.json();
	if (!isTemplateSearchResponse(data)) {
		throw new Error('Invalid response format from templates API');
	}
	return data;
}

/**
 * Fetch a specific workflow template by ID from n8n API
 */
export async function fetchTemplateByID(id: number): Promise<TemplateFetchResponse> {
	const url = `${N8N_API_BASE_URL}/workflows/templates/${id}`;

	const response = await fetch(url, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json',
		},
	});

	if (!response.ok) {
		throw new Error(`Failed to fetch template ${id}: ${response.status} ${response.statusText}`);
	}

	const data: unknown = await response.json();
	if (!isTemplateFetchResponse(data)) {
		throw new Error(`Invalid response format from template ${id} API`);
	}
	return data;
}

/**
 * Result of fetching workflows from templates
 */
export interface FetchWorkflowsResult {
	workflows: WorkflowMetadata[];
	totalFound: number;
	templateIds: number[];
}

/**
 * Fetch workflows from templates API and return full workflow data
 * Shared utility used by both get-workflow-examples and get-node-examples tools
 */
export async function fetchWorkflowsFromTemplates(
	query: {
		search?: string;
		category?: Category;
		rows?: number;
		nodes?: string;
	},
	options?: {
		/** Maximum number of templates to fetch full data for (default: all) */
		maxTemplates?: number;
		logger?: Logger;
	},
): Promise<FetchWorkflowsResult> {
	const { maxTemplates, logger } = options ?? {};

	logger?.debug('Fetching workflows from templates', { query });

	// First, fetch the list of workflow templates (metadata)
	const response = await fetchTemplateList(query);

	// Determine which templates to fetch full data for
	const templatesToFetch = maxTemplates
		? response.workflows.slice(0, maxTemplates)
		: response.workflows;

	// Fetch complete workflow data for each template
	const workflowResults = await Promise.all(
		templatesToFetch.map(async (template) => {
			try {
				const fullWorkflow = await fetchTemplateByID(template.id);
				return {
					metadata: {
						templateId: template.id,
						name: template.name,
						description: template.description,
						workflow: fullWorkflow.workflow,
					} satisfies WorkflowMetadata,
					templateId: template.id,
				};
			} catch (error) {
				// Individual template fetch failures are non-fatal
				logger?.warn(`Failed to fetch full workflow for template ${template.id}`, { error });
				return null;
			}
		}),
	);

	// Filter out failed fetches
	const validResults = workflowResults.filter(
		(result): result is NonNullable<typeof result> => result !== null,
	);

	return {
		workflows: validResults.map((r) => r.metadata),
		totalFound: response.totalWorkflows,
		templateIds: validResults.map((r) => r.templateId),
	};
}
