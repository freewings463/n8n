"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/types/web/templates.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/types/web 的工作流类型。导入/依赖:外部:无；内部:无；本地:../workflow。导出:categories、Category、TemplateSearchQuery、TemplateWorkflowDescription、TemplateSearchResponse、TemplateFetchResponse。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/types/web/templates.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/types/web/templates.py

import type { SimpleWorkflow } from '../workflow';

// retrieved from https://api.n8n.io/api/templates/categories
export const categories = [
	'AI',
	'AI Chatbot',
	'AI RAG',
	'AI Summarization',
	'Content Creation',
	'CRM',
	'Crypto Trading',
	'DevOps',
	'Document Extraction',
	'Document Ops',
	'Engineering',
	'File Management',
	'HR',
	'Internal Wiki',
	'Invoice Processing',
	'IT Ops',
	'Lead Generation',
	'Lead Nurturing',
	'Marketing',
	'Market Research',
	'Miscellaneous',
	'Multimodal AI',
	'Other',
	'Personal Productivity',
	'Project Management',
	'Sales',
	'SecOps',
	'Social Media',
	'Support',
	'Support Chatbot',
	'Ticket Management',
] as const;

export type Category = (typeof categories)[number];

/**
 * Query parameters for workflow examples search
 */
export interface TemplateSearchQuery {
	search?: string;
	rows?: number;
	page?: number;
	// sort is structured like column:desc/asc
	// examples: createdAt:desc|asc, _text_match:desc|asc, rank:desc|asc, trendingScore:desc|asc
	sort?: string;
	// 0 represents free
	price?: number;
	// how to combine these filters together
	combineWith?: 'or' | 'and';
	// category can be used to search by a pre-defined list
	category?: Category;
	// a specific node is used in the template, should be in node format like n8n-nodes-base.editImage
	nodes?: string;
	// there are apps search properties as well - but have a specific format which is
	// hard to feed to the agent for use in search (free search will work better)
}

// describes a workflow that can be retrieved, there are many more properties such as
// icons, created at dates and user information - but these would not be useful to the builder
export interface TemplateWorkflowDescription {
	id: number;
	name: string;
	description: string;
	price: number;
	totalViews: number;
	nodes: Array<{
		id: number;
		name: string;
		displayName: string;
		nodeCategories: Array<{ id: number; name: string }>;
	}>;
	user: {
		id: number;
		name: string;
		username: string;
		verified: boolean;
		bio: string;
	};
}

export interface TemplateSearchResponse {
	totalWorkflows: number;
	workflows: TemplateWorkflowDescription[];
	// there is also a filters field which lists what was matched, but this isn't
	// useful to the workflow builder
}

export interface TemplateFetchResponse {
	id: number;
	name: string;
	workflow: SimpleWorkflow;
}
