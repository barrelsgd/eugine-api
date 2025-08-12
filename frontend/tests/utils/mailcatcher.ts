import type { APIRequestContext } from "@playwright/test"

type Email = {
  id: number
  recipients: string[]
  subject: string
}

function getMailcatcherBaseUrl(): string {
  return process.env.MAILCATCHER_HOST ?? "http://mailcatcher:1080"
}

async function findEmail({
  request,
  filter,
}: { request: APIRequestContext; filter?: (email: Email) => boolean }) {
  const baseUrl = getMailcatcherBaseUrl()
  const response = await request.get(`${baseUrl}/messages`)

  if (!response.ok()) {
    // Log status for diagnostics, but keep returning null to allow retry loop
    console.warn(
      `[mailcatcher] GET ${baseUrl}/messages failed: ${response.status()} ${response.statusText()}`,
    )
    return null
  }

  let emails = (await response.json()) as Email[]

  if (filter) {
    emails = emails.filter(filter)
  }

  const email = emails[emails.length - 1]

  if (email) {
    return email as Email
  }

  return null
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
  console.log(`[mailcatcher] polling base: ${baseUrl}, timeout: ${timeout}ms`)

  const timeoutPromise = new Promise<never>((_, reject) =>
    setTimeout(
      () => reject(new Error("Timeout while trying to get latest email")),
      timeout,
    ),
  )

  const checkEmails = async () => {
    let delay = 100
    const maxDelay = 2000

    while (true) {
      try {
        const emailData = await findEmail({ request, filter })

        if (emailData) {
          return emailData
        }
      } catch (err) {
        console.warn(`[mailcatcher] transient error: ${(err as Error).message}`)
      }
      // backoff up to maxDelay
      await new Promise((resolve) => setTimeout(resolve, delay))
      delay = Math.min(maxDelay, Math.floor(delay * 1.5))
    }
  }

  return Promise.race([timeoutPromise, checkEmails()])
}
