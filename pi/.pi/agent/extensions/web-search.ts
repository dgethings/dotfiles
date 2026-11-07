/**
 * Web Search Extension (keyless)
 *
 * Registers two tools:
 *   - web_search: DuckDuckGo web search (HTML/lite endpoints, no API key)
 *   - fetch_url:  fetch a URL and return readable plain text
 *
 * No npm dependencies; uses Node's global fetch.
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

const UA =
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36";

interface SearchResult {
	title: string;
	url: string;
	snippet: string;
}

/** DuckDuckGo wraps outbound links as /l/?uddg=<urlencoded>; unwrap them. */
function unwrapDdgUrl(href: string): string {
	let url = href;
	if (url.startsWith("//")) url = "https:" + url;
	try {
		const u = new URL(url, "https://duckduckgo.com");
		if (u.hostname.endsWith("duckduckgo.com") && u.pathname === "/l/") {
			const uddg = u.searchParams.get("uddg");
			if (uddg) return uddg;
		}
	} catch {
		/* fall through */
	}
	return url;
}

function decodeEntities(s: string): string {
	return s
		.replace(/&amp;/g, "&")
		.replace(/&lt;/g, "<")
		.replace(/&gt;/g, ">")
		.replace(/&quot;/g, '"')
		.replace(/&#39;|&apos;/g, "'")
		.replace(/&nbsp;/g, " ")
		.replace(/&#x27;/gi, "'")
		.replace(/&#x2F;/gi, "/")
		.replace(/&#(\d+);/g, (_m, d) => String.fromCharCode(Number(d)));
}

function stripTags(html: string): string {
	return decodeEntities(
		html
			.replace(/<script[\s\S]*?<\/script>/gi, " ")
			.replace(/<style[\s\S]*?<\/style>/gi, " ")
			.replace(/<[^>]+>/g, " "),
	)
		.replace(/[ \t]+/g, " ")
		.replace(/\s*\n\s*/g, "\n")
		.trim();
}

/** Parse the simple lite.duckduckgo.com result table. */
function parseLite(html: string): SearchResult[] {
	const results: SearchResult[] = [];
	// Rows: <a rel="nofollow" href="URL" class='result-link'>Title</a>
	const linkRe = /<a[^>]*href="([^"]+)"[^>]*class=['"]result-link['"][^>]*>([\s\S]*?)<\/a>/gi;
	// Snippet appears in a following <td class='result-snippet'>...</td>
	const snippetRe = /class=['"]result-snippet['"][^>]*>([\s\S]*?)<\/td>/i;
	let m: RegExpExecArray | null;
	while ((m = linkRe.exec(html)) !== null) {
		const title = stripTags(m[2]);
		const url = unwrapDdgUrl(decodeEntities(m[1]));
		if (!title || !/^https?:\/\//.test(url)) continue;
		const after = html.slice(linkRe.lastIndex, linkRe.lastIndex + 4000);
		const sm = after.match(snippetRe);
		results.push({ title, url, snippet: sm ? stripTags(sm[1]) : "" });
	}
	return results;
}

/** Parse the html.duckduckgo.com results page. */
function parseHtml(html: string): SearchResult[] {
	const results: SearchResult[] = [];
	const blockRe = /<a[^>]*class="[^"]*result__a[^"]*"[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>([\s\S]*?)(?=<a[^>]*class="[^"]*result__a|<\/div>\s*<\/div>\s*<\/div>|$)/gi;
	let m: RegExpExecArray | null;
	while ((m = blockRe.exec(html)) !== null) {
		const title = stripTags(m[2]);
		const url = unwrapDdgUrl(decodeEntities(m[1]));
		if (!title || !/^https?:\/\//.test(url)) continue;
		const sn = m[3].match(/class="[^"]*result__snippet[^"]*"[^>]*>([\s\S]*?)<\/a>/i);
		results.push({ title, url, snippet: sn ? stripTags(sn[1]) : "" });
	}
	return results;
}

async function duckDuckGo(query: string, max: number, signal?: AbortSignal): Promise<SearchResult[]> {
	// 1) lite endpoint (simplest, most stable layout)
	let res = await fetch("https://lite.duckduckgo.com/lite/", {
		method: "POST",
		headers: { "Content-Type": "application/x-www-form-urlencoded", "User-Agent": UA },
		body: new URLSearchParams({ q: query }).toString(),
		signal,
	});
	if (res.ok) {
		const results = parseLite(await res.text());
		if (results.length > 0) return results.slice(0, max);
	}

	// 2) html endpoint fallback
	res = await fetch("https://html.duckduckgo.com/html/?q=" + encodeURIComponent(query), {
		headers: { "User-Agent": UA },
		signal,
	});
	if (res.ok) {
		return parseHtml(await res.text()).slice(0, max);
	}

	throw new Error(`DuckDuckGo returned HTTP ${res.status}`);
}

export default function webSearchExtension(pi: ExtensionAPI) {
	pi.registerTool({
		name: "web_search",
		label: "Web Search",
		description:
			"Search the web with DuckDuckGo. Returns a list of results with title, URL, and snippet. Use fetch_url to read the full content of a promising result.",
		parameters: Type.Object({
			query: Type.String({ description: "Search query" }),
			max_results: Type.Optional(
				Type.Number({ description: "Maximum results to return (default 5)", minimum: 1, maximum: 10 }),
			),
		}),
		async execute(_toolCallId, params, signal) {
			try {
				const results = await duckDuckGo(params.query, params.max_results ?? 5, signal);
				if (results.length === 0) {
					return {
						content: [{ type: "text", text: `No results for: ${params.query}` }],
						details: { query: params.query, count: 0 },
					};
				}
				const text = results
					.map((r, i) => `${i + 1}. ${r.title}\n   ${r.url}${r.snippet ? `\n   ${r.snippet}` : ""}`)
					.join("\n\n");
				return {
					content: [{ type: "text", text }],
					details: { query: params.query, results },
				};
			} catch (err) {
				const msg = err instanceof Error ? err.message : String(err);
				return {
					content: [{ type: "text", text: `Web search failed: ${msg}` }],
					isError: true,
				};
			}
		},
	});

	pi.registerTool({
		name: "fetch_url",
		label: "Fetch URL",
		description:
			"Fetch a web page and return its readable plain text (scripts/styles/tags stripped). Useful for reading a page found via web_search.",
		parameters: Type.Object({
			url: Type.String({ description: "Absolute http(s) URL to fetch" }),
			max_chars: Type.Optional(
				Type.Number({
					description: "Maximum characters of text to return (default 10000)",
					minimum: 500,
					maximum: 100000,
				}),
			),
		}),
		async execute(_toolCallId, params, signal) {
			try {
				const res = await fetch(params.url, {
					headers: { "User-Agent": UA, Accept: "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.8" },
					redirect: "follow",
					signal,
				});
				if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
				const contentType = res.headers.get("content-type") ?? "";
				const body = await res.text();
				const limit = params.max_chars ?? 10000;
				const text = (contentType.includes("html") ? stripTags(body) : body).slice(0, limit);
				return {
					content: [{ type: "text", text: `${params.url}\n\n${text}` }],
					details: { url: params.url, status: res.status, truncated: body.length > limit },
				};
			} catch (err) {
				const msg = err instanceof Error ? err.message : String(err);
				return {
					content: [{ type: "text", text: `Fetch failed: ${msg}` }],
					isError: true,
				};
			}
		},
	});
}
