"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Sheet/v2/methods/credentialTest.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Sheet 的节点。导入/依赖:外部:无；内部:无；本地:../../GenericFunctions。导出:无。关键函数/方法:googleApiCredentialTest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Sheet/v2/methods/credentialTest.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Sheet/v2/methods/credentialTest.py

import type {
	ICredentialsDecrypted,
	ICredentialTestFunctions,
	INodeCredentialTestResult,
} from 'n8n-workflow';

import { getGoogleAccessToken } from '../../../GenericFunctions';

export async function googleApiCredentialTest(
	this: ICredentialTestFunctions,
	credential: ICredentialsDecrypted,
): Promise<INodeCredentialTestResult> {
	try {
		const tokenRequest = await getGoogleAccessToken.call(this, credential.data!, 'sheetV2');
		if (!tokenRequest.access_token) {
			return {
				status: 'Error',
				message: 'Could not generate a token from your private key.',
			};
		}
	} catch (err) {
		return {
			status: 'Error',
			message: `Private key validation failed: ${err.message}`,
		};
	}

	return {
		status: 'OK',
		message: 'Connection successful!',
	};
}
