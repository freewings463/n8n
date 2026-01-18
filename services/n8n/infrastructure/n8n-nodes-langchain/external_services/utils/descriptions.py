"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/descriptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:schemaTypeField、buildJsonSchemaExampleField、buildJsonSchemaExampleNotice、jsonSchemaExampleField、buildInputSchemaField、inputSchemaField、promptTypeOptionsDeprecated、promptTypeOptions 等4项。关键函数/方法:buildJsonSchemaExampleField、buildJsonSchemaExampleNotice、buildInputSchemaField。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/descriptions.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/descriptions.py

import type { DisplayCondition, INodeProperties, NodeParameterValue } from 'n8n-workflow';

export const schemaTypeField: INodeProperties = {
	displayName: 'Schema Type',
	name: 'schemaType',
	type: 'options',
	noDataExpression: true,
	options: [
		{
			name: 'Generate From JSON Example',
			value: 'fromJson',
			description: 'Generate a schema from an example JSON object',
		},
		{
			name: 'Define using JSON Schema',
			value: 'manual',
			description: 'Define the JSON schema manually',
		},
	],
	default: 'fromJson',
	description: 'How to specify the schema for the function',
};

/**
 * Returns a field for inputting a JSON example that can be used to generate the schema.
 * @param props
 */
export const buildJsonSchemaExampleField = (props?: {
	showExtraProps?: Record<string, Array<NodeParameterValue | DisplayCondition> | undefined>;
}): INodeProperties => ({
	displayName: 'JSON Example',
	name: 'jsonSchemaExample',
	type: 'json',
	default: `{
	"some_input": "some_value"
}`,
	noDataExpression: true,
	typeOptions: {
		rows: 10,
	},
	displayOptions: {
		show: {
			...props?.showExtraProps,
			schemaType: ['fromJson'],
		},
	},
	description: 'Example JSON object to use to generate the schema',
});

/**
 * Returns a notice field about the generated schema properties being required by default.
 * @param props
 */
export const buildJsonSchemaExampleNotice = (props?: {
	showExtraProps?: Record<string, Array<NodeParameterValue | DisplayCondition> | undefined>;
}): INodeProperties => ({
	displayName:
		"All properties will be required. To make them optional, use the 'JSON Schema' schema type instead",
	name: 'notice',
	type: 'notice',
	default: '',
	displayOptions: {
		show: {
			...props?.showExtraProps,
			schemaType: ['fromJson'],
		},
	},
});

export const jsonSchemaExampleField = buildJsonSchemaExampleField();

export const buildInputSchemaField = (props?: {
	showExtraProps?: Record<string, Array<NodeParameterValue | DisplayCondition> | undefined>;
}): INodeProperties => ({
	displayName: 'Input Schema',
	name: 'inputSchema',
	type: 'json',
	default: `{
"type": "object",
"properties": {
	"some_input": {
		"type": "string",
		"description": "Some input to the function"
		}
	}
}`,
	noDataExpression: false,
	typeOptions: {
		rows: 10,
	},
	displayOptions: {
		show: {
			...props?.showExtraProps,
			schemaType: ['manual'],
		},
	},
	description: 'Schema to use for the function',
	hint: 'Use <a target="_blank" href="https://json-schema.org/">JSON Schema</a> format (<a target="_blank" href="https://json-schema.org/learn/miscellaneous-examples.html">examples</a>). $refs syntax is currently not supported.',
});

export const inputSchemaField = buildInputSchemaField();

export const promptTypeOptionsDeprecated: INodeProperties = {
	displayName: 'Source for Prompt (User Message)',
	name: 'promptType',
	type: 'options',
	options: [
		{
			name: 'Connected Chat Trigger Node',
			value: 'auto',
			description:
				"Looks for an input field called 'chatInput' that is coming from a directly connected Chat Trigger",
		},
		{
			name: 'Connected Guardrails Node',
			value: 'guardrails',
			description:
				"Looks for an input field called 'guardrailsInput' that is coming from a directly connected Guardrails Node",
		},
		{
			name: 'Define below',
			value: 'define',
			description: 'Use an expression to reference data in previous nodes or enter static text',
		},
	],
	default: 'auto',
};

export const promptTypeOptions: INodeProperties = {
	displayName: 'Source for Prompt (User Message)',
	name: 'promptType',
	type: 'options',
	options: [
		{
			name: 'Connected Chat Trigger Node',
			value: 'auto',
			description:
				"Looks for an input field called 'chatInput' that is coming from a directly connected Chat Trigger",
		},
		{
			name: 'Define below',
			value: 'define',
			description: 'Use an expression to reference data in previous nodes or enter static text',
		},
	],
	default: 'auto',
};

export const textInput: INodeProperties = {
	displayName: 'Prompt (User Message)',
	name: 'text',
	type: 'string',
	required: true,
	default: '',
	placeholder: 'e.g. Hello, how can you help me?',
	typeOptions: {
		rows: 2,
	},
};

export const textFromPreviousNode: INodeProperties = {
	displayName: 'Prompt (User Message)',
	name: 'text',
	type: 'string',
	required: true,
	default: '={{ $json.chatInput }}',
	typeOptions: {
		rows: 2,
	},
	disabledOptions: { show: { promptType: ['auto'] } },
};

export const textFromGuardrailsNode: INodeProperties = {
	displayName: 'Prompt (User Message)',
	name: 'text',
	type: 'string',
	required: true,
	default: '={{ $json.guardrailsInput }}',
	typeOptions: {
		rows: 2,
	},
	disabledOptions: { show: { promptType: ['guardrails'] } },
};

export const toolDescription: INodeProperties = {
	displayName: 'Description',
	name: 'toolDescription',
	type: 'string',
	default: 'AI Agent that can call other tools',
	required: true,
	typeOptions: { rows: 2 },
	description:
		'Explain to the LLM what this tool does, a good, specific description would allow LLMs to produce expected results much more often',
};
