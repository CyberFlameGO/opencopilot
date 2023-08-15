'use server'

import {revalidatePath} from 'next/cache'
import {redirect} from 'next/navigation'
import {kv} from '@vercel/kv'

import {type Chat, CopilotList, Message} from '@/lib/types'

export async function getChats(userId?: string | null): Promise<Chat[]> {
  console.log(`getChats ${userId}`)
  if (!userId) {
    return []
  }

  try {
    const pipeline = kv.pipeline()
    const chats: string[] = await kv.zrange(`user:chat:${userId}`, 0, -1, {
      rev: true
    })

    for (const chat of chats) {
      pipeline.hgetall(chat)
    }

    const results = await pipeline.exec()
    console.log(`getChats results ${results}`)
    return results as Chat[]
  } catch (error) {
    console.log(`getChats got error ${error}`)
    return []
  }
}

export async function getChat(id: string, userId: string): Promise<Chat | null> {
  if (!validateUser(userId)) {
    return null
  }
  try {
    const chat: Chat | null = await kv.hgetall<Chat>(`chat:${id}`)
    // console.log(`GetChat ${chat}`)
    // if (!chat || (userId && chat.userId !== userId)) {
    //   return null
    // }
    return chat
  } catch {

  }
  return null
}

export async function removeChat({id, path, userId}: {
  id: string;
  path: string,
  userId: string | undefined,
}): Promise<{ error: string } | void> {

  if (!validateUser(userId)) {
    return {
      error: 'Unauthorized'
    }
  }

  const uid = await kv.hget<string>(`chat:${id}`, 'userId')

  if (uid !== userId) {
    return {
      error: 'Unauthorized'
    }
  }

  await kv.del(`chat:${id}`)
  await kv.zrem(`user:chat:${userId}`, `chat:${id}`)

  revalidatePath('/')
  return revalidatePath(path)
}

export async function clearChats(): Promise<{ error: string } | never> {
  const session: any = undefined;

  if (!session || !session?.user?.sub) {
    return {
      error: 'Unauthorized'
    }
  }

  const chats: string[] = await kv.zrange(`user:chat:${session.user.sub}`, 0, -1)
  if (!chats.length) {
    return redirect('/')
  }
  const pipeline = kv.pipeline()

  for (const chat of chats) {
    pipeline.del(chat)
    pipeline.zrem(`user:chat:${session.user.sub}`, chat)
  }

  await pipeline.exec()

  revalidatePath('/')
  return redirect('/')
}

export async function getSharedChat(id: string): Promise<Chat | null> {
  // console.log(`Get shared chat ${id}`)
  try {
    const chat = await kv.hgetall<Chat>(`chat:${id}`)
    if (!chat || !chat.sharePath) {
      return null
    }
    return chat
  } catch (e) {
    console.log(`getSharedChat error with id ${id}`)
  }
  // console.log(`Shared chat ${chat}`)

  return null
}

export async function shareChat(chat: Chat, userId: string) {
  if (chat.userId !== userId) {
    return {
      error: 'Unauthorized'
    }
  }

  const payload = {
    ...chat,
    sharePath: `/share/${chat.id}`
  }
  try {
    await kv.hmset(`chat:${chat.id}`, payload)
    return payload
  } catch (e) {
    return {error: "error"}
  }

}

export async function saveChat(
  messagesSnapshot: Message[],
  createdAt: Date,
  id: string | undefined,
  userId: string | undefined,
  result: string,
  copilotName: string,
) {
  if (!id || !userId) {
    return
  }
  const title = messagesSnapshot[0].content.substring(0, 100)
  const path = `/chat/${id}`
  const payload = {
    id,
    title,
    userId: userId,
    copilotName: copilotName,
    createdAt,
    path,
    messages: [
      ...messagesSnapshot,
      {
        content: result,
        role: 'assistant'
      }
    ]
  }
  try {
    await kv.hmset(`chat:${id}`, payload)
    await kv.zadd(`user:chat:${userId}`, {
      score: Date.now(),
      member: `chat:${id}`
    })
  } catch (e) {
    console.log(`Error saving chat: ${id}`)
  }
}

function validateUser(
  userId: string | undefined
): boolean {
  // TODO: validate jwt against backend and check that userId matches jwt?
  // Validate email too if present
  return true
}