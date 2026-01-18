"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/user-settings.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的控制器。导入/依赖:外部:无；内部:@n8n/decorators、n8n-workflow、@/errors/…/bad-request.error、@/requests、@/services/user.service；本地:无。导出:UserSettingsController。关键函数/方法:getNpsSurveyState、updateNpsSurvey。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/user-settings.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/user_settings_controller.py

import { Patch, RestController } from '@n8n/decorators';
import type { NpsSurveyState } from 'n8n-workflow';

import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import { NpsSurveyRequest } from '@/requests';
import { UserService } from '@/services/user.service';

function getNpsSurveyState(state: unknown): NpsSurveyState | undefined {
	if (typeof state !== 'object' || state === null) {
		return;
	}
	if (!('lastShownAt' in state) || typeof state.lastShownAt !== 'number') {
		return;
	}
	if ('responded' in state && state.responded === true) {
		return {
			responded: true,
			lastShownAt: state.lastShownAt,
		};
	}

	if (
		'waitingForResponse' in state &&
		state.waitingForResponse === true &&
		'ignoredCount' in state &&
		typeof state.ignoredCount === 'number'
	) {
		return {
			waitingForResponse: true,
			ignoredCount: state.ignoredCount,
			lastShownAt: state.lastShownAt,
		};
	}

	return;
}

@RestController('/user-settings')
export class UserSettingsController {
	constructor(private readonly userService: UserService) {}

	@Patch('/nps-survey')
	async updateNpsSurvey(req: NpsSurveyRequest.NpsSurveyUpdate): Promise<void> {
		const state = getNpsSurveyState(req.body);
		if (!state) {
			throw new BadRequestError('Invalid nps survey state structure');
		}

		await this.userService.updateSettings(req.user.id, {
			npsSurvey: state,
		});
	}
}
