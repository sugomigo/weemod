# `async-retry`

A dependency-free, bounded retry helper for Node.js 18+ ES modules.

**Use when:** an asynchronous operation is idempotent (or secured with a deduplication key), may fail transiently, and can be retried safely.

**Do NOT use:** for unprotected payments, POSTs causing side effects, irreversible operations, unbounded API retries, or when a caller's framework already manages retries. A retry can increase load during outages; configure `shouldRetry`, attempt count and backoff to match the actual API's policy. `Retry-After` response handling is **not implemented**.

```js
import { retryAsync } from './retry.mjs'
const result = await retryAsync(
  async () => fetch('https://example.org/status').then(r => {
    if (!r.ok) throw new Error(`HTTP ${r.status}`)
    return r.text()
  }),
  { maxAttempts: 3, shouldRetry: err => err.message.startsWith('HTTP 5') }
)
```

This example is illustrative; adapt error handling and cancellation before production use. `retryAsync` provides `maxAttempts`, `initialDelayMs`, `maxDelayMs`, `multiplier`, `shouldRetry`, `onRetry`, and `AbortSignal`.

Test:

```bash
node --test modules/async-retry/retry.test.mjs
```

Status: **experimental**, not a production-tested networking SDK. MIT license draft pending repository's copyright holder verification.
