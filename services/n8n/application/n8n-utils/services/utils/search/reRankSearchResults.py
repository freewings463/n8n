"""
MIGRATION-META:
  source_path: packages/@n8n/utils/src/search/reRankSearchResults.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/utils/src/search 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:reRankSearchResults。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Generic shared utilities -> application/services/utils
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/utils/src/search/reRankSearchResults.ts -> services/n8n/application/n8n-utils/services/utils/search/reRankSearchResults.py

export function reRankSearchResults<T extends { key: string }>(
	searchResults: Array<{ score: number; item: T }>,
	additionalFactors: Record<string, Record<string, number>>,
): Array<{ score: number; item: T }> {
	return searchResults
		.map(({ score, item }) => {
			// For each additional factor, we check if it exists for the item and type,
			// and if so, we add the score to the item's score.
			const additionalScore = Object.entries(additionalFactors).reduce((acc, [_, factorScores]) => {
				const factorScore = factorScores[item.key];
				if (factorScore) {
					return acc + factorScore;
				}

				return acc;
			}, 0);

			return {
				score: score + additionalScore,
				item,
			};
		})
		.sort((a, b) => {
			return b.score - a.score;
		});
}
