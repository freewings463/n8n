"""
MIGRATION-META:
  source_path: packages/cli/src/mfa/mfa.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/mfa 的服务。导入/依赖:外部:uuid；内部:@n8n/backend-common、@n8n/db、@n8n/di、n8n-core、@/errors/…/invalid-mfa-code.error 等1项；本地:./constants、./totp.service。导出:MfaService。关键函数/方法:init、generateRecoveryCodes、loadMFASettings、enforceMFA、isMFAEnforced、saveSecretAndRecoveryCodes、encryptSecretAndRecoveryCodes、decryptSecretAndRecoveryCodes、getSecretAndRecoveryCodes、validateMfa 等4项。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/mfa/mfa.service.ts -> services/n8n/application/cli/services/mfa/mfa_service.py

import { LicenseState, Logger } from '@n8n/backend-common';
import { SettingsRepository, UserRepository } from '@n8n/db';
import { Service } from '@n8n/di';
import { Cipher } from 'n8n-core';
import { v4 as uuid } from 'uuid';

import { InvalidMfaCodeError } from '@/errors/response-errors/invalid-mfa-code.error';
import { InvalidMfaRecoveryCodeError } from '@/errors/response-errors/invalid-mfa-recovery-code-error';

import { MFA_ENFORCE_SETTING } from './constants';
import { TOTPService } from './totp.service';

@Service()
export class MfaService {
	private enforceMFAValue: boolean = false;

	constructor(
		private userRepository: UserRepository,
		private settingsRepository: SettingsRepository,
		private license: LicenseState,
		public totp: TOTPService,
		private cipher: Cipher,
		private logger: Logger,
	) {}

	async init() {
		try {
			await this.loadMFASettings();
		} catch (error) {
			this.logger.warn('Failed to load MFA settings', { error });
		}
	}

	generateRecoveryCodes(n = 10) {
		return Array.from(Array(n)).map(() => uuid());
	}

	private async loadMFASettings() {
		const value = await this.settingsRepository.findByKey(MFA_ENFORCE_SETTING);
		if (value) {
			this.enforceMFAValue = value.value === 'true';
		}
	}

	async enforceMFA(value: boolean) {
		if (!this.license.isMFAEnforcementLicensed()) {
			value = false; // If the license does not allow MFA enforcement, set it to false
		}
		await this.settingsRepository.upsert(
			{
				key: MFA_ENFORCE_SETTING,
				value: `${value}`,
				loadOnStartup: true,
			},
			['key'],
		);
		this.enforceMFAValue = value;
	}

	isMFAEnforced() {
		return this.license.isMFAEnforcementLicensed() && this.enforceMFAValue;
	}

	async saveSecretAndRecoveryCodes(userId: string, secret: string, recoveryCodes: string[]) {
		const { encryptedSecret, encryptedRecoveryCodes } = this.encryptSecretAndRecoveryCodes(
			secret,
			recoveryCodes,
		);

		const user = await this.userRepository.findOneByOrFail({ id: userId });
		user.mfaSecret = encryptedSecret;
		user.mfaRecoveryCodes = encryptedRecoveryCodes;
		await this.userRepository.save(user);
	}

	encryptSecretAndRecoveryCodes(rawSecret: string, rawRecoveryCodes: string[]) {
		const encryptedSecret = this.cipher.encrypt(rawSecret),
			encryptedRecoveryCodes = rawRecoveryCodes.map((code) => this.cipher.encrypt(code));
		return {
			encryptedRecoveryCodes,
			encryptedSecret,
		};
	}

	private decryptSecretAndRecoveryCodes(mfaSecret: string, mfaRecoveryCodes: string[]) {
		return {
			decryptedSecret: this.cipher.decrypt(mfaSecret),
			decryptedRecoveryCodes: mfaRecoveryCodes.map((code) => this.cipher.decrypt(code)),
		};
	}

	async getSecretAndRecoveryCodes(userId: string) {
		const { mfaSecret, mfaRecoveryCodes } = await this.userRepository.findOneByOrFail({
			id: userId,
		});
		return this.decryptSecretAndRecoveryCodes(mfaSecret ?? '', mfaRecoveryCodes ?? []);
	}

	async validateMfa(
		userId: string,
		mfaCode: string | undefined,
		mfaRecoveryCode: string | undefined,
	) {
		const user = await this.userRepository.findOneByOrFail({ id: userId });
		if (mfaCode) {
			const decryptedSecret = this.cipher.decrypt(user.mfaSecret!);
			return this.totp.verifySecret({ secret: decryptedSecret, mfaCode });
		}

		if (mfaRecoveryCode) {
			const validCodes = user.mfaRecoveryCodes.map((code) => this.cipher.decrypt(code));
			const index = validCodes.indexOf(mfaRecoveryCode);
			if (index === -1) return false;
			// remove used recovery code
			validCodes.splice(index, 1);
			user.mfaRecoveryCodes = validCodes.map((code) => this.cipher.encrypt(code));
			await this.userRepository.save(user);
			return true;
		}

		return false;
	}

	async enableMfa(userId: string) {
		const user = await this.userRepository.findOneOrFail({
			where: { id: userId },
			relations: ['role'],
		});
		user.mfaEnabled = true;
		return await this.userRepository.save(user);
	}

	async disableMfaWithMfaCode(userId: string, mfaCode: string) {
		const isValidToken = await this.validateMfa(userId, mfaCode, undefined);

		if (!isValidToken) {
			throw new InvalidMfaCodeError();
		}

		await this.disableMfaForUser(userId);
	}

	async disableMfaWithRecoveryCode(userId: string, recoveryCode: string) {
		const isValidToken = await this.validateMfa(userId, undefined, recoveryCode);

		if (!isValidToken) {
			throw new InvalidMfaRecoveryCodeError();
		}

		await this.disableMfaForUser(userId);
	}

	private async disableMfaForUser(userId: string) {
		await this.userRepository.update(userId, {
			mfaEnabled: false,
			mfaSecret: null,
			mfaRecoveryCodes: [],
		});
	}
}
