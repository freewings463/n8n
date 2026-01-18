"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/custom/prompts.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的模块。导入/依赖:外部:@clack/prompts；内部:无；本地:./types、../utils/prompts。导出:credentialTypePrompt、baseUrlPrompt、oauthFlowPrompt。关键函数/方法:credentialTypePrompt、baseUrlPrompt、text、oauthFlowPrompt。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/custom/prompts.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/custom/prompts.py

import { select, text } from '@clack/prompts';

import type { CredentialType } from './types';
import { withCancelHandler } from '../../../../utils/prompts';

export const credentialTypePrompt = async () =>
	await withCancelHandler(
		select<CredentialType>({
			message: 'What type of authentication does your API use?',
			options: [
				{
					label: 'API Key',
					value: 'apiKey',
					hint: 'Send a secret key via headers, query, or body',
				},
				{
					label: 'Bearer Token',
					value: 'bearer',
					hint: 'Send a token via Authorization header (Authorization: Bearer <token>)',
				},
				{
					label: 'OAuth2',
					value: 'oauth2',
					hint: 'Use an OAuth 2.0 flow to obtain access tokens on behalf of a user or app',
				},
				{
					label: 'Basic Auth',
					value: 'basicAuth',
					hint: 'Send username and password encoded in base64 via the Authorization header',
				},
				{
					label: 'Custom',
					value: 'custom',
					hint: 'Create your own credential logic; an empty credential class will be scaffolded for you',
				},
				{
					label: 'None',
					value: 'none',
					hint: 'No authentication; no credential class will be generated',
				},
			],
			initialValue: 'apiKey',
		}),
	);

export const baseUrlPrompt = async () =>
	await withCancelHandler(
		text({
			message: "What's the base URL of the API?",
			placeholder: 'https://api.example.com/v2',
			defaultValue: 'https://api.example.com/v2',
			validate: (value) => {
				if (!value) return;

				if (!value.startsWith('https://') && !value.startsWith('http://')) {
					return 'Base URL must start with http(s)://';
				}

				try {
					new URL(value);
				} catch (error) {
					return 'Must be a valid URL';
				}
				return;
			},
		}),
	);

export const oauthFlowPrompt = async () =>
	await withCancelHandler(
		select<'clientCredentials' | 'authorizationCode'>({
			message: 'What OAuth2 flow does your API use?',
			options: [
				{
					label: 'Authorization code',
					value: 'authorizationCode',
					hint: 'Users log in and approve access (use this if unsure)',
				},
				{
					label: 'Client credentials',
					value: 'clientCredentials',
					hint: 'Server-to-server auth without user interaction',
				},
			],
			initialValue: 'authorizationCode',
		}),
	);
