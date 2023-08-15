'use client'

import * as React from "react";
import {Input} from "@/components/ui/input";
import {useEffect, useState} from "react";

import {IconCheck, IconCopy, IconSpinnerNew} from "@/components/ui/icons";
import {useCopilot} from "@/lib/hooks/copilot-provider";
import {Copilot} from "@/lib/types";
import {useCopyToClipboard} from "@/lib/hooks/use-copy-to-clipboard";
import {useUser} from "@/lib/hooks/user-provider";

interface PollingData {
  status: string
  name: string
}

export function NewCopilotForm() {
  const {email, jwt} = useUser()

  const {isCopied, copyToClipboard} = useCopyToClipboard({timeout: 2000})

  const inputRef = React.useRef<HTMLInputElement>(null)
  const inputNameRef = React.useRef<HTMLInputElement>(null)
  const pRef = React.useRef<HTMLParagraphElement>(null);
  const formRef = React.useRef<HTMLFormElement>(null)
  const [ssh_key, setSSHKey] = useState<string | undefined>();
  const [pollingData, setPollingData] = useState<PollingData | null>(null);
  const [isPolling, setIsPolling] = useState(false);
  const [github_url, setGithubURL] = useState<string>("");
  const [copilot_name, setCopilotLocalName] = useState<string>("");
  const [isSynced, setCopilotSynced] = useState<boolean>(false);
  const [isGithubURLValid, setGithubURLValid] = useState(false);
  const [isNameValid, setNameValid] = useState(false);
  const {copilotName, setCopilotName} = useCopilot();
  const [ghURLForLink, setGhURLForLink] = useState<string>("");

  useEffect(() => {
    // setSSHKey("dsdnsajhdsajfnsajkfdjkfdngjkdsngngjkfn")
    // if (pRef && pRef.current)
    //     pRef.current.textContent = "dsdnsajhdsajfnsajkfdjkfdngjkdsngngjkfn";
    // setIsPolling(true);
    // setCopilotSynced(true);
  }, [ssh_key]);

  const validateGithubURL = (value: any) => {
    let result = value.replace("https://github.com/", "")
    result = result.replace("git@github.com:", "")
    result = result.replace(".git", "")
    result = result.replace("gh repo clone ", "")
    result = result.trim();
    if (result.split("/").length === 2) {
      setGithubURLValid(true);
      setGhURLForLink("https://github.com/" + result);
    } else {
      setGithubURLValid(false);
    }
    setGithubURL(value);
  };

  const validateNameInput = (value: any) => {
    const allowed = new Set<string>('abcdefghijklmnopqrstuvwxyz0123456789-'.split(''));
    const nameSet = new Set<string>(value.split(''));
    const isSubset = [...nameSet].every(c => allowed.has(c));

    setNameValid(isSubset);
    setCopilotLocalName(value);
  };

  const copyKey = () => {
    copyToClipboard(ssh_key || "")
  };

  function getConfigurationField(option: Copilot, field: string) {
    try {
      return option.configuration[field] || null;
    } catch (e) {
      return null
    }
  }

  useEffect(() => {
    let interval: any = null;
    if (isPolling) {
      interval = setInterval(async () => {
        await fetch(`${window.location.origin}/api/copilot`, {
          method: "POST",
          headers: {
            "accept": "application/json",
            "Content-Type": "application/json",
            "email": email || "",
            "Authorization": `Bearer ${jwt || ""}`,
          },
          body: JSON.stringify({})
        }).then(response => response.json())
          .then(data => {
            setPollingData(data);
            for (let i = 0; i < data['copilots'].length; i++) {
              let copilot = data['copilots'][i];

              if (copilot['copilot_id'] == copilot_name) {
                if (copilot['status'] == 'SYNCED') {
                  setCopilotSynced(true);
                  setCopilotName(
                    copilot_name,
                    getConfigurationField(copilot, "title"),
                    getConfigurationField(copilot, "example_messages"),
                    getConfigurationField(copilot, "description"),
                    getConfigurationField(copilot, "footer"),
                  );
                  window.location.href = window.location.origin;
                }
              }
            }
          })
          .catch(error => console.error(error));
      }, 5000);
    } else if (!isPolling && interval) {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isPolling]);


  const handleFormSubmit = async (e: { preventDefault: () => void }) => {
    e.preventDefault();
    let github_url, name;
    if (inputRef && inputRef.current) {
      github_url = inputRef.current.value || "";
      setGithubURL(github_url);
    }
    if (inputNameRef && inputNameRef.current) {
      name = inputNameRef.current.value || "";
      setCopilotLocalName(name);
    }
    if (isGithubURLValid && isNameValid) {
      setIsPolling(true);
    }
    try {
      const response = await fetch(`${window.location.origin}/api/copilots`, {
        method: "POST",
        headers: {
          "accept": "application/json",
          "Content-Type": "application/json",
          "email": email || "",
          "Authorization": `Bearer ${jwt || ""}`,
        },
        body: JSON.stringify({
          github_url: github_url,
          name: name
        })
      });

      const responseJson = await response.json();
      console.log(responseJson);
      if ("public_key" in responseJson) {
        setSSHKey(responseJson['public_key']);
      }
    } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
    }
  };


  return (
    <>
      <div className="mx-auto max-w-3xl px-4" style={{marginTop: `150px`}}>
        {!isPolling ?
          <div className="rounded-lg border p-8 bg-background">
            <form onSubmit={handleFormSubmit} ref={formRef} className="w-full">
              <h1 className="mb-2 text-lg" style={{fontSize: `25px`}}>
                Here’s how you can easily create a new Copilot ✌️
              </h1>
              <br/>
              <p className="mb-2 leading-normal text-muted-foreground" style={{color: '#E9F0F4'}}>
                Here is a step by step guide: <br/>
                1. Follow the set up steps in: <a style={{textDecoration: "underline"}}
                                                  href={'https://github.com/nftport/copilot-starter'}
                                                  target="_blank">https://github.com/nftport/copilot-starter</a> <br/>
                2. Come back with your copilot github url and add it below
              </p>
              <div className="mt-4 flex flex-col items-start space-y-2">
                <div className={"flex"}
                     style={{display: 'flex', alignItems: 'center', gap: '10px', paddingBottom: '10px'}}>
                  <div>
                    <p style={{
                      fontSize: '10px',
                      color: copilot_name.length > 0 ? (isNameValid ? 'green' : 'red') : '#838383'
                    }}>Your Copilot Name:</p>
                    <Input
                      ref={inputNameRef}
                      tabIndex={0}
                      placeholder=""
                      spellCheck={false}
                      style={{width: '250px'}}
                      onChange={e => validateNameInput(e.target.value)}
                    />
                  </div>
                  <div>
                    <p style={{
                      fontSize: '10px',
                      color: github_url.length > 0 ? (isGithubURLValid ? 'green' : 'red') : '#838383'
                    }}>Git URL:</p>
                    <Input
                      ref={inputRef}
                      tabIndex={0}
                      placeholder=""
                      spellCheck={false}
                      style={{width: '250px'}}
                      onChange={e => validateGithubURL(e.target.value)}
                    />
                  </div>

                </div>
              </div>

              <div className="w-full" style={{display: 'flex', justifyContent: 'flex-end', paddingTop: '20px'}}>
                <button type="submit" style={{
                  background: '#474747',
                  borderRadius: '5px',
                  width: '100px',
                  height: '41px',
                  padding: '10px',
                  opacity: (!isGithubURLValid || !isNameValid || isPolling) ? '0.5' : '1',
                  cursor: (!isGithubURLValid || !isNameValid || isPolling) ? 'not-allowed' : 'pointer'
                }} disabled={!isGithubURLValid || !isNameValid || isPolling}>
                  <span>Submit</span>
                </button>
              </div>
            </form>
          </div>
          : (
            isSynced ? <div>Success!</div> :
              <div className="rounded-lg border p-8 bg-background">
                <div>
                  <p style={{fontSize: '28px', color: '#EBF2F6'}}>Hang on tight, creating your Copilot</p>
                </div>
                <p className="mb-2 leading-normal text-muted-foreground" style={{color: '#E9F0F4', fontSize: '16px'}}>
                  Reminder: Add <a style={{textDecoration: "underline"}}
                                   href={ghURLForLink + "/settings/keys"} target="_blank">Deploy
                  Key</a> in your Copilot Github project <br/>
                </p>
                {ssh_key?.length ?
                  <div className="mt-4 flex flex-row items-start">
                    <p style={{color: '#B8B8B8'}} className="mr-4">click to copy key: </p>
                    {isCopied ? <IconCheck/> : <IconCopy/>}
                    <p ref={pRef} onClick={copyKey} className={"white-on-hover"} style={{
                      resize: 'none',
                      paddingLeft: '5px',
                      textOverflow: 'ellipsis',
                      textDecoration: 'underline',
                      whiteSpace: 'nowrap',
                      width: '400px',
                      overflow: 'hidden',
                      cursor: "pointer",
                    }}>{ssh_key}</p>
                  </div>
                  : <></>}
                <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', paddingTop: '20px'}}>
                  <br/>
                  <IconSpinnerNew className="mr-2 animate-spin" style={{flex: 1}}></IconSpinnerNew>
                </div>
              </div>)}
      </div>
    </>
  )
}
