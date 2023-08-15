export const runtime = 'edge'


export async function POST(req: Request) {
  const json = await req.json()
  // TODO: fix this stupid logic?
  const auth = req.headers.get("Authorization")
  if (!auth || auth.length < 10) {
    const newAuth = await getJwtToken(json.email)
    req.headers.set("Authorization", "Bearer " + newAuth)
  }

  const {messages, chatId, copilotName} = json
  // TODO: choose which url to use (custom copilot or not)
  let url = `${process.env.BACKEND_HOST}/v0/conversation_stream/${chatId}`;
  if (copilotName && copilotName != process.env.NEXT_PUBLIC_COPILOT_DISPLAY_NAME) {
    url = `${process.env.BACKEND_HOST}/v0/custom/${copilotName}/conversation_stream/${chatId}`;
  }
  console.log(`API url: ${url}`)
  const requestBody = JSON.stringify({
    inputs: messages.slice(-1)[0].content,
    email: json.email || "",
    response_message_id: json.responseMessageId,
  })
  console.log(`Request body: ${requestBody}`)

  const res = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      "Authorization": req.headers.get("Authorization") || "",
      // Should not rely on this email, but rather decode jwt and take email from payload
      "email": json.email || "",
    },
    method: 'POST',
    body: requestBody,
  });
  const encoder = new TextEncoder();
  const decoder = new TextDecoder();

  console.log(`Status code: ${res.status}`)
  if (res.status !== 200) {
    console.log(`Error response text: ${await res.text()}`)
    const result = await res.json();
    if (result.error) {
      throw new Error(
        result.error.message,
        result.error.type,
      );
    } else {
      throw new Error(
        `OpenAI API returned an error: ${
          decoder.decode(result?.value) || result.statusText
        }`,
      );
    }
  }

  // const stream = OpenAIStream(res, {
  //   async onCompletion(completion) {
  //     const title = json.messages[0].content.substring(0, 100)
  //     const userId = "asdasd"
  //     if (userId) {
  //       const id = json.id ?? "asdasd"
  //       const createdAt = Date.now()
  //       const path = `/chat/${id}`
  //       const payload = {
  //         id,
  //         title,
  //         userId,
  //         createdAt,
  //         path,
  //         messages: [
  //           ...messages,
  //           {
  //             content: completion,
  //             role: 'assistant'
  //           }
  //         ]
  //       }
  //       // await kv.hmset(`chat:${id}`, payload)
  //       // await kv.zadd(`user:chat:${userId}`, {
  //       //   score: createdAt,
  //       //   member: `chat:${id}`
  //       // })
  //     }
  //   }
  // })
  //
  // return new StreamingTextResponse(stream)

  return res
}

async function getJwtToken(email: string) {
  if (!email) {
    email = "localhost@localhost.com"
  }
  const url = `${process.env.BACKEND_HOST}/v0/token`;
  const requestBody = JSON.stringify({
    client_id: process.env.JWT_CLIENT_ID,
    client_secret: process.env.JWT_CLIENT_SECRET,
    user_id: email
  })
  console.log("getJwtToken url: " + url)
  console.log("getJwtToken requestBody: " + requestBody)
  const res = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
    },
    method: 'POST',
    body: requestBody,
  });
  if (res.status !== 200) {
    const result = await res.json();
    throw new Error(
        "Failed to authenticate with backend"
      );
  } else {
    const result = await res.json();
    console.log("getJwtToken result: " + JSON.stringify(result))
    const token = result.token
    return token
  }
}
