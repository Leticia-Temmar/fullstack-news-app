import {database as db} from "../database";
export const dynamic = 'force-static';
 
export async function GET() {
    let statement = db.prepare("SELECT * FROM user");
    let res = statement.all();
 
    return Response.json(res);
}

export async function POST(request: Request) {
    let body = await request.json();
    console.log(body);
    let statement = db.prepare("INSERT INTO user(name, password) VALUES (?, ?)");
    statement.run(body.name, body.password);
    return Response.json({});
}

export async function PATCH(request: Request) {

}

export async function DELETE() {

}