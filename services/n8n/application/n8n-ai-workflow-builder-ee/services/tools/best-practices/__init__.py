"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/best-practices/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools/best-practices 的工作流入口。导入/依赖:外部:无；内部:@/types、@/types/categorization；本地:./chatbot、./content-generation、./data-extraction、./data-persistence 等6项。导出:documentation。关键函数/方法:无。用于汇总导出并完成工作流模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/best-practices/index.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/tools/best-practices/__init__.py

import type { BestPracticesDocument } from '@/types';
import { WorkflowTechnique, type WorkflowTechniqueType } from '@/types/categorization';

import { ChatbotBestPractices } from './chatbot';
import { ContentGenerationBestPractices } from './content-generation';
// import { DataAnalysisBestPractices } from './data-analysis';
import { DataExtractionBestPractices } from './data-extraction';
import { DataPersistenceBestPractices } from './data-persistence';
import { DataTransformationBestPractices } from './data-transformation';
import { DocumentProcessingBestPractices } from './document-processing';
// import { EnrichmentBestPractices } from './enrichment';
import { FormInputBestPractices } from './form-input';
// import { HumanInTheLoopBestPractices } from './human-in-the-loop';
// import { KnowledgeBaseBestPractices } from './knowledge-base';
// import { MonitoringBestPractices } from './monitoring';
import { NotificationBestPractices } from './notification';
import { ScrapingAndResearchBestPractices } from './scraping-and-research';
// import { SchedulingBestPractices } from './scheduling';
import { TriageBestPractices } from './triage';

export const documentation: Record<WorkflowTechniqueType, BestPracticesDocument | undefined> = {
	[WorkflowTechnique.SCRAPING_AND_RESEARCH]: new ScrapingAndResearchBestPractices(),
	[WorkflowTechnique.CHATBOT]: new ChatbotBestPractices(),
	[WorkflowTechnique.CONTENT_GENERATION]: new ContentGenerationBestPractices(),
	[WorkflowTechnique.DATA_ANALYSIS]: undefined, // new DataAnalysisBestPractices(),
	[WorkflowTechnique.DATA_EXTRACTION]: new DataExtractionBestPractices(),
	[WorkflowTechnique.DATA_PERSISTENCE]: new DataPersistenceBestPractices(),
	[WorkflowTechnique.DATA_TRANSFORMATION]: new DataTransformationBestPractices(),
	[WorkflowTechnique.DOCUMENT_PROCESSING]: new DocumentProcessingBestPractices(),
	[WorkflowTechnique.ENRICHMENT]: undefined, // new EnrichmentBestPractices(),
	[WorkflowTechnique.FORM_INPUT]: new FormInputBestPractices(),
	[WorkflowTechnique.KNOWLEDGE_BASE]: undefined, // new KnowledgeBaseBestPractices(),
	[WorkflowTechnique.NOTIFICATION]: new NotificationBestPractices(),
	[WorkflowTechnique.TRIAGE]: new TriageBestPractices(),
	[WorkflowTechnique.HUMAN_IN_THE_LOOP]: undefined, // new HumanInTheLoopBestPractices(),
	[WorkflowTechnique.MONITORING]: undefined, // new MonitoringBestPractices(),
	[WorkflowTechnique.SCHEDULING]: undefined, // new SchedulingBestPractices(),
};
