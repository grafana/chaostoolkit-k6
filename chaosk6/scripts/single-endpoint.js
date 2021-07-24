import { Rate } from 'k6/metrics';
import http from 'k6/http';

const failures = new Rate('failures');

export const options = {
  thresholds: {
    failures: [{ threshold: 'rate<=0', abortOnFail: true }],
  },
};

export default function () {
  console.log(__ENV.CHAOS_K6_URL)
  const r = http.get(__ENV.CHAOS_K6_URL);
  console.log(`Status: ${r.status}`);
  failures.add(r.status !== 200);
}
