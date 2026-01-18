"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Zoho/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Zoho 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:CamelCaseResource、SnakeCaseResource、GetAllFilterOptions、ZohoOAuth2ApiCredentials、IdType、NameType、LocationType、DateType 等10项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Zoho/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Zoho/types.py

import type { IDataObject } from 'n8n-workflow';

// ----------------------------------------
//          for generic functions
// ----------------------------------------

type Resource =
	| 'account'
	| 'contact'
	| 'deal'
	| 'invoice'
	| 'lead'
	| 'product'
	| 'quote'
	| 'vendor';

export type CamelCaseResource = Resource | 'purchaseOrder' | 'salesOrder';

export type SnakeCaseResource = Resource | 'purchase_order' | 'sales_order';

export type GetAllFilterOptions = {
	fields: string[];
	[otherOptions: string]: unknown;
};

// ----------------------------------------
//               for auth
// ----------------------------------------

export type ZohoOAuth2ApiCredentials = {
	oauthTokenData: {
		api_domain: string;
	};
};

// ----------------------------------------
//         for field adjusters
// ----------------------------------------

export type IdType = 'accountId' | 'contactId' | 'dealId' | 'purchaseOrderId';

export type NameType = 'Account_Name' | 'Full_Name' | 'Deal_Name' | 'Product_Name' | 'Vendor_Name';

export type LocationType =
	| 'Address'
	| 'Billing_Address'
	| 'Mailing_Address'
	| 'Shipping_Address'
	| 'Other_Address';

export type DateType =
	| 'Date_of_Birth'
	| 'Closing_Date'
	| 'Due_Date'
	| 'Invoice_Date'
	| 'PO_Date'
	| 'Valid_Till';

export type AllFields = { [Date in DateType]?: string } & {
	[Location in LocationType]?: { address_fields: { [key: string]: string } };
} & { Account?: { subfields: { id: string; name: string } } } & {
	[key in 'accountId' | 'contactId' | 'dealId']?: string;
} & { customFields?: { customFields: Array<{ fieldId: string; value: string }> } } & {
	Product_Details?: ProductDetails;
} & IDataObject;

export type ProductDetails = Array<{ id: string; quantity: number }>;

export type ResourceItems = Array<{ [key: string]: string }>;

// ----------------------------------------
//         for resource loaders
// ----------------------------------------

export type LoadedAccounts = Array<{
	Account_Name: string;
	id: string;
}>;

export type LoadedContacts = Array<{
	Full_Name: string;
	id: string;
}>;

export type LoadedDeals = Array<{
	Deal_Name: string;
	id: string;
}>;

export type LoadedFields = {
	fields: Array<{
		field_label: string;
		api_name: string;
		custom_field: boolean;
	}>;
};

export type LoadedVendors = Array<{
	Vendor_Name: string;
	id: string;
}>;

export type LoadedProducts = Array<{
	Product_Name: string;
	id: string;
}>;

export type LoadedLayouts = {
	layouts: Array<{
		sections: Array<{
			api_name: string;
			fields: Array<{
				api_name: string;
				pick_list_values: Array<{
					display_value: string;
					actual_value: string;
				}>;
			}>;
		}>;
	}>;
};
