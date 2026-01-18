"""
MIGRATION-META:
  source_path: packages/cli/src/events/events.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/events 的控制器。导入/依赖:外部:无；内部:@n8n/db、@n8n/decorators；本地:./event.service。导出:EventsController。关键函数/方法:sessionStarted。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/events/events.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/events/events_controller.py

import { AuthenticatedRequest } from '@n8n/db';
import { Get, RestController } from '@n8n/decorators';

import { EventService } from './event.service';

/** This controller holds endpoints that the frontend uses to trigger telemetry events */
@RestController('/events')
export class EventsController {
	constructor(private readonly eventService: EventService) {}

	@Get('/session-started')
	sessionStarted(req: AuthenticatedRequest) {
		const pushRef = req.headers['push-ref'];
		this.eventService.emit('session-started', { pushRef });
	}
}
