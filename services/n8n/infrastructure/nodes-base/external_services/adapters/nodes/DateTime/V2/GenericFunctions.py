"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DateTime/V2/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DateTime/V2 的节点。导入/依赖:外部:luxon、moment-timezone；内部:n8n-workflow；本地:无。导出:parseDate。关键函数/方法:parseDate、offset。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DateTime/V2/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DateTime/V2/GenericFunctions.py

import { DateTime } from 'luxon';
import moment from 'moment-timezone';
import type { IExecuteFunctions } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

export function parseDate(
	this: IExecuteFunctions,
	date: string | number | DateTime,
	options: Partial<{
		timezone: string;
		fromFormat: string;
	}> = {},
) {
	let parsedDate;

	if (date instanceof DateTime) {
		parsedDate = date;
	} else {
		// Check if the input is a number, don't convert to number if fromFormat is set
		if (!Number.isNaN(Number(date)) && !options.fromFormat) {
			//input is a number, convert to number in case it is a string formatted number
			date = Number(date);
			// check if the number is a timestamp in float format and convert to integer
			if (!Number.isInteger(date)) {
				date = date * 1000;
			}
		}

		let timezone = options.timezone;
		if (Number.isInteger(date)) {
			const timestampLengthInMilliseconds1990 = 12;
			// check if the number is a timestamp in seconds or milliseconds and create a moment object accordingly
			if (date.toString().length < timestampLengthInMilliseconds1990) {
				parsedDate = DateTime.fromSeconds(date as number);
			} else {
				parsedDate = DateTime.fromMillis(date as number);
			}
		} else {
			if (!timezone && (date as string).includes('+')) {
				const offset = (date as string).split('+')[1].slice(0, 2) as unknown as number;
				timezone = `Etc/GMT-${offset * 1}`;
			}

			if (options.fromFormat) {
				parsedDate = DateTime.fromFormat(date as string, options.fromFormat);
			} else {
				parsedDate = DateTime.fromISO(moment(date).toISOString());
			}
		}

		parsedDate = parsedDate.setZone(timezone || 'Etc/UTC');

		if (parsedDate.invalidReason === 'unparsable') {
			throw new NodeOperationError(this.getNode(), 'Invalid date format');
		}
	}
	return parsedDate;
}
