import {type UseChatHelpers} from '@/lib/hooks/use-chat'

import {Button} from '@/components/ui/button'
import {PromptForm} from '@/components/prompt-form'
import {ButtonScrollToBottom} from '@/components/button-scroll-to-bottom'
import {IconRefresh, IconStop} from '@/components/ui/icons'
import {FooterText} from '@/components/footer'
import * as React from "react";
import {Tooltip, TooltipContent, TooltipTrigger} from "@/components/ui/tooltip";
import {useSidebar} from "@/lib/hooks/sidebar-provider";


export interface ChatPanelProps
  extends Pick<
    UseChatHelpers,
    | 'append'
    | 'isLoading'
    | 'reload'
    | 'messages'
    | 'stop'
    | 'input'
    | 'setInput'
  > {
  id?: string
}

const MAX_MESSAGE_LENGTH: number = 10000


export function ChatPanel({
                            id,
                            isLoading,
                            stop,
                            append,
                            reload,
                            input,
                            setInput,
                            messages
                          }: ChatPanelProps) {
  
                            const { isSidebarOpen } = useSidebar();

  return (
    <div className="fixed inset-x-0 bottom-0" style={{ right: isSidebarOpen ? '320px' : '0px', transition: "right 0.2s ease-in-out"}}>
      <ButtonScrollToBottom/>
      <div className="mx-auto sm:max-w-2xl sm:px-4">
        <div className="flex h-10 items-center justify-center">
          {isLoading ? (
            <Button
              variant="outline"
              onClick={() => stop()}
              className="bg-background"
            >
              <IconStop className="mr-2"/>
              Stop generating
            </Button>
          ) : (
            messages?.length > 0 && (
              <Button
                variant="outline"
                onClick={() => reload()}
                className="bg-background"
              >
                <IconRefresh className="mr-2"/>
                Regenerate response
              </Button>
            )
          )}
        </div>
        <div className="space-y-4 border-t bg-background px-4 py-2 shadow-lg sm:rounded-xl sm:border md:py-4">
          <PromptForm
            onSubmit={async value => {
              if (value.length > MAX_MESSAGE_LENGTH) {
                return
              }
              await append({
                id,
                content: value,
                role: 'user'
              })
            }}
            input={input}
            setInput={setInput}
            isLoading={isLoading}
            maxMessageLength={MAX_MESSAGE_LENGTH}
          />
          <div className="hidden flex-row sm:flex md:h-4 sm:h-6 md:pb-0 sm:pb-2">
            <div style={{width: "10%"}}/>
            <FooterText className="sm:block"/>
            <div style={{width: "10%", position: "relative"}}>
              <CharacterLimitCounter input={input}/>
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}

const CharacterLimitCounter = ({input}: { input: string }) => {

  const getColor = () => {
    if (input.length < (MAX_MESSAGE_LENGTH - 1000)) {
      return "#4982f8"
    }
    if (input.length < MAX_MESSAGE_LENGTH) {
      return "#d3ad1b"
    }
    return "#d50c0c"
  }

  const getRemainingCount = () => {
    if (input.length >= (MAX_MESSAGE_LENGTH - 1000)) {
      return MAX_MESSAGE_LENGTH - input.length
    }
  }

  const getDescription = () => {
    if (input.length > MAX_MESSAGE_LENGTH) {
      return "Character limit exceeded. LLMs have a limited context length."
    }
    return "Characters left. LLMs have a limited context length."
  }


  if (input.length < (MAX_MESSAGE_LENGTH - 1000)) {
    return <></>
  }
  return <Tooltip delayDuration={1000}>
    <TooltipTrigger
      tabIndex={-1}
      className="focus:bg-muted focus:ring-1 focus:ring-ring"
    >
      <div
        style={{
          height: "30px",
          width: "30px",
          marginLeft: "auto",
          position: "absolute",
          bottom: "-6px",
          right: "5px"
        }}>
        <span style={{
          position: "absolute",
          top: "0",
          left: "0",
          width: "30px",
          textAlign: "center",
          paddingTop: "2px",
          color: getColor(),
        }}>
      {getRemainingCount()}
    </span>
      </div>
    </TooltipTrigger>
    <TooltipContent>{getDescription()}</TooltipContent>
  </Tooltip>
}
