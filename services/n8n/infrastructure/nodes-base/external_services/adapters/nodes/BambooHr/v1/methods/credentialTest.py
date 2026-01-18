"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/methods/credentialTest.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:validateCredentials、bambooHrApiCredentialTest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/methods/credentialTest.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/methods/credentialTest.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialsDecrypted,
	ICredentialTestFunctions,
	IHttpRequestOptions,
	INodeCredentialTestResult,
} from 'n8n-workflow';

async function validateCredentials(
	this: ICredentialTestFunctions,
	decryptedCredentials: ICredentialDataDecryptedObject,
): Promise<any> {
	const credentials = decryptedCredentials;

	const { subdomain, apiKey } = credentials as {
		subdomain: string;
		apiKey: string;
	};

	const options: IHttpRequestOptions = {
		method: 'GET',
		auth: {
			username: apiKey,
			password: 'x',
		},
		url: `https://api.bamboohr.com/api/gateway.php/${subdomain}/v1/employees/directory`,
	};

	return await this.helpers.request(options);
}

export async function bambooHrApiCredentialTest(
	this: ICredentialTestFunctions,
	credential: ICredentialsDecrypted,
): Promise<INodeCredentialTestResult> {
	try {
		await validateCredentials.call(this, credential.data as ICredentialDataDecryptedObject);
	} catch (error) {
		return {
			status: 'Error',
			message: 'The API Key included in the request is invalid',
		};
	}

	return {
		status: 'OK',
		message: 'Connection successful!',
	} as INodeCredentialTestResult;
}
