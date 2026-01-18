"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DebugHelper/randomData.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DebugHelper 的节点。导入/依赖:外部:minifaker/…/en；内部:无；本地:无。导出:generateRandomUser、generateRandomAddress、generateRandomEmail、generateUUID、generateNanoid、generateCreditCard、generateURL、generateIPv4 等4项。关键函数/方法:generateRandomUser、generateRandomAddress、generateRandomEmail、generateUUID、generateNanoid、generateCreditCard、generateURL、generateIPv4 等4项。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DebugHelper/randomData.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DebugHelper/randomData.py

import {
	firstName,
	lastName,
	streetAddress,
	cityName,
	zipCode,
	state,
	country,
	password,
	creditCardNumber,
	creditCardCVV,
	email,
	boolean,
	uuid,
	nanoId,
	domainUrl,
	semver,
	latLong,
	macAddress,
	ip,
	ipv6,
	number,
} from 'minifaker';
import 'minifaker/locales/en';

export function generateRandomUser() {
	return {
		uid: uuid.v4(),
		email: email(),
		firstname: firstName(),
		lastname: lastName(),
		password: password(),
	};
}

export function generateRandomAddress() {
	return {
		firstname: firstName(),
		lastname: lastName(),
		street: streetAddress(),
		city: cityName(),
		zip: zipCode({ format: '#####' }),
		state: state(),
		country: country(),
	};
}

export function generateRandomEmail() {
	return {
		email: email(),
		confirmed: boolean(),
	};
}

export function generateUUID() {
	return { uuid: uuid.v4() };
}

export function generateNanoid(customAlphabet: string, length: string) {
	return { nanoId: nanoId.customAlphabet(customAlphabet, parseInt(length, 10))().toString() };
}

export function generateCreditCard() {
	return {
		type: boolean() ? 'MasterCard' : 'Visa',
		number: creditCardNumber(),
		ccv: creditCardCVV(),
		exp: `${number({ min: 1, max: 12, float: false }).toString().padStart(2, '0')}/${number({
			min: 1,
			max: 40,
			float: false,
		})
			.toString()
			.padStart(2, '0')}`,
		holder_name: `${firstName()} ${lastName()}`,
	};
}

export function generateURL() {
	return { url: domainUrl() };
}

export function generateIPv4() {
	return { ip: ip() };
}

export function generateIPv6() {
	return { ipv6: ipv6() };
}

export function generateMAC() {
	return { mac: macAddress() };
}

export function generateLocation() {
	return { location: latLong() };
}

export function generateVersion() {
	return { version: semver() };
}
