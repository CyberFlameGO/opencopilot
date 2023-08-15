export const runtime = 'edge'

export async function POST(req: Request) {

  const feedback = await req.json();
  Object.keys(feedback).forEach(key => {
    if (feedback[key] === null) {
      delete feedback[key];
    }
  });

  let url = `${process.env.BACKEND_HOST}/v0/conversation/${feedback.id}/feedback`;
  const res = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      "email": req.headers.get("email") || "",
      "Authorization": req.headers.get("Authorization") || "",
    },
    method: 'POST',
    body: JSON.stringify(feedback),
  });
  return res;
}
