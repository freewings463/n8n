"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/survey-answers.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的控制器。导入/依赖:外部:class-transformer、class-validator；内部:@n8n/db、n8n-workflow；本地:无。导出:PersonalizationSurveyAnswersV4。关键函数/方法:无。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Controller -> presentation/api/v1/controllers
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/survey-answers.dto.ts -> services/n8n/presentation/cli/api/v1/controllers/survey_answers_dto.py

import { NoXss } from '@n8n/db';
import { Expose } from 'class-transformer';
import { IsString, IsArray, IsOptional, IsEmail, IsEnum } from 'class-validator';
import type { IPersonalizationSurveyAnswersV4 } from 'n8n-workflow';

export class PersonalizationSurveyAnswersV4 implements IPersonalizationSurveyAnswersV4 {
	@NoXss()
	@Expose()
	@IsEnum(['v4'])
	version: 'v4';

	@NoXss()
	@Expose()
	@IsString()
	personalization_survey_submitted_at: string;

	@NoXss()
	@Expose()
	@IsString()
	personalization_survey_n8n_version: string;

	@Expose()
	@IsOptional()
	@IsArray()
	@NoXss({ each: true })
	@IsString({ each: true })
	automationGoalDevops?: string[] | null;

	@NoXss()
	@Expose()
	@IsOptional()
	@IsString()
	automationGoalDevopsOther?: string | null;

	@NoXss({ each: true })
	@Expose()
	@IsOptional()
	@IsArray()
	@IsString({ each: true })
	companyIndustryExtended?: string[] | null;

	@NoXss({ each: true })
	@Expose()
	@IsOptional()
	@IsString({ each: true })
	otherCompanyIndustryExtended?: string[] | null;

	@IsEnum(['<20', '20-99', '100-499', '500-999', '1000+', 'personalUser'])
	@Expose()
	@IsOptional()
	@IsString()
	companySize?: string | null;

	@NoXss()
	@Expose()
	@IsOptional()
	@IsString()
	companyType?: string | null;

	@NoXss({ each: true })
	@Expose()
	@IsOptional()
	@IsArray()
	@IsString({ each: true })
	automationGoalSm?: string[] | null;

	@NoXss()
	@Expose()
	@IsOptional()
	@IsString()
	automationGoalSmOther?: string | null;

	@NoXss({ each: true })
	@Expose()
	@IsOptional()
	@IsArray()
	@IsString({ each: true })
	usageModes?: string[] | null;

	@NoXss()
	@Expose()
	@IsOptional()
	@IsEmail()
	email?: string | null;

	@NoXss()
	@Expose()
	@IsOptional()
	@IsString()
	role?: string | null;

	@NoXss()
	@Expose()
	@IsOptional()
	@IsString()
	roleOther?: string | null;

	@NoXss()
	@Expose()
	@IsOptional()
	@IsString()
	reportedSource?: string | null;

	@NoXss()
	@Expose()
	@IsOptional()
	@IsString()
	reportedSourceOther?: string | null;
}
