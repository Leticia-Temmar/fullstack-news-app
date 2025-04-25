// fetchers/fetchAddNews.ts

interface AddNewsInput {
    title: string;
    content: string;
    categorie_id: number; 
  }
  

  const fetchAddNews = async ({ title, content, categorie_id }: AddNewsInput) => {
    const token = localStorage.getItem("token");
    const response = await fetch("http://localhost:8000/news", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({ title, content, categorie_id }), 
    });
  
    if (!response.ok) {
      throw new Error("Erreur lors de l’ajout de l’actualité.");
    }
  
    const result = await response.json();
    return result;
  };
  
  export default fetchAddNews;
  