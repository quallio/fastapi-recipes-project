function IngredientField({
  index,
  ingredient,
  options,
  onChange,
  onRemove,
  removable,
}) {
  return (
    <div className="ingredient-row">
      <select
        className="ingredient-select"
        value={ingredient.ingredient_id}
        onChange={(e) =>
          onChange(index, "ingredient_id", e.target.value)
        }
        required
      >
        <option value="">-- choose ingredient --</option>
        {options.map((opt) => (
          <option key={opt.id} value={opt.id}>
            {opt.name}
          </option>
        ))}
      </select>

      <input
        className="ingredient-quantity"
        type="number"
        placeholder="Quantity"
        value={ingredient.quantity}
        onChange={(e) =>
          onChange(index, "quantity", e.target.value)
        }
        required
      />

      <input
        className="ingredient-unit"
        type="text"
        placeholder="Unit"
        value={ingredient.unit}
        onChange={(e) => onChange(index, "unit", e.target.value)}
        required
      />

      {removable && (
        <button
          type="button"
          onClick={() => onRemove(index)}
          className="btn-secondary"
        >
          ✕
        </button>
      )}
    </div>
  );
}

export default IngredientField;
