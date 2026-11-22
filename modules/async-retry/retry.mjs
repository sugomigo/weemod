/**
 * Execute an async operation with bounded retry attempts.
 * Use only for idempotent operations or calls protected by an idempotency key.
 * No third-party dependencies.
 * @template T
 * @param {(context: {attempt: number, signal?: AbortSignal}) => Promise<T>} operation
 * @param {{maxAttempts?: number, initialDelayMs?: number, maxDelayMs?: number,
 *          multiplier?: number, shouldRetry?: (error: unknown, attempt: number) => boolean,
 *          onRetry?: (error: unknown, attempt: number, delayMs: number) => void,
 *          signal?: AbortSignal, sleep?: (delayMs: number, signal?: AbortSignal) => Promise<void>}} [options]
 * @returns {Promise<T>}
 */
export async function retryAsync(operation, options = {}) {
  if (typeof operation !== 'function') throw new TypeError('operation must be a function')
  const {
    maxAttempts = 3, initialDelayMs = 200, maxDelayMs = 2000,
    multiplier = 2, shouldRetry = () => true, onRetry,
    signal, sleep = abortableSleep,
  } = options
  if (!Number.isSafeInteger(maxAttempts) || maxAttempts < 1) throw new RangeError('maxAttempts must be >= 1')
  for (const [name, value, min] of [['initialDelayMs', initialDelayMs, 0], ['maxDelayMs', maxDelayMs, 0], ['multiplier', multiplier, 1]]) {
    if (!Number.isFinite(value) || value < min) throw new RangeError(`${name} must be finite and >= ${min}`)
  }
  if (typeof shouldRetry !== 'function' || typeof sleep !== 'function') throw new TypeError('shouldRetry and sleep must be functions')
  if (onRetry !== undefined && typeof onRetry !== 'function') throw new TypeError('onRetry must be a function')

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    throwIfAborted(signal)
    try {
      return await operation({ attempt, signal })
    } catch (error) {
      if (signal?.aborted) throwIfAborted(signal)
      if (attempt === maxAttempts || !shouldRetry(error, attempt)) throw error
      const delayMs = Math.min(maxDelayMs, initialDelayMs * multiplier ** (attempt - 1))
      if (onRetry) onRetry(error, attempt, delayMs)
      await sleep(delayMs, signal)
    }
  }
  throw new Error('Unreachable retry state')
}

function throwIfAborted(signal) {
  if (signal?.aborted) {
    const error = new Error('Operation aborted', { cause: signal.reason })
    error.name = 'AbortError'
    throw error
  }
}

function abortableSleep(ms, signal) {
  throwIfAborted(signal)
  if (ms === 0) return Promise.resolve()
  return new Promise((resolve, reject) => {
    let timeout
    function cleanup() {
      clearTimeout(timeout)
      signal?.removeEventListener('abort', onAbort)
    }
    function onAbort() {
      cleanup()
      const error = new Error('Operation aborted', { cause: signal?.reason })
      error.name = 'AbortError'
      reject(error)
    }
    timeout = setTimeout(() => { cleanup(); resolve() }, ms)
    signal?.addEventListener('abort', onAbort, { once: true })
    if (signal?.aborted) onAbort()
  })
}
