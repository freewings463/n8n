"""
MIGRATION-META:
  source_path: packages/core/src/encryption/cipher.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/encryption 的模块。导入/依赖:外部:无；内部:@n8n/di、@/instance-settings；本地:无。导出:Cipher。关键函数/方法:encrypt、decrypt、getKeyAndIv。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/encryption/cipher.ts -> services/n8n/application/core/services/encryption/cipher.py

import { Service } from '@n8n/di';
import { createHash, createCipheriv, createDecipheriv, randomBytes } from 'crypto';

import { InstanceSettings } from '@/instance-settings';

// Data encrypted by CryptoJS always starts with these bytes
const RANDOM_BYTES = Buffer.from('53616c7465645f5f', 'hex');

@Service()
export class Cipher {
	constructor(private readonly instanceSettings: InstanceSettings) {}

	encrypt(data: string | object, customEncryptionKey?: string) {
		const salt = randomBytes(8);
		const [key, iv] = this.getKeyAndIv(salt, customEncryptionKey);
		const cipher = createCipheriv('aes-256-cbc', key, iv);
		const encrypted = cipher.update(typeof data === 'string' ? data : JSON.stringify(data));
		return Buffer.concat([RANDOM_BYTES, salt, encrypted, cipher.final()]).toString('base64');
	}

	decrypt(data: string, customEncryptionKey?: string) {
		const input = Buffer.from(data, 'base64');
		if (input.length < 16) return '';
		const salt = input.subarray(8, 16);
		const [key, iv] = this.getKeyAndIv(salt, customEncryptionKey);
		const contents = input.subarray(16);
		const decipher = createDecipheriv('aes-256-cbc', key, iv);
		return Buffer.concat([decipher.update(contents), decipher.final()]).toString('utf-8');
	}

	private getKeyAndIv(salt: Buffer, customEncryptionKey?: string): [Buffer, Buffer] {
		const encryptionKey = customEncryptionKey ?? this.instanceSettings.encryptionKey;
		const password = Buffer.concat([Buffer.from(encryptionKey, 'binary'), salt]);
		const hash1 = createHash('md5').update(password).digest();
		const hash2 = createHash('md5')
			.update(Buffer.concat([hash1, password]))
			.digest();
		const iv = createHash('md5')
			.update(Buffer.concat([hash2, password]))
			.digest();
		const key = Buffer.concat([hash1, hash2]);
		return [key, iv];
	}
}
