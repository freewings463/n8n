"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/types/source-control-preferences.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/source-control.ee/types 的类型。导入/依赖:外部:class-validator；内部:无；本地:./key-pair-type。导出:SourceControlPreferences。关键函数/方法:fromJSON、merge。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/types/source-control-preferences.ts -> services/n8n/application/cli/services/modules/source-control.ee/types/source_control_preferences.py

import { IsBoolean, IsHexColor, IsOptional, IsString, IsIn } from 'class-validator';

import { KeyPairType } from './key-pair-type';

export class SourceControlPreferences {
	constructor(preferences: Partial<SourceControlPreferences> | undefined = undefined) {
		if (preferences) Object.assign(this, preferences);
	}

	@IsBoolean()
	connected: boolean;

	@IsString()
	repositoryUrl: string;

	@IsString()
	branchName = 'main';

	@IsBoolean()
	branchReadOnly: boolean;

	@IsHexColor()
	branchColor: string;

	@IsOptional()
	@IsString()
	readonly publicKey?: string;

	@IsOptional()
	@IsBoolean()
	readonly initRepo?: boolean;

	@IsOptional()
	@IsString()
	readonly keyGeneratorType?: KeyPairType;

	@IsOptional()
	@IsIn(['ssh', 'https'])
	connectionType?: 'ssh' | 'https' = 'ssh';

	@IsOptional()
	@IsString()
	httpsUsername?: string;

	@IsOptional()
	@IsString()
	httpsPassword?: string;

	static fromJSON(json: Partial<SourceControlPreferences>): SourceControlPreferences {
		return new SourceControlPreferences(json);
	}

	static merge(
		preferences: Partial<SourceControlPreferences>,
		defaultPreferences: Partial<SourceControlPreferences>,
	): SourceControlPreferences {
		return new SourceControlPreferences({
			connected: preferences.connected ?? defaultPreferences.connected,
			repositoryUrl: preferences.repositoryUrl ?? defaultPreferences.repositoryUrl,
			branchName: preferences.branchName ?? defaultPreferences.branchName,
			branchReadOnly: preferences.branchReadOnly ?? defaultPreferences.branchReadOnly,
			branchColor: preferences.branchColor ?? defaultPreferences.branchColor,
			keyGeneratorType: preferences.keyGeneratorType ?? defaultPreferences.keyGeneratorType,
			connectionType: preferences.connectionType ?? defaultPreferences.connectionType,
			httpsUsername: preferences.httpsUsername ?? defaultPreferences.httpsUsername,
			httpsPassword: preferences.httpsPassword ?? defaultPreferences.httpsPassword,
		});
	}
}
