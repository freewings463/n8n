"""
MIGRATION-META:
  source_path: packages/core/nodes-testing/credentials-helper.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/nodes-testing 的模块。导入/依赖:外部:无；内部:@n8n/di、n8n-workflow；本地:../dist/credentials、./credential-types。导出:CredentialsHelper。关键函数/方法:setCredentials、getCredentialsProperties、authenticate、preAuthentication、getParentTypes、getDecrypted、getCredentials、updateCredentials、updateCredentialsOauthTokenData。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/nodes-testing/credentials-helper.ts -> services/n8n/application/core/services/nodes-testing/credentials_helper.py

import { Service } from '@n8n/di';
import { ICredentialsHelper } from 'n8n-workflow';
import type {
	ICredentialDataDecryptedObject,
	IHttpRequestHelper,
	IHttpRequestOptions,
	INode,
	INodeCredentialsDetails,
	IWorkflowExecuteAdditionalData,
} from 'n8n-workflow';

import { Credentials } from '../dist/credentials';
import { CredentialTypes } from './credential-types';

@Service()
export class CredentialsHelper extends ICredentialsHelper {
	private credentialsMap: Record<string, ICredentialDataDecryptedObject> = {};

	constructor(private readonly credentialTypes: CredentialTypes) {
		super();
	}

	setCredentials(credentialsMap: Record<string, ICredentialDataDecryptedObject>) {
		this.credentialsMap = credentialsMap;
	}

	getCredentialsProperties() {
		return [];
	}

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		typeName: string,
		requestParams: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		const credentialType = this.credentialTypes.getByName(typeName);
		if (typeof credentialType.authenticate === 'function') {
			return await credentialType.authenticate(credentials, requestParams);
		}
		return requestParams;
	}

	async preAuthentication(
		_helpers: IHttpRequestHelper,
		_credentials: ICredentialDataDecryptedObject,
		_typeName: string,
		_node: INode,
		_credentialsExpired: boolean,
	): Promise<ICredentialDataDecryptedObject | undefined> {
		return undefined;
	}

	getParentTypes(_name: string): string[] {
		return [];
	}

	async getDecrypted(
		_additionalData: IWorkflowExecuteAdditionalData,
		_nodeCredentials: INodeCredentialsDetails,
		type: string,
	): Promise<ICredentialDataDecryptedObject> {
		return this.credentialsMap[type] ?? {};
	}

	async getCredentials(
		_nodeCredentials: INodeCredentialsDetails,
		_type: string,
	): Promise<Credentials> {
		return new Credentials({ id: null, name: '' }, '', '');
	}

	async updateCredentials(
		_nodeCredentials: INodeCredentialsDetails,
		_type: string,
		_data: ICredentialDataDecryptedObject,
	): Promise<void> {}

	async updateCredentialsOauthTokenData(
		_nodeCredentials: INodeCredentialsDetails,
		_type: string,
		_data: ICredentialDataDecryptedObject,
	): Promise<void> {}
}
