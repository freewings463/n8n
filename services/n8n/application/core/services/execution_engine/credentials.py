"""
MIGRATION-META:
  source_path: packages/core/src/credentials.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src 的模块。导入/依赖:外部:node:assert；内部:@n8n/backend-common、@n8n/di、n8n-workflow、@/constants、@/encryption/cipher；本地:无。导出:CredentialDataError、Credentials。关键函数/方法:setData、updateData、getData、getDataToSave。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core src/* defaulted to execution engine application services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/credentials.ts -> services/n8n/application/core/services/execution_engine/credentials.py

import { isObjectLiteral } from '@n8n/backend-common';
import { Container } from '@n8n/di';
import type { ICredentialDataDecryptedObject, ICredentialsEncrypted } from 'n8n-workflow';
import { ApplicationError, ICredentials, jsonParse } from 'n8n-workflow';
import * as a from 'node:assert';

import { CREDENTIAL_ERRORS } from '@/constants';
import { Cipher } from '@/encryption/cipher';

export class CredentialDataError extends ApplicationError {
	constructor({ name, type, id }: Credentials<object>, message: string, cause?: unknown) {
		super(message, {
			extra: { name, type, id },
			cause,
		});
	}
}

export class Credentials<
	T extends object = ICredentialDataDecryptedObject,
> extends ICredentials<T> {
	private readonly cipher = Container.get(Cipher);

	/**
	 * Sets new credential object
	 */
	setData(data: T): void {
		a.ok(isObjectLiteral(data));

		this.data = this.cipher.encrypt(data);
	}

	/**
	 * Update parts of the credential data.
	 * This decrypts the data, modifies it, and then re-encrypts the updated data back to a string.
	 */
	updateData(toUpdate: Partial<T>, toDelete: Array<keyof T> = []) {
		const updatedData: T = { ...this.getData(), ...toUpdate };
		for (const key of toDelete) {
			delete updatedData[key];
		}
		this.setData(updatedData);
	}

	/**
	 * Returns the decrypted credential object
	 */
	getData(): T {
		if (this.data === undefined) {
			throw new CredentialDataError(this, CREDENTIAL_ERRORS.NO_DATA);
		}

		let decryptedData: string;
		try {
			decryptedData = this.cipher.decrypt(this.data);
		} catch (cause) {
			throw new CredentialDataError(this, CREDENTIAL_ERRORS.DECRYPTION_FAILED, cause);
		}

		try {
			return jsonParse(decryptedData);
		} catch (cause) {
			throw new CredentialDataError(this, CREDENTIAL_ERRORS.INVALID_JSON, cause);
		}
	}

	/**
	 * Returns the encrypted credentials to be saved
	 */
	getDataToSave(): ICredentialsEncrypted {
		if (this.data === undefined) {
			throw new ApplicationError('No credentials were set to save.');
		}

		return {
			id: this.id,
			name: this.name,
			type: this.type,
			data: this.data,
		};
	}
}
