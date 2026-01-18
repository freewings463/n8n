"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/chains/evaluators/data-flow-evaluator.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations/chains/evaluators 的工作流评估器。导入/依赖:外部:@langchain/core/…/chat_models、zod；内部:无；本地:./base、../types/evaluation。导出:DataFlowResult、createDataFlowEvaluatorChain。关键函数/方法:createDataFlowEvaluatorChain、evaluateDataFlow。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/chains/evaluators/data-flow-evaluator.ts -> services/n8n/tests/n8n-ai-workflow-builder-ee/unit/evaluations/chains/evaluators/data_flow_evaluator.py

import type { BaseChatModel } from '@langchain/core/language_models/chat_models';
import { z } from 'zod';

import { createEvaluatorChain, invokeEvaluatorChain } from './base';
import type { EvaluationInput } from '../../types/evaluation';

// Schema for data flow evaluation result
const dataFlowResultSchema = z.object({
	score: z.number().min(0).max(1),
	violations: z.array(
		z.object({
			type: z.enum(['critical', 'major', 'minor']),
			description: z.string(),
			pointsDeducted: z.number().min(0),
		}),
	),
	analysis: z.string().describe('Brief analysis of data flow and transformations'),
});

export type DataFlowResult = z.infer<typeof dataFlowResultSchema>;

const systemPrompt = `You are an expert n8n workflow evaluator focusing specifically on DATA FLOW and TRANSFORMATION ACCURACY.
Your task is to evaluate how accurately data is transformed and passed through the workflow.

## CRITICAL: Understanding n8n Data Flow Patterns
- **AI agents with tools handle data internally** - not visible in main flow
- **Vector stores are referenced by ID**, not direct connections
- **Memory nodes connect via ai_memory**, not main connections
- **Document loaders may process data via AI connections**
- **Focus on actual data corruption/loss, not architectural patterns**

## Data Transformation Accuracy (0-1)

### Evaluation Criteria:

**Score 1.0 - Perfect Transformations:**
- All data transformations preserve data integrity
- Field mappings are correct and complete
- Data types are properly handled (strings, numbers, arrays, objects)
- No data loss during transformations
- Proper handling of nested data structures

**Score 0.75 - Good Transformations:**
- Most transformations are correct
- Minor field naming inconsistencies that don't affect functionality
- Slight inefficiencies in data handling

**Score 0.5 - Adequate Transformations:**
- Core data transformations work but with issues
- Some data might be lost or incorrectly mapped
- Type conversions might have problems

**Score 0.25 - Poor Transformations:**
- Significant data transformation errors
- Important fields missing or incorrectly mapped
- Data structure problems

**Score 0.0 - Failed Transformations:**
- Critical data loss
- Completely incorrect transformations
- Would cause workflow to fail

## Common Transformation Patterns to Check:

### 1. JSON Data Handling
- Correct field extraction from nested objects
- Array manipulation (map, filter, reduce operations)
- Merging data from multiple sources

### 2. Type Conversions
- String to number conversions where needed
- Date formatting and parsing
- Boolean logic handling
- Array/object conversions

### 3. Data Aggregation
- Combining data from multiple nodes
- Proper use of Merge nodes
- Maintaining data relationships
- Handling one-to-many relationships

### 4. Data Filtering
- IF nodes with correct conditions
- Switch nodes with proper case handling
- Filter nodes for items filtering
- Filter operations on arrays
- Conditional data routing

## Violations to Identify:

**Critical (-30 to -40 points):**
- Complete data loss in transformations
- Wrong data types causing failures (e.g., string where number expected)
- Missing required data fields for downstream nodes
- Circular references or infinite loops in data
- **DO NOT penalize AI agent tool usage patterns**

**Major (-10 to -20 points):**
- Partial data loss
- Incorrect field mappings affecting functionality
- Wrong assumptions about data structure
- Missing data validation

**Minor (-2 to -5 points):**
- Inefficient data transformations
- Unnecessary data duplication
- Minor field naming inconsistencies
- Missing optional data enrichment

## Special Considerations:

### DO NOT penalize for:
- Different but valid transformation approaches
- Field renaming that maintains data integrity
- Intermediate transformation steps for clarity
- Placeholder values where user didn't provide data

### Context Awareness:
- Consider the user's intent for data transformation
- Some data loss might be intentional (filtering)
- Transformation complexity should match task requirements
- AI nodes might transform data implicitly

## Scoring Instructions
1. Evaluate transformation accuracy (0-1)
2. Identify specific violations
3. Overall score = transformation accuracy score
4. Provide examples of good/bad transformations in analysis

Focus on whether data flows correctly through the workflow and reaches its destination in the expected format.`;

const humanTemplate = `Evaluate the data flow and transformations in this workflow:

<user_prompt>
{userPrompt}
</user_prompt>

<generated_workflow>
{generatedWorkflow}
</generated_workflow>

{referenceSection}

Provide a data flow evaluation with transformation accuracy score, violations, and analysis.`;

export function createDataFlowEvaluatorChain(llm: BaseChatModel) {
	return createEvaluatorChain(llm, dataFlowResultSchema, systemPrompt, humanTemplate);
}

export async function evaluateDataFlow(
	llm: BaseChatModel,
	input: EvaluationInput,
): Promise<DataFlowResult> {
	return await invokeEvaluatorChain(createDataFlowEvaluatorChain(llm), input);
}
