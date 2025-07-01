# 🥗 Recipe App — Frontend

This is the **React + Vite** frontend for the **Recipe App** project.  
It communicates with a FastAPI backend to allow users to:

- View a list of recipes
- Create a new recipe (selecting author and ingredients)
- See form validation feedback

> **Note**  
> The API base URL is currently **hard-coded** to `http://localhost:8000`  
> in `src/api/recipeApi.js`. Environment-based configuration using `.env`  
> has not been implemented yet.

---

## 🚀 Features

| Area             | Details                                                                 |
| ---------------- | ------------------------------------------------------------------------ |
| **Tech stack**   | React 18, Vite 5, Axios, plain CSS                                       |
| **State**        | React hooks (`useState`, `useEffect`)                                    |
| **API calls**    | Centralized in `src/api/recipeApi.js`                                    |
| **Styling**      | Custom CSS — no external UI library                                      |
| **Responsiveness** | Basic mobile tweaks via simple media queries                           |

---

## 🌐 Backend Expectations

This frontend assumes the FastAPI backend is already running (via Docker Compose or separately) at:

```
src/
 ├─ api/
 │   └─ recipeApi.js         # Axios wrappers for API calls
 ├─ components/
 │   ├─ RecipeList/
 │   │   └─ RecipeList.jsx   # Recipe list component
 │   └─ RecipeForm/
 │       ├─ RecipeForm.jsx   # Form to create recipes
 │       └─ IngredientField.jsx # Single ingredient input row
 ├─ App.jsx                  # Main layout / routing
 ├─ main.jsx                 # React entry point
 └─ index.css                # Global + component styling
```

---

## 🛠️ Future Improvements

- Use `.env` for configurable API base URL
- Add support for editing & deleting recipes
- Display recipe images or categories
- Improve validation UX (e.g. using Yup or Zod)
- Add pagination or filtering to recipe list

---

## 📝 License

MIT