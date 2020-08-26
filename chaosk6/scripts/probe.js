import { Rate } from 'k6/metrics';
import http from 'k6/http';

const failures = new Rate('failures');

export const options = {
  discardResponseBodies: true,
  thresholds: {
    failures: [{ threshold: 'rate<=0', abortOnFail: true }],
  },
};

const env = getEnvs();

export default function () {
  const r = doRequest(env);
  console.log(JSON.stringify(r.headers));
  failures.add(r.status !== env.status);
}

function getEnvs() {
  return {
    method: __ENV.CHAOS_K6_METHOD.toLowerCase(),
    url: __ENV.CHAOS_K6_URL,
    status: parseInt(__ENV.CHAOS_K6_STATUS, 10),
    body: __ENV.CHAOS_K6_BODY,
    headers: JSON.parse(__ENV.CHAOS_K6_HEADERS || '{}'),
  };
}

function doRequest(env) {
  if (env.method === 'get') {
    return http.get(env.url, { headers: { data: 'pata' } });
  }

  return (env.method === 'delete' ? http.delete : http[env.method])(
    env.url,
    env.body,
    { headers: env.headers }
  );
}
