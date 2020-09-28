import { Counter, Rate } from 'k6/metrics';
import http from 'k6/http';

const defaults = {
  vus: 1,
  duration: '1s',
  headers: '{}',
};

const env = getEnvs();
const failures = new Rate('failures');
const completed = new Counter('completed');

export const options = {
  discardResponseBodies: true,
  vus: env.vus,
  duration: env.duration,
  thresholds: {
    completed: [
      {
        threshold: 'count>0',
      },
    ],
    failures: [
      {
        threshold: 'rate<=0',
        abortOnFail: true,
      },
    ],
  },
};

export default function () {
  completed.add(0);
  const r = doRequest(env);
  completed.add(1);
  failures.add(r.status !== env.status);
}

function getEnvs() {
  return {
    method: __ENV.CHAOS_K6_METHOD.toLowerCase(),
    url: __ENV.CHAOS_K6_URL,
    status: parseInt(__ENV.CHAOS_K6_STATUS, 10),
    body: __ENV.CHAOS_K6_BODY,
    vus: __ENV.CHAOS_K6_VUS || defaults.vus,
    duration: __ENV.CHAOS_K6_DURATION || defaults.duration,
    headers: JSON.parse(__ENV.CHAOS_K6_HEADERS || defaults.headers),
    timeout: parseInt(__ENV.CHAOS_K6_HTTP_TIMEOUT, 10),
  };
}

function doRequest(env) {
  if (env.method === 'get') {
    return http.get(env.url, {
      headers: env.headers,
      timeout: env.timeout * 1000,
    });
  }

  return (env.method === 'delete' ? http.delete : http[env.method])(
    env.url,
    env.body,
    { headers: env.headers, timeout: env.timeout * 1000 }
  );
}
