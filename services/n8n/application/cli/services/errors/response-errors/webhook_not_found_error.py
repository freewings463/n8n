"""
MIGRATION-META:
  source_path: packages/cli/src/errors/response-errors/webhook-not-found.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/errors/response-errors 的Webhook错误。导入/依赖:外部:无；内部:无；本地:./not-found.error。导出:webhookNotFoundErrorMessage、WebhookNotFoundError。关键函数/方法:webhookNotFoundErrorMessage。用于承载Webhook实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/errors/response-errors/webhook-not-found.error.ts -> services/n8n/application/cli/services/errors/response-errors/webhook_not_found_error.py

import { NotFoundError } from './not-found.error';

export const webhookNotFoundErrorMessage = ({
	path,
	httpMethod,
	webhookMethods,
}: {
	path: string;
	httpMethod?: string;
	webhookMethods?: string[];
}) => {
	let webhookPath = path;

	if (httpMethod) {
		webhookPath = `${httpMethod} ${webhookPath}`;
	}

	if (webhookMethods?.length && httpMethod) {
		let methods = '';

		if (webhookMethods.length === 1) {
			methods = webhookMethods[0];
		} else {
			const lastMethod = webhookMethods.pop();

			methods = `${webhookMethods.join(', ')} or ${lastMethod as string}`;
		}

		return `This webhook is not registered for ${httpMethod} requests. Did you mean to make a ${methods} request?`;
	} else {
		return `The requested webhook "${webhookPath}" is not registered.`;
	}
};

export class WebhookNotFoundError extends NotFoundError {
	constructor(
		{
			path,
			httpMethod,
			webhookMethods,
		}: {
			path: string;
			httpMethod?: string;
			webhookMethods?: string[];
		},
		{ hint }: { hint: 'default' | 'production' } = { hint: 'default' },
	) {
		const errorMsg = webhookNotFoundErrorMessage({ path, httpMethod, webhookMethods });

		let hintMsg = '';
		if (!webhookMethods?.length) {
			hintMsg =
				hint === 'default'
					? "Click the 'Execute workflow' button on the canvas, then try again. (In test mode, the webhook only works for one call after you click this button)"
					: "The workflow must be active for a production URL to run successfully. You can activate the workflow using the toggle in the top-right of the editor. Note that unlike test URL calls, production URL calls aren't shown on the canvas (only in the executions list)";
		}

		super(errorMsg, hintMsg);
	}
}
