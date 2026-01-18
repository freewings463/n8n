"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/shared/transport.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:githubApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/shared/transport.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/github-issues/template/nodes/GithubIssues/shared/transport.py

import type {
	IHookFunctions,
	IExecuteFunctions,
	IExecuteSingleFunctions,
	ILoadOptionsFunctions,
	IHttpRequestMethods,
	IDataObject,
	IHttpRequestOptions,
} from 'n8n-workflow';

export async function githubApiRequest(
	this: IHookFunctions | IExecuteFunctions | IExecuteSingleFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	qs: IDataObject = {},
	body: IDataObject | undefined = undefined,
) {
	const authenticationMethod = this.getNodeParameter('authentication', 0);

	const options: IHttpRequestOptions = {
		method: method,
		qs,
		body,
		url: `https://api.github.com${resource}`,
		json: true,
	};

	const credentialType =
		authenticationMethod === 'accessToken' ? 'githubIssuesApi' : 'githubIssuesOAuth2Api';

	return this.helpers.httpRequestWithAuthentication.call(this, credentialType, options);
}
