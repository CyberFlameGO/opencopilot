import {createContext, ReactNode, useContext, useEffect, useState} from "react";

type CopilotContextType = {
  copilotName: string | null;
  title: string | null;
  exampleMessages: string[] | null;
  description: string | null;
  footer: string | null;
  setCopilotName: (
    copilotName: string | null,
    title: string | null,
    exampleMessages: string[] | null,
    description: string | null,
    footer: string | null,
  ) => void;
};

const copilotContextDefaultValues: CopilotContextType = getDefaultCopilotContextValues();

function getDefaultCopilotContextValues(): CopilotContextType {
  return {
    copilotName: null,
    title: null,
    exampleMessages: null,
    description: null,
    footer: null,
    setCopilotName: (
      copilotName: string | null,
      title: string | null,
      exampleMessages: string[] | null,
      description: string | null,
      footer: string | null,
    ) => {
    },
  }
}

const CopilotContext = createContext<CopilotContextType>(copilotContextDefaultValues);

export function useCopilot() {
  return useContext(CopilotContext);
}


type Props = {
  children: ReactNode;
};

export function CopilotProvider({children}: Props) {
  const selectedCopilot = window.localStorage.getItem("selectedCopilot")
  let parsedData = null
  try {
    if (selectedCopilot) {
      parsedData = JSON.parse(selectedCopilot)
    }
  } catch (e) {

  }

  const [copilotName, setCopilotName] = useState<string | null>(parsedData ? parsedData.copilotName : null);
  const [title, setTitle] = useState<string | null>(parsedData ? parsedData.title : null);
  const [exampleMessages, setExampleMessages] = useState<string[] | null>(parsedData ? parsedData.exampleMessages : null);
  const [description, setDescription] = useState<string | null>(parsedData ? parsedData.description : null);
  const [footer, setFooter] = useState<string | null>(parsedData ? parsedData.footer : null);


  const changeCopilotName = (
    copilotName: string | null,
    title: string | null,
    exampleMessages: string[] | null,
    description: string | null,
    footer: string | null,
  ) => {
    setCopilotName(copilotName);
    setTitle(title)
    setExampleMessages(exampleMessages)
    setDescription(description)
    setFooter(footer)
    window.localStorage.setItem("selectedCopilot", JSON.stringify({
      copilotName,
      title,
      exampleMessages,
      description,
      footer
    }))
  };

  const value: CopilotContextType = {
    copilotName,
    title,
    exampleMessages,
    description,
    footer,
    setCopilotName: changeCopilotName
  };

  return (
    <>
      <CopilotContext.Provider value={value}>
        {children}
      </CopilotContext.Provider>
    </>
  );
}
