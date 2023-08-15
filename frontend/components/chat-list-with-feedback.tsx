import {type UseChatHelpers} from '@/lib/hooks/use-chat'

import {Separator} from '@/components/ui/separator'
import {ChatMessage} from '@/components/chat-message'
import {FeedbackForm} from '@/components/feedback-form';
import {useUser} from "@/lib/hooks/user-provider";

export interface ChatListWithFeedbackProps
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
  isDebug?: boolean
  onDebugMessage: (messageId: string) => void
  debugMessageId: string | undefined
}

export function ChatListWithFeedback(
  {isLoading, id, messages, isDebug, onDebugMessage, debugMessageId}: ChatListWithFeedbackProps) {
  const {email, jwt} = useUser()

  if (!messages.length) {
    return null
  }
  const isLastMessageByAssistant = messages[messages.length - 1].role == 'assistant' && !isLoading;

  return (
    <div className="relative mx-auto max-w-2xl px-4">
      {messages.map((message, index) => (
        <div key={index}>
          <ChatMessage
            message={message}
            isDebug={isDebug}
            onDebugMessage={onDebugMessage}
            debugMessageId={debugMessageId}
          />
          {index < messages.length - 1 && (
            <Separator className="my-4 md:my-8"/>
          )}
        </div>
      ))}

      {isLastMessageByAssistant ?
        <FeedbackForm
          onSubmit={async (value) => {
            try {
              const response = await fetch(`${window.location.origin}/api/feedback`, {
                method: "POST",
                headers: {
                  "accept": "application/json",
                  "Content-Type": "application/json",
                  "email": email || "",
                  "Authorization": `Bearer ${jwt || ""}`
                },
                body: JSON.stringify({
                  id: value.id,
                  correctness: value.correctness,
                  helpfulness: value.helpfulness,
                  easy_to_understand: value.easy_to_understand,
                  free_form_feedback: value.free_form_feedback,
                })
              });

            } catch (error) {
              console.error('There has been a problem with your fetch operation:', error);
            }
          }}
          id={id || ""}
        />
        : <></>}


    </div>
  )
}
