import type { APIRequestContext } from "@playwright/test"

type Email = {
  id: number
  recipients: string[]
  subject: string
}

async function findEmail({
  request,
  filter,
}: { request: APIRequestContext; filter?: (email: Email) => boolean }) {
  const baseUrl = process.env.MAILCATCHER_HOST ?? "http://mailcatcher:1080"
  const response = await request.get(`${baseUrl}/messages`)

  if (!response.ok()) {
    return null
  }

  let emails = await response.json()

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
  const timeoutPromise = new Promise<never>((_, reject) =>
    setTimeout(
      () => reject(new Error("Timeout while trying to get latest email")),
      timeout,
    ),
  )

  const checkEmails = async () => {
    while (true) {
      try {
        const emailData = await findEmail({ request, filter })

        if (emailData) {
          return emailData
        }
      } catch {
        // ignore transient request errors and retry
      }
      // Wait for 100ms before checking again
      await new Promise((resolve) => setTimeout(resolve, 100))
    }
  }

  return Promise.race([timeoutPromise, checkEmails()])
}
