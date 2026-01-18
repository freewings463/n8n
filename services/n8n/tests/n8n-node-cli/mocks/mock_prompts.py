"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/test-utils/mock-prompts.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/test-utils 的模块。导入/依赖:外部:@clack/prompts；内部:无；本地:无。导出:MockPrompt。关键函数/方法:setup、reset、getAskedQuestions、setupMocks。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - CLI test utilities -> tests/mocks
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/test-utils/mock-prompts.ts -> services/n8n/tests/n8n-node-cli/mocks/mock_prompts.py

import { confirm, isCancel, text, select } from '@clack/prompts';

interface PromptConfig {
	message: string;
	placeholder?: string;
	defaultValue?: string;
	options?: Array<{ label: string; value: unknown; hint?: string }>;
}

type PromptAnswer<T = unknown> = T | 'CANCEL';

interface QuestionAnswerPair<T = unknown> {
	question: string | Partial<PromptConfig>;
	answer: PromptAnswer<T>;
}

export class MockPrompt {
	private static readonly questionAnswers = new Map<string, PromptAnswer>();
	private static readonly askedQuestions = new Set<string>();

	static setup(pairs: QuestionAnswerPair[]): void {
		MockPrompt.reset();

		for (const { question, answer } of pairs) {
			const key = typeof question === 'string' ? question : question.message!;
			MockPrompt.questionAnswers.set(key, answer);
		}

		MockPrompt.setupMocks();
	}

	static reset(): void {
		vi.mocked(confirm).mockReset();
		vi.mocked(text).mockReset();
		vi.mocked(select).mockReset();
		vi.mocked(isCancel).mockReset();
		MockPrompt.questionAnswers.clear();
		MockPrompt.askedQuestions.clear();
	}

	static getAskedQuestions(): string[] {
		return Array.from(MockPrompt.askedQuestions);
	}

	private static setupMocks(): void {
		vi.mocked(select).mockImplementation(async (config) => {
			MockPrompt.askedQuestions.add(config.message);
			const answer = MockPrompt.questionAnswers.get(config.message);
			if (answer === undefined) {
				throw new Error(`No mock answer configured for select question: "${config.message}"`);
			}
			if (answer === 'CANCEL') {
				return await Promise.resolve(Symbol('cancel'));
			}
			return answer;
		});

		vi.mocked(text).mockImplementation(async (config) => {
			MockPrompt.askedQuestions.add(config.message);
			const answer = MockPrompt.questionAnswers.get(config.message);
			if (answer === undefined) {
				throw new Error(`No mock answer configured for text question: "${config.message}"`);
			}
			if (answer === 'CANCEL') {
				return await Promise.resolve(Symbol('cancel'));
			}
			// eslint-disable-next-line @typescript-eslint/no-base-to-string
			return String(answer);
		});

		vi.mocked(confirm).mockImplementation(async (config) => {
			MockPrompt.askedQuestions.add(config.message);
			const answer = MockPrompt.questionAnswers.get(config.message);
			if (answer === undefined) {
				throw new Error(`No mock answer configured for confirm question: "${config.message}"`);
			}
			if (answer === 'CANCEL') {
				return await Promise.resolve(Symbol('cancel'));
			}
			return Boolean(answer);
		});

		vi.mocked(isCancel).mockImplementation((value) => {
			return typeof value === 'symbol' && value.description === 'cancel';
		});
	}
}
