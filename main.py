import yaml

def define_env(env):
    with open("data/ingredients.yml", "r") as f:
        db = yaml.safe_load(f)

    @env.macro
    def render_ingredients():
        ingredients = env.page.meta.get("ingredients", [])
        lines = []
        for entry in ingredients:
            item_key = entry["item"]
            item = db.get(item_key, {})
            name = item.get("name", item_key)
            amount = entry.get("display", f"{entry['grams']}g")
            note = f" ({entry['note']})" if entry.get("note") else ""
            lines.append(f"- **{amount}** {name}{note}")
        return "\n".join(lines)

    @env.macro
    def render_nutrition():
        meta = env.page.meta
        ingredients = meta.get("ingredients", [])
        servings = meta.get("servings", 1)
        totals = {"kcal": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}

        for entry in ingredients:
            item = db.get(entry["item"])
            if not item:
                continue
            factor = entry["grams"] / 100.0
            for key in totals:
                totals[key] += item[key] * factor

        return f"""
| Nutrition | Whole Batch | Per Serving ({servings}) |
| :--- | :--- | :--- |
| **Calories** | {totals['kcal']:.0f} kcal | {totals['kcal']/servings:.0f} kcal |
| **Protein** | {totals['protein']:.1f}g | **{totals['protein']/servings:.1f}g** |
| **Carbs** | {totals['carbs']:.1f}g | {totals['carbs']/servings:.1f}g |
| **Fat** | {totals['fat']:.1f}g | {totals['fat']/servings:.1f}g |
"""