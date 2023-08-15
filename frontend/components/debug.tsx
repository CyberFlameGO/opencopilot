import {useEffect, useState} from "react";
import * as React from "react";
import {IconTriangleClosed, IconTriangleOpen} from "@/components/ui/icons";
import ReactJson from "react-json-view";

// TODO: revise types etc
export interface DebugProps {
  metrics: DebugMetrics | undefined
  isLoading: boolean
  messageNumber: number | undefined
}

export interface DebugMetrics {
  promptTemplate: DebugMetric
  dataSources: string
  userQuestion: DebugMetric
  citations: DebugMetric
  context: DebugMetric
  chatHistory: DebugMetric
  fullPrompt: DebugMetric
  llmResponse: DebugMetric
}

export interface DebugMetric {
  value: string
  tokenCount: number | null
}

export function Debug({metrics, isLoading, messageNumber}: DebugProps) {

  return <div className="p-1">
    {isLoading ?
      <div>
        Loading...
      </div>
      :
      <>
        {!metrics ?
          <div>Nothing to display</div>
          :
          <div>
            <div className="h-10">
              Debug Message #{messageNumber || 0}
            </div>
            {/*<div>{JSON.stringify(metrics)}</div>*/}
            <DropDown title="Prompt template">
              <DebugText metric={metrics.promptTemplate}/>
            </DropDown>
            {/*<DropDown title="Data sources">*/}
            {/*  <DebugText metric={metrics.dataSources}/>*/}
            {/*</DropDown>*/}
            <DropDown title="User question">
              <DebugText metric={metrics.userQuestion}/>
            </DropDown>
            {/*<DropDown title="Citations - retrieved documents' sources">*/}
            {/*  <DebugText metric={metrics.citations}/>*/}
            {/*</DropDown>*/}
            <DropDown title="Context - retrieved documents' content">
              <DebugText metric={metrics.context}/>
            </DropDown>
            <DropDown title="Chat history">
              <DebugText metric={metrics.chatHistory}/>
            </DropDown>
            <DropDown title="Full prompt sent to the LLM">
              <DebugText metric={metrics.fullPrompt}/>
            </DropDown>
            <DropDown title="LLM response">
              <DebugText metric={metrics.llmResponse}/>
            </DropDown>
          </div>
        }
      </>
    }
  </div>
}

interface DropdownProps {
  title: string
  children: React.ReactNode
}

const DropDown = ({title, children}: DropdownProps) => {
  const [isOpen, setIsOpen] = useState<boolean>(false)

  return <div>
    <div
      className="cursor-pointer border-y-2 flex flex-row justify-between"
      onClick={() => setIsOpen(!isOpen)}>
      {title}
      <div style={{alignSelf: "center"}}>
        {isOpen ? <IconTriangleOpen/> : <IconTriangleClosed/>}
      </div>
    </div>
    {isOpen && <>
      {children}
    </>}
  </div>
}

const DebugText = ({metric}: { metric: DebugMetric }) => {
  function isJson(text: string): boolean {
    try {
      JSON.parse(text)
      return true
    } catch (e) {
      return false
    }
  }

  return <div
    style={{fontSize: "14px"}}
  >
    {metric.tokenCount && <div className="font-bold">Token count: {metric.tokenCount}</div>}
    {isJson(metric.value) ?
      <div>
        {JSON.parse(metric.value).map((v: any, i: number) => {
          return <div
            key={`v-${i}`}
            style={{fontSize: "14px"}}
          >
            <ReactJson src={v} theme="bright" indentWidth={2} name={null}/>
          </div>
        })}
      </div>
      :
      <div
        style={{whiteSpace: "pre-wrap"}}
      >
        {metric.value}
      </div>
    }
  </div>
}