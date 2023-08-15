import {FooterText} from '@/components/footer'
import {NewCopilotForm} from "@/components/new-copilot-form";

export const runtime = 'edge'
export const preferredRegion = 'home'


export default async function NewCopilotPage() {

  return (
    <>
      <NewCopilotForm/>
      <FooterText className="py-8"/>
    </>
  )
}
