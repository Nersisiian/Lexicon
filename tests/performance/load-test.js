import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
    stages: [
        { duration: '30s', target: 5 },
        { duration: '1m', target: 15 },
        { duration: '30s', target: 0 },
    ],
    thresholds: {
        http_req_duration: ['p(95)<2000'],
        http_req_failed: ['rate<0.1'],
    },
};

export default function () {
    const payload = {
        file: http.file(open('/tmp/sample.pdf', 'b'), 'sample.pdf'),
    };
    const res = http.post('http://localhost:8000/api/v2/documents', payload);
    check(res, {
        'status is 200 or 429': (r) => r.status === 200 || r.status === 429,
    });
    sleep(1);
}
