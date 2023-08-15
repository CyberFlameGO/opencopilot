"use client"

import {notFound, redirect} from 'next/navigation'

import {getChat} from '@/app/actions'
import {Chat} from '@/components/chat'
import {useUser} from "@/lib/hooks/user-provider";
import {useEffect, useState} from "react";
import {useUser as auth0useUser} from "@auth0/nextjs-auth0/client";

export interface ChatPageProps {
  params: {
    id: string
  }
}

export default function ChatPage({params}: ChatPageProps) {
  let {userId} = useUser()
  const {user} = auth0useUser()
  if (!userId) {
    if (user && user.email) {
      userId = user.email
    }
  }

  const [currentChat, setChat] = useState<any | undefined>()

  if (!userId) {
    redirect(`/sign-in?next=/chat/${params.id}`)
  }

  let isQueried: boolean = false
  useEffect(() => {
    if (!isQueried) {
      isQueried = true
      getChat(params.id, userId || "").then(chat => {
        if (chat) {
          if ((chat?.userId !== userId)
            && process.env.VERCEL_ENV !== 'preview') {
            notFound()
          } else {
            setChat(chat)
          }
        } else {
          notFound()
        }
      })
    }
  }, [])

  return (<>
      {currentChat ?
        <Chat id={currentChat.id} initialMessages={currentChat.messages}/>
        :
        <></>
      }
    </>
  )
}
