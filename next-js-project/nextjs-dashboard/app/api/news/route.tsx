import { database as db } from "@/app/database";
import { NextRequest } from "next/server";

export const dynamic = "force-dynamic";

// GET /api/news
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const limit = Number(searchParams.get("limit")) || 5;
  const offset = Number(searchParams.get("offset")) || 0;

  const data = db.prepare("SELECT * FROM news ORDER BY created_at DESC LIMIT ? OFFSET ?").all(limit, offset);
  const total = db.prepare("SELECT COUNT(*) as count FROM news").get().count;

  return Response.json({ news: data, total });
}

// POST /api/news
export async function POST(request: NextRequest) {
  const body = await request.json();
  const { title, content } = body;

  if (!title || !content) {
    return new Response("Champs manquants", { status: 400 }); //syntaxe invalide 
  }

  const createNews = db.prepare("INSERT INTO news (title, content) VALUES (?, ?)");
  const result = createNews.run(title, content);

  const news= db.prepare("SELECT * FROM news WHERE id = ?");
  const newNews= news.get(result.lastInsertRowid); // l'id creer pour le tuple

  return Response.json(newNews, { status: 201 }); // creation de l'objet
}
