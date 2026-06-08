# Grocery Sync Summary — 2026-06-03

## Task
Sync the Weekly Meal Plan shopping list from the Obsidian wiki to the Apple Reminders "Shopping" list.

## Results

| Metric | Count |
|--------|-------|
| Items extracted from wiki page | 60 |
| Items added to Reminders | 60 |
| Items skipped (duplicates) | 0 |
| Final count of open items on Shopping list | 60 |

## Details

### Source
- **Page**: `Weekly Meal Plan.md`
- **Section**: `## Shopping List`
- **Categories parsed**: Fish & Seafood (4), Meat & Poultry (1), Eggs & Dairy (2), Legumes (2), Grains (5), Vegetables (18), Fruits (8), Nuts & Seeds (11), Oils & Condiments (6), Beverages (3)

### Pre-sync state
- The Shopping list had 48 existing items, all with `isCompleted: true`
- 0 open items — no duplicates to skip
- All previous items were from a prior week's sync

### Actions taken
1. Read the `Weekly Meal Plan.md` wiki page via `obsidian read`
2. Fetched existing Shopping list via `remindctl list Shopping --json` — confirmed 0 open items
3. Extracted 60 individual bullet-point items from the `## Shopping List` section
4. Added all 60 items via `remindctl add "item" --list Shopping` in 6 parallel batches of 10
5. Verified final state via `remindctl list Shopping --plain` — confirmed 60 open items

### Items added
```
Salmon fillets x2 (360g total)
Sea bass fillets x2 (400g total)
Trout fillet x1 (200g)
Cod fillet x1 (200g)
Turkey breast x1 (200g)
Eggs (18 — reduced from 2 dozen with smaller weekday breakfasts)
Full-fat natural yoghurt (400g)
Green/brown/Puy lentils (3 cups dry)
Chickpeas (3 cans)
Pearl barley
Bulgur wheat
Wholewheat bread (sourdough if possible)
Wholewheat brown pasta
Oats
Kale (large bag)
Rocket (large bag)
Spinach / watercress
Mushrooms
Courgette x3
Cauliflower x2
Cucumber x3
Avocado x4
Fennel x2
Leeks x2
Brussels sprouts (250g)
Green beans (250g)
Tomatoes / cherry tomatoes
Green olives (jar)
Garlic
Onions
Carrots
Red peppers
Blackberries (250g)
Raspberries (250g)
Strawberries (250g)
Cherries (250g)
Oranges x2
Apples x1
Passion fruit x2
Lemons x3
Walnuts (70g)
Almonds (50g)
Pistachios (50g)
Hazelnuts (30g)
Pecans (30g)
Macadamia nuts (30g)
Brazil nuts (20g)
Pine nuts (30g)
Almond butter (jar)
Tahini (jar)
Chia seeds
Extra virgin olive oil (primary cooking fat)
Sesame oil
Houmous (tub)
Balsamic vinegar
Vegetable stock
Cumin, turmeric, black pepper, chilli flakes
Black coffee beans/ground
Green tea bags
Herbal tea bags
```

## Issues encountered
None. All 60 items were added successfully with no errors. No duplicates were found since the list was fully cleared (all previous items completed). The `remindctl` CLI responded correctly for all operations.
