import {useCallback, useRef, useEffect, useState} from 'react'
import useSWRMutation from 'swr/mutation'
import useSWR from 'swr'
import {v4} from 'uuid'

import type {
  Message,
  CreateMessage,
  UseChatOptions,
  RequestOptions,
  Feedback,
  UseFeedbackOptions,
} from '../types'
import {nanoid} from "nanoid";
import {createChunkDecoder} from "@/lib/utils";
import {saveChat} from "@/app/actions";
import {useCopilot} from "@/lib/hooks/copilot-provider";
import {LoadingMessage} from "../types";
import {useUser} from "@/lib/hooks/user-provider";
import {useUser as auth0useUser} from "@auth0/nextjs-auth0/client";

export type {Message, CreateMessage, UseChatOptions, Feedback, UseFeedbackOptions}

export type UseChatHelpers = {
  /** Current messages in the chat */
  messages: Message[]
  /** The error object of the API request */
  error: undefined | Error
  /**
   * Append a user message to the chat list. This triggers the API call to fetch
   * the assistant's response.
   * @param message The message to append
   * @param options Additional options to pass to the API call
   */
  append: (
    message: Message | CreateMessage,
    options?: RequestOptions
  ) => Promise<string | null | undefined>
  /**
   * Reload the last AI chat response for the given chat history. If the last
   * message isn't from the assistant, it will request the API to generate a
   * new response.
   */
  reload: (options?: RequestOptions) => Promise<string | null | undefined>
  /**
   * Abort the current request immediately, keep the generated tokens if any.
   */
  stop: () => void
  /**
   * Update the `messages` state locally. This is useful when you want to
   * edit the messages on the client, and then trigger the `reload` method
   * manually to regenerate the AI response.
   */
  setMessages: (messages: Message[]) => void
  /** The current value of the input */
  input: string
  /** setState-powered method to update the input value */
  setInput: React.Dispatch<React.SetStateAction<string>>
  /** An input/textarea-ready onChange handler to control the value of the input */
  handleInputChange: (
    e:
      | React.ChangeEvent<HTMLInputElement>
      | React.ChangeEvent<HTMLTextAreaElement>
  ) => void
  /** Form submission handler to automattically reset input and append a user message  */
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void
  /** Whether the API request is in progress */
  isLoading: boolean
}

export type UseFeedbackHelpers = {
  /** The error object of the API request */
  error: undefined | Error
  /**
   * Sends a user feed to the server. This triggers the API call to send feedback.
   * @param feedback The feedback to submit
   * @param options Additional options to pass to the API call
   */
  submit: (
    feedback: Feedback,
    options?: RequestOptions
  ) => Promise<string | null | undefined>
  /** Whether the API request is in progress */
  isLoading: boolean
}

