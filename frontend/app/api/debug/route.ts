export const runtime = 'edge'

interface CopilotResponse {
  name: string,
  github_url: string,
  status: string
}

export async function POST(req: Request) {
  const json = await req.json()
  let url = `${process.env.BACKEND_HOST}/v0/debug/${json.conversationId}/${json.messageId}`;

  const res = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      "email": req.headers.get("email") || "",
      "Authorization": req.headers.get("Authorization") || "",
    },
    method: 'GET'
  });

  console.log(`Status code: ${res.status}`)
  if (res.status !== 200) {
    console.log(`Error response text: ${await res.text()}`)
    const result = await res.json();
  }

  return res
}
