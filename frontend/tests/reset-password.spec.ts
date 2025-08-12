import { expect, test } from "@playwright/test"
// Allow up to 120s for email-based flows in CI
test.setTimeout(120_000)
import { findLastEmail } from "./utils/mailcatcher"
import { randomEmail, randomPassword } from "./utils/random"
import { logInUser, signUpNewUser } from "./utils/user"

test.use({ storageState: { cookies: [], origins: [] } })

// Generate shard-specific email suffix to avoid cross-shard interference
const getShardId = () => process.env.PLAYWRIGHT_SHARD_INDEX || "local"
const createShardEmail = (baseEmail: string) => {
  const [local, domain] = baseEmail.split("@")
  return `${local}_shard${getShardId()}@${domain}`
}

test("Password Recovery title is visible", async ({ page }) => {
  await page.goto("/recover-password")

  await expect(
    page.getByRole("heading", { name: "Password Recovery" }),
  ).toBeVisible()
})

test("Input is visible, empty and editable", async ({ page }) => {
  await page.goto("/recover-password")

  await expect(page.getByPlaceholder("Email")).toBeVisible()
  await expect(page.getByPlaceholder("Email")).toHaveText("")
  await expect(page.getByPlaceholder("Email")).toBeEditable()
})

test("Continue button is visible", async ({ page }) => {
  await page.goto("/recover-password")

  await expect(page.getByRole("button", { name: "Continue" })).toBeVisible()
})

test("User can reset password successfully using the link", async ({
  page,
  request,
}) => {
  const fullName = "Test User"
  const baseEmail = randomEmail()
  const email = createShardEmail(baseEmail)
  const password = randomPassword()
  const newPassword = randomPassword()

  console.log(`[test] Shard ${getShardId()}: Using email ${email}`)

  // Sign up a new user
  await signUpNewUser(page, fullName, email, password)

  // Ensure clean mailbox for this test
  await request
    .delete(`${process.env.MAILCATCHER_HOST ?? "http://mailcatcher:1080"}/messages`)
    .catch(() => {})

  await page.goto("/recover-password")
  await page.getByPlaceholder("Email").fill(email)

  // Set up API response listener BEFORE clicking the button
  const apiResponsePromise = new Promise<void>((resolve) => {
    page.on('response', async response => {
      if (response.url().includes('/password-recovery/')) {
        const status = response.status()
        const statusText = response.statusText()
        console.log(`[test] Shard ${getShardId()}: Password recovery API response: ${status} ${statusText}`)
        console.log(`[test] Shard ${getShardId()}: API URL: ${response.url()}`)
        
        try {
          const responseBody = await response.text()
          console.log(`[test] Shard ${getShardId()}: Response body: ${responseBody}`)
        } catch (e) {
          console.log(`[test] Shard ${getShardId()}: Could not read response body: ${e}`)
        }
        resolve()
      }
    })
  })

  // Also listen for request failures
  page.on('requestfailed', request => {
    if (request.url().includes('/password-recovery/')) {
      console.log(`[test] Shard ${getShardId()}: Password recovery request FAILED: ${request.failure()?.errorText}`)
    }
  })

  await page.getByRole("button", { name: "Continue" }).click()

  console.log(`[test] Shard ${getShardId()}: Password recovery request sent, waiting for email...`)
  
  // Wait for the API response (max 10 seconds)
  try {
    await Promise.race([
      apiResponsePromise,
      new Promise((_, reject) => setTimeout(() => reject(new Error('API response timeout')), 10000))
    ])
    console.log(`[test] Shard ${getShardId()}: API response received, waiting for email processing...`)
  } catch (e) {
    console.log(`[test] Shard ${getShardId()}: API response timeout or error: ${e}`)
  }
  
  // Small delay for email processing
  await page.waitForTimeout(1000)

  const emailData = await findLastEmail({
    request,
    timeout: Number(process.env.MAILCATCHER_TIMEOUT_MS ?? "60000"),
    filter: (email) => email.recipients.some(recipient => recipient.includes(`shard${getShardId()}`))
  })

  await page.goto(
    `${process.env.MAILCATCHER_HOST ?? "http://mailcatcher:1080"}/messages/${emailData.id}.html`,
  )

  const selector = 'a[href*="/reset-password?token="]'

  let url = await page.getAttribute(selector, "href")

  // TODO: update var instead of doing a replace
  url = url!.replace("http://localhost/", "http://localhost:5173/")

  // Set the new password and confirm it
  await page.goto(url)

  await page.getByPlaceholder("New Password").fill(newPassword)
  await page.getByPlaceholder("Confirm Password").fill(newPassword)
  await page.getByRole("button", { name: "Reset Password" }).click()
  await expect(page.getByText("Password updated successfully")).toBeVisible()

  // Check if the user is able to login with the new password
  await logInUser(page, email, newPassword)
})

