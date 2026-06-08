# Grocery Sync Summary — Weekend Meal Plan

## Results

| Metric | Count |
|--------|-------|
| Items extracted from wiki page | 29 |
| Items checked for duplicates | 29 |
| Items skipped (already on list) | 27 |
| Items actually added | 2 |
| Final open items on Shopping list | 62 |

## Items Added

1. **Chicken breast** — no existing match found
2. **Green lentils** — no existing match found (existing "Green/brown/Puy lentils" has a different core name)

## Items Skipped (27 duplicates)

All 27 remaining items from the Weekend Meal Plan already existed on the Shopping list (matched by core item name, case-insensitive, ignoring emoji prefixes and quantities):

- Salmon fillets (matched "Salmon fillets x2 (360g total)")
- Sea bass fillets (matched "Sea bass fillets x2 (400g total)")
- Turkey breast (matched "Turkey breast x1 (200g)")
- Eggs (matched "Eggs (18 — reduced from 2 dozen with smaller weekday breakfasts)")
- Chickpeas (canned) (matched "Chickpeas (3 cans)")
- Pearl barley (matched "Pearl barley")
- Bulgur wheat (matched "Bulgur wheat")
- Kale (matched "Kale (large bag)")
- Green beans (matched "Green beans (250g)")
- Rocket (matched "Rocket (large bag)")
- Cucumber (matched "Cucumber x3")
- Tomatoes (matched "Tomatoes / cherry tomatoes")
- Avocado (matched "Avocado x4")
- Fennel (matched "Fennel x2")
- Red peppers (matched "Red peppers")
- Mushrooms (matched "Mushrooms")
- Onions (matched "Onions")
- Courgette (matched "Courgette x3")
- Blackberries (matched "Blackberries (250g)")
- Apple (matched "Apples x1")
- Lemons (matched "Lemons x3")
- Almonds (matched "Almonds (50g)")
- Pistachios (matched "Pistachios (50g)")
- Walnuts (matched "Walnuts (70g)")
- Extra virgin olive oil (matched "Extra virgin olive oil (primary cooking fat)")
- Sesame oil (matched "Sesame oil")
- Full-fat natural yoghurt (matched "Full-fat natural yoghurt (400g)")

## Issues Encountered

- **Green lentils vs Green/brown/Puy lentils**: The existing list has "Green/brown/Puy lentils (3 cups dry)" which is a broader item that includes green lentils. Since the core names don't match exactly ("green lentils" vs "green/brown/puy lentils"), "Green lentils" was added as a separate item. This could be considered a near-duplicate — the user may already have green lentils covered by the existing entry. A fuzzy-matching approach could have caught this.
- No other issues encountered. All `remindctl` commands succeeded without errors.
