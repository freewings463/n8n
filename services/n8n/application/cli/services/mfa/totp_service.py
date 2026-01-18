"""
MIGRATION-META:
  source_path: packages/cli/src/mfa/totp.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/mfa 的服务。导入/依赖:外部:otpauth；内部:@n8n/di；本地:无。导出:TOTPService。关键函数/方法:generateSecret、generateTOTPUri、verifySecret、generateTOTP。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/mfa/totp.service.ts -> services/n8n/application/cli/services/mfa/totp_service.py

import { Service } from '@n8n/di';
import OTPAuth from 'otpauth';

@Service()
export class TOTPService {
	generateSecret(): string {
		return new OTPAuth.Secret()?.base32;
	}

	generateTOTPUri({
		issuer = 'n8n',
		secret,
		label,
	}: {
		secret: string;
		label: string;
		issuer?: string;
	}) {
		return new OTPAuth.TOTP({
			secret: OTPAuth.Secret.fromBase32(secret),
			issuer,
			label,
		}).toString();
	}

	verifySecret({
		secret,
		mfaCode,
		window = 2,
	}: { secret: string; mfaCode: string; window?: number }) {
		return new OTPAuth.TOTP({
			secret: OTPAuth.Secret.fromBase32(secret),
		}).validate({ token: mfaCode, window }) === null
			? false
			: true;
	}

	generateTOTP(secret: string) {
		return OTPAuth.TOTP.generate({
			secret: OTPAuth.Secret.fromBase32(secret),
		});
	}
}
