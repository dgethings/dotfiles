---
name: grocery-sync
description: Sync grocery shopping lists from Obsidian wiki pages to the Apple Reminders Shopping list using remindctl. Use whenever the user asks to add items to their shopping list, update their shopping list, sync a meal plan to reminders, add groceries, or push a shopping list to Apple Reminders. Also trigger when the user mentions meal planning and wants the ingredients added to their shopping list. Skip for pure questions about meal planning or nutrition that don't involve updating the Reminders list.
---

# Grocery Sync

This skill reads shopping list sections from Obsidian wiki pages and adds the items to the Apple Reminders "Shopping" list using `remindctl`. It deduplicates against items already on the list.

## When this skill triggers

Any request that involves adding grocery/shopping items to Apple Reminders, including:
- "Add my shopping list to Reminders"
- "Sync the weekly meal plan shopping list"
- "Update my shopping list from the meal plan"
- "Add these groceries to my reminders"
- "Push the shopping list from [page name]"

## Workflow

### 1. Read the source page(s)

Use `obsidian read path="Page Name.md"` to read the wiki page(s) containing the shopping list. The user may specify one or more pages, or ask you to figure out which page to use.

Common source pages:
- `Weekly Meal Plan` — the main weekly meal plan with a comprehensive shopping list
- `Weekend Meal Plan` — a weekend-only plan with a shorter list

Look for a `## Shopping List` section. Items are grouped by category headings with bullet points.

### 2. Extract individual items

Parse the shopping list into individual items. Each bullet point is one item. Items may include:
- Quantities (e.g., "x2", "(200g)", "(1 punnet ~150g)")
- Descriptors (e.g., "fresh or frozen", "sourdough if possible")

Keep each item as a single line suitable for a reminder title. Combine the item name with its quantity/notes into one clean string.

Example extraction from:
```
- Salmon fillets x2 (360g total)
- Sea bass fillets x2 (400g total)
```

Produces:
```
Salmon fillets x2 (360g total)
Sea bass fillets x2 (400g total)
```

### 3. Check existing Shopping list for duplicates

Before adding items, fetch what is already on the Shopping list:

```bash
remindctl list Shopping --json
```

Parse the JSON output. Filter to items where `isCompleted` is `false` — these are the current open items. Compare the titles of open items against the items to be added.

Skip any item that already exists (case-insensitive match on the core item name, ignoring emoji prefixes). Report skipped items to the user.

### 4. Add items to Shopping list

For each new item, add it using:

```bash
remindctl add "item text" --list Shopping
```

Add items one at a time. If an item contains double quotes, use the `--title` flag instead:

```bash
remindctl add --title 'item with "quotes"' --list Shopping
```

### 5. Summarise

After processing all items, report:
- How many items were added
- How many were skipped (already on the list)
- How many total items are now on the Shopping list (run `remindctl list Shopping --plain` and count incomplete)

## Important notes

- The existing Shopping list uses emoji prefixes in item titles (e.g., "🐟 Salmon fillets x2"). You do NOT need to add emoji prefixes when adding new items unless the source page already includes them. Match the source page's formatting.
- Always check for duplicates before adding. Users find duplicate reminder items annoying.
- If the user asks to "refresh" or "replace" the shopping list, first confirm: do they want to clear the existing items first? If yes, complete the incomplete items using `remindctl complete <id>` before adding the new ones.
- The `--list` flag is `Shopping` (capital S) — this matches the existing Apple Reminders list name.
- If `remindctl` returns a permission error, suggest the user run `remindctl authorize` or `remindctl doctor`.
