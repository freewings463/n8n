"""
MIGRATION-META:
  source_path: packages/cli/src/modules/insights/database/repositories/insights-by-period-query.helper.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/insights/database 的Insights仓储。导入/依赖:外部:luxon；内部:@n8n/config、@n8n/db；本地:无。导出:getDateRangesCommonTableExpressionQuery、getDateRangesSelectQuery。关键函数/方法:getDateRangesCommonTableExpressionQuery、getDateRangesSelectQuery、CAST。用于封装Insights数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/insights/database/repositories/insights-by-period-query.helper.ts -> services/n8n/application/cli/services/modules/insights/database/repositories/insights_by_period_query_helper.py

import type { DatabaseConfig } from '@n8n/config';
import { sql } from '@n8n/db';
import { DateTime } from 'luxon';

/**
 * Generates a SQL Common Table Expression (CTE) query that provides three date boundaries for insights queries
 *
 * Behavior:
 * - If the end date is today and the start date is also today, start date is set to the start of the day to take today's data.
 * - If the end date is in the past, both start and end dates are set to the start of their respective days, to take full days.
 *
 * The SQL CTE can be joined with the insights table for filtering/aggregation.
 *
 * @param startDate - The start date of the range (inclusive)
 * @param endDate - The end date of the range (inclusive, or "now" if today)
 * @param dbType - The database type (postgresdb, mysqldb, mariadb, or sqlite)
 * @returns SQL CTE query with `prev_start_date`, `start_date`, and `end_date` columns
 * - `prev_start_date`: The start of the previous period (used for comparison)
 * - `start_date`: The start of the current period (inclusive)
 * - `end_date`: The end of the current period (exclusive)
 */
export const getDateRangesCommonTableExpressionQuery = ({
	startDate,
	endDate,
	dbType,
}: {
	startDate: Date;
	endDate: Date;
	dbType: DatabaseConfig['type'];
}) => {
	let startDateTime = DateTime.fromJSDate(startDate).toUTC();
	let endDateTime = DateTime.fromJSDate(endDate).toUTC();

	const today = DateTime.now().toUTC();
	const isEndDateToday = endDateTime.hasSame(today, 'day');

	// Past range, take full days
	if (!isEndDateToday) {
		startDateTime = startDateTime.startOf('day');
		endDateTime = endDateTime.plus({ days: 1 }).startOf('day');
	}

	// Today range, take all day data starting from the beginning of the day
	if (isEndDateToday && startDateTime.hasSame(endDateTime, 'day')) {
		startDateTime = startDateTime.startOf('day');
	}

	const prevStartDateTime = startDateTime.minus(endDateTime.diff(startDateTime));

	return getDateRangesSelectQuery({ dbType, prevStartDateTime, startDateTime, endDateTime });
};

export function getDateRangesSelectQuery({
	dbType,
	prevStartDateTime,
	startDateTime,
	endDateTime,
}: {
	dbType: DatabaseConfig['type'];
	prevStartDateTime: DateTime;
	startDateTime: DateTime;
	endDateTime: DateTime;
}) {
	const prevStartStr = prevStartDateTime.toSQL({ includeZone: false, includeOffset: false });
	const startStr = startDateTime.toSQL({ includeZone: false, includeOffset: false });
	const endStr = endDateTime.toSQL({ includeZone: false, includeOffset: false });

	// Database-specific timestamp casting
	// PostgreSQL requires explicit CAST or :: syntax for timestamp comparisons
	// SQLite and MySQL/MariaDB can work with string literals in comparisons
	if (dbType === 'postgresdb') {
		return sql`SELECT
			CAST('${prevStartStr}' AS TIMESTAMP) AS prev_start_date,
			CAST('${startStr}' AS TIMESTAMP) AS start_date,
			CAST('${endStr}' AS TIMESTAMP) AS end_date
		`;
	}

	return sql`SELECT
			'${prevStartStr}' AS prev_start_date,
			'${startStr}' AS start_date,
			'${endStr}' AS end_date
	`;
}
