"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/utils/csv-prompt-loader.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations/utils 的工作流工具。导入/依赖:外部:csv-parse/sync；内部:无；本地:../types/evaluation.js。导出:loadTestCasesFromCsv。关键函数/方法:isHeaderRow、detectColumnIndex、sanitizeValue、generateNameFromPrompt、parseCsv、loadTestCasesFromCsv。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/utils/csv-prompt-loader.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/container/evaluations/utils/csv_prompt_loader.py

import { parse } from 'csv-parse/sync';
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';

import type { TestCase } from '../types/evaluation.js';

type ParsedCsvRow = string[];

function isHeaderRow(row: ParsedCsvRow) {
	return row.some((cell) => cell.trim().toLowerCase() === 'prompt');
}

function detectColumnIndex(header: ParsedCsvRow, name: string) {
	const normalized = name.toLowerCase();
	const index = header.findIndex((cell) => cell.trim().toLowerCase() === normalized);
	return index >= 0 ? index : undefined;
}

function sanitizeValue(value: string | undefined) {
	return value?.trim() ?? '';
}

function generateNameFromPrompt(prompt: string, index: number) {
	const normalized = prompt.replace(/\s+/g, ' ').trim();
	if (!normalized) {
		return `CSV Prompt ${index + 1}`;
	}

	const maxLength = 60;
	if (normalized.length <= maxLength) {
		return normalized;
	}

	return `${normalized.slice(0, maxLength - 3)}...`;
}

function parseCsv(content: string): ParsedCsvRow[] {
	try {
		const rows = parse(content.replace(/^\ufeff/, ''), {
			columns: false,
			skip_empty_lines: true,
			trim: true,
			relax_column_count: true,
		}) as ParsedCsvRow[];

		return rows.map((row) => row.map((cell) => cell ?? ''));
	} catch (error) {
		const message = error instanceof Error ? error.message : 'Unknown parsing error';
		throw new Error(`Failed to parse CSV file: ${message}`);
	}
}

export function loadTestCasesFromCsv(csvPath: string): TestCase[] {
	const resolvedPath = path.isAbsolute(csvPath) ? csvPath : path.resolve(process.cwd(), csvPath);

	if (!existsSync(resolvedPath)) {
		throw new Error(`CSV file not found at ${resolvedPath}`);
	}

	const fileContents = readFileSync(resolvedPath, 'utf8');
	const rows = parseCsv(fileContents);

	if (rows.length === 0) {
		throw new Error('The provided CSV file is empty');
	}

	let header: ParsedCsvRow | undefined;
	let dataRows = rows;

	if (isHeaderRow(rows[0])) {
		header = rows[0]!;
		dataRows = rows.slice(1);
	}

	if (dataRows.length === 0) {
		throw new Error('No prompt rows found in the provided CSV file');
	}

	const promptIndex = header ? (detectColumnIndex(header, 'prompt') ?? 0) : 0;
	const idIndex = header ? detectColumnIndex(header, 'id') : undefined;
	const nameIndex = header
		? (detectColumnIndex(header, 'name') ?? detectColumnIndex(header, 'title'))
		: undefined;

	const testCases = dataRows
		.map<TestCase | undefined>((row, index) => {
			const prompt = sanitizeValue(row[promptIndex]);
			if (!prompt) {
				return undefined;
			}

			const idSource = sanitizeValue(idIndex !== undefined ? row[idIndex] : undefined);
			const nameSource = sanitizeValue(nameIndex !== undefined ? row[nameIndex] : undefined);

			return {
				id: idSource || `csv-case-${index + 1}`,
				name: nameSource || generateNameFromPrompt(prompt, index),
				prompt,
			};
		})
		.filter((testCase): testCase is TestCase => testCase !== undefined);

	if (testCases.length === 0) {
		throw new Error('No valid prompts found in the provided CSV file');
	}

	return testCases;
}
