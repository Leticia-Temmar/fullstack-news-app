//le BackEnd (côté serveur)

import { database as db } from "@/app/database";
import { NextRequest } from "next/server";

export const dynamic = "force-dynamic";

// DELETE /api/news/:id
export async function DELETE(request: NextRequest, context: { params: { id: string } }) {
  const id = context.params.id;
  const deleteNews = db.prepare("DELETE FROM news WHERE id = ?");
  deleteNews.run(id);
  return Response.json({}, { status: 200 });
}

// PUT /api/news/:id
export async function PUT(request: NextRequest, context: { params: { id: string } }) {
  const newsId = context.params.id;
  const body = await request.json();
  const { title, content } = body;

  if (!title || !content) {
    return new Response("Champs manquants", { status: 400 });
  }

  const updateNews = db.prepare("UPDATE news SET title = ?, content = ? WHERE id = ?");
  updateNews.run(title, content, newsId);

  const news = db.prepare("SELECT * FROM news WHERE id = ?");
  const updated = news.get(newsId);
  return Response.json(updated, { status: 200 });
}

// GET /api/news/:id {pour tester le cas de conflit}
export async function GET(_: NextRequest, { params }: { params: { id: string } }) {
  const id = params.id;
  const statement = db.prepare("SELECT * FROM news WHERE id = ?");
  const result = statement.get(id);

  if (!result) {
    return new Response("Actualité introuvable", { status: 404 });
  }

  return Response.json(result);
}