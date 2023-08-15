import {clsx, type ClassValue} from 'clsx'
import {customAlphabet} from 'nanoid'
import {twMerge} from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const nanoid = customAlphabet(
  '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
  7
) // 7-character random string

interface Chunk {
  text?: string;
  [key: string]: any;
}


export function createChunkDecoder(): (chunk: Uint8Array | undefined) => Chunk[]  {
  const decoder = new TextDecoder();
  return function (chunk: Uint8Array | undefined): Chunk[] {
    if (!chunk) return [];
    const jsonString = decoder.decode(chunk, {stream: true});
    const jsonLines = jsonString.split('\n').filter(Boolean); // Split by line and remove empty lines
    const chunks: Chunk[] = [];
    for (const line of jsonLines) {
      try {
        const chunkObject = JSON.parse(line) as Chunk;
        chunks.push(chunkObject);
      } catch (error) {
        console.error('Failed to parse JSON:', line);
      }
    }
    return chunks;
  }
}

export async function fetcher<JSON = any>(
  input: RequestInfo,
  init?: RequestInit
): Promise<JSON> {
  const res = await fetch(input, init)

  if (!res.ok) {
    const json = await res.json()
    if (json.error) {
      const error = new Error(json.error) as Error & {
        status: number
      }
      error.status = res.status
      throw error
    } else {
      throw new Error('An unexpected error occurred')
    }
  }

  return res.json()
}

export function formatDate(input: string | number | Date): string {
  const date = new Date(input)
  return date.toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  })
}
