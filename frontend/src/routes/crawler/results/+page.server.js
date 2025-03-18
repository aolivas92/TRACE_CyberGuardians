export async function load() {
  const response = await fetch("http://localhost:3000/api/crawler/results"); 
  const results = await response.json();
  
  return { results };
}
