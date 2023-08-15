import {type UseChatHelpers} from '@/lib/hooks/use-chat'

import remarkGfm from 'remark-gfm'

import {Button} from '@/components/ui/button'
import {IconArrowRight} from '@/components/ui/icons'
import {MemoizedReactMarkdown} from '@/components/markdown'
import ReactMarkdown from 'react-markdown'
import {CopilotConfig, getCopilotConfig} from '@/assets/config'
import {useEffect, useState} from "react";
import {useCopilot} from "@/lib/hooks/copilot-provider";

export function EmptyScreen({setInput}: Pick<UseChatHelpers, 'setInput'>) {

  const {
    copilotName,
    title,
    exampleMessages,
    description,
    footer,
  } = useCopilot()

  const [config, setConfig] = useState<CopilotConfig | undefined>();
  useEffect(() => {
    setConfig(getCopilotConfig(process.env.NEXT_PUBLIC_COPILOT_NAME))
  }, []);
  if (!config) {
    // Returns null on first render, so the client and server match
    return null;
  }

  return (
    <>
      <div className="mx-auto max-w-2xl px-4" style={{marginTop: `200px`}}>
        <div className="rounded-lg border p-8 bg-background">
          <h1 className="mb-2 text-lg" style={{fontSize: `25px`}}>
            {title || config.EMPTY_SCREEN_TITLE}
          </h1>
          <br/>
          {description ?
            <ReactMarkdown
              className="prose break-words dark:prose-invert prose-p:leading-relaxed prose-pre:p-0"
              remarkPlugins={[remarkGfm]}
              linkTarget="_blank"
              components={{
                p({children}) {
                  return <p className="mb-2 leading-normal text-muted-foreground last:mb-0">{children}</p>
                }
              }}
            >
              {description}
            </ReactMarkdown>
            :
            <ReactMarkdown
              className="prose break-words dark:prose-invert prose-p:leading-relaxed prose-pre:p-0"
              remarkPlugins={[remarkGfm]}
              linkTarget="_blank"
              components={{
                p({children}) {
                  return <p className="mb-2 leading-normal text-muted-foreground last:mb-0">{children}</p>
                }
              }}
            >
              {config.EMPTY_SCREEN_BODY || ""}
            </ReactMarkdown>
          }


          <br/>
          <p className="leading-normal text-muted-foreground">
            You can start a conversation below or try the following examples:
          </p>
          <div className="mt-4 flex flex-col items-start space-y-2">
            {exampleMessages ? <>
                {(exampleMessages).map((message, index) => (
                  <Button
                    key={index}
                    variant="link"
                    className="h-auto p-0 text-base"
                    onClick={() => setInput(message)}
                  >
                    <IconArrowRight className="mr-2 text-muted-foreground"/>
                    {message}
                  </Button>
                ))}
              </>
              :
              <>
                {(config.EXAMPLE_MESSAGES).map((message, index) => (
                  <Button
                    key={index}
                    variant="link"
                    className="h-auto p-0 text-base"
                    onClick={() => setInput(message.message)}
                  >
                    <IconArrowRight className="mr-2 text-muted-foreground"/>
                    {message.heading}
                  </Button>
                ))}
              </>}

          </div>
        </div>
      </div>
    </>
  )
}
