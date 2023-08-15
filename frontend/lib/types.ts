export const PREVIEW_USER_ID = "preview-user-123"

export type Message = {
  id: string
  createdAt?: Date
  content: string
  error?: string
  loadingMessage?: LoadingMessage
  role: 'system' | 'user' | 'assistant'
}

export type LoadingMessage = {
  message: string
  calledCopilot?: string
}

export type Feedback = {
  id: string
  correctness?: number
  helpfulness?: number
  easy_to_understand?: number
  free_form_feedback?: string
}

export type Copilot = {
  name: string,
  github_url: string,
  status: string,
  configuration: any,
  git_message: string,
  git_hash: string
}

export type CopilotList = Copilot[]

export type CreateMessage = {
  id?: string
  createdAt?: Date
  content: string
  role: 'system' | 'user' | 'assistant'
}

export type RequestOptions = {
  headers?: Record<string, string> | Headers
  body?: object
}

export type UseChatOptions = {
  userId?: string
  /**
   * The API endpoint that accepts a `{ messages: Message[] }` object and returns
   * a stream of tokens of the AI chat response. Defaults to `/api/chat`.
   */
  api?: string

  /**
   * A unique identifier for the chat. If not provided, a random one will be
   * generated. When provided, the `useChat` hook with the same `id` will
   * have shared states across components.
   */
  id?: string

  /**
   * Initial messages of the chat. Useful to load an existing chat history.
   */
  initialMessages?: Message[]

  /**
   * Initial input of the chat.
   */
  initialInput?: string

  /**
   * Callback function to be called when the API response is received.
   */
  onResponse?: (response: Response) => void | Promise<void>

  /**
   * Callback function to be called when the chat is finished streaming.
   */
  onFinish?: (message: Message) => void

  /**
   * Callback function to be called when an error is encountered.
   */
  onError?: (error: Error) => void

  /**
   * HTTP headers to be sent with the API request.
   */
  headers?: Record<string, string> | Headers

  /**
   * Extra body object to be sent with the API request.
   * @example
   * Send a `sessionId` to the API along with the messages.
   * ```js
   * useChat({
   *   body: {
   *     sessionId: '123',
   *   }
   * })
   * ```
   */
  body?: object

  /**
   * Whether to send extra message fields such as `message.id` and `message.createdAt` to the API.
   * Defaults to `false`. When set to `true`, the API endpoint might need to
   * handle the extra fields before forwarding the request to the AI service.
   */
  sendExtraMessageFields?: boolean
}

export type UseFeedbackOptions = {
  /**
   * The API endpoint that accepts a `{"correctness": 5,
   *   "helpfulness": 5,
   *   "easy_to_understand": 5,
   *   "free_form_feedback": "string" }` object and returns
   * response "OK".
   */
  api?: string

  /**
   * A unique identifier for the chat. If not provided, a random one will be
   * generated. When provided, the `useChat` hook with the same `id` will
   * have shared states across components.
   */
  id?: string

  /**
   * HTTP headers to be sent with the API request.
   */
  headers?: Record<string, string> | Headers

  /**
   * Extra body object to be sent with the API request.
   * @example
   * Send a `sessionId` to the API along with the messages.
   * ```js
   * useChat({
   *   body: {
   *     sessionId: '123',
   *   }
   * })
   * ```
   */
  body?: object

  /**
   * Whether to send extra message fields such as `message.id` and `message.createdAt` to the API.
   * Defaults to `false`. When set to `true`, the API endpoint might need to
   * handle the extra fields before forwarding the request to the AI service.
   */
  sendExtraMessageFields?: boolean
}

export type UseCompletionOptions = {
  /**
   * The API endpoint that accepts a `{ prompt: string }` object and returns
   * a stream of tokens of the AI completion response. Defaults to `/api/completion`.
   */
  api?: string
  /**
   * A unique identifier for the chat. If not provided, a random one will be
   * generated. When provided, the `useChat` hook with the same `id` will
   * have shared states across components.
   */
  id?: string

  /**
   * Initial prompt input of the completion.
   */
  initialInput?: string

  /**
   * Initial completion result. Useful to load an existing history.
   */
  initialCompletion?: string

  /**
   * Callback function to be called when the API response is received.
   */
  onResponse?: (response: Response) => void | Promise<void>

  /**
   * Callback function to be called when the completion is finished streaming.
   */
  onFinish?: (prompt: string, completion: string) => void

  /**
   * Callback function to be called when an error is encountered.
   */
  onError?: (error: Error) => void

  /**
   * HTTP headers to be sent with the API request.
   */
  headers?: Record<string, string> | Headers

  /**
   * Extra body object to be sent with the API request.
   * @example
   * Send a `sessionId` to the API along with the prompt.
   * ```js
   * useChat({
   *   body: {
   *     sessionId: '123',
   *   }
   * })
   * ```
   */
  body?: object
}

export interface Chat extends Record<string, any> {
  id: string
  title: string
  createdAt: Date
  userId: string
  path: string
  messages: Message[]
  sharePath?: string,
  copilotName: string,
}

export type ServerActionResult<Result> = Promise<
  | Result
  | {
  error: string
}
>


