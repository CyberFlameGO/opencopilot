import config from "tailwindcss/defaultConfig";

export interface CopilotConfig {
  EXAMPLE_MESSAGES: any[]
  EMPTY_SCREEN_TITLE: string
  EMPTY_SCREEN_BODY: string
  FOOTER: string

  TAB_TITLE_BASE: string
  TAB_TITLE_FORMAT: string
  DESCRIPTION: string
  // Paths could be improved by copilot name?
  ICON_PATH: string
  ICON_SHORTCUT: string
  ICON_APPLE: string
  LOGO_PATH: string,
  LOGO_LINK_URL: string
  LOGO_IMAGE_ATL: string
}

export interface Config {
  default: CopilotConfig
  rpm: CopilotConfig
  unity: CopilotConfig
}

export function getCopilotConfig(copilotName: string | undefined): CopilotConfig {
  // @ts-ignore
  if (!copilotName || !CONFIG[copilotName]) return CONFIG.default
  // @ts-ignore
  return CONFIG[copilotName]
}

export const CONFIG: Config = {
  default: {
    EXAMPLE_MESSAGES: [
      {
        heading: 'Who are you?',
        message: `Who are you?`
      },
    ],
    EMPTY_SCREEN_TITLE: "Hey, I’m Sidekik (Beta) 👋",
    EMPTY_SCREEN_BODY: "I’m here to help you make your own copilots!\n To create your own copilot, follow the README [here](https://github.com/opencopilotdev/opencopilot).",
    FOOTER: "Copilot may produce inaccurate information about people, places, or facts.",
    TAB_TITLE_BASE: "Sidekik Copilot",
    TAB_TITLE_FORMAT: "%s - Sidekik Copilot",
    DESCRIPTION: "An AI-powered copilot that help developers quickly build copilots.",
    ICON_PATH: "/default/favicon.ico",
    ICON_SHORTCUT: "/default/favicon-16x16.png",
    ICON_APPLE: "/default/apple-touch-icon.png",
    LOGO_PATH: "/default/logo.svg",
    LOGO_LINK_URL: "https://app.sidekik.ai",
    LOGO_IMAGE_ATL: "Sidekik logo",
  },
  rpm: {
    EXAMPLE_MESSAGES: [
      {
        heading: 'What is Ready Player Me and what platforms does it support?',
        message: `What is Ready Player Me and what platforms does it support?`
      },
      {
        heading: 'Integrating RPM avatars in Unity or Unreal Engine.',
        message: 'Integrating RPM avatars in Unity or Unreal Engine.'
      },
      {
        heading: 'Customizing the Avatar Creator appearance.',
        message: `Customizing the Avatar Creator appearance.`
      }
    ],
    EMPTY_SCREEN_TITLE: "Hey, I’m Ready Player Me’s Copilot (Beta) 👋",
    EMPTY_SCREEN_BODY: "I’m here to help developers like you with any questions you have about RPM \n \
          so you can integrate avatars into your app fast, without any previous experience. \n \
          I can help you debug, provide code, tutorials and much more. \n \ ",
    FOOTER: "RPM Copilot may produce inaccurate information about people, places, or facts.",
    TAB_TITLE_BASE: "Ready Player Me Copilot",
    TAB_TITLE_FORMAT: "%s - Ready Player Me Copilot",
    DESCRIPTION: "An AI-powered copilot that help developers quickly integrate Ready Player Me avatars into their app.",
    ICON_PATH: "/rpm/favicon.ico",
    ICON_SHORTCUT: "/rpm/favicon-16x16.png",
    ICON_APPLE: "/rpm/apple-touch-icon.png",
    LOGO_PATH: "/rpm/logo.svg",
    LOGO_LINK_URL: "https://docs.readyplayer.me",
    LOGO_IMAGE_ATL: "Ready Player Me logo",
  },
  unity: {
    EXAMPLE_MESSAGES: [
      {
        heading: 'Does Unity take royalties?',
        message: `Does Unity take royalties?`
      },
      {
        heading: 'How do I install unity?',
        message: 'How do I install unity?'
      },
      {
        heading: 'How to create a new scene?',
        message: `How to create a new scene?`
      }
    ],
    EMPTY_SCREEN_TITLE: "Hey, I’m Unity’s Copilot (Beta) 👋",
    EMPTY_SCREEN_BODY: "I’m here to help developers like you with any questions you have about Unity \n \
          so you can develop your games fast, without any previous experience. \n \
          I can help you debug, provide code, tutorials and much more. \n \ ",
    FOOTER: "Unity Copilot may produce inaccurate information about people, places, or facts.",

    TAB_TITLE_BASE: "Unity Copilot",
    TAB_TITLE_FORMAT: "%s - Unity Copilot",
    DESCRIPTION: "An AI-powered copilot that help developers quickly integrate Unity avatars into their app.",
    ICON_PATH: "/unity/favicon.ico",
    ICON_SHORTCUT: "/unity/favicon-16x16.png",
    ICON_APPLE: "/unity/apple-touch-icon.png",
    LOGO_PATH: "/unity/logo.svg",
    LOGO_LINK_URL: "https://docs.unity3d.com",
    LOGO_IMAGE_ATL: "Unity logo",
  },
}