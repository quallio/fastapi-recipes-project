import { useState, useEffect } from "react";
import { Routes, Route, NavLink, useNavigate } from "react-router-dom";
import { getRecipes } from "./api/recipeApi";
import RecipeList from "./components/RecipeList/RecipeList";
import RecipeForm from "./components/RecipeForm/RecipeForm";

function App() {
  // Shared state for all recipes
  const [recipes, setRecipes] = useState([]);
  const navigate = useNavigate();

  // Fetch all recipes from backend
  const fetchRecipes = async () => {
    try {
      const res = await getRecipes();
      setRecipes(res.data);
    } catch (err) {
      console.error("Error fetching recipes:", err);
    }
  };

  // Initial fetch
  useEffect(() => {
    fetchRecipes();
  }, []);

  // Callback fired after a successful create
  const handleRecipeCreated = () => {
    fetchRecipes();
    navigate("/recipes");
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Recipe App</h1>

      {/* Simple nav bar */}
      <nav style={{ marginBottom: "1rem" }}>
        <NavLink to="/recipes" style={{ marginRight: "1rem" }}>
          Recipe List
        </NavLink>
        <NavLink to="/create">Create Recipe</NavLink>
      </nav>

      <hr />

      {/* Routes */}
      <Routes>
        <Route path="/recipes" element={<RecipeList recipes={recipes} />} />
        <Route
          path="/create"
          element={<RecipeForm onRecipeCreated={handleRecipeCreated} />}
        />
        {/* Fallback */}
        <Route path="*" element={<RecipeList recipes={recipes} />} />
      </Routes>
    </div>
  );
}

export default App;
