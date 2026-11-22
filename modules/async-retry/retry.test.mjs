import test from 'node:test'
import assert from 'node:assert/strict'
import { retryAsync } from './retry.mjs'

test('returns on first success', async () => {
  const attempts = []
  const value = await retryAsync(async ({ attempt }) => { attempts.push(attempt); return 42 })
  assert.equal(value, 42)
  assert.deepEqual(attempts, [1])
})

test('retries then succeeds, bounded backoff and hooks', async () => {
  const attempts = []; const delays = []; const hooks = []
  const result = await retryAsync(async ({ attempt }) => {
    attempts.push(attempt)
    if (attempt < 3) throw Error('transient')
    return 'ok'
  }, { initialDelayMs: 100, maxDelayMs: 150, sleep: async ms => { delays.push(ms) }, onRetry: (_, n, ms) => hooks.push([n, ms]) })
  assert.equal(result, 'ok')
  assert.deepEqual(attempts, [1, 2, 3])
  assert.deepEqual(delays, [100, 150])
  assert.deepEqual(hooks, [[1, 100], [2, 150]])
})

test('stops at maximum attempts', async () => {
  let calls = 0
  await assert.rejects(retryAsync(async () => { calls++; throw Error('down') }, { maxAttempts: 2, initialDelayMs: 0 }), /down/)
  assert.equal(calls, 2)
})

test('does not retry when shouldRetry returns false', async () => {
  let calls = 0
  await assert.rejects(retryAsync(async () => { calls++; throw Error('fatal') }, { shouldRetry: () => false }), /fatal/)
  assert.equal(calls, 1)
})

test('aborted signal prevents any attempt', async () => {
  const ac = new AbortController(); ac.abort()
  let calls = 0
  await assert.rejects(retryAsync(async () => { calls++ }, { signal: ac.signal }), { name: 'AbortError' })
  assert.equal(calls, 0)
})

test('abort interrupts the delay', async () => {
  const ac = new AbortController()
  let calls = 0
  const pending = retryAsync(async () => { calls++; throw Error('transient') }, { signal: ac.signal, initialDelayMs: 500 })
  setTimeout(() => ac.abort(), 10)
  await assert.rejects(pending, { name: 'AbortError' })
  assert.equal(calls, 1)
})

test('validates options', async () => {
  await assert.rejects(retryAsync(async () => 1, { maxAttempts: 0 }), /maxAttempts/)
  await assert.rejects(retryAsync(async () => 1, { multiplier: 0 }), /multiplier/)
})
