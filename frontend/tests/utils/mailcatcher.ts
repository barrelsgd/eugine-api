import type { APIRequestContext } from "@playwright/test"

type Email = {
  id: number
  recipients: string[]
  subject: string
  created_at?: string
}

const DEFAULT_MAILCATCHER_BASE_URL = "http://mailcatcher:1080"

function getMailcatcherBaseUrl(): string {
  return process.env.MAILCATCHER_HOST ?? DEFAULT_MAILCATCHER_BASE_URL
}

async function findEmail({
  request,
  filter,
}: { request: APIRequestContext; filter?: (email: Email) => boolean }) {
  const baseUrl = getMailcatcherBaseUrl()
  
  try {
    console.log(`[mailcatcher] GET ${baseUrl}/messages`)
    const response = await request.get(`${baseUrl}/messages`)

    if (!response.ok()) {
      const responseText = await response.text().catch(() => "failed to read response")
      console.warn(
        `[mailcatcher] GET ${baseUrl}/messages failed: ${response.status()} ${response.statusText()}, body: ${responseText}`,
      )
      return null
    }

    const responseText = await response.text()
    console.log(`[mailcatcher] Raw response: ${responseText}`)
    
    let emails: Email[]
    try {
      emails = JSON.parse(responseText) as Email[]
    } catch (parseError) {
      console.error(`[mailcatcher] JSON parse error: ${parseError}, raw: ${responseText}`)
      return null
    }

    console.log(`[mailcatcher] Found ${emails.length} total emails:`)
    emails.forEach((email, index) => {
      console.log(`  [${index}] ID: ${email.id}, Recipients: ${JSON.stringify(email.recipients)}, Subject: "${email.subject}", Created: ${email.created_at || 'unknown'}`)
    })

    if (filter) {
      const originalCount = emails.length
      emails = emails.filter(filter)
      console.log(`[mailcatcher] After filter: ${emails.length}/${originalCount} emails`)
    }

    const email = emails[emails.length - 1]

    if (email) {
      console.log(`[mailcatcher] Selected email: ID ${email.id}, Subject: "${email.subject}"`)
      return email as Email
    }

    console.log(`[mailcatcher] No email found (total: ${emails.length}, after filter: ${emails.length})`)
    return null
  } catch (error) {
    console.error(`[mailcatcher] Request error: ${error}`)
    return null
  }
}

export function findLastEmail({
  request,
  filter,
  timeout = Number(process.env.MAILCATCHER_TIMEOUT_MS ?? "60000"),
}: {
  request: APIRequestContext
  filter?: (email: Email) => boolean
  timeout?: number
}) {
  const baseUrl = getMailcatcherBaseUrl()
  console.log(`[mailcatcher] Starting polling: base=${baseUrl}, timeout=${timeout}ms, filter=${!!filter}`)

  const timeoutPromise = new Promise<never>((_, reject) =>
    setTimeout(
      () => {
        console.error(`[mailcatcher] TIMEOUT after ${timeout}ms - no email found`)
        reject(new Error("Timeout while trying to get latest email"))
      },
      timeout,
    ),
  )

  const checkEmails = async () => {
    let delay = 500
    const maxDelay = 2000
    let attemptCount = 0
    const maxAttempts = 5 // Reduced from unlimited to 5 attempts for faster feedback

    while (attemptCount < maxAttempts) {
      attemptCount++
      console.log(`[mailcatcher] Attempt #${attemptCount}/${maxAttempts}`)
      
      try {
        const emailData = await findEmail({ request, filter })

        if (emailData) {
          console.log(`[mailcatcher] SUCCESS: Found email after ${attemptCount} attempts`)
          return emailData
        }
      } catch (err) {
        console.warn(`[mailcatcher] Attempt #${attemptCount} error: ${(err as Error).message}`)
      }

      if (attemptCount < maxAttempts) {
        console.log(`[mailcatcher] Attempt #${attemptCount} failed, retrying in ${delay}ms`)
        await new Promise((resolve) => setTimeout(resolve, delay))
        delay = Math.min(maxDelay, Math.floor(delay * 1.5))
      }
    }
    
    console.error(`[mailcatcher] FAILED: No email found after ${maxAttempts} attempts`)
    throw new Error(`No email found after ${maxAttempts} attempts`)
  }

  return Promise.race([timeoutPromise, checkEmails()])
}
