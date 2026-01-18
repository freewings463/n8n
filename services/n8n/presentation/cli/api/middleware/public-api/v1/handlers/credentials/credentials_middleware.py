"""
MIGRATION-META:
  source_path: packages/cli/src/public-api/v1/handlers/credentials/credentials.middleware.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/public-api/v1/handlers 的中间件。导入/依赖:外部:express、jsonschema；内部:@n8n/di、n8n-workflow 等2项；本地:./credentials.service 等1项。导出:validCredentialType、validCredentialsProperties、validCredentialTypeForUpdate、validCredentialsPropertiesForUpdate。关键函数/方法:validateCredentialData、validCredentialType、validCredentialsProperties、validCredentialTypeForUpdate 等1项。用于为该模块提供鉴权、拦截、上下文或统一异常处理。注释目标:eslint-dis…
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/public-api/v1/handlers/credentials/credentials.middleware.ts -> services/n8n/presentation/cli/api/middleware/public-api/v1/handlers/credentials/credentials_middleware.py

/* eslint-disable @typescript-eslint/no-invalid-void-type */

import { Container } from '@n8n/di';
import type express from 'express';
import { validate } from 'jsonschema';
import type { IDataObject } from 'n8n-workflow';

import { CredentialTypes } from '@/credential-types';
import { CredentialsHelper } from '@/credentials-helper';

import { getCredentials, toJsonSchema } from './credentials.service';
import type { CredentialRequest } from '../../../types';

/**
 * Helper function to validate credential data against a credential type schema
 * @param credentialType - The credential type to validate against
 * @param data - The credential data to validate
 * @param res - Express response object
 * @returns Express response with error message if validation fails, or undefined if valid
 */
function validateCredentialData(
	credentialType: string,
	data: IDataObject,
	res: express.Response,
): express.Response | void {
	const properties = Container.get(CredentialsHelper)
		.getCredentialsProperties(credentialType)
		.filter((property) => property.type !== 'hidden');

	const schema = toJsonSchema(properties);

	const { valid, errors } = validate(data, schema, { nestedErrors: true });

	if (!valid) {
		return res.status(400).json({
			message: errors.map((error) => `request.body.data ${error.message}`).join(','),
		});
	}
}

export const validCredentialType = (
	req: CredentialRequest.Create,
	res: express.Response,
	next: express.NextFunction,
): express.Response | void => {
	try {
		Container.get(CredentialTypes).getByName(req.body.type);
	} catch {
		return res.status(400).json({ message: 'req.body.type is not a known type' });
	}

	return next();
};

export const validCredentialsProperties = (
	req: CredentialRequest.Create,
	res: express.Response,
	next: express.NextFunction,
): express.Response | void => {
	const { type, data } = req.body;

	const validationResult = validateCredentialData(type, data, res);
	if (validationResult) {
		return validationResult;
	}

	return next();
};

export const validCredentialTypeForUpdate = (
	req: CredentialRequest.Update,
	res: express.Response,
	next: express.NextFunction,
): express.Response | void => {
	const { type } = req.body;

	// If type is provided, validate it
	if (type !== undefined) {
		try {
			Container.get(CredentialTypes).getByName(type);
		} catch {
			return res.status(400).json({ message: 'req.body.type is not a known type' });
		}
	}

	return next();
};

export const validCredentialsPropertiesForUpdate = async (
	req: CredentialRequest.Update,
	res: express.Response,
	next: express.NextFunction,
): Promise<express.Response | void> => {
	let { type } = req.body;
	const { data } = req.body;
	const { id: credentialId } = req.params;

	// Only validate if data is provided
	if (data !== undefined) {
		// Fetch existing credential to get type if not provided
		if (type === undefined) {
			const existingCredential = await getCredentials(credentialId);
			if (!existingCredential) {
				return res.status(404).json({ message: 'Credential not found' });
			}
			type = existingCredential.type;
		}

		// Validate data against type
		const validationResult = validateCredentialData(type, data, res);
		if (validationResult) {
			return validationResult;
		}
	}

	// If type is provided but data is not, check if type is changing
	if (type !== undefined && data === undefined) {
		const existingCredential = await getCredentials(credentialId);
		if (!existingCredential) {
			return res.status(404).json({ message: 'Credential not found' });
		}

		// If the type is changing, data must be provided
		if (existingCredential.type !== type) {
			return res.status(400).json({
				message:
					'req.body.data is required when changing credential type. The existing data cannot be used with the new type.',
			});
		}
	}

	return next();
};
