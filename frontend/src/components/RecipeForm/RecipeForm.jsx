import { useState, useEffect } from "react";
import { getIngredients, getAuthors, createRecipe } from "../../api/recipeApi";
import IngredientField from "./IngredientField";

function RecipeForm({ onRecipeCreated }) {
  // ───────────── form state ─────────────
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [authorId, setAuthorId] = useState("");
  const [ingredients, setIngredients] = useState([
    { ingredient_id: "", quantity: "", unit: "" },
  ]);
  const [ingredientsOptions, setIngredientsOptions] = useState([]);
  const [authorsOptions, setAuthorsOptions] = useState([]);
  const [errorMessages, setErrorMessages] = useState([]);

  // ───────── fetch authors + ingredients ─────────
  useEffect(() => {
    async function fetchData() {
      try {
        const [ingRes, authRes] = await Promise.all([
          getIngredients(),
          getAuthors(),
        ]);
        setIngredientsOptions(ingRes.data);
        setAuthorsOptions(authRes.data);
      } catch (err) {
        console.error("Error fetching data:", err);
      }
    }
    fetchData();
  }, []);

  // ───────── helpers for ingredient list ─────────
  const handleIngredientChange = (index, field, value) => {
    const updated = [...ingredients];
    updated[index][field] = value;
    setIngredients(updated);
  };

  const addIngredient = () => {
    setIngredients([
      ...ingredients,
      { ingredient_id: "", quantity: "", unit: "" },
    ]);
  };

  const removeIngredient = (index) => {
    setIngredients(ingredients.filter((_, i) => i !== index));
  };

  // ───────── submit form ─────────
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessages([]);

    const payload = {
      title,
      description,
      author_id: parseInt(authorId),
      ingredients: ingredients.map((ing) => ({
        ingredient_id: parseInt(ing.ingredient_id),
        quantity: parseFloat(ing.quantity),
        unit: ing.unit,
      })),
    };

    try {
      await createRecipe(payload);

      // Reset form
      setTitle("");
      setDescription("");
      setAuthorId("");
      setIngredients([{ ingredient_id: "", quantity: "", unit: "" }]);
      alert("Recipe created successfully!");
      onRecipeCreated?.();
    } catch (err) {
      console.error("Error creating recipe:", err);

      if (err.response?.status === 422) {
        const details = err.response.data?.detail ?? [];
        const msgs = details.map((d) => `${d.loc.join(".")} → ${d.msg}`);
        setErrorMessages(msgs);
      } else {
        setErrorMessages(["Unexpected error occurred."]);
      }
    }
  };

  // ───────── render ─────────
  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h2>Create Recipe</h2>

      <input
        className="form-input"
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />

      <textarea
        className="form-input"
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
      />

      {/* Author dropdown */}
      <select
        className="form-input"
        value={authorId}
        onChange={(e) => setAuthorId(e.target.value)}
        required
      >
        <option value="">-- choose author --</option>
        {authorsOptions.map((author) => (
          <option key={author.id} value={author.id}>
            {author.name}
          </option>
        ))}
      </select>

      <h4>Ingredients</h4>
      {ingredients.map((ing, index) => (
        <IngredientField
          key={index}
          index={index}
          ingredient={ing}
          options={ingredientsOptions}
          onChange={handleIngredientChange}
          onRemove={removeIngredient}
          removable={index > 0}
        />
      ))}

      <button
        type="button"
        onClick={addIngredient}
        className="btn-secondary"
        style={{ marginBottom: "10px" }}
      >
        Add Ingredient
      </button>

      <div className="form-submit">
        <button type="submit" className="btn-primary large">
          Create Recipe
        </button>
      </div>

      {errorMessages.length > 0 && (
        <div style={{ color: "red", marginTop: "1rem" }}>
          <h4>Validation Errors:</h4>
          <ul>
            {errorMessages.map((msg, i) => (
              <li key={i}>{msg}</li>
            ))}
          </ul>
        </div>
      )}
    </form>
  );
}

export default RecipeForm;
