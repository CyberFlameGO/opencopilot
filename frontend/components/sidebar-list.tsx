"use client"

import {SidebarButton} from "@/components/sidebar-button";
import React, {useEffect, useState} from "react";
import {Chat} from "@/lib/types";
import {getChats, removeChat, shareChat} from "@/app/actions";
import {SidebarItem} from "@/components/sidebar-item";
import {SidebarActions} from "@/components/sidebar-actions";

export interface SidebarListProps {
  userId: string
}

export function SidebarList({userId}: SidebarListProps) {
  const [chats, setChats] = useState<Chat[]>([])

  let isQueried: boolean = false
  useEffect(() => {
    if (!isQueried) {
      isQueried = true
      getChats(userId).then(chats => {
        setChats(chats)
      })
    }
  }, [])

  return (
    <div className="flex-1 overflow-auto">
      <div className="space-y-2 px-2 mb-4">
        <SidebarButton/>
      </div>
      {chats?.length ? (
        <div className="space-y-2 px-2">
          {chats.map(
            chat =>
              chat && (
                <SidebarItem key={chat?.id} chat={chat}>
                  <SidebarActions
                    chat={chat}
                    removeChat={removeChat}
                    shareChat={shareChat}
                    userId={userId}
                  />
                </SidebarItem>
              )
          )}
        </div>
      ) : (
        <div className="p-8 text-center">
          <p className="text-sm text-muted-foreground">No chat history</p>
        </div>
      )}
    </div>
  )
}