export function useChat({
                          api = '/api/chat',
                          id,
                          initialMessages = [],
                          initialInput = '',
                          sendExtraMessageFields,
                          onResponse,
                          onFinish,
                          onError,
                          headers,
                          body
                        }: UseChatOptions = {}): UseChatHelpers {
  let {jwt, userId} = useUser()
  const {user} = auth0useUser()
  if (!userId) {
    if (user && user.email) {
      userId = user.email
    }
  }

  // Generate a unique id for the chat if not provided.
  const hookId = v4()
  const chatId = id || hookId

  const {copilotName, setCopilotName} = useCopilot()


  // Store the chat state in SWR, using the chatId as the key to share states.
  const {data, mutate} = useSWR<Message[]>([api, chatId], null, {
    fallbackData: initialMessages
  })
  const messages = data!

  // Keep the latest messages in a ref.
  const messagesRef = useRef<Message[]>(messages)
  useEffect(() => {
    messagesRef.current = messages
  }, [messages])

  // Abort controller to cancel the current API call.
  const abortControllerRef = useRef<AbortController | null>(null)

  const extraMetadataRef = useRef<any>({
    headers,
    body
  })
  useEffect(() => {
    extraMetadataRef.current = {
      headers,
      body
    }
  }, [headers, body])

  // Actual mutation hook to send messages to the API endpoint and update the
  // chat state.
  const {error, trigger, isMutating} = useSWRMutation<
    string | null,
    any,
    [string, string],
    {
      messages: Message[]
      options?: RequestOptions
    }
  >(
    [api, chatId],
    async (_, {arg}) => {
      try {
        const {messages: messagesSnapshot, options} = arg
        const abortController = new AbortController()
        abortControllerRef.current = abortController

        // Do an optimistic update to the chat state to show the updated messages
        // immediately.
        const previousMessages = messagesRef.current
        mutate(messagesSnapshot, false)
        const responseMessageId: string = v4()

        const res = await fetch(api, {
          method: 'POST',
          body: JSON.stringify({
            messages: sendExtraMessageFields
              ? messagesSnapshot
              : messagesSnapshot.map(({role, content}) => ({
                role,
                content
              })),
            ...extraMetadataRef.current.body,
            ...options?.body,
            chatId,
            copilotName,
            responseMessageId,
            email: user?.email,
          }),
          headers: {
            Authorization: `Bearer ${jwt || ""}`,
            ...extraMetadataRef.current.headers,
            ...options?.headers
          },
          signal: abortController.signal
        }).catch(err => {
          // Restore the previous messages if the request fails.
          mutate(previousMessages, false)
          throw err
        })

        if (onResponse) {
          try {
            await onResponse(res)
          } catch (err) {
            throw err
          }
        }

        if (!res.ok) {
          // Restore the previous messages if the request fails.
          mutate(previousMessages, false)
          throw new Error(
            (await res.text()) || 'Failed to fetch the chat response.'
          )
        }

        if (!res.body) {
          throw new Error('The response body is empty.')
        }

        let result: string = ''
        let error: string = ''
        let loadingMessage: LoadingMessage | undefined = undefined
        const createdAt = new Date()
        const reader = res.body.getReader()
        const decode = createChunkDecoder()

        while (true) {
          const {done, value} = await reader.read()
          if (done) {
            break
          }
          // Update the chat state with the new message tokens.
          const chunks = decode(value);
          for (const chunk of chunks) {
            result += chunk.text || "";
            error += chunk.error || ""
            if (chunk.loading_message) {
              loadingMessage = {
                message: chunk.loading_message.message,
                calledCopilot: chunk.loading_message.called_copilot || undefined
              }
            }
          }
          mutate(
            [
              ...messagesSnapshot,
              {
                id: responseMessageId,
                createdAt,
                content: result,
                error,
                loadingMessage,
                role: 'assistant'
              }
            ],
            false
          )

          // The request has been aborted, stop reading the stream.
          if (abortControllerRef.current === null) {
            reader.cancel()
            break
          }
        }

        await saveChat(
          messagesSnapshot,
          createdAt,
          id,
          userId,
          result,
          copilotName || ""
        )

        if (onFinish) {
          onFinish({
            id: responseMessageId,
            createdAt,
            content: result,
            role: 'assistant'
          })
        }

        abortControllerRef.current = null
        return result
      } catch (err) {
        // Ignore abort errors as they are expected.
        if ((err as any).name === 'AbortError') {
          abortControllerRef.current = null
          return null
        }

        if (onError && err instanceof Error) {
          onError(err)
        }

        throw err
      }
    },
    {
      populateCache: false,
      revalidate: false
    }
  )

  const append = useCallback<UseChatHelpers['append']>(
    async (message, options) => {
      if (!message.id) {
        message.id = nanoid()
      }
      return trigger({
        messages: messagesRef.current.concat(message as Message),
        options
      })
    },
    [trigger]
  )

  const reload = useCallback<UseChatHelpers['reload']>(
    async options => {
      if (messagesRef.current.length === 0) return null

      const lastMessage = messagesRef.current[messagesRef.current.length - 1]
      if (lastMessage.role === 'assistant') {
        return trigger({
          messages: messagesRef.current.slice(0, -1),
          options
        })
      }
      return trigger({
        messages: messagesRef.current,
        options
      })
    },
    [trigger]
  )

  const stop = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }
  }, [])

  const setMessages = useCallback(
    (messages: Message[]) => {
      mutate(messages, false)
      messagesRef.current = messages
    },
    [mutate]
  )

  // Input state and handlers.
  const [input, setInput] = useState(initialInput)

  const handleSubmit = useCallback(
    (e: React.FormEvent<HTMLFormElement>, metadata?: Object) => {
      if (metadata) {
        extraMetadataRef.current = {
          ...extraMetadataRef.current,
          ...metadata
        }
      }

      e.preventDefault()
      if (!input) return
      append({
        content: input,
        role: 'user',
        createdAt: new Date()
      })
      setInput('')
    },
    [input, append]
  )

  const handleInputChange = (e: any) => {
    setInput(e.target.value)
  }

  return {
    messages,
    error,
    append,
    reload,
    stop,
    setMessages,
    input,
    setInput,
    handleInputChange,
    handleSubmit,
    isLoading: isMutating
  }
}
