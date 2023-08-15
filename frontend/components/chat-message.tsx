"use client"

import {LoadingMessage, Message} from '@/lib/types'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'

import {cn} from '@/lib/utils'
import {CodeBlock} from '@/components/ui/codeblock'
import {MemoizedReactMarkdown} from '@/components/markdown'
import {IconCopilot, IconDebug, IconError, IconSpinner, IconUser} from '@/components/ui/icons'
import {ChatMessageActions} from '@/components/chat-message-actions'
import * as React from "react";
import {useEffect, useState} from "react";
import {Tooltip, TooltipContent, TooltipTrigger} from "@/components/ui/tooltip";

export interface ChatMessageProps {
  message: Message
  isDebug?: boolean
  onDebugMessage: (messageId: string) => void
  debugMessageId?: string | undefined
}

export function ChatMessage(
  {message, isDebug, onDebugMessage, debugMessageId, ...props}: ChatMessageProps) {
  // This should only be done once I guess and not duplicated
  const [copilotName, setCopilotName] = useState<string | undefined>();
  useEffect(() => {
    if (process.env.NEXT_PUBLIC_COPILOT_NAME) {
      setCopilotName(process.env.NEXT_PUBLIC_COPILOT_NAME)
    }
  }, []);
  if (!copilotName) {
    // Returns null on first render, so the client and server match
    return <></>;
  }

  return (
    <div
      className={cn('group relative mb-4 flex items-start md:-ml-12')}
      {...props}
    >
      {(message.loadingMessage && !message.content && !message.error) ?
        <LoadingMessage loadingMessage={message.loadingMessage} copilotName={copilotName}/>
        :
        <>
          <div className="flex flex-col">
            <div
              className={cn(
                'flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow',
                message.role === 'user'
                  ? 'bg-background'
                  : 'bg-primary text-primary-foreground'
              )}
            >
              {message.role === 'user' ? <IconUser/> : <IconCopilot copilotName={copilotName}/>}
              {message.error && <IconError className={"absolute w-4 h-4"} style={{top: "1.2rem", left: "1.2rem"}}/>}
            </div>
            {(isDebug && message.role !== "user") &&
                <div className="pt-4">
                    <Tooltip>
                        <TooltipTrigger asChild>
                            <div
                                className="cursor-pointer"
                                style={{display: "flex", justifyContent: "center"}}
                                onClick={() => {
                                  onDebugMessage(message.id)
                                }}
                            >
                              {(debugMessageId && debugMessageId == message.id) ?
                                <IconDebug isActive={true}/>
                                :
                                <IconDebug isActive={false}/>
                              }
                            </div>
                        </TooltipTrigger>
                        <TooltipContent>Debug this message</TooltipContent>
                    </Tooltip>
                </div>
            }
          </div>
          <div className="ml-4 flex-1 space-y-2 overflow-hidden px-1">
            {message.error ?
              <div
                className="py-4 pl-2 border-red-500 border-2 bg-red-300 text-black"
                style={{borderRadius: "8px"}}
              >
                {message.error}
              </div>
              :
              <MemoizedReactMarkdown
                className="prose break-words dark:prose-invert prose-p:leading-relaxed prose-pre:p-0"
                remarkPlugins={[remarkGfm, remarkMath]}
                linkTarget="_blank"
                components={{
                  p({children}) {
                    return <p className="mb-2 last:mb-0">{children}</p>
                  },
                  code({node, inline, className, children, ...props}) {
                    if (children.length) {
                      if (children[0] == '▍') {
                        return (
                          <span className="mt-1 animate-pulse cursor-default">▍</span>
                        )
                      }

                      children[0] = (children[0] as string).replace('`▍`', '▍')
                    }

                    const match = /language-(\w+)/.exec(className || '')

                    if (inline) {
                      return (
                        <code className={className} {...props}>
                          {children}
                        </code>
                      )
                    }

                    return (
                      <CodeBlock
                        key={Math.random()}
                        language={(match && match[1]) || ''}
                        value={String(children).replace(/\n$/, '')}
                        {...props}
                      />
                    )
                  }
                }}
              >
                {message.content || ""}
              </MemoizedReactMarkdown>
            }
            <ChatMessageActions message={message}/>
          </div>
        </>
      }
    </div>
  )
}


function LoadingMessage({loadingMessage, copilotName}: { loadingMessage: LoadingMessage, copilotName: string }) {
  return <>
    <div
      className={cn(
        'flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow',
        'bg-white text-primary-foreground'
      )}
    >
      <IconCopilot copilotName={loadingMessage.calledCopilot || copilotName}/>
    </div>
    <div className="ml-4 h-8 flex-1 space-y-2 overflow-hidden px-1">
        <span
          className="bg-green-300 px-8 font-bold text-black"
          style={{
            height: "100%",
            width: "max-content",
            alignItems: "center",
            display: "flex",
            borderRadius: "5px"
          }}
        >
          {loadingMessage.message || ""}
          <IconSpinner className="ml-2 animate-spin"/>
        </span>
    </div>
  </>
}