test("Expired or invalid reset link", async ({ page }) => {
  const password = randomPassword()
  const invalidUrl = "/reset-password?token=invalidtoken"

  await page.goto(invalidUrl)

  await page.getByPlaceholder("New Password").fill(password)
  await page.getByPlaceholder("Confirm Password").fill(password)
  await page.getByRole("button", { name: "Reset Password" }).click()

  await expect(page.getByText("Invalid token")).toBeVisible()
})

test("Weak new password validation", async ({ page, request }) => {
  const fullName = "Test User"
  const baseEmail = randomEmail()
  const email = createShardEmail(baseEmail)
  const password = randomPassword()
  const weakPassword = "123"

  console.log(`[test] Shard ${getShardId()}: Using email ${email}`)

  // Sign up a new user
  await signUpNewUser(page, fullName, email, password)

  // Ensure clean mailbox for this test
  await request
    .delete(`${process.env.MAILCATCHER_HOST ?? "http://mailcatcher:1080"}/messages`)
    .catch(() => {})

  await page.goto("/recover-password")
  await page.getByPlaceholder("Email").fill(email)

  // Set up API response listener BEFORE clicking the button
  const apiResponsePromise = new Promise<void>((resolve) => {
    page.on('response', async response => {
      if (response.url().includes('/password-recovery/')) {
        const status = response.status()
        const statusText = response.statusText()
        console.log(`[test] Shard ${getShardId()}: Password recovery API response: ${status} ${statusText}`)
        console.log(`[test] Shard ${getShardId()}: API URL: ${response.url()}`)
        
        try {
          const responseBody = await response.text()
          console.log(`[test] Shard ${getShardId()}: Response body: ${responseBody}`)
        } catch (e) {
          console.log(`[test] Shard ${getShardId()}: Could not read response body: ${e}`)
        }
        resolve()
      }
    })
  })

  // Also listen for request failures
  page.on('requestfailed', request => {
    if (request.url().includes('/password-recovery/')) {
      console.log(`[test] Shard ${getShardId()}: Password recovery request FAILED: ${request.failure()?.errorText}`)
    }
  })

  await page.getByRole("button", { name: "Continue" }).click()

  console.log(`[test] Shard ${getShardId()}: Password recovery request sent, waiting for email...`)
  
  // Wait for the API response (max 10 seconds)
  try {
    await Promise.race([
      apiResponsePromise,
      new Promise((_, reject) => setTimeout(() => reject(new Error('API response timeout')), 10000))
    ])
    console.log(`[test] Shard ${getShardId()}: API response received, waiting for email processing...`)
  } catch (e) {
    console.log(`[test] Shard ${getShardId()}: API response timeout or error: ${e}`)
  }
  
  // Small delay for email processing
  await page.waitForTimeout(1000)

  const emailData = await findLastEmail({
    request,
    timeout: Number(process.env.MAILCATCHER_TIMEOUT_MS ?? "60000"),
    filter: (email) => email.recipients.some(recipient => recipient.includes(`shard${getShardId()}`))
  })

  await page.goto(
    `${process.env.MAILCATCHER_HOST ?? "http://mailcatcher:1080"}/messages/${emailData.id}.html`,
  )

  const selector = 'a[href*="/reset-password?token="]'
  let url = await page.getAttribute(selector, "href")
  url = url!.replace("http://localhost/", "http://localhost:5173/")

  // Set a weak new password
  await page.goto(url)
  await page.getByPlaceholder("New Password").fill(weakPassword)
  await page.getByPlaceholder("Confirm Password").fill(weakPassword)
  await page.getByRole("button", { name: "Reset Password" }).click()

  await expect(
    page.getByText("Password must be at least 8 characters"),
  ).toBeVisible()
})
