function RecipeList({ recipes }) {
  return (
    <div className="recipe-list-container">
      <h2>Recipes</h2>
      <ul className="recipe-list">
        {recipes.map((recipe) => (
          <li key={recipe.id} className="card">
            <strong>{recipe.title}</strong>: {recipe.description}
            <br />

            {recipe.author && (
              <p>
                <em>Author:</em> {recipe.author.name}
              </p>
            )}

            <p><em>Ingredients:</em></p>
            <ul className="recipe-ingredients">
              {recipe.ingredients.map((ing, idx) => (
                <li key={idx}>
                  {ing.quantity} {ing.unit} of {ing.ingredient_name}
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RecipeList;
