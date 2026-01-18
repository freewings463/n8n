"""
MIGRATION-META:
  source_path: packages/cli/src/services/jwt.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/services 的JWT服务。导入/依赖:外部:jsonwebtoken；内部:@n8n/config、@n8n/di、n8n-core；本地:无。导出:JwtService、JwtPayload。关键函数/方法:sign。用于封装JWT业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/services/jwt.service.ts -> services/n8n/application/cli/services/jwt_service.py

import { GlobalConfig } from '@n8n/config';
import { Container, Service } from '@n8n/di';
import { createHash } from 'crypto';
import jwt from 'jsonwebtoken';
import { InstanceSettings } from 'n8n-core';

@Service()
export class JwtService {
	jwtSecret: string = '';

	constructor({ encryptionKey }: InstanceSettings, globalConfig: GlobalConfig) {
		this.jwtSecret = globalConfig.userManagement.jwtSecret;
		if (!this.jwtSecret) {
			// If we don't have a JWT secret set, generate one based on encryption key.
			// For a key off every other letter from encryption key
			// CAREFUL: do not change this or it breaks all existing tokens.
			let baseKey = '';
			for (let i = 0; i < encryptionKey.length; i += 2) {
				baseKey += encryptionKey[i];
			}
			this.jwtSecret = createHash('sha256').update(baseKey).digest('hex');
			Container.get(GlobalConfig).userManagement.jwtSecret = this.jwtSecret;
		}
	}

	sign(payload: object, options: jwt.SignOptions = {}): string {
		return jwt.sign(payload, this.jwtSecret, options);
	}

	decode<T = JwtPayload>(token: string) {
		return jwt.decode(token) as T;
	}

	verify<T = JwtPayload>(token: string, options: jwt.VerifyOptions = {}) {
		return jwt.verify(token, this.jwtSecret, options) as T;
	}
}

export type JwtPayload = jwt.JwtPayload;
