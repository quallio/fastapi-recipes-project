import axios from "axios";

const API_URL = "http://localhost:8000";

export const getRecipes = () => axios.get(`${API_URL}/recipes`);
export const getIngredients = () => axios.get(`${API_URL}/ingredients`);
export const getAuthors = () => axios.get(`${API_URL}/authors`);
export const createRecipe = (data) =>
  axios.post(`${API_URL}/recipes`, data, {
    headers: { "Content-Type": "application/json" },
  });